# Investor Presentation (Korean)

**On the website:** [landing.ai/document-type/investor-presentation-korean](https://landing.ai/document-type/investor-presentation-korean)

NAVER's third-quarter 2026 earnings presentation (2026년도 3분기 실적발표), dated
2026-11-12, in Korean. It covers the quarter's results summary, revenue by segment,
costs and net income, with ruled tables comparing five quarters and stacked bar charts
of the trends.

| | |
|---|---|
| Pages | 10 |
| Fields in the extraction schema | 47 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 13,738 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 15.3 s |
| Per page | 1.5 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 8.5 credits |
| Per page | 0.85 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:23 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 47 |
| Non-null fields returned | 47 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 283.2 s |
| Per schema field (47) | 6.03 s |
| Per value returned | 4.16 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 4.6 credits |
| Per schema field (47) | 0.098 credits |
| Per value returned | 0.068 credits |

## Origin

`source/naver-3q26-earnings-kor.pdf` is NAVER's third-quarter 2026 earnings presentation
(2026년도 3분기 실적발표), dated 2026-11-12. It is **10 pages, landscape (4:3), Korean**,
exported from PowerPoint with a text layer.

| | |
|---|---|
| Publisher | NAVER Corporation (KRX: 035420) |
| Source | [navercorp.com/api/article/download/…](https://navercorp.com/api/article/download/5424bdee-8b0f-4f03-b38f-a308a9381eb9) |
| Retrieved | 2026-11-15, downloaded by script directly from the publisher |
| Clearance | Public |

This is investor relations material that a listed company published on its own domain
for general distribution. The source URL is a download endpoint rather than a file path.
It returned `application/pdf` with the filename `3Q26_Naver_Earnings_KOR_vF.pdf`, and the
file was checked to be a 10-page PDF, not an HTML or JSON response. It is stored here
under a descriptive name. The deck names no individuals, so nothing needed redacting.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Listed companies publish an earnings deck every quarter, and in Korea the primary
version is often in Korean only.

- **Equity research analysts:** they pull segment revenue, operating profit and margins
  into their models each quarter.
- **Institutional investors and asset managers:** they track results across the
  companies they hold or cover.
- **Financial data providers:** they extract figures from filings and decks to build
  standardized datasets.
- **Corporate strategy and competitive intelligence teams:** they follow peers' segment
  trends and costs.
- **Credit analysts and rating agencies:** they review earnings when assessing an
  issuer.

### What it contains

- **Korean text throughout,** including financial labels (매출액, 영업이익, 당기순이익),
  units (십억 원, 조 원) and percentage-point notation (`-5.2%p`).
- **Ruled financial tables on slides,** with five quarters plus Y/Y and Q/Q columns.
- **Indented sub-segment rows** under segment totals.
- **Stacked bar charts with value labels.**
- **A slide deck layout** exported from PowerPoint, with a text layer.
