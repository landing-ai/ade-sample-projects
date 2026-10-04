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
import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdfmeta  # noqa: E402

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
ITALIC_FONT = "heit"
BOLD_ITALIC_FONT = "hebi"
MONO_FONT = "cour"
MONO_BOLD_FONT = "cobo"
BOLD_FLAG = 16  # PyMuPDF span flag for a bold font
MONO_FLAG = 8   # PyMuPDF span flag for a monospaced font
ITALIC_FLAG = 2  # PyMuPDF span flag for an italic font
# Typed e-signatures are set in handwriting fonts. Replacing one in Helvetica turns a
# signature into a printed name, which on a lease erased the evidence that it was signed.
HANDWRITING_HINTS = ("hand", "script", "brush", "signature", "cursive", "bradley", "autograph")
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
    parser.add_argument(
        "--remove-marks", nargs="*", default=[], metavar="PAGE:X0,Y0,X1,Y1",
        help="Delete text and vector paths inside this rectangle, drawing nothing in their "
             "place. Use for a mailing barcode, which may be set in a barcode font or drawn "
             "as bars, and for rotated reference text. Paths only partly inside survive, so "
             "a background behind the area is kept; text touching the area does not, so "
             "keep the rectangle tight.",
    )
    parser.add_argument(
        "--draw-signature", nargs="*", default=[], metavar="PAGE:X0,Y0,X1,Y1=TEXT",
        help="Write TEXT in --handwriting-font inside this rectangle, as a stand-in for a "
             "signature removed with --remove-images. Sized to fit the rectangle.",
    )
    parser.add_argument(
        "--handwriting-font", type=Path, metavar="FONT.ttf",
        help="Font file for replacing text set in a handwriting font, such as a typed "
             "e-signature, so it still reads as a signature. Use an openly licensed font "
             "(e.g. SIL OFL): it is embedded in the published PDF.",
    )
    args = parser.parse_args()
    if args.handwriting_font and not args.handwriting_font.is_file():
        sys.exit(f"--handwriting-font: no such file {args.handwriting_font}")
    handwriting = str(args.handwriting_font) if args.handwriting_font else None
    signatures = [_parse_signature(spec) for spec in args.draw_signature]
    if signatures and not handwriting:
        sys.exit("--draw-signature needs --handwriting-font")

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
    regions = [_parse_region(spec, "--remove-images") for spec in args.remove_images]
    for page_no, region in regions:
        page = doc[page_no - 1]
        removed = [xref for xref, *_ in page.get_images(full=True)
                   if any(region.contains(r) for r in page.get_image_rects(xref))]
        for xref in removed:
            page.delete_image(xref)
        # A court order's judge's signature was an inline image (BI ... ID ... EI in the
        # content stream). get_images does not list those, so the loop above removed
        # nothing and said so without complaint. They are cut out of the stream instead.
        inline = _remove_inline_images(page, region)
        print(f"Removed {len(removed)} image(s) and {inline} inline image(s) inside "
              f"{tuple(region)} on page {page_no}.")

    # Mailing barcodes have arrived as text in a barcode font with a rotated reference line
    # beside them, and as forty-odd vector bars on a white backing box. Neither is an image
    # and neither matches a text rule, so both need a region of their own. No fill, so the
    # page behind them shows through; line art goes only when it lies wholly inside.
    marks = [_parse_region(spec, "--remove-marks") for spec in args.remove_marks]
    for page_no, region in marks:
        page = doc[page_no - 1]
        before = len(_marks_inside(page, region))
        page.add_redact_annot(region)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        print(f"Removed {before} mark(s) (text spans and paths) inside {tuple(region)} "
              f"on page {page_no}.")

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
        pending: list[tuple[pymupdf.Point, str, str, float, str | None, tuple]] = []
        # search_for also finds the text a form field displays. Those values are replaced
        # in the field itself below; redacting them here as well drew a second copy of
        # every value on an SBA 413, overprinting the field's own.
        fields = [w.rect for w in page.widgets() if w.field_type in _TEXT_FIELDS]
        for original, replacement in rules.items():
            for rect in _merge_line_rects(page.search_for(original)):
                if any(f.contains(rect.tl + (rect.br - rect.tl) * 0.5) for f in fields):
                    continue
                # Match the text being replaced: its size, weight and baseline. Sizing
                # from the rect instead drew an 8.8pt bold name at 4.3pt regular, since
                # the inset rect is shorter than the line and the redaction annotation
                # shrinks its text until it fits -- an edit visible at a glance.
                span = _span_at(spans, rect)
                size = span["size"] if span else min(11.0, rect.height * 0.86)
                font, fontfile = _replacement_font(span, handwriting)
                baseline = span["origin"][1] if span else rect.y1 - rect.height * 0.2
                # Then size by WIDTH as well. A narrow rect in a mailing-address block
                # wrapped "JANE DOE" into "JA" / "NE", fragmenting the text layer so the
                # field no longer extracted. Shrink until it fits the original's width.
                if replacement:
                    if fontfile:
                        width = pymupdf.Font(fontfile=fontfile).text_length(replacement, size)
                    else:
                        width = pymupdf.get_text_length(replacement, font, size)
                    if width > rect.width:
                        size *= rect.width / width * 0.97  # a hair under, for rounding
                    size = max(size, 3.0)
                    # In the original's colour: a lease's e-signatures are navy ink, and
                    # a black stand-in signature beside two navy ones reads as an edit.
                    color = _rgb(span["color"]) if span else TEXT_COLOR
                    pending.append((pymupdf.Point(rect.x0, baseline), replacement,
                                    font, round(size, 1), fontfile, color))
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
                page.insert_text(origin, "_", fontname=FONT, fontsize=size, color=_rgb(color))
        # Written after the redaction, not as the annotation's text, so the replacement
        # sits on the original baseline at the original size instead of being fitted
        # into the trimmed rect.
        for point, text, font, size, fontfile, color in pending:
            page.insert_text(point, text, fontname=font, fontfile=fontfile,
                             fontsize=size, color=color)

    # A filled-in fillable form keeps its values in the form fields, not in the page text,
    # so the rules above find nothing and the check below used to pass regardless: an SBA
    # Form 413 carried the applicant's name, SSN, phones and addresses only there.
    field_counts = _replace_field_values(doc, rules)
    for original, count in field_counts.items():
        per_rule[original] = per_rule.get(original, 0) + count
        total += count

    for page_no, region, text in signatures:
        _draw_signature(doc[page_no - 1], region, text, handwriting)
        print(f"Drew a stand-in signature inside {tuple(region)} on page {page_no}.")

    # Document metadata is a separate leak path from page text, and a quiet one. This
    # statement carried the account number in /Info "author" as 04822863413 -- the same
    # digits as the account number on the page, minus the separators, so every grep for
    # the hyphenated form missed it. Producers routinely stash account and customer ids
    # here. Drop the whole dictionary rather than trying to sanitise it field by field.
    scrubbed = {k: v for k, v in (doc.metadata or {}).items() if v}
    pdfmeta.clear(doc)
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
    text += "\n" + "\n".join(_field_text(verify, w) for p in verify for w in p.widgets())
    if pdfmeta.remaining(verify):
        sys.exit(f"FAILED: metadata survives in {args.output}: {pdfmeta.remaining(verify)}")
    verify.close()

    # Compare on digits alone as well as literally: an identifier is often stored
    # without its separators, which a literal check sails straight past.
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
        # counts as surviving only if it still has real pixels. Inline images have no
        # xref and show up only in get_image_info.
        verify = pymupdf.open(args.output)
        left = [(n, xref) for n, region in regions
                for xref, _, w, h, *_ in verify[n - 1].get_images(full=True)
                if w * h > 1
                and any(region.contains(r) for r in verify[n - 1].get_image_rects(xref))]
        left += [(n, "inline") for n, region in regions
                 for info in verify[n - 1].get_image_info(xrefs=True)
                 if info["xref"] == 0 and region.contains(pymupdf.Rect(info["bbox"]))]
        verify.close()
        if left:
            sys.exit(f"FAILED — images still inside a removed region: {left}")
        print("Verified: no image remains inside a removed region.")

    if marks:
        verify = pymupdf.open(args.output)
        left = [(n, len(_marks_inside(verify[n - 1], region))) for n, region in marks
                if _marks_inside(verify[n - 1], region)]
        verify.close()
        if left:
            sys.exit(f"FAILED — text or paths still inside a --remove-marks region: {left}")
        print("Verified: no text or path remains inside a --remove-marks region.")

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


