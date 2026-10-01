# Loan history

Source assets for `landing.ai/document-type/loan-history`.

## Sample document

`source/loan-servicing-soft-loan-payment-history-sample.pdf` — a Loan Payment History
report for loan C-2, a $50,000 loan with an impound (escrow) account, covering every
payment from February 2010 to October 2014. **2 pages, landscape (US Letter)**: a header
with the servicer, loan and borrower, then one ruled table of 57 payments with
thirteen columns, carried over the page break with its header repeated, and a Total row.

| | |
|---|---|
| Publisher | Loan Servicing Soft Inc. (loan servicing software vendor) |
| Source | [loanservicingsoft.com/…/Loan_Payment_History-LOAN_SERVICING_SOFT-www.loanservicingsoft.com.pdf](https://www.loanservicingsoft.com/reports/Loan_Payment_History-LOAN_SERVICING_SOFT-www.loanservicingsoft.com.pdf) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

Demonstration output of the vendor's product, published on its
[sample reports page](https://www.loanservicingsoft.com/reports.html). The data is
fictitious: the servicer is "YOUR SERVICING COMPANY NAME" at 1234 Main St, and the
borrower is "Irene Impound", a pun on the report's impound column. No redaction was
needed.

**How it was chosen.** Web research for a document showing the complete payment and
servicing history of an existing mortgage found that the most authoritative version,
the loan payment history in bankruptcy Official Form 410A (Mortgage Proof of Claim
Attachment), is published only blank; completed ones exist only in real bankruptcy
filings. A software vendor's sample report shows the same content with fictitious data.
It has no real servicer's branding.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **loan servicing history**, and its densest numeric table:

- **One table, 57 rows, 13 columns,** over two landscape pages, nearly all numbers.
- **Irregular rows among regular ones.** A partial first payment numbered 0.3, two late
  payments with $43.88 late fees, one short payment with $0.00 to principal, and an
  impound increase from $100.00 to $108.33 in 2014.
- **Blank cells next to filled ones.** The reference column is blank, "000" or a number
  from row to row.
- **A Total row** that the rows must add up to, and a wrapped column header ("Impoun /
  d").

## Featured fields: one problem payment

All on page 1, from a single row, payment 7. The request named no fields, so these were
chosen:

| Field | Value |
|---|---|
| Date due | 2010-09-01 |
| Date received | 2010-09-20 |
| Late fee | 22.25 |
| Applied to principal | 0.00 |
| Principal balance | 49864.47 |

The kind of row a servicing review is looking for: due September 1, received September
20 with a late fee, and short of the scheduled payment, so nothing was applied to
principal and the balance stayed where it was the month before.

## What it surfaced

**Every value grounds to its own cell.** Across all 57 rows the boxes land on single
table cells, dates included, so any row can be illustrated cleanly.

**The table extracts completely and adds up.** All 57 rows come back across the page
break, every value matches the page, no payment number is missing, and the column sums
equal the printed Total row to the cent: $30,581.66 received, of which $1,570.25
principal, $23,238.12 interest, $5,641.65 impound and $131.64 late fees.

**Blank is an empty string.** Blank reference numbers come back as empty strings rather
than null, which is harmless here.

## Extraction

**27 leaf fields**: servicer, loan and borrower, the date range, every payment row's
thirteen columns, and the totals.

## Cost

**22.80 credits** at standard tier for 2 pages: 4.20 to parse, 18.60 to extract. The
extraction cost is driven by the 57-row array.

## Regenerating

```bash
curl -sSL -o document-types/collection/loan-history/source/loan-servicing-soft-loan-payment-history-sample.pdf \
  "https://www.loanservicingsoft.com/reports/Loan_Payment_History-LOAN_SERVICING_SOFT-www.loanservicingsoft.com.pdf"
.venv/bin/python document-types/scripts/run_ade.py loan-history                # 22.80 credits
.venv/bin/python document-types/scripts/run_ade.py loan-history --extract-only # 18.60, schema iteration
.venv/bin/python document-types/scripts/build_images.py loan-history           # free
.venv/bin/python document-types/scripts/inspect_fields.py loan-history --page 1
```
