# Property Inspection Report

**On the website:** [landing.ai/document-type/property-inspection-report](https://landing.ai/document-type/property-inspection-report)

A residential home inspection report for a two-story single-family house in Virginia
Beach, published as a sample by a maker of inspection report software. After a cover
and site details, it covers each system of the house in turn with numbered,
categorized observations and photographs, then closes with a conclusion and a Report
Summary table of significant deficiencies.

| | |
|---|---|
| Pages | 30 |
| Fields in the extraction schema | 36 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:45 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 98,246 | 103,752 |
| Words under 0.95 confidence | 134 | n/a |
| Words under 0.80 confidence | 25 | n/a |
| Words under 0.50 confidence | 5 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 25.6 s | 34.2 s |
| Per page | 0.9 s | 1.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 14.4 credits | 41.0 credits |
| Per page | 0.48 credits | 1.37 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:23 | 2026-11-19 03:46 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 36 | 36 |
| Non-null fields returned | 36 | 36 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 610.1 s | 201.6 s |
| Per schema field (36) | 16.95 s | 5.60 s |
| Per value returned | 2.60 s | 0.86 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 33.2 credits | 34.3 credits |
| Per schema field (36) | 0.922 credits | 0.953 credits |
| Per value returned | 0.141 credits | 0.146 credits |

## Origin

`source/VideoSampleReport1.pdf` is a residential home inspection report for a two-story
single-family house in Virginia Beach, written by Safe House Property Inspections LLC
with Home Inspector Pro's report software. It is **30 pages, portrait**: a cover page,
site details, then one section per system (roof and attic, exterior, interior, kitchen,
HVAC, plumbing, electrical, garage, crawlspace), each with numbered, color-coded
observations and photographs, a conclusion, and a two-page Report Summary table of
significant deficiencies.

| | |
|---|---|
| Publisher | Home Inspector Pro, Inc. (sample produced by Safe House Property Inspections LLC) |
| Source | [homeinspectorpro.com/…/VideoSampleReport1.pdf](https://homeinspectorpro.com/wp-content/uploads/2025/04/VideoSampleReport1.pdf) |
| Linked from | [Home Inspector Pro Sample Reports](https://homeinspectorpro.com/inspection-sample-reports/) |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public |

Home Inspector Pro sells inspection report software and publishes this report as a
sample of what it produces. The client and agent are specimen entries ("Mr. and Mrs.
Sample", "Top Agent - Virginia Beach Realty") and the address is the specimen "1234
Sample Report Rd". The only real person named is the inspector, as the report's author
and the company's owner. There are no phone numbers, email addresses or license numbers.
The photographs show a real house and its systems, with no people, no legible house
number and no plates. **No redaction was needed.** The file is committed unchanged: it
carries an owner password only (it opens without one) and video annotations on three
pages. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A home inspection report records the condition of a house, usually before a sale. Buyers,
agents and others downstream read it to decide what needs fixing and who pays.

- **Real estate agents and buyers:** they use the findings to negotiate repairs, credits
  or price before closing.
- **Mortgage lending:** lenders and appraisers review safety and structural findings
  that can affect a loan.
- **Home insurance:** underwriters check the roof, electrical and plumbing findings
  before writing or renewing a policy.
- **Home warranty companies and contractors:** they use the deficiency list to scope
  coverage, quotes and repairs.
- **Sellers and listing agents:** pre-listing inspections tell a seller what to repair
  or disclose before the house goes on the market.

### What it contains

- **A long narrative report.** Most of its content is numbered findings in running
  prose, each prefixed with a category label (IMPROVE, MAINTENANCE, SAFETY CONCERN, FYI)
  and often ending in a LOCATION.
- **Many photographs,** with descriptive sentences printed above the photos they
  describe.
- **Findings that run over several lines,** with the item number and location on
  different lines of the same item.
- **A Report Summary table** over two pages whose cells each hold one or more findings.
- **Running page headers** with printed page numbers ("Page 3 of 29") that do not
  count the cover.
- **Video annotations** on three pages.
