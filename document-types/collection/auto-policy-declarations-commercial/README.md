# Auto Policy Declarations (Commercial)

**On the website:** [landing.ai/document-type/auto-policy-declarations-commercial](https://landing.ai/document-type/auto-policy-declarations-commercial)

The Automobile Policy Declarations of an Owners Insurance Company commercial auto
renewal for a small excavation contractor, for the term 12-29-2015 to 12-29-2016. Ten
vehicles and trailers each have their own block with a VIN, coverages, limits, premiums
and interested parties. The last page totals the premium by coverage.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 25 |

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
| Characters returned | 17,441 | 18,031 |
| Words under 0.95 confidence | 68 | n/a |
| Words under 0.80 confidence | 34 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.7 s | 14.2 s |
| Per page | 1.3 s | 2.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.7 credits | 7.6 credits |
| Per page | 0.45 credits | 1.27 credits |

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
| Fields requested | 25 | 25 |
| Non-null fields returned | 25 | 25 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 436.1 s | 147.7 s |
| Per schema field (25) | 17.44 s | 5.91 s |
| Per value returned | 1.73 s | 0.59 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 11.6 credits | 11.8 credits |
| Per schema field (25) | 0.464 credits | 0.472 credits |
| Per value returned | 0.046 credits | 0.047 credits |

## Origin

`source/owners-insurance-commercial-auto-declarations-redacted.pdf` is the Automobile
Policy Declarations of an Owners Insurance Company (Auto-Owners Insurance Group)
commercial auto renewal for a small excavation contractor, for the term 12-29-2015 to
12-29-2016. It is **6 pages, portrait**, born-digital with a text layer.

| | |
|---|---|
| Publisher | Owners Insurance Company (Auto-Owners Insurance Group) |
| Source | [scribd.com/doc/297561971](https://www.scribd.com/doc/297561971/commercial-auto-policy-12-29-2015-5-3) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | **Redacted** |

Scribd is a user-upload site, so the account that posted this file is not its publisher.
It is a real policy for a real business, and it was treated as a private record and
redacted before it entered the repo.

**Pages kept.** The original file is 58 pages. Only the six declarations pages
(original pages 2 to 7) were kept:

- Page 1, the agency's cover letter, was dropped. It carried the policy number and an
  online-account enrollment code.
- Page 8, the Scheduled Drivers List, was dropped. It lists eight individual drivers
  with their full names and dates of birth, and adds nothing the vehicle schedule does
  not already show.
- Pages 9 to 58 are the policy form, endorsements and the insurer's signature page. They
  are not the declarations and were dropped.

**Values replaced** on the six kept pages:

| What | Occurrences | Replaced with |
|---|---|---|
| Insured business name | 6 | `SAMPLE EXCAVATION INC` |
| Insured mailing address (PO box, city, ZIP+4) | 3 | `PO BOX 10`, `ANYTOWN`, `84790-1394` |
| Agency name | 6 | `EXAMPLE AGENCY` |
| Agency code | 6 | `32-2356-69` |
| Agency phone | 1 | `(435) 555-0176` |
| Policy number | 6 | `95-342-160-75` |
| Company-use account number | 6 | `46-31-UT-3494` |
| VINs, one per vehicle | 10 | random VINs of the same shape |
| Individual named in care of a lienholder | 2 | `PAT EXAMPLE` |

Names and the address are obviously fake. Numeric identifiers are randomly drawn
stand-ins of the same shape, so the page still reads as a real policy. Kept as printed:
the insurer and its address, the two lienholder institutions, the territory county, the
vehicle descriptions, and every limit and premium.

The redaction used `document-types/scripts/redact.py`, which removes the underlying text
rather than drawing a box over it, and clears the PDF metadata. A check afterwards found
no original string in the committed PDF or anywhere in this folder. The rules file stays
outside the repo. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

The declarations pages are the summary of an insurance policy: who and what is covered,
for how much, and at what premium. A commercial fleet policy repeats that summary for
every vehicle.

- **Commercial insurance agents and brokers:** they compare declarations at renewal and
  re-market fleets to other carriers.
- **Underwriters:** they review the vehicle schedule, coverages and rating details of a
  prior policy when quoting a new one.
- **Equipment lenders and lessors:** they confirm that each financed vehicle is listed
  and that they appear as lienholder or interested party.
- **Fleet managers and risk managers:** they track coverage and cost per vehicle across
  a fleet.
- **Contractors' clients and general contractors:** they check auto liability limits
  before work starts.

### What it contains

- **A repeating block per vehicle,** ten in all, each with a description, VIN,
  territory, coverage rows, limits, premiums, a total, interested parties and rating
  details.
- **A schedule that runs across page breaks,** with blocks spread over five pages.
- **Nested lists:** vehicles, each with its own list of coverages.
- **Blank and "None" entries,** such as coverage rows with no limit printed and vehicles
  with no lienholder.
- **A totals page** with premiums by coverage, a paid-in-full discount and the term
  premium. The coverage totals sum to the policy premium, so the figures can be checked
  against each other.
- **Abbreviated running headers** that repeat the insurer's name in short form on later
  pages.