def _replacement_font(span: dict | None, handwriting: str | None = None) -> tuple[str, str | None]:
    """The font to write a replacement in, as (fontname, fontfile or None).

    Matches the replaced span's weight, slant and, for monospace, its family. A pay stub
    set in Courier had its name replaced in Helvetica, which reads as an edit among
    fixed-width text; its regular Courier spans do not set the monospace flag, so the
    font name is checked as well. Text in a handwriting font, such as a typed
    e-signature, uses the --handwriting-font file when one is given.
    """
    if not span:
        return FONT, None
    name = span["font"].lower()
    if handwriting and any(hint in name for hint in HANDWRITING_HINTS):
        return "handwriting", handwriting
    bold = bool(span["flags"] & BOLD_FLAG)
    italic = bool(span["flags"] & ITALIC_FLAG) or "italic" in name or "oblique" in name
    mono = bool(span["flags"] & MONO_FLAG) or "courier" in name
    if mono:
        return (MONO_BOLD_FONT if bold else MONO_FONT), None
    if italic:
        return (BOLD_ITALIC_FONT if bold else ITALIC_FONT), None
    return (BOLD_FONT if bold else FONT), None


def _rgb(color: int) -> tuple[float, float, float]:
    """A PyMuPDF span colour (0xRRGGBB) as the 0-1 RGB tuple insert_text takes."""
    return tuple(((color >> shift) & 0xFF) / 255 for shift in (16, 8, 0))


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


