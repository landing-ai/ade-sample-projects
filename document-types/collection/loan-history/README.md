# Loan history

**On the website:** [landing.ai/document-type/loan-history](https://landing.ai/document-type/loan-history)

A Loan Payment History report for loan C-2, a $50,000 loan with an impound (escrow)
account, covering every payment from February 2010 to October 2014. A header names the
servicer, the loan and the borrower. One table lists 57 payments across thirteen
columns, from due and received dates to principal, interest, impound and fees, and
ends in a Total row. The data is fictitious.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 27 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:16 | 2026-11-19 03:34 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 12,550 | 12,669 |
| Words under 0.95 confidence | 0 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.0 s | 10.2 s |
| Per page | 2.0 s | 5.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.6 credits | 4.2 credits |
| Per page | 0.80 credits | 2.10 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:17 | 2026-11-19 03:34 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 27 | 27 |
| Non-null fields returned | 27 | 27 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 136.4 s | 173.7 s |
| Per schema field (27) | 5.05 s | 6.43 s |
| Per value returned | 0.19 s | 0.24 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 18.6 credits | 18.6 credits |
| Per schema field (27) | 0.689 credits | 0.689 credits |
| Per value returned | 0.026 credits | 0.026 credits |

## Origin

`source/loan-servicing-soft-loan-payment-history-sample.pdf` is a Loan Payment History
report for loan C-2, a $50,000 loan with an impound (escrow) account, covering every
payment from February 2010 to October 2014. It is **2 pages, landscape (US Letter)**: a
header with the servicer, loan and borrower, then one ruled table of 57 payments with
thirteen columns, carried over the page break with its header repeated, and a Total row.

| | |
|---|---|
| Publisher | Loan Servicing Soft Inc. (loan servicing software vendor) |
| Source | [loanservicingsoft.com/…/Loan_Payment_History-LOAN_SERVICING_SOFT-www.loanservicingsoft.com.pdf](https://www.loanservicingsoft.com/reports/Loan_Payment_History-LOAN_SERVICING_SOFT-www.loanservicingsoft.com.pdf) |
| Linked from | [loanservicingsoft.com/reports.html](https://www.loanservicingsoft.com/reports.html) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

This is demonstration output of the vendor's product, published on its sample reports
page. The data is fictitious: the servicer is "YOUR SERVICING COMPANY NAME" at 1234 Main
St, and the borrower is "Irene Impound", a pun on the report's impound column. No
redaction was needed.

Web research for a document showing the complete payment and servicing history of an
existing mortgage found that the most authoritative version, the loan payment history in
bankruptcy Official Form 410A (Mortgage Proof of Claim Attachment), is published only
blank; completed ones exist only in real bankruptcy filings. A software vendor's sample
report shows the same content with fictitious data. It has no real servicer's branding.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A loan payment history shows every payment made on a loan and how each one was applied.
It is the record people turn to when a loan changes hands or comes into dispute.

- **Mortgage servicers:** they produce and reconcile payment histories, and pass them on
  when servicing transfers.
- **Bankruptcy and foreclosure:** creditors attach a payment history to a proof of claim,
  and debtors' attorneys and trustees check it.
- **Loan sale and securitization due diligence:** buyers review pay histories to judge
  how a loan has performed.
- **Borrowers and housing counselors:** they review payments, fees and escrow to resolve
  disputes and plan modifications.
- **Auditors and regulators:** they test that payments, late fees and escrow were
  applied correctly.

### What it contains

- **One dense numeric table,** 57 rows by 13 columns, over two landscape pages.
- **A table split across a page break,** with its header repeated.
- **Irregular rows among regular ones:** a partial first payment numbered 0.3, late
  payments with late fees, a short payment with $0.00 to principal, and an impound
  increase in 2014.
- **Blank cells next to filled ones,** with the reference column blank, "000" or a
  number from row to row.
- **A wrapped column header** ("Impoun / d") and a Total row.
