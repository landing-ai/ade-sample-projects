# Auto loan statement

Source assets for `landing.ai/document-type/auto-loan-statement`.

## Sample document

`source/gm-financial-sample-auto-loan-statement.pdf` — GM Financial's sample monthly
account statement for a retail auto loan on a 2021 GMC Acadia Denali, dated
September 15, 2022. **2 pages, portrait, US Legal (8.5 × 14 in)**: page 1 is the
statement with a tear-off payment coupon; page 2 is the reverse side with the payment
allocation, payment options, general disclosures and a contact-update coupon.

| | |
|---|---|
| Publisher | GM Financial |
| Source | [gmfinancial.com/…/Sample-Statement.pdf](https://www.gmfinancial.com/content/dam/gmf/myaccount/documents/Sample-Statement.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

The lender's own specimen, served from its own domain. It is plainly a template: a large
SAMPLE watermark, a dealer block of "Dealership name / Address line 1 / City, State
01234 / 555-555-5555", business hours of "H a.m. to H p.m.", a lorem ipsum Account
Details block, and the placeholder borrower JOHN Q SMITH. The coupon's mailing address is
a commercial office address, not a residence. No redaction was needed.

The page content is used exactly as published. The PDF metadata's author field carried a
GM Financial employee's user ID, so the metadata (Info dictionary and XMP) was cleared.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

The collection's first **auto loan statement**, and a different shape from the mortgage
and HELOC statements already here:

- **A designed, marketing-style layout** (it was produced in Illustrator), with the key
  loan facts set as a large-type header and a graphical Account Details panel rather than
  in ruled tables.
- **A payment coupon that repeats the header values**, so the same amount appears more
  than once on the page and the occurrence matters.
- **A template that does not agree with itself.** The header and transactions are dated
  2022, the coupon's due date is October 15, 2020, and the payment allocation on page 2
  is dated 8/21/20 against 8/21/22 on page 1. Extraction returns each date as printed.

## Featured fields: what is owed on which car

All on page 1.

| Field | Value |
|---|---|
| Model year | 2021 |
| Vehicle | GMC ACADIA DENALI |
| Total amount due | $496.31 (statement header) |
| Current payment | $496.31 |
| Last payment received | $496.31 |

Total amount due is pinned to occurrence 1, the statement header; occurrence 0 is the
same figure on the payment coupon, which the request asked to avoid. Dates are avoided
for the reason above.

The request suggested the principal balance, term and account number too. They extract
correctly (12-digit account number, $42,328.50, 48 months) but cannot be illustrated:
see below.

## Grounding on this document

- **The Account Details panel was parsed as a chart.** DPT-3 Pro classified the panel
  (account number, payment progress bar, account opened, current principal balance,
  terms) as a `CHART` figure and reconstructed it as a two-column table. Values read from
  a figure carry no cell-level boxes: `account_number` grounds to the "Account Opened"
  label and `current_principal_balance` to "Terms", both one row adrift, and
  `term_months` has no ranges at all. The progress bar is probably what made the panel
  look like a chart.
- **Dates ground correctly** to their printed form ("SEPTEMBER 15, 2022", "9/17/22");
  `inspect_fields.py` flags them `OFF` only because they are normalized to ISO.
- **The dealer name lost a line.** The three-line "Chevrolet Buick GMC Cadillac" sits
  beside a three-line address, and the parse paired them line by line as key-value
  text, so `dealer_name` came back as "Chevrolet Buick GMC".
- The header, transaction table and page-2 payment allocation (principal $461.56,
  interest $34.75) all ground cleanly.

The schema has 23 leaf fields.

## Credits

6.00 credits at the standard tier (parse and extract, DPT-3 Pro, jobs API).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py auto-loan-statement      # spends credits
.venv/bin/python document-types/scripts/build_images.py auto-loan-statement # free
.venv/bin/python document-types/scripts/inspect_fields.py auto-loan-statement
```