def _parse_region(spec: str, flag: str) -> tuple[int, pymupdf.Rect]:
    """'4:50,332,131,373' -> (4, Rect(50, 332, 131, 373))."""
    try:
        page, coords = spec.split(":")
        x0, y0, x1, y1 = (float(v) for v in coords.split(","))
    except ValueError:
        sys.exit(f"{flag} expects PAGE:X0,Y0,X1,Y1, got {spec!r}")
    return int(page), pymupdf.Rect(x0, y0, x1, y1)


def _parse_signature(spec: str) -> tuple[int, pymupdf.Rect, str]:
    """'1:430,700,560,730=J Q Sample' -> (1, Rect(430, 700, 560, 730), 'J Q Sample')."""
    region, sep, text = spec.partition("=")
    if not sep or not text.strip():
        sys.exit(f"--draw-signature expects PAGE:X0,Y0,X1,Y1=TEXT, got {spec!r}")
    page, rect = _parse_region(region, "--draw-signature")
    return page, rect, text.strip()


def _digits(value: str) -> str:
    return "".join(c for c in value if c.isdigit())


# "BI/W 120 ..." with no space is legal: a slash delimits a token as well as whitespace.
_BI = re.compile(rb"(?:^|(?<=\s))BI(?=[\s/])")
_ID = re.compile(rb"(?<=\s)ID\s")
_EI_AFTER = re.compile(rb"\s*EI(?=\s|$)")
_EI_SEARCH = re.compile(rb"\sEI(?=\s|$)")
_COMPONENTS = {b"/G": 1, b"/DeviceGray": 1, b"/RGB": 3, b"/DeviceRGB": 3,
               b"/CMYK": 4, b"/DeviceCMYK": 4, b"/I": 1, b"/Indexed": 1}


