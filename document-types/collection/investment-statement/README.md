# Investment statement

**On the website:** [landing.ai/document-type/investment-statement](https://landing.ai/document-type/investment-statement)

Fidelity's sample monthly investment report for July 2015, covering an individual
brokerage account, a traditional IRA and a 529 education account for a specimen
customer. It has a portfolio summary, asset allocation charts, holdings tables for
stocks, bonds, mutual funds and ETFs, activity ledgers, an estimated cash flow table and
several pages of disclosures.

| | |
|---|---|
| Pages | 28 |
| Fields in the extraction schema | 23 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:10 | 2026-11-19 03:17 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 82,520 | 84,683 |
| Words under 0.95 confidence | 253 | n/a |
| Words under 0.80 confidence | 68 | n/a |
| Words under 0.50 confidence | 22 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 22.0 s | 54.9 s |
| Per page | 0.8 s | 2.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 12.5 credits | 35.2 credits |
| Per page | 0.45 credits | 1.26 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:10 | 2026-11-19 03:18 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 220.6 s | 265.7 s |
| Per schema field (23) | 9.59 s | 11.55 s |
| Per value returned | 0.82 s | 2.23 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 24.7 credits | 20.5 credits |
| Per schema field (23) | 1.074 credits | 0.891 credits |
| Per value returned | 0.091 credits | 0.172 credits |

## Origin

`source/sample-new-fidelity-acnt-stmt.pdf` is Fidelity's sample monthly investment
report for July 2015, covering three accounts: an individual brokerage account, a
traditional IRA and a 529 education account. It is **28 pages, landscape (756×612)**,
with a full text layer. The last three pages are disclosures printed on 792×612 pages
rotated 90°.

| | |
|---|---|
| Publisher | Fidelity Investments |
| Source | [fidelity.com/…/sample-new-fidelity-acnt-stmt.pdf](https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/sample-new-fidelity-acnt-stmt.pdf) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

Fidelity publishes this sample on fidelity.com to show customers what a statement looks
like, and every page is marked "*** SAMPLE STATEMENT *** For informational purposes
only". All the personal data is specimen: the account holder is "John W. Doe, 100 Main
St.", the account numbers are 111-111111, 222-222222 and 333-333333, and the phone
numbers are Fidelity's and SIPC's published lines. No redaction was needed.

The consolidated 1099's rotated mailing panel was dropped. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A brokerage statement is the monthly record of what an investor holds and what changed.
It is one of the most common proofs of assets in finance.

- **Mortgage and consumer lending:** underwriters verify liquid assets and reserves
  from recent statements.
- **Wealth management and financial planning:** advisers read statements from other
  firms to consolidate a client's full picture.
- **Account transfers and onboarding:** receiving firms use statements to set up
  incoming transfers of holdings.
- **Tax preparation and accounting:** preparers check cost basis, income and
  distributions.
- **Estate settlement and divorce:** attorneys and fiduciaries inventory accounts and
  value them as of a date.

### What it contains

- **Long and varied content:** 28 pages of summaries, holdings, activity ledgers, an
  estimated cash flow table and dense disclosures.
- **Asset allocation pie charts.**
- **Holdings tables** for stocks, bonds, mutual funds and ETFs, with negative values for
  a short position and footnote markers attached to numbers.
- **The same structure repeated per account,** so a security name or account number
  appears in many places.
- **Values printed as words,** such as a cost basis printed "unknown".
- **Rotated pages.** The three closing disclosure pages are stored rotated 90°.
- **A printed typo** in the publisher's own figures: a beginning value of
  "$88,0853.95".
