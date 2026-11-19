# Master Services Agreement

**On the website:** [landing.ai/document-type/master-services-agreement](https://landing.ai/document-type/master-services-agreement)

A Master Services Agreement between Williamson County, Texas and Power DMS by NEOGOV,
with the vendor's order form attached as Exhibit A. The county's terms cover the
services, a 12-month term with automatic renewals, a not-to-exceed amount, payment,
indemnification, venue and audit rights. The order form adds billing details, payment
terms and two subscription pricing tables.

| | |
|---|---|
| Pages | 7 |
| Fields in the extraction schema | 39 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:18 | 2026-11-19 03:35 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 21,128 | 21,912 |
| Words under 0.95 confidence | 63 | n/a |
| Words under 0.80 confidence | 27 | n/a |
| Words under 0.50 confidence | 7 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 10.6 s | 18.8 s |
| Per page | 1.5 s | 2.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.2 credits | 9.0 credits |
| Per page | 0.46 credits | 1.29 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:18 | 2026-11-19 03:35 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 39 | 39 |
| Non-null fields returned | 37 | 37 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 131.4 s | 372.5 s |
| Per schema field (39) | 3.37 s | 9.55 s |
| Per value returned | 1.85 s | 5.25 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.6 credits | 6.7 credits |
| Per schema field (39) | 0.169 credits | 0.172 credits |
| Per value returned | 0.093 credits | 0.094 credits |

## Origin

`source/msa-williamson-county-powerdms.pdf` is a **Master Services Agreement** between
Williamson County, Texas and Power DMS by NEOGOV, with the vendor's order form attached
as Exhibit A. It is **7 pages, portrait**, born digital except for page 5, which is a
scan.

- **Pages 1-5** are the county's standard master agreement: recitals, services, a
  12-month term with up to five automatic one-year renewals, a not-to-exceed amount of
  $7,564.33, Texas prompt-payment terms, indemnification, venue, a three-year audit
  right, no assignment, and the signature page.
- **Page 5**, the signature page, is a scan, not a text page. The vendor's block carries
  a DocuSign signature, printed name and date, with a legal-review initials stamp beside
  it. The county's block is blank.
- **Pages 6-7** are Exhibit A, the vendor's two-page order form: contract records,
  billing and shipping contacts, Net 60 payment terms, two subscription pricing tables
  (a prorated October-November 2024 period and a December 2024-November 2025 year),
  special conditions, and side-by-side signature columns for the two parties.

| | |
|---|---|
| Publisher | Williamson County, Texas (Commissioners Court) |
| Source | [Commissioners Court agenda attachment, February 11, 2025](https://public.destinyhosted.com/wilcodocs/2025/COM/20250211_1884/36121%5FMSA%5FPower%5FDMS%5F%2D%5F02%2E05%2E2025%5FGC%5FStamp%5F%2D%5FRedacted%2Epdf) |
| Linked from | [The court's public agenda](https://public.destinyhosted.com/94526/agenda/agenda.cfm?seq=1872) |
| Retrieved | 2026-10-28, by script |
| Clearance | Public |

The county published this contract as an attachment to a public Commissioners Court
agenda. **It is published here as the county filed it: nothing was replaced.** That was
the document owner's explicit decision. The county had already blacked out the order
form's account and order numbers, and no text sits under those boxes. The parties are a
county and a software company. The vendor's signer appears in a professional capacity
on pages 5 and 7, with two DocuSign signatures. The contact details on the order form
are a county department's accounts-payable mailbox and office phone. The PDF carried no
metadata. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A master services agreement sets the legal terms for an ongoing vendor relationship, and
the order forms under it set what is bought and at what price.

- **Procurement and vendor management:** teams track terms, renewal dates and spending
  caps across every contract with a vendor.
- **Government purchasing and contract administration:** counties and agencies check
  contracts against approved amounts and statutory payment terms.
- **Legal and contract management:** lawyers review indemnification, venue, audit and
  assignment clauses, and contract systems store them as structured terms.
- **Accounts payable and finance:** staff match invoices to the order form's pricing,
  periods and payment terms.
- **Software vendors and revenue operations:** sales and billing teams record
  subscription quantities, periods and totals from signed order forms.

### What it contains

- **Two documents with different authors in one file:** numbered legal clauses on pages
  1-5 and a vendor-branded order form on pages 6-7.
- **An amount in words and figures** inside a contract clause.
- **Label/value grids and ruled pricing tables** on the order form, with a table that
  breaks across the page.
- **A scanned page in a born-digital PDF,** with a DocuSign signature and a handwritten
  legal-review initials stamp.
- **Side-by-side signature columns,** one signed and one blank.
- **Redaction boxes** over the account and order numbers.
