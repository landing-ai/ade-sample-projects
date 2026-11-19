# Audited financial statements

**On the website:** [landing.ai/document-type/audited-financial-statement](https://landing.ai/document-type/audited-financial-statement)

The audited financial statements of Family First, Inc., a Florida nonprofit, for the
year ended December 31, 2024. The package opens with the independent auditor's report,
then the four basic statements and their notes, and ends with the Single Audit section:
the schedule of federal and state awards, two compliance reports and the schedule of
findings.

| | |
|---|---|
| Pages | 27 |
| Fields in the extraction schema | 46 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:28 | 2026-11-19 02:27 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 56,360 | 56,389 |
| Words under 0.95 confidence | 47 | n/a |
| Words under 0.80 confidence | 18 | n/a |
| Words under 0.50 confidence | 5 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 16.1 s | 20.1 s |
| Per page | 0.6 s | 0.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.7 credits | 27.6 credits |
| Per page | 0.36 credits | 1.02 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:28 | 2026-11-19 02:27 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 46 | 46 |
| Non-null fields returned | 44 | 44 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 451.1 s | 189.4 s |
| Per schema field (46) | 9.81 s | 4.12 s |
| Per value returned | 3.27 s | 1.39 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 16.6 credits | 16.8 credits |
| Per schema field (46) | 0.361 credits | 0.365 credits |
| Per value returned | 0.120 credits | 0.124 credits |

## Origin

`source/family-first-2024-audited-financial-statements.pdf` is the audited financial
statements of **Family First, Inc.**, a Florida nonprofit, for the year ended
December 31, 2024, with the independent auditor's report from Schafer, Tschopp,
Whitcomb, Mitchell & Sheridan, LLP. It is **27 pages, all portrait except page 9**,
which is a landscape statement of functional expenses. The PDF has a text layer: it was
made from Excel and Word.

The package follows the usual order for a nonprofit that receives government money. It
opens with the auditor's opinion, then the four basic statements (financial position,
activities, functional expenses and cash flows) and the notes. Pages 19 to 27 hold the
Single Audit material: the Schedule of Expenditures of Federal Awards and State
Financial Assistance, two compliance reports from the auditor, and the Schedule of
Findings and Questioned Costs.

| | |
|---|---|
| Publisher | Family First, Inc. and its auditor; posted by the Florida Auditor General |
| Source | [flauditor.gov/…/2024 family first.pdf](https://www.flauditor.gov/pages/nonprofit_forprofit%20rpts/2024%20family%20first.pdf) |
| Linked from | [flauditor.gov/…/family first.htm](https://flauditor.gov/pages/nonprofit_forprofit%20pages/family%20first.htm) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

Nonprofits that receive Florida state financial assistance must file their audit
reports with the Auditor General, which posts them publicly. The text layer names no
individual. The auditor's reports are addressed to the Board of Directors. The
signatures on pages 6, 23 and 26 are the firm's name written by hand, not an
individual's signature. The firm's letterhead on pages 4, 22 and 24 is an image that
lists six partners by name, with the office address and phone number. The operator
chose to keep it as published. No redaction was made. The committed PDF is the
publisher's file, unaltered. It carries an owner-password permissions restriction and
opens without a password, and its metadata names only the audit firm. Full provenance
is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Audited statements are the version of a set of accounts that an independent firm has
checked, so anyone who funds, lends to or oversees an organization asks for them.

- **Commercial lending:** banks require audited statements for larger loans and test
  covenants against the balance sheet and cash flow figures.
- **Grantmakers and government agencies:** funders read the Single Audit schedules and
  findings before renewing awards.
- **State oversight offices:** offices like the Florida Auditor General collect and
  review the audits that recipients of state money must file.
- **Investors, donors and rating analysts:** they compare revenue, expenses and net
  assets across years and across organizations.
- **Accounting and audit firms:** staff tie the statements to the trial balance and
  reconcile the notes and schedules.

### What it contains

- **An opinion in prose.** The opinion type, the accounting framework, the report date
  and the signing city sit in the auditor's letter, under a letterhead image and above a
  handwritten firm signature.
- **Statements that tie together.** Total assets equal total liabilities and net
  assets, and the same totals appear on more than one statement.
- **Multi-column financial tables** with indented line items, subtotals and negative
  amounts.
- **A landscape page** for the statement of functional expenses in an otherwise
  portrait document.
- **A nested awards schedule.** Programs sit under grantors and subtotals under states,
  with CFDA and CSFA numbers and contract numbers in their own columns.
- **A findings summary** written as a numbered list of yes/no conclusions.
- **Long narrative notes** that run across several pages.
