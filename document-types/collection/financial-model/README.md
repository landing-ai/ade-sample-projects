# Financial Model

**On the website:** [landing.ai/document-type/financial-model](https://landing.ai/document-type/financial-model)

A real estate development pro forma, the Aloha Development Model by Jones Lang LaSalle,
printed as Exhibit C to a 2017 redevelopment report for the State of Hawaii. It values a
1.21 million square foot mixed-use district around a new stadium, with assumptions,
budgets and multi-year cash flows for office, retail, residential and hotel, and a
returns summary for two scenarios.

| | |
|---|---|
| Pages | 16 |
| Fields in the extraction schema | 40 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:56 | 2026-11-19 03:03 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 124,172 | 124,972 |
| Words under 0.95 confidence | 154 | n/a |
| Words under 0.80 confidence | 33 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 45.3 s | 39.9 s |
| Per page | 2.8 s | 2.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 14.9 credits | 39.3 credits |
| Per page | 0.93 credits | 2.46 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:57 | 2026-11-19 03:04 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 40 | 40 |
| Non-null fields returned | 40 | 40 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 628.1 s | 443.1 s |
| Per schema field (40) | 15.70 s | 11.08 s |
| Per value returned | 3.90 s | 2.82 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 30.7 credits | 30.8 credits |
| Per schema field (40) | 0.767 credits | 0.770 credits |
| Per value returned | 0.191 credits | 0.196 credits |

## Origin

`source/aloha-development-model-jll.pdf` is the **Aloha Development Model** by Jones Lang
LaSalle (JLL). It was published as Exhibit C to the *Aloha Stadium Conceptual
Redevelopment Report* (February 23, 2017), which Foley & Lardner LLP prepared for the
State of Hawaii Department of Accounting and General Services and Stadium Authority.
Most cash flow sheets run 13 development years (3 of construction, then 10 of hold); the
office long-term sheet on page 7 runs 18 (3 of construction, then 15 of hold).

The file keeps **16 of the report's 181 pages**, the whole of Exhibit C as printed
("Page 1 of 16" to "Page 16 of 16"). The pages are **landscape** spreadsheet printouts at
eleven different page sizes, from 792x612 pt up to 1685x1302 pt.

| Page here | Content |
|---|---|
| 1 | Returns summary: two scenarios (sale on stabilization, long-term hold) |
| 2 | Mixed-use assumptions: program, land valuation, parking |
| 3 | Budget assumptions by product type |
| 4 | Mixed-use cash flows, 13 years |
| 5-7 | Office: assumptions, then two own-operate cash flow sheets |
| 8-10 | Retail: assumptions, then two own-operate cash flow sheets |
| 11-13 | Residential: assumptions, then two own-operate cash flow sheets |
| 14-16 | Hotel: assumptions, own-operate cash flows, own-operate sale cash flows |

| | |
|---|---|
| Publisher | Jones Lang LaSalle (model), within a Foley & Lardner LLP report for the State of Hawaii DAGS / Stadium Authority |
| Source | https://alohastadium.hawaii.gov/wp-content/uploads/2026/03/alohastadiumconceptualredevelopmentreport.pdf |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

The State publishes the full report on its own alohastadium.hawaii.gov domain. The
report cover is marked "Privileged and Confidential / Attorney-Client Communication", and
every model page has a "Confidential" footer. Those markings predate the State's own
publication of the report, and they are left as printed. Source pages 160-175 were split
out unchanged. The Exhibit D cash flow projections (source pages 177-181) were left out by
operator decision: they are a separate renovate-versus-rebuild comparison by a different
author. The Exhibit D slip sheet, which names an individual preparer, was also left out.

The kept pages name no individuals and carry no contact details, so nothing was
redacted. The PDF's metadata named an individual author, and it was cleared. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A development pro forma projects what a real estate project will cost, earn and be
worth over time. It is the model behind most decisions to fund, build or sell.

- **Real estate developers and investors:** they test returns, land value and financing
  under different scenarios before committing capital.
- **Construction and permanent lenders:** they read loan terms, cost budgets and debt
  service coverage to size and approve loans.
- **Governments and public agencies:** they review developer and adviser models in
  public-private redevelopment projects, as Hawaii did here.
- **Real estate advisory and valuation firms:** they build and audit pro formas for
  clients and compare assumptions across deals.
- **Asset managers:** they track actual performance against the original projections.

### What it contains

- **Wide cash flow grids** with a Total column followed by 13 or 18 years.
- **Three-row column headers** giving the calendar year, development year and hold
  year.
- **Empty construction-period cells** and negatives shown red and in parentheses.
- **Small type and highlighted key rows,** such as the debt service coverage ratio.
- **One structure repeated for four product types** with identical row labels.
- **Landscape spreadsheet printouts at eleven page sizes.**
