#!/usr/bin/env python3
"""Replace personal data in a source PDF before it enters the collection.

    python document-types/scripts/redact.py in.pdf out.pdf --rules rules.json

Real documents make the best samples, and most real documents carry someone's name,
address or account number. Publishing those is not an option, and a blank box makes a
poor demonstration — so this substitutes obviously-fake values of a similar shape,
leaving a document that still looks and parses like the real thing.

It uses PyMuPDF redaction annotations, which **remove the underlying text** rather than
drawing a rectangle over it. Text hidden under a filled box is still in the file and
still extractable, which is the usual way a "redacted" PDF leaks.

`--rules` is JSON mapping each string to its replacement:

    { "<name as printed>": "JANE DOE", "<account number>": "000-00000-0-0" }

Keep that file OUTSIDE the repo: it pairs every original string with its replacement,
so it is the personal data in plain text. For the same reason, never paste the originals
into a README or manifest to "record the provenance" -- note what was replaced, not what
it replaced.

After writing, it re-extracts the text and fails loudly if any original string survives.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pymupdf

# Same grey as surrounding body text usually sits on; replacements are drawn in black on
# white so they read as ordinary content rather than as an obvious edit.
FILL = (1, 1, 1)
TEXT_COLOR = (0, 0, 0)

# search_for returns a rect spanning the full line height, including ascender space that
# can graze the line above. apply_redactions removes any glyph intersecting the rect, so
# an untrimmed rect silently eats the first words of the label overhead — "Recipient's
# Name:" became "Name:" before this was added. Trimming the top costs nothing: a glyph is
# still removed as long as the rect crosses its body.
FONT = "helv"
TOP_INSET_PT = 2.5
BOTTOM_INSET_PT = 0.5


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument(
        "--drop-pages", type=int, nargs="*", default=[],
        help="1-indexed pages to remove entirely. Use for pages that carry personal "
             "data but no demonstration value -- a mailing panel, for instance, whose "
             "rotated text cannot be replaced cleanly anyway.",
    )
    args = parser.parse_args()

    rules: dict[str, str] = json.loads(args.rules.read_text(encoding="utf-8"))

    # A replacement longer than what it replaces gets wrapped by PyMuPDF to fit the
    # rect, and wrapping a short field breaks it into fragments: "SAMPLE TAXPAYER" came
    # back from the text layer as "SAM" / "PLE" / "TAX" / "PAY", which then failed to
    # extract as a name at all. Keep replacements no longer than the original.
    too_long = {k: v for k, v in rules.items() if len(v) > len(k)}
    if too_long:
        print("Replacements longer than the text they replace will wrap and fragment:")
        for k, v in too_long.items():
            print(f"  {k!r} ({len(k)}) -> {v!r} ({len(v)})")
        sys.exit("Shorten them and re-run.")

    doc = pymupdf.open(args.source)

    if args.drop_pages:
        for index in sorted((n - 1 for n in args.drop_pages), reverse=True):
            doc.delete_page(index)
        print(f"Dropped page(s) {sorted(args.drop_pages)}; {doc.page_count} remain.\n")

    total = 0
    per_rule: dict[str, int] = {}
    for page in doc:
        for original, replacement in rules.items():
            for rect in page.search_for(original):
                rect.y0 += TOP_INSET_PT
                rect.y1 -= BOTTOM_INSET_PT
                # Size by WIDTH, not height. Height alone is not enough: a narrow
                # rect in a mailing-address block wrapped "JANE DOE" into "JA" / "NE",
                # fragmenting the text layer so the field no longer extracted. Measure
                # the replacement and shrink until it fits the box it has to live in.
                size = min(11.0, rect.height * 0.86)
                if replacement:
                    width = pymupdf.get_text_length(replacement, FONT, size)
                    if width > rect.width:
                        size *= rect.width / width * 0.97  # a hair under, for rounding
                    size = max(size, 3.0)
                page.add_redact_annot(
                    rect,
                    text=replacement,
                    fontsize=round(size, 1),
                    fill=FILL,
                    text_color=TEXT_COLOR,
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )
                per_rule[original] = per_rule.get(original, 0) + 1
                total += 1
        page.apply_redactions()

    # Document metadata is a separate leak path from page text, and a quiet one. This
    # statement carried the account number in /Info "author" as 04822863413 -- the same
    # digits as the account number on the page, minus the separators, so every grep for
    # the hyphenated form missed it. Producers routinely stash account and customer ids
    # here. Drop the whole dictionary rather than trying to sanitise it field by field.
    scrubbed = {k: v for k, v in (doc.metadata or {}).items() if v}
    doc.set_metadata({})
    doc.del_xml_metadata()
    if scrubbed:
        print("Cleared document metadata (values not printed): "
              f"{', '.join(sorted(scrubbed))}\n")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, garbage=4, deflate=True, clean=True)
    doc.close()

    print(f"{total} replacement(s) across {args.source.name}:")
    for original, count in per_rule.items():
        print(f"  {count:>3}  {original!r} -> {rules[original]!r}")
    missing = [r for r in rules if r not in per_rule]
    for original in missing:
        print(f"    0  {original!r}  NOT FOUND — check spelling and spacing")

    # The check that matters: is the original text actually gone from the file?
    verify = pymupdf.open(args.output)
    text = "\n".join(p.get_text() for p in verify)
    text += "\n" + "\n".join(str(v) for v in (verify.metadata or {}).values() if v)
    text += "\n" + (verify.get_xml_metadata() or "")
    verify.close()

    # Compare on digits alone as well as literally: an identifier is often stored
    # without its separators, which a literal check sails straight past.
    def _digits(value: str) -> str:
        return "".join(c for c in value if c.isdigit())

    text_digits = _digits(text)
    survivors = [
        r for r in rules
        if r in text or (len(_digits(r)) >= 6 and _digits(r) in text_digits)
    ]
    if survivors:
        print("\nFAILED — these strings are still extractable from the output:")
        for s in survivors:
            print(f"  {s!r}")
        sys.exit(1)
    print(f"\nVerified: no original string is extractable from {args.output.name}")

    # Clearing the PDF is only half the job. The rules file is a verbatim copy of the
    # personal data, and it is easy to "document the provenance" by pasting the same
    # before/after map into a manifest or README sitting next to the redacted PDF --
    # which republishes exactly what was just removed. This has happened once already.
    if _inside_repo(args.rules):
        print(f"\nWARNING: {args.rules} is inside the repo. It maps every original "
              f"string to its replacement, so it is the personal data in plain text. "
              f"Move it out before committing.")
    print("\nBefore committing, sweep the WHOLE output folder, not just the PDF:")
    print(f"    grep -ril <original> {args.output.parent.parent}")
    print("Record in the manifest only WHAT was replaced and with what -- never the "
          "original values.")


def _inside_repo(path: Path) -> bool:
    """True if path sits under the repository this script lives in."""
    repo = Path(__file__).resolve().parents[2]
    try:
        path.resolve().relative_to(repo)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
