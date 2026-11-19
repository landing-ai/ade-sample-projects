# FDA Flowcharts

**On the website:** [landing.ai/document-type/fda-flowchart](https://landing.ai/document-type/fda-flowchart)

Five pages from the FDA guidance on deciding when to submit a 510(k) for a change to an
existing medical device: the cover and the four decision flowcharts a manufacturer
follows. Each chart is a set of numbered yes-or-no questions joined by arrows that lead
to further questions or to an outcome, such as a new 510(k) or documenting the change.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 10 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:56 | 2026-11-19 03:02 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 9,767 | 9,662 |
| Words under 0.95 confidence | 3 | n/a |
| Words under 0.80 confidence | 2 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.0 s | 15.1 s |
| Per page | 1.2 s | 3.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.8 credits | 5.0 credits |
| Per page | 0.36 credits | 1.00 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:56 | 2026-11-19 03:02 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 10 | 10 |
| Non-null fields returned | 10 | 10 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 221.4 s | 400.6 s |
| Per schema field (10) | 22.14 s | 40.06 s |
| Per value returned | 1.66 s | 3.01 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 7.3 credits | 7.1 credits |
| Per schema field (10) | 0.730 credits | 0.710 credits |
| Per value returned | 0.055 credits | 0.053 credits |

## Origin

`source/fda-510k-change-flowcharts.pdf` holds five pages from the U.S. Food and Drug
Administration's guidance *Deciding When to Submit a 510(k) for a Change to an Existing
Device* (October 25, 2017). The pages are the cover and the four decision flowcharts a
manufacturer follows to decide whether a device change needs a new 510(k) premarket
notification:

- the main chart
- Chart A, labeling changes
- Chart B, technology, engineering and performance changes
- Chart C, materials changes

It is **5 pages, portrait**, with a text layer.

| | |
|---|---|
| Publisher | U.S. Food and Drug Administration (CDRH and CBER) |
| Source | https://www.fda.gov/media/99812/download |
| Retrieved | 2026-11-15 |
| Clearance | Public |

This is a US federal government work, published on fda.gov for general use. The
original runs to 78 pages. The operator extracted pages 2, 13, 17, 25 and 34 into a
local file, and that file is the source here. Each page's text was checked against the
same page of a fresh download from the URL above, and all five match. The PDF metadata
was cleared.

There is no personal data in it. The only contact details are FDA office phone lines.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Decision flowcharts turn a regulation or policy into a sequence of yes-or-no questions.
The logic lives in the arrows, so the chart has to be read as a graph.

- **Medical device regulatory affairs:** manufacturers document their path through
  these charts each time they change a marketed device.
- **Quality and compliance:** quality teams tie change-control records to the chart
  decisions that justified filing or not filing.
- **Regulatory consultants and law firms:** advisors use the charts to support and
  defend a client's filing decision.
- **Regulatory intelligence:** teams turn agency guidance into rules and checklists for
  internal tools.

### What it contains

- **Flowcharts whose data is the structure:** which question leads to which, and on
  which answer.
- **Decision diamonds with printed IDs** (A1, B3.1, C4.1 and so on), except on the main
  chart, whose diamonds carry no IDs.
- **Yes and No arrows** that branch and rejoin between questions and outcome boxes,
  so the answer that leads to each step has to be read from the drawing.
- **Long question text** wrapped inside diamonds and boxes.
- **Figure captions** such as "Figure 4 - Flowchart C: Materials Changes", plus the
  cover page of the guidance.
