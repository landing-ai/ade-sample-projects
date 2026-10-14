# Land Appraisal

Source assets for `landing.ai/document-type/land-appraisal`.

## Sample document

`source/land-appraisal-uaar-warren-land-redacted.pdf`: five pages of a real
**Uniform Agricultural Appraisal Report (UAAR)**, the AgWare form used for farm and
ranch lending, valuing a 10,777.89-acre grazing ranch in Powder River County, Montana
for estate planning, effective January 22, 2015. **5 pages, portrait, US letter**, cut
from a 74-page report.

| | |
|---|---|
| Publisher | Warren Land & Livestock, Inc., an agricultural appraisal firm in Billings, Montana |
| Source | [Redacted-Appraisal-Report.pdf](https://warrenlandinc.com/wp-content/uploads/2018/12/Redacted-Appraisal-Report.pdf), linked as "Redacted Appraisal Report" from the firm's [Samples page](https://warrenlandinc.com/samples/) |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted** (by the publisher, before release) |

### Pages kept

The full report is 74 pages and costly to parse, so this folder keeps the five pages
that carry the valuation, split out with PyMuPDF:

| Here | Source page | Report page | Content |
|---|---|---|---|
| 1 | 6 | 2 of 70 | Property identification and summary of facts and conclusions |
| 2 | 40 | 36 of 70 | Sales Comparison Approach grid, sales 1-5 |
| 3 | 41 | 37 of 70 | Sales Comparison Approach grid, sales 6-10 |
| 4 | 43 | 39 of 70 | Income Approach |
| 5 | 44 | 40 of 70 | Reconciliation and opinion of value |

Everything else was left out: the cover and transmittal letter, table of contents,
signed certification, limiting conditions, area narrative, photographs, maps, the cost
approach worksheets, the per-sale land adjustment pages, deeds and the appraisers'
resumes.

### Clearance

The firm publishes this report as a work sample, and had already replaced the personal
data with a visible `***REDACTED***` placeholder: the owner, client, ranch name,
property address and location, legal description (section, township and range, shown as
`***`), the file number in every page header, and the grantor and grantee of every
comparable sale. The placeholder is real replacement text, not a box drawn over the
original; the original strings are not in the file. Those placeholders stay visible on
the pages here.

This build checked the five kept pages for anything the publisher missed and found
nothing: no name, signature, phone number, email or account number; no hidden or
off-page text (the only white text is the section headings on the blue bars); no
annotations, form fields, links or embedded files. The appraisers' names appear only on
dropped pages, in a professional capacity. **So no text was replaced, no page content
was changed, and the build did not pause for review.**

Two things that do not render were removed while splitting out the pages:

- **The PDF metadata**, which named one of the appraisers as author, and the bookmarks.
- **The original's shared image resources.** Every page of the original references the
  same twelve images (the photographs, maps and resume scans drawn on other pages), so a
  plain page split would have carried them along unseen. None is drawn on the kept
  pages, so they were removed from the resource dictionary.

Verified: the five pages render pixel-identical to the source pages and their text is
unchanged; the file has no metadata and no image objects; neither appraiser's name is
extractable from the PDF or present anywhere in this folder.

## Why this document

The collection's other appraisal, `appraisal-report`, is a residential URAR specimen
with three comparables and invented data. This is a real agricultural appraisal, on a
different form, with:

- **ten comparable sales** over two grid pages, each column a chain of per-acre
  arithmetic (CEV price, land and improvement adjustments, time adjustment, net
  adjustment, adjusted price);
- **all three approaches to value** (cost, income, sales comparison) reconciled into
  one opinion, with the same dollar figures repeated across the summary and
  reconciliation pages;
- dense small-type form fields, dotted leaders, and a publisher's own redaction
  placeholders sitting in the grid.

`schema.json` covers the subject property, the dates, the three value indications, the
opinion of value and marketing time, the allocation, the income summary, every
comparable sale, and the sales comparison summary box. **43 leaf fields** (counted from
the schema).

## Featured fields: one comparable's column

All on page 2 (source page 40, report page 36 of 70): comparable Sale #1 (D155).

| Field | Value |
|---|---|
| Sale #1 date | 10/14 |
| Sale #1 acres | 9781 |
| Sale #1 price | 4050000 |
| Net adjustment per acre | 58 |
| Adjusted price per acre | 472 |

Top to bottom they are one comparable's story: when it sold, how big it was, what it sold
for, and how far the appraiser adjusted its per-acre price to make it comparable to the
subject. Every box lands on the Sale #1 column, not its neighbours on the same row. No
person is featured.

### What the request suggested, and why it is not featured

The request named no feature page or fields; its notes suggested the reconciliation
(source page 44) or the sales grid (40-41), and suggested the three approach values,
the opinion of value and marketing time, total deeded acres and overall value per acre.
All of those extract **correctly**, but:

- **The reconciliation page received no groundings at all.** Every value printed there
  also appears on the summary page, and the extraction grounded to the summary instead.
- On the summary page, Cost Approach ($5,152,000), Sales Comparison Approach
  ($5,227,000), Opinion of Value ($5,200,000) and Total Deeded Acres (10,777.89) ground
  correctly, but **Income Approach ($5,132,000) grounds off**, to a dash, and
  **marketing time (12 months) and overall value per acre ($482) are synthesized**, with
  no ranges.

That left four headline values on the summary page against five fully grounded cells in
one grid column, so the grid won.

## Grounding and extraction notes

- **Both sales grids extract and ground perfectly.** All ten comparables, nine fields
  each, are right, and every one grounds to its own column on page 2 or 3: 90 cells
  across ten narrow columns with the redaction placeholders in between.
- **Labelled form fields ground well** on the summary page: county, ZIP, acres, land
  type, commodity, rights appraised and the approach values all point at their own line.
- **Values with dotted leaders or split layouts are synthesized.** The whole allocation
  block (land value, per-acre, percent; improvement contribution), the marketing time,
  and the Sales Comparison Approach summary box come back right but with no ranges.
  Those layouts scatter one value's pieces (`$`, amount, `/`, `Acre`, `%`) across
  separate text runs.
- **Reformatted dates read `OFF`.** Inspection and effective dates extract as
  2015-01-22 from `01/22/15` because the schema asked for YYYY-MM-DD; the ranges are
  right, but the boxed text does not literally contain the value.
- `build_images.py` warned that OCR could not read 58 and 472 inside their boxes. Both
  crops were opened: the boxes sit exactly on the Net Adjustments and Adjusted Price
  cells.
- The Sales Comparison summary's printed value range is $304 to $448 per acre, below the
  $485 concluded rate. That is what the report prints, and the extraction reports it
  faithfully.

## Credits

17.30 credits at the standard tier (5-page parse plus extraction), via the jobs API.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py land-appraisal        # spends credits
.venv/bin/python document-types/scripts/build_images.py land-appraisal   # free
.venv/bin/python document-types/scripts/inspect_fields.py land-appraisal --page 2
```

The source PDF was cut from the original with PyMuPDF: `select()` source pages 6, 40,
41, 43 and 44 (1-indexed), clear the bookmarks, clear the metadata with
`document-types/scripts/pdfmeta.py`, empty the shared `/XObject` resource dictionary
(no image is drawn on these pages), and save with `garbage=4`.
