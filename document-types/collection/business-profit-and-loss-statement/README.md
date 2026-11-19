# Business Profit and Loss Statement

**On the website:** [landing.ai/document-type/business-profit-and-loss-statement](https://landing.ai/document-type/business-profit-and-loss-statement)

Two QuickBooks profit and loss reports for Craig's Design and Landscaping Services,
the fictional sample company that ships with QuickBooks Online. The first compares
August 2017 with July 2017. The second covers January to August 2017. Each lists income
and expense accounts with subtotals, gross profit and net income.

| | |
|---|---|
| Pages | 2 |
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
| Processed (UTC) | 2026-11-19 02:36 | 2026-11-19 02:34 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 4,467 | 4,065 |
| Words under 0.95 confidence | 1 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.5 s | 5.9 s |
| Per page | 2.7 s | 3.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.8 credits | 2.1 credits |
| Per page | 0.40 credits | 1.05 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:36 | 2026-11-19 02:34 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 16 | 16 |
| Non-null fields returned | 16 | 16 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 159.0 s | 389.1 s |
| Per schema field (16) | 9.94 s | 24.32 s |
| Per value returned | 0.60 s | 1.34 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 8.0 credits | 8.9 credits |
| Per schema field (16) | 0.500 credits | 0.556 credits |
| Per value returned | 0.030 credits | 0.031 credits |

## Origin

`source/business-profit-and-loss-statement-score-quickbooks-sample.pdf` holds two
QuickBooks profit and loss reports for Craig's Design and Landscaping Services: a
month-over-month **Profit and Loss Comparison** (August 2017 against July 2017) and a
year-to-date **Profit and Loss** (January to August 2017). It is **2 pages, portrait**.

| | |
|---|---|
| Publisher | Champlain Valley SCORE, with Davis & Hodgdon Associates CPAs |
| Source | [2017-11 Need Answers About Accounting.pdf](https://s3.amazonaws.com/mentoring.redesign/s3fs-public/2017-11%20Need%20Answers%20About%20Accounting.pdf) |
| Retrieved | 2026-10-03, by script |
| Clearance | Public (nonprofit workshop handout; the company is Intuit's fictional sample company) |

The source is the handout for "Need Answers About Accounting?", a 2017-2018 education
series workshop run by the Champlain Valley chapter of SCORE, the SBA-affiliated
small-business mentoring nonprofit, with Davis & Hodgdon Associates CPAs presenting.
It is served from SCORE's own file store (the `mentoring.redesign` bucket behind
score.org), and every page carries both the Champlain Valley SCORE and Davis & Hodgdon
logos. The score.org page that links the file could not be confirmed, because the
chapter site refuses scripted requests, so provenance rests on the file store and the
branding.

The original PDF is 16 pages: a balance sheet comparison, the two profit and loss
reports, cash-flow statement templates, the workshop slides and a reprinted accounting
software review. This folder keeps **pages 2 and 3 only**.

Craig's Design and Landscaping Services is the fictional sample company that ships with
QuickBooks Online, so every figure is demonstration data, and small: hundreds of
dollars a month. No person is named. Nothing needed redacting. The PDF metadata was
reset to the publisher and a title naming the report. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A profit and loss statement is the basic record of how a business made or lost money
over a period. Small businesses usually produce it straight from their accounting
software, as here.

- **Small-business and SBA lending:** lenders read recent and year-to-date P&Ls to
  judge whether a business can carry a loan.
- **Bookkeeping and accounting firms:** they review and adjust client P&Ls at month end
  and year end.
- **Tax preparation:** preparers map P&L accounts onto business tax returns.
- **Merchant cash advance and alternative lenders:** underwriters compare reported
  income with bank deposits.
- **Business mentoring and advisory:** advisers, like SCORE here, use P&Ls to coach
  owners on their finances.

### What it contains

- **A nested chart of accounts.** Accounts sit two and three levels deep, and the same
  account name (Job Materials, Plants and Soil) appears under both income and expenses.
- **Comparison columns with gaps.** The comparison report has a current-period and a
  prior-period column, and many lines are blank in one of them.
- **Subtotal and total rows** at each level of the hierarchy.
- **Negative amounts in QuickBooks style.** August's loss is printed `$ -19.68`, with
  the sign separated from the currency symbol.
- **Two reports in one file,** each with its own title, period and column layout.
- **Publisher logos** on every page, from the workshop handout the reports came from.
