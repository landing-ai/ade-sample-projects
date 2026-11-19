# Rate lock

**On the website:** [landing.ai/document-type/rate-lock](https://landing.ai/document-type/rate-lock)

WHEDA's sample mortgage rate lock confirmation for its correspondent lending channel,
dated February 24, 2014. It records the locked loan program, amount, rate, price, lock
date, lock period and expiration, the pricing adjustments, the loan officer, and a
summary of the borrower, property, loan, underwriting and mortgage insurance details.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 34 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:28 | 2026-11-19 03:48 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,268 | 3,383 |
| Words under 0.95 confidence | 11 | n/a |
| Words under 0.80 confidence | 3 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.5 s | 7.5 s |
| Per page | 7.5 s | 7.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.4 credits |
| Per page | 0.50 credits | 1.40 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:28 | 2026-11-19 03:49 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 34 | 34 |
| Non-null fields returned | 34 | 34 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 277.4 s | 76.2 s |
| Per schema field (34) | 8.16 s | 2.24 s |
| Per value returned | 8.16 s | 2.24 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.7 credits | 1.7 credits |
| Per schema field (34) | 0.050 credits | 0.050 credits |
| Per value returned | 0.050 credits | 0.050 credits |

## Origin

`source/wheda-sample-rate-lock-confirmation.pdf` is WHEDA's sample mortgage rate lock
confirmation for its correspondent lending channel, dated February 24, 2014. It is **1
page, portrait (legal, 8.5 × 14 in)**, with a text layer: the lock itself, pricing
adjustments, the loan officer, and a loan summary of borrower, property, loan,
automated underwriting and mortgage insurance details.

| | |
|---|---|
| Publisher | Wisconsin Housing and Economic Development Authority (WHEDA) |
| Source | [wheda.com/…/sample-rate-lock-confirmation---correspondent-channel.pdf](https://www.wheda.com/globalassets/documents/mortgage-lending/sample-rate-lock-confirmation---correspondent-channel.pdf) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

WHEDA, Wisconsin's housing finance agency, publishes this as a sample in its mortgage
lending materials. The borrower and property are placeholders ("John S Correspondent",
123 Main Street, Waukesha). The loan officer contact is a named WHEDA staff member with a
work phone and email, which WHEDA itself publishes as a business contact in the sample;
it is kept as printed. No redaction was needed. Full provenance is in `manifest.json`
under `source.origin`.

## Why this document

### Who processes it

A rate lock confirmation fixes a mortgage's rate and price for a set period while the
loan is processed, so every party to the loan checks its terms before closing.

- **Mortgage lenders and loan processors:** staff check the locked rate, program and
  expiry, and extend or relock before the lock runs out.
- **Correspondent lenders and housing finance agencies:** they match the lock to the
  loan they deliver for purchase.
- **Secondary marketing and hedging desks:** they track open locks and their expiry
  dates to manage pipeline risk.
- **Mortgage brokers:** they confirm the terms the borrower was quoted.
- **Quality control and compliance:** reviewers compare the lock with the closing
  disclosure and the pricing inputs.

### What it contains

- **A key table row** with program, payment type, amount, rate, price, lock date, lock
  period and expiry in eight narrow columns.
- **A dense two-column summary** of borrower, property and loan attributes, mostly label
  and value pairs.
- **Many yes or no values,** such as first-time home buyer and self-employed.
- **Combined values in one cell,** such as LTV and CLTV ("95.000% / 95.000%") and term
  ("360 / 360").
- **Pricing inputs next to the price,** with credit score, LTV and occupancy alongside
  the rate.
- **A legal-size page** with a text layer.
