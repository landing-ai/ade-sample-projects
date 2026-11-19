# Investor Presentation (Arabic)

**On the website:** [landing.ai/document-type/investor-presentation-arabic](https://landing.ai/document-type/investor-presentation-arabic)

Barwa Real Estate's Arabic-language investor presentation for the first quarter of
2026, dated April 2026. The deck covers the company's Q1 results, capital structure,
debt maturities and property portfolio, in KPI cards, tables, charts, a map and
photographs, with text that runs right to left.

| | |
|---|---|
| Pages | 34 |
| Fields in the extraction schema | 27 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:19 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 48,204 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 29.6 s |
| Per page | 0.9 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 29.1 credits |
| Per page | 0.86 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:19 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 27 |
| Non-null fields returned | 27 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 238.4 s |
| Per schema field (27) | 8.83 s |
| Per value returned | 6.81 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 10.7 credits |
| Per schema field (27) | 0.396 credits |
| Per value returned | 0.306 credits |

## Origin

`source/barwa-investor-presentation-q1-2026-ar.pdf` is Barwa Real Estate's
Arabic-language **investor presentation** for the first quarter of 2026, dated April
2026. It is **34 pages, landscape (792×612)**, exported from PowerPoint with a text
layer.

| | |
|---|---|
| Publisher | Barwa Real Estate Company Q.P.S.C. (Qatar Stock Exchange) |
| Source | [barwa.com.qa/documents/investor-presentations/2026/…الربع الاول2026.pdf](https://www.barwa.com.qa/documents/investor-presentations/2026/%D8%A7%D9%84%D8%B9%D8%B1%D8%B6%20%D8%A7%D9%84%D8%AA%D9%82%D8%AF%D9%8A%D9%85%D9%8A%20%D9%84%D9%84%D9%85%D8%B3%D8%AA%D8%AB%D9%85%D8%B1%D9%8A%D9%86-%D8%A7%D9%84%D8%B1%D8%A8%D8%B9%20%D8%A7%D9%84%D8%A7%D9%88%D9%842026.pdf) |
| Retrieved | 2026-11-15, downloaded by script |
| Clearance | Public |

This is investor relations material that a listed company publishes for general
distribution. The slides carry no personal data. The only contact details are the
investor relations team's corporate mailbox and switchboard number on the last slide.

The PDF's document metadata named the employee who exported the file, so all metadata
was cleared. No page content was changed. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Listed companies in the Gulf publish investor presentations in Arabic, often alongside
an English version, each quarter.

- **Equity research and asset management:** analysts covering GCC markets pull
  quarterly results, debt and dividend figures from the deck.
- **Credit analysis and banking:** lenders and rating teams track debt, maturities and
  leverage ratios.
- **Financial data providers:** vendors capture company figures from Arabic filings for
  their databases.
- **Investor relations and corporate finance:** teams compare their own disclosures
  with peers'.
- **Regulators and exchanges:** market supervisors review what listed companies
  disclose.

### What it contains

- **Arabic text that runs right to left.** Tables put the label column on the right and
  the value on the left.
- **Two digit systems in one deck.** Some slides print Western digits (`12,976`) and
  others Arabic-Indic digits (`٤٨٦`). The PDF's text layer stores Western digits even
  where the font draws Arabic-Indic ones.
- **An Arabic-Indic zero** drawn as a small raised dot, which looks like a decimal
  point.
- **KPI cards** with headline figures.
- **Ruled tables** of capital structure and leverage.
- **Bar and stacked charts,** including a debt maturity chart with value labels, plus a
  map and photographs.
