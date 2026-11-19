# Compliance inspection report

**On the website:** [landing.ai/document-type/compliance-inspection-report](https://landing.ai/document-type/compliance-inspection-report)

A Washington State Department of Ecology inspection report for a construction site
covered by the Construction Stormwater General Permit, from an unannounced inspection on
December 4, 2024. It records the permit and site data and the weather, a table of
violations with the required action and deadline for each, the inspector's sign-off, and
four pages of GPS-stamped site photos.

| | |
|---|---|
| Pages | 7 |
| Fields in the extraction schema | 26 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:43 | 2026-11-19 02:46 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 8,675 | 9,287 |
| Words under 0.95 confidence | 18 | n/a |
| Words under 0.80 confidence | 3 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.9 s | 19.4 s |
| Per page | 1.0 s | 2.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.0 credits | 5.9 credits |
| Per page | 0.29 credits | 0.84 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:43 | 2026-11-19 02:47 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 26 | 26 |
| Non-null fields returned | 25 | 25 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 233.9 s | 198.1 s |
| Per schema field (26) | 9.00 s | 7.62 s |
| Per value returned | 5.57 s | 4.72 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.0 credits | 5.1 credits |
| Per schema field (26) | 0.192 credits | 0.196 credits |
| Per value returned | 0.119 credits | 0.121 credits |

## Origin

`source/ecology-construction-stormwater-inspection-war313805.pdf` is a Washington State
Department of Ecology Construction Stormwater General Permit inspection report for the
Good Neighbor Village construction project, permit WAR313805, inspected December 4,
2024. It is **7 pages, mixed orientation**: three portrait pages (general data and
background, a violations table, and the enforcement notice with the inspector's
sign-off) and four landscape photo pages with GPS-stamped captions.

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

The request was for a report verifying that construction or renovation work meets
required regulatory standards. Web research found the closest building-standards form,
HUD's Form HUD-92051 "Compliance Inspection Report" for FHA construction, published only
blank, and California's DSA inspection-card samples are blank forms stamped "SAMPLE – DO
NOT USE". This report checks construction against environmental permit conditions
(erosion and sediment control) rather than building code, but it is a completed,
published compliance inspection with citations, findings and deadlines. Full provenance
is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Compliance inspections record whether a site or facility meets the conditions of its
permit, and the findings drive deadlines, penalties and follow-up visits.

- **Construction contractors and developers:** site teams track each cited violation and
  its deadline until the corrective action is done.
- **Environmental regulators:** agencies log inspection findings against permits and
  follow up on open violations.
- **Environmental and engineering consultants:** they review inspection history for
  permit renewals and due diligence on a site.
- **Construction lenders and insurers:** they check open violations that could delay a
  project or lead to fines.
- **Legal and compliance teams:** they assemble inspection records when a violation
  turns into an enforcement action.

### What it contains

- **A ruled general-data grid** with permit, site, inspection and weather fields.
- **Findings tied to citations.** Each violation cites a permit condition, describes
  what the inspector saw, states the required action and a deadline, and links guidance.
- **Long table cells** that mix bold, red and plain text, with one date column holding
  an instruction in place of a date.
- **Narrative background** in free text.
- **Photos as evidence,** each with a caption and a date, time, latitude, longitude and
  bearing stamp.
- **A signature** in the inspector's sign-off.
- **Mixed orientation,** with portrait text pages and landscape photo pages in one PDF.
