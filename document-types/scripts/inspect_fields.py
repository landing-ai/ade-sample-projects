#!/usr/bin/env python3
"""List every extracted field with the page and quality of each of its groundings.

    python document-types/scripts/inspect_fields.py investor-presentation
    python document-types/scripts/inspect_fields.py investor-presentation --page 20

Use this to choose what a page features. Picking fields by reading `extract-*.json`
alone does not work, because a value can be:

  - **synthesized** — correct, but with no ranges at all, so it cannot be illustrated
  - **grounded off** — pointing at text that supports the value without containing it
  - **grounded elsewhere** — on a different page from the one being featured

All three are invisible until you look, and all three produce a bad page.

Reads the committed parse and extract output. Never calls the API.

Columns:
  page   the page an occurrence lands on
  match  whether the extracted value appears in the text that would be boxed
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_images import flatten, locate, value_appears_in  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
COLLECTION = REPO_ROOT / "document-types" / "collection"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--model", default="pro")
    parser.add_argument("--page", type=int, help="only show occurrences on this page")
    parser.add_argument("--good", action="store_true",
                        help="only show occurrences that are grounded and match")
    args = parser.parse_args()

    folder = COLLECTION / args.slug
    parse = json.loads((folder / f"parse-{args.model}.json").read_text(encoding="utf-8"))
    extract = json.loads((folder / f"extract-{args.model}.json").read_text(encoding="utf-8"))
    markdown = extract["markdown"]

    fields = flatten(extract.get("extraction_metadata") or {})
    print(f"{len(fields)} leaf field(s)\n")
    print(f"{'field':58} {'occ':>3} {'page':>5} {'match':>6}  value / boxed text")
    print("-" * 118)

    shown = 0
    for path, meta in fields.items():
        ranges = meta.get("ranges") or []
        value = str(meta.get("value"))[:26]

        if not ranges:
            if not args.page and not args.good:
                print(f"{path[:58]:58} {'-':>3} {'-':>5} {'SYNTH':>6}  {value}")
            continue

        for i, rng in enumerate(ranges):
            hit = locate(parse, rng)
            page = hit[0] if hit else None
            if args.page and page != args.page:
                continue
            source = markdown[rng["start"]:rng["end"]].replace("\n", " ")
            ok = value_appears_in(meta.get("value"), source)
            if args.good and not ok:
                continue
            print(f"{path[:58]:58} {i:>3} {str(page):>5} {'ok' if ok else 'OFF':>6}  "
                  f"{value} <- {source[:40]!r}")
            shown += 1

    if args.page:
        print(f"\n{shown} occurrence(s) on page {args.page}")
        print("Feature only rows marked ok. A row marked OFF boxes text that does not "
              "contain the value.")


if __name__ == "__main__":
    main()
