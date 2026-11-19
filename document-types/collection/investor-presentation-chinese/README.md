# Investor Presentation (Chinese)

**On the website:** [landing.ai/document-type/investor-presentation-chinese](https://landing.ai/document-type/investor-presentation-chinese)

Bank of China's 2026 interim results presentation, in Simplified Chinese, dated August
28, 2026. Its slides report the bank's operating results for the first half, total
assets and liabilities, asset quality and capital ratios, and the proposed interim
dividend, in charts, tables and headline figures.

| | |
|---|---|
| Pages | 21 |
| Fields in the extraction schema | 38 |

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
| Characters returned | 18,369 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 30.3 s |
| Per page | 1.4 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 15.1 credits |
| Per page | 0.72 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:20 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 38 |
| Non-null fields returned | 38 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 203.0 s |
| Per schema field (38) | 5.34 s |
| Per value returned | 5.34 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 5.1 credits |
| Per schema field (38) | 0.134 credits |
| Per value returned | 0.134 credits |

## Origin

`source/boc-2026-interim-results.pdf` is Bank of China's 2026 interim results
presentation (2026年中期业绩发布), dated 2026-08-28. It is **21 pages, landscape (16:9),
Simplified Chinese**. The PDF has no text layer: each page is one raster image produced
by Acrobat's image-conversion plug-in.

| | |
|---|---|
| Publisher | Bank of China Limited (SSE: 601988, HKEX: 3988) |
| Source | [pic.bankofchina.com/…/P020260828571239979382.pdf](https://pic.bankofchina.com/bocappd/report/202608/P020260828571239979382.pdf) |
| Retrieved | 2026-11-15, downloaded by script directly from the publisher |
| Clearance | Public |

This is investor relations material that a listed bank published on its own domain for
general distribution. It names no individuals, so nothing needed redacting. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Listed companies present their results to investors in slide decks, and Chinese issuers
publish them in Chinese first. Anyone covering these companies has to read the Chinese
original.

- **Equity research and asset management:** analysts covering Chinese banks pull
  earnings, asset quality and capital figures from each results deck.
- **Credit analysis and rating agencies:** they track non-performing loan ratios,
  provisioning coverage and capital adequacy.
- **Financial data providers:** they extract headline metrics from issuer presentations
  into databases.
- **Bank regulators and peer banks:** they benchmark capital and asset quality ratios
  across institutions.
- **Investor relations teams:** they compare their own disclosures with peers'.

### What it contains

- **Simplified Chinese throughout,** including labels, units (百万元人民币, 十亿元人民币)
  and change notation (个百分点, 个基点).
- **Image-only pages** with no text layer.
- **Very large pages,** each 5759 × 3240 pt, about eight times the size of a normal
  slide.
- **Charts whose values appear only as data labels,** including 3D bar charts.
- **Label-value pairs in text boxes** for ratios such as NPL and capital adequacy.
- **Branded design** with pink gradients and decorative arrows.
