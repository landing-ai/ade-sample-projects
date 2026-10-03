# Form 6251 - AMT

Source assets for `landing.ai/document-type/form-6251-amt`.

## Sample document

`source/form-6251-2025-irs-ats-scenario-13.pdf`: IRS Form 6251 (2025), Alternative
Minimum Tax—Individuals, completed for an IRS e-file test scenario. **2 pages, portrait.**
It has a text layer.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [1040-mef-ats-scenario-13.pdf](https://www.irs.gov/pub/irs-efile/1040-mef-ats-scenario-13.pdf), listed on the [TY2025 Form 1040 series MeF ATS information page](https://www.irs.gov/e-file-providers/tax-year-2025-form-1040-series-and-extensions-modernized-e-file-mef-assurance-testing-system-ats-information) |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** |

The IRS publishes these Assurance Testing System (ATS) scenarios so that e-file software
developers can test their returns against known answers. As a US government work, it is
in the public domain.

The source is a 9-page packet for Test Scenario 13. Pages 5–6, the completed Form 6251,
were split out unchanged with PyMuPDF. The same packet supplies the `form-1040` folder
(pages 2–3).

Every value is IRS test data for a fictitious taxpayer. The SSN is in the
400-00-13xx range that the ATS keeps for test scenarios. The PDF metadata names only
the IRS, Acrobat and Distiller. Nothing needed redacting.

The IRS replaces these undated files in place from time to time, so the committed copy
is the record.

## Why this document

It is the collection's first IRS schedule that computes something, rather than one
that reports amounts. Form 6251 works out whether the alternative minimum tax applies:
income is adjusted to AMTI, the exemption is subtracted, and the tentative minimum tax
is compared with the regular tax. A consumer needs the answer and the figures that
produced it.

It tests two things about layout:
- **Line 1a's value sits in an inner column**, to the left of the main amount column.
- **Line 5's exemption appears twice**: once in the threshold table beside the line
  and once as the line's own entry.

Both resolve correctly: line 1a grounds to its own inner box, and line 5 grounds to the
amount column rather than to the table.

The form is sparse. Only about eight lines are filled, and the AMT result is zero.
Page 2 (Part III, capital gains rates) is blank but is kept so the folder holds the
whole form.

`schema.json` has **21 leaf fields** (counted from the schema). Every line on page 1
with a value extracts correctly. The `other_adjustments` array for lines 2b–2t comes
back empty, which is correct.

## Featured fields: the AMT computation in order, on page 1

| Field | Value |
|---|---|
| Tax year | 2025 |
| Alternative minimum taxable income (line 4) | 31620 |
| Exemption (line 5) | 137000 |
| Regular tax (line 10) | 162 |
| AMT (line 11) | 0 |

These are the fields the request suggested, and all five shipped. Read top to bottom,
they tell the story: AMTI of 31,620 is below the 137,000 exemption for a married couple
filing jointly, so no AMT is owed against regular tax of 162. No person is featured.

## Grounding and extraction notes

- **Every filled amount grounds to the box holding its own value.** All 12 page-1
  fields with a printed value read `ok`.
- **The parse is right about blank lines, but extraction is not.** Lines 3 and 8, and
  Part III lines 12 and 40, are empty on the form, and the parse shows those cells as
  empty. Extraction still returns `0` for them, even after the schema descriptions were
  changed to ask for null. Arithmetically 0 is the same, but a consumer cannot tell
  "blank" from "0 entered". These lines read `OFF` in `inspect_fields.py`, because there
  is no text to box, and none of them is featured.
- `part_iii_capital_gains.completed` is a derived boolean (false). It has no single
  span to point at, so it is not illustrable.

## Cost

**10.70 credits** at standard tier:
- 7.50 for the first run, a 2-page parse plus extraction
- 3.20 for one re-extraction after the blank-line descriptions were changed

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py form-6251-amt
.venv/bin/python document-types/scripts/build_images.py form-6251-amt
.venv/bin/python document-types/scripts/inspect_fields.py form-6251-amt --page 1
```

To rebuild the source from the IRS packet:

```python
import fitz
src = fitz.open("1040-mef-ats-scenario-13.pdf")
out = fitz.open(); out.insert_pdf(src, from_page=4, to_page=5)
out.save("form-6251-2025-irs-ats-scenario-13.pdf")
```
