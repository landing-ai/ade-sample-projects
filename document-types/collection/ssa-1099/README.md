# SSA-1099

Source assets for `landing.ai/document-type/ssa-1099`.

## Sample document

`source/ssa-1099-irs-form-6744-specimen.pdf`: a Form SSA-1099, Social Security Benefit
Statement, for benefit year 2026, filled with IRS test data. **1 page, landscape**
(612 x 470 pt, the top of a letter page).

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [f6744.pdf](https://www.irs.gov/pub/irs-pdf/f6744.pdf), Form 6744 (Rev. 10-2026), *VITA/TCE Volunteer Assistor's Test/Retest* |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

Form 6744 is the IRS's certification test booklet for Volunteer Income Tax Assistance
and Tax Counseling for the Elderly volunteers. It is served as `application/pdf` from
the IRS's own forms path. Its scenarios print filled specimen tax documents for
fictitious taxpayers, and this SSA-1099 is one of them.

Every value is IRS test data: a fictitious beneficiary at 1234 Charity Avenue, Your
City, Your State, with the Social Security number already masked to `417-00-XXXX` in
the source. Nothing needed redacting. The PDF metadata was reset to the IRS as author
and a title naming the source page.

### How the page was cut out

The source is 210 pages. The SSA-1099 is the top half of PDF page 93 (printed page 88);
the bottom half of that page is an unrelated Form 1099-C for a different fictitious
taxpayer. The crop was done with PyMuPDF:

1. `insert_pdf` copied page 93 alone into a new document.
2. A redaction annotation over everything below y = 470 pt, applied with
   `apply_redactions(images=PDF_REDACT_IMAGE_NONE)`, removed the 1099-C's text and
   vector art. Without this the 1099-C's text would still be in the file, outside the
   visible area, and extractable.
3. The page's **MediaBox and CropBox were both set to `[0 322 612 792]`**, the top
   470 pt of the 612 x 792 page in PDF coordinates (origin bottom-left). The SSA-1099
   ends at about 440 pt from the top and the 1099-C started at about 505 pt, so the cut
   falls in the white space between them.

```python
import fitz
src = fitz.open("f6744.pdf")
doc = fitz.open()
doc.insert_pdf(src, from_page=92, to_page=92)
page = doc[0]
page.add_redact_annot(fitz.Rect(0, 470, 612, 792))
page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
page.set_mediabox(fitz.Rect(0, 322, 612, 792))          # PDF space
doc.xref_set_key(page.xref, "CropBox", "[0 322 612 792]")
```

The SSA-1099 itself is a raster image on the source page with a text layer drawn over
it, so the PDF has both an image and selectable text.

## Why this document

The SSA-1099 is the statement every Social Security recipient gets, and it feeds line
6a of Form 1040. It is small, but it is a different shape from the collection's other
tax forms: a government statement rather than an IRS information return, with the
year printed as a large standalone figure, a pair of boxes (3 and 5) that print the same
amount, and a free-form "Description of amount in Box 3" panel that breaks the
benefits into what was deposited and what was withheld for Medicare.

`schema.json` covers the beneficiary, every numbered box and the box 3 and box 4
description panels. **16 leaf fields** (counted from the schema).

## Featured fields: the boxes a preparer copies

All on page 1.

| Field | Value |
|---|---|
| Benefit year | 2026 |
| Benefits paid (box 3) | 25182 |
| Net benefits (box 5) | 25182 |
| Federal tax withheld (box 6) | 2518 |

Box 5 is what goes on the return and box 6 is the withholding credit; box 3 and box 5
print the same $25,182 and each grounds to its own ruled box. No person is featured.

The request suggested two more, the direct-deposit amount ($20,229) and the Medicare
Part B premium ($2,435). Both extract correctly and read `ok` in `inspect_fields.py`,
but see below: they ground to the whole description panel, so their crops would be two
identical full-panel boxes. The benefit year replaces them.

## Grounding and extraction notes

- **The ruled boxes ground exactly.** Box 3, box 5 and box 6 each ground to their own
  cell, and the large `2026` grounds to just the figure.
- **The description panel grounds coarsely.** The parse returns the "Description of
  amount in Box 3" panel as one tall table cell holding all four lines, and Extract
  gives every value in it (direct deposit, Part B premium, benefits for the year) the
  same range: the whole cell. The values are right; the highlight covers the panel
  rather than the line. Line-level `atomic_grounding` exists on this parse for text
  blocks, but not inside table cells.
- **Blank box 4 extracts as 0**, not null, although the schema description asks for
  null when the box is blank. Its range is the empty box 4 cell.
- **`form_variant` comes back `SSA-1099-SM`**, the form revision code printed in the
  footer, rather than the `SSA-1099` heading.
- Blank box 8, the empty box 4 panel, and the absent Part D and total-additions amounts
  are correctly null with no ranges.

## Cost

**1.60 credits** at standard tier, for one parse and one extraction.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py ssa-1099
.venv/bin/python document-types/scripts/build_images.py ssa-1099
.venv/bin/python document-types/scripts/inspect_fields.py ssa-1099 --page 1
```
