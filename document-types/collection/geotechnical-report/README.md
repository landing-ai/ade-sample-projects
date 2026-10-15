# Geotechnical Report

A geotechnical engineering investigation by Moore Twining Associates, Inc. for the
Monterey Peninsula Regional Park District: **Proposed Classroom Project, Garland Ranch
Regional Park, 700 West Carmel Valley Road, Carmel Valley, California** (project
H07802.01, November 21, 2023). Two hollow-stem auger borings, B-1 and B-2, were drilled
on October 19, 2023 to about 33 feet, and the samples went to the lab for gradation,
density, shear, consolidation and corrosion tests.

This folder keeps **14 of the report's 61 pages**. All are portrait, US Letter.

| Page here | Source page | Content |
|---|---|---|
| 1 | 2 | Report cover |
| 2-4 | 34-36 | Appendix A: divider, site location map (USGS topo), test boring location plan (CAD) |
| 5 | 37 | Appendix B divider |
| 6-8 | 38-40 | Log of Test Boring B-1, three pages |
| 9-11 | 41-43 | Log of Test Boring B-2, three pages |
| 12 | 44 | Log notes, abbreviations and key to symbols |
| 13-14 | 54-55 | Consolidation test reports, two samples from B-1 |

Left out: the district's Exhibit D slip sheet (page 1), the transmittal letter (page 3),
the table of contents and the 27-page report body, the sieve analysis sheets, the direct
shear and other lab sheets, and the corrosion lab report. That keeps the parse cost
proportionate to the page this folder feeds, and the kept pages are the part of a
geotechnical report that pipelines actually mine: the logs and the lab tables.

## Provenance

| | |
|---|---|
| Publisher | Moore Twining Associates, Inc. (consultant); posted by the Monterey Peninsula Regional Park District |
| Source URL | https://www.mprpd.org/files/bee0b37d7/Item0724-6E_ApprvRFBOutdoorClassroom_Attach1.ExhibitD.GeotechRpt.pdf |
| Context | Exhibit D to the district's July 2024 board item 6E, approving the Request for Bids for the Garland Ranch Outdoor Classroom |
| Retrieved | 2026-10-14, downloaded by script |
| Clearance | `public` |

The file is on the district's own domain, published with its board packet and bid
documents for anyone bidding on the work. It was split out with PyMuPDF; nothing on the
kept pages was redacted.

**Personal data.** The transmittal letter carries the certified engineering geologist's
signature and licence seal and names a district staff member as addressee. That page was
not kept. The kept pages name only the two organizations, plus the driller's, logger's
and draftsman's initials, which are professional details in a public record. The PDF's
metadata named a district staff member as author and was cleared.

## Why this document

Boring logs are the hardest thing in the collection to read by layout alone. Each log
page is a narrow multi-column graphic: a depth and elevation scale, a soil symbol column
with sampler blow counts in 6-inch increments, the USCS class, a free-text description,
a Remarks column of stacked lab values, then N-values and moisture. Rows are positioned
by depth, not ruled, so pairing a moisture value with its N-value means reading vertical
position. A log also continues across pages, so one boring is three pages of the same
header. The folder adds a CAD site plan, a topo map, and consolidation reports with a
chart above a merged-header property table.

## Featured fields

All five are on **page 6**, the first page of the B-1 log (source page 38):

| Field | Label | Value |
|---|---|---|
| `borings[0].boring_id` | Boring | B-1 |
| `borings[0].surface_elevation_ft` | Surface elevation (ft AMSL) | 183 |
| `borings[0].groundwater_first_encountered_ft` | Groundwater first encountered (ft) | 18.2 |
| `borings[0].samples[0].uscs` | First sample USCS class | SM |
| `borings[0].samples[0].n_value_blows_per_ft` | First sample N-value (blows/ft) | 27 |

Read top to bottom, they follow one boring from its header to its first sample: which
hole, where the ground surface is, where water was hit, and what the first soil is and
how dense. The request suggested nine fields on this page. All nine ground correctly, but
a page carries at most five, so date drilled, first sample moisture, drill rig and hammer
type were left off the overlay. They are in `extract-pro.json`. No person is featured.

## Grounding notes

- **Log headers ground cleanly on the first page of each log.** Boring ID, date, rig,
  auger, hammer, elevation and groundwater depth each box their own label-and-value line.
  The header repeats on every log page; on B-2 it grounds line by line on all three
  pages, but on B-1 pages 2 and 3 the repeats box a whole header block instead.
- **Table cells box the whole depth band.** The USCS and N-value crops are tall boxes,
  because ADE reads the log body as a table whose rows are depth intervals. The value is
  at the top of the box. `build_images.py` warned that OCR could not read them inside the
  box; on inspection both crops contain their values.
- **Row pairing held on the featured page.** The request flagged the risk that the narrow
  columns would mis-pair values with N-value rows. On B-1 page 1 every N-value, moisture
  and Remarks entry landed on its own row, including the GP/SW-SM row at the foot of the
  page where two USCS classes share one cell.
- **It slipped once, on B-2 page 2 (page 10).** The page prints three moisture values
  against three N-values, but one moisture is a second reading on the 17.5-foot sample,
  not a row of its own. Extraction gave the 24-blow sample the second reading (15.1)
  instead of its own (19.9), and 19.9 was lost. This is the failure a reviewer should
  check for on logs.
- **Descriptions that cross a page break** come back merged or split (B-1 sample 6
  concatenates three strata), and ground OFF because of embedded line breaks.
- **USCS is printed once per stratum**, so samples deeper in a stratum come back with
  `uscs` null rather than inheriting the class. Correct to the page, not to the soil.
- **The consolidation tables extract almost exactly** under a two-row merged header
  ("Natural" over Sat. and Moist.): every printed value on both reports is right. One
  slip: the second report heads its last-but-one column "Swell %" rather than
  "Clpse. %" and leaves it blank, and extraction returned `collapse_pct` 0 for it
  instead of null.

The schema has **35 leaf fields**.

## Credits

Standard tier, jobs API, DPT-3 Pro: **24.50 credits** for one parse and one extract of
the 14 pages.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py geotechnical-report        # spends credits
.venv/bin/python document-types/scripts/build_images.py geotechnical-report   # free
.venv/bin/python document-types/scripts/inspect_fields.py geotechnical-report --page 6
```

The source PDF is source pages 2, 34-44, 54 and 55 of the URL above, extracted with
PyMuPDF and with its metadata cleared.
