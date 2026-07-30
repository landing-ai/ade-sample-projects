"""FastAPI backend for the ADE human-in-the-loop review UI.

Single-user local app: no auth, no database, run state lives in the process.

    uvicorn app:app --reload --port 8000
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import ade_pipeline
import hil_output
from fields import flatten_schema
from grounding import resolve_regions
from paths import (
    APP_ROOT,
    FolderPaths,
    list_input_folders,
    list_schemas,
    resolve_folder,
    resolve_schema,
)

STATIC_DIR = APP_ROOT / "static"
RENDER_SCALE = 2.0  # PyMuPDF matrix scale; 2x keeps small print legible

app = FastAPI(title="ADE Human Review", docs_url=None, redoc_url=None)


# ----------------------------------------------------------------- helpers


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def _schema_and_extract(dirs: FolderPaths, schema_name: str, stem: str) -> tuple[dict, dict | None]:
    schema_path = resolve_schema(schema_name)
    if not schema_path.is_file():
        raise HTTPException(404, f"Schema not found: {schema_name}")
    schema = _load_json(schema_path)
    if schema is None:
        raise HTTPException(400, f"Schema is not valid JSON: {schema_name}")
    return schema, _load_json(dirs.extract_json(stem))


def _regions_for(dirs: FolderPaths, stem: str) -> dict:
    """Cached regions map, rebuilt from parse+extract on a cache miss."""
    cached = _load_json(dirs.regions_json(stem))
    if cached and "regions" in cached:
        return cached
    parse = _load_json(dirs.parse_json(stem))
    extract = _load_json(dirs.extract_json(stem))
    if not parse or not extract:
        return {"paired": False, "page_count": 1, "regions": {}, "pages": {}}
    resolved = resolve_regions(parse, extract)
    try:
        dirs.regions_json(stem).write_text(
            json.dumps(resolved, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    except OSError:
        pass
    return resolved


# ----------------------------------------------------------------- routes


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/folders")
def api_folders() -> dict:
    return {"folders": list_input_folders()}


@app.get("/api/schemas")
def api_schemas() -> dict:
    return {"schemas": list_schemas()}


class RunRequest(BaseModel):
    folder: str
    schema_name: str
    force: bool = False


@app.post("/api/run")
def api_run(req: RunRequest) -> dict:
    dirs = resolve_folder(req.folder)
    if not dirs.documents.is_dir():
        raise HTTPException(400, f"No documents/ folder under {dirs.root}")
    if not resolve_schema(req.schema_name).is_file():
        raise HTTPException(404, f"Schema not found: {req.schema_name}")
    started = ade_pipeline.start_batch(req.folder, req.schema_name, req.force)
    if not started:
        raise HTTPException(409, "A run is already in progress")
    return {"started": True}


@app.get("/api/progress")
def api_progress() -> dict:
    with ade_pipeline.RUN_LOCK:
        return ade_pipeline.RUN_STATE.snapshot()


@app.get("/api/files")
def api_files(folder: str) -> dict:
    dirs = resolve_folder(folder)
    out = []
    for doc in dirs.documents_list():
        stem = doc.stem
        hil = _load_json(dirs.hil_json(stem))
        out.append(
            {
                "name": doc.name,
                "stem": stem,
                "has_parse": dirs.parse_json(stem).is_file(),
                "has_extract": dirs.extract_json(stem).is_file(),
                "submitted": hil is not None,
                "override_count": (hil or {}).get("override_count", 0),
            }
        )
    return {"folder": str(dirs.root), "files": out}


@app.get("/api/doc")
def api_doc(folder: str, stem: str, schema_name: str) -> dict:
    dirs = resolve_folder(folder)
    schema, extract = _schema_and_extract(dirs, schema_name, stem)
    if extract is None:
        raise HTTPException(404, f"No extraction results for {stem}. Run Parse+Extract first.")

    extraction = extract.get("extraction") or {}
    rows = flatten_schema(schema, extraction)
    resolved = _regions_for(dirs, stem)
    regions = resolved.get("regions") or {}

    # Reload any previously submitted overrides so review work is resumable.
    hil = _load_json(dirs.hil_json(stem)) or {}
    saved_overrides = {
        ov["path"]: ov["final_value"] for ov in (hil.get("overrides") or []) if "path" in ov
    }

    for row in rows:
        row["regions"] = regions.get(row["path"], [])

    parse_meta = (_load_json(dirs.parse_json(stem)) or {}).get("metadata") or {}

    return {
        "stem": stem,
        "document": next(
            (d.name for d in dirs.documents_list() if d.stem == stem), f"{stem}.pdf"
        ),
        "page_count": resolved.get("page_count", 1),
        "paired": resolved.get("paired", False),
        "failed_pages": parse_meta.get("failed_pages") or [],
        "warnings": extract.get("warnings") or [],
        "schema_violation_error": extract.get("schema_violation_error"),
        "fields": rows,
        "saved_overrides": saved_overrides,
        "submitted": bool(hil),
    }


@app.get("/api/page-image")
def api_page_image(folder: str, stem: str, page: int) -> FileResponse:
    """Render (and cache) one page as PNG.

    ADE `grounding.page` is 1-indexed; PyMuPDF pages are 0-indexed. The
    conversion happens here and nowhere else.
    """
    if page < 1:
        raise HTTPException(400, "page is 1-indexed")

    dirs = resolve_folder(folder)
    cached = dirs.page_images / f"{stem}_p{page}.png"
    if cached.is_file():
        return FileResponse(cached, media_type="image/png")

    source = next((d for d in dirs.documents_list() if d.stem == stem), None)
    if source is None:
        raise HTTPException(404, f"Document not found for stem {stem}")

    dirs.page_images.mkdir(parents=True, exist_ok=True)

    if source.suffix.lower() != ".pdf":
        # Single-page image document: serve it directly.
        if page != 1:
            raise HTTPException(404, "Image documents have a single page")
        return FileResponse(source)

    import pymupdf

    with pymupdf.open(source) as doc:
        if page > len(doc):
            raise HTTPException(404, f"{stem} has {len(doc)} pages")
        pix = doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(RENDER_SCALE, RENDER_SCALE))
        pix.save(cached)

    return FileResponse(cached, media_type="image/png")


class SubmitFileRequest(BaseModel):
    folder: str
    schema_name: str
    stem: str
    overrides: dict[str, Any] = {}


def _build_result(dirs: FolderPaths, schema_name: str, stem: str, overrides: dict, opened: bool) -> dict:
    schema, extract = _schema_and_extract(dirs, schema_name, stem)
    if extract is None:
        raise HTTPException(404, f"No extraction results for {stem}")
    extraction = extract.get("extraction") or {}
    rows = flatten_schema(schema, extraction)
    resolved = _regions_for(dirs, stem)
    parse_meta = (_load_json(dirs.parse_json(stem)) or {}).get("metadata") or {}
    extract_meta = extract.get("metadata") or {}
    document = next((d.name for d in dirs.documents_list() if d.stem == stem), f"{stem}.pdf")

    return hil_output.build_file_result(
        document=document,
        schema_name=schema_name,
        extraction=extraction,
        field_rows=rows,
        overrides=overrides,
        regions=resolved.get("regions") or {},
        parse_job_id=parse_meta.get("job_id"),
        extract_job_id=extract_meta.get("job_id"),
        doc_id=extract_meta.get("doc_id"),
        opened=opened,
    )


@app.post("/api/submit-file")
def api_submit_file(req: SubmitFileRequest) -> dict:
    dirs = resolve_folder(req.folder)
    result = _build_result(dirs, req.schema_name, req.stem, req.overrides, opened=True)
    hil_output.write_file_result(dirs.hil_json(req.stem), result)
    return {
        "written": str(dirs.hil_json(req.stem)),
        "override_count": result["override_count"],
    }


class SubmitBatchRequest(BaseModel):
    folder: str
    schema_name: str
    # path -> value, per document stem, for whatever the reviewer has in progress
    overrides_by_stem: dict[str, dict[str, Any]] = {}
    opened_stems: list[str] = []


@app.post("/api/submit-batch")
def api_submit_batch(req: SubmitBatchRequest) -> dict:
    """Write HIL output for every document, then the batch report.

    Files the reviewer never opened still get a record, marked
    opened_by_reviewer=false, so a partial batch is never mistaken for a
    complete one.
    """
    dirs = resolve_folder(req.folder)
    opened = set(req.opened_stems)
    results: list[dict] = []
    skipped: list[dict] = []

    for doc in dirs.documents_list():
        stem = doc.stem
        if not dirs.extract_json(stem).is_file():
            skipped.append({"document": doc.name, "reason": "no extraction results"})
            continue
        overrides = req.overrides_by_stem.get(stem)
        if overrides is None:
            # Fall back to whatever was already submitted for this file.
            prior = _load_json(dirs.hil_json(stem)) or {}
            overrides = {
                ov["path"]: ov["final_value"] for ov in (prior.get("overrides") or []) if "path" in ov
            }
        result = _build_result(
            dirs, req.schema_name, stem, overrides, opened=stem in opened or bool(overrides)
        )
        hil_output.write_file_result(dirs.hil_json(stem), result)
        results.append(result)

    report = hil_output.build_batch_report(
        folder=str(dirs.root), schema_name=req.schema_name, results=results
    )
    written = hil_output.write_batch_report(dirs.hil_results, report)

    return {
        "documents_written": len(results),
        "skipped": skipped,
        "report": written,
        "summary": report["summary"],
    }


class ResetRequest(BaseModel):
    folder: str


# Only these may ever be deleted. The folder itself and documents/ are never
# touched -- important because some folders keep their PDFs at the root, and
# because `folder` can be an arbitrary path typed into the UI.
RESETTABLE_SUBDIRS = (
    "parse_results",
    "extract_results",
    "regions",
    "page_images",
    "HIL_results",
)


@app.post("/api/reset")
def api_reset(req: ResetRequest) -> dict:
    """Delete generated results for one folder. Source documents are preserved."""
    import shutil

    dirs = resolve_folder(req.folder)
    if not dirs.root.is_dir():
        raise HTTPException(400, f"Not a folder: {dirs.root}")

    documents = dirs.documents.resolve()
    removed: list[str] = []

    for name in RESETTABLE_SUBDIRS:
        target = (dirs.root / name).resolve()
        # Belt-and-braces: never step outside the folder, and never delete the
        # directory that holds the source documents.
        if target.parent != dirs.root.resolve():
            continue
        if target == documents or target == dirs.root.resolve():
            continue
        if target.is_dir():
            file_count = sum(1 for p in target.rglob("*") if p.is_file())
            shutil.rmtree(target)
            removed.append(f"{name} ({file_count} files)")

    dirs.ensure()
    return {"removed": removed, "documents_kept": len(dirs.documents_list())}


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
