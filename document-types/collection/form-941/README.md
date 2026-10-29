# Form 941

Source assets for `landing.ai/document-type/form-941`.

## Sample document

`source/form-941-2023-ocrolus-sample.pdf`: IRS Form 941 for 2023, Employer's Quarterly
Federal Tax Return (Rev. March 2023), filled with specimen data for the first quarter.
**3 pages, portrait.**

| | |
|---|---|
| Publisher | Ocrolus (document-AI vendor sample) |
| Source | [drive.google.com/file/d/1gD_JCWFhLjuJKIoE_EDzTqv4IbcGZ1_M](https://drive.google.com/file/d/1gD_JCWFhLjuJKIoE_EDzTqv4IbcGZ1_M/view?usp=sharing) |
| Linked from | [docs.ocrolus.com: 941 Employer's Quarterly Federal Tax Return](https://docs.ocrolus.com/docs/941-employers-quarterly-federal-tax-return) |
| Retrieved | 2026-10-28 |
| Clearance | **Public**: vendor-published specimen |

Ocrolus publishes this sample in its public developer documentation for Form 941,
alongside its own extraction of it. Google Drive is only the host. The file was downloaded
by script from Drive's direct-download URL and checked to be a 3-page PDF, not Drive's
HTML viewer page.

Every value is specimen data: `SAMPLE NAME`, `SAMPLE TRADE LLC`, `123 ANY STREET`,
`FAKE CITY`, EIN `12-3456789`, designee `JOHN SAMPLE`, preparer `SAMPLE SMITH` of
`SAMPLE FIRM LLC`, placeholder phone numbers and PTIN, and script-font "Sample Name" and
"Sample Smith" signatures. No real person or business appears, so nothing was redacted.
The PDF metadata was reset to a title naming the sample and Ocrolus as author, and the XMP
packet was removed.

## Why this document

The collection's first payroll tax return. Form 941 is the quarterly filing lenders and
underwriters ask for to verify payroll, and it has a layout the other IRS forms here do
not: boxed single-digit EIN entry, a quarter checkbox panel, and the two-column
wage-times-rate computation on lines 5a to 5d. The PDF is also hard to read
mechanically. The text layer on pages 1 and 2 uses a garbled font encoding, and page 3
is mostly vector art and images, so ADE has to read it from the page image.

`schema.json` covers the header, all of Part 1 (lines 1 to 15, including each column of
lines 5a to 5d), the Part 2 deposit schedule, Part 3, the third-party designee, the
signature block and the paid preparer: **69 leaf fields**. All ten top-level groups
populate.

## Featured fields: page 1

| Field | Value |
|---|---|
| Employer identification number | 12-3456789 |
| Quarter | 1 (January, February, March) |
| Wages, tips and other compensation (line 2) | 10,000.00 |
| Total taxes after adjustments (line 10) | 10,840.00 |

Together they read as the core of the return: who is filing, for which quarter, what they
paid in wages, and the payroll tax owed.

The request suggested a fifth, line 5e (total social security and Medicare taxes), which
did not survive. See below.

## Grounding on this document: mostly poor in Part 1

This is a contrast with Form 1120, where every page-1 amount boxed its own cell.

**Lines 1 to 11c parse as a single text block**, and the line-level boxes inside it fall
out of step with their text from line 3 down. The text and the extracted values are
right. The boxes are not:

- Line 5e's amount (`410 . 00`) boxes the sidebar footnote beside lines 5a to 5c.
- Line 6's amount boxes the line 5e label row.
- The amounts for lines 1, 3, 5a to 5d column 2, 8, 9 and 11a box a neighbouring row or
  the label column.
- Lines 2, 10 and 11b box their own rows. The two featured amounts were checked by eye:
  each crop shows its line with the amount in it.

The EIN grounds well despite being nine separate digit boxes, and the quarter grounds to
the checked box and its label. `build_images.py` warns that OCR cannot read the EIN in
its crop. That is the boxed digit layout; the crop is correct.

The parse also **renumbers the two-column lines** in its markdown: 5a(i) reads as 5b,
5a(ii) as 5c, 5b as 5d, 5c as 5e and 5d as 5f. This is the layout risk the request
anticipated. Every value still lands in the right row and column, and extraction maps
all twelve column values correctly.

Each amount field's occurrence 0 grounds to its line label, and occurrence 1 to the
amount, so the manifest pins occurrence 1. The EIN's occurrence 0 is the page 3 header.

One extraction fault is left visible: `employer.zip_code` comes back null, although the
parse reads `ZIP code: 12345`.

## Cost

**8.30 credits** at standard tier: 3 pages, parse and extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py form-941
.venv/bin/python document-types/scripts/build_images.py form-941
.venv/bin/python document-types/scripts/inspect_fields.py form-941 --page 1
```
