# Property tax bill

**On the website:** [landing.ai/document-type/property-tax-bill](https://landing.ai/document-type/property-tax-bill)

The Clark County, Washington Treasurer's sample 2026 property tax statement. It shows
the account number, property information, assessed values with levy rates, an account
summary, past-due details, a 12-line breakdown of tax and assessments by district, and a
payment coupon. Every personal value on it is specimen data.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 28 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:23 | 2026-11-19 03:46 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,951 | 3,172 |
| Words under 0.95 confidence | 9 | n/a |
| Words under 0.80 confidence | 5 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.1 s | 9.6 s |
| Per page | 9.1 s | 9.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.3 credits |
| Per page | 0.50 credits | 1.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:24 | 2026-11-19 03:46 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 28 | 28 |
| Non-null fields returned | 28 | 28 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 197.2 s | 132.8 s |
| Per schema field (28) | 7.04 s | 4.74 s |
| Per value returned | 3.23 s | 2.18 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.4 credits | 2.4 credits |
| Per schema field (28) | 0.086 credits | 0.086 credits |
| Per value returned | 0.039 credits | 0.039 credits |

## Origin

`source/clark-county-property-tax-statement-sample.pdf` is the Clark County (Washington)
Treasurer's sample 2026 property tax statement. It is **1 page, portrait (612×900)**,
with a full text layer: the statement header and account number, property information,
value information with levy rates, an account summary, past-due details, a 12-line tax
and assessment detail by district, and a payment coupon.

| | |
|---|---|
| Publisher | Clark County (WA) Treasurer |
| Source | [clark.wa.gov/…/tax-statement-sample.pdf](https://clark.wa.gov/sites/default/files/media/document/2026-03/tax-statement-sample.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

The Treasurer's office publishes this sample itself and links it from the county's
"Understanding your tax bill" page. Every personal value on it is specimen data: the
owner is "SAMPLE TAXPAYER", the property and mailing addresses are on "MAIN ST", and the
legal description is "#13 TOWNSVILLE ADDITION". The only person named is the elected
County Treasurer, in the office letterhead in her official capacity. The phone numbers,
PO boxes and website are the office's own. **No redaction was needed.**

Two changes were made to the downloaded file. **Only page 1 was kept:** the source is an
11-page explainer, where page 1 is the sample statement and pages 2–11 explain each
lettered section. **The PDF metadata was cleared:** it named the individual who built
the file in Canva.

The teal "Understanding your Tax Statement" banner and the lettered callouts (A–G) are
the publisher's own and were left in place. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A property tax bill states what a property owner owes the county for the year and how
that amount was built up from assessed value and local levies.

- **Mortgage servicers:** they pay tax bills from borrowers' escrow accounts and set the
  escrow payment from the amount due.
- **Mortgage lending and title:** underwriters and closing agents confirm taxes are paid
  and prorate them at closing.
- **Property management and commercial real estate:** owners track tax bills across
  portfolios and pass taxes through to tenants.
- **Property tax consultants:** they compare assessed values and levy rates when they
  prepare appeals.
- **Homeowners and accountants:** they record property tax payments for budgeting and
  tax deductions.

### What it contains

- **Seven lettered sections of different shapes** on one page: key-value panels, a value
  table, a past-due grid, a district list and a payment coupon.
- **Levy rates to 10 decimal places.**
- **Figures that reconcile,** with assessed value times levy rate equal to the sum of the
  levy districts.
- **Two addresses that look alike,** the property address and the owner's mailing
  address on the coupon.
- **Publisher callouts and a banner** laid over the statement.
- **A born-digital text layer.**
