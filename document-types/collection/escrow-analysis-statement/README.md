# Escrow analysis statement

Source assets for `landing.ai/document-type/escrow-analysis-statement`.

## Sample document

`source/onity-escrow-analysis-statement-sample.pdf` — Onity Mortgage's sample annual
escrow analysis statement for a loan whose escrow account has a shortage. **2 pages,
portrait, US Legal (8.5 x 14 in)**, with a text layer. Page 1 is the letter: the new
monthly payment, what changed in taxes and insurance, and the shortage calculation.
Page 2 holds the 12-month projection and the past year's escrow account history.

| | |
|---|---|
| Publisher | Onity Mortgage (formerly Ocwen / PHH), NMLS 2726 |
| Source | [mortgagequestions.com/…/Escrow-Statement-Sample-Shortage.pdf](https://www.mortgagequestions.com/getattachment/f9ef11d4-d1dc-46a1-b478-96c6b88ed36b/Escrow-Statement-Sample-Shortage.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

The servicer's own specimen, hosted on its MortgageQuestions.com domain and loaded by its
escrow guide at <https://www.mortgagequestions.com/Escrow/Guide>. The borrower, mailing
and property address, and account number are obvious placeholders ("JOHN SMITH",
"123 YOUR ST.", "CITY, ST", 1234567890). The only phone, fax and PO box numbers are
Onity's own published contact details. No redaction was needed.

The original PDF has three pages. The third, a generic FAQ, was dropped; pages 1 and 2
are unchanged.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

The collection's first **escrow analysis statement**, and a document that is mostly
arithmetic laid out across awkward structures:

- **Prose beside tables.** Page 1 pairs left-column callouts and explanations with
  right-column tables, the layout that has caused label-to-value pairing errors before.
  Here the headline $1,448.71 sits in a callout to the left of a table that prints the
  same figure again.
- **Current against new.** Payment components and annual tax and insurance amounts are
  each printed in two columns, so every value has to land in the right one.
- **A history table with merged group headers and flags.** Estimated and actual columns
  sit under three spanning headers, and actual values carry `*` (differs from projection)
  and `E` (estimated, not yet happened) flags.

## Featured fields: the shortage and what it does to the payment

All on page 1. The request suggested a shortage-and-payment-change story; these tell it:

| Field | Value |
|---|---|
| New monthly mortgage payment | $1,448.71 |
| Current escrow payment | $550.04 |
| New escrow payment | $582.83 |
| Shortage amount | $814.27 |
| New annual escrow total | $6,993.90 |

The new annual total divided by 12 is the new escrow payment, and the shortage spread over
12 months ($67.86) plus the new escrow payment and unchanged principal and interest is the
new monthly payment. The new monthly payment pins the large headline figure in the
Section 1 callout (occurrence 1), not the copy in the payment table.

**Two suggested fields were left out.** The statement date and the payment's effective
date extract correctly, normalized to 2026-03-23 and 2025-11 from "March 23, 2026" and
"November 2025". Because the extracted value does not appear verbatim in the boxed text,
`inspect_fields.py` marks both as OFF, so neither is featured.

## What it surfaced

**Every value on both pages came back correct.** All 9 payment-table values, both annual
disbursement rows and totals, the shortage calculation, the low point ($351.38 in July
2026 against a required $1,165.65), all 12 projection rows and all 12 history rows match
the page. Left-column prose and right-column tables on page 1 did not cause any
mispairing.

**The flags were read, not copied into the numbers.** All 12 history rows are marked as
differing from projection (`*`), only October 2025 is marked `E`, and the flagged values
(`550.04 *`, `1700.00 *`) come back as plain numbers.

**Blank cells are inconsistent.** Blank projection descriptions come back as the string
`"null"`, not a JSON null, and blank history descriptions as an empty string. Blank
"paid from escrow" cells come back as 0 rather than null, though the schema allows null.

**The specimen's dates disagree with each other.** The statement is dated March 23, 2026,
and the new payment takes effect November 2025, before the statement date. Extraction
returns both as printed.

## Extraction

**45 leaf fields**: servicer, statement date, account, borrower and property address, the
analysis outcome, the payment comparison table, the annual disbursements by type, the
shortage calculation, the projection with its low point and monthly rows, and the
history with its monthly rows and flags.

## Cost

**11.90 credits** at standard tier for 2 pages: 3.60 to parse, 8.30 to extract.

## Regenerating

```bash
# Source: pages 1-2 of the downloaded PDF (page 3, a FAQ, dropped with PyMuPDF).
.venv/bin/python document-types/scripts/run_ade.py escrow-analysis-statement                # 11.90 credits
.venv/bin/python document-types/scripts/run_ade.py escrow-analysis-statement --extract-only # 8.30, schema iteration
.venv/bin/python document-types/scripts/build_images.py escrow-analysis-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py escrow-analysis-statement --page 1
```
