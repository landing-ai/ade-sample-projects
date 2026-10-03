#!/usr/bin/env python3
"""Replace personal data in a scanned PDF -- page images with no text layer.

    python document-types/scripts/redact_scan.py in.pdf out.pdf --rules rules.json

The third redaction route, beside `redact.py` (text layer) and `redact_outlined.py`
(vector glyphs). A scan is one raster image per page: there is no text to remove and no
path to delete, so the replacement has to happen in the pixels.

Each page is rendered upright at 300 dpi, located with Tesseract OCR through the same
matcher as `redact_outlined.py` (word-bounded, punctuation-blind, across line breaks),
and every hit is painted over with the page's background and redrawn in a stand-in font
at the original's cap height, ink colour and set width. The page is then rebuilt from the
edited image alone: the original raster is not carried into the output, so nothing under
the paint survives, and neither does the source's /Rotate or any hidden layer.

`--rules` is the same JSON as the other two scripts, with the same warning: it pairs every
original with its replacement, so keep it OUTSIDE the repo.

After writing, it OCRs every output page and fails loudly if any original survives --
compared as literals and, for anything with five or more digits, as bare digits.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import statistics
import subprocess
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redact_outlined import _norm, find  # noqa: E402

DPI = 300
DEFAULT_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
DARK = 140          # grey level below which a pixel counts as ink
PAPER = 200         # grey level above which a pixel counts as paper
PAD_PX = 4          # paint this far beyond the OCR box, to catch anti-aliased edges
DESCENDERS = set("gjpqy,;")
JPEG_QUALITY = 88   # a scan was a JPEG to begin with; PNG would triple the file


def pixels(image: Image.Image) -> list:
    """Every pixel value, row by row (getdata() is deprecated from Pillow 12)."""
    flat = getattr(image, "get_flattened_data", None)
    return list(flat() if flat else image.getdata())


def render(page: pymupdf.Page) -> Image.Image:
    pix = page.get_pixmap(dpi=DPI)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def ocr_lines(image: Image.Image) -> list[list[dict]]:
    """Words grouped by line, each with its text and a rect in pixels."""
    buf = io.BytesIO()
    image.save(buf, "PNG")
    out = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "4", "tsv"],
                         input=buf.getvalue(), capture_output=True, check=True).stdout.decode()
    lines: dict[tuple, list[dict]] = {}
    for row in csv.DictReader(io.StringIO(out), delimiter="\t", quoting=csv.QUOTE_NONE):
        text = (row.get("text") or "").strip()
        if row["level"] != "5" or not text:
            continue
        x, y, w, h = (int(row[k]) for k in ("left", "top", "width", "height"))
        lines.setdefault((row["block_num"], row["par_num"], row["line_num"]), []).append(
            {"text": text, "rect": pymupdf.Rect(x, y, x + w, y + h)})
    return list(lines.values())


def line_metrics(words: list[dict], rect: pymupdf.Rect) -> tuple[float, float]:
    """(cap height, baseline) in pixels for the line a hit sits on, from its words that
    have capitals or digits and no descenders -- their boxes run cap top to baseline."""
    line = [w for w in words if w["rect"].intersects(rect) or abs(w["rect"].y1 - rect.y1) < 12]
    clean = [w["rect"] for w in line
             if not (set(w["text"]) & DESCENDERS)
             and any(c.isupper() or c.isdigit() for c in w["text"])]
    if clean:
        return (statistics.median(r.height for r in clean),
                statistics.median(r.y1 for r in clean))
    return rect.height * 0.8, rect.y1 - rect.height * 0.2


def paint(image: Image.Image, rect: pymupdf.Rect, text: str, covered: str,
          cap_h: float, baseline: float, font_path: str) -> None:
    box = (int(rect.x0) - PAD_PX, int(rect.y0) - PAD_PX,
           int(rect.x1) + PAD_PX, int(rect.y1) + PAD_PX)
    region = image.crop(box)
    grey = region.convert("L")
    ink_px = [p for p, g in zip(pixels(region), pixels(grey)) if g < DARK]
    ink = tuple(int(statistics.median(c[i] for c in ink_px)) for i in range(3)) if ink_px else (30, 30, 30)

    # Background: the paper's own tone around the box, taken from non-ink pixels only,
    # so a cream or grey scan is not patched with pure white and ink never darkens it.
    ring = image.crop((box[0] - 12, box[1] - 12, box[2] + 12, box[3] + 12))
    paper = [p for p in pixels(ring) if sum(p) >= 3 * PAPER] or [(255, 255, 255)]
    # The 90th percentile, not the median: paper near ink is pulled a level or two
    # darker by scanner blur and JPEG ringing, and a patch even one level darker than
    # the paper around it shows as a faint rectangle.
    bg = tuple(sorted(c[i] for c in paper)[int(len(paper) * 0.9)] for i in range(3))
    ImageDraw.Draw(image).rectangle(box, fill=bg)

    # Size the font so a capital is as tall as the original's, then compress it
    # horizontally to the original's set width per character (scanned Calibri runs
    # narrower than Arial), and never wider than the space the original occupied.
    probe = ImageFont.truetype(font_path, 100)
    cap = probe.getbbox("H")
    size = max(6, round(100 * cap_h / (cap[3] - cap[1])))
    font = ImageFont.truetype(font_path, size)
    natural = font.getlength(covered) or 1
    squeeze = min(rect.width / natural, 1.15)
    width = font.getlength(text) * squeeze
    if width > rect.width:
        squeeze *= rect.width / width
    ascent, descent = font.getmetrics()
    glyphs = Image.new("L", (int(font.getlength(text)) + 4, ascent + descent + 4), 0)
    ImageDraw.Draw(glyphs).text((2, 2), text, font=font, fill=255)
    glyphs = glyphs.resize((max(1, int(glyphs.width * squeeze)), glyphs.height), Image.LANCZOS)
    glyphs = glyphs.filter(ImageFilter.GaussianBlur(0.6))   # a scan is never crisp
    top = int(baseline - ascent - 2)
    image.paste(Image.new("RGB", glyphs.size, ink), (int(rect.x0), top), glyphs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--pages", type=int, nargs="*",
                        help="1-indexed pages of the source to keep, in order (default: all)")
    parser.add_argument("--font", default=DEFAULT_FONT,
                        help="TrueType font for the replacements (default: Arial)")
    parser.add_argument("--verify-also", nargs="*", default=[],
                        help="Extra strings that must not survive, such as a surname "
                             "that only ever appears inside a longer rule.")
    args = parser.parse_args()

    rules: dict[str, str] = json.loads(args.rules.read_text(encoding="utf-8"))
    too_long = {k for k, v in rules.items() if len(v) > len(k)}
    if too_long:
        sys.exit(f"Replacements longer than their originals: {sorted(too_long)}")

    source = pymupdf.open(args.source)
    pages = args.pages or list(range(1, source.page_count + 1))
    ordered = sorted(rules, key=len, reverse=True)
    counts = {k: 0 for k in rules}
    out = pymupdf.open()

    for number in pages:
        page = source[number - 1]
        image = render(page)
        lines = ocr_lines(image)
        taken: list[pymupdf.Rect] = []
        for original in ordered:
            for occurrence in find(lines, original, rules[original]):
                for rect, text, covered in occurrence:
                    if any(rect.intersects(t) for t in taken):
                        continue
                    words = next((l for l in lines if any(w["rect"].intersects(rect) for w in l)), [])
                    cap_h, baseline = line_metrics(words, rect)
                    paint(image, rect, text, covered, cap_h, baseline, args.font)
                    taken.append(pymupdf.Rect(rect))
                    counts[original] += 1
        # A fresh page from the edited pixels alone, at the rendered page's own size.
        width, height = page.rect.width, page.rect.height
        new = out.new_page(width=width, height=height)
        buf = io.BytesIO()
        image.save(buf, "JPEG", quality=JPEG_QUALITY)
        new.insert_image(new.rect, stream=buf.getvalue())

    out.set_metadata({})
    out.del_xml_metadata()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output, garbage=4, deflate=True, clean=True)

    print(f"Kept page(s) {pages} of {source.page_count}.")
    print("Replacements per rule (originals not shown):")
    for i, original in enumerate(rules, 1):
        print(f"  rule {i:>2} -> {rules[original]!r}: {counts[original]}")

    check = pymupdf.open(args.output)
    terms = list(rules) + args.verify_also
    failures = []
    for page in check:
        text = " ".join(w["text"] for line in ocr_lines(render(page)) for w in line)
        flat, digits = _norm(text), "".join(c for c in text if c.isdigit())
        for i, term in enumerate(terms, 1):
            d = "".join(c for c in term if c.isdigit())
            if _norm(term) in flat or (len(d) >= 5 and d in digits):
                failures.append((page.number + 1, i))
    meta = {k: v for k, v in check.metadata.items() if v and k != "format"}
    if meta:
        failures.append(("metadata", sorted(meta)))
    if failures:
        sys.exit(f"FAILED: originals survive (page, term #): {failures}")
    print(f"\nVerified: no original survives in {args.output} (OCR, literals and digits);"
          f" metadata cleared.")


if __name__ == "__main__":
    main()
