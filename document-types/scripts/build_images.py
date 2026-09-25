#!/usr/bin/env python3
"""Build the page images from a completed parse and extract run.

    python document-types/scripts/build_images.py invoice

Reads  collection/<slug>/parse.json, extract.json, manifest.json, source/<doc>
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
BOX_RGB = (220, 38, 38)
BOX_WIDTH_PX = 3
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


def draw_box(img: Image.Image, box: dict) -> None:
    w, h = img.size
    ImageDraw.Draw(img).rectangle(
        [box["xmin"] * w, box["ymin"] * h, box["xmax"] * w, box["ymax"] * h],
        outline=BOX_RGB,
        width=BOX_WIDTH_PX,
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
    args = parser.parse_args()

    folder = COLLECTION / args.slug
    for required in ("parse.json", "extract.json", "manifest.json"):
        if not (folder / required).is_file():
            sys.exit(
                f"Missing {folder / required}.\n"
                f"Run: python document-types/scripts/run_ade.py {args.slug}"
            )

    parse = json.loads((folder / "parse.json").read_text(encoding="utf-8"))
    extract = json.loads((folder / "extract.json").read_text(encoding="utf-8"))
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))

    sources = sorted(p for p in (folder / "source").iterdir() if p.is_file())
    if not sources:
        sys.exit(f"No document in {folder / 'source'}")
    document = sources[0]

    fields = [f["path"] for f in manifest.get("fields", [])]
    if not fields:
        sys.exit("manifest.json lists no fields; nothing to illustrate.")

    resolved = flatten(extract.get("extraction_metadata") or {})
    images_dir = folder / "images"

    located: dict[int, list[dict]] = {}
    print(f"Resolving {len(fields)} field(s) ...")
    for path in fields:
        meta = resolved.get(path)
        if not meta:
            print(f"  {path}: NOT IN EXTRACTION — check the path against extract.json")
            continue
        if not meta.get("ranges"):
            print(f"  {path}: value present but ungrounded (synthesized); no image")
            continue

        hit = locate(parse, meta["ranges"][0])
        if not hit:
            print(f"  {path}: range did not fall inside any block")
            continue

        page_number, box = hit
        located.setdefault(page_number, []).append({"path": path, "box": box})
        print(f"  {path}: page {page_number}  {meta['value']!r}")

    if not located:
        sys.exit("\nNothing could be located. Images not written.")

    print("\nWriting images ...")
    for page_number, items in sorted(located.items()):
        page_img = render_page(document, page_number)

        for item in items:
            crop = crop_around(page_img, item["box"])
            # Draw on the crop, not the page, so the stroke is not scaled down twice.
            crop_box = item["box"]
            w, h = page_img.size
            offset_x = max(0.0, crop_box["xmin"] - CROP_PAD_X) * w
            offset_y = max(0.0, crop_box["ymin"] - CROP_PAD_Y) * h
            ImageDraw.Draw(crop).rectangle(
                [
                    crop_box["xmin"] * w - offset_x,
                    crop_box["ymin"] * h - offset_y,
                    crop_box["xmax"] * w - offset_x,
                    crop_box["ymax"] * h - offset_y,
                ],
                outline=BOX_RGB,
                width=BOX_WIDTH_PX,
            )
            name = item["path"].replace(".", "-").replace("[", "-").replace("]", "")
            save(crop, images_dir / f"{name}.png")

        annotated = page_img.copy()
        for item in items:
            draw_box(annotated, item["box"])
        save(annotated, images_dir / f"page-{page_number}.png", MAX_PAGE_WIDTH_PX)

    print(f"\nWrote {folder / 'images'}")
    print("Open the images and check them. A wrong crop is not visible from a listing.")


if __name__ == "__main__":
    main()
