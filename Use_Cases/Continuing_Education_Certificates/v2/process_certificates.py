"""
CME certificate processing pipeline using the LandingAI ADE **v2** (DPT-3) async APIs.

Steps:
  1. Submit every file in input_folder to Parse Jobs v2 (standard service_tier).
  2. Save each parse result as <name>_parse.json and its Markdown as <name>_parse.md
     under results_folder/parse/.
  3. Load the extraction schema from schema/cme_demo_schema.json.
  4. Submit each parsed document's Markdown + schema to Extract Jobs v2
     (standard service_tier).
  5. Save each extract result as <name>_extract.json under results_folder/extract/.
  6. Write a CSV of all extracted fields (one row per document), plus job_id,
     document name, and processing date.
  7. Write a CSV of parse + extract metadata (one row per document).

Only v2 endpoints are used. Run from anywhere:

    python process_certificates.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd

import ade_v2_client as ade

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
INPUT_FOLDER = HERE.parent / "input_folder"          # Continuing_Education_Certificates/input_folder
SCHEMA_PATH = HERE / "schema" / "cme_demo_schema.json"
RESULTS_FOLDER = HERE / "results_folder"

PARSE_DIR = RESULTS_FOLDER / "parse"
EXTRACT_DIR = RESULTS_FOLDER / "extract"
CSV_DIR = RESULTS_FOLDER / "csv_summaries"

ENV_PATH = HERE.parent / ".env"                      # Continuing_Education_Certificates/.env

SERVICE_TIER = "standard"
SUPPORTED_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------

def load_env(env_path: Path = ENV_PATH) -> None:
    """
    Populate os.environ from a simple KEY=VALUE .env file, without overwriting
    variables already set in the environment. Lightweight so no extra dependency
    is required (python-dotenv would work too).
    """
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def flatten(obj: Any, prefix: str = "", sep: str = ".") -> dict[str, Any]:
    """Flatten a nested dict into dot-notation columns. Lists are left as-is."""
    flat: dict[str, Any] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{prefix}{sep}{key}" if prefix else key
            if isinstance(value, dict):
                flat.update(flatten(value, new_key, sep))
            else:
                flat[new_key] = value
    else:
        flat[prefix] = obj
    return flat


def discover_documents(folder: Path) -> list[Path]:
    """Return supported document files in folder, sorted by natural order."""
    docs = [p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED_SUFFIXES]

    def sort_key(p: Path) -> tuple[str, int]:
        # keep numbered files (e.g. ..._ex1, ..._ex2, ..._ex10) in numeric order
        stem = p.stem
        digits = "".join(ch for ch in stem if ch.isdigit())
        return (stem.rsplit("_", 1)[0] if "_" in stem else stem, int(digits) if digits else 0)

    return sorted(docs, key=sort_key)


# ---------------------------------------------------------------------------
# Pipeline stages
# ---------------------------------------------------------------------------

def run_parse_stage(documents: list[Path], api_key: str) -> dict[str, dict[str, Any]]:
    """
    Steps 1-2: submit all parse jobs, poll to completion, and save JSON + Markdown.

    Returns a mapping: document stem -> {"job_id", "markdown", "metadata"}.
    """
    print(f"\n=== Parse stage: submitting {len(documents)} document(s) ===")
    PARSE_DIR.mkdir(parents=True, exist_ok=True)

    # Submit every job first so the server processes them in parallel.
    submitted: dict[str, str] = {}  # stem -> job_id
    for doc in documents:
        job_id = ade.create_parse_job(doc, api_key, service_tier=SERVICE_TIER)
        submitted[doc.stem] = job_id
        print(f"  submitted {doc.name:<20} -> {job_id}")

    # Poll each to completion and persist results.
    parsed: dict[str, dict[str, Any]] = {}
    for stem, job_id in submitted.items():
        job = ade.poll_job(ade.get_parse_job, job_id, api_key)
        if job.get("status") != "completed":
            err = job.get("error") or {}
            print(f"  !! parse FAILED for {stem}: {err.get('code')}: {err.get('message')}")
            continue

        result = job["result"]  # full Parse v2 response: markdown, structure, metadata
        _write_json(PARSE_DIR / f"{stem}_parse.json", result)
        (PARSE_DIR / f"{stem}_parse.md").write_text(result.get("markdown", ""), encoding="utf-8")

        parsed[stem] = {
            "job_id": job_id,
            "markdown": result.get("markdown", ""),
            "metadata": result.get("metadata", {}),
        }
        pages = result.get("metadata", {}).get("page_count")
        print(f"  parsed   {stem:<20} ({pages} page(s)) -> {stem}_parse.json / {stem}_parse.md")

    return parsed


def run_extract_stage(
    parsed: dict[str, dict[str, Any]], schema_json: str, api_key: str
) -> dict[str, dict[str, Any]]:
    """
    Steps 4-5: submit an extract job per parsed document, poll, and save JSON.

    Returns a mapping: document stem -> full Extract v2 result dict.
    """
    print(f"\n=== Extract stage: submitting {len(parsed)} document(s) ===")
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    submitted: dict[str, str] = {}  # stem -> job_id
    for stem, info in parsed.items():
        job_id = ade.create_extract_job(
            markdown=info["markdown"],
            schema_json=schema_json,
            api_key=api_key,
            service_tier=SERVICE_TIER,
            filename=f"{stem}.md",
        )
        submitted[stem] = job_id
        print(f"  submitted {stem:<20} -> {job_id}")

    extracted: dict[str, dict[str, Any]] = {}
    for stem, job_id in submitted.items():
        job = ade.poll_job(ade.get_extract_job, job_id, api_key)
        if job.get("status") != "completed":
            err = job.get("error") or {}
            print(f"  !! extract FAILED for {stem}: {err.get('code')}: {err.get('message')}")
            continue

        result = job["result"]  # extraction, extraction_metadata, markdown, metadata
        # Record the extract job_id alongside the result for the CSV summaries.
        result["_extract_job_id"] = job_id
        _write_json(EXTRACT_DIR / f"{stem}_extract.json", result)
        extracted[stem] = result
        print(f"  extracted {stem:<20} -> {stem}_extract.json")

    return extracted


def build_summaries(
    parsed: dict[str, dict[str, Any]],
    extracted: dict[str, dict[str, Any]],
    processing_date: str,
) -> None:
    """Steps 6-7: write the field-summary and metadata CSVs."""
    print("\n=== Summary stage: writing CSVs ===")
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    fields_rows: list[dict[str, Any]] = []
    metadata_rows: list[dict[str, Any]] = []

    for stem, result in extracted.items():
        extract_job_id = result.get("_extract_job_id")
        parse_info = parsed.get(stem, {})

        extraction = result.get("extraction") or {}

        # --- Step 6: flat per-document extracted fields ---
        row = {
            "document_name": stem,
            "job_id": extract_job_id,
            "processing_date": processing_date,
        }
        row.update(flatten(extraction))
        fields_rows.append(row)

        # --- Step 7: parse + extract metadata, one row per document ---
        meta_row: dict[str, Any] = {
            "document_name": stem,
            "processing_date": processing_date,
        }
        meta_row.update(flatten(parse_info.get("metadata", {}), prefix="parse"))
        meta_row.update(flatten(result.get("metadata", {}), prefix="extract"))
        metadata_rows.append(meta_row)

    _save_csv(fields_rows, CSV_DIR / "certificate_fields_summary.csv")
    _save_csv(metadata_rows, CSV_DIR / "processing_metadata.csv")


def _save_csv(rows: list[dict[str, Any]], path: Path) -> None:
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"  wrote {path.name:<32} ({len(df)} row(s), {len(df.columns)} column(s))")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="CME certificate pipeline on ADE v2 (DPT-3).")
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Process only the first N documents (useful for a smoke test).",
    )
    parser.add_argument(
        "--only", nargs="+", default=None, metavar="STEM",
        help="Process only these documents by name stem (e.g. --only CME_Mendez_ex1).",
    )
    args = parser.parse_args()

    load_env()
    api_key = ade.get_api_key()
    processing_date = dt.date.today().isoformat()

    schema_json = SCHEMA_PATH.read_text(encoding="utf-8")
    documents = discover_documents(INPUT_FOLDER)
    if not documents:
        raise SystemExit(f"No supported documents found in {INPUT_FOLDER}")
    if args.only:
        wanted = set(args.only)
        documents = [d for d in documents if d.stem in wanted]
        missing = wanted - {d.stem for d in documents}
        if missing:
            raise SystemExit(f"Documents not found in {INPUT_FOLDER}: {sorted(missing)}")
    if args.limit is not None:
        documents = documents[: args.limit]

    print(f"Processing {len(documents)} document(s) from {INPUT_FOLDER}")
    print(f"Service tier: {SERVICE_TIER} | Parse model: {ade.DEFAULT_PARSE_MODEL}")

    parsed = run_parse_stage(documents, api_key)
    extracted = run_extract_stage(parsed, schema_json, api_key)
    build_summaries(parsed, extracted, processing_date)

    print(
        f"\nDone. Parsed {len(parsed)}/{len(documents)}, extracted {len(extracted)}. "
        f"Results in {RESULTS_FOLDER}"
    )


if __name__ == "__main__":
    main()
