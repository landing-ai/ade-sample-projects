# Motor Vehicle Report

**On the website:** [landing.ai/document-type/motor-vehicle-report](https://landing.ai/document-type/motor-vehicle-report)

The New York State DMV's sample Standard Abstract of a driving record, published as
form DS-242.1 to show drivers what an abstract contains. Each page repeats the
motorist's identification header, then shows one part of the record: license status
and credentials, credential history, suspensions, convictions, crashes and mailing
address history. The motorist is a specimen, and every page carries a SAMPLE watermark.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 41 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:37 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 18,556 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 16.4 s |
| Per page | 2.7 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 7.7 credits |
| Per page | 1.28 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:38 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 41 |
| Non-null fields returned | 41 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 179.8 s |
| Per schema field (41) | 4.39 s |
| Per value returned | 2.22 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 6.3 credits |
| Per schema field (41) | 0.154 credits |
| Per value returned | 0.078 credits |

## Origin

`source/ds2421.pdf` is the sample *Standard Abstract* of a driving record from the New
York State Department of Motor Vehicles. The DMV publishes it as form DS-242.1 (2/26),
*Description of Standard Abstract of Driving Record*, to show drivers what an abstract
contains. Every page carries a diagonal "SAMPLE - TEST LETTER" watermark, and the
motorist is a specimen. It is **6 pages, portrait, raster**. The DMV's PDF has 13 pages.
Only pages 1 to 6, the six-page sample abstract, are kept. Pages 7 to 13 are reference
tables of license classes and codes, and were dropped.

Each page of the abstract repeats the same identification header, then shows one part of
the record:

| Page | Content |
|---|---|
| 1 | Status, mailing address, active credential, endorsements, restrictions |
| 2 | Credential history, compliance, crash prevention course |
| 3 | Merges, impaired driving program, non-scofflaw suspensions |
| 4 | Scofflaw suspensions |
| 5 | Convictions / bail forfeitures, vessel convictions |
| 6 | Snowmobile convictions, crashes, mailing address history |

| | |
|---|---|
| Publisher | New York State Department of Motor Vehicles |
| Source | [dmv.ny.gov/forms/ds2421.pdf](https://dmv.ny.gov/forms/ds2421.pdf) |
| Retrieved | 2026-10-13. The operator downloaded it by hand, because the host blocks scripted downloads. |
| Clearance | **Redacted**, see below |

The motorist is a DMV specimen, but the sample uses a realistic full name, and four
mailing addresses on real streets in Troy and Manhattan with real ZIP+4 codes. A
realistic name can belong to a real person, and the addresses belong to real buildings,
so these were replaced before anything was parsed:

| What | Replaced with | Count |
|---|---|---|
| First, middle and last name in the identification header on every page and in the page 1 Active Credentials row | `JANE`, `Q`, `SAMPLE`, one per cell | 21 |
| Full name in the page 3 Merges table | `JANE Q SAMPLE` | 1 |
| Four mailing addresses (page 1 current address, page 6 address history) | `100 MAIN ST`, `200 OAK ST`, `300 ELM ST` and `400 ASH ST`, each `ANYTOWN NY 00000-0000`. The county and country cells were kept. | 5 |

The originals are not recorded anywhere in this folder. All other values were left as
published: the dates, the ticket, order, case and letter numbers, the specimen client ID
numbers and the birth date.

The abstract pages are images, with a text layer that held only the footer, so the
replacements were made in the pixels. Each kept page was rebuilt from a 300 dpi render
of the edited image, so the original rasters are not carried into the output. The output
was verified by OCR, by a second OCR sweep for every token of every original, by eye on
150 to 300 dpi renders, and by a sweep of every file in this folder. The PDF's metadata
is empty. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A motor vehicle report is the state's record of a person's license, violations,
suspensions and crashes. Real ones are never published, so this is the issuing agency's
own specimen with the real layout.

- **Auto insurance underwriting:** insurers order MVRs to rate new policies and review
  drivers at renewal.
- **Employment screening:** employers check MVRs for anyone who will drive on the job.
- **Commercial fleets and trucking:** carriers review drivers' records each year, as
  federal rules require for commercial drivers.
- **Rideshare and delivery platforms:** they screen drivers before onboarding and
  monitor them afterward.
- **Traffic and criminal defense attorneys:** they review a client's record before a
  hearing or plea.

### What it contains

- **Repeated record blocks:** convictions, suspensions and credential history are
  stacked label/value grids, one per event, rather than tables with a header row.
- **The same identification header on every page.**
- **Records of the same shape under different headings,** such as vessel and snowmobile
  convictions, and suspensions labelled "Violation" or "Reason".
- **A diagonal watermark** that crosses several values on every page.
- **Raster pages with no usable text layer,** so every value has to be read from the
  page image.
