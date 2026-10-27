# Vehicle Inspection Report

Source assets for `landing.ai/document-type/vehicle-inspection-report`.

## Sample document

`source/dekra-used-car-report-redacted.pdf` is a **DEKRA Used Car Report** (a condition
report) issued by DEKRA Automotive (PTY) Ltd. in South Africa for the dealer We Buy Cars.
It records an inspection of a 2013 BMW X6 with 143,723 km on the odometer.

**3 pages, portrait, generated PDF with a text layer.** Page 1 has a strip of inspection
photos, the Assignment block (client) and a two-column Vehicle Data block, followed by
the Interior and Exterior condition tables. Each table row has a component, a rating
(Very Good, Good, As Expected) and a sentence of inspection result. Page 2 continues with
the Engine/Gearbox/Drivetrain and Axles/Undercarriage tables, a brake test table (braking
force per side, in kN), a tyre table (size, load/speed index, make, model, production
date code and tread depth for each wheel and the spare), and the diagnostic and
inspection-condition notes. Page 3 has the comments, concluding remarks, the technician
and DEKRA's general remarks.

| | |
|---|---|
| Publisher | DEKRA Automotive (PTY) Ltd., South Africa, inspecting for the dealer We Buy Cars |
| Source | [scribd.com/document/882663399](https://www.scribd.com/document/882663399) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

Scribd is a user-upload site, so the uploader is not the publisher. This is a real
inspection report on a real vehicle, and was treated as a personal record. The Scribd
URL is recorded without its trailing slug, a bare number of unknown meaning that may be a
stock or account reference.

## Redaction

Done with `document-types/scripts/redact.py` before anything was parsed. Text was
replaced, not covered: the originals are not extractable from the committed PDF.

| What | Replaced with | Count |
|---|---|---|
| VIN | a random 17-character stand-in keeping the manufacturer prefix (`plausible.py`) | 4 |
| Registration number | a random stand-in of the same shape (`plausible.py`) | 1 |
| Report number | a random 10-digit stand-in (`plausible.py`) | 3 |
| Technician's name | `JANE Q SAMPLE` | 1 |

- **Photos.** The two exterior photos at the top of page 1 showed the licence plate and
  were removed, leaving their empty frames. The interior, instrument cluster and odometer
  photos were kept.
- **Pages 4 to 8 were dropped.** They were photo pages (engine bay, spare wheel,
  photographed brake-test and diagnostic printouts, a front three-quarter shot showing
  the plate) with no extractable data. The page footers still read `1/8` to `3/8`.
- **Kept:** make, model, year, odometer reading and specification, every condition
  rating, the brake and tyre measurements, the dealer's business name, and DEKRA's
  corporate address and phone number.
- PDF metadata cleared.

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. Verified by redact.py's text check, by eye on a render, and by
`ship.py check --rules` over every file in this folder.

## Why this document

It is a non-US, non-form document: a vendor-generated report that mixes a key/value
block, long rating tables and small measurement tables.

- **34 rating rows across four tables**, each needing the right section, component,
  rating and result kept together. Extraction returned all 34, in order.
- **Measurement tables with units in the headers** (kN) and in the cells (`4 mm`), which
  the schema asks for as numbers.
- **Odd values printed as printed.** The front-left tyre's load/speed index reads `3323`,
  the same as its production date code and almost certainly a data-entry error in the
  original. Extraction reproduced it rather than "correcting" it. The spare tyre's
  production date is printed `////`.
- **Photos with data in them.** The odometer photo shows the same reading as the Vehicle
  Data block.

## Featured fields

All on **page 1**:

| Field | Label | Value |
|---|---|---|
| `vehicle.manufacturer` | Manufacturer | BMW |
| `vehicle.model` | Model | X6 |
| `vehicle.model_year` | Model year | 2013 |
| `vehicle.odometer_km` | Odometer (km) | 143723 |
| `component_ratings[12].condition` | Vehicle body condition | As Expected |

Together they say what an inspection report is for: which car, how far it has gone, and
what the inspector found. The VIN, registration number and technician are redacted
stand-ins and are not featured.

## Grounding notes

- **Every field on pages 1 and 2 grounds `ok`**, including every brake and tyre cell.
  The ruled tables ground cell by cell.
- **The odometer reading grounds twice:** to `143,723 KM` in the Vehicle Data block and
  to the odometer photo, which the parser described in words ("a total mileage of
  '143723 km'"). The featured field is pinned to the printed value (occurrence 0).
- **Each rating row's second range points at the table heading** (Interior, Exterior,
  Engine, Gearbox, Drivetrain), which supports the row without containing its value.
  The featured rating uses its first range, the cell itself.
- **General comments ground `OFF`**: the range covers the whole line including the
  `General Comments:` label, and the wrapped last word is a separate line.
- **The spare's unreadable production date** (`////`) came back as the string `"null"`
  instead of a JSON null.

## Schema

`schema.json` has 35 leaf fields: report identifiers, the vehicle block, an array of
component ratings, the brake test and tyre tables, and the diagnostic, inspection
condition and comment text.

## Credits

14.00 credits for parse and extract, at the standard tier.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py vehicle-inspection-report
.venv/bin/python document-types/scripts/build_images.py vehicle-inspection-report
```
