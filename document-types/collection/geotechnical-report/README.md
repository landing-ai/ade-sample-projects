# Geotechnical Report

**On the website:** [landing.ai/document-type/geotechnical-report](https://landing.ai/document-type/geotechnical-report)

Selected pages from a geotechnical engineering investigation by Moore Twining
Associates for a classroom project at Garland Ranch Regional Park in Carmel Valley,
California. It has the report cover, a site location map and boring location plan, the
logs of two test borings drilled to about 33 feet, a key to the log symbols, and two
consolidation test reports.

| | |
|---|---|
| Pages | 14 |
| Fields in the extraction schema | 35 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:06 | 2026-11-19 03:12 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 21,411 | 22,754 |
| Words under 0.95 confidence | 97 | n/a |
| Words under 0.80 confidence | 55 | n/a |
| Words under 0.50 confidence | 31 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.3 s | 567.4 s |
| Per page | 1.1 s | 40.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.3 credits | 12.2 credits |
| Per page | 0.31 credits | 0.87 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:07 | 2026-11-19 03:21 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 35 | 35 |
| Non-null fields returned | 35 | 35 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 537.3 s | 567.7 s |
| Per schema field (35) | 15.35 s | 16.22 s |
| Per value returned | 4.10 s | 4.14 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 10.9 credits | 11.2 credits |
| Per schema field (35) | 0.311 credits | 0.320 credits |
| Per value returned | 0.083 credits | 0.082 credits |

## Origin

`source/geotechnical-report-moore-twining-garland-ranch.pdf` is a **geotechnical
engineering investigation** by Moore Twining Associates, Inc. for the Monterey Peninsula
Regional Park District: Proposed Classroom Project, Garland Ranch Regional Park, 700 West
Carmel Valley Road, Carmel Valley, California (project H07802.01, November 21, 2023). Two
hollow-stem auger borings, B-1 and B-2, were drilled on October 19, 2023 to about 33
feet, and the samples went to the lab for gradation, density, shear, consolidation and
corrosion tests.

This folder keeps **14 of the report's 61 pages**. All are **portrait, US Letter**, with
a text layer.

| Page here | Source page | Content |
|---|---|---|
| 1 | 2 | Report cover |
| 2-4 | 34-36 | Appendix A: divider, site location map (USGS topo), test boring location plan (CAD) |
| 5 | 37 | Appendix B divider |
| 6-8 | 38-40 | Log of Test Boring B-1, three pages |
| 9-11 | 41-43 | Log of Test Boring B-2, three pages |
| 12 | 44 | Log notes, abbreviations and key to symbols |
| 13-14 | 54-55 | Consolidation test reports, two samples from B-1 |

| | |
|---|---|
| Publisher | Moore Twining Associates, Inc. (consultant); posted by the Monterey Peninsula Regional Park District |
| Source | [mprpd.org/files/bee0b37d7/…GeotechRpt.pdf](https://www.mprpd.org/files/bee0b37d7/Item0724-6E_ApprvRFBOutdoorClassroom_Attach1.ExhibitD.GeotechRpt.pdf) |
| Context | Exhibit D to the district's July 2024 board item 6E, approving the Request for Bids for the Garland Ranch Outdoor Classroom |
| Retrieved | 2026-10-14, downloaded by script |
| Clearance | Public |

The file is on the district's own domain, published with its board packet and bid
documents for anyone bidding on the work. The kept pages were split out of it, and
nothing on them was redacted.

Left out: the district's Exhibit D slip sheet (page 1), the transmittal letter (page 3),
the table of contents and the 27-page report body, the sieve analysis sheets, the direct
shear and other lab sheets, and the corrosion lab report. The kept pages are the logs
and lab tables, the part of a geotechnical report that is most often mined for data.

The transmittal letter carries the certified engineering geologist's signature and
license seal and names a district staff member as addressee. That page was not kept. The
kept pages name only the two organizations, plus the driller's, logger's and
draftsman's initials, which are professional details in a public record. The PDF's
metadata named a district staff member as author and was cleared. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A geotechnical report describes the soil and groundwater under a site, and engineers
design foundations from it.

- **Structural and civil engineering:** designers take bearing capacity, settlement and
  groundwater depth from the logs and lab results.
- **Construction and bidding:** contractors read the logs to price excavation,
  dewatering and foundation work, which is why this report was published with the bid
  documents.
- **Public agencies and owners:** districts and cities commission reports for their
  projects and keep them with the permit record.
- **Geotechnical firms:** consultants compile boring data from past reports into
  databases for nearby sites.
- **Insurance and risk:** underwriters and claims teams review soil conditions for
  settlement and subsidence risk.

### What it contains

- **Boring logs as narrow multi-column graphics:** a depth and elevation scale, a soil
  symbol column with blow counts, the USCS class, a free-text description, a Remarks
  column of stacked lab values, then N-values and moisture.
- **Rows positioned by depth, not ruled,** so values pair by vertical position.
- **Logs that continue across pages,** with the same header repeated on each page and
  descriptions that cross the page break.
- **A CAD site plan and a USGS topographic map.**
- **Consolidation reports** with a chart above a property table with a two-row merged
  header.
- **A key to symbols and abbreviations** that the logs depend on.
