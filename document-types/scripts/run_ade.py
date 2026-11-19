#!/usr/bin/env python3
"""Parse and extract one document type's sample, writing the output the page needs.

    python document-types/scripts/run_ade.py invoice                  # DPT-3 Pro
    python document-types/scripts/run_ade.py invoice --parse verity
    python document-types/scripts/run_ade.py invoice --parse verity --extract-only

Reads  collection/<slug>/source/<doc>  and  collection/<slug>/schema.json
Writes collection/<slug>/runs/<parse snapshot>/parse.json, parse.md
       collection/<slug>/runs/<parse snapshot>/<extract snapshot>/extract.json
and records the run, with its credits, under "runs" in manifest.json.

Snapshots are pinned in runs.py. The directories are named for the snapshot the API
reports in metadata.model_version, which is normally the one requested: a superseded
snapshot resolves to its replacement, and the files say what actually ran.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runs import (COLLECTION, EXTRACT_MODEL, Run, extract_snapshot,  # noqa: E402
                  parse_snapshot, record_run, runs_in)

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


def resolved(result, requested: str, kind: str) -> str:
    """The snapshot that actually ran. Superseded snapshots resolve to their
    replacement; the files are named for what ran, not what was asked for."""
    version = getattr(getattr(result, "metadata", None), "model_version", None) or requested
    if version != requested:
        print(f"  NOTE: requested {kind} {requested}, API ran {version}; filing under {version}")
    return version


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="folder name under document-types/collection/")
    parser.add_argument("--parse", default="pro", metavar="MODEL",
                        help="pro, verity, or an exact dpt-3 snapshot (default: pro)")
    parser.add_argument("--extract", default=EXTRACT_MODEL, metavar="MODEL",
                        help=f"extract snapshot (default: {EXTRACT_MODEL})")
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="reuse the committed parse for this parse model and only re-run "
             "extraction. Use this when iterating on schema.json, or to extract an "
             "existing parse with another extract snapshot: re-parsing a long "
             "document is the expensive half and the markdown does not change.",
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
    parse_model = parse_snapshot(args.parse)
    extract_model = extract_snapshot(args.extract)
    load_api_key()

    from landingai_ade import LandingAIADE  # imported late so --help works without a key

    client = LandingAIADE()
    parse_credits = 0.0

    if args.extract_only:
        # The parse to reuse: exactly the requested snapshot, else the only parse of
        # that family already in the folder.
        parse_dirs = [d for d in sorted((folder / "runs").glob("*/"))
                      if (d / "parse.md").is_file()
                      and (d.name == parse_model or d.name == args.parse
                           or (args.parse in ("pro", "verity")
                               and d.name.startswith(f"dpt-3-{args.parse}-")))]
        exact = [d for d in parse_dirs if d.name == parse_model]
        parse_dirs = exact or parse_dirs
        if len(parse_dirs) != 1:
            have = ", ".join(d.name for d in (folder / "runs").glob("*/")) or "none"
            sys.exit(f"--extract-only needs exactly one committed parse for {args.parse}; "
                     f"parses present: {have}")
        parse_model = parse_dirs[0].name
        markdown = (parse_dirs[0] / "parse.md").read_text(encoding="utf-8")
        print(f"Reusing runs/{parse_model}/parse.md ({len(markdown):,} chars); not re-parsing.")
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
        parse_model = resolved(parse_result, parse_model, "parse")

        parse_dir = folder / "runs" / parse_model
        parse_dir.mkdir(parents=True, exist_ok=True)
        write_json(parse_result, parse_dir / "parse.json")
        # Keep the trailing `doc_id` comment: v2 Extract reads it to link the extraction
        # back to this parse job.
        (parse_dir / "parse.md").write_text(parse_result.markdown, encoding="utf-8")
        markdown = parse_result.markdown
        parse_credits = credits_of(parse_result)

        failed = parse_result.metadata.failed_pages or []
        print(f"  {parse_result.metadata.page_count} page(s)" + (f", FAILED: {failed}" if failed else ""))

    print(f"Extracting with {extract_model} ({SERVICE_TIER} tier) ...")
    extract_job = client.v2.extract_jobs.create(
        markdown=markdown,
        schema=schema,
        model=extract_model,
        service_tier=SERVICE_TIER,
    )
    extract_done = client.v2.extract_jobs.wait(
        extract_job.job_id, timeout=JOB_TIMEOUT_S, raise_on_failure=True
    )
    extract_result = extract_done.result
    extract_model = resolved(extract_result, extract_model, "extract")

    run = Run(folder, parse_model, extract_model)
    run.dir.mkdir(parents=True, exist_ok=True)
    write_json(extract_result, run.extract_json)

    if getattr(extract_result, "schema_violation_error", None):
        print(f"  partial extraction: {extract_result.schema_violation_error}")
    for warning in getattr(extract_result, "warnings", None) or []:
        print(f"  warning: {warning}")

    found = sum(1 for v in extract_result.extraction.values() if v not in (None, "", []))
    print(f"  {found}/{len(extract_result.extraction)} top-level fields populated")

    if not record_run(run):
        print("  (no manifest.json yet: build_images.py records the run once it exists)")

    total = parse_credits + credits_of(extract_result)
    print(f"\nWrote {run.rel(run.dir)}/" + ("" if args.extract_only else
          f" and {run.rel(run.parse_dir)}/parse.json, parse.md"))
    print(f"Credits used: {total:.2f} ({SERVICE_TIER} tier)")
    others = [r.label for r in runs_in(folder) if r != run]
    if others:
        print(f"Other runs in this folder: {', '.join(others)}")
    print(f"\nNext: python document-types/scripts/build_images.py {args.slug} "
          f"--parse {run.parse_model} --extract {run.extract_model}")


if __name__ == "__main__":
    main()
