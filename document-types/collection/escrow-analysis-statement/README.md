# Escrow analysis statement

**On the website:** [landing.ai/document-type/escrow-analysis-statement](https://landing.ai/document-type/escrow-analysis-statement)

Onity Mortgage's sample annual escrow analysis statement for a loan whose escrow
account has a shortage. The first page explains the new monthly payment, what changed
in taxes and insurance, and how the shortage was calculated. The second page holds the
12-month projection and the past year's escrow account history.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 45 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:56 | 2026-11-19 03:01 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 10,064 | 10,277 |
| Words under 0.95 confidence | 30 | n/a |
| Words under 0.80 confidence | 14 | n/a |
| Words under 0.50 confidence | 11 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.3 s | 25.6 s |
| Per page | 7.7 s | 12.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.4 credits | 3.6 credits |
| Per page | 0.70 credits | 1.80 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:56 | 2026-11-19 03:02 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 45 | 45 |
| Non-null fields returned | 44 | 44 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 442.3 s | 233.0 s |
| Per schema field (45) | 9.83 s | 5.18 s |
| Per value returned | 2.37 s | 1.25 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 8.3 credits | 8.3 credits |
| Per schema field (45) | 0.184 credits | 0.184 credits |
| Per value returned | 0.044 credits | 0.044 credits |

## Origin

`source/onity-escrow-analysis-statement-sample.pdf` is Onity Mortgage's sample annual
**escrow analysis statement** for a loan whose escrow account has a shortage. It is **2
pages, portrait, US Legal (8.5 x 14 in)**, with a text layer. Page 1 is the letter: the
new monthly payment, what changed in taxes and insurance, and the shortage calculation.
Page 2 holds the 12-month projection and the past year's escrow account history.

| | |
|---|---|
| Publisher | Onity Mortgage (formerly Ocwen / PHH), NMLS 2726 |
| Source | [mortgagequestions.com/…/Escrow-Statement-Sample-Shortage.pdf](https://www.mortgagequestions.com/getattachment/f9ef11d4-d1dc-46a1-b478-96c6b88ed36b/Escrow-Statement-Sample-Shortage.pdf) |
| Linked from | [mortgagequestions.com/Escrow/Guide](https://www.mortgagequestions.com/Escrow/Guide) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

This is the servicer's own specimen, hosted on its MortgageQuestions.com domain and
loaded by its escrow guide. The borrower, mailing and property address, and account
number are obvious placeholders ("JOHN SMITH", "123 YOUR ST.", "CITY, ST", 1234567890).
The only phone, fax and PO box numbers are Onity's own published contact details. No
redaction was needed.

The original PDF has three pages. The third, a generic FAQ, was dropped; pages 1 and 2
are unchanged. The specimen's dates disagree with each other: the statement is dated
March 23, 2026, and the new payment takes effect November 2025. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Mortgage servicers send an escrow analysis every year to borrowers whose taxes and
insurance are paid from an escrow account. It resets the monthly payment and explains any
shortage or surplus.

- **Mortgage servicing:** servicers produce the analysis and answer borrower questions
  about payment changes.
- **Mortgage lending and refinancing:** underwriters use the current escrow payment and
  tax and insurance amounts to calculate housing expense.
- **Loan boarding and servicing transfers:** a new servicer checks escrow balances and
  disbursements against the prior servicer's history.
- **Housing counseling and loss mitigation:** counselors review shortage calculations
  when a borrower's payment jumps.
- **Compliance and audit:** reviewers check the analysis against RESPA escrow rules,
  including the cushion and the low point.

### What it contains

- **Prose beside tables.** Page 1 pairs left-column callouts and explanations with
  right-column tables, and the headline payment sits in a callout next to a table that
  prints the same figure again.
- **Current against new columns.** Payment components and annual tax and insurance
  amounts are each printed twice, so every value has to land in the right column.
- **A 12-row monthly projection** with a marked low point.
- **A history table with merged group headers and flags.** Estimated and actual columns
  sit under three spanning headers, and actual values carry `*` and `E` flags.
- **Arithmetic that ties together:** the annual total, shortage and payment change all
  follow from one another.
- **Blank cells** in descriptions and payment columns.
