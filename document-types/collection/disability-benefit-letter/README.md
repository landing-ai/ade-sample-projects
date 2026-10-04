# Disability Benefit Letter

Source assets for `landing.ai/document-type/disability-benefit-letter`.

## Sample document

`source/disability-benefit-letter.pdf`: a Social Security Administration **Benefit
Verification Letter** for a Social Security Disability Insurance (SSDI) beneficiary. This is
the letter lenders, landlords and benefit programs ask for as proof of disability income.
It has **2 pages, portrait**, and a native text layer.

| | |
|---|---|
| Publisher | Social Security Administration |
| Source | https://www.scribd.com/document/1034680635/Benefit-Verification-Letter (a user upload; shown as plain text, not linked) |
| Retrieved | 2026-10-03, downloaded manually by the operator (Scribd blocks scripted downloads) |
| Clearance | **Redacted** (details below) |

## This document was redacted before it entered the repo

Scribd is a user-upload site, not the publisher, so this letter was treated as a real
person's record. It was. All personal data was replaced or removed **before anything was
parsed**:

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Recipient's name | 1 | `JANE SAMPLE` |
| Street line | 1 | `100 MAIN ST` |
| Unit number line | 1 | `101` |
| City, state and ZIP line | 1 | `ANYTOWN PR  00999` |
| BNC reference number (page 1 header and page 2 running head) | 2 | a random stand-in of the same shape |
| Medicare number (MBI) | 1 | a random MBI-shaped stand-in |
| Date of birth | 1 | `November 14, 1981` |
| Intelligent Mail barcode above the address | 1 | removed |
| Vertical barcode down the left edge (mail-piece ID) | 1 | removed |
| Rotated reference line down the right edge | 1 | removed |

The replacements were made with `document-types/scripts/redact.py`, which removes the
underlying text with PyMuPDF redaction annotations. It doesn't just draw over it. The
script also cleared the PDF metadata. The script re-extracted the output and found no
original value. A sweep of every file in this folder, on literals and on runs of digits,
found none either. The rules file that maps originals to replacements stays outside the
repo.

**The barcodes were text, not pictures.** All three mailing marks were typeset, not drawn
as images or vector paths: the Intelligent Mail barcode is a string in a USPS IMb barcode
font, the left-edge barcode is a 72pt barcode font rotated 90°, and the right-edge line is
rotated body text. Rotated text can't be replaced cleanly, so a one-off pre-pass removed
those three spans with text-only redactions. It left images and line art alone, so the SSA
seal survives. Nothing was drawn in their place. Afterwards: no rotated text remains, the
SSA seal is the only image, neither content stream has an inline image, and the only
drawings are the white fills under the replaced values.

The page 2 signature is the typeset words "Social Security Administration" in a script font.
It names no official, so it was kept.

Kept as printed: the SSA, Medicare and Inspector General phone numbers and URLs, the
local field office's address (a government office), the letter date, the benefit amounts
and dates, and the disability onset date. The operator decided to keep the onset date.
The stand-ins are set in Helvetica, not the letter's Century Schoolbook, so they look
slightly different on close inspection.

## Why this document

A prose letter with no tables, ruled boxes or labels: every value sits inside a sentence
("We deduct $81.90 for medical insurance premiums each month"). That tests a different
skill from the forms in this collection. Extract has to pull a number out of running text
and tell two parallel sections apart. "Current" and "past" benefits use almost identical
sentences with different amounts and periods, and every field went to the right section.

## Featured fields: one benefit calculation

Page 1, the *Information About Current Social Security Benefits* section, from start to
finish:

| Field | Value |
|---|---|
| Benefit amounts effective from | December 2025 |
| Monthly benefit before deductions | 1137.30 |
| Medicare premium deduction | 81.90 |
| Net monthly payment | 1055.00 |

Gross minus the premium, rounded down to the whole dollar, gives the net, so the overlay
reads as one calculation. No person is featured. The Medicare entitlement dates also
ground correctly, but they're on page 2 and can't share the overlay.

## Grounding

Grounding is good and lands at line level. Each amount boxes the one sentence line that
holds it.

- `gross_monthly_benefit` grounds to **both** lines of its two-line sentence. Occurrence 0
  is the first line ("Beginning December 2025, the full monthly ..."), which doesn't
  contain the amount, so occurrence 1, the line with `$1,137.30`, is pinned. The past
  section's gross amount behaves the same way.
- Multi-line values that Extract joins into one string, such as the mailing address, the
  local office address and the payment day, ground across several lines. Each line is
  flagged `OFF` because no single line contains the joined value. They're correct, just
  not featurable.
- `current_benefits.period_end` has no end month in the letter. It came back as the
  **string** `"null"` rather than a JSON null, so it is `SYNTH`. That's a small extraction
  fault, left as is.

All 13 top-level fields populated; the schema has **25 leaf fields**.

## Cost

**3.30 credits** at standard tier: 2 pages.

## Regenerating

```bash
# Redaction, from the original (kept outside the repo):
python barcodes.py original.pdf nobarcodes.pdf      # one-off pre-pass, outside the repo
.venv/bin/python document-types/scripts/redact.py nobarcodes.pdf \
    document-types/collection/disability-benefit-letter/source/disability-benefit-letter.pdf \
    --rules rules.json

.venv/bin/python document-types/scripts/run_ade.py disability-benefit-letter
.venv/bin/python document-types/scripts/build_images.py disability-benefit-letter
.venv/bin/python document-types/scripts/inspect_fields.py disability-benefit-letter --page 1
```

`manifest.json` records **what** was replaced and what replaced it, under
`source.origin.redactions`. It never records the original values.
