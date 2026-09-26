#!/usr/bin/env python3
"""Build the page images from a completed parse and extract run.

    python document-types/scripts/build_images.py invoice

Reads  collection/<slug>/parse-<model>.json, extract-<model>.json, manifest.json,
       source/<doc>
Writes collection/<slug>/images/

Produces, for each field named in the manifest:
  <field>.png          a zoomed crop of the value with its box drawn
  page-<n>.png         the full page with every featured field boxed

This script NEVER calls the ADE API. It is a pure function of the committed output,
so re-rendering to adjust padding, stroke weight or resolution costs nothing and
always produces the same result for the same inputs.

Box resolution, in order of preference:
  1. atomic_grounding  line-level boxes on text blocks
  2. table_cell children  tight per-cell boxes on table blocks
  3. the block box itself  last resort; covers the whole block

Preference matters: a block can be coarse. On a real invoice a single text block held
Invoice Date, Invoice #, Payment Terms, Due Date, Account Number and Currency together,
so boxing the block would have pointed at seven lines instead of the value.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

import pymupdf
from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parents[2]
COLLECTION = REPO_ROOT / "document-types" / "collection"

# One look across the whole library. Changing these changes every page, which is the
# point — the images sit side by side and must not drift.
#
# Highlighter, not error marker: a translucent fill marks the *region* a value came
# from, which an outline alone does not. Side by side at page scale the difference is
# large — an outline makes the eye find a line and then work out what it encloses.
# Amber rather than red because red reads as "something is wrong", and the message here
# is that the value was found correctly.
BOX_RGB = (217, 119, 6)            # amber border
FILL_RGBA = (250, 204, 21, 70)     # translucent yellow, ~27% alpha
# Fraction of the image's short side, not a pixel count: a fixed width is proportionally
# far heavier on a 240px crop than on a 1200px page render.
BOX_WIDTH_FRAC = 0.0035
BOX_WIDTH_MIN_PX = 2
CROP_PAD_X = 0.035          # fraction of page width added around a crop
CROP_PAD_Y = 0.020          # fraction of page height
RENDER_SCALE = 2.0          # 144 DPI; sharp on high-DPI screens without bloating files
JPEG_QUALITY = 90
MAX_PAGE_WIDTH_PX = 1400    # full-page renders are downscaled to this


def overlaps(a: dict, b: dict) -> bool:
    """Do two {start, end} ranges intersect?"""
    return a["start"] < b["end"] and b["start"] < a["end"]


def union_box(boxes: Iterable[dict]) -> dict | None:
    boxes = list(boxes)
    if not boxes:
        return None
    return {
        "xmin": min(b["xmin"] for b in boxes),
        "ymin": min(b["ymin"] for b in boxes),
        "xmax": max(b["xmax"] for b in boxes),
        "ymax": max(b["ymax"] for b in boxes),
    }


def iter_blocks(parse: dict) -> Iterable[dict]:
    for page in parse["structure"]["children"]:
        yield from page["children"]


def locate(parse: dict, field_range: dict) -> tuple[int, dict] | None:
    """Resolve a markdown range to (1-indexed page, normalized box)."""
    for block in iter_blocks(parse):
        grounding = block.get("grounding") or {}
        block_range = grounding.get("range")
        if not block_range or not overlaps(block_range, field_range):
            continue

        page = grounding["page"]

        atomic = block.get("atomic_grounding") or []
        tight = union_box(
            a["box"] for a in atomic
            if a.get("range") and overlaps(a["range"], field_range)
        )
        if tight:
            return page, tight

        cells = block.get("children") or []
        tight = union_box(
            c["grounding"]["box"] for c in cells
            if c.get("grounding", {}).get("range")
            and overlaps(c["grounding"]["range"], field_range)
        )
        if tight:
            return page, tight

        return page, grounding["box"]
    return None


def value_appears_in(value: Any, source: str) -> bool:
    """Is the extracted value visible in the text that was boxed? Compared loosely:
    ADE normalizes as it extracts, so "2025-12-31" may be grounded to "December 31,
    2025" and 3099.67 to "$ 3,099.67"."""
    if value is None:
        return True
    text = source.lower()
    literal = str(value).lower().strip()
    if literal and literal in text:
        return True
    # Numbers: compare digits only, so thousands separators and currency do not matter.
    digits = "".join(c for c in literal if c.isdigit())
    text_digits = "".join(c for c in text if c.isdigit())
    if digits and len(digits) >= 3:
        if digits in text_digits:
            return True
        # Dates are reordered by normalization: "2023-09-02" is grounded to
        # "09/02/2023". Same digits, different order, so a substring test fails on
        # every date field. Fall back to comparing the multiset for date-shaped values.
        if len(digits) == 8 and sorted(digits) == sorted(text_digits.strip()):
            return True
    return False


