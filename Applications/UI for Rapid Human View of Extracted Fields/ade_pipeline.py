"""ADE v2 parse + extract orchestration.

v2 only. Every call goes through `client.v2.*`; nothing here touches the v1
Parse/Extract/Section/Split endpoints or the dpt-2 model family.

Both stages run as async jobs at the `standard` service tier, which costs half
the credits of `priority` in exchange for slower turnaround -- the right trade
for batch review work.
"""

from __future__ import annotations

import json
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from grounding import resolve_regions
from paths import FolderPaths, resolve_folder, resolve_schema

PARSE_MODEL = "dpt-3-pro-latest"
SERVICE_TIER = "standard"
JOB_TIMEOUT_SECONDS = 900
MAX_WORKERS = 4

load_dotenv(Path(__file__).resolve().parent / ".env")


def make_client():
    """Construct the SDK client. Imported lazily so the app can start and serve
    the UI even when no API key is configured yet."""
    from landingai_ade import LandingAIADE

    return LandingAIADE()


def _dump(obj: Any) -> Any:
    """SDK pydantic model -> plain JSON-safe dict."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if isinstance(obj, dict):
        return obj
    raise TypeError(f"cannot serialize {type(obj)!r}")


def _valid_json(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return False


@dataclass
class RunState:
    """Progress for the current (or last) batch run. Single-user local app, so
    one module-level instance guarded by a lock is sufficient."""

    running: bool = False
    folder: str = ""
    schema: str = ""
    total: int = 0
    parsed: int = 0
    extracted: int = 0
    skipped: int = 0
    failures: list[dict] = field(default_factory=list)
    started_at: str | None = None
    finished_at: str | None = None
    message: str = ""

    def snapshot(self) -> dict:
        return {
            "running": self.running,
            "folder": self.folder,
            "schema": self.schema,
            "total": self.total,
            "parsed": self.parsed,
            "extracted": self.extracted,
            "skipped": self.skipped,
            "failures": list(self.failures),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "message": self.message,
        }


RUN_LOCK = threading.Lock()
RUN_STATE = RunState()


def _bump(attr: str, amount: int = 1) -> None:
    with RUN_LOCK:
        setattr(RUN_STATE, attr, getattr(RUN_STATE, attr) + amount)


def _fail(document: str, stage: str, error: str) -> None:
    with RUN_LOCK:
        RUN_STATE.failures.append({"document": document, "stage": stage, "error": error})


def parse_document(client, doc_path: Path, dirs: FolderPaths) -> dict:
    """Parse one document as an async job and persist markdown + full response."""
    job = client.v2.parse_jobs.create(
        document=doc_path,
        model=PARSE_MODEL,
        service_tier=SERVICE_TIER,
    )
    done = client.v2.parse_jobs.wait(
        job.job_id, timeout=JOB_TIMEOUT_SECONDS, raise_on_failure=True
    )
    parse = _dump(done.result)

    stem = doc_path.stem
    dirs.parse_json(stem).write_text(
        json.dumps(parse, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    # The trailing `<!-- doc_id=... -->` line must survive: v2 Extract reads it
    # to link the extraction back to this parse job.
    dirs.markdown(stem).write_text(parse.get("markdown") or "", encoding="utf-8")
    return parse


def extract_document(client, stem: str, schema: dict, dirs: FolderPaths) -> dict:
    """Extract one document's fields as an async job and persist the response."""
    markdown = dirs.markdown(stem).read_text(encoding="utf-8")
    job = client.v2.extract_jobs.create(
        markdown=markdown,
        schema=schema,
        service_tier=SERVICE_TIER,
    )
    done = client.v2.extract_jobs.wait(
        job.job_id, timeout=JOB_TIMEOUT_SECONDS, raise_on_failure=True
    )
    extract = _dump(done.result)
    dirs.extract_json(stem).write_text(
        json.dumps(extract, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return extract


def cache_regions(dirs: FolderPaths, stem: str, parse: dict, extract: dict) -> dict:
    """Precompute the field path -> highlight regions map so click-to-highlight
    never waits on anything."""
    resolved = resolve_regions(parse, extract)
    dirs.regions_json(stem).write_text(
        json.dumps(resolved, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return resolved


def process_document(client, doc_path: Path, schema: dict, dirs: FolderPaths, force: bool) -> None:
    stem = doc_path.stem
    have_parse = _valid_json(dirs.parse_json(stem)) and dirs.markdown(stem).is_file()
    have_extract = _valid_json(dirs.extract_json(stem))

    if have_parse and have_extract and not force:
        # Skipped files still count as complete so the bars reach 100%.
        _bump("skipped")
        _bump("parsed")
        _bump("extracted")
        if not _valid_json(dirs.regions_json(stem)):
            try:
                parse = json.loads(dirs.parse_json(stem).read_text(encoding="utf-8"))
                extract = json.loads(dirs.extract_json(stem).read_text(encoding="utf-8"))
                cache_regions(dirs, stem, parse, extract)
            except Exception as exc:  # noqa: BLE001 - cache rebuild is best-effort
                _fail(doc_path.name, "regions", str(exc))
        return

    try:
        if have_parse and not force:
            parse = json.loads(dirs.parse_json(stem).read_text(encoding="utf-8"))
        else:
            parse = parse_document(client, doc_path, dirs)
        _bump("parsed")
    except Exception as exc:  # noqa: BLE001 - one bad document must not stop the batch
        _fail(doc_path.name, "parse", f"{type(exc).__name__}: {exc}")
        return

    try:
        extract = extract_document(client, stem, schema, dirs)
        _bump("extracted")
    except Exception as exc:  # noqa: BLE001
        _fail(doc_path.name, "extract", f"{type(exc).__name__}: {exc}")
        return

    try:
        cache_regions(dirs, stem, parse, extract)
    except Exception as exc:  # noqa: BLE001
        _fail(doc_path.name, "regions", f"{type(exc).__name__}: {exc}")


def run_batch(folder: str, schema_name: str, force: bool) -> None:
    """Blocking batch run. Call on a background thread."""
    dirs = resolve_folder(folder)
    dirs.ensure()
    schema_path = resolve_schema(schema_name)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    documents = dirs.documents_list()

    with RUN_LOCK:
        RUN_STATE.running = True
        RUN_STATE.folder = folder
        RUN_STATE.schema = schema_name
        RUN_STATE.total = len(documents)
        RUN_STATE.parsed = 0
        RUN_STATE.extracted = 0
        RUN_STATE.skipped = 0
        RUN_STATE.failures = []
        RUN_STATE.finished_at = None
        RUN_STATE.message = ""
        from datetime import datetime, timezone

        RUN_STATE.started_at = datetime.now(timezone.utc).isoformat()

    try:
        if not documents:
            with RUN_LOCK:
                RUN_STATE.message = "No documents found in the documents/ folder."
            return
        client = make_client()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            list(
                pool.map(
                    lambda p: process_document(client, p, schema, dirs, force),
                    documents,
                )
            )
    except Exception as exc:  # noqa: BLE001 - surface setup failures in the UI
        with RUN_LOCK:
            RUN_STATE.message = f"{type(exc).__name__}: {exc}"
        traceback.print_exc()
    finally:
        from datetime import datetime, timezone

        with RUN_LOCK:
            RUN_STATE.running = False
            RUN_STATE.finished_at = datetime.now(timezone.utc).isoformat()


def start_batch(folder: str, schema_name: str, force: bool) -> bool:
    """Kick off a run on a background thread. False if one is already going."""
    with RUN_LOCK:
        if RUN_STATE.running:
            return False
    thread = threading.Thread(
        target=run_batch, args=(folder, schema_name, force), daemon=True
    )
    thread.start()
    return True
