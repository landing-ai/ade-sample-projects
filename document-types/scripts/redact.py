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
BOLD_FONT = "hebo"
MONO_FONT = "cour"
MONO_BOLD_FONT = "cobo"
BOLD_FLAG = 16  # PyMuPDF span flag for a bold font
MONO_FLAG = 8   # PyMuPDF span flag for a monospaced font
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
    parser.add_argument(
        "--remove-images", nargs="*", default=[], metavar="PAGE:X0,Y0,X1,Y1",
        help="Delete every image lying entirely inside this rectangle on this 1-indexed "
             "page (PDF points, after any --drop-pages). Use for a signature or a photo. "
             "Only wholly contained images go, so a watermark behind the area survives.",
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

    # Signatures arrive as images, which the text rules cannot touch. An offer letter's
    # signature sat over a corner of a full-page watermark: blanking the area would have
    # left a white patch on the watermark, and deleting every overlapping image would have
    # taken the watermark with it. So delete only images wholly inside the area.
    regions = [_parse_region(spec) for spec in args.remove_images]
    for page_no, region in regions:
        page = doc[page_no - 1]
        removed = [xref for xref, *_ in page.get_images(full=True)
                   if any(region.contains(r) for r in page.get_image_rects(xref))]
        for xref in removed:
            page.delete_image(xref)
        print(f"Removed {len(removed)} image(s) inside {tuple(region)} on page {page_no}.")

    total = 0
    per_rule: dict[str, int] = {}
    for page in doc:
        spans = [s for b in page.get_text("dict")["blocks"]
                 for l in b.get("lines", []) for s in l["spans"]]
        # A filled form types each value over a line of underscores, and the two overlap
        # completely, so redacting the value also takes the underscores beneath it: a
        # lease came back with gaps in the fill lines under the tenant and the address.
        # Remember every underscore now, and put back the ones a redaction removed.
        underscores = [(pymupdf.Rect(c["bbox"]), c["origin"], s["size"], s["color"])
                       for b in page.get_text("rawdict")["blocks"]
                       for l in b.get("lines", []) for s in l["spans"]
                       for c in s["chars"] if c["c"] == "_"]
        redacted: list[pymupdf.Rect] = []
        pending: list[tuple[pymupdf.Point, str, str, float]] = []
        for original, replacement in rules.items():
            for rect in _merge_line_rects(page.search_for(original)):
                # Match the text being replaced: its size, weight and baseline. Sizing
                # from the rect instead drew an 8.8pt bold name at 4.3pt regular, since
                # the inset rect is shorter than the line and the redaction annotation
                # shrinks its text until it fits -- an edit visible at a glance.
                span = _span_at(spans, rect)
                size = span["size"] if span else min(11.0, rect.height * 0.86)
                font = _replacement_font(span)
                baseline = span["origin"][1] if span else rect.y1 - rect.height * 0.2
                # Then size by WIDTH as well. A narrow rect in a mailing-address block
                # wrapped "JANE DOE" into "JA" / "NE", fragmenting the text layer so the
                # field no longer extracted. Shrink until it fits the original's width.
                if replacement:
                    width = pymupdf.get_text_length(replacement, font, size)
                    if width > rect.width:
                        size *= rect.width / width * 0.97  # a hair under, for rounding
                    size = max(size, 3.0)
                    pending.append((pymupdf.Point(rect.x0, baseline), replacement,
                                    font, round(size, 1)))
                # apply_redactions removes every character whose bbox touches the rect,
                # and a character's bbox is the font's full ascender-to-descender height,
                # so on an employment certificate the characters of the line below
                # overlapped the name's rect and "2017 and is currently designa" was
                # erased. Removal is by overlap, so when the span is known a band through
                # the middle of the letters takes every character of the match while
                # staying clear of neighbouring lines. The band replaces the fixed insets
                # rather than following them: on a lease's 2pt "Prepared by" line the
                # insets alone emptied the rect, and the agent's name survived.
                if span:
                    rect.y0 = baseline - span["size"] * 0.6
                    rect.y1 = baseline - span["size"] * 0.1
                else:
                    rect.y0 += TOP_INSET_PT
                    rect.y1 -= BOTTOM_INSET_PT
                page.add_redact_annot(rect, fill=FILL)
                redacted.append(pymupdf.Rect(rect))
                per_rule[original] = per_rule.get(original, 0) + 1
                total += 1
        page.apply_redactions()
        # Only the ones actually removed: some touch a rect and survive, and drawing
        # those again left a stray raised underscore beside the tenant's name.
        survivors = {(round(c["origin"][0], 1), round(c["origin"][1], 1))
                     for b in page.get_text("rawdict")["blocks"]
                     for l in b.get("lines", []) for s in l["spans"]
                     for c in s["chars"] if c["c"] == "_"}
        for bbox, origin, size, color in underscores:
            gone = (round(origin[0], 1), round(origin[1], 1)) not in survivors
            if gone and any(bbox.intersects(r) for r in redacted):
                rgb = tuple(((color >> shift) & 0xFF) / 255 for shift in (16, 8, 0))
                page.insert_text(origin, "_", fontname=FONT, fontsize=size, color=rgb)
        # Written after the redaction, not as the annotation's text, so the replacement
        # sits on the original baseline at the original size instead of being fitted
        # into the trimmed rect.
        for point, text, font, size in pending:
            page.insert_text(point, text, fontname=font, fontsize=size, color=TEXT_COLOR)

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

    if regions:
        # delete_image leaves a 1x1 blank image in the deleted one's place, so an image
        # counts as surviving only if it still has real pixels.
        verify = pymupdf.open(args.output)
        left = [(n, xref) for n, region in regions
                for xref, _, w, h, *_ in verify[n - 1].get_images(full=True)
                if w * h > 1
                and any(region.contains(r) for r in verify[n - 1].get_image_rects(xref))]
        verify.close()
        if left:
            sys.exit(f"FAILED — images still inside a removed region: {left}")
        print("Verified: no image remains inside a removed region.")

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


def _replacement_font(span: dict | None) -> str:
    """A base-14 font matching the replaced span's weight and, for monospace, its family.

    A pay stub set in Courier had its name replaced in Helvetica, which reads as an edit
    among fixed-width text. Its regular Courier spans do not set the monospace flag, so
    the font name is checked as well.
    """
    if not span:
        return FONT
    bold = bool(span["flags"] & BOLD_FLAG)
    mono = bool(span["flags"] & MONO_FLAG) or "courier" in span["font"].lower()
    if mono:
        return MONO_BOLD_FONT if bold else MONO_FONT
    return BOLD_FONT if bold else FONT


def _merge_line_rects(rects: list[pymupdf.Rect]) -> list[pymupdf.Rect]:
    """Join the per-word rects search_for returns for one match on a justified line.

    On a justified line the spaces are wider than the font's own, and search_for returns
    one rect per word. An employment certificate's name came back as three rects, and
    each got its own copy of the replacement, drawn on top of one another. Consecutive
    rects on the same line with no more than a line-height's gap belong to one match.
    """
    merged: list[pymupdf.Rect] = []
    for rect in rects:
        last = merged[-1] if merged else None
        same_line = last is not None and abs(rect.y0 - last.y0) < 1 and abs(rect.y1 - last.y1) < 1
        if same_line and 0 <= rect.x0 - last.x1 <= rect.height:
            last.include_rect(rect)
        else:
            merged.append(pymupdf.Rect(rect))
    return merged


def _span_at(spans: list[dict], rect: pymupdf.Rect) -> dict | None:
    """The text span a search hit sits in: the one its rect overlaps most."""
    best, best_area = None, 0.0
    for span in spans:
        overlap = rect & pymupdf.Rect(span["bbox"])
        area = overlap.get_area() if not overlap.is_empty else 0.0
        if area > best_area:
            best, best_area = span, area
    return best


def _parse_region(spec: str) -> tuple[int, pymupdf.Rect]:
    """'4:50,332,131,373' -> (4, Rect(50, 332, 131, 373))."""
    try:
        page, coords = spec.split(":")
        x0, y0, x1, y1 = (float(v) for v in coords.split(","))
    except ValueError:
        sys.exit(f"--remove-images expects PAGE:X0,Y0,X1,Y1, got {spec!r}")
    return int(page), pymupdf.Rect(x0, y0, x1, y1)


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
