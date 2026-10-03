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
import pdfmeta  # noqa: E402
from redact_outlined import _norm, find  # noqa: E402

DPI = 300
DEFAULT_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
DEFAULT_BOLD_FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
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
    def ok(w):
        return (not (set(w["text"]) & DESCENDERS)
                and any(c.isupper() or c.isdigit() for c in w["text"]))
    # Prefer the line's OTHER words: a highlighter stroke over the hit makes its own
    # OCR boxes taller than the type, which drew a replacement half again too large.
    others = [w["rect"] for w in words if ok(w) and overlap(w["rect"], rect) < 0.3]
    inside = [w["rect"] for w in words if ok(w)]
    clean = others if len(others) >= 2 else inside
    if clean:
        return (statistics.median(r.height for r in clean),
                statistics.median(r.y1 for r in clean))
    return rect.height * 0.8, rect.y1 - rect.height * 0.2


def background(image: Image.Image, box: tuple) -> tuple:
    """The tone to paint over `box` with: the non-ink pixels inside the box itself, so
    text under a highlighter is patched in the highlighter's colour, falling back to a
    ring around it. Near-white paper takes the 90th percentile, not the median: paper
    beside ink is pulled a level or two darker by scanner blur and JPEG ringing, and a
    patch even one level darker than the page shows as a faint rectangle."""
    inside = [p for p in pixels(image.crop(box)) if sum(p) >= 3 * PAPER]
    if len(inside) < 50:
        ring = image.crop((box[0] - 12, box[1] - 12, box[2] + 12, box[3] + 12))
        inside = [p for p in pixels(ring) if sum(p) >= 3 * PAPER] or [(255, 255, 255)]
    median = tuple(int(statistics.median(c[i] for c in inside)) for i in range(3))
    if min(median) >= 245:
        return tuple(sorted(c[i] for c in inside)[int(len(inside) * 0.9)] for i in range(3))
    return median


def overlap(a: pymupdf.Rect, b: pymupdf.Rect) -> float:
    """Share of `a`'s area that `b` covers."""
    inter = pymupdf.Rect(a) & b
    return 0.0 if inter.is_empty else inter.get_area() / max(a.get_area(), 1)


def carry_punctuation(words: list[dict], rect: pymupdf.Rect, text: str, covered: str):
    """Extend a hit over the punctuation that ends its last word ("JR.;"), and append
    that punctuation to the replacement. Otherwise a shorter stand-in leaves the
    original's ".;" stranded after a gap, reading as a stray mark."""
    last = next((w for w in words if w["rect"].x0 < rect.x1 - 1 <= w["rect"].x1
                 and w["rect"].intersects(rect)), None)
    if not last:
        return rect, text, covered
    raw = last["text"]
    tail = raw[len(raw.rstrip(".,;:")):]
    if tail and last["rect"].x1 - rect.x1 > 1:
        rect = pymupdf.Rect(rect.x0, rect.y0, last["rect"].x1, rect.y1)
        text, covered = text + tail, covered + tail
    return rect, text, covered


def match_case(replacement: str, printed: str) -> str:
    """Rules are written once, in capitals; a hit printed in mixed case ("Doe, Jr.")
    gets its replacement in title case, keeping initials and number-letter codes."""
    letters = [c for c in printed if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) / len(letters) > 0.7:
        return replacement
    def title(word: str) -> str:
        core = word.rstrip(".,;:")
        return core.capitalize() + word[len(core):] if core.isalpha() and len(core) > 1 else word
    return " ".join(title(w) for w in replacement.split(" "))


def erase(image: Image.Image, spec: str, font_path: str | None) -> None:
    """Paint over a region given in PDF points, `x0,y0,x1,y1`, and optionally redraw a
    stand-in inside it (`...=Jonah Q Sample`) in a handwriting font, in the region's own
    ink colour: a signature or initials that OCR cannot read and rules cannot match."""
    coords, _, text = spec.partition("=")
    x0, y0, x1, y1 = (float(v) * DPI / 72 for v in coords.split(","))
    box = (int(x0), int(y0), int(x1), int(y1))
    region = image.crop(box)
    ink_px = [p for p, g in zip(pixels(region), pixels(region.convert("L"))) if g < DARK]
    ink = tuple(int(statistics.median(c[i] for c in ink_px)) for i in range(3)) if ink_px else (40, 40, 60)
    if text == "__":   # a rule line the erase above it had to cut: redraw it in its ink
        ImageDraw.Draw(image).rectangle(box, fill=ink)
        return
    ImageDraw.Draw(image).rectangle(box, fill=background(image, box))
    if text and font_path:
        height = (box[3] - box[1]) * 0.7
        font = ImageFont.truetype(font_path, max(8, int(height)))
        while font.getlength(text) > (box[2] - box[0]) * 0.95 and font.size > 8:
            font = ImageFont.truetype(font_path, font.size - 2)
        glyphs = Image.new("L", image.size, 0)
        ImageDraw.Draw(glyphs).text((box[0] + 4, box[1] + (box[3] - box[1] - font.size) / 2),
                                    text, font=font, fill=255)
        image.paste(Image.new("RGB", image.size, ink), (0, 0), glyphs.filter(ImageFilter.GaussianBlur(0.7)))


