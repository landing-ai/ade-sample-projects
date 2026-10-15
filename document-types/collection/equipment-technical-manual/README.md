# Equipment Technical Manual

Source assets for `landing.ai/document-type/equipment-technical-manual`.

## Sample document

`source/john-deere-tm1360-torque-and-fuel.pdf` is five pages from **Deere & Company's
Technical Manual TM1360** (John Deere Lawn & Grounds Care Division, June 1996), the
repair manual for the 655, 755, 855, 955, 756 and 856 Compact Utility Tractors. They are
the service-reference pages a technician looks things up on:

- Page 1 (printed 10-15-1): **Metric fastener torque values**. Property-class head and
  nut markings drawn as vector diagrams, then a 14-row table, M6 to M36, with two header
  tiers above the size rows: property class (4.8, 8.8 or 9.8, 10.9, 12.9), then
  lubricated or dry, then N·m and lb-ft. Footnote markers sit on the header cells.
- Page 2 (printed 10-15-2): **Inch fastener torque values**, the same layout for SAE
  grades 1, 2, 5 and 8, sizes 1/4 to 1-1/2.
- Page 3 (printed 10-15-3): **O-ring face seal fittings**: a fitting drawing, six service
  steps, and a torque chart by tube O.D., dash size and thread (swivel nut and bulkhead
  nut torque).
- Page 4 (printed 10-15-4): **O-ring boss fittings**: numbered steps interleaved with
  drawings beside a straight-fitting torque table that gives N·m, lb-ft and a number of
  flats to turn when a torque wrench cannot be used.
- Page 5 (printed 10-20-1): **Diesel fuel** specifications for North America: ASTM D975
  grades, cetane, cold filter plugging point, sulfur, lubricity (BOCLE) and storage.

5 pages, portrait, born-digital text layer throughout (producer VERSACOMP/MASTER), with
the fastener markings and fitting drawings as vector paths.

| | |
|---|---|
| Publisher | Deere & Company (John Deere Lawn & Grounds Care Division) |
| Source | [golftechs.us/Manuals/JDtractors.pdf](http://www.golftechs.us/Manuals/JDtractors.pdf) |
| Retrieved | 2026-10-14, by script |
| Clearance | **Public**, by the operator's decision (see below) |

### Provenance

The manual is marked COPYRIGHT 1996 Deere & Company, and Deere still sells it (for
example through deeremanuals.com as TM1360). The copy used here is hosted on
golftechs.us, a site unrelated to Deere whose home page is a placeholder and whose
Manuals folder is not browsable; nothing found links to the file. It is a mirror, not a
publisher distribution. That doubt was put to the operator, who chose to use the
document with clearance `public` on 2026-10-14.

The original is 570 pages. This sample keeps original pages 21-25 only, in order, and
the PDF metadata was cleared. The pages carry no personal data, so nothing was redacted.

## Why this document

It is a reference manual rather than a form or a statement: dense numeric lookup tables
whose meaning depends on multi-tier column headers, with diagrams, numbered procedures
and footnotes around them. The question it tests is whether every number lands under
the right size, class, condition and unit, which is exactly how a technician reads it.
Nothing else in the collection has a two-tier header grid of this size (16 value columns
per row).

## Schema

`schema.json` has 66 leaf fields: the group headings; both fastener torque tables as
arrays of rows, each row an object per class or grade with lubricated and dry torque in
N·m and lb-ft; the two O-ring fitting charts with their service steps and tolerances;
and the diesel fuel specifications. Across all four tables the extraction returns 624
values.

## Featured fields

Page 2, one complete lookup: the 1/2-inch row and its four SAE grade 5 torque values.

| Field | Value |
|---|---|
| Bolt size (in) | 1/2 |
| SAE grade 5 lubricated torque (N·m) | 85 |
| SAE grade 5 lubricated torque (lb-ft) | 63 |
| SAE grade 5 dry torque (N·m) | 110 |
| SAE grade 5 dry torque (lb-ft) | 80 |

The overlay shows the point of the document type: a value is only correct if it is
paired with its row and with all three header tiers above it.

The request suggested the metric table on page 1 (M12 class 10.9 lubricated torque, M20
class 8.8 dry torque, the JDS-G200 reference) or the O-ring boss page. Those are not
featured because of the grounding instability described next.

## Grounding

Every value extracted correctly in every run, including all 624 table cells. The ranges
did not.

- **The first extraction grounded every table cell on all five pages**, each to its own
  cell. After a one-line fix to a schema description, five further runs (four
  extraction-only, one full parse and extract) each returned one or more whole table
  sections with correct values but **no ranges at all**: the metric table and the O-ring
  boss table in all five, the O-ring face seal table and the inch table in four each.
  No warning or schema violation was reported. The committed output is the full run, in
  which the inch table grounds cell for cell and the other three tables do not. That is
  why page 2 is featured rather than page 1.
- **Where the tables ground, they ground exactly**: the featured crops sit on the right
  cell of a 17-column grid with no drift. The OCR check flags all five crops only
  because they are small single-number cells; each was opened and is correct.
- **The numbered service steps ground OFF** on pages 3 and 4: each step wraps across
  several printed lines and is matched line by line, so no single line contains the
  whole value. The text extracted is right.
- **A printed error passes straight through.** The metric table prints M14 class 12.9
  dry as 260 N·m and 109 lb-ft; 260 N·m is about 192 lb-ft, so the 109 looks like a
  transposition in the source. Extraction reports what is printed, which is correct
  behaviour, and does not flag it.
- Page 2's running header reads "Metric Cap Screw Torque Values" above the inch table, as
  printed.

## Credits

The committed output (one parse of 5 pages and one extraction, DPT-3 Pro, standard tier)
cost **26.70 credits**. Building it cost 130.20 in all: two full runs at 26.70 and four
extraction-only runs at 19.20, spent chasing the grounding instability above.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py equipment-technical-manual
.venv/bin/python document-types/scripts/build_images.py equipment-technical-manual
.venv/bin/python document-types/scripts/inspect_fields.py equipment-technical-manual --page 2
```

A re-run may ground different tables from the committed one; check with
`inspect_fields.py` before featuring anything.
