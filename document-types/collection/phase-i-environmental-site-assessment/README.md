# Phase I Environmental Site Assessment

**On the website:** [landing.ai/document-type/phase-i-environmental-site-assessment](https://landing.ai/document-type/phase-i-environmental-site-assessment)

A Phase I Environmental Site Assessment by Kimley-Horn and Associates for Norman Y.
Mineta San José International Airport, covering the 3.6-acre Orange Lot in Santa Clara,
California, issued June 30, 2025. It describes the site and its history, reviews
regulatory databases and nearby release sites, and reports one controlled recognized
environmental condition and one business environmental risk.

| | |
|---|---|
| Pages | 39 |
| Fields in the extraction schema | 43 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:21 | 2026-11-19 03:42 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 96,089 | 96,208 |
| Words under 0.95 confidence | 297 | n/a |
| Words under 0.80 confidence | 93 | n/a |
| Words under 0.50 confidence | 25 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 34.5 s | 45.1 s |
| Per page | 0.9 s | 1.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.5 credits | 43.6 credits |
| Per page | 0.40 credits | 1.12 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:43 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 43 | 43 |
| Non-null fields returned | 43 | 43 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 344.2 s | 246.7 s |
| Per schema field (43) | 8.00 s | 5.74 s |
| Per value returned | 1.10 s | 0.80 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 29.9 credits | 29.9 credits |
| Per schema field (43) | 0.695 credits | 0.695 credits |
| Per value returned | 0.095 credits | 0.096 credits |

## Origin

`source/orange-lot-phase-i-esa.pdf` is a Phase I Environmental Site Assessment (ESA) by
Kimley-Horn and Associates, Inc. for Norman Y. Mineta San José International Airport:
**San Jose Airport Orange Lot, Martin Avenue and De La Cruz Boulevard, Santa Clara,
California** (Kimley-Horn project 097042828, issued June 30, 2025). The assessment covers
a 3.6-acre parking lot and taxiway strip at the northwest corner of the airport,
performed under ASTM E1527-21 and the EPA's All Appropriate Inquiries rule. It finds no
RECs or HRECs, one CREC (residual contamination from a nearby Unocal station that reached
the property) and one business environmental risk (a 2016 firefighting foam release at a
neighbouring hangar).

It is **39 pages, portrait, US Letter**, with a text layer. The file is the report body
only: the appendices it lists (figures, photographs, EDR reports, closure documents,
resumes) were not posted, and all 39 pages are kept.

| | |
|---|---|
| Publisher | Kimley-Horn and Associates, Inc. (consultant); posted by Norman Y. Mineta San José International Airport |
| Source | https://www.flysanjose.com/sites/default/files/users/user143716/Orange%20Lot%20ESA%20Report.pdf |
| Context | Posted on the airport's own website; no linking page was found |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

A consultant's report prepared for a city-owned airport and published by the airport on
its own domain. The PDF's pages are committed exactly as downloaded; only its document
metadata was cleared.

The report names the Environmental Professional who conducted it (executive summary,
reconnaissance table and declaration page, which also carries her signature) and one
airport staff member interviewed in her professional role. Both are professional details
in a public agency record, and by the operator's decision the document is published
unredacted, as the publisher filed it. The PDF's hidden /Info and XMP metadata, which
named the Environmental Professional as author, was cleared, also by the operator's
decision; the visible pages are unchanged. The assessor's parcel number is a public
parcel identifier. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A Phase I ESA checks a property's current and past uses for signs of contamination
before it is bought, financed or developed. It is a standard step in commercial real
estate due diligence.

- **Commercial real estate lending:** lenders require a Phase I before they take a
  property as collateral, and read its findings and recommendations.
- **Buyers and investors:** a Phase I done under ASTM E1527-21 supports defenses to
  liability under federal cleanup law.
- **Environmental consultants:** they prepare reports and review earlier ones for the
  same or nearby sites.
- **Public agencies and airports:** owners such as this one commission assessments
  before leasing or redeveloping land.
- **Insurers and attorneys:** they review the findings when underwriting environmental
  risk or negotiating indemnities.

### What it contains

- **39 pages of narrative prose,** with key facts scattered across sections.
- **Findings stated twice,** in the executive summary and again in Section 7.
- **A regulatory database table** that runs across three pages.
- **A two-column table of 22 nearby release sites** whose rows break across pages.
- **A small table of viability dates** below the executive summary.
- **A signed declaration page.**
- **A source error:** page 7 carries a paragraph pasted from another report, citing a
  different ASTM standard and address.
