#!/usr/bin/env python3
"""Write the generated part of a document type's README: everything above `## Origin`.

    python document-types/scripts/build_readme.py <slug>
    python document-types/scripts/build_readme.py --all
    python document-types/scripts/build_readme.py <slug> --check   # exit 1 if out of date

A README has two parts. You write the title (`# ...`), a description paragraph under
it, and everything from `## Origin` down: Origin, then Why this document with "Who
processes it" and "What it contains". This script writes the rest: the website link,
the page and schema-field counts, and the Parse performance and Extract performance
sections. It reads the numbers from the folder's runs on the pinned snapshots in
runs.py, DPT-3 Verity first when the folder has a Verity run.

To start a new README, write just the title, the description and the Origin and Why
sections, then run this script; it inserts the generated sections between them.

Speed is the processing time the API reports (`metadata.duration_ms`). Cost is the
credits billed (`metadata.billing.total_credits`). Processed time is decoded from the
job ID, which begins with its creation time (a ULID); the API returns no timestamp.
Reads committed files only. No API calls.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_images import flatten  # noqa: E402
from runs import COLLECTION, EXTRACT_MODEL, PARSE_MODELS, Run  # noqa: E402

WEBSITE = "https://landing.ai/document-type"
REGION = "US"   # run_ade.py uses the SDK's default endpoint, api.va.landing.ai
FAMILIES = ("verity", "pro")
NAMES = {"verity": "DPT-3 Verity", "pro": "DPT-3 Pro"}
MARKDOWN = {"verity": "Verity markdown", "pro": "Pro markdown"}
CONFIDENCE = (0.95, 0.80, 0.50)
SPEED_NOTE = ("Times are from a single run of each model. They vary from run to run with\n"
              "server load, so treat small differences between models as noise.")
ULID = "0123456789abcdefghjkmnpqrstvwxyz"


def job_time(job_id: str) -> str:
    """Creation time encoded in the first 10 characters of a job ID's ULID."""
    ms = 0
    for ch in job_id.split("-", 1)[1][:10]:
        ms = ms * 32 + ULID.index(ch)
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M")


def walk(node: dict):
    yield node
    for child in node.get("children") or []:
        yield from walk(child)


def schema_fields(node: dict) -> int:
    """Leaf fields in a JSON schema; an array of objects counts its item's leaves once."""
    if node.get("type") == "object" or "properties" in node:
        return sum(schema_fields(v) for v in node.get("properties", {}).values())
    if node.get("type") == "array":
        return schema_fields(node.get("items", {}))
    return 1


def measure(folder: Path) -> dict:
    n_fields = schema_fields(json.loads((folder / "schema.json").read_text()))
    out = {"fields": n_fields, "pages": None, "models": {}}
    for fam in FAMILIES:
        run = Run(folder, PARSE_MODELS[fam], EXTRACT_MODEL)
        if not run.extract_json.is_file():
            continue
        parse = json.loads(run.parse_json.read_text())
        extract = json.loads(run.extract_json.read_text())
        pm, em = parse["metadata"], extract["metadata"]
        pages = pm["page_count"]
        conf = [a["confidence"] for n in walk(parse["structure"])
                for a in n.get("atomic_grounding") or [] if "confidence" in a]
        flat = flatten(extract.get("extraction_metadata") or {})
        values = [k for k, m in flat.items() if m.get("value") not in (None, "", [])]
        fields = {re.sub(r"\[\d+\]", "[]", k) for k in values}
        ps, es = pm["duration_ms"] / 1000, em["duration_ms"] / 1000
        pc, ec = pm["billing"]["total_credits"], em["billing"]["total_credits"]
        out["pages"] = pages
        out["models"][fam] = {
            "run": run, "parse_time": job_time(pm["job_id"]), "extract_time": job_time(em["job_id"]),
            "chars": pm["output_markdown_chars"],
            "conf": {t: sum(c < t for c in conf) for t in CONFIDENCE} if conf else None,
            "parse_s": ps, "parse_s_page": ps / pages, "parse_c": pc, "parse_c_page": pc / pages,
            "fields_returned": len(fields),
            "extract_s": es, "extract_s_field": es / n_fields, "extract_s_value": es / max(len(values), 1),
            "extract_c": ec, "extract_c_field": ec / n_fields, "extract_c_value": ec / max(len(values), 1),
        }
    if not out["models"]:
        sys.exit(f"{folder.name}: no run on {', '.join(PARSE_MODELS.values())} with {EXTRACT_MODEL}")
    return out


def table(head: list[str], rows: list[tuple[str, list[str]]]) -> str:
    lines = ["| | " + " | ".join(head) + " |", "|---" * (len(head) + 1) + "|"]
    lines += ["| " + label + " | " + " | ".join(cells) + " |" for label, cells in rows]
    return "\n".join(lines)