def flatten(metadata: Any, prefix: str = "") -> dict[str, dict]:
    """Walk extraction_metadata into {dotted.path: {value, ranges}}."""
    out: dict[str, dict] = {}
    if isinstance(metadata, dict):
        if "value" in metadata and "ranges" in metadata:
            out[prefix] = metadata
            return out
        for key, value in metadata.items():
            out.update(flatten(value, f"{prefix}.{key}" if prefix else key))
    elif isinstance(metadata, list):
        for i, item in enumerate(metadata):
            out.update(flatten(item, f"{prefix}[{i}]"))
    return out


def render_page(document: Path, page_number: int) -> Image.Image:
    """Render a 1-indexed page. PyMuPDF is 0-indexed — the off-by-one lands the box
    on the wrong page entirely, so the conversion happens here and nowhere else."""
    if document.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        return Image.open(document).convert("RGB")
    with pymupdf.open(document) as doc:
        if not 1 <= page_number <= len(doc):
            raise ValueError(f"page {page_number} outside 1..{len(doc)}")
        pix = doc[page_number - 1].get_pixmap(
            matrix=pymupdf.Matrix(RENDER_SCALE, RENDER_SCALE)
        )
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def stroke_width(img: Image.Image) -> int:
    return max(BOX_WIDTH_MIN_PX, int(min(img.size) * BOX_WIDTH_FRAC))


