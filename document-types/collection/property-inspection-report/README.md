# Property Inspection Report

Source assets for `landing.ai/document-type/property-inspection-report`.

## Sample document

`source/VideoSampleReport1.pdf` — a residential home inspection report for a two-storey
single family house in Virginia Beach, written by Safe House Property Inspections LLC with
Home Inspector Pro's report software. **30 pages, portrait.** A cover page, site details,
then one section per system (roof and attic, exterior, interior, kitchen, HVAC, plumbing,
electrical, garage, crawlspace), each with numbered, colour-coded observations and
photographs, a conclusion, and a two-page Report Summary table of significant deficiencies.

| | |
|---|---|
| Publisher | Home Inspector Pro, Inc. (sample produced by Safe House Property Inspections LLC) |
| Source | [homeinspectorpro.com/…/VideoSampleReport1.pdf](https://homeinspectorpro.com/wp-content/uploads/2025/04/VideoSampleReport1.pdf), linked from the vendor's [Sample Reports](https://homeinspectorpro.com/inspection-sample-reports/) page |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | **Public** |

Home Inspector Pro sells inspection report software and publishes this report as a sample
of what it produces. The client and agent are specimen entries ("Mr. and Mrs. Sample",
"Top Agent - Virginia Beach Realty") and the address is the specimen "1234 Sample Report
Rd". The only real person named is the inspector, as the report's author and the
company's owner. There are no phone numbers, email addresses or licence numbers. The
photographs show a real house and its systems, with no people, no legible house number
and no plates. **No redaction was needed.** The file is committed unchanged: it carries an
owner password only (it opens without one) and video annotations on three pages, neither
of which affected parsing.

## Why this document

A long narrative report, rather than a form or a table: most of its content is numbered
findings in running prose, each prefixed with a category label (IMPROVE, MAINTENANCE,
SAFETY CONCERN, FYI) and often ending in a LOCATION. It tests whether extraction can pull
structured findings out of prose, and whether it can rebuild a summary table whose cells
each hold several findings. It is also photo-heavy, with the descriptive sentence for the
roof printed above the photographs it describes.

## Featured fields — page 4 (printed "Page 3 of 29", Roof and Attic)

| Field | Value |
|---|---|
| Roof covering material | fiberglass based asphalt shingles |
| Recommendation category (item 2.2) | IMPROVE |
| Recommendation category (item 2.3) | MAINTENANCE |
| Damaged shingles item | 2.4 |
| Damaged shingles location | front upper left side |

One page, one system: what the roof is, how the inspector classed two of its
recommendations (exposed nail heads to improve, moss to maintain), and the deficiency
that reached the Report Summary, with where on the roof it is.

The request suggested a system page or the summary table, with these fields and drainage
item 3.1 as suggestions. Item 3.1 is not featured: its text runs over three lines and
grounds as one range per line, so no single box contains the value. The summary table on
page 29 grounds correctly, but each value there is a whole multi-line cell, which crowds
the overlay, and deficiency 2.4 is shown on page 4 in context instead.

## What it surfaced

**Prose findings ground per line.** Single-line values (an item number, a category label,
a location) ground to exactly the right line. A whole observation spanning two to five
lines comes back with one range per line, so it is correct but cannot be shown as one
box. A finding's item number and its LOCATION ground to different lines of the same
item.

**A sentence became a figure caption.** "The roofing material was fiberglass based
asphalt shingles…" sits directly above three roof photographs, and the parse made it the
caption of a photograph figure. The roof covering material therefore grounds to the whole
figure, sentence and photos together. The value is in the box. The roof's life cycle stage
("second third of their life cycle") comes from the same sentence and drew the identical
box, so it was dropped from the featured fields.

**Scoping the findings array mattered.** Asking for every observation in the Roof and
Attic section returned the Report Summary's roof rows a second time, dropped item 5.1 and
lost the heading for items 9.1 and 9.2. Narrowing the array to roof coverings and drainage
(items 2.x and 3.x) made it clean.

**Summary cells hold several findings.** Asking for one summary entry per table row
returned 23 of the 29 numbered deficiencies, because cells such as Cooling System
Observations hold two (7.4 and 7.5) and Crawlspace Observations four. Asking for one entry
per deficiency number returned all 29, with the four SAFETY CONCERN items flagged.

**The duplicated text layer did not leak through.** The PDF's own text layer carries every
page header twice; the parse output has each once.

**Empty locations are inconsistent.** Where a summary item has no LOCATION, extraction
returns an empty string for some and null for others; in the roof findings it is null.

## Extraction

**36 leaf fields** in the schema: the inspection (company, inspector, address, client,
agent, date, start time, attendance, standards), the property and the day's weather, the
roof and attic (covering, life cycle, attic access, insulation, ventilation), the roof
coverings and drainage findings (item, heading, category, observation, location) and the
Report Summary deficiencies (system, report page, component, item, safety flag,
deficiency, location).

## Cost

**72.50 credits** at standard tier for 30 pages: 39.40 to parse, 33.10 to extract. The
three earlier extractions, before the schema revisions, cost a further 36.80, 36.40 and
32.80, for 178.50 in all.

## Regenerating

```bash
curl -sSL -A "Mozilla/5.0" -o document-types/collection/property-inspection-report/source/VideoSampleReport1.pdf \
  "https://homeinspectorpro.com/wp-content/uploads/2025/04/VideoSampleReport1.pdf"
.venv/bin/python document-types/scripts/run_ade.py property-inspection-report                # 72.50 credits
.venv/bin/python document-types/scripts/run_ade.py property-inspection-report --extract-only # 33.10, schema iteration
.venv/bin/python document-types/scripts/build_images.py property-inspection-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py property-inspection-report --page 4
```