def _inline_spans(stream: bytes) -> list[tuple[int, int]]:
    """(start, end) of every BI ... ID <data> EI block in a content stream.

    An unfiltered image's data length follows from its width, height, bits per component
    and colour space, which is the only reliable way past data that happens to contain
    the bytes "EI". A filtered one is ended at the first EI token after its data.
    """
    spans, pos = [], 0
    while (bi := _BI.search(stream, pos)) is not None:
        id_ = _ID.search(stream, bi.end())
        if id_ is None:
            break
        params, start = stream[bi.end():id_.start()], id_.end()
        end = None
        if not re.search(rb"/(?:F|Filter)\b", params):
            def number(pattern: bytes, default: int | None = None) -> int | None:
                m = re.search(pattern + rb"\s+(\d+)", params)
                return int(m.group(1)) if m else default
            mask = re.search(rb"/(?:IM|ImageMask)\s+true", params)
            width, height = number(rb"/(?:W|Width)"), number(rb"/(?:H|Height)")
            bpc = number(rb"/(?:BPC|BitsPerComponent)", 1 if mask else 8)
            space = re.search(rb"/(?:CS|ColorSpace)\s*(/\w+|\[)", params)
            comps = 1 if mask or not space else _COMPONENTS.get(space.group(1), 1)
            if width and height:
                after = _EI_AFTER.match(stream, start + ((width * bpc * comps + 7) // 8) * height)
                end = after.end() if after else None
        if end is None:
            ei = _EI_SEARCH.search(stream, start)
            if ei is None:
                break
            end = ei.end()
        spans.append((bi.start(), end))
        pos = end
    return spans


def _remove_inline_images(page: pymupdf.Page, region: pymupdf.Rect) -> int:
    """Cut every inline image lying wholly inside region out of the page's content
    streams. Returns how many were cut.

    Inline images are matched to their on-page boxes by order of appearance: the n-th
    BI block in the content streams is the n-th xref-less entry of get_image_info. When
    the two counts differ (an inline image inside a form XObject, say), stop rather than
    guess.
    """
    boxes = [pymupdf.Rect(i["bbox"]) for i in page.get_image_info(xrefs=True) if i["xref"] == 0]
    if not boxes:
        return 0
    doc = page.parent
    blocks = [(xref, start, end) for xref in page.get_contents()
              for start, end in _inline_spans(doc.xref_stream(xref))]
    if len(blocks) != len(boxes):
        sys.exit(f"page {page.number + 1}: {len(blocks)} inline image(s) in the content "
                 f"stream but {len(boxes)} on the page; cannot match them safely")
    cuts: dict[int, list[tuple[int, int]]] = {}
    for (xref, start, end), box in zip(blocks, boxes):
        if region.contains(box):
            cuts.setdefault(xref, []).append((start, end))
    for xref, spans in cuts.items():
        stream, out, last = doc.xref_stream(xref), bytearray(), 0
        for start, end in spans:
            out += stream[last:start]
            last = end
        out += stream[last:]
        doc.update_stream(xref, bytes(out))
    return sum(len(spans) for spans in cuts.values())


def _marks_inside(page: pymupdf.Page, region: pymupdf.Rect) -> list:
    """Text spans centred inside region, and vector paths lying wholly inside it."""
    spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
             for s in l["spans"]
             if s["text"].strip() and region.contains(
                 pymupdf.Point((s["bbox"][0] + s["bbox"][2]) / 2,
                               (s["bbox"][1] + s["bbox"][3]) / 2))]
    paths = [d for d in page.get_drawings() if region.contains(d["rect"])]
    return spans + paths


# Values the form's own JavaScript formats for display: AFSpecial_Format(n) shows a ZIP,
# ZIP+4, phone number or SSN with separators while storing the bare digits.
_SPECIAL_FORMAT = re.compile(r"AFSpecial_Format\(\s*(\d)\s*\)")
_TEXT_FIELDS = (pymupdf.PDF_WIDGET_TYPE_TEXT, pymupdf.PDF_WIDGET_TYPE_COMBOBOX,
                pymupdf.PDF_WIDGET_TYPE_LISTBOX)


def _replace_field_values(doc: pymupdf.Document, rules: dict[str, str]) -> dict[str, int]:
    """Apply the rules to every text form field's value, and redraw its appearance.

    A rule matches a field when the original appears in its value, or when the value is
    the same digits stored without separators: a form that formats an SSN for display
    keeps 9 bare digits. Returns the number of fields each rule changed.
    """
    counts: dict[str, int] = {}
    for page in doc:
        for widget in page.widgets():
            value = widget.field_value
            if widget.field_type not in _TEXT_FIELDS or not isinstance(value, str) or not value:
                continue
            new, hit = value, []
            for original, replacement in rules.items():
                if original in new:
                    new = new.replace(original, replacement)
                    hit.append(original)
                elif len(_digits(original)) >= 6 and _digits(new) == _digits(original):
                    new = _digits(replacement) if new.isdigit() else replacement
                    hit.append(original)
            if new == value:
                continue
            fmt = _SPECIAL_FORMAT.search(widget.script_format or "")
            # update() draws the appearance from field_value, so set the displayed form
            # first, then store the bare value in /V as the form's own script would.
            widget.field_value = _special_format(new, int(fmt.group(1))) if fmt else new
            widget.update()
            if fmt:
                doc.xref_set_key(widget.xref, "V", pymupdf.get_pdf_str(new))
            for original in hit:
                counts[original] = counts.get(original, 0) + 1
    return counts


def _special_format(value: str, kind: int) -> str:
    """Acrobat's AFSpecial_Format: 0 ZIP, 1 ZIP+4, 2 phone, 3 SSN. Anything that does not
    have the right number of digits is shown as stored."""
    d = _digits(value)
    if kind == 0 and len(d) == 5:
        return d
    if kind == 1 and len(d) == 9:
        return f"{d[:5]}-{d[5:]}"
    if kind == 2 and len(d) == 10:
        return f"({d[:3]}) {d[3:6]}-{d[6:]}"
    if kind == 2 and len(d) == 7:
        return f"{d[:3]}-{d[3:]}"
    if kind == 3 and len(d) == 9:
        return f"{d[:3]}-{d[3:5]}-{d[5:]}"
    return value


def _field_text(doc: pymupdf.Document, widget: pymupdf.Widget) -> str:
    """A form field's stored value and the text drawn in its appearance stream."""
    parts = [str(widget.field_value or "")]
    kind, ref = doc.xref_get_key(widget.xref, "AP/N")
    if kind == "xref":
        parts.append(doc.xref_stream(int(ref.split()[0])).decode("latin-1"))
    return "\n".join(parts)


SIGNATURE_INK = (0.05, 0.05, 0.15)


def _draw_signature(page: pymupdf.Page, region: pymupdf.Rect, text: str, fontfile: str) -> None:
    """Write text in the handwriting font, as large as fits region, sitting on its lower
    edge the way a signature sits on its line."""
    size = region.height * 0.8
    width = pymupdf.Font(fontfile=fontfile).text_length(text, size)
    if width > region.width:
        size *= region.width / width * 0.97
    page.insert_text(pymupdf.Point(region.x0, region.y1 - region.height * 0.2), text,
                     fontname="handwriting", fontfile=fontfile, fontsize=size,
                     color=SIGNATURE_INK)


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