def generated(slug: str, title: str, description: str, s: dict) -> str:
    fams = list(s["models"])
    m = s["models"]
    both = len(fams) == 2
    nf = s["fields"]

    def col(fn):
        return [fn(m[f]) for f in fams]

    def parse_dir(f):
        return m[f]["run"].rel(m[f]["run"].parse_dir) + "/"

    def extract_dir(f):
        return m[f]["run"].rel(m[f]["run"].dir) + "/"

    head, mhead = [NAMES[f] for f in fams], [MARKDOWN[f] for f in fams]
    parts = [
        f"# {title}", "",
        f"**On the website:** [landing.ai/document-type/{slug}]({WEBSITE}/{slug})", "",
        description.strip(), "",
        "| | |\n|---|---|", f"| Pages | {s['pages']} |", f"| Fields in the extraction schema | {nf} |", "",
        ("Both models ran at standard tier through the jobs API, and both extractions used\n"
         f"`{EXTRACT_MODEL}`.") if both else
        ("DPT-3 Pro ran at standard tier through the jobs API, and the extraction used\n"
         f"`{EXTRACT_MODEL}`."),
        "Times are the processing time the API reports (`metadata.duration_ms`), not counting\n"
        "time queued. Costs are the credits billed (`metadata.billing.total_credits`).", "",
        "## Parse performance", "",
        table(head, [
            ("Snapshot", col(lambda x: f"`{x['run'].parse_model}`")),
            ("Output", [f"[`{parse_dir(f)}`]({parse_dir(f)})" for f in fams]),
            ("Processed (UTC)", col(lambda x: x["parse_time"])),
            ("Region", col(lambda x: REGION)),
        ]), "",
        "### Parse accuracy", "",
    ]
    conf_rows = []
    if both:
        parts += ["Word confidence is the `confidence` DPT-3 Verity reports on each word box.", ""]
        conf_rows = [(f"Words under {t:.2f} confidence",
                      col(lambda x, t=t: f"{x['conf'][t]:,}" if x["conf"] else "n/a"))
                     for t in CONFIDENCE]
    parts += [
        table(head, [("Characters returned", col(lambda x: f"{x['chars']:,}"))] + conf_rows
              + [("Accuracy", col(lambda x: "To come"))]), "",
        "### Parse speed", "", SPEED_NOTE, "",
        table(head, [("Total", col(lambda x: f"{x['parse_s']:.1f} s")),
                     ("Per page", col(lambda x: f"{x['parse_s_page']:.1f} s"))]), "",
        "### Parse cost", "",
        table(head, [("Total", col(lambda x: f"{x['parse_c']:.1f} credits")),
                     ("Per page", col(lambda x: f"{x['parse_c_page']:.2f} credits"))]), "",
        "## Extract performance", "",
        ("Each model's markdown was extracted separately with the same schema. " if both
         else "The Pro markdown was extracted with the schema. ")
        + "\"Per value\nreturned\" divides by every non-empty value extracted, so an array of six "
          "items counts\nsix.", "",
        table(mhead, [
            ("Snapshot", col(lambda x: f"`{x['run'].extract_model}`")),
            ("Output", [f"[`{extract_dir(f)}`]({extract_dir(f)})" for f in fams]),
            ("Processed (UTC)", col(lambda x: x["extract_time"])),
            ("Region", col(lambda x: REGION)),
        ]), "",
        "### Extract accuracy", "",
        table(mhead, [("Fields requested", col(lambda x: str(nf))),
                      ("Non-null fields returned", col(lambda x: str(x["fields_returned"]))),
                      ("Accuracy", col(lambda x: "To come"))]), "",
        "### Extract speed", "", SPEED_NOTE, "",
        table(mhead, [("Total", col(lambda x: f"{x['extract_s']:.1f} s")),
                      (f"Per schema field ({nf})", col(lambda x: f"{x['extract_s_field']:.2f} s")),
                      ("Per value returned", col(lambda x: f"{x['extract_s_value']:.2f} s"))]), "",
        "### Extract cost", "",
        table(mhead, [("Total", col(lambda x: f"{x['extract_c']:.1f} credits")),
                      (f"Per schema field ({nf})", col(lambda x: f"{x['extract_c_field']:.3f} credits")),
                      ("Per value returned", col(lambda x: f"{x['extract_c_value']:.3f} credits"))]), "",
    ]
    return "\n".join(parts)


def split(readme: str, slug: str) -> tuple[str, str, str]:
    """(title, description, hand-written tail from ## Origin) of an existing README."""
    title = re.search(r"^# (.+)$", readme, re.M)
    if not title or "\n## Origin" not in "\n" + readme:
        sys.exit(f"{slug}: README.md needs a '# Title' line and a '## Origin' section")
    head, tail = readme.split("## Origin", 1) if readme.startswith("## Origin") else \
        readme.split("\n## Origin", 1)
    body = head[title.end():].strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    description = next((p for p in paragraphs if not p.startswith(("**On the website:**", "|"))), "")
    if not description:
        sys.exit(f"{slug}: README.md has no description paragraph under the title")
    return title.group(1).strip(), description, "## Origin" + tail


def build(slug: str) -> tuple[str, str]:
    path = COLLECTION / slug / "README.md"
    if not path.is_file():
        sys.exit(f"{slug}: write README.md first (title, description, ## Origin, ## Why this document)")
    old = path.read_text()
    title, description, tail = split(old, slug)
    new = generated(slug, title, description, measure(COLLECTION / slug)) + "\n" + tail.strip() + "\n"
    return old, new


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--check", action="store_true", help="report, do not write; exit 1 if stale")
    args = parser.parse_args()
    slugs = sorted(p.name for p in COLLECTION.iterdir() if p.is_dir()) if args.all else args.slugs
    if not slugs:
        parser.error("name slugs or pass --all")
    stale = []
    for slug in slugs:
        old, new = build(slug)
        if old != new:
            stale.append(slug)
            if not args.check:
                (COLLECTION / slug / "README.md").write_text(new)
    verb = "out of date" if args.check else "rewritten"
    print(f"{len(stale)} of {len(slugs)} README(s) {verb}" + (": " + ", ".join(stale) if stale else ""))
    if args.check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
