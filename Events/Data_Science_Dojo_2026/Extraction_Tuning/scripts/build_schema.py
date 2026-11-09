"""
build_schema.py  —  Generate or refine an extraction schema via LandingAI Build Schema API.

On first run, the API analyzes your parsed markdowns and a prompt describing
what to extract, then returns a JSON schema you can pass directly to Extract.

On subsequent runs, pass the existing schema with a revision prompt — the API
refines it in place.

The previous schema is always versioned to schemas/history/ before overwriting.

Usage:
  # Initial build — describe the fields you want:
  python scripts/build_schema.py \\
      --prompt "Extract patient name, age, gender, and all CBC panel values including
                rbc_count_value, rbc_count_unit, hemoglobin_value, hemoglobin_unit ..."

  # Refinement — pass current schema + what to fix:
  python scripts/build_schema.py \\
      --schema schemas/current.json \\
      --prompt "The age field is returning strings; change its type to integer.
                The rbc_count_value field is missing; ensure it maps to the RBC count row."
"""

import argparse
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["VISION_AGENT_API_KEY"]
BUILD_URL = "https://api.va.landing.ai/v1/ade/extract/build-schema"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

PARSED_DIR = Path("data/pipeline_outputs/parsed")
SCHEMA_PATH = Path("schemas/current.json")
HISTORY_DIR = Path("schemas/history")


def main():
    parser = argparse.ArgumentParser(description="Build or refine a LandingAI extraction schema.")
    parser.add_argument(
        "--prompt", required=True,
        help="Instructions for schema generation or refinement",
    )
    parser.add_argument(
        "--schema", type=Path, default=None,
        help="Existing schema to refine (omit for initial build)",
    )
    parser.add_argument(
        "--markdowns", type=Path, nargs="*", default=None,
        help="Markdown files to analyze (default: all files in pipeline_outputs/parsed/)",
    )
    args = parser.parse_args()

    # Resolve markdown files
    md_files = args.markdowns if args.markdowns else sorted(PARSED_DIR.glob("*_markdown.md"))

    if not md_files:
        print("No markdown files found. Run parse.py first.")
        return

    mode = "Refinement" if args.schema else "Initial build"
    print(f"Mode:     {mode}")
    print(f"Docs:     {len(md_files)} markdown file(s)")
    print(f"Prompt:   {args.prompt}\n")

    # Build multipart form.
    # The requests library encodes each entry as (field_name, (filename, data, content_type)).
    # For plain string values (not file uploads), use (None, value) — no filename or mimetype.
    files = []
    opened_handles = []

    for md_path in md_files:
        fh = open(md_path, "rb")
        opened_handles.append(fh)
        files.append(("markdowns", (md_path.name, fh, "text/plain")))

    files.append(("model", (None, "extract-latest")))
    files.append(("prompt", (None, args.prompt)))

    if args.schema and args.schema.exists():
        # Strip the internal _meta block before sending to the API.
        # _meta is added by the Build Schema API itself (it records model version,
        # prompt history, etc.) and is not a valid JSON Schema keyword — sending it
        # back would cause an extraction error.
        schema_obj = json.loads(args.schema.read_text())
        schema_obj.pop("_meta", None)
        files.append(("schema", (None, json.dumps(schema_obj))))

    t_start = time.perf_counter()
    response = requests.post(BUILD_URL, headers=HEADERS, files=files)
    elapsed = time.perf_counter() - t_start

    for fh in opened_handles:
        fh.close()

    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)
        return

    data = response.json()
    new_schema = json.loads(data["extraction_schema"])

    # Version previous schema before overwriting
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    if SCHEMA_PATH.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = HISTORY_DIR / f"current_{timestamp}.json"
        shutil.copy(SCHEMA_PATH, backup)
        print(f"Previous schema backed up to: {backup}")

    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_PATH.write_text(json.dumps(new_schema, indent=2))

    fields = list(new_schema.get("properties", {}).keys())
    print(f"\nSchema saved to:  {SCHEMA_PATH}")
    print(f"Fields ({len(fields)}):  {fields}")
    print(f"API time:         {elapsed:.1f}s")

    warnings = data.get("metadata", {}).get("warnings", [])
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  [{w.get('code')}] {w.get('msg')}")


if __name__ == "__main__":
    main()
