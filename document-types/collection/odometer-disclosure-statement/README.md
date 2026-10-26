# Odometer Disclosure Statement

Source assets for `landing.ai/document-type/odometer-disclosure-statement`.

## Sample document

`source/florida-hsmv-82993-odometer-disclosure-redacted.pdf` is the Florida Department of
Highway Safety and Motor Vehicles form **HSMV 82993, Separate Odometer Disclosure
Statement and Acknowledgment (Rev. 11/11)**, filled in for a private sale. The seller
states the odometer reading and the date it was read, and certifies whether it shows the
actual mileage. The buyer acknowledges it. Federal and state law require this statement
when a vehicle changes hands and the title has no odometer section.

**1 page, portrait, fillable form with a text layer.** The page has a Vehicle Description
table (VIN, year, make, colour, body, title number) and a one-line odometer statement with
a 5/6-digit checkbox and spaced digit boxes. Below that are the date-read blanks and three
numbered certification checkboxes. Then come seller and buyer blocks, each with
signature/printed-name and city/state/zip rows. The lower third is the form's printed
instructions.

The filled sample is a 2018 Honda sedan with an odometer reading of 75,123 miles (no
tenths), read on 15 March 2026 and certified as the actual mileage. Colour, title number
and both signatures are blank, as in the original.

| | |
|---|---|
| Publisher | Instafill.ai (an AI form-filling vendor), filling the official Florida DHSMV form HSMV 82993 |
| Source | [instafill.ai/…/florida-hsmv-82993-private-sale-example.pdf](https://instafill.ai/forms/state-of-florida-department-of-highway-safety-and/examples/state-of-florida-department-of-highway-safety-and-florida-hsmv-82993-private-sale-example.pdf) |
| Retrieved | 2026-10-26, by script |
| Clearance | **Redacted**, see below |

Instafill publishes the PDF as a worked example on its
[examples page for the form](https://instafill.ai/forms/state-of-florida-department-of-highway-safety-and/examples),
which links the file directly. The form is a public Florida government form and the data
is specimen data. Instafill is a form-automation vendor, which is adjacent to document AI,
so the page should credit the filled sample to Instafill and the form to the Florida
DHSMV.

## Redaction

The data is specimen data, but the seller and buyer names looked realistic and sat beside
realistic street addresses. A realistic fake name can belong to a real person, so four
values were replaced with `document-types/scripts/redact.py`. They live in fillable form
fields, so the rules were applied to the field values and their appearance:

| What | Replaced with | Count |
|---|---|---|
| Seller's printed name | `Jane Q Sample` | 1 |
| Seller's street address | `100 Main St` | 1 |
| Buyer's printed name | `John Q Sample` | 1 |
| Buyer's street address | `200 Oak St` | 1 |

The city, state and ZIP of each party are kept. The VIN fails its check-digit test
(position 9), so it cannot belong to a real vehicle. It was checked locally, not sent to a
decoding service, and kept as printed. The PDF metadata was cleared. The originals are not
recorded anywhere in this folder, and the rules file stays outside the repo. Verified by
redact.py's text check, by eye on a render, and by `ship.py check --rules` over every
file in this folder.

## Why this document

It is a short government form whose key values are hard to read:

- **The odometer reading is split into spaced digit boxes** with a printed comma between
  them, so the parse sees `7 5 1, 2 3` rather than a number.
- **The year carries a fill artifact.** The form filler formatted it as `2,018`.
- **The certification is a checkbox choice.** The meaning is which of three statements is
  ticked, not any text that was typed.
- **It has two near-identical party blocks** (seller and buyer) that must not be swapped.

## Featured fields

All on **page 1**:

| Field | Label | Value |
|---|---|---|
| `vehicle.year` | Vehicle year | 2018 |
| `vehicle.make` | Vehicle make | Honda |
| `odometer.reading_miles` | Odometer reading (miles) | 75123 |
| `odometer.date_read` | Date read | 2026-03-15 |
| `mileage_certification` | Mileage certification | REFLECTS ACTUAL MILEAGE |

Together they tell one disclosure: which car, what its odometer read, when, and what the
seller certified about that reading. They are the request's suggestions except the
odometer type (5-digit). That field grounds correctly but to the same line as the reading,
so it would only have added a duplicate highlight. Seller and buyer names are not
featured, because the impersonal fields make the same point.

## Grounding notes

- **The digit boxes and the year artifact were handled cleanly.** Extraction joined
  `7 5 1, 2 3` into 75123 and turned `2,018` into 2018, and both ground to the right cells.
- **Checkboxes parse as `[x]` / `[ ]` markers** inline with their statements, and the
  checked states are all correct.
- **Booleans ground right but cannot be featured.** The first schema used three booleans
  for the certification. `reflects_actual_mileage: true` grounded to exactly the right line,
  but because the text `true` is not in that line, `inspect_fields.py` marks it OFF. An enum
  that holds the checked statement's printed wording grounds to the same line and passes.
  That is the better schema for a feature page anyway.
- **The odometer reading, the odometer type and the date ground to whole lines,** because
  DPT-3 kept each statement line as one text block. The boxes are wide but correct. The
  date crop triggers the OCR warning in `build_images.py` only because the value is ISO
  (2026-03-15) and the form prints `03 / 15 / 2026`.
- **Blank cells came back as empty strings, not null.** Colour and title number are blank.
  The schema allows null, but extraction returned `""`, grounded OFF to the column labels.
  The empty signature boxes were reported as unsigned, also grounded to their labels.
- **The City/State row was parsed as a small pipe table inside an HTML cell**
  (`| City | State |<br>| Miami | FL |`). Both values still extracted and grounded.

## Schema

`schema.json` has **24 leaf fields**: issuing state and form number; the vehicle (VIN,
year, make, colour, body, title number); the odometer (reading, 5 or 6 digits, date read);
the mileage certification as a three-way enum; and the seller and buyer, each with printed
name, street address, city, state, ZIP and whether the signature box is signed. All
top-level fields were populated with no warnings.

## Credits

**2.7 credits** at the standard tier for the committed output: 1.4 for parsing 1 page with
DPT-3 Pro and 1.3 for extraction. The first extraction (1.4 credits), with the
certification as three booleans, was superseded, for **4.1 credits** in all.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py odometer-disclosure-statement               # spends credits
.venv/bin/python document-types/scripts/run_ade.py odometer-disclosure-statement --extract-only
.venv/bin/python document-types/scripts/build_images.py odometer-disclosure-statement          # free
.venv/bin/python document-types/scripts/inspect_fields.py odometer-disclosure-statement --page 1
```