def highlight(img: Image.Image, xy: list[float]) -> Image.Image:
    """Translucent fill then border. Returns a new image; alpha compositing cannot be
    done in place on an RGB canvas."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle(xy, fill=FILL_RGBA)
    out = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    ImageDraw.Draw(out).rectangle(xy, outline=BOX_RGB, width=stroke_width(out))
    return out


def draw_box(img: Image.Image, box: dict) -> Image.Image:
    w, h = img.size
    return highlight(
        img, [box["xmin"] * w, box["ymin"] * h, box["xmax"] * w, box["ymax"] * h]
    )


def crop_around(img: Image.Image, box: dict) -> Image.Image:
    w, h = img.size
    left = max(0.0, box["xmin"] - CROP_PAD_X) * w
    top = max(0.0, box["ymin"] - CROP_PAD_Y) * h
    right = min(1.0, box["xmax"] + CROP_PAD_X) * w
    bottom = min(1.0, box["ymax"] + CROP_PAD_Y) * h
    return img.crop((int(left), int(top), int(right), int(bottom)))


def save(img: Image.Image, path: Path, max_width: int | None = None) -> None:
    if max_width and img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=JPEG_QUALITY)
    print(f"  {path.name:38} {img.width}x{img.height}  {path.stat().st_size // 1024} KB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="folder name under document-types/collection/")
    parser.add_argument(
        "--model",
        default="pro",
        help="which parse model's output to render (default: pro)",
    )
    args = parser.parse_args()

    folder = COLLECTION / args.slug
    parse_path = folder / f"parse-{args.model}.json"
    extract_path = folder / f"extract-{args.model}.json"
    for required in (parse_path, extract_path, folder / "manifest.json"):
        if not required.is_file():
            sys.exit(
                f"Missing {required}.\n"
                f"Run: python document-types/scripts/run_ade.py {args.slug} "
                f"--model {args.model}"
            )

    parse = json.loads(parse_path.read_text(encoding="utf-8"))
    extract = json.loads(extract_path.read_text(encoding="utf-8"))
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))

    sources = sorted(p for p in (folder / "source").iterdir() if p.is_file())
    if not sources:
        sys.exit(f"No document in {folder / 'source'}")
    document = sources[0]

    field_specs = manifest.get("fields", [])
    if not field_specs:
        sys.exit("manifest.json lists no fields; nothing to illustrate.")

    resolved = flatten(extract.get("extraction_metadata") or {})
    # Per model: two parse models must not overwrite each other's renders.
    images_dir = folder / "images" / args.model

    located: dict[int, list[dict]] = {}
    print(f"Resolving {len(field_specs)} field(s) ...")
    for spec in field_specs:
        path = spec["path"]
        meta = resolved.get(path)
        if not meta:
            print(f"  {path}: NOT IN EXTRACTION — check the path against extract.json")
            continue
        ranges = meta.get("ranges")
        if not ranges:
            print(f"  {path}: value present but ungrounded (synthesized); no image")
            continue

        # A value printed in several places has several ranges, and their order is not
        # guaranteed stable across runs — on the sample invoice the total appears both
        # in CHARGE DETAILS and in INVOICE TOTALS. Set "occurrence" in the manifest to
        # pin which one gets boxed; otherwise the first is used.
        index = int(spec.get("occurrence", 0))
        if index >= len(ranges):
            print(f"  {path}: occurrence {index} requested but only {len(ranges)} found")
            continue
        if len(ranges) > 1 and "occurrence" not in spec:
            print(f"  {path}: {len(ranges)} occurrences, boxing the first "
                  f"(set \"occurrence\" in manifest.json to pin one)")

        hit = locate(parse, ranges[index])
        if not hit:
            print(f"  {path}: range did not fall inside any block")
            continue

        # A value can be grounded to text that supports it without containing it --
        # "$9.8 billion" grounded to a table cell reading "$ 9,805". Both are right, but
        # a crop whose text does not match the value shown beside it reads as a mistake.
        # Warn, and name the alternatives, since another occurrence often matches.
        source = extract["markdown"][ranges[index]["start"]:ranges[index]["end"]]
        if not value_appears_in(meta["value"], source):
            better = [
                i for i, r in enumerate(ranges)
                if i != index and value_appears_in(
                    meta["value"], extract["markdown"][r["start"]:r["end"]]
                )
            ]
            print(f"  {path}: value {meta['value']!r} is NOT in the boxed text "
                  f"{source.strip()[:40]!r}")
            if better:
                print(f"      occurrence {better[0]} does contain it — consider pinning it")

        # A field can legitimately be featured twice from different occurrences -- the
        # same figure printed in a bullet and again on a chart. The image filename
        # derives from the path, so those would collide; "name" in the manifest
        # overrides it.
        name = spec.get("name") or path.replace(".", "-").replace("[", "-").replace("]", "")
        page_number, box = hit
        located.setdefault(page_number, []).append(
            {"path": path, "box": box, "name": name}
        )
        print(f"  {path}: page {page_number}  {meta['value']!r}")

    if not located:
        sys.exit("\nNothing could be located. Images not written.")

    # A web page can realistically embed one page overlay, so every featured field
    # should live on the same page. Declaring it in the manifest turns that from an
    # assumption into something the script checks.
    feature_page = manifest.get("feature_page")
    if feature_page is not None:
        stray = {p: [i["path"] for i in items]
                 for p, items in located.items() if p != feature_page}
        if stray:
            print(f"\n  WARNING: manifest declares feature_page {feature_page}, but "
                  f"fields also resolved on {sorted(stray)}:")
            for page_number, paths in sorted(stray.items()):
                for path in paths:
                    print(f"      page {page_number}: {path}")
            print("      A page overlay can only show one page. Either pick fields from "
                  "one page or change feature_page.")
        elif len(located) == 1:
            print(f"\n  All featured fields are on page {feature_page}, as declared.")

    print("\nWriting images ...")
    for page_number, items in sorted(located.items()):
        page_img = render_page(document, page_number)

        for item in items:
            # Highlight on the full page first, then crop, so the stroke is in page
            # coordinates and every crop carries the same visual weight regardless of
            # how large the region happens to be.
            marked = draw_box(page_img, item["box"])
            crop = crop_around(marked, item["box"])
            name = item["name"]
            save(crop, images_dir / f"{name}.png")

        annotated = page_img
        for item in items:
            annotated = draw_box(annotated, item["box"])
        save(annotated, images_dir / f"page-{page_number}.png", MAX_PAGE_WIDTH_PX)

    print(f"\nWrote {images_dir}")
    print("Open the images and check them. A wrong crop is not visible from a listing.")


if __name__ == "__main__":
    main()
