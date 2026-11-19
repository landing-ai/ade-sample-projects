"""Where a document type's ADE output lives, and which model snapshots produce it.

Every run is filed under the exact snapshots that produced it:

    collection/<slug>/runs/<parse snapshot>/parse.json
                                           parse.md
                                           <extract snapshot>/extract.json
                                                              grounding.json
                                                              images/

The extraction sits inside the parse it came from, because an extraction only means
anything against the markdown that produced it. A folder can hold several runs side by
side: DPT-3 Pro and DPT-3 Verity, or one parse extracted by two extract snapshots.

Snapshots are always pinned. A `-latest` alias moves without warning: when this
collection used `extract-latest`, its extractions ended up split across two snapshots
with nothing in the file names to say so.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COLLECTION = REPO_ROOT / "document-types" / "collection"

# The snapshots new runs use. Change these deliberately, never to an alias.
PARSE_MODELS = {
    "pro": "dpt-3-pro-20261111",
    "verity": "dpt-3-verity-20261111",
}
EXTRACT_MODEL = "extract-20261111"


def parse_snapshot(name: str) -> str:
    """A family name (pro, verity) or an exact snapshot, as the snapshot to request."""
    if name in PARSE_MODELS:
        return PARSE_MODELS[name]
    if name.endswith("-latest") or name in {"dpt-3-pro", "dpt-3-verity"}:
        sys.exit(f"{name} is an alias. Pin a dated snapshot, e.g. {PARSE_MODELS['pro']}.")
    if not name.startswith("dpt-3-"):
        sys.exit(f"Unknown parse model {name!r}. Use {', '.join(PARSE_MODELS)} or a "
                 "dated dpt-3 snapshot.")
    return name


def extract_snapshot(name: str) -> str:
    if name in {"extract", "extract-latest"}:
        sys.exit(f"{name} is an alias. Pin a dated snapshot, e.g. {EXTRACT_MODEL}.")
    if not name.startswith("extract-"):
        sys.exit(f"Unknown extract model {name!r}.")
    return name


def family(parse_model: str) -> str:
    """dpt-3-verity-20261111 -> verity"""
    parts = parse_model.split("-")
    return parts[2] if len(parts) > 2 else parse_model


@dataclass(frozen=True)
class Run:
    folder: Path
    parse_model: str
    extract_model: str

    @property
    def parse_dir(self) -> Path:
        return self.folder / "runs" / self.parse_model

    @property
    def dir(self) -> Path:
        return self.parse_dir / self.extract_model

    @property
    def parse_json(self) -> Path:
        return self.parse_dir / "parse.json"

    @property
    def parse_md(self) -> Path:
        return self.parse_dir / "parse.md"

    @property
    def extract_json(self) -> Path:
        return self.dir / "extract.json"

    @property
    def grounding_json(self) -> Path:
        return self.dir / "grounding.json"

    @property
    def images_dir(self) -> Path:
        return self.dir / "images"

    @property
    def label(self) -> str:
        return f"{self.parse_model}/{self.extract_model}"

    def rel(self, path: Path) -> str:
        return str(path.relative_to(self.folder))


def runs_in(folder: Path) -> list[Run]:
    """Every completed run in a folder: a parse directory with an extraction in it."""
    found = []
    for parse_dir in sorted((folder / "runs").glob("*/")):
        for extract_dir in sorted(parse_dir.glob("*/")):
            if (extract_dir / "extract.json").is_file():
                found.append(Run(folder, parse_dir.name, extract_dir.name))
    return found


def matches_parse(run: Run, wanted: str) -> bool:
    return run.parse_model == wanted or family(run.parse_model) == wanted


def select_run(folder: Path, parse: str | None = None, extract: str | None = None) -> Run:
    """The one run that --parse / --extract pick out. Either may be a family name
    (pro, verity), an exact snapshot, or omitted. Stops when the choice is ambiguous."""
    all_runs = runs_in(folder)
    chosen = [r for r in all_runs
              if (parse is None or matches_parse(r, parse))
              and (extract is None or r.extract_model == extract)]
    if len(chosen) == 1:
        return chosen[0]
    listing = "\n".join(f"    {r.label}" for r in all_runs) or "    (none)"
    if not chosen:
        sys.exit(f"No run in {folder.name} matches --parse {parse} --extract {extract}. "
                 f"Runs present:\n{listing}")
    sys.exit(f"{folder.name} has several runs; pick one with --parse and --extract:\n{listing}")


def is_current(run: Run) -> bool:
    """Made with the snapshots new runs use. Older runs stay in the folder as a record,
    but the manifest's featured fields are chosen for, and checked against, these."""
    return (run.parse_model in PARSE_MODELS.values()
            and run.extract_model == EXTRACT_MODEL)


def occurrence_for(spec: dict, run: Run) -> int:
    """Which of a field's ranges to box. "occurrence" is a number, or, when two parse
    models report a value's appearances in a different order, a map from parse model
    (family or exact snapshot) to number: {"pro": 0, "verity": 1}."""
    occ = spec.get("occurrence", 0)
    if isinstance(occ, dict):
        occ = occ.get(run.parse_model, occ.get(family(run.parse_model), 0))
    return int(occ)


def add_run_args(parser) -> None:
    parser.add_argument("--parse", metavar="MODEL",
                        help="parse model of the run: pro, verity, or an exact snapshot")
    parser.add_argument("--extract", metavar="MODEL",
                        help="extract snapshot of the run, e.g. extract-20261111")


def run_entry(run: Run) -> dict:
    """The manifest's record of a run, read from the responses themselves."""
    def meta(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")).get("metadata") or {}
    parse_meta, extract_meta = meta(run.parse_json), meta(run.extract_json)
    return {
        "parse_model": run.parse_model,
        "extract_model": run.extract_model,
        "path": run.rel(run.dir),
        "pages": parse_meta.get("page_count"),
        "service_tier": (parse_meta.get("billing") or {}).get("service_tier"),
        "parse_credits": (parse_meta.get("billing") or {}).get("total_credits"),
        "extract_credits": (extract_meta.get("billing") or {}).get("total_credits"),
    }


def record_run(run: Run) -> bool:
    """Add or refresh the run's entry under "runs" in manifest.json, which is what the
    website compares runs by. Returns False when there is no manifest yet."""
    manifest_path = run.folder / "manifest.json"
    if not manifest_path.is_file():
        return False
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = run_entry(run)
    others = [r for r in manifest.get("runs", [])
              if (r.get("parse_model"), r.get("extract_model"))
              != (run.parse_model, run.extract_model)]
    runs = sorted(others + [entry], key=lambda r: (r["parse_model"], r["extract_model"]))
    if manifest.get("runs") != runs:
        manifest["runs"] = runs
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
    return True
