# Pay stub

**On the website:** [landing.ai/document-type/pay-stub](https://landing.ai/document-type/pay-stub)

A Lenovo direct deposit earnings statement for the pay period January 19 to February 1,
2026, with the employee's personal details replaced. It shows the employee's earnings,
taxes, payroll deductions such as a 401(k) contribution, the direct deposit, current and
year-to-date totals, and hours and PTO.

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
| Processed (UTC) | 2026-11-19 03:20 | 2026-11-19 03:41 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,354 | 2,288 |
| Words under 0.95 confidence | 8 | n/a |
| Words under 0.80 confidence | 3 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.4 s | 49.9 s |
| Per page | 3.4 s | 49.9 s |

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
| Processed (UTC) | 2026-11-19 03:20 | 2026-11-19 03:42 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 171.3 s | 141.7 s |
| Per schema field (24) | 7.14 s | 5.90 s |
| Per value returned | 5.19 s | 4.29 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.2 credits | 1.2 credits |
| Per schema field (24) | 0.050 credits | 0.050 credits |
| Per value returned | 0.036 credits | 0.036 credits |

## Origin

`source/lenovo-pay-stub-2026-02-redacted.pdf` is a Lenovo direct deposit earnings
statement for the pay period January 19 to February 1, 2026, redacted. It is **1 page,
portrait (612×792)**: earnings, taxes, payroll deductions, direct deposit, totals, and a
miscellaneous block, in a ruled form set largely in Courier.

| | |
|---|---|
| Publisher | Lenovo (employer) |
| Source | [scribd.com/document/993398120/…](https://www.scribd.com/document/993398120/Lenovo-PayStub-2026-03) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

This is a real employee's pay statement, uploaded to Scribd by a third party. Scribd is
a user-upload site, so the uploader is not the publisher, and the statement is treated as
a personal record. Scribd also blocks scripted requests, so the file was downloaded by
hand.

Six identifiers were replaced using `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it:

| What | Replaced with |
|---|---|
| Employee's name | Jane Q Sample |
| Employee's street address | 100 Main St |
| Employee's city, state and ZIP | Anytown, NC 00000 |
| Last four of the employee's SSN | XXX-XX-0000 |
| Employee ID | 0000 |
| Direct deposit advice number | DD00000000 |

The identifiers are set in Courier and Courier Bold, so the replacements were written in
Courier to match. The PDF metadata was also cleared; its title carried an internal file
identifier. The pay amounts are left as printed: with the identifiers gone, nothing on
the page identifies the employee. Lenovo's name, address, phone number and EIN are the
employer's published details and are left as printed. The bank and account numbers were
already masked in the original.

No original identifier is extractable from the committed PDF, and none appears anywhere
in this folder. The original values are deliberately not recorded here or in
`manifest.json`. The rules file used by `redact.py` stays outside the repo. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A pay stub is the most common proof of income. Anyone who needs to confirm what a person
earns asks for recent ones.

- **Mortgage and consumer lending:** underwriters verify gross pay, year-to-date
  earnings and deductions against the loan application.
- **Property management:** landlords check that an applicant's income meets the rent
  requirement.
- **Income verification services:** they read pay stubs to confirm employment and
  earnings for lenders and employers.
- **Government benefits and social services:** caseworkers use pay stubs to determine
  eligibility.
- **Payroll and HR:** teams reconcile statements when onboarding clients or auditing
  payroll.

### What it contains

- **Ruled tables** for earnings, taxes and deductions, each with current and
  year-to-date amounts.
- **Amounts printed off their labels.** In the Taxes table each amount sits about half a
  line below its code, so pairing by position alone gives the wrong result.
- **A scrambled text layer.** The labels use a font with shifted encoding, so "Amount"
  copies out of the PDF as "$PRXQW". Only the values and the address block carry usable
  text.
- **The same amount printed twice,** as gross pay in the earnings line and the Totals
  row.
- **Tall table cells** that run from a single entry down to the Total row.
- **Monospace Courier type** throughout and masked bank account numbers.
