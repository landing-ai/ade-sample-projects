# Closing Disclosure

Source assets for `landing.ai/document-type/closing-disclosure`.

## Sample document

`source/closing-disclosure.pdf` — the Consumer Financial Protection Bureau's filled
sample of the TRID Closing Disclosure for a purchase loan, dated April 15, 2013. **5 pages,
portrait (letter)**: loan terms, projected payments and costs at closing on page 1;
itemized closing cost details on page 2; the cash-to-close calculation and summaries of
the borrower's and seller's transactions on page 3; loan disclosures and the escrow
account on page 4; loan calculations, other disclosures and contact information on page 5.

| | |
|---|---|
| Publisher | Consumer Financial Protection Bureau |
| Source | [files.consumerfinance.gov/f/201311_cfpb_kbyo_closing-disclosure.pdf](https://files.consumerfinance.gov/f/201311_cfpb_kbyo_closing-disclosure.pdf) |
| Retrieved | 2026-10-03 |
| Clearance | Public |

The CFPB links this file from its Closing Disclosure explainer page and publishes it for
general use. It is the same form content as Regulation Z Appendix H-25(B), without the
cover sheet. Every party is a specimen placeholder: the borrowers, sellers, Ficus Bank,
Epsilon Title Co., "Anywhere Street" and "Somewhere Drive" addresses, phone numbers such as
123-456-7890 and made-up email domains. The file was downloaded directly by script. No
redaction was needed.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's **closing-stage mortgage document**, the federally mandated summary a
borrower receives three days before closing. It sits after the rate lock and alongside
the title documents already here.

- **A dense, regulated layout.** Five pages of fixed sections, lettered A to N, with
  borrower-paid, seller-paid and paid-by-others columns, each split into at-closing and
  before-closing.
- **The same number in several places.** Closing costs and cash to close appear on page 1
  and again on pages 2 and 3; the payment appears in Loan Terms and in Projected Payments.
  A field has to be pinned to the occurrence a reader expects.
- **Arithmetic across pages.** Page 1's totals are sums of page 2's sections, which a
  consumer of the extraction can check.

## Featured fields: what the loan costs, monthly and at closing

All on page 1. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| Interest rate | 3.875% |
| Monthly principal and interest | $761.78 |
| Estimated total monthly payment (years 1-7) | $1,050.26 |
| Closing costs | $9,712.10 |
| Cash to close | $14,147.26 |

Page 1 read top to bottom the way a borrower reads it: the rate, the monthly payment it
produces, the all-in payment while mortgage insurance applies, and what is due at closing.

The request's notes suggested loan amount, interest rate, monthly P&I, the prepayment
penalty and cash to close. Interest rate, monthly P&I and cash to close are featured.
**Loan amount** is extracted correctly but `inspect_fields.py` marks it OFF, the number
162000 against the printed "$162,000", so it was left out. The **prepayment penalty
maximum** ($3,240) grounds to the whole "YES • As high as $3,240…" cell, also OFF. The
header dates the notes said to avoid are extracted as ISO dates and are OFF as well.

## What it surfaced

**Page 1 grounds cell by cell.** Every featured value boxes exactly its cell in the Loan
Terms, Projected Payments and Costs at Closing tables, including the Years 1-7 column of
a two-column table.

**Ten values are right but synthesized.** The four borrower-transaction totals on page 3
(due from borrower, paid already, deposit, seller credit), the J. Total Closing Costs
line on page 2, and all five Loan Calculations on page 5 (total of payments, finance
charge, amount financed, APR, TIP) came back with no ranges, although every one is in
the parse markdown as its own table cell. They cannot be illustrated. The seller's
transaction totals on the same page 3 ground normally.

**The PDF carries text that is not on the page.** Its text layer holds a filled-in
Mortgage Broker column on page 5, with a company, address, contact and IDs, but the
column prints empty. ADE parsed what is visible and returned the column empty, so the
lender's NMLS ID comes back as an empty string rather than the broker's hidden one. A
text-layer extractor would have picked it up.

**Lender credits come back null.** Page 2's Lender Credits line is blank, and page 1
prints "– $0 in Lender Credits". The schema allows null for this field.

**Booleans and percentages from prose.** The escrow-account checkbox, the late fee
("5% of the monthly principal and interest payment") and the YES/NO features extract
correctly, but ground to the whole sentence or cell, so they read as OFF.

## Extraction

**59 leaf fields**: closing, transaction and loan information from the header; loan
terms; the projected payments table; costs at closing; the section totals of closing
cost details; the borrower's and seller's transaction totals; the escrow account; late
payment terms; loan calculations; and the lender's contact column.

## Cost

**23.10 credits** at standard tier for 5 pages: 15.90 for the first parse and extract,
and 7.20 for one extraction re-run after making `lender_credits` nullable. A fresh run
costs about 15.90.

## Regenerating

```bash
curl -sSL -o document-types/collection/closing-disclosure/source/closing-disclosure.pdf \
  "https://files.consumerfinance.gov/f/201311_cfpb_kbyo_closing-disclosure.pdf"
.venv/bin/python document-types/scripts/run_ade.py closing-disclosure                # ~15.90 credits
.venv/bin/python document-types/scripts/run_ade.py closing-disclosure --extract-only # ~7.20, schema iteration
.venv/bin/python document-types/scripts/build_images.py closing-disclosure           # free
.venv/bin/python document-types/scripts/inspect_fields.py closing-disclosure --page 1
```
