# Food sensitivity report

Source assets for `landing.ai/document-type/food-sensitivity-report`.

## Sample document

`source/1001-IgG-Food-Antibodies-Sample-Report.pdf` — Genova Diagnostics' sample IgG Food
Antibodies profile, a clinical lab report. **4 pages, portrait (612×792)**, with a full
text layer. Page 1 is a grid of 87 foods in seven categories, each with an IgG reactivity
code and a color-coded box, plus a Total IgE panel. Page 2 groups the foods by reactivity
level, and pages 3 and 4 are commentary on the elimination diet.

| | |
|---|---|
| Publisher | Genova Diagnostics |
| Source | [gdx.net/core/sample-reports/1001-IgG-Food-Antibodies-Sample-Report.pdf](https://www.gdx.net/core/sample-reports/1001-IgG-Food-Antibodies-Sample-Report.pdf) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

Genova publishes this among its sample reports for clinicians. The patient is "SAMPLE
PATIENT", with date of birth, sex, MRN and ID left blank. The only person named is the
laboratory director, in the page footer, in a professional capacity, and the CLIA and
Medicare license numbers are the laboratory's. No redaction was needed.

**Why "sensitivity", not "allergy".** The folder was first named `food-allergy-report`.
The report itself says IgG responses are "in a class distinct from Immunoglobulin E (IgE)
food allergy reactions", and that its elimination diet is "specific to food sensitivities
… not those defined as classic (IgE-mediated) food allergy reactions". The slug names
what the document is.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **clinical lab report**, and a layout that is hard on purpose:

- **A results grid, not a table.** 87 foods in four columns, grouped under category
  headings that break each column at different heights, with no ruling between cells.
- **Meaning carried by color.** Each result has a code (0, VL, 1+, 2+, 3+) and a colored
  box beside it, and the Total IgE result sits in an "Inside" or "Outside" box that says
  whether it is within range.
- **The same data twice.** Page 2 restates the grid as lists by reactivity level, so the
  extraction can be checked against the document itself.

## Featured fields: the hard page

All on **page 1**, featured by the document owner's decision to show the hard page
rather than the easy one:

| Field | Value |
|---|---|
| Test profile | 1001 IgG Food Antibodies Profile |
| Methodology | EIA and Chemiluminescent |
| Patient | SAMPLE PATIENT |
| Gluten result (from the results grid) | 3+ |

The three header fields box exactly their lines. **The Gluten result boxes the entire
results grid**, for the reason below: the value was extracted correctly from the hard
layout, but it cannot be located any more precisely than "somewhere in this grid". No
second grid value is featured, because it would render the identical crop.
`specimen_type` is not featured because it shares a line with the test profile.

The patient is the specimen "SAMPLE PATIENT", not a real person.

## What it surfaced

**The grid is parsed as a single figure.** DPT-3 returns the whole results grid as one
`<figure type="CHART">` and writes its own table into the figure's description, with
columns Category, Item, Result and Level. The Level column is invented: it names the box
colors ("Green", "White", "Red"), which are not printed as text anywhere. The legend bar
below the grid is a second chart figure. This is the engineering drawing's problem again,
on a document that is mostly text: once a region is a figure, nothing inside it can be
boxed on its own.

**Every grid value grounds to the whole grid, one cell adrift.** Inside the generated
table, each field's range lands on the next cell along: `category` on the food name,
`food` on the result code, and `result` on the color word. So `build_images.py` warns
that Gluten's "3+" is not in its boxed text, "Red". The box itself is the figure block,
the entire grid. The Total IgE value and reference range also ground to the figure.

**Two results are wrong, and the error is in the parse.** The generated table has Tomato
as 0 (printed VL) and Pear as VL (printed 0), and extraction copies both. Every other
result is right, so extraction is **85 of 87 correct**, with every food, category and
the Total IgE panel present. Page 2 has both foods in the right place, so checking the
grid against the summary would catch the errors.

**The summary page grounds precisely.** On page 2, Gluten, Sesame and Sunflower seed each
box their own name. Coffee and Wheat share a cell because they are printed one under the
other, so they share a box. This was the recommended feature page, but it was set aside
as the easy case.

## Extraction

`schema.json` was written for this report, with **13 leaf fields** in four groups:
`report` (laboratory, test, specimen, methodology, patient), `total_ige` (value, unit,
reference range, and whether it is within range), `food_results[]` (food, category and
result for each of the 87 foods) and `high_reactive_foods[]` (the page 2 High list).
Everything populates, with no warnings.

## Cost

**15.30 credits** at standard tier for 4 pages: 6.40 to parse, 8.90 to extract. The
extract share is high because it returns 87 grid rows.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py food-sensitivity-report                # 15.30 credits
.venv/bin/python document-types/scripts/run_ade.py food-sensitivity-report --extract-only # 8.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py food-sensitivity-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py food-sensitivity-report --page 1 --good
```
