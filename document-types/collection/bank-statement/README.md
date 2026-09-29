# Bank statement

Source assets for `landing.ai/document-type/bank-statement`.

## Sample document

`source/carson-bank-sample-statement.pdf` — Carson Bank's sample statement for a TRUE
CHECKING account, July 2019. **6 pages, portrait (US Letter)**: an account activity
summary with a debits and credits pie chart, a 47-row transaction register across two
pages, a checks list, a daily balance summary, a linked Ready Reserve overdraft line of
credit with its interest calculation, and a reconciliation form and disclosures.

| | |
|---|---|
| Publisher | Carson Bank (Mulvane, Kansas) |
| Source | [carsonbank.com/…/Sample-Statement.pdf](https://www.carsonbank.com/wp-content/uploads/2021/01/Sample-Statement.pdf) |
| Retrieved | 2026-09-29 |
| Clearance | Public |

The bank's own sample, published on its website. The holder and address are specimen data
("JOHN TEST", "123 TEST", "YOUR CITY, KS"), the statement date is printed "July 31, 20XX",
and the account numbers are four-digit placeholders. The transactions name a retailer,
C&J Clark, and a store number, which is an organization rather than a person. No
redaction was needed.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

**This replaces a first choice.** The page was first built from Manulife Bank's Manulife
One sample statement, which turned out to be a home-equity line of credit combined with a
mortgage rather than a standard bank statement. It now lives at `heloc-statement`.

## Why this document

The collection's first **standard checking statement**:

- **A register that runs over a page break.** 47 transactions across pages 1 and 2, with
  descriptions that wrap onto a second line.
- **The same figures in several forms.** The summary totals are printed again as pie
  chart labels, and balances appear in the summary, the register and a daily balance
  table.
- **Two accounts on one statement.** The checking account and a linked overdraft line of
  credit, each with its own account number and summary.
- **Checks in a three-column list,** with asterisks marking breaks in the number sequence.

## Featured fields: what a lender verifies

All on page 1. At the document owner's request, these are the fields a lender reads from a
bank statement to verify an applicant's funds:

| Field | Value |
|---|---|
| Institution | CARSON BANK |
| Account holder | JOHN TEST |
| Account number | 6547 |
| Statement date | July 31, 20XX |
| Ending balance | $6,682.22 |

Inflows and outflows are extracted but not featured; for lending, what matters is who
holds the account, where, and what was in it on the statement date. The account holder
is specimen data. The ending balance grounds to its whole row of the summary table
(label, date and amount). The statement date is kept as printed, since the sample's year
is "20XX".

## What it surfaced

**The sample does not agree with itself, and extraction does not smooth it over.** The
summary's previous and ending balances are $3,005.93 and $6,682.22. The transaction
register runs from $445.28 to $942.82, and its own running balance is consistent row by
row. The page 3 daily balance summary follows neither. The summary's $6.00 service charge
differs from the register's $10.00 service charge and $3.00 paper statement charge.
Extraction returns every figure as printed, so a reconciliation check downstream would
catch every one of these.

**The register extracts completely.** All 47 transactions match the page on date,
description, amount and running balance, including across the page break and where
descriptions wrap. All 8 checks come back, with both sequence breaks flagged.

**The bank name is read from artwork.** The CARSON BANK wordmark is vector drawing
with no text behind it, so a PDF text extractor finds nothing there. The parse reads the
name off the drawing, and extraction grounds the institution to it.

**The chart labels ground too.** The pie chart's "$18,041.50" and "$14,365.21" labels are
the second occurrence of the deposits and withdrawals totals, so the values are found in
the graphic as well as in the table.

**Two small misses.** An empty Credits cell sometimes comes back as 0 rather than null.
The checks list is read column by column in a different order from the page's, though
every check is there.

## Extraction

**33 leaf fields**: the bank, holder, account and statement date, the twelve-value
activity summary, the transactions, the checks, and the overdraft line. Everything
extracts correctly apart from the small misses above.

## Cost

**18.20 credits** at standard tier for 6 pages: 7.90 to parse, 10.30 to extract.

## Regenerating

```bash
curl -sSL -o document-types/collection/bank-statement/source/carson-bank-sample-statement.pdf \
  "https://www.carsonbank.com/wp-content/uploads/2021/01/Sample-Statement.pdf"
.venv/bin/python document-types/scripts/run_ade.py bank-statement                # 18.20 credits
.venv/bin/python document-types/scripts/run_ade.py bank-statement --extract-only # 10.30, schema iteration
.venv/bin/python document-types/scripts/build_images.py bank-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py bank-statement --page 1
```
