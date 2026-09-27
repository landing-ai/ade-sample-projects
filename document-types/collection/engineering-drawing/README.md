# Engineering drawing

Source assets for `landing.ai/document-type/engineering-drawing`.

## Sample document

`source/Standard-Construction-Street-Details.pdf` — the City of Albany's standard
construction details for streets and sidewalks. **11 pages, portrait (612×792).** One
standard detail per sheet, C-1 through CW-1: curbs, curb ramps, a driveway crossing,
street restoration and a crosswalk, each with a drawing, callouts, numbered notes and
the same title block.

| | |
|---|---|
| Publisher | City of Albany, NY — Department of Engineering |
| Source | [albanyny.gov/DocumentCenter/View/14719/…](https://www.albanyny.gov/DocumentCenter/View/14719/Standard-Construction-Street-Details) |
| Retrieved | 2026-09-25 |
| Clearance | Public |

Municipal construction standards published on the city's website for contractors and
the general public. The only people named are the Mayor and the City Engineer, in their
official capacity in the title block, the same basis on which the investor presentation
names executives. Every sheet carries the City of Albany logo.

Unlike US federal works, municipal documents are not automatically public domain, so
this is publicly distributed material rather than copyright-free material.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first document that is mostly drawing rather than text:

- **No text layer.** The PDF was plotted from AutoCAD LT and every label is vector
  geometry — PyMuPDF finds zero characters on every page. Nothing can be copied out of
  the file; every value has to be read off the drawing.
- **Callouts, not fields.** The values sit at the end of leader lines pointing into
  isometric and section views, with dimensions set along skewed axes.
- **A repeating title block.** Eleven sheets share one layout, so the schema can index
  the whole set, and a value like the City Engineer's name appears eleven times.

## What it surfaced

**The drawing is parsed as one figure.** DPT-3 returns every drawing as a
`<figure type="DIAGRAM">` — 12 across the 11 pages, since page 4 carries a plan and a
section. The callout labels do not come back as text blocks. They exist only inside the
figure's generated description, as a bulleted list:

```
- "MAX. GRADIENT 1:12 (AND 1:50 CROSS-SLOPE IF WITHIN WALKING PATH)" with a directional arrow ...
- "6'-0"" dimension labels indicating the width of the driveway ramp transition.
```

Extraction reads them correctly: every drawing field on page 5 is right, including the
angled 6'-0" dimension and the cross-reference to detail SW-1. But grounding can only
point at the figure block as a whole, so the gradient, the transition length and the
concrete thickness all boxed the **entire drawing** and rendered identical crops. This is
the same trap as the investor deck's pie chart, at a larger scale.

**Text outside the drawing grounds precisely.** The notes, the title block table and the
names beside the logo all resolve to the exact line or cell. Page 10's Design Element
Tolerances table, drawn in the same CAD file, came back as a proper HTML table with
every cell.

**The title block is not parsed the same way on every page.** On most sheets the logo
and the two names sit outside the table; on pages 6 and 10 they were folded into it. As
a result the eleven `city_engineer` ranges are not in page order: occurrence 0 lands on
page 6 and boxes the logo cell, and the page 5 occurrence is number 6. The manifest pins
it.

## Extraction

`schema.json` has three parts:

| Part | Fields | From |
|---|---|---|
| Top level | `issuing_department`, `city_engineer` | Title block, same on every sheet |
| `sheets[]` | `detail_number`, `detail_name`, `file_name`, `revision_date` | Title block, one entry per sheet |
| `drop_curb` | gradient, cross-slope, transition length, driveway width, concrete thickness and reference, curb material, finish, curb reveal, notes | Page 5, DW-1 |

Everything extracts correctly. All eleven sheets come back in page order with the right
detail number, name, file name and revision date, so `sheets[4]` is DW-1.

`revision_date` is normalized to `2024-03-08` as the schema asks, so it no longer matches
the printed `03/08/24` and the consistency check flags it. The value is right; it is not
featured because its crop would appear to disagree with it.

## Featured fields

All on **page 5, DW-1 Driveway/Sidewalk Drop Curb**, and all outside the drawing:

| Field | Value | Region |
|---|---|---|
| Detail name | DRIVEWAY/SIDEWALK DROP CURB | Title block table |
| Maximum curb reveal | 1/2" MAX | Note 1 |
| CAD file name | DW-1.DWG | Title block table |
| City Engineer | Howard M. Goebel P.E. | Beside the logo |

Together they say which standard this is, what it requires, which file it came from and
who is responsible for it.

The drawing's own values are not featured, for the reason above. To feature them, the
drawing would need to parse as text blocks rather than a figure; until then, a page
about reading engineering drawings has to say that the callouts are extracted but not
located. Page 10 is the alternative if a featured table matters more than a featured
drawing.

## Cost

**16.60 credits** at standard tier for 11 pages: 10.50 to parse, 6.10 to extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py engineering-drawing                # 16.60 credits
.venv/bin/python document-types/scripts/run_ade.py engineering-drawing --extract-only # 6.10, schema iteration
.venv/bin/python document-types/scripts/build_images.py engineering-drawing           # free
.venv/bin/python document-types/scripts/inspect_fields.py engineering-drawing --page 5 --good
```
