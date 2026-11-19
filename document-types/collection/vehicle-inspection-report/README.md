# Vehicle Inspection Report

**On the website:** [landing.ai/document-type/vehicle-inspection-report](https://landing.ai/document-type/vehicle-inspection-report)

A DEKRA Used Car Report from South Africa recording a condition inspection of a 2013
BMW X6 with 143,723 km on the odometer, done for a used car dealer. It holds the
vehicle data, ratings and inspection results for the interior, exterior, engine and
undercarriage, a brake test, a tire table for each wheel, and the technician's
comments and concluding remarks.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 35 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:42 | 2026-11-19 03:57 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 9,826 | 9,969 |
| Words under 0.95 confidence | 83 | n/a |
| Words under 0.80 confidence | 5 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.7 s | 14.9 s |
| Per page | 2.6 s | 5.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.5 credits | 4.0 credits |
| Per page | 0.50 credits | 1.33 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:43 | 2026-11-19 03:57 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 35 | 35 |
| Non-null fields returned | 35 | 35 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 181.9 s | 119.7 s |
| Per schema field (35) | 5.20 s | 3.42 s |
| Per value returned | 0.91 s | 0.60 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 10.0 credits | 10.0 credits |
| Per schema field (35) | 0.286 credits | 0.286 credits |
| Per value returned | 0.050 credits | 0.050 credits |

## Origin

`source/dekra-used-car-report-redacted.pdf` is a **DEKRA Used Car Report** (a condition
report) issued by DEKRA Automotive (PTY) Ltd. in South Africa for the dealer We Buy Cars.
It records an inspection of a 2013 BMW X6 with 143,723 km on the odometer. It is **3
pages, portrait, a generated PDF with a text layer**.

Page 1 has a strip of inspection photos, the Assignment block (client) and a two-column
Vehicle Data block, followed by the Interior and Exterior condition tables. Each table
row has a component, a rating (Very Good, Good, As Expected) and a sentence of
inspection result. Page 2 continues with the Engine/Gearbox/Drivetrain and
Axles/Undercarriage tables, a brake test table (braking force per side, in kN), a tire
table (size, load/speed index, make, model, production date code and tread depth for
each wheel and the spare), and the diagnostic and inspection-condition notes. Page 3 has
the comments, concluding remarks, the technician and DEKRA's general remarks.

| | |
|---|---|
| Publisher | DEKRA Automotive (PTY) Ltd., South Africa, inspecting for the dealer We Buy Cars |
| Source | [scribd.com/document/882663399](https://www.scribd.com/document/882663399) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | Redacted |

Scribd is a user-upload site, so the uploader is not the publisher. This is a real
inspection report on a real vehicle, and was treated as a personal record. The Scribd
URL is recorded without its trailing slug, a bare number of unknown meaning that may be
a stock or account reference.

Redaction was done with `document-types/scripts/redact.py` before anything was parsed.
Text was replaced, not covered, so the originals are not extractable from the committed
PDF.

| What | Replaced with | Count |
|---|---|---|
| VIN | a random 17-character stand-in keeping the manufacturer prefix | 4 |
| Registration number | a random stand-in of the same shape | 1 |
| Report number | a random 10-digit stand-in | 3 |
| Technician's name | `JANE Q SAMPLE` | 1 |

- **Photos.** The two exterior photos at the top of page 1 showed the license plate and
  were removed, leaving their empty frames. The interior, instrument cluster and
  odometer photos were kept.
- **Pages 4 to 8 were dropped.** They were photo pages (engine bay, spare wheel,
  photographed brake-test and diagnostic printouts, a front three-quarter shot showing
  the plate) with no extractable data. The page footers still read `1/8` to `3/8`.
- **Kept:** make, model, year, odometer reading and specification, every condition
  rating, the brake and tire measurements, the dealer's business name, and DEKRA's
  corporate address and phone number.
- PDF metadata cleared.

The original values are not recorded anywhere in this folder, and the rules file stays
outside the repo. The redaction was verified by the script's text check, by eye on a
render, and by a rules check over every file in this folder. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A vehicle inspection report records a used car's condition at a point in time,
component by component. It moves between dealers, buyers, lenders and insurers when a
car changes hands.

- **Used car dealers and remarketing:** dealers and auction houses use condition
  reports to price, recondition and list vehicles.
- **Vehicle finance and leasing:** lenders and lessors check the condition and mileage
  of a car they finance or take back at lease end.
- **Motor insurance:** insurers use inspections to underwrite policies and assess the
  pre-existing condition of a vehicle.
- **Fleet management:** fleet operators track the condition of vehicles across their
  service life and at disposal.
- **Buyers and online marketplaces:** platforms attach independent inspection reports
  to listings so buyers can check a car before purchase.

### What it contains

- **A two-column key/value block** with the vehicle data.
- **34 rating rows across four tables,** each with a section, component, rating and
  result sentence that have to stay together.
- **Measurement tables with units** in the headers (kN) and in the cells (`4 mm`).
- **Odd values printed as they are.** The front-left tire's load/speed index reads
  `3323`, the same as its production date code, and the spare's production date is
  printed `////`.
- **Photos with data in them.** The odometer photo shows the same reading as the Vehicle
  Data block.
- **Page footers that count dropped pages** (`1/8` to `3/8`).
