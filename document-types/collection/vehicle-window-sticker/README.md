# Vehicle window sticker

Source assets for `landing.ai/document-type/vehicle-window-sticker`.

## Sample document

`source/kia-niro-ex-touring-2023-window-sticker.jpg`: the Monroney label (new-vehicle
window sticker) of a 2023 Kia Niro EX Touring, photographed on a display car at the 2023
Denver Auto Show. **1 image, landscape (2980×1830)**, cropped from a phone photo.

| | |
|---|---|
| Publisher | Corqe, the photographer, on Wikimedia Commons (CC0 1.0); label content printed by Kia America, Inc. |
| Source | [2023 Denver Auto Show Kia Niro EX Touring window sticker](https://commons.wikimedia.org/wiki/File:2023_Denver_Auto_Show_Kia_Niro_EX_Touring_window_sticker.jpg) ([file](https://upload.wikimedia.org/wikipedia/commons/0/0a/2023_Denver_Auto_Show_Kia_Niro_EX_Touring_window_sticker.jpg)) |
| Retrieved | 2026-10-25 |
| Clearance | Public |

Wikimedia Commons is an upload site, but here the uploader is the photographer, who
states the photo as own work (2023-04-16) and dedicates it to the public domain under
CC0 1.0. The sticker reads Sold To Kia America, Inc. and Ship To the Colorado Convention
Center: a manufacturer-owned show car, not a customer's vehicle. It carries corporate
data and that car's VIN, and no personal data, so nothing was redacted. Downloaded by
script.

**Preprocessing.** The original is a 4032×3024 iPhone photo in which the label sits in a
black display frame with the engine bay above it. The committed file is a perspective
crop of the label alone: the four corners of its printed border, plus an 18-pixel
margin, mapped to a rectangle, which removes the frame and the slight keystone. It was
re-encoded without EXIF, which held GPS coordinates and the camera model.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

The collection's first **photographed label**, and one of its densest single pages:

- **A real photo, not a scan.** Ceiling lights glare off the display glass and wash out
  a few words in the driver-assist list and the safety panel.
- **Five panels, each with its own layout.** A feature list, a price column, the EPA
  fuel economy label with its large numerals and rating sliders, the NHTSA safety
  ratings grid, and the parts content statement.
- **A price column that pairs names with right-aligned amounts across a wide gap**,
  with several rows reading "Included" instead of a price.

## Featured fields: what the car costs to buy and to run

All on page 1. The request named no fields; its notes suggested these, and five were
taken:

| Field | Value |
|---|---|
| Base MSRP | 31490 |
| Inland freight and handling | 1325 |
| Total MSRP | 33295 |
| Combined MPG | 49 |
| Annual fuel cost | 900 |

The price column read top to bottom, then the EPA label's two headline numbers. The
suggested final assembly point grounds correctly only on its second occurrence (the
first points at the "FINAL ASSEMBLY POINT:" caption) and was left out to keep the
overlay to five fields.

## What it surfaced

**The price column grounds cleanly.** Every amount, including the bare
"$ 1,325.00" on the freight row and the total in the red band, boxes on the amount
alone, despite the wide gap from its label.

**The two EPA ratings came back swapped on the first extraction.** The parse prints
both slider headings and then both numbers ("Fuel Economy & Greenhouse Gas Rating /
Smog Rating / 8 / 7"), and extraction gave GHG 7 and smog 8. Sharpening the two schema
descriptions to name each slider ("the wider, left-hand slider") fixed it on a
re-extraction. Neither is featured.

**"Included" options have no price to point at.** Their `price` is null and has no
range, as expected, and their `included` flag grounds to the price cell, which reads
"Included" but is flagged as not matching the boolean.

**The large "49" box takes in the pump icon** beside it, and OCR cannot read the 49
inside the box at that scale; the crop was checked by eye and is right.

**Sold To and Ship To sit side by side** and parse as interleaved lines, so the two
addresses ground to shared lines. Names and codes extract correctly.

## Extraction

`schema.json`: **44 leaf fields** across vehicle, sold to, ship to, pricing (with an
options array), fuel economy, safety ratings and parts content. Everything printed
extracts correctly in the committed run, including all 14 option rows and the
"Not Rated" safety grid.

## Cost

**9.40 credits** at standard tier for 1 image: 5.80 for the first parse and extract
(2.20 parse, 3.60 extract), and 3.60 for one re-extraction after the rating
descriptions were sharpened.

## Regenerating

```bash
# The source is a perspective crop of the Commons photo, without EXIF:
curl -sSL -o /tmp/niro.jpg "https://upload.wikimedia.org/wikipedia/commons/0/0a/2023_Denver_Auto_Show_Kia_Niro_EX_Touring_window_sticker.jpg"
.venv/bin/python -c "
from PIL import Image
im = Image.open('/tmp/niro.jpg').convert('RGB'); m = 18
quad = (700-m, 843-m, 706-m, 2633+m, 3627+m, 2637+m, 3653+m, 848-m)  # TL, BL, BR, TR
im.transform((2980, 1830), Image.Transform.QUAD, quad, resample=Image.Resampling.BICUBIC) \
  .save('document-types/collection/vehicle-window-sticker/source/kia-niro-ex-touring-2023-window-sticker.jpg', quality=92)"

.venv/bin/python document-types/scripts/run_ade.py vehicle-window-sticker                # 5.80 credits
.venv/bin/python document-types/scripts/run_ade.py vehicle-window-sticker --extract-only # 3.60, schema iteration
.venv/bin/python document-types/scripts/build_images.py vehicle-window-sticker           # free
.venv/bin/python document-types/scripts/inspect_fields.py vehicle-window-sticker --page 1
```
