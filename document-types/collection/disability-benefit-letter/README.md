# Disability Benefit Letter

**On the website:** [landing.ai/document-type/disability-benefit-letter](https://landing.ai/document-type/disability-benefit-letter)

A Social Security Administration Benefit Verification Letter for a Social Security
Disability Insurance (SSDI) beneficiary, the letter used as proof of disability income.
It states the current monthly benefit, the Medicare premium deducted and the net
payment, the past benefit amounts, the disability onset date and Medicare entitlement
dates, all in running prose.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 25 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:49 | 2026-11-19 02:56 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,571 | 3,207 |
| Words under 0.95 confidence | 10 | n/a |
| Words under 0.80 confidence | 6 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.5 s | 8.3 s |
| Per page | 1.3 s | 4.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.6 credits | 1.9 credits |
| Per page | 0.30 credits | 0.95 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:49 | 2026-11-19 02:56 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 25 | 25 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 324.9 s | 86.9 s |
| Per schema field (25) | 13.00 s | 3.48 s |
| Per value returned | 13.54 s | 3.62 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.6 credits | 1.7 credits |
| Per schema field (25) | 0.064 credits | 0.068 credits |
| Per value returned | 0.067 credits | 0.071 credits |

## Origin

`source/disability-benefit-letter.pdf` is a Social Security Administration **Benefit
Verification Letter** for a Social Security Disability Insurance (SSDI) beneficiary. It
is **2 pages, portrait**, with a native text layer.

| | |
|---|---|
| Publisher | Social Security Administration |
| Source | https://www.scribd.com/document/1034680635/Benefit-Verification-Letter (a user upload; shown as plain text, not linked) |
| Retrieved | 2026-10-03, downloaded manually by the operator (Scribd blocks scripted downloads) |
| Clearance | Redacted |

Scribd is a user-upload site, not the publisher, so this letter was treated as a real
person's record. It was one. All personal data was replaced or removed **before anything
was parsed**:

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
underlying text with PyMuPDF redaction annotations instead of drawing over it. The
script also cleared the PDF metadata. It re-extracted the output and found no original
value, and a sweep of every file in this folder, on literals and on runs of digits,
found none either. The rules file that maps originals to replacements stays outside the
repo.

**The barcodes were text, not pictures.** All three mailing marks were typeset: the
Intelligent Mail barcode is a string in a USPS IMb barcode font, the left-edge barcode
is a 72pt barcode font rotated 90°, and the right-edge line is rotated body text. A
one-off pre-pass removed those three spans with text-only redactions, leaving images and
line art alone, so the SSA seal survives. Nothing was drawn in their place.

The page 2 signature is the typeset words "Social Security Administration" in a script
font. It names no official, so it was kept.

Kept as printed: the SSA, Medicare and Inspector General phone numbers and URLs, the
local field office's address (a government office), the letter date, the benefit
amounts and dates, and the disability onset date. The operator decided to keep the onset
date. The stand-ins are set in Helvetica, not the letter's Century Schoolbook, so they
look slightly different on close inspection. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A benefit verification letter is the standard proof that someone receives Social
Security disability benefits and how much. Beneficiaries download it and hand it to
anyone who needs to verify their income.

- **Mortgage and consumer lending:** underwriters count disability benefits as income
  and need the monthly amount and its continuation.
- **Property management:** landlords and affordable-housing programs verify income for
  rental applications and recertifications.
- **Public assistance programs:** agencies running SNAP, Medicaid, energy assistance and
  similar programs use it to confirm eligibility.
- **Insurance:** long-term disability carriers offset their payments by the Social
  Security benefit the claimant receives.
- **Legal and advocacy:** disability attorneys, benefits counselors and courts use it to
  document a person's benefit history.

### What it contains

- **Prose with no tables, ruled boxes or labels.** Every value sits inside a sentence,
  such as "We deduct $81.90 for medical insurance premiums each month".
- **Two parallel sections** for current and past benefits, written in almost identical
  sentences with different amounts and periods.
- **Amounts split across lines,** where a sentence wraps before the figure it states.
- **Multi-line address blocks** for the recipient and the local field office.
- **A government seal** and a signature set in a script font.
- **Stand-in values in a different typeface** from the rest of the letter.
