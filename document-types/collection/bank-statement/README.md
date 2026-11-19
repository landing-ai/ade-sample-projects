# Bank statement

**On the website:** [landing.ai/document-type/bank-statement](https://landing.ai/document-type/bank-statement)

Carson Bank's sample statement for a TRUE CHECKING account, for July 2019. It has an
account activity summary with a pie chart, a 47-row transaction register, a checks list,
a daily balance summary, and a linked overdraft line of credit with its interest
calculation, followed by a reconciliation form and disclosures.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 33 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:35 | 2026-11-19 02:32 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 18,763 | 20,820 |
| Words under 0.95 confidence | 65 | n/a |
| Words under 0.80 confidence | 37 | n/a |
| Words under 0.50 confidence | 5 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.6 s | 24.4 s |
| Per page | 1.1 s | 4.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.8 credits | 8.3 credits |
| Per page | 0.47 credits | 1.38 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:35 | 2026-11-19 02:32 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 33 | 33 |
| Non-null fields returned | 33 | 33 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 104.0 s | 115.1 s |
| Per schema field (33) | 3.15 s | 3.49 s |
| Per value returned | 0.43 s | 0.47 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 10.2 credits | 10.6 credits |
| Per schema field (33) | 0.309 credits | 0.321 credits |
| Per value returned | 0.042 credits | 0.043 credits |

## Origin

`source/carson-bank-sample-statement.pdf` is Carson Bank's sample statement for a **TRUE
CHECKING** account, July 2019. It is **6 pages, portrait (US Letter)**, created
digitally with a text layer. It has an account activity summary with a debits and
credits pie chart, a 47-row transaction register across two pages, a checks list, a
daily balance summary, a linked Ready Reserve overdraft line of credit with its interest
calculation, and a reconciliation form and disclosures.

| | |
|---|---|
| Publisher | Carson Bank (Mulvane, Kansas) |
| Source | [carsonbank.com/…/Sample-Statement.pdf](https://www.carsonbank.com/wp-content/uploads/2021/01/Sample-Statement.pdf) |
| Retrieved | 2026-09-29 |
| Clearance | Public |

This is the bank's own sample, published on its website. The holder and address are
specimen data ("JOHN TEST", "123 TEST", "YOUR CITY, KS"), the statement date is printed
"July 31, 20XX", and the account numbers are four-digit placeholders. The transactions
name a retailer, C&J Clark, and a store number, which is an organization rather than a
person. No redaction was needed.

This replaces a first choice. The page was first built from Manulife Bank's Manulife
One sample statement, which turned out to be a home-equity line of credit combined with
a mortgage. It now lives at `heloc-statement`. Full provenance is in `manifest.json`
under `source.origin`.

## Why this document

### Who processes it

A bank statement is the standard proof of what passed through an account and what was in
it on a given date.

- **Mortgage and consumer lending:** lenders verify an applicant's funds, deposits and
  recurring payments from recent statements.
- **Small-business lending:** underwriters read cash flow and balances to judge whether
  a business can carry a loan.
- **Accounting and bookkeeping:** statements are reconciled against the general ledger
  each month.
- **Tenant screening and income verification:** landlords and agencies check deposits
  to confirm stated income.
- **Audit and fraud review:** auditors and investigators trace transactions and check
  that the summary totals agree with the register.

### What it contains

- **A transaction register that runs over a page break,** with 47 rows and descriptions
  that wrap onto a second line.
- **A pie chart** whose labels repeat the deposit and withdrawal totals.
- **The same figures in several places:** balances appear in the summary, the register
  and a daily balance table, and in this sample they do not all agree.
- **Two accounts on one statement:** the checking account and a linked overdraft line
  of credit, each with its own account number and summary.
- **Checks in a three-column list,** with asterisks marking breaks in the number
  sequence.
- **A bank name drawn as vector artwork,** with no text behind it.
