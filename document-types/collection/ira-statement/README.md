# IRA statement

**On the website:** [landing.ai/document-type/ira-statement](https://landing.ai/document-type/ira-statement)

A monthly Premiere Select Rollover IRA statement for September 2025, issued through
Commonwealth Financial Network and carried by National Financial Services. It has a
summary with a portfolio value chart, an account overview with allocation, change in
value, retirement contributions and distributions, income and fees, a beneficiary
summary, holdings, activity, bank deposit detail, footnotes and a glossary.

| | |
|---|---|
| Pages | 10 |
| Fields in the extraction schema | 30 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:11 | 2026-11-19 03:23 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 42,884 | 43,058 |
| Words under 0.95 confidence | 111 | n/a |
| Words under 0.80 confidence | 36 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 10.4 s | 18.8 s |
| Per page | 1.0 s | 1.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.8 credits | 15.8 credits |
| Per page | 0.58 credits | 1.58 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:11 | 2026-11-19 03:24 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 30 | 30 |
| Non-null fields returned | 30 | 30 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 188.1 s | 721.3 s |
| Per schema field (30) | 6.27 s | 24.04 s |
| Per value returned | 2.07 s | 7.93 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 11.3 credits | 11.3 credits |
| Per schema field (30) | 0.377 credits | 0.377 credits |
| Per value returned | 0.124 credits | 0.124 credits |

## Origin

`source/ira-statement-redacted.pdf` is a monthly Premiere Select Rollover IRA statement
for September 1 to September 30, 2025. It is **10 pages, landscape (US Letter)**: a
summary with a portfolio value chart, an account overview (allocation, change in value,
retirement contributions and distributions, income, fees), a beneficiary summary and
messages, holdings, activity, bank deposit detail, footnotes and a glossary.

| | |
|---|---|
| Publisher | Commonwealth Financial Network (broker-dealer); account carried by National Financial Services LLC; advised by SageRock Wealth Partners |
| Source | [scribd.com/document/970556624](https://www.scribd.com/document/970556624) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted |

This is a real account holder's statement, uploaded to Scribd by a third party. It was
downloaded by hand, because Scribd blocks scripted requests. Scribd is not the
publisher, so the file is treated as a personal record. The listing's title ends in the
account number's last digits, so the URL is recorded without it.

These values were replaced, removing the underlying text rather than covering it:

| What | With |
|---|---|
| Account holder's name, in every page header and the mailing block | JOHN Q SAMPLE |
| Mailing address | 100 MAIN ST, ANYTOWN MI 00000 (state kept) |
| Account number, on every page | A plausible random stand-in of the same shape |
| Mail envelope code, on every page | Random letters of the same length |
| Three designated beneficiaries | JANE Q SAMPLE, ALEX Q SAMPLE, SAM Q SAMPLE |
| Two financial advisors' names, rep code and email | A ADVISOR / B ADVISOR, a random rep code, advisor@example.com |

Kept as printed: every balance, holding, transaction and fee, the beneficiaries'
allocations, relationships and designations, and the firms' names, business addresses,
phone numbers and website. The PDF metadata was cleared. Verified: no original value is
extractable from the committed PDF, no other line of text changed, and none appears in
any file in this folder. The stand-in name is shorter than the original, so the page
header leaves a gap before "- Premiere Select Rollover IRA".

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An IRA statement is the monthly record of an individual retirement account held at a
brokerage. It is a standard proof of retirement assets.

- **Mortgage lending:** underwriters count vested retirement assets toward reserves
  and verify them from recent statements.
- **Wealth management and financial planning:** advisers consolidate IRA holdings
  held at other firms into one plan.
- **Rollovers and account transfers:** receiving custodians use statements to set up
  incoming transfers.
- **Tax preparation:** preparers check contributions by tax year and distributions.
- **Estate settlement:** executors and attorneys identify designated beneficiaries and
  their allocations.

### What it contains

- **Three firms on one statement:** the broker-dealer, the clearing firm that carries the
  account and the advisory firm. The advisory firm appears only as a logo and in small
  print.
- **A beneficiary table** with allocations, relationships and primary or contingent
  status.
- **IRA-specific activity,** with contributions for the current and prior tax year and
  distributions reported apart from ordinary income.
- **A portfolio value chart** on the summary page.
- **Landscape pages with a brokerage holdings layout,** with multi-line security
  descriptions and estimated yield and income per holding.
- **Footnotes and a glossary** in small print.