def ink_metrics(image: Image.Image, rect: pymupdf.Rect) -> tuple[float, float] | None:
    """(cap height, baseline) in pixels, measured from the hit's own ink: the rows that
    carry at least a fifth of the busiest row's dark pixels span cap top (or ascender) to
    baseline, while descenders, a neighbouring line's tails and highlighter fall below
    that. OCR boxes proved too loose for this -- a word alone on its line, or under a
    highlighter, drew its replacement half again too large."""
    box = (int(rect.x0), int(rect.y0) - 2, int(rect.x1), int(rect.y1) + 2)
    grey = image.crop(box).convert("L")
    w, h = grey.size
    data = pixels(grey)
    rows = [sum(1 for x in range(w) if data[y * w + x] < DARK) for y in range(h)]
    peak = max(rows, default=0)
    if peak == 0:
        return None
    # On single-spaced lines one OCR box can take in the line above or below as well;
    # split the busy rows into contiguous bands and keep the one with the most ink.
    bands, run = [], []
    for y, n in enumerate(rows):
        if n >= peak * 0.2:
            run.append(y)
        elif run:
            bands.append(run); run = []
    if run:
        bands.append(run)
    band = max(bands, key=lambda b: sum(rows[y] for y in b))
    # In mixed case the busy band is the x-height: capitals and ascenders are too thin
    # to clear the threshold. Climb from the band's top through any ink at all, up to
    # the band's own height again, so the stand-in is sized to the capitals and the
    # paint reaches their tops. Without this, "Name, Jr." came back half size, with
    # the original's capitals left as specks above it.
    top, limit = band[0], max(0, band[0] - len(band))
    while top > limit and rows[top - 1] > 0:
        top -= 1
    return band[-1] - top + 1, box[1] + band[-1] + 1


def paint(image: Image.Image, rect: pymupdf.Rect, text: str, covered: str,
          cap_h: float, baseline: float, font_path: str) -> None:
    box = (int(rect.x0) - PAD_PX, int(rect.y0) - PAD_PX,
           int(rect.x1) + PAD_PX, int(rect.y1) + PAD_PX)
    region = image.crop(box)
    grey = region.convert("L")
    ink_px = [p for p, g in zip(pixels(region), pixels(grey)) if g < DARK]
    ink = tuple(int(statistics.median(c[i] for c in ink_px)) for i in range(3)) if ink_px else (30, 30, 30)

    bg = background(image, box)
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
    parser.add_argument("--bold", nargs="*", default=[], metavar="PAGE:RULE",
                        help="Set this rule's replacement in --bold-font on this source page. "
                             "Explicit, because stroke weight on small scanned type did not "
                             "separate bold from regular reliably: a bold address measured "
                             "only 1.08x the stroke of its regular neighbours.")
    parser.add_argument("--bold-font", default=DEFAULT_BOLD_FONT,
                        help="TrueType bold font for --bold hits (default: Arial Bold)")
    parser.add_argument("--erase", nargs="*", default=[], metavar="PAGE:X0,Y0,X1,Y1[=TEXT]",
                        help="Paint over a region of a source page, in PDF points on the "
                             "upright page, and optionally redraw TEXT there in "
                             "--handwriting-font. For signatures and initials.")
    parser.add_argument("--handwriting-font", type=Path, metavar="FONT.ttf",
                        help="Openly licensed handwriting font for --erase stand-ins "
                             "(document-types/scripts/fonts/IndieFlower-Regular.ttf).")
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
    bold = {(int(n), r) for n, _, r in (spec.partition(":") for spec in args.bold)}
    unknown = {r for _, r in bold} - set(rules)
    if unknown:
        sys.exit(f"--bold names rules that are not in --rules: {sorted(unknown)}")
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
                    # Skip only a real overlap with something already painted: OCR boxes
                    # on single-spaced lines touch by a pixel, and treating that as a
                    # collision left the wrapped half of a name behind.
                    if any(overlap(rect, t) > 0.5 for t in taken):
                        continue
                    words = max(lines, key=lambda l: sum(
                        (pymupdf.Rect(w["rect"]) & rect).get_area()
                        for w in l if w["rect"].intersects(rect)), default=[])
                    rect, text, covered = carry_punctuation(words, rect, text, covered)
                    font = args.bold_font if (number, original) in bold else args.font
                    cap_h, baseline = ink_metrics(image, rect) or line_metrics(words, rect)
                    # Paint only this line's band, so a box that strays into the next
                    # line does not take its tops or tails with it.
                    rect = pymupdf.Rect(rect.x0, max(rect.y0, baseline - cap_h * 1.2),
                                        rect.x1, min(rect.y1, baseline + cap_h * 0.35))
                    printed = " ".join(w["text"] for w in words if w["rect"].intersects(rect))
                    paint(image, rect, match_case(text, printed), covered, cap_h, baseline,
                          font)
                    taken.append(pymupdf.Rect(rect))
                    counts[original] += 1
        for spec in args.erase:
            page_no, _, region = spec.partition(":")
            if int(page_no) == number:
                erase(image, region, str(args.handwriting_font) if args.handwriting_font else None)
        # A fresh page from the edited pixels alone, at the rendered page's own size.
        width, height = page.rect.width, page.rect.height
        new = out.new_page(width=width, height=height)
        buf = io.BytesIO()
        image.save(buf, "JPEG", quality=JPEG_QUALITY)
        new.insert_image(new.rect, stream=buf.getvalue())

    pdfmeta.clear(out)
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
    if pdfmeta.remaining(check):
        failures.append(("metadata", pdfmeta.remaining(check)))
    if failures:
        sys.exit(f"FAILED: originals survive (page, term #): {failures}")
    print(f"\nVerified: no original survives in {args.output} (OCR, literals and digits);"
          f" metadata cleared.")


if __name__ == "__main__":
    main()
