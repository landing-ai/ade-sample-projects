# Attending Physician Statement

Source assets for `landing.ai/document-type/attending-physician-statement`.

## Sample document

`source/de2501-physician-certificate-sample.pdf` is Part B, the Physician or
Practitioner's Certificate, of California EDD form DE 2501, Application for Disability
Insurance Benefits (Rev. 82, 10-24). The EDD fills it with specimen data. It is
**3 pages, portrait**, with a text layer:

- Page 1 (printed page 11): patient, the practitioner and their license, the treatment
  period, and when the disability began
- Page 2 (printed page 12): ICD diagnosis codes, diagnosis, findings and treatment
- Page 3 (printed page 13): prior treatment, surgery, work-relatedness, and the signed
  certification

**This is a state disability-insurance physician certificate, not an insurance
carrier's Attending Physician Statement (APS).** California's State Disability
Insurance program requires one from the treating physician for every claim. A carrier
APS for a life, disability or long-term-care policy asks for the same core information:
who treated the patient, since when, the diagnosis and ICD codes, the treatment, and when
the patient is expected back at work. Publishers rarely release a filled-in carrier APS,
and this is the closest public specimen.

| | |
|---|---|
| Publisher | State of California Employment Development Department (EDD), State Disability Insurance program |
| Source | https://edd.ca.gov/siteassets/files/pdf_pub_ctr/de2501.pdf |
| Retrieved | 2026-10-04, downloaded by script |
| Clearance | **Public** |

The EDD's Forms and Publications page links this file as "DE 2501 - Sample claim
form", and the same filled pages appear in its paper-claim tutorial. Every page carries a
red "SAMPLE, this page for reference only" banner. The patient is "Sample Claimant", the
SSN is all zeros, and the physician's address is in "Anywhere, CA", so there is no
personal data and nothing was redacted.

The original has 13 pages. Pages 1-10 are instructions, the claimant's authorization
and Part A (the claimant's own statement), so only pages 11-13 were kept, using PyMuPDF.
The PDF metadata was cleared.

## Why this document

It is a comb-box form: almost every value is printed one character per box, and dates are
eight digits with no separators (`01252025`). The form is also printed in red, with
white entry boxes on a red ground. Together these test whether parsing can put a value
back together from separate boxes and still ground it, which the collection's other
forms do not test.

## Featured fields: who certified it, and the timeline of care

All on page 1:

| Field | Value |
|---|---|
| License type | MD |
| License issuing state | CA |
| Under care from | 2025-01-25 |
| Treatment interval | Monthly |
| Date disability began | 2025-01-25 |

The request suggested these five fields and the B12 "still treating" checkbox. The
checkbox extracted correctly (`true`) but grounds `OFF`, as boolean values do on this
form, so it was left out. The request's other option was page 2: the diagnosis, the
treatment and the ICD-10 box. It was not used because the diagnosis and treatment ground
to individual comb boxes (see below), which would leave only the ICD-10 box.

**The primary ICD-10 code is misprinted by the publisher.** It reads `552.92XA`. A
forearm fracture code begins with the letter S, and the form has the digit 5 in its
place. ADE transcribes it exactly as printed. It is deliberately not featured.

## Grounding

- **Dates in comb boxes ground well.** ADE reads `0 1 2 5 2 0 2 5` across eight boxes as
  one date, normalizes it to `2025-01-25`, and the box covers the whole row of digits.
- **Checkbox groups ground to the whole row.** The treatment-interval box covers the full
  "At Intervals Of" line with the marked option in it. That is reasonable for a value
  chosen from a set.
- **Comb-box text does not ground as a value.** In tables, the parser makes each
  character box its own cell. Free text such as the diagnosis, findings and treatment
  extracts correctly ("Broken left forearm closed fracture") but grounds to more than 100
  single-character cells each, which `inspect_fields.py` reads as `OFF`. The patient's
  name, file number and address behave the same way.
- **Several boxes are wide.** License type, issuing state and "under care from" each
  cover the whole entry row, including the field caption and the empty boxes. OCR flagged
  these three crops, but each one does contain its value.
- **One checkbox was misread.** In B29 ("caused or aggravated by regular work?") the X
  is on "No", but the parse reads `[x] Yes`, so `history.work_related` comes back `true`.
  B30, the next row with the same layout, reads correctly.
- **Unanswered questions come back as false.** In B13, neither box for "Was the
  disability caused by an accident or trauma?" is marked, but the result is `false`
  rather than null.

## Schema

`schema.json` has 35 leaf fields, grouped as patient, practitioner, treatment period,
disability, diagnosis, history and certification. The patient's SSN is left out on
purpose.

## Cost

**10.40 credits** at standard tier, for parse and extract together.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py attending-physician-statement
.venv/bin/python document-types/scripts/run_ade.py attending-physician-statement --extract-only
.venv/bin/python document-types/scripts/build_images.py attending-physician-statement
.venv/bin/python document-types/scripts/inspect_fields.py attending-physician-statement --good
```
