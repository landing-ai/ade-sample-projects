# Compliance inspection report

Source assets for `landing.ai/document-type/compliance-inspection-report`.

## Sample document

`source/ecology-construction-stormwater-inspection-war313805.pdf` — a Washington State
Department of Ecology Construction Stormwater General Permit inspection report for the
Good Neighbor Village construction project, permit WAR313805, inspected December 4,
2024. **7 pages, mixed orientation**: three portrait pages (general data and background,
a violations table, and the enforcement notice with the inspector's sign-off) and four
landscape photo pages with GPS-stamped captions.

| | |
|---|---|
| Publisher | Washington State Department of Ecology |
| Source | [apps.ecology.wa.gov/paris/DownloadDocument.aspx?id=521477](https://apps.ecology.wa.gov/paris/DownloadDocument.aspx?id=521477) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

A public record from Ecology's PARIS facility and permit database, downloaded directly.
The only person named is the Ecology inspector, acting in an official capacity; no
on-site representative was present. The photos show the site entrance, the public road
and machinery, with no people and no legible plates. No redaction was needed.

**How it was chosen.** The request was for a report verifying that construction or
renovation work meets required regulatory standards. Web research found the closest
building-standards form, HUD's Form HUD-92051 "Compliance Inspection Report" for FHA
construction, published only blank, and California's DSA inspection-card samples are
blank forms stamped "SAMPLE – DO NOT USE". This report checks construction against
environmental permit conditions (erosion and sediment control) rather than building
code, but it is a completed, published compliance inspection with citations, findings
and deadlines.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **regulatory inspection report**:

- **Findings tied to citations.** Each violation cites a permit condition (S9.D.2,
  S9.D.11), describes what the inspector saw, states the required action and a deadline,
  and links guidance.
- **Free text inside a form.** A ruled general-data grid, then narrative background and
  long table cells mixing bold, red and plain text.
- **Photos as evidence.** Four landscape pages of site photos, each with a caption and a
  date, time, latitude, longitude and bearing stamp.
- **Mixed orientation** in one PDF.

## Featured fields: the inspection record

All on page 1. The request named no page or fields, so these were chosen:

| Field | Value |
|---|---|
| Permit number | WAR313805 |
| Inspection date | 2024-12-04 |
| Inspection type | Unannounced |
| Receiving waters | Groundwater |
| Weather at inspection | 39 degrees Fahrenheit, mostly cloudy with a WSW wind at 1 mph. |

Which permit, when, what kind of inspection, where the site drains, and the weather,
which matters for a stormwater inspection. The inspector is named on the same page but
not featured; the date carries the same point without a person.

**The inspection date is flagged, and correct.** It is extracted as the ISO date
2024-12-04 and boxed on the cell "Inspection Date and Entry/Exit Time: December 4, 2024,
11:28/11:47", which contains it, so `build_images.py` warns that the value is not in the
boxed text. The crop was checked by eye.

## What it surfaced

**The violations extract well but are hard to illustrate.** Both violations come back
with the right condition, requirement, finding, action, guidance and the 12/20/2024
deadline. But each value grounds to a whole table cell, including its empty space, and a
violation's condition, requirement and finding all share the first cell. Featuring them
highlighted most of page 2, so page 1 is featured instead.

**The schema had to match the table, not the idea of it.** The first schema split each
violation into a finding, an action and a due date. The table has three columns
(violation and action, complete or submit date, guidance), and for the first violation
the date column holds an instruction rather than a date, so its due date came back null
with a `nonconformant_output` warning. The revised schema follows the table's columns.

**"null" as a string.** Where a nullable field has nothing to report, extraction returns
the text "null" rather than a JSON null: for the absent on-site representative, and for
the first violation's due date.

**The photo captions are read precisely.** All four photos come back with their
descriptions and full-precision latitude and longitude. The inspector's signature on
page 3 is transcribed as text.

## Extraction

**26 leaf fields**: agency, title, permit, project, date, entry and exit times, type,
inspector, on-site representative, receiving waters, weather, precipitation and UIC
flags, the violations, the signed date and the photos.

## Cost

**10.80 credits** at standard tier for 7 pages: 5.80 to parse, 5.00 to extract. The
first extraction, before the schema revision, cost a further 5.00, for 15.80 in all.

## Regenerating

```bash
curl -sSL -o document-types/collection/compliance-inspection-report/source/ecology-construction-stormwater-inspection-war313805.pdf \
  "https://apps.ecology.wa.gov/paris/DownloadDocument.aspx?id=521477"
.venv/bin/python document-types/scripts/run_ade.py compliance-inspection-report                # 10.80 credits
.venv/bin/python document-types/scripts/run_ade.py compliance-inspection-report --extract-only # 5.00, schema iteration
.venv/bin/python document-types/scripts/build_images.py compliance-inspection-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py compliance-inspection-report --page 1
```
