# SSA-1099

**On the website:** [landing.ai/document-type/ssa-1099](https://landing.ai/document-type/ssa-1099)

A Form SSA-1099, Social Security Benefit Statement, for benefit year 2026, filled with
IRS test data for a fictitious beneficiary. It shows the benefits paid, the benefits
repaid, the net benefits and the federal tax withheld in numbered boxes, with a panel
that breaks the year's benefits into what was deposited and what was withheld for
Medicare.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 16 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:38 | 2026-11-19 03:54 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 1,112 | 1,192 |
| Words under 0.95 confidence | 6 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.0 s | 4.9 s |
| Per page | 4.0 s | 4.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.3 credits | 0.8 credits |
| Per page | 0.30 credits | 0.80 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:38 | 2026-11-19 03:54 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 16 | 16 |
| Non-null fields returned | 11 | 11 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 203.5 s | 74.2 s |
| Per schema field (16) | 12.72 s | 4.64 s |
| Per value returned | 18.50 s | 6.75 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 0.8 credits | 0.8 credits |
| Per schema field (16) | 0.050 credits | 0.050 credits |
| Per value returned | 0.073 credits | 0.073 credits |

## Origin

`source/ssa-1099-irs-form-6744-specimen.pdf` is a **Form SSA-1099, Social Security
Benefit Statement**, for benefit year 2026, filled with IRS test data. It is **1 page,
landscape** (612 x 470 pt, the top of a letter page). The form is a raster image on the
page with a text layer drawn over it, so the PDF has both an image and selectable text.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [f6744.pdf](https://www.irs.gov/pub/irs-pdf/f6744.pdf), Form 6744 (Rev. 10-2026), *VITA/TCE Volunteer Assistor's Test/Retest* |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

Form 6744 is the IRS's certification test booklet for Volunteer Income Tax Assistance
and Tax Counseling for the Elderly volunteers. It is served as a PDF from the IRS's own
forms path. Its scenarios print filled specimen tax documents for fictitious taxpayers,
and this SSA-1099 is one of them.

Every value is IRS test data: a fictitious beneficiary at 1234 Charity Avenue, Your
City, Your State, with the Social Security number already masked to `417-00-XXXX` in
the source. Nothing needed redacting. The PDF metadata was reset to the IRS as author
and a title naming the source page.

The source is 210 pages. The SSA-1099 is the top half of PDF page 93 (printed page 88);
the bottom half of that page is an unrelated Form 1099-C for a different fictitious
taxpayer. The 1099-C's text and vector art were removed, so they are not hidden in the
file outside the visible area. The page was then cropped to its top 470 pt, in the white
space between the two forms. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

The Social Security Administration sends an SSA-1099 to every person who received
Social Security benefits in the year. Its net benefits feed line 6a of Form 1040.

- **Tax preparation:** preparers and volunteer programs such as VITA and TCE copy the
  boxes onto the return, which is why the IRS uses it in its volunteer test.
- **Mortgage and consumer lending:** lenders use the benefit statement to verify fixed
  income for retired and disabled borrowers.
- **Public benefits and housing programs:** agencies check Social Security income for
  eligibility for assistance such as Medicaid or housing subsidies.
- **Financial planning and wealth management:** advisers use it to plan income and tax
  withholding for retired clients.
- **Elder law and estate administration:** attorneys and fiduciaries gather it when
  managing a beneficiary's finances.

### What it contains

- **Numbered ruled boxes** for benefits paid, repaid, net benefits and tax withheld.
- **Two boxes (3 and 5) that print the same amount.**
- **A free-form description panel** that breaks the benefits into what was deposited
  and what was withheld for Medicare, in one tall cell.
- **The year as a large standalone figure** in the header.
- **Blank boxes** that should come back empty.
- **A form image with a text layer drawn over it.**
- **A Social Security number masked** in the source.
