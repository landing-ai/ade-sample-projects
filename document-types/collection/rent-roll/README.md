# Rent Roll

**On the website:** [landing.ai/document-type/rent-roll](https://landing.ai/document-type/rent-roll)

The rent roll for Lund Pointe Apartments, a 25-unit multifamily property in Port
Orchard, Washington, from the broker's 2016 offering memorandum. It is one table with a
row per unit (unit, bed/bath, status, square feet, total rent and other charges) and a
totals row, under a header naming the property and its address.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 16 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:28 | 2026-11-19 03:48 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,845 | 2,875 |
| Words under 0.95 confidence | 2 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.4 s | 6.8 s |
| Per page | 2.4 s | 6.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.3 credits |
| Per page | 0.50 credits | 1.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:28 | 2026-11-19 03:49 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 16 | 16 |
| Non-null fields returned | 16 | 16 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 386.2 s | 111.3 s |
| Per schema field (16) | 24.14 s | 6.96 s |
| Per value returned | 2.10 s | 0.60 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 4.3 credits | 4.3 credits |
| Per schema field (16) | 0.269 credits | 0.269 credits |
| Per value returned | 0.023 credits | 0.023 credits |

## Origin

`source/lund-pointe-rent-roll.pdf` is the **rent roll** for Lund Pointe Apartments, a
25-unit multifamily property in Port Orchard, Washington. It comes from the offering
memorandum the listing broker, Neil Walter Company, published to market the property in
2016. It is **1 page, landscape** (page 11 of the 17-page offering memorandum), with a
native text layer and no scanning.

| | |
|---|---|
| Publisher | Neil Walter Company Commercial Real Estate |
| Source | [neilwalter.com/…/Lund-PointeApts_OfferingMemorandum.pdf](https://www.neilwalter.com/wp-content/uploads/2016/02/Lund-PointeApts_OfferingMemorandum.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

The broker publishes the offering memorandum on its own website for prospective buyers.
Only the rent roll page was kept. The page carries no personal data: no tenant names,
lease dates, deposits or contact details. Nothing was redacted. The source PDF's
document metadata named the preparer's user account, so it was cleared when the page was
split out, and the committed file carries none.

The `Other Charges` column repeats the `Total` column on every row, which is an error in
the source. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A rent roll lists every unit in a rental property with its status and rent. It is the
first schedule anyone reads when valuing or lending on an income property.

- **Commercial real estate investors:** buyers underwrite a property's income from the
  rent roll in the offering memorandum.
- **Multifamily and commercial lenders:** underwriters check occupancy and rents to size
  a loan, and ask for updated rent rolls during the loan.
- **Brokers:** listing brokers publish rent rolls to market properties, as Neil Walter
  Company does here.
- **Appraisers:** appraisers compare in-place rents with market rents to value the
  property.
- **Property management and asset management:** managers reconcile rent rolls against
  leases and collections each month.

### What it contains

- **One long, repetitive table** of 25 unit rows that all look alike, so rows must stay
  aligned without dropping, duplicating or shifting.
- **A totals row** that reconciles to the unit rows for rent and square footage.
- **Combined cells,** such as `3/2.00` for bedrooms and bathrooms.
- **Two columns with the same values** on every row.
- **A header line** that packs the property name, address range, unit list, city, state
  and ZIP into one line.
