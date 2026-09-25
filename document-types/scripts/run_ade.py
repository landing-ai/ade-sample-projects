#!/usr/bin/env python3
"""Parse and extract one document type's sample, writing the output the page needs.

    python document-types/scripts/run_ade.py invoice

Reads  collection/<slug>/source/<doc>  and  collection/<slug>/schema.json
Writes collection/<slug>/parse.json, parse.md, extract.json

This is the script that spends credits. Image generation is deliberately separate
(build_images.py) so that re-rendering never costs anything and never depends on a
fresh parse returning identical output.

ADE v2 (DPT-3) only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
COLLECTION = REPO_ROOT / "document-types" / "collection"

# Pinned rather than -latest: the committed output and the images built from it are a
# record of one model's behaviour, and a silent model bump would make them disagree.
PARSE_MODEL = "dpt-3-pro-latest"
EXTRACT_MODEL = "extract-latest"

SOURCE_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def load_api_key() -> None:
    """Find a VISION_AGENT_API_KEY without ever printing it."""
    if os.environ.get("VISION_AGENT_API_KEY"):
        return
    for directory in (Path.cwd(), *Path.cwd().parents):
        candidate = directory / ".env"
        if candidate.is_file():
            load_dotenv(candidate)
            if os.environ.get("VISION_AGENT_API_KEY"):
                return
    sys.exit(
        "VISION_AGENT_API_KEY not set and no .env found.\n"
        "Get a key at https://va.landing.ai/settings/api-key and put it in a .env "
        "at the repo root:\n    VISION_AGENT_API_KEY=<key>"
    )


def find_source(folder: Path) -> Path:
    source_dir = folder / "source"
    if not source_dir.is_dir():
        sys.exit(f"No source/ directory in {folder}")
    docs = sorted(p for p in source_dir.iterdir() if p.suffix.lower() in SOURCE_SUFFIXES)
    if not docs:
        sys.exit(f"No document found in {source_dir}")
    if len(docs) > 1:
        sys.exit(
            f"{source_dir} holds {len(docs)} documents; a page features exactly one.\n"
            "Keep the featured document here and move the rest elsewhere."
        )
    return docs[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="folder name under document-types/collection/")
    args = parser.parse_args()

    folder = COLLECTION / args.slug
    if not folder.is_dir():
        sys.exit(f"No such document type: {folder}")

    schema_path = folder / "schema.json"
    if not schema_path.is_file():
        sys.exit(f"Missing {schema_path}. Every document type needs a schema.")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    document = find_source(folder)
    load_api_key()

    from landingai_ade import LandingAIADE  # imported late so --help works without a key

    client = LandingAIADE()

    print(f"Parsing {document.name} with {PARSE_MODEL} ...")
    parse_result = client.v2.parse(
        document=document,
        model=PARSE_MODEL,
        save_to=str(folder / "parse.json"),
    )

    # Keep the trailing `doc_id` comment: v2 Extract reads it to link the extraction
    # back to this parse job.
    (folder / "parse.md").write_text(parse_result.markdown, encoding="utf-8")

    pages = parse_result.metadata.page_count
    failed = parse_result.metadata.failed_pages or []
    print(f"  {pages} page(s) parsed" + (f", FAILED: {failed}" if failed else ""))

    print(f"Extracting with {EXTRACT_MODEL} ...")
    extract_result = client.v2.extract(
        markdown=parse_result.markdown,
        schema=schema,
        model=EXTRACT_MODEL,
        save_to=str(folder / "extract.json"),
    )

    if getattr(extract_result, "schema_violation_error", None):
        print(f"  partial extraction: {extract_result.schema_violation_error}")
    for warning in getattr(extract_result, "warnings", None) or []:
        print(f"  warning: {warning}")

    found = sum(1 for v in extract_result.extraction.values() if v not in (None, "", []))
    print(f"  {found}/{len(extract_result.extraction)} top-level fields populated")

    credits = 0.0
    for result in (parse_result, extract_result):
        billing = getattr(result.metadata, "billing", None)
        if billing and billing.total_credits:
            credits += billing.total_credits
    print(f"\nWrote parse.json, parse.md, extract.json to {folder}")
    print(f"Credits used: {credits:.2f}")
    print(f"\nNext: python document-types/scripts/build_images.py {args.slug}")


if __name__ == "__main__":
    main()
