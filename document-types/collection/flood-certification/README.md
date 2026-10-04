# Flood certification

Source assets for `landing.ai/document-type/flood-certification`.

## Sample document

`source/flood-certification.pdf` is a completed FEMA **Standard Flood Hazard
Determination Form** (SFHDF, form FF-206-FY-21-116). ServiceLink National Flood prepared
it in September 2023 for a residential mortgage from a bank lender, for a property in
Jackson Township, Ocean County, New Jersey. It has **3 pages, portrait (US Letter)**, with
a text layer:

1. The determination form: loan information, the NFIP community, the map panel, the
   flood zone, insurance availability, the Special Flood Hazard Area answer, HMDA codes
   and the preparer.
2. A short fee slip with the order number, loan number and fee.
3. The borrower notice, *Notice of Special Flood Hazards and Availability of Federal
   Disaster Relief Assistance*, with "Property NOT IN SFHA" checked.

| | |
|---|---|
| Publisher | ServiceLink National Flood, on FEMA's Standard Flood Hazard Determination Form |
| Source | https://www.scribd.com/document/671333520/Flood-Certificate (Scribd listing, shown as plain text) |
| Retrieved | 2026-10-03, downloaded manually by the operator because Scribd blocks scripted downloads |
| Clearance | Redacted |

Scribd is a user-upload site, not a publisher, so this was treated as a personal record.
**Redaction happened before anything was parsed.** It used `document-types/scripts/redact.py`,
which removes the underlying text rather than covering it. The rules file was kept
outside the repo. What was replaced:

| What | Replaced with | Occurrences |
|---|---|---|
| Borrower's name | SAMPLE, JANE Q | 2 |
| Property street address | 100 MAIN ST | 2 |
| ZIP+4 add-on of the property address | a random 4-digit add-on (the 5-digit ZIP is kept) | 2 |
| Lender's customer number with the preparer | a plausible random 10-digit number | 1 |
| Loan identifier | a plausible random 11-digit number | 3 |
| Flood order number | a plausible random 10-digit number | 3 |

Kept: the lender (a bank) and its address, ServiceLink, FEMA, the NFIP community and map
data, the town, state and 5-digit ZIP, and the HMDA census tract codes. These describe
organizations, a FEMA map and a neighbourhood, not a person. The form has no signatures
(the signature lines on page 3 are blank) and no barcodes. Its only image is the
preparer's logo. Document metadata was cleared. Verified: no original value is
extractable from the committed PDF, and none appears anywhere in this folder.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

This is the collection's first **flood determination**, a form attached to almost every
US mortgage file:

- **A federally standardized ruled form**, with lettered sections and numbered boxes.
- **The answers are checkboxes and radio buttons.** Program type, insurance
  availability, LOMC and, above all, the YES/NO SFHA determination are marks, not text.
  On page 3 the borrower notice that applies is chosen by a checked box.
- **The same facts appear on more than one page.** The loan and order numbers are on all
  three pages, and the community and map panel are repeated on the notice.

## Featured fields: the determination

All on page 1. The request suggested fields in its notes but named none formally.

| Field | Value |
|---|---|
| NFIP community | JACKSON, TOWNSHIP OF |
| NFIP community number | 340375 |
| Flood zone | X |
| In special flood hazard area | NO |
| Date of determination | September 05, 2023 |

These follow the chain of reasoning the form records: which community the property is
in, which flood zone the map puts it in, so whether it is in a Special Flood Hazard Area,
and when the determination was made. A lender's flood-compliance check reads exactly
these. Every featured field is impersonal.

The request's notes also suggested the **map panel number** and the **map panel
effective date**. Both extract correctly and their ranges are right, but they share a box
with the flood zone (see below), so they were left out. Three highlights on one region
would read as one.

## What it surfaced

**Section II.B collapsed into one cell.** The parse read the NFIP map grid (panel number,
effective date, LOMC, flood zone, No NFIP Map) as one table cell, with the sub-boxes
joined by `|`. The values are all correct and correctly ranged, but they can only be
boxed as the whole section. The flood zone crop therefore highlights all of II.B.
Section II.A, laid out in the same ruled style, did come back cell by cell.

**Checkboxes read correctly.** Both the SFHA YES/NO pair and the four notices on page 3
come back with the right box checked. The SFHA answer is extracted as the literal `NO`,
not as a boolean, so that it grounds to text on the page. A boolean grounds "off",
because `false` never appears in the document. Booleans elsewhere in the schema (LOMC,
No NFIP Map, the availability boxes) are right but flagged `OFF` for that reason.

**Dates ground only as printed.** With an ISO-date instruction, the panel effective date
and determination date came back normalized and were flagged `OFF`. The schema now asks
for them as printed.

**A blank amount becomes 0.** Box 5, amount of flood insurance required, is empty. It
comes back as `0` although the schema asks for null. The blank LOMC date and case number
come back as empty strings.

## Extraction

**41 leaf fields**: form number and OMB expiry, the lender, the collateral, the loan
identifier, amount required, NFIP community, NFIP map data and LOMC, insurance
availability, the SFHA determination, life-of-loan flag, HMDA codes, the preparer, the
determination date, order number, fee, and which borrower notice is checked.

## Credits

**11.0 credits at standard tier**: 7.5 for the parse and the first extraction, plus 3.5
for one re-extraction with `--extract-only` after the schema change for dates and the
SFHA answer.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py flood-certification            # parse + extract (spends credits)
.venv/bin/python document-types/scripts/run_ade.py flood-certification --extract-only
.venv/bin/python document-types/scripts/build_images.py flood-certification       # images, no API calls
.venv/bin/python document-types/scripts/inspect_fields.py flood-certification
```
