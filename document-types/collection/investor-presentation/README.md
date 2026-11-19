# Investor presentation

**On the website:** [landing.ai/document-type/investor-presentation](https://landing.ai/document-type/investor-presentation)

Park National Corporation's investor slides for the fourth quarter of 2025, a bank
holding company's 43-slide deck. It covers the company's financial results and
business lines in bullet points, tables, bar and pie charts and footnotes, with an
appendix of supporting data.

| | |
|---|---|
| Pages | 43 |
| Fields in the extraction schema | 23 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:10 | 2026-11-19 03:17 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 94,561 | 96,043 |
| Words under 0.95 confidence | 88 | n/a |
| Words under 0.80 confidence | 22 | n/a |
| Words under 0.50 confidence | 7 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 21.4 s | 36.6 s |
| Per page | 0.5 s | 0.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 16.0 credits | 45.6 credits |
| Per page | 0.37 credits | 1.06 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:11 | 2026-11-19 03:18 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 86.3 s | 245.0 s |
| Per schema field (23) | 3.75 s | 10.65 s |
| Per value returned | 1.76 s | 5.00 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 20.8 credits | 21.2 credits |
| Per schema field (23) | 0.904 credits | 0.922 credits |
| Per value returned | 0.424 credits | 0.433 credits |

## Origin

`source/Q4-2025-Investor-Slides.pdf` is Park National Corporation's Q4 2025 investor
slides. It is **43 pages, landscape (720×540)**, with a text layer.

| | |
|---|---|
| Publisher | Park National Corporation (NYSE American: PRK) |
| Source | [s201.q4cdn.com/960710146/…/Q4-2025-Investor-Slides.pdf](https://s201.q4cdn.com/960710146/files/doc_presentations/2026/Feb/09/Q4-2025-Investor-Slides.pdf) |
| Retrieved | 2026-09-25 |
| Clearance | Public |

Investor relations material published by a listed company for general distribution, so
it is publishable without further clearance. It names executives, but only in their
professional capacity, which is the point of the document. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Public companies publish a deck like this each quarter alongside their earnings, and
the figures in it are read across the investment industry.

- **Equity research and investment banking:** analysts pull results and ratios from
  each quarter's deck into their models.
- **Asset managers and institutional investors:** portfolio teams compare peers on the
  same metrics quarter after quarter.
- **Bank and credit analysis:** analysts and rating agencies track asset quality,
  capital and income mix for lenders like this one.
- **Financial data providers:** they capture slide figures into datasets for their
  subscribers.
- **Corporate development and competitive intelligence:** teams follow competitors'
  stated strategy and results.

### What it contains

- **Landscape slides** in a 43-page deck.
- **Bar and pie charts** whose values appear only as chart labels.
- **Financial tables,** some in an appendix, with figures in millions.
- **Bullet points** that restate chart figures in prose.
- **Footnotes** with detail the charts and bullets leave out.
- **A dark cover slide** with light text.
- **The same company name and dates repeated** on nearly every slide.
