# SBA Form 413

Source assets for `landing.ai/document-type/sba-form-413`.

## Sample document

`source/sba-form-413.pdf`: a completed SBA Form 413, Personal Financial Statement (05-21
edition). This is the form an SBA loan applicant, owner or guarantor fills in for a
7(a), 504, disaster or surety bond application, or for the WOSB or 8(a) programs. It is
**6 pages, portrait**:

- Page 1: program checkboxes and instructions
- Page 2: applicant details, the assets and liabilities balance sheet, income and
  contingent liabilities
- Page 3: supporting schedules (notes payable, stocks, real estate, other property)
- Page 4: more schedules and the certification
- Pages 5–6: statutory notices

| | |
|---|---|
| Publisher | U.S. Small Business Administration (the form). It was completed by an unidentified filer |
| Source | scribd.com/document/567494949/completed-sba-form-413 (shown as plain text, not linked) |
| Retrieved | 2026-10-03, downloaded manually by the operator (Scribd blocks scripted downloads) |
| Clearance | **Redacted**: see below |

## This document was redacted before it was parsed

Scribd is a user-upload site, not a publisher, so this was treated as a personal record.
Some of the values look illustrative rather than real, but the business name and address
could belong to a real business, so every identifying field was replaced.

**The form is a fillable AcroForm, and the values lived only in its form fields, not in
the page text.** Page-text redaction would have found nothing to remove. Each field's
stored value (`/V`) and its appearance stream were replaced instead. Then
`scripts/redact.py` cleared the PDF metadata and checked that no original text was
extractable.

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Applicant's name | 2 | `Jane Q Sample` |
| Business name | 1 | `Sample Bookstore` |
| Home street address | 1 | `100 Main St.` |
| Home city, state and ZIP | 1 | `Anytown, SD 57000` |
| Business address | 1 | `200 MAIN ST, Anytown, SD 57000` |
| Business and home phones | 2 | reserved `555-01xx` numbers |
| Social security number | 1 | `987-65-4324` (reserved range) |
| PDF metadata (`/Info`, XMP) | — | removed |

Checks run:

- The page text, the form fields, every decompressed PDF object and the raw file bytes
  were searched, and none contains an original value.
- `ship.py check` found no original value anywhere in this folder, checking literal text
  and runs of digits.

The rules file that maps originals to replacements is kept outside the repo.

There was nothing else to replace:

- **No signature.** Both signature fields are empty, so the form is unsigned.
- **No spouse.**
- **No account or loan numbers.**
- **No real estate.** Section 4 reads N/A.

Dollar amounts, checkboxes and dates were left unchanged.

**Integrity check.** The previous Scribd candidate for this type was an altered document,
so this one was checked before use, and nothing suggests editing:

- **The figures agree.** The asset lines sum to total assets, and total liabilities plus
  net worth equals total assets.
- **The dates agree.** The as-of date matches the signature-block date, and both fall
  within the form's OMB expiry date.
- **The file is the SBA's own Word-to-Acrobat form, saved once.** It has a single
  revision, and every value sits in a form field whose appearance matches its stored
  value. No text has been laid over the page.

## Why this document

It is a government form completed in form fields rather than printed text, and the
collection has few such forms. It tests a balance sheet laid out as two dotted-leader
columns, checkbox groups for program and business type, and a section-based form whose
supporting schedules are mostly blank. The data is sparse: only page 2 carries real
figures, so most of the 53-leaf schema resolves to zeros or blanks.

## Featured fields: the balance sheet balancing

All on page 2:

| Field | Value |
|---|---|
| Business type | Sole Proprietor |
| Total assets | 23,000 |
| Total liabilities | 0 |
| Net worth | 23,000 |

The request suggested the 7(a) program checkbox alongside the three totals. That
checkbox is on page 1, so it cannot share page 2's overlay, and its grounding reads OFF
in any case: the box covers the whole checkbox line. The checked business-type box
replaced it. The as-of date was the other candidate, but its box covers the label rather
than the date.

## Grounding

- **The totals ground well.** Every asset and liability line on page 2 reads `ok`.
- **Two boxes sit slightly low.** The boxes for total liabilities and net worth clip the
  top of their glyphs, but the value is still visibly inside each box.
- **The business-type box covers the whole checkbox row.** That is reasonable for a
  value picked from a group of options.
- **The signature tabs were misread on the first extraction.** The form's printed orange
  "SIGN" flag tabs parse as `[SIGN]`. On the first extraction, `certification.signed`
  came back `true` for an unsigned form. Saying in the field description that a sign-here
  tab is not a signature fixed it on a re-extract.
- **Blank cells come back as zeros.** The blank Section 4 cells for market value and
  mortgage balance return `0` instead of null, with no grounding (`OFF`).

## Cost

**20.80 credits** at standard tier:

- 14.70 for the parse and the first extraction
- 6.10 for one re-extraction (`--extract-only`) after the `signed` description was fixed

## Regenerating

```bash
# Redaction, from the original download (form-field values, then metadata and verification).
# widgets.py and rules.json are kept outside the repo.
python widgets.py <original>.pdf stage1.pdf rules.json
.venv/bin/python document-types/scripts/redact.py stage1.pdf \
    document-types/collection/sba-form-413/source/sba-form-413.pdf --rules rules.json

.venv/bin/python document-types/scripts/run_ade.py sba-form-413
.venv/bin/python document-types/scripts/build_images.py sba-form-413
.venv/bin/python document-types/scripts/inspect_fields.py sba-form-413 --page 2
```
