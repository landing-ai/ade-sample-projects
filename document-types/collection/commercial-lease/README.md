# Commercial Lease

**On the website:** [landing.ai/document-type/commercial-lease](https://landing.ai/document-type/commercial-lease)

The Basic Lease Information page of an office lease for 730 Broadway, Redwood City,
California, between Bauen Fund 2018-730, LLC as landlord and Serve Robotics Inc. as
tenant, dated February 25, 2021. It sets out the notice addresses, the premises, a
48-month term, an escalating base-rent schedule with a one-month rent waiver, the
permitted use, the security deposit and the brokers.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 23 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:41 | 2026-11-19 02:44 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,395 | 2,521 |
| Words under 0.95 confidence | 6 | n/a |
| Words under 0.80 confidence | 2 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.4 s | 24.1 s |
| Per page | 3.4 s | 24.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.4 credits | 1.2 credits |
| Per page | 0.40 credits | 1.20 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:41 | 2026-11-19 02:44 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 79.9 s | 89.5 s |
| Per schema field (23) | 3.47 s | 3.89 s |
| Per value returned | 1.86 s | 2.08 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.0 credits | 2.0 credits |
| Per schema field (23) | 0.087 credits | 0.087 credits |
| Per value returned | 0.047 credits | 0.047 credits |

## Origin

`source/commercial-lease-serve-robotics.pdf` is page 1 of an office **Lease Agreement**
for 730 Broadway, Redwood City, California, between Bauen Fund 2018-730, LLC (landlord)
and Serve Robotics Inc. (tenant), dated February 25, 2021. It is **1 page, portrait**,
with a clean text layer, since it was born digital.

The page is the lease's **Basic Lease Information** summary: lease date, landlord and
tenant notice blocks, the premises (an entire 4,200 rentable-square-foot building), a
48-month term, an escalating base-rent table with a one-month rent waiver, permitted
use, security deposit, and the brokers on each side. The remaining 26 pages of the lease
are the standard lease terms, exhibits and conformed signatures.

| | |
|---|---|
| Publisher | Serve Robotics Inc. (filing as Patricia Acquisition Corp.), as filed with the SEC |
| Source | [SEC EDGAR, ea180762ex10-6_patriciaacq.htm](https://www.sec.gov/Archives/edgar/data/1832483/000121390023063662/ea180762ex10-6_patriciaacq.htm) |
| Filing | Exhibit 10.6 (material contract) to Form 8-K, accession 0001213900-23-063662, 2023 |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** |

Serve Robotics filed this lease publicly on EDGAR as a material contract; the filing
index lists `ea180762ex10-6_patriciaacq.htm`. Landlord and tenant are companies. The
people named on the page (a notice contact for each party and the landlord's broker)
appear in a professional capacity. No private individual's personal data is present,
so nothing was replaced.

EDGAR publishes this exhibit as HTML, not PDF. The EDGAR URL above remains the source of
record, and the PDF here is a rendering of it. The `.htm` exhibit was downloaded by
script, the EDGAR SGML wrapper lines and a tracking `<script>` tag EDGAR injects were
stripped, and the exhibit's own HTML was printed, unchanged, to a US Letter PDF with
headless Chrome. The full exhibit renders to 27 pages. Only page 1, the Basic Lease
Information, is kept, and the PDF metadata (Chrome creator and producer, a temp-file
title, creation dates) was cleared. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A commercial lease sets the rent, term and obligations for a business's space, and its
summary page holds the terms that people track for years afterward.

- **Commercial real estate and property management:** landlords and managers abstract
  rent schedules, deposits and notice addresses into their lease administration
  systems.
- **Corporate real estate and finance:** tenants record lease terms and payments for
  lease accounting under ASC 842 and IFRS 16.
- **Lenders and investors:** they review the leases behind a property in a rent roll
  during underwriting and due diligence.
- **Brokers:** they compare deal terms such as rent per square foot, term and
  concessions across transactions.
- **Legal and M&A teams:** they review material leases, often from public filings like
  this one, during acquisitions and audits.

### What it contains

- **A two-column defined-terms grid** with no ruling, pairing each term with its value.
- **Prose values** for the premises, term and use, with numbers written in words and
  figures.
- **A base-rent table** with per-square-foot rates and a footnoted partial-month rate.
- **Multi-line notice address blocks** for landlord and tenant.
- **A born-digital text layer** rendered from HTML.
