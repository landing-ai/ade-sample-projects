"""
extract.py  —  Batch-extract structured fields using the LandingAI ADE Extract API.

Reads:
  schemas/current.json                              (active extraction schema)
  data/pipeline_outputs/parsed/<stem>_markdown.md  (one per PDF)

Saves:
  data/pipeline_outputs/extracted/<stem>_extract_response.json  (full API response)
  data/pipeline_outputs/extracted/<stem>_extracted.json         (extracted fields only)

Timing: prints per-file duration and a final summary.

Usage:
  python scripts/extract.py
  python scripts/extract.py --workers 2
  python scripts/extract.py --force      # archive prior outputs, then re-run all files
"""

import argparse
import json
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["VISION_AGENT_API_KEY"]
EXTRACT_URL = "https://api.va.landing.ai/v1/ade/extract"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

PARSED_DIR = Path("data/pipeline_outputs/parsed")
OUT_DIR = Path("data/pipeline_outputs/extracted")
HISTORY_DIR = OUT_DIR / "history"
SCHEMA_PATH = Path("schemas/current.json")
DEFAULT_WORKERS = 6


def archive_existing_outputs() -> str | None:
    """Move all existing extracted files into a timestamped history subfolder.
    Returns the archive path if anything was moved, else None."""
    existing = [
        p for p in OUT_DIR.glob("*.json")
        if p.is_file()
    ]
    if not existing:
        return None

    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    archive_dir = HISTORY_DIR / run_id
    archive_dir.mkdir(parents=True, exist_ok=True)

    for f in existing:
        shutil.move(str(f), archive_dir / f.name)

    return str(archive_dir)


def extract_one(md_path: Path, schema_str: str) -> dict:
    """Extract structured data from one markdown file. Returns a result dict with timing."""
    stem = md_path.stem.replace("_markdown", "")
    t_start = time.perf_counter()

    with open(md_path, "rb") as f:
        response = requests.post(
            EXTRACT_URL,
            headers=HEADERS,
            files={
                "markdown": (md_path.name, f, "text/plain"),
                "schema":   (None, schema_str),
            },
        )

    elapsed = time.perf_counter() - t_start

    # 200 = full success; 206 = Partial Content (extraction succeeded but the schema
    # contained unsupported keywords that were ignored — data is still usable).
    if response.status_code not in (200, 206):
        return {
            "file": md_path.name,
            "status": "error",
            "elapsed_s": elapsed,
            "error": f"HTTP {response.status_code}: {response.text[:300]}",
        }

    data = response.json()

    # Save full API response
    (OUT_DIR / f"{stem}_extract_response.json").write_text(json.dumps(data, indent=2))

    # Save extracted fields only — this is what evaluate.py reads
    extraction = data.get("extraction", {})
    (OUT_DIR / f"{stem}_extracted.json").write_text(json.dumps(extraction, indent=2))

    notes = []
    if data.get("metadata", {}).get("schema_violation_error"):
        notes.append(f"schema_violation: {data['metadata']['schema_violation_error']}")
    if data.get("metadata", {}).get("fallback_model_version"):
        notes.append(f"fallback_model: {data['metadata']['fallback_model_version']}")

    return {"file": md_path.name, "status": "ok", "elapsed_s": elapsed, "notes": notes}


def main():
    parser = argparse.ArgumentParser(description="Batch-extract using LandingAI ADE.")
    parser.add_argument(
        "--workers", type=int, default=DEFAULT_WORKERS,
        help=f"Parallel workers (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-run files that already have extracted output",
    )
    args = parser.parse_args()

    if not SCHEMA_PATH.exists():
        print(f"No schema at {SCHEMA_PATH}. Run build_schema.py first.")
        return

    # Load schema and strip the internal _meta block before sending.
    # _meta is added by the Build Schema API (model version, prompt history, etc.)
    # and is not a valid JSON Schema keyword — sending it to Extract causes an error.
    schema_obj = json.loads(SCHEMA_PATH.read_text())
    schema_obj.pop("_meta", None)
    schema_str = json.dumps(schema_obj)
    fields = list(schema_obj.get("properties", {}).keys())
    print(f"Schema: {len(fields)} field(s) — {fields}\n")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md_files = sorted(PARSED_DIR.glob("*_markdown.md"))

    if not md_files:
        print(f"No markdown files found in {PARSED_DIR}/. Run parse.py first.")
        return

    # Archive prior outputs before this run
    if not args.force:
        pending = [
            p for p in md_files
            if not (OUT_DIR / f"{p.stem.replace('_markdown', '')}_extracted.json").exists()
        ]
        skipped = len(md_files) - len(pending)
        if skipped:
            print(f"Skipping {skipped} already-extracted file(s). Use --force to re-run.\n")
        md_files = pending
    else:
        archive_path = archive_existing_outputs()
        if archive_path:
            print(f"Archived prior outputs to: {archive_path}\n")

    if not md_files:
        print("Nothing to do.")
        return

    print(f"Extracting {len(md_files)} file(s) with {args.workers} worker(s)...\n")
    wall_start = time.perf_counter()
    results = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(extract_one, p, schema_str): p for p in md_files}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            notes_str = f"  [{', '.join(result.get('notes', []))}]" if result.get("notes") else ""
            if result["status"] == "ok":
                print(f"  OK  {result['file']:<40}  {result['elapsed_s']:>5.1f}s{notes_str}")
            else:
                print(f"  ERR {result['file']:<40}  {result['error']}")

    wall_elapsed = time.perf_counter() - wall_start
    ok = sum(1 for r in results if r["status"] == "ok")
    errors = [r for r in results if r["status"] == "error"]

    print(f"\n{'─' * 65}")
    print(f"  {ok}/{len(results)} succeeded  |  wall time: {wall_elapsed:.1f}s  |  avg: {wall_elapsed/len(results):.1f}s/file")
    if errors:
        print(f"\n  Failed files:")
        for e in errors:
            print(f"    {e['file']}: {e['error']}")
    print(f"\n  Outputs saved to: {OUT_DIR}/\n")


if __name__ == "__main__":
    main()
