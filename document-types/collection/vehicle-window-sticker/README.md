# Vehicle window sticker

**On the website:** [landing.ai/document-type/vehicle-window-sticker](https://landing.ai/document-type/vehicle-window-sticker)

The Monroney label of a 2023 Kia Niro EX Touring, photographed on a display car at the
2023 Denver Auto Show. It lists the standard and optional equipment with their prices,
the base and total MSRP, the EPA fuel economy and environment label, the NHTSA safety
ratings and the parts content statement.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 44 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:59 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 6,874 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 17.4 s |
| Per page | 17.4 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 2.3 credits |
| Per page | 2.30 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 04:00 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 44 |
| Non-null fields returned | 44 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 80.5 s |
| Per schema field (44) | 1.83 s |
| Per value returned | 1.12 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 3.6 credits |
| Per schema field (44) | 0.082 credits |
| Per value returned | 0.050 credits |

## Origin

`source/kia-niro-ex-touring-2023-window-sticker.jpg` is the Monroney label (new-vehicle
window sticker) of a 2023 Kia Niro EX Touring, photographed on a display car at the 2023
Denver Auto Show. It is **1 image, landscape (2980×1830)**, cropped from a phone photo.

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

The original is a 4032×3024 iPhone photo in which the label sits in a black display
frame with the engine bay above it. The committed file is a perspective crop of the
label alone: the four corners of its printed border, plus an 18-pixel margin, mapped to
a rectangle, which removes the frame and the slight keystone. It was re-encoded without
EXIF, which held GPS coordinates and the camera model. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Every new car sold in the US carries a Monroney label, and its contents follow the car
from the factory through every later sale.

- **Car dealers and dealer groups:** they check equipment and pricing against inventory
  and advertised prices.
- **Auto lenders:** underwriters use the MSRP and options to set loan-to-value and
  confirm the collateral.
- **Used-car marketplaces and vehicle history providers:** they decode original
  equipment and price from a car's sticker.
- **Insurers and appraisers:** they value vehicles and claims from the original
  equipment and price.
- **Fleet managers and leasing companies:** they record specifications, fuel economy
  and price for each vehicle acquired.

### What it contains

- **A photo, not a scan.** Ceiling lights glare off the display glass and wash out a
  few words in the driver-assist list and the safety panel.
- **Five panels, each with its own layout:** a feature list, a price column, the EPA
  fuel economy label, the NHTSA safety ratings grid, and the parts content statement.
- **A price column** that pairs names with right-aligned amounts across a wide gap, with
  several rows reading "Included" instead of a price.
- **Large numerals and rating sliders** on the EPA label, with two slider headings
  printed before their two values.
- **Side-by-side address blocks** for Sold To and Ship To.
- **Icons and a VIN** among the printed text.
