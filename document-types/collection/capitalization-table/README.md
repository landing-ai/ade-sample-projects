# Capitalization Table

Source assets for `landing.ai/document-type/capitalization-table`.

## Sample document

`source/cooley-sample-pro-forma-cap-table.pdf`: the pro forma capitalization table of a
fictional Acme, Inc., after a Series B financing, from Cooley LLP's startup resource site
Cooley GO. **1 page, landscape.** It shows Common Stock, Series A and Series B columns with
per-class and fully diluted percentages for five existing investors, a new investor, two
founders and three option pool rows, and a footnote on the preferred-to-common conversion
ratio.

| | |
|---|---|
| Publisher | Cooley LLP (Cooley GO) |
| Source | [Sample-Pre-and-Post-Cap-Table-w-Pricing-Worksheet.pdf](https://www.cooleygo.com/wp-content/uploads/2014/06/Sample-Pre-and-Post-Cap-Table-w-Pricing-Worksheet.pdf), linked from [Sample Cap Table (Pro Forma)](https://www.cooleygo.com/documents/sample-cap-table-pro-forma/) |
| Retrieved | 2026-10-28, by script |
| Clearance | **Public**: a sample a law firm publishes for general use |

Every holder is a placeholder (Investor #1–#5, Founder #1–#2, New Investor), so no content
was redacted. The PDF's metadata (the firm's name as author, Excel as creator, a creation
date) and its tagged-PDF structure tree were cleared. None of it was personal data.

**Why the PDF and not the spreadsheet.** Cooley also publishes the workbook this page was
printed from, as a legacy `.xls` with two more sheets: the pre-money cap table and an
up-round pricing model. ADE accepts no legacy `.xls` in either API generation. v2 takes
XLSX, but spreadsheet output is grounded by cell address with no page boxes, so the page
overlay and crops this collection is built on would not exist. The PDF is Cooley's own
print of the Post-$ Pro Forma sheet, and it needs no change to the shared tooling.

## Why this document

It is the collection's first cap table: a dense numeric grid, 11 columns wide. Share counts
and percentages alternate, headers wrap over two lines, and zero holdings print as dashes.
The test is whether extraction keeps each number in its share-class column across rows
that are mostly zeros.

`schema.json` covers the company, the table's basis (current or pro forma), the share
classes, one object per holder row (group, name, shares per class, total shares, total
percent), the totals row, the option pool increase, and the conversion footnote. **16 leaf
fields** (counted from the schema); all 7 top-level fields were populated.

## Featured fields: the Series B round

All on page 1.

| Field | Value |
|---|---|
| Company | Acme, Inc. |
| New investor Series B shares | 4,775,322 |
| Option pool increase | 4,252,854 |
| Total Series A shares | 36,500,000 |
| Fully diluted shares | 57,528,176 |

Together they describe the financing the table models: the new money's shares, the pool
top-up that comes with it, the preferred already outstanding, and the fully diluted count
after both. All five read ok in `inspect_fields.py`. The crops and the page overlay were
checked by eye. No person is featured.

## Grounding and extraction notes

- **Every value is right.** All 11 holder rows, every share count, every total percent and
  all four totals extract correctly. The Series A and B totals and the fully diluted total
  match the column sums.
- **The parse table is messier than the extraction.** The two-line header did not line up:
  "Common % w/o Pool" splits across both header rows and "Total %" lands in the wrong
  column. The "Common %" and "w/o Pool" cells of the option rows merge into one cell
  (`6.2% n/a`). Zero holdings come through three ways: as an em dash, as a hyphen, or as
  an empty cell. Extraction placed every value in the right column anyway.
- **Dashes cannot be featured.** The 22 zero holdings extract correctly as 0, but their
  ranges point at a dash or an empty cell, so `inspect_fields.py` reads them as off.
- **The option pool increase box is loose.** It covers the whole cell including blank
  space to its left, with the value in its upper right. The value is legible in the crop.
  The other four boxes fit their values tightly.

## Credits

4.50 credits at standard tier: 1.40 to parse, 3.10 to extract (1 page).

## Regenerate

```bash
# the PDF's metadata was cleared with document-types/scripts/pdfmeta.py (clear, then save)
.venv/bin/python document-types/scripts/run_ade.py capitalization-table
.venv/bin/python document-types/scripts/build_images.py capitalization-table
```
