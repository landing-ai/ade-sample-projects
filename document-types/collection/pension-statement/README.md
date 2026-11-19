# Pension statement

**On the website:** [landing.ai/document-type/pension-statement](https://landing.ai/document-type/pension-statement)

The specimen pension pay stub that the New York State and Local Retirement System shows
its retirees: the monthly payment advice for August 2023. It shows the monthly service
annuity, federal tax withheld, before-tax and after-tax deductions, current and
year-to-date totals, and how the net payment was deposited.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 36 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:44 | 2026-11-19 03:42 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,253 | 2,327 |
| Words under 0.95 confidence | 7 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.7 s | 17.2 s |
| Per page | 2.7 s | 17.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.4 credits | 1.1 credits |
| Per page | 0.40 credits | 1.10 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:44 | 2026-11-19 03:42 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 36 | 36 |
| Non-null fields returned | 36 | 36 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 258.4 s | 126.6 s |
| Per schema field (36) | 7.18 s | 3.52 s |
| Per value returned | 7.18 s | 3.52 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.6 credits | 1.7 credits |
| Per schema field (36) | 0.044 credits | 0.047 credits |
| Per value returned | 0.044 credits | 0.047 credits |

## Origin

`source/nys-ers-pension-pay-stub-2022-specimen.pdf` is the specimen pension pay stub
that the New York State and Local Retirement System shows its retirees. It is the
monthly payment advice the Employees' Retirement System (ERS) issues to a retiree, for
the period 8/01/2023 to 8/31/2023. It is **1 page, landscape**, with no text layer. It
has a header with the pay group, pay period, advice number and date, then a recipient
block and federal tax data, earnings and taxes tables, before-tax and after-tax
deduction tables, a summary band with current and year-to-date totals, and a net pay
distribution table.

| | |
|---|---|
| Publisher | Office of the New York State Comptroller (New York State and Local Retirement System) |
| Source | [web.osc.state.ny.us/…/pay-stub-2022-for-web.svg](https://web.osc.state.ny.us/retire/retirees/paystub-tutorial/pay-stub-2022-for-web.svg) |
| Retrieved | 2026-10-03, by script |
| Clearance | Public (specimen) |

The Comptroller's "Your Pension Pay Stub" tutorial page for retirees embeds this image
and explains each part of the stub. Every personal value is a placeholder: John Smith,
123 Main Street, Any Town NY 12345-0000, employee ID R12345678, and an account number
masked as XXXXXXX1234. The only real address is the Comptroller's own office. Nothing
needed redacting. The file is named for 2022, but the stub is for August 2023.

The publisher distributes the stub as an **SVG**, not a PDF. It was exported from Adobe
Illustrator with every character outlined as a vector path, so it has no text at all.
The SVG was printed to PDF with headless Chrome, placed in a small local HTML page sized
to its 615.27 x 459.91 viewBox, which gave a one-page 11 x 8.2225 in landscape page with
no margins. The PDF's document metadata (Chrome's title and producer strings) was then
cleared, and the result was checked by eye against the SVG. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A pension payment advice shows one month's defined-benefit pension payment and what was
taken out of it. Retirees use it as proof of income, much as workers use a pay stub.

- **Mortgage and consumer lending:** underwriters verify pension income from the gross
  annuity and its continuation.
- **Property management and housing programs:** landlords and senior housing programs
  verify a retiree's income.
- **Public benefits:** agencies check pension income when deciding eligibility for
  programs such as Medicaid or SNAP.
- **Tax preparation and financial planning:** preparers and advisors reconcile
  withholding and deductions against year-end tax forms.
- **Family law:** attorneys and courts check equitable distribution payments made to a
  former spouse under a divorce order.

### What it contains

- **A pay-stub layout for a pension.** The single earnings line is a Monthly Service
  Annuity, and the recipient is a retiree, not an employee.
- **Pension-specific deductions.** An equitable distribution, the share of the pension
  paid to a former spouse, is taken before tax, and a county retiree health premium is
  taken after tax.
- **Current and year-to-date figures side by side** in every table and in the summary
  band, so each value has a twin in the next column.
- **Several small tables** for earnings, taxes, deductions and the net pay distribution.
- **Masked and zero-padded identifiers,** such as a masked account number and an advice
  number with leading zeros.
- **Outlined text with no text layer,** so every value has to be read from the page
  image.
