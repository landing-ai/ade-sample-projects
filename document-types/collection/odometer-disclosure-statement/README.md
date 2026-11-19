# Odometer Disclosure Statement

**On the website:** [landing.ai/document-type/odometer-disclosure-statement](https://landing.ai/document-type/odometer-disclosure-statement)

Florida DHSMV form HSMV 82993, Separate Odometer Disclosure Statement and
Acknowledgment, filled in with specimen data for a private sale of a 2018 Honda sedan.
The seller states the odometer reading and the date it was read and certifies whether it
shows the actual mileage, and the buyer acknowledges it. The page also has a vehicle
description table, seller and buyer blocks, and the form's printed instructions.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 24 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:19 | 2026-11-19 03:39 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,328 | 3,504 |
| Words under 0.95 confidence | 5 | n/a |
| Words under 0.80 confidence | 2 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.5 s | 7.8 s |
| Per page | 6.5 s | 7.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.4 credits |
| Per page | 0.50 credits | 1.40 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:19 | 2026-11-19 03:39 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 21 | 22 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 148.7 s | 158.2 s |
| Per schema field (24) | 6.20 s | 6.59 s |
| Per value returned | 7.08 s | 7.19 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.3 credits | 1.3 credits |
| Per schema field (24) | 0.054 credits | 0.054 credits |
| Per value returned | 0.062 credits | 0.059 credits |

## Origin

`source/florida-hsmv-82993-odometer-disclosure-redacted.pdf` is the Florida Department
of Highway Safety and Motor Vehicles form **HSMV 82993, Separate Odometer Disclosure
Statement and Acknowledgment (Rev. 11/11)**, filled in for a private sale. It is **1
page, portrait**, a fillable form with a text layer. The filled sample is a 2018 Honda
sedan with an odometer reading of 75,123 miles (no tenths), read on 15 March 2026 and
certified as the actual mileage. Colour, title number and both signatures are blank, as
in the original.

| | |
|---|---|
| Publisher | Instafill.ai (an AI form-filling vendor), filling the official Florida DHSMV form HSMV 82993 |
| Source | [instafill.ai/…/florida-hsmv-82993-private-sale-example.pdf](https://instafill.ai/forms/state-of-florida-department-of-highway-safety-and/examples/state-of-florida-department-of-highway-safety-and-florida-hsmv-82993-private-sale-example.pdf) |
| Linked from | [instafill.ai: examples page for the form](https://instafill.ai/forms/state-of-florida-department-of-highway-safety-and/examples) |
| Retrieved | 2026-10-26, by script |
| Clearance | Redacted |

Instafill publishes the PDF as a worked example on its examples page for the form, which
links the file directly. The form is a public Florida government form and the data is
specimen data. Instafill is a form-automation vendor, which is adjacent to document AI,
so the page should credit the filled sample to Instafill and the form to the Florida
DHSMV.

**Redaction.** The data is specimen data, but the seller and buyer names looked realistic
and sat beside realistic street addresses. A realistic fake name can belong to a real
person, so four values were replaced. They live in fillable form fields, so each was
replaced in the field value and in how it displays:

| What | Replaced with | Count |
|---|---|---|
| Seller's printed name | `Jane Q Sample` | 1 |
| Seller's street address | `100 Main St` | 1 |
| Buyer's printed name | `John Q Sample` | 1 |
| Buyer's street address | `200 Oak St` | 1 |

The city, state and ZIP of each party are kept. The VIN fails its check-digit test
(position 9), so it cannot belong to a real vehicle. It was checked locally, not sent to
a decoding service, and kept as printed. The PDF metadata was cleared. The originals are
not recorded anywhere in this folder, and the rules file stays outside the repo. The
result was verified by a text check, by eye on a render, and by a sweep of every file in
this folder.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Federal and state law require an odometer disclosure when a vehicle changes hands and
the title has no odometer section. The statement travels with the title paperwork.

- **State motor vehicle agencies and tag offices:** they record the disclosed mileage
  when they issue a new title.
- **Car dealers:** they collect disclosures on every trade-in and purchase.
- **Auto lenders:** they check the mileage when valuing the vehicle that secures a loan.
- **Vehicle history and title services:** they track reported mileage across sales to
  flag rollbacks.
- **Insurers:** they use disclosed mileage in valuation and fraud checks.

### What it contains

- **A vehicle description table** (VIN, year, make, colour, body, title number).
- **Spaced digit boxes** for the odometer reading, with a printed comma between them.
- **Checkboxes that carry meaning:** a 5- or 6-digit odometer choice and three numbered
  certification statements, of which one is ticked.
- **Two near-identical party blocks** for seller and buyer, each with signature, printed
  name and address rows.
- **Fill artifacts and blanks,** such as a year formatted as `2,018` and empty colour,
  title number and signature boxes.
- **Printed instructions** in the lower third of the page.
