# Auto Insurance Application

Source assets for `landing.ai/document-type/auto-insurance-application`.

## Sample document

`source/progressive-ma-auto-application-redacted.pdf`: a completed Progressive
*Application for Massachusetts Motor Vehicle Insurance* (Form 7982 MA, 12/24 edition),
written through an independent agency. **6 pages, portrait**, a native text PDF.

| | |
|---|---|
| Publisher | Progressive Casualty Insurance Co |
| Source | [scribd.com/document/1038741316](https://www.scribd.com/document/1038741316/AUTO-DOCS) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

## This document was redacted before it entered the repo

Scribd is not the publisher. An unknown user uploaded a 10-page "AUTO DOCS" packet that
was a real person's application, so it was treated as a personal record.

What it contained, and what replaced it:

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Applicant's full name | 9 | `JOHN Q SAMPLE` |
| Applicant's street address | 1 | `100 Main St` |
| Applicant's city, state and ZIP | 1 | `Mytown, MA 01890` |
| Garaging ZIP code | 2 | `01890` |
| Applicant's date of birth | 1 | `Jun 14, 1990` |
| Policy number | 8 | `325288425` (random, same shape) |
| VIN | 2 | `3FA6P0HD2FR401300` (make and model positions kept; check digit and serial random) |
| Registration plate | 1 | `2FSM98` (random, same shape) |
| Date of the at-fault accident | 1 | `Mar 6, 2025` |
| Agent's name | 1 | `PAT EXAMPLE` |
| Agency name, street, city/ZIP | 1 each | `ACME AGENCY`, `200 MAIN ST #100`, `ANYTOWN, MA 01880` |
| Agent code | 1 | `75S1F` (random, same shape) |
| Agency phone | 1 | `1-781-555-0112` (fiction-reserved range) |

Done with `document-types/scripts/redact.py`, which removes the underlying text rather
than drawing a box over it, then re-extracts and fails if any original survives. It
verified clean, and a sweep of every file in this folder, on literals and on runs of
digits, found none of the originals.

Three things a text rule would have missed:

- **Hidden tracking text.** Every page carries a 1pt line in a white font holding the
  policy number, the agent code and Progressive's form-routing ids. Invisible on the
  page, but fully extractable and parsed. It was removed outright with `--remove-marks`.
- **DataGlyph codes.** Pages 5 and 6 carry a 2D code in the left margin, set as text in
  a DataGlyph font. It probably encodes the same routing data, so it was removed too.
- **Pages 7-10 were dropped.** They are separate forms appended to the application in
  the uploaded packet: an EFT authorization naming the bank account holder with partial
  routing and account numbers, an automatic payment schedule, a payment receipt with the
  card's last four, and the ID card. None is part of the 6-page application.

PDF metadata was cleared. Replacement text is set in Helvetica, slightly wider than the
form's condensed face, so a careful eye can spot the edited values on page 1 and page 3.

## Why this document

The collection's other auto insurance documents are issued *after* a policy is bound:
declarations pages, loss runs, an MVR. This is the document that comes before, where the
applicant states who drives, what is driven and how it is used, and signs to it. It
tests a different shape: a header block of label/value pairs, per-driver and per-vehicle
blocks, a coverage table with Massachusetts' numbered policy parts, a driving-history
table, and fee amounts buried in agreement prose.

The schema was written for this document: 19 top-level fields resolving to **60 leaf
fields**. All 19 populate.

## Featured fields: what is insured, and at what cost

Page 3, the outline of coverage, carries the vehicle and every coverage line:

| Field | Value |
|---|---|
| VIN | 3FA6P0HD2FR401300 |
| Coverage | Personal Injury Protection |
| Deductible | 8000 |
| Coverage premium | 129 |
| Total 12-month premium | 3559 |

Personal Injury Protection is the only line with a deductible, so it shows every column
of the table. The VIN is pinned to occurrence 0, the outline of coverage; occurrence 1 is
the repeat under Vehicle information. The applicant's name was avoided.

## Grounding

Good. Everything on the coverage table, the driver block and the page 1 premium block
grounds `ok`, and every crop was checked by eye. `build_images.py` warned that OCR could
not read the PIP coverage name, deductible and premium in their boxes; the crops are
right, and the misses are down to the thin condensed face.

What came back `OFF`:

- `driving_history[0].sources`: split over two lines in the source column, so each
  range holds half the value.
- `form_title`: split over the two heading lines.
- `prior_insurance` and `vehicles[0].leased`: booleans, grounded to the printed "No".
- `fees.installment_fee_note`: a summary of a sentence, grounded to its first half.

One extraction quirk: `vehicles[0].primary_use` came back `Pleasure`, from Vehicle
information, although the schema description asks for the outline of coverage, which
prints `Pleasure/Personal`.

The fee amounts ($50 cancellation, $25 late, returned-payment and SR22 fees) were read out
of running agreement prose on pages 5 and 6 and all ground `ok`.

## Credits

12.50 credits at standard tier (parse and extract, 6 pages).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py auto-insurance-application      # spends credits
.venv/bin/python document-types/scripts/inspect_fields.py auto-insurance-application --page 3
.venv/bin/python document-types/scripts/build_images.py auto-insurance-application  # free
```

Redaction is not reproducible from this folder by design: the rules file pairs each
original with its replacement and is kept outside the repo.
