# 401(k) statement

**On the website:** [landing.ai/document-type/401k-statement](https://landing.ai/document-type/401k-statement)

A quarterly participant statement for the Publix Super Markets, Inc. 401(k) SMART Plan,
administered by Voya Financial, for January 1 to March 31, 2023. It shows the account
value and its history, an estimated retirement income, holdings by fund, contribution
rates and elections, and the quarter's account activity.

| | |
|---|---|
| Pages | 7 |
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
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:25 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 25,400 | 26,966 |
| Words under 0.95 confidence | 75 | n/a |
| Words under 0.80 confidence | 24 | n/a |
| Words under 0.50 confidence | 5 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 30.3 s | 42.1 s |
| Per page | 4.3 s | 6.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.6 credits | 10.3 credits |
| Per page | 0.51 credits | 1.47 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:26 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 25 | 25 |
| Non-null fields returned | 25 | 25 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 303.6 s | 57.4 s |
| Per schema field (25) | 12.15 s | 2.30 s |
| Per value returned | 6.46 s | 1.22 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.5 credits | 6.8 credits |
| Per schema field (25) | 0.260 credits | 0.272 credits |
| Per value returned | 0.138 credits | 0.145 credits |

## Origin

`source/401k-statement-redacted.pdf` is a quarterly statement for the Publix Super
Markets, Inc. 401(k) SMART Plan, administered by Voya Financial, for January 1 to March
31, 2023. It is **7 pages, portrait (US Letter)**: an account summary with a balance
history chart, an estimated retirement income illustration, holdings by fund,
contribution rates and investment elections, an account activity table, fees and
messages, and two scanned plan-sponsor inserts (fund performance, and news about the
company match and Publix stock dividends).

| | |
|---|---|
| Publisher | Voya Financial, recordkeeper for the Publix Super Markets, Inc. 401(k) SMART Plan |
| Source | [scribd.com/document/816135454](https://www.scribd.com/document/816135454/Safari) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted |

This is a real participant's statement, saved to PDF from Safari on an iPhone and
uploaded to Scribd under the title "Safari". Scribd is not the publisher, so the file is
treated as a personal record. It was downloaded by hand because Scribd blocks scripted
requests.

The personal details were replaced with `document-types/scripts/redact.py`, which removes
the underlying text rather than covering it:

| What | With |
|---|---|
| Participant's name, on every page | JANE Q SAMPLE |
| Street address | 100 MAIN ST |
| City, state and ZIP | ANYTOWN FL  00000 (state kept) |
| Employee number | A plausible random stand-in, keeping the leading zeros |

Kept as printed: the plan, sponsor and recordkeeper, every balance, fund and price, the
contribution rates and elections, the payroll location code, and the two scanned
inserts. None of these identifies the participant once the name, address and employee
number are gone. The PDF metadata was cleared. No original value is extractable from the
committed PDF, no other line of text changed, and no original value appears in any file
in this folder. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A 401(k) statement is the quarterly record of a worker's retirement savings: what went
in, how it is invested and what it is worth.

- **Mortgage and consumer lending:** lenders verify retirement assets as reserves, and
  check the balance and the statement date.
- **Financial advisors and wealth managers:** they consolidate statements from many
  recordkeepers to see a client's full holdings and contribution rates.
- **Rollover and account transfer teams:** receiving institutions read the plan,
  holdings and balances to move money out of an employer plan.
- **Divorce and estate attorneys:** retirement accounts are divided or valued from the
  statements as of a given date.
- **Plan sponsors and auditors:** employers and their auditors check contributions and
  the company match against payroll.

### What it contains

- **Designed panels and icon rows** in the recordkeeper's colors, with figures set in
  large type inside banners.
- **A bar chart** of the account balance history.
- **Tables of holdings and account activity,** with units, prices and values per fund,
  and an internal transfer between employer stock and its cash component.
- **Contribution rates and investment elections** by category.
- **Scanned pages inside a digital PDF.** Pages 6 and 7 are images of the plan sponsor's
  inserts, including a fund performance table, so their text has to be read from the
  page image.
