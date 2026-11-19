# Auto Loss Run

**On the website:** [landing.ai/document-type/auto-loss-run](https://landing.ai/document-type/auto-loss-run)

The Automobile Physical Damage section of a claim/loss report that the Texas
Association of Counties Risk Management Pool produced for Cameron County, Texas. It
covers five policy years, July 2011 to July 2016, and lists 112 claims with their loss
dates, causes and amounts paid, recovered and incurred. Each year closes with a Totals
row, and a summary block repeats the five totals.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 24 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:31 | 2026-11-19 02:30 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 23,603 | 24,800 |
| Words under 0.95 confidence | 19 | n/a |
| Words under 0.80 confidence | 3 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.2 s | 11.4 s |
| Per page | 1.8 s | 2.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.0 credits | 8.2 credits |
| Per page | 0.75 credits | 2.05 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:31 | 2026-11-19 02:30 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 239.4 s | 181.6 s |
| Per schema field (24) | 9.98 s | 7.56 s |
| Per value returned | 0.20 s | 0.16 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 33.8 credits | 34.0 credits |
| Per schema field (24) | 1.408 credits | 1.417 credits |
| Per value returned | 0.029 credits | 0.029 credits |

## Origin

`source/cameron-county-apd-loss-runs-2011-2016.pdf` is the Automobile Physical Damage
section of a Claim/Loss Report produced by the Texas Association of Counties Risk
Management Pool for its member Cameron County, Texas, covering five policy years (July
2011 to July 2016). It is **4 pages, landscape**. Pages 1 to 3 list 112 claims under five
policy headers, each closed by a Totals row; page 3 ends and page 4 continues a summary
block that repeats the five Totals rows.

| | |
|---|---|
| Publisher | Texas Association of Counties Risk Management Pool, posted by Cameron County, Texas |
| Source | [cameroncountytx.gov](https://cameroncountytx.gov/wp-content/uploads/Purchasing/Exhibit-X-F-TAC-GL-AL-APD-Loss-Runs-2011-2016.pdf) |
| Retrieved | 2026-10-25 (downloaded by script) |
| Clearance | **Public** |

Cameron County published this loss run on its own official website, under its
Purchasing uploads, as Exhibit X-F to an insurance RFP, so that bidders could price the
account. The solicitation page that links the exhibit was not found, so provenance rests
on the official county domain. The same pool and county produced the workers'
compensation run behind the [`loss-run`](../loss-run/) page; this one is the auto line.

**Nine pages were dropped and no page text was changed.** The original is 13 pages
across three lines of coverage. Only original pages 5 to 8, Automobile Physical Damage,
are kept, unaltered. On those pages every claimant is the county itself. The Automobile
Liability pages (1 to 4) and General Liability pages (9 to 13) name private claimants;
they were removed whole before the file entered the repo or was parsed. The output was
verified to carry none of the dropped pages' claimant strings, and the PDF's document
metadata was cleared. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A loss run is an insurer's or pool's history of claims on an account. Underwriters ask
for one at every new quote and renewal.

- **Commercial insurance underwriting:** carriers price an account from its claim
  frequency, severity and open reserves across recent years.
- **Insurance brokers:** brokers collect loss runs from the incumbent carrier and send
  them to markets when they shop a renewal.
- **Public entities and risk pools:** counties and cities publish loss runs with
  insurance RFPs, as Cameron County did here, so bidders can price the account.
- **Fleet and risk management:** risk managers track causes of loss across years to
  target safety programs.
- **Mergers and acquisitions:** buyers review a target's loss history during due
  diligence.

### What it contains

- **A wide 10-column claim table** on landscape pages, with most rows showing $0 in
  several columns.
- **Policy headers and Totals rows** that bracket each year's claims inside one
  continuous table.
- **Tables that break across pages,** with two policy years split over a page break.
- **Columns that cannot be derived from one another,** since recoveries can exceed
  what was paid, so each amount has to be read by position.
- **A summary block that spans two pages** and repeats the yearly totals.
- **A logo** in the page header.
