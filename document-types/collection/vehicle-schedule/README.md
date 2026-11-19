# Vehicle Schedule

**On the website:** [landing.ai/document-type/vehicle-schedule](https://landing.ai/document-type/vehicle-schedule)

Addendum 1 to Louisa County, Virginia's request for proposals for property and casualty
insurance for its fire and EMS services, April 2021. It answers bidders' questions, with
a table of current premiums by coverage, and attaches the vehicle schedule: 86 fire and
EMS units with year, make, model, body type, VIN, agreed value and location, grouped by
fire company and rescue squad.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 20 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:43 | 2026-11-19 03:58 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 16,618 | 16,899 |
| Words under 0.95 confidence | 29 | n/a |
| Words under 0.80 confidence | 3 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.3 s | 7.6 s |
| Per page | 1.3 s | 1.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.3 credits | 6.3 credits |
| Per page | 0.57 credits | 1.57 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:43 | 2026-11-19 03:58 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 20 | 20 |
| Non-null fields returned | 20 | 20 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 161.3 s | 159.8 s |
| Per schema field (20) | 8.06 s | 7.99 s |
| Per value returned | 0.22 s | 0.22 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 22.2 credits | 22.1 credits |
| Per schema field (20) | 1.110 credits | 1.105 credits |
| Per value returned | 0.030 credits | 0.030 credits |

## Origin

`source/louisa-county-fire-ems-vehicle-schedule-2021.pdf` is Addendum 1 to Louisa
County, Virginia's RFP ES-21-04, *Property and Casualty Insurance Services for Louisa
County Fire and EMS* (April 29, 2021). It is **4 pages, portrait**. Pages 1 and 2 are
the addendum's questions and answers, including a current-premium-by-coverage table on
page 1. Pages 3 and 4 are the attached vehicle schedule "as of April 2021": 86 fire and
EMS units in a nine-column table (Veh #, Year, Make, Model, Body Type, VIN, Agreed
Value, Unique Id, Loc), grouped under twelve section headers, one per fire company,
rescue squad or the county itself.

| | |
|---|---|
| Publisher | County of Louisa, Virginia, Finance Department |
| Source | [louisacounty.gov](https://louisacounty.gov/DocumentCenter/View/6988/RFP-ES-21-04-Property-and-Casualty-Addendum-1?bidId=) |
| Retrieved | 2026-10-25 (downloaded by script) |
| Clearance | **Public** |

The county published this addendum on its own website so that insurers bidding on the
fire and EMS program could price the fleet. A vehicle schedule is exactly what an auto
liability and physical damage quote is priced from, so this is a public record of a real
one.

No page content was changed. The schedule lists government fleet vehicles, VINs and
station identifiers, and names no private individual. The PDF's document metadata
carried the Word user name of the county employee who prepared it. It was cleared
before the file entered the repo, and the source PDF now carries no metadata.

It is an entity-prepared fleet list, not an ACORD 129 vehicle schedule form. The
operator accepted that when choosing this sample, since most commercial fleets submit
their schedule as a spreadsheet export like this one. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A vehicle schedule lists every unit a business or public body wants insured. Commercial
auto quotes, renewals and mid-term changes are priced from it.

- **Commercial insurance brokers:** they collect the schedule from the client and
  submit it to insurers with the application.
- **Underwriters:** they rate each vehicle by year, type, value and garaging location.
- **Public entities and procurement offices:** counties and cities attach fleet lists to
  insurance RFPs, as Louisa County did here.
- **Fleet and risk managers:** they keep the schedule current as units are added or
  retired.
- **Insurance carriers' policy administration teams:** they load the schedule into the
  policy system and issue certificates and ID cards from it.

### What it contains

- **A dense ruled table** of about 55 rows per page with nine columns.
- **Section header rows** that split the table by fire company or rescue squad, with one
  section running across the page break.
- **Irregular cells:** blank models, blank or starred vehicle numbers, a VIN with an
  embedded space, and a value printed as `280 ,000`.
- **Text in a numeric column,** such as "Portable Equip" and "Inland Marine" where an
  amount is expected.
- **Values in the wrong column.** A boat and outboard motor have their values written in
  the VIN column.
- **Questions and answers in prose** on the first two pages, with a small premium table.
