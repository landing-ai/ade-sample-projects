#!/usr/bin/env python3
"""Parse and extract one document type's sample, writing the output the page needs.

    python document-types/scripts/run_ade.py invoice

Reads  collection/<slug>/source/<doc>  and  collection/<slug>/schema.json
Writes collection/<slug>/parse-<model>.json, parse-<model>.md, extract-<model>.json

This is the script that spends credits. Image generation is deliberately separate
(build_images.py) so that re-rendering never costs anything and never depends on a
fresh parse returning identical output.

Runs through the **jobs APIs at the standard service tier**, which costs half of
priority. Synchronous calls always bill at priority regardless of what you ask for, so
the jobs API is the only way to get the cheaper rate. Web content is never urgent.

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

# Output files carry the parse model, because a document type may eventually be parsed
# by more than one and the results must not overwrite each other.
#
# Verity is in Preview and changing; it gets added here once it is GA, at which point a
# folder can hold parse-pro.json and parse-verity.json side by side.
PARSE_MODELS = {
    "pro": "dpt-3-pro-latest",
}

EXTRACT_MODEL = "extract-latest"
SERVICE_TIER = "standard"   # half the credits of priority; turnaround is slower
JOB_TIMEOUT_S = 900

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


def write_json(obj, path: Path) -> None:
    """Serialize an SDK response model to disk. The jobs APIs do not accept save_to,
    so unlike the sync calls this is written by hand."""
    if hasattr(obj, "model_dump_json"):
        path.write_text(obj.model_dump_json(indent=2), encoding="utf-8")
    else:
        path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")


def credits_of(result) -> float:
    billing = getattr(getattr(result, "metadata", None), "billing", None)
    return float(getattr(billing, "total_credits", 0) or 0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="folder name under document-types/collection/")
    parser.add_argument(
        "--model",
        default="pro",
        choices=sorted(PARSE_MODELS),
        help="parse model; names the output files (default: pro)",
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="reuse the committed parse output and only re-run extraction. Use this "
             "when iterating on schema.json: re-parsing a long document is the "
             "expensive half and the markdown does not change.",
    )
    args = parser.parse_args()

    folder = COLLECTION / args.slug
    if not folder.is_dir():
        sys.exit(f"No such document type: {folder}")

    schema_path = folder / "schema.json"
    if not schema_path.is_file():
        sys.exit(f"Missing {schema_path}. Every document type needs a schema.")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    document = find_source(folder)
    parse_model = PARSE_MODELS[args.model]
    load_api_key()

    from landingai_ade import LandingAIADE  # imported late so --help works without a key

    client = LandingAIADE()

    parse_md_path = folder / f"parse-{args.model}.md"
    parse_credits = 0.0

    if args.extract_only:
        if not parse_md_path.is_file():
            sys.exit(f"--extract-only needs {parse_md_path}, which does not exist.")
        markdown = parse_md_path.read_text(encoding="utf-8")
        print(f"Reusing {parse_md_path.name} ({len(markdown):,} chars); not re-parsing.")
    else:
        print(f"Parsing {document.name} with {parse_model} ({SERVICE_TIER} tier) ...")
        parse_job = client.v2.parse_jobs.create(
            document=document,
            model=parse_model,
            service_tier=SERVICE_TIER,
        )
        parse_done = client.v2.parse_jobs.wait(
            parse_job.job_id, timeout=JOB_TIMEOUT_S, raise_on_failure=True
        )
        parse_result = parse_done.result

        write_json(parse_result, folder / f"parse-{args.model}.json")
        # Keep the trailing `doc_id` comment: v2 Extract reads it to link the extraction
        # back to this parse job.
        parse_md_path.write_text(parse_result.markdown, encoding="utf-8")
        markdown = parse_result.markdown
        parse_credits = credits_of(parse_result)

        failed = parse_result.metadata.failed_pages or []
        print(f"  {parse_result.metadata.page_count} page(s)" + (f", FAILED: {failed}" if failed else ""))

    print(f"Extracting with {EXTRACT_MODEL} ({SERVICE_TIER} tier) ...")
    extract_job = client.v2.extract_jobs.create(
        markdown=markdown,
        schema=schema,
        model=EXTRACT_MODEL,
        service_tier=SERVICE_TIER,
    )
    extract_done = client.v2.extract_jobs.wait(
        extract_job.job_id, timeout=JOB_TIMEOUT_S, raise_on_failure=True
    )
    extract_result = extract_done.result

    # Named for the parse model it came from: an extraction is only meaningful against
    # the markdown that produced it.
    write_json(extract_result, folder / f"extract-{args.model}.json")

    if getattr(extract_result, "schema_violation_error", None):
        print(f"  partial extraction: {extract_result.schema_violation_error}")
    for warning in getattr(extract_result, "warnings", None) or []:
        print(f"  warning: {warning}")

    found = sum(1 for v in extract_result.extraction.values() if v not in (None, "", []))
    print(f"  {found}/{len(extract_result.extraction)} top-level fields populated")

    total = parse_credits + credits_of(extract_result)
    written = (f"extract-{args.model}.json" if args.extract_only else
               f"parse-{args.model}.json, parse-{args.model}.md, extract-{args.model}.json")
    print(f"\nWrote {written} to {folder}")
    print(f"Credits used: {total:.2f} ({SERVICE_TIER} tier)")
    print(f"\nNext: python document-types/scripts/build_images.py {args.slug}")


if __name__ == "__main__":
    main()
