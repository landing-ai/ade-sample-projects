#!/usr/bin/env python3
"""Replace personal data in a PDF whose text has been converted to vector outlines.

    python document-types/scripts/redact_outlined.py in.pdf out.pdf --rules rules.json

`redact.py` finds strings through the PDF's text layer. Some producers -- "Microsoft:
Print To PDF" among them -- emit every glyph as a filled path instead, so the page reads
as text but has no text layer: `search_for` finds nothing and every rule silently misses.

This locates each string with Tesseract OCR on a page rendering, snaps the hit to the
glyph paths underneath it, and removes those paths with a PyMuPDF redaction annotation
(line art removed if covered). That deletes the glyphs from the content stream, rather
than painting over them, which would leave them in the file. The replacement is drawn in
Helvetica at the size and baseline of the glyphs it replaces.

`--rules` is the same JSON as `redact.py`, and the same warning applies: it pairs every
original with its replacement, so it is the personal data in plain text. Keep it OUTSIDE
the repo.

Matching ignores case and punctuation, so `Smith,` matches the rule `Smith` and the
comma is kept. A hit must start and end on a word boundary, so the rule `123` does not
fire inside `9990123`; a boundary includes punctuation inside a token, so
`ABC-12345678` is found inside a printed URL.

After writing, it OCRs every page again and fails loudly if any original survives --
compared as literals and, for anything with five or more digits, as bare digits.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import statistics
import subprocess
import sys
from pathlib import Path

import pymupdf

DPI = 300
SCALE = 72 / DPI
FILL = (1, 1, 1)
TEXT_COLOR = (0, 0, 0)
# Arial / Helvetica cap height as a fraction of the em. Glyph boxes give cap height in
# points; dividing by this gives the font size that reproduces it.
CAP_HEIGHT_EM = 0.716
# Width cannot tell bold from regular: digits are the same width in both. Ink density
# can -- the share of dark pixels in the glyphs' bounding box. On the title commitment a
# bold number measured 0.46 and the same number in regular 0.33; mixed-case text sits
# lower still (~0.23) because of ascender and descender space. Calibrated on one
# document: check the bold/regular choice by eye on anything new.
BOLD_DENSITY = 0.40
SNAP_PAD_PT = 0.3


def ocr_lines(page: pymupdf.Page) -> list[list[dict]]:
    """Words grouped by line, each with its raw text and a rect in PDF points."""
    png = page.get_pixmap(dpi=DPI).tobytes("png")
    out = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "4", "tsv"],
                         input=png, capture_output=True, check=True).stdout.decode()
    lines: dict[tuple, list[dict]] = {}
    for row in csv.DictReader(io.StringIO(out), delimiter="\t", quoting=csv.QUOTE_NONE):
        text = (row.get("text") or "").strip()
        if row["level"] != "5" or not text:
            continue
        x, y, w, h = (int(row[k]) for k in ("left", "top", "width", "height"))
        rect = pymupdf.Rect(x, y, x + w, y + h) * SCALE
        lines.setdefault((row["block_num"], row["par_num"], row["line_num"]), []).append(
            {"text": text, "rect": rect})
    return list(lines.values())


def _norm(s: str) -> str:
    return "".join(c.lower() for c in s if c.isalnum())


def _occurrences(words: list[dict], target: str) -> list[tuple]:
    """Word-bounded occurrences of a normalized `target` in one line, as
    (first char, last char, starts the line, ends the line); chars are (word, index)."""
    raw = " ".join(w["text"] for w in words)
    stream = [(c.lower(), i) for i, c in enumerate(raw) if c.isalnum()]
    flat = "".join(c for c, _ in stream)
    owner = []
    for wi, w in enumerate(words):
        owner += [(wi, k) for k in range(len(w["text"]))] + [(wi, None)]
    found = []
    start = flat.find(target) if target else -1
    while start != -1:
        a, b = stream[start][1], stream[start + len(target) - 1][1]
        if (a == 0 or not raw[a - 1].isalnum()) and \
           (b == len(raw) - 1 or not raw[b + 1].isalnum()):
            found.append((owner[a], owner[b], start == 0, start + len(target) == len(flat)))
        start = flat.find(target, start + 1)
    return found


def find(lines: list[list[dict]], original: str, replacement: str) -> list[list[tuple]]:
    """Every occurrence of `original`, each as [(rect in PDF points, text to draw,
    the part of the original it covers)].

    One pair for an occurrence on a single line; two when it wraps onto the next line
    ("... Debtor: John" / "Henry Smith;"), with the replacement split the same
    way, so the wrapped half is not left behind."""
    hits = []
    for words in lines:
        for first, last, _, _ in _occurrences(words, _norm(original)):
            hits.append([(_span_rect(words, first, last), replacement, original)])

    tokens, rep = original.split(), replacement.split()
    for upper, lower in zip(lines, lines[1:]):
        for k in range(1, len(tokens)):
            head = [o for o in _occurrences(upper, _norm(" ".join(tokens[:k]))) if o[3]]
            tail = [o for o in _occurrences(lower, _norm(" ".join(tokens[k:]))) if o[2]]
            if head and tail:
                cut = max(1, min(k, len(rep) - 1))
                hits.append([(_span_rect(upper, *head[-1][:2]), " ".join(rep[:cut]),
                              " ".join(tokens[:k])),
                             (_span_rect(lower, *tail[0][:2]), " ".join(rep[cut:]),
                              " ".join(tokens[k:]))])
    return hits


def _span_rect(words, first, last) -> pymupdf.Rect:
    """Rect from char `first` to char `last` (inclusive), interpolating inside a word
    by Helvetica advance widths -- close enough, since it is snapped to glyphs next."""
    def x_at(wi, k, end):
        w = words[wi]
        full = pymupdf.get_text_length(w["text"], "helv", 10) or 1
        part = pymupdf.get_text_length(w["text"][: k + (1 if end else 0)], "helv", 10)
        return w["rect"].x0 + w["rect"].width * part / full
    (fw, fk), (lw, lk) = first, last
    span = words[fw: lw + 1]
    return pymupdf.Rect(x_at(fw, fk, False), min(w["rect"].y0 for w in span),
                        x_at(lw, lk, True), max(w["rect"].y1 for w in span))


def _density(page: pymupdf.Page, rect: pymupdf.Rect) -> float:
    """Share of dark pixels in `rect`, rendered at 600 dpi."""
    pix = page.get_pixmap(dpi=600, clip=rect, colorspace=pymupdf.csGRAY)
    return sum(1 for b in pix.samples if b < 128) / max(1, len(pix.samples))


def snap(glyphs: list[pymupdf.Rect], rect: pymupdf.Rect) -> list[pymupdf.Rect]:
    """Glyph paths whose centre lies inside the OCR rect."""
    probe = pymupdf.Rect(rect.x0 - 0.4, rect.y0 - 1, rect.x1 + 0.4, rect.y1 + 1)
    return [g for g in glyphs if probe.contains(pymupdf.Point((g.x0 + g.x1) / 2,
                                                              (g.y0 + g.y1) / 2))]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--drop-pages", type=int, nargs="*", default=[],
                        help="1-indexed pages to remove entirely, before matching.")
    parser.add_argument("--verify-also", nargs="*", default=[],
                        help="Extra strings that must not survive, such as a surname "
                             "that only ever appears inside a longer rule.")
    args = parser.parse_args()

    # A rule's value is the replacement, or {"with": ..., "font": ...} to force a
    # PyMuPDF base-14 font -- "hebi" for a bold italic link, which density cannot see.
    raw_rules = json.loads(args.rules.read_text(encoding="utf-8"))
    rules = {k: v["with"] if isinstance(v, dict) else v for k, v in raw_rules.items()}
    forced = {k: v["font"] for k, v in raw_rules.items() if isinstance(v, dict) and "font" in v}
    too_long = {k: v for k, v in rules.items() if len(v) > len(k)}
    if too_long:
        sys.exit(f"Replacements longer than their originals: {sorted(too_long)}")

    doc = pymupdf.open(args.source)
    for index in sorted((n - 1 for n in args.drop_pages), reverse=True):
        doc.delete_page(index)
    if args.drop_pages:
        print(f"Dropped page(s) {sorted(args.drop_pages)}; {doc.page_count} remain.\n")

    # Longest first, so "John Henry Smith" is taken before any shorter rule
    # could claim part of it.
    ordered = sorted(rules, key=len, reverse=True)
    counts = {k: 0 for k in rules}

    for page in doc:
        lines = ocr_lines(page)
        glyphs = [d["rect"] for d in page.get_drawings() if d["rect"].width < 40]
        taken: list[pymupdf.Rect] = []
        pending = []
        for original in ordered:
            for occurrence in find(lines, original, rules[original]):
                for rect, text, covered in occurrence:
                    hit = [g for g in snap(glyphs, rect) if not any(g in t for t in taken)]
                    if not hit:
                        print(f"  page {page.number + 1}: a rule matched by OCR but no "
                              f"glyphs lie under it -- skipped")
                        continue
                    ink = pymupdf.Rect(hit[0])
                    for g in hit[1:]:
                        ink |= g
                    baseline = statistics.median(g.y1 for g in hit)
                    size = (baseline - ink.y0) / CAP_HEIGHT_EM
                    font = forced.get(original) or (
                        "hebo" if _density(page, ink) > BOLD_DENSITY else "helv")
                    # The source font sets ~5% narrower than Helvetica. Scale the
                    # replacement horizontally by the same ratio, or a same-length
                    # number runs into the word after it.
                    squeeze = ink.width / pymupdf.get_text_length(covered, font, size)
                    # A replacement with fewer characters can still set wider ("Mmmm"
                    # against "Illinois") and would overprint the next word. Squeeze it
                    # into the space instead, and say so when that becomes visible.
                    fit = ink.width / pymupdf.get_text_length(text, font, size)
                    if fit < squeeze:
                        squeeze = fit
                        if fit < 0.88:
                            print(f"  page {page.number + 1}: {text!r} squeezed to "
                                  f"{fit:.0%} to fit -- choose a narrower replacement")
                    if os.environ.get("REDACT_DEBUG"):
                        print(f"    p{page.number + 1} {font} size={size:.1f} "
                              f"squeeze={squeeze:.3f} {text!r}")
                    box = pymupdf.Rect(ink.x0 - SNAP_PAD_PT, ink.y0 - SNAP_PAD_PT,
                                       ink.x1 + SNAP_PAD_PT, ink.y1 + SNAP_PAD_PT)
                    page.add_redact_annot(box, fill=FILL)
                    taken.append(box)
                    pending.append((pymupdf.Point(ink.x0, baseline), text, font,
                                    round(size, 1), squeeze))
                    counts[original] += 1
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        for point, text, font, size, squeeze in pending:
            page.insert_text(point, text, fontname=font, fontsize=size, color=TEXT_COLOR,
                             morph=(point, pymupdf.Matrix(squeeze, 1)))

    doc.set_metadata({})
    doc.del_xml_metadata()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output, garbage=4, deflate=True, clean=True)

    print("Replacements per rule (originals not shown):")
    for i, original in enumerate(rules, 1):
        print(f"  rule {i:>2} -> {rules[original]!r}: {counts[original]}")

    # Verify on a fresh open, by OCR, as literals and as bare digits.
    check = pymupdf.open(args.output)
    terms = list(rules) + args.verify_also
    failures = []
    for page in check:
        text = " ".join(w["text"] for line in ocr_lines(page) for w in line)
        flat, digits = _norm(text), "".join(c for c in text if c.isdigit())
        for term in terms:
            d = "".join(c for c in term if c.isdigit())
            if _norm(term) in flat or (len(d) >= 5 and d in digits):
                failures.append((page.number + 1, terms.index(term) + 1))
    meta = {k: v for k, v in check.metadata.items() if v and k not in ("format",)}
    if meta:
        failures.append(("metadata", sorted(meta)))
    if failures:
        sys.exit(f"FAILED: originals survive (page, term #): {failures}")
    print(f"\nVerified: no original survives in {args.output} (OCR, literals and digits);"
          f" metadata cleared.")


if __name__ == "__main__":
    main()
