# Purchase and Sale Agreement

**On the website:** [landing.ai/document-type/purchase-and-sale-agreement](https://landing.ai/document-type/purchase-and-sale-agreement)

A fully executed Arizona Association of REALTORS Residential Resale Real Estate
Purchase Contract, in which one LLC buys a single-family home in Tucson from another for
$845,000, all cash. It sets out the property and price, title and escrow, disclosures,
warranties, due diligence, remedies and additional terms, with DocuSign signatures and
initials on every page.

| | |
|---|---|
| Pages | 10 |
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
| Processed (UTC) | 2026-11-19 03:26 | 2026-11-19 03:47 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 54,078 | 56,528 |
| Words under 0.95 confidence | 234 | n/a |
| Words under 0.80 confidence | 125 | n/a |
| Words under 0.50 confidence | 47 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 12.1 s | 24.2 s |
| Per page | 1.2 s | 2.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.0 credits | 19.2 credits |
| Per page | 0.70 credits | 1.92 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:27 | 2026-11-19 03:47 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 43 | 43 |
| Non-null fields returned | 42 | 42 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 132.3 s | 158.6 s |
| Per schema field (43) | 3.08 s | 3.69 s |
| Per value returned | 2.88 s | 3.37 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 12.7 credits | 13.2 credits |
| Per schema field (43) | 0.295 credits | 0.307 credits |
| Per value returned | 0.276 credits | 0.281 credits |

## Origin

`source/purchase-and-sale-agreement-az-realtors.pdf` is a fully executed Arizona
Association of REALTORS **Residential Resale Real Estate Purchase Contract** (form dated
February 2020). It is **10 pages, portrait**. The pre-printed form has a text layer, but
the filled-in values are drawn without one.

An LLC buys a single-family home in Tucson from another LLC for $845,000, all cash. The
form is the standard Arizona resale contract: property and price (Section 1), financing
(not used here), title and escrow, disclosures, warranties, due diligence, remedies,
typed additional terms, and the buyer's offer and seller's acceptance with DocuSign
signatures and initials on every page.

| | |
|---|---|
| Publisher | Here Collection LLC, as filed with the SEC; pre-printed form by the Arizona Association of REALTORS |
| Source | [SEC EDGAR, here_ex6z17.pdf](https://www.sec.gov/Archives/edgar/data/1876769/000109690622001941/here_ex6z17.pdf) |
| Filing | Exhibit EX1A-6 (material contract) to Form 1-A POS, accession 0001096906-22-001941, filed 2022-08-18 |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** |

Here Collection filed this contract publicly on EDGAR as a material contract of its
Regulation A offering, and the filing index lists `here_ex6z17.pdf`. Buyer and seller
are both LLCs. Everyone else named acts in a professional capacity: the seller's listing
agent and brokerage with their license numbers, the escrow officer at the title company,
and the LLC signers whose e-signatures and initials are on the form. No private
individual's personal data is present, so nothing was replaced.

Two changes from the filed PDF:

- **Page 1 was dropped.** It is the one-page Buyer Attachment, an advisory checklist that
  says on its face it is not part of the contract's terms. The sample is the ten-page
  contract alone, so page numbers here are the filed PDF's minus one.
- **PDF metadata was cleared** (PDFium creator/producer and a creation date). The pages
  are otherwise unchanged.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A purchase contract sets the terms of a real estate sale: the parties, the property, the
price, and the dates and conditions that lead to closing. Every transaction file starts
from one.

- **Title and escrow companies:** they open escrow from the contract and follow its
  price, earnest money, close-of-escrow date and addenda.
- **Mortgage lenders:** underwriters check the price, parties and property against the
  loan application and appraisal.
- **Real estate brokerages:** transaction coordinators track the inspection period,
  deadlines and signatures for compliance files.
- **Real estate investors and funds:** they keep contracts as records of each
  acquisition, as Here Collection did in its SEC filing.
- **Real estate attorneys:** they review the terms, remedies and additional terms when
  a deal is negotiated or disputed.

### What it contains

- **Filled-in values with no text layer,** set on a pre-printed form that does have
  one, so the values have to be read from the page image.
- **Values threaded through numbered form lines.**
- **Checkboxes** for financing, addenda, warranties and other elections.
- **Split date blanks,** with month, day and year in separate blanks.
- **Printed defaults** that a typed value overrides.
- **DocuSign signatures and initials** on every page.
- **A typed additional terms section** in free text.
