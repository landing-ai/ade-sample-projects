# Stool test report

Source assets for `landing.ai/document-type/lab-report-stool`.

## Sample document

`source/mosaic-stool-chemistries-sample.pdf` — a **Stool Chemistries** report, Mosaic
Diagnostics' published sample of its stool chemistry panel. **3 pages, portrait**, a native
PDF with a text layer. Page 1 has a three-box header (order, patient, sample collection)
over one results table of 18 analytes in six sections: digestion and absorption,
inflammation, immunology, short-chain fatty acids, intestinal health markers and
macroscopic appearance. Each row has its result, unit and reference interval, plus a
coloured Low / Within / High range bar with a triangle marking the result. Page 2 explains
each analyte; page 3 is the lab's written commentary.

| | |
|---|---|
| Publisher | Mosaic Diagnostics (formerly Great Plains Laboratory); analyzed by Doctor's Data, Inc. |
| Source | [mosaicdx.com/…/MDX_Report_StoolChemistries_ENG.pdf](https://mosaicdx.com/wp-content/uploads/2026/07/MDX_Report_StoolChemistries_ENG.pdf) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

Mosaic links the PDF from its
[Sample Test Reports](https://mosaicdx.com/resource/stool-chemistry-test-sample-report/)
resource page, alongside Japanese, Portuguese and Spanish versions. It is specimen data
throughout: "Sample Patient", "Sample Doctor, MD", IDs of 999999 and "123 Main St." The
PDF carries no copyright or reuse notice, and Mosaic's site states no reuse restriction.
It is used unaltered.

**One caveat on terms, accepted by the operator.** The report is analyzed by Doctor's
Data, Inc., and its footer names that lab and its director. Doctor's Data's own website
terms restrict that site's content to non-commercial use. This copy is hosted and
published by Mosaic, not by Doctor's Data, and the operator accepted it on that basis.

**This replaces the request's original source.** The request first pointed at Nordic
Laboratories' GI-MAP sample report, whose footer limits reproduction to personal use and
prohibits commercial reproduction; the operator rejected it.

## Why this document

The collection's first **stool test report**, and its first lab report whose results
table is drawn with graphics between the columns:

- **A range-bar graphic in every row,** between the unit and the reference interval, with
  the result marked by a triangle whose colour carries the interpretation. No `L` or `H`
  letter is printed.
- **A results table repeated in six sections,** each with its own header row.
- **Comparators in results and intervals:** `>500`, `<10`, `> 200`, `≤ 500`.
- **Qualitative and quantitative results side by side:** "Negative", "None", "Brown",
  "Soft" next to numbers with units.

## Featured fields: the specimen's record

All on page 1. The request's notes suggested results-table fields; see below for why none
could be used.

| Field | Value |
|---|---|
| Report | Stool Chemistries |
| Order number | 999999-9999 |
| Collected | 06/28/2026 |
| Received | 07/01/2026 |
| Reported | 07/07/2026 |

Which test, which order, and the specimen's path through the lab: collected, received,
reported. The schema keeps dates as printed, so they ground cleanly, unlike the many
documents in this collection whose dates are normalised to ISO and read `OFF`.

## What it surfaced

**Every result grounds one cell off.** All 18 rows of the results table extract
correctly: analyte, result, unit and reference interval are all right. But every range
points one table cell after its value. The analyte grounds to its result cell, the result
to its unit cell, the unit to the empty graphic column, and the reference interval to the
next row's analyte. The parse is correct cell by cell, so the shift is in the
extraction's ranges. It affects only this table, which the parse wraps in a
`<figure type="CHART">` because of the range bars, while header fields above it ground
exactly. A second extract-only run reproduced the shift exactly. As a result, none of the
suggested fields (elastase, calprotectin, secretory IgA, occult blood, total SCFAs) could
be featured.

**The range-bar interpretation is mostly inferred correctly.** The schema asks whether
each result is outside its interval. Both genuinely out-of-range rows, % propionate (6.3
against 11–25) and β-glucuronidase (2240 against 2800–8000), are flagged. Elastase is also
flagged, which is wrong: `>500` meets `> 200`.

**Footnote markers are stripped.** Analytes print with `*`, `†` or `‡`; the extraction
drops them as the schema asks.

**The commentary topics are found:** "Short Chain Fatty Acids (SCFAs)" and
"β-glucuronidase", the two headings on page 3.

## Extraction

**23 leaf fields**: report title; the analyzing lab (name, address, director, CLIA ID);
the order (number, client, ordering provider); the patient (name, ID, age, date of birth,
sex); the specimen's collected, received and reported dates; each result row (section,
analyte, result, unit, reference interval, outside-reference flag); and the commentary
topics. All 7 top-level fields populate, with all 18 result rows.

## Cost

**16.70 credits** at standard tier for 3 pages: 4.90 to parse, 5.90 for the first
extraction, and 5.90 for a second extract-only run that confirmed the grounding shift.

## Regenerating

```bash
curl -sSL -o document-types/collection/lab-report-stool/source/mosaic-stool-chemistries-sample.pdf \
  "https://mosaicdx.com/wp-content/uploads/2026/07/MDX_Report_StoolChemistries_ENG.pdf"
.venv/bin/python document-types/scripts/run_ade.py lab-report-stool                # 10.80 credits
.venv/bin/python document-types/scripts/run_ade.py lab-report-stool --extract-only # 5.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py lab-report-stool           # free
.venv/bin/python document-types/scripts/inspect_fields.py lab-report-stool --page 1
```
