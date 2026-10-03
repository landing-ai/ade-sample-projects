# Schedule K-1

Source assets for `landing.ai/document-type/schedule-k-1`.

## Sample document

`source/schedule-k-1-2025-irs-ats-1065-scenario-1.pdf`: the 2025 IRS Schedule K-1
(Form 1065), Partner's Share of Income, Deductions, Credits, etc., filled with IRS test
data. **1 page, portrait.**

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [ty25-f1065-ats-scenario01.pdf](https://www.irs.gov/pub/irs-wi/ty25-f1065-ats-scenario01.pdf), linked from the IRS Tax Year 2025 Form 1065 MeF ATS information page |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Scenario 1 for
tax year 2025 Form 1065, which software vendors use to test their e-file output. The
original PDF is 28 pages: the full partnership return with its schedules (B, K, L, M-1,
M-2, M-3), Forms 4562, 4797, 8825 and 8882, and the partners' K-1s. This folder keeps
**page 12 only**, the first Schedule K-1, split out with PyMuPDF.

Every value is IRS test data: a fictitious partnership, SAM STARLING LLP of Reno NV,
with an EIN in the `00-` test range, and a foreign individual partner whose TIN has the
`000-00-` form the IRS uses in ATS scenarios. Nothing needed redacting. The PDF metadata
was reset to the IRS as author and a title naming the scenario, and the XMP packet was
removed.

## Why this document

The K-1 is what every partner in a partnership receives, and what lenders, preparers and
fund administrators have to read in bulk. It is denser than the Form 1065 sample in this
collection, which is page 1 of the partnership return itself. This page has:

- **Three parts in two columns.** Parts I and II, the partnership and the partner, run
  down the left. Part III, the partner's share of each line, runs down the right.
- **Checkboxes**: final or amended K-1, PTP, general or limited partner, domestic or
  foreign, retirement plan, K-3 attached, item M.
- **A code-letter grid.** Boxes 11 and 13 to 21 pair a box number, a code letter and
  an amount, and several boxes can hold more than one row. Reading a code against the
  wrong amount is the classic K-1 extraction error.
- **A beginning/ending matrix** for profit, loss and capital share (item J) and for
  liabilities (item K1), and a capital-account roll-forward (item L).

`schema.json` covers the tax period, Parts I and II, the J, K1 and L matrices, every
Part III box, and the coded boxes as arrays of `{code, amount}`. **70 leaf fields**
(counted from the schema). On this K-1, 64 leaf values come back, since three of the
eight coded boxes are empty and the other five hold one row each.

## Featured fields: the capital account roll-forward

All on page 1.

| Field | Value |
|---|---|
| Ordinary business income (box 1) | 8,068,141 |
| Beginning capital account (item L) | 4,488,892 |
| Other increase (item L) | 12,143,540 |
| Withdrawals and distributions (item L) | 7,514,031 |
| Ending capital account (item L) | 9,118,401 |

Item L reconciles: 4,488,892 + 12,143,540 − 7,514,031 = 9,118,401. Each line grounds to
its own amount cell. The withdrawal is the same 7,514,031 reported in box 19 code A, so
the distribution still appears on the page. Box 1 is the headline number of any K-1.

The request suggested five fields as suggestions only: box 1, box 19A distributions,
the ending capital account, the item J ending profit share and the item K1 ending
nonrecourse liabilities. Box 1 and the ending capital account shipped. The other three
grounded correctly (`ok`) but their crops would not read cleanly:

- **Box 19A.** The parse merged boxes 18, 19 and 20 into one table cell, with their
  code letters in another, so 7,514,031 can only be boxed together with 77,513 and
  9,265.
- **Item J profit ending.** The Profit row was merged into the I1/I2/J cell, so the box
  covers the entity type line, the retirement plan checkbox and both 10% values.
- **Item K1 nonrecourse ending.** The range covers both the empty beginning column and
  the ending column.

## Grounding and extraction notes

- **The code-letter grid paired correctly.** Even though the parse merged boxes 18–20
  into one cell and their code letters into another, extraction read every pair right:
  15 P 3,560, 17 A 19,946, 18 C 77,513, 19 A 7,514,031, 20 A 9,265. The pairing risk
  in the request did not happen in the values. It shows up in grounding instead: values
  are right, but boxes for these fields cover the merged cell.
- **Every checkbox read correctly**: limited partner, foreign partner, item M No, and
  the empty Final K-1, Amended K-1, PTP, K-3, retirement plan and boxes 22/23.
- **Item J's six percentages are all correct (10%).** Loss and capital ground to their
  own cells; profit grounds to the merged I1/I2/J cell.
- **Blank amount lines extract as 0, not null**, with ranges pointing at the label or an
  empty `$` cell. This matches the Form 1040 sample in this collection. The schema asks
  for null on a blank line. A consumer who needs to tell blank from zero cannot rely on
  this.
- **Addresses** extract in full; `partnership.address` grounds as two ranges, one per
  printed line, so it reads `OFF` in `inspect_fields.py` although both lines are right.

## Cost

**5.40 credits** at standard tier: one parse and one extraction of a single page.

## Regenerating

```bash
# Page 12 of the IRS PDF, split out with PyMuPDF:
#   doc.insert_pdf(src, from_page=11, to_page=11)
.venv/bin/python document-types/scripts/run_ade.py schedule-k-1
.venv/bin/python document-types/scripts/build_images.py schedule-k-1
.venv/bin/python document-types/scripts/inspect_fields.py schedule-k-1 --page 1
```
