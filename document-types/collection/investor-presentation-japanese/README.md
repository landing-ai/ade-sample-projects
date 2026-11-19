# Investor Presentation (Japanese)

**On the website:** [landing.ai/document-type/investor-presentation-japanese](https://landing.ai/document-type/investor-presentation-japanese)

Nintendo's Japanese-language earnings presentation for the second quarter of the fiscal
year ending March 2027. Slides with presenter commentary cover consolidated results,
digital sales, hardware and software unit sales and the full-year forecast, followed by
reference tables of regional sales, quarterly figures, million-seller titles and the
release schedule.

| | |
|---|---|
| Pages | 18 |
| Fields in the extraction schema | 26 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:20 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 27,113 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 18.1 s |
| Per page | 1.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 15.8 credits |
| Per page | 0.88 credits |

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
| Fields requested | 26 |
| Non-null fields returned | 26 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 424.3 s |
| Per schema field (26) | 16.32 s |
| Per value returned | 7.58 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 7.1 credits |
| Per schema field (26) | 0.273 credits |
| Per value returned | 0.127 credits |

## Origin

`source/nintendo-fy27-q2-earnings-presentation.pdf` is Nintendo's 決算説明資料 (earnings
explanatory material) for the second quarter of the fiscal year ending March 2027. It is
**18 pages, portrait (A4)**.

| | |
|---|---|
| Publisher | Nintendo Co., Ltd. (任天堂株式会社, TSE: 7974) |
| Source | [nintendo.co.jp/ir/pdf/2026/261105_3.pdf](https://www.nintendo.co.jp/ir/pdf/2026/261105_3.pdf) |
| Retrieved | 2026-11-15 |
| Clearance | Public |

This is investor relations material that a listed company publishes on its own IR site
for general distribution. It was downloaded directly from the URL, not by hand. No
individual is named anywhere in the deck, so nothing was redacted. The file is
byte-for-byte the publisher's copy, including its owner-password permissions flag (there
is no open password). Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Listed companies publish an earnings presentation each quarter alongside their results.
This one is in Japanese, with financial units that do not map directly to English
ones.

- **Equity research:** sell-side and buy-side analysts pull results, forecasts and unit
  sales into their models each quarter.
- **Asset management and investing:** portfolio managers and foreign investors track
  Japanese holdings from the original Japanese materials.
- **Financial data providers:** vendors collect figures from IR decks to populate
  company fundamentals databases.
- **Corporate strategy and competitive intelligence:** competitors and partners follow
  platform and title performance.
- **Investor relations and translation:** IR teams and translators prepare English
  versions and summaries of the Japanese originals.

### What it contains

- **Japanese text throughout,** with financial units the reader has to interpret:
  amounts in 億円 (hundred millions of yen), 百万円 on the reference pages, and unit
  sales in 万台 and 万本 (tens of thousands).
- **A handout layout.** Pages 2 to 11 are A4 sheets with a slide in the top third and
  the presenter's commentary as prose underneath, so most headline figures are printed
  twice.
- **Ruled slide tables** of results and forecasts.
- **Slides that combine a results table with a chart.**
- **Dense reference tables** on pages 13 to 17: regional sales, quarterly KPIs, unit
  sales by region, million-seller titles and the release schedule.
- **Footnotes** that carry assumptions, such as the exchange rate behind the forecast.
