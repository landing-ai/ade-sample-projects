# Bid tabulation

**On the website:** [landing.ai/document-type/bid-tabulation](https://landing.ai/document-type/bid-tabulation)

The engineer's bid tabulation for a sewer collection system project in Jackson
Township, Indiana, for bids received June 12, 2026. It sets three bidders' unit prices
and totals beside the Engineer's Estimate for every line item, across a base bid and
four mandatory alternates, with a checklist of each bidder's submittals and the
engineer's certification.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 32 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:36 | 2026-11-19 02:33 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 24,001 | 24,223 |
| Words under 0.95 confidence | 37 | n/a |
| Words under 0.80 confidence | 25 | n/a |
| Words under 0.50 confidence | 10 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.6 s | 11.0 s |
| Per page | 2.4 s | 2.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.1 credits | 8.1 credits |
| Per page | 0.78 credits | 2.02 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:36 | 2026-11-19 02:33 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 32 | 32 |
| Non-null fields returned | 32 | 32 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 377.7 s | 339.2 s |
| Per schema field (32) | 11.80 s | 10.60 s |
| Per value returned | 0.29 s | 0.26 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 41.0 credits | 41.0 credits |
| Per schema field (32) | 1.281 credits | 1.281 credits |
| Per value returned | 0.032 credits | 0.032 credits |

## Origin

`source/S18018-Div-B-Bid-Tab.pdf` is the bid tabulation for **Jackson Township Regional
Sewer District, Wastewater System Improvements, Division "B" - Collection System
Improvements** (Indiana), for bids received June 12, 2026. Commonwealth Engineers, Inc.,
the consulting engineer of record, prepared and certified it. It is **4 pages,
landscape**, with a text layer: it is an Excel workbook printed to PDF.

| | |
|---|---|
| Publisher | Commonwealth Engineers, Inc., for the Jackson Township Regional Sewer District |
| Source | [commonwealthengineers.com/…/S18018-Div-B-Bid-Tab.pdf](https://commonwealthengineers.com/wp-content/uploads/2026/06/S18018-Div-B-Bid-Tab.pdf) |
| Retrieved | 2026-10-14, downloaded directly by script |
| Clearance | Public |

The engineer posts the tabulation on its own website, as public bid results usually are.
The bidders are companies. The only people named act in an official capacity: the staff
member who prepared the tabulation (page 1), and the certifying professional engineer,
with his Indiana P.E. registration number, signature and seal (page 4). P.E.
registrations are public record. No redaction was needed. The PDF's metadata named a
staff username as author, so it was cleared. Each page footer prints the engineer's
internal file-server path, which is kept as printed.

The engineer's projects-for-bid page now lists this project as a rebid, so these bids
were probably rejected. That makes no difference to the document as a sample. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A bid tabulation is the engineer's record of a public bid opening: every bidder's price
for every line item, set beside the Engineer's Estimate. Owners use it to find the
apparent low bidder and check the bids for irregularities before an award.

- **Public works owners:** cities, utilities and districts review the tabulation before
  recommending a contract award.
- **Consulting engineers:** they prepare and certify the tabulation and flag
  irregularities, such as a bidder's unit price that differs between schedules.
- **Contractors and estimators:** bidders study competitors' unit prices to price
  future work.
- **Cost estimators and analysts:** published tabulations feed historical unit-cost
  databases used to build engineer's estimates.
- **Surety and construction finance:** sureties and funding agencies check the bid
  amounts and the bid bond behind the award.

### What it contains

- **A wide table with eleven columns per row.** Item, description, quantity and unit,
  then a Unit Price and Total pair for the Engineer's Estimate and for each of three
  bidders, with blank spacer columns between them.
- **Merged header cells** with each bidder's name and address over its price pair.
- **A checklist grid** of submittal rows ("Bid Bond", "E-Verify" and so on) where every
  cell reads "Yes", so only the cell's position says which bidder and document it
  belongs to.
- **Five schedules over three pages,** the base bid and four mandatory alternates, each
  repeating the bidder header and column layout.
- **Deduct lines** with negative quantities and totals, and totals that reconcile down
  the columns and across pages to the grand total.
- **Yellow-highlighted cells and engineer's notes** on a bidder irregularity.
- **A signature and an embossed engineer's seal** on the certification page.
