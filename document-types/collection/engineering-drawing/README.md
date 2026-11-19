# Engineering drawing

**On the website:** [landing.ai/document-type/engineering-drawing](https://landing.ai/document-type/engineering-drawing)

The City of Albany's standard construction details for streets and sidewalks, one detail
per sheet across eleven sheets, from C-1 to CW-1. Each sheet shows a curb, curb ramp,
driveway crossing, street restoration or crosswalk detail as a drawing with callouts and
dimensions, numbered notes, and the same title block.

| | |
|---|---|
| Pages | 11 |
| Fields in the extraction schema | 16 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:59 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 22,713 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 11.2 s |
| Per page | 1.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 11.2 credits |
| Per page | 1.02 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:00 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 16 |
| Non-null fields returned | 16 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 128.1 s |
| Per schema field (16) | 8.01 s |
| Per value returned | 2.21 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 6.7 credits |
| Per schema field (16) | 0.419 credits |
| Per value returned | 0.116 credits |

## Origin

`source/Standard-Construction-Street-Details.pdf` is the City of Albany's set of
standard construction details for streets and sidewalks. It is **11 pages, portrait
(612×792)**, with one standard detail per sheet, C-1 through CW-1: curbs, curb ramps, a
driveway crossing, street restoration and a crosswalk. Each sheet has a drawing,
callouts, numbered notes and the same title block. The PDF was plotted from AutoCAD LT
and has no text layer: every label is vector geometry.

| | |
|---|---|
| Publisher | City of Albany, NY, Department of Engineering |
| Source | [albanyny.gov/DocumentCenter/View/14719/…](https://www.albanyny.gov/DocumentCenter/View/14719/Standard-Construction-Street-Details) |
| Retrieved | 2026-09-25 |
| Clearance | Public |

The city publishes these municipal construction standards on its website for
contractors and the general public. The only people named are the Mayor and the City
Engineer, in their official capacity in the title block. Every sheet carries the City of
Albany logo.

Unlike US federal works, municipal documents are not automatically public domain, so
this is publicly distributed material rather than copyright-free material. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Standard details are the reference drawings that tell contractors exactly how a city
wants its curbs, ramps and sidewalks built. Drawing sets like this sit behind every
public works bid and permit.

- **Civil contractors and estimators:** they read the details to price and build curbs,
  ramps and driveways to the city's specification.
- **Municipal engineering and permitting:** inspectors and permit reviewers check work
  and plans against the standard details.
- **Civil engineering and design firms:** they cite the standard details in their own
  plan sets and specifications.
- **Accessibility compliance:** reviewers check curb ramp gradients and cross-slopes
  against ADA requirements.
- **Asset and document management:** cities and firms index large drawing sets by sheet
  number, title and revision date.

### What it contains

- **No text layer.** Every label is vector geometry, so every value has to be read off
  the drawing.
- **Callouts, not fields.** Values sit at the end of leader lines that point into
  isometric and section views.
- **Dimensions set along skewed axes,** such as an angled 6'-0" width.
- **A repeating title block** on all eleven sheets, with the detail number, name, file
  name, revision date, the city logo and the names of the Mayor and City Engineer.
- **Numbered notes** in a text column beside each drawing.
- **A tolerances table** drawn in the same CAD file, on page 10.
- **Two drawings on one sheet,** a plan and a section, on page 4.
