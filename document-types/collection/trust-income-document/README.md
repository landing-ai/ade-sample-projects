# Trust Income Document

Source assets for `landing.ai/document-type/trust-income-document`.

## Sample document

`source/trust-income-k1-2025-irs-ats-1041-scenario-3.pdf`: the 2025 IRS Schedule K-1
(Form 1041), Beneficiary's Share of Income, Deductions, Credits, etc., filled with IRS
test data. This is the statement a trust or estate issues to each beneficiary to report
the income passed through to them. **1 page, portrait.**

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [form-1041-ty2025-ats-scenario-3.pdf](https://www.irs.gov/pub/irs-efile/form-1041-ty2025-ats-scenario-3.pdf), linked from the IRS Tax Year 2025 Form 1041 MeF ATS page |
| Retrieved | 2026-10-03, by script |
| Clearance | **Redacted** (US government work, public domain; one identifier replaced as a precaution) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Scenario 3 for
tax year 2025 Form 1041, which software vendors use to test their e-file output. The
original PDF is 19 pages: the full trust return with Schedules D and I, Forms 3800,
4797, 8864 and 8960, and the beneficiaries' K-1s. This folder keeps **page 10 only**,
the first beneficiary's Schedule K-1, split out with PyMuPDF.

Every value is IRS test data: a fictitious trust, Cyan Magenta Trust of Lanham MD, with
an EIN in the `00-` test range, and a test beneficiary. The beneficiary's identifying
number (item F) is an ATS test value, but it falls outside the standard specimen SSN
ranges, so as a precaution it was replaced with **987-65-4322**, from the reserved
987-65-4320 to 4329 range, using `document-types/scripts/redact.py`. That removes the
underlying text rather than covering it. The original number is not recorded anywhere
in this folder. The document metadata was cleared. Verified: the original is not
extractable from the committed PDF, in hyphenated or digits-only form, and the folder
sweep finds it nowhere.

## Why this document

Trust income is what lenders and preparers need to verify when a borrower or client
lives partly on distributions from a trust, and the K-1 (Form 1041) is the document that
proves it. It sits beside the partnership K-1 (Form 1065) in this collection but is a
different form: a two-column layout with the trust and beneficiary down the left
(Parts I and II) and the beneficiary's share of each income line down the right
(Part III), plus code-letter boxes 11 to 14 that pair a code with an amount. This
sample is sparse in a realistic way: two income lines, one credit and one item of
other information, with most boxes blank. Telling blank from zero is part of the test.

`schema.json` covers the tax period, the K-1 checkboxes, Parts I and II, every Part III
amount box, and boxes 11 to 14 as arrays of `{code, amount}`. **38 leaf fields**
(counted from the schema). On this K-1, 34 leaf values come back, since boxes 11 and
12 are empty and boxes 13 and 14 hold one row each.

## Featured fields: which trust paid what

All on page 1.

| Field | Value |
|---|---|
| Trust name (item B) | Cyan Magenta Trust |
| Trust EIN (item A) | 00-4012343 |
| Interest income (box 1) | 8,500 |
| Ordinary dividends (box 2a) | 189,300 |

Together they read as one statement: this trust passed this much interest and dividend
income through to the beneficiary. No person is featured; the beneficiary's name and
identifying number are on the page but not highlighted.

The request suggested five fields as suggestions only: these four plus the Final K-1
checkbox. The checkbox was dropped because a boolean cannot ground as a literal. Its
range covers the checked box and its label, which `inspect_fields.py` reports as `OFF`,
and the crop would show a check mark beside the value `True`.

## Grounding and extraction notes

- **Ruled cells ground cleanly.** Each of the four featured values grounds to its own
  form cell. The box covers the whole cell, label included, so the trust-name box takes
  in the trust's address lines too, since item B is a single block.
- **Box 13 code misread.** Box 13 prints code **O** with 125. The parse read the letter
  as a circle glyph and merged the box 13 and 14 amount cells, and the extraction then
  returned box 13 as code **A**, borrowing the letter from box 14. The amount is right.
  Left visible as a finding.
- **Blank boxes extract as 0, not null**, despite the schema allowing null. Their ranges
  point at the box labels. The same pattern appears on the Form 1065 K-1.
- The parse reads the box 4c label as "Uncaptured section 1250 gain".
- Item C (fiduciary), item D's date and the tax-period dates are blank on the form and
  come back null or empty.

## Credits

3.00 credits at the standard tier (one page parsed with DPT-3 Pro, plus extraction).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py trust-income-document
.venv/bin/python document-types/scripts/inspect_fields.py trust-income-document
.venv/bin/python document-types/scripts/build_images.py trust-income-document
```
