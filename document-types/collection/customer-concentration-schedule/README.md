# Customer Concentration Schedule

**On the website:** [landing.ai/document-type/customer-concentration-schedule](https://landing.ai/document-type/customer-concentration-schedule)

Two exhibits from DC Water's FY2025 Annual Comprehensive Financial Report: its ten
largest commercial customers and its ten largest government customers, each over the
last ten fiscal years. Each page is one grid of revenue by customer and year, in
thousands of dollars, with a total row and that total's share of operating revenues.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 13 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:48 | 2026-11-19 02:54 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 6,193 | 6,284 |
| Words under 0.95 confidence | 6 | n/a |
| Words under 0.80 confidence | 2 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.3 s | 6.1 s |
| Per page | 1.6 s | 3.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.0 credits | 2.6 credits |
| Per page | 0.50 credits | 1.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:48 | 2026-11-19 02:54 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 13 | 13 |
| Non-null fields returned | 13 | 13 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 106.8 s | 94.4 s |
| Per schema field (13) | 8.22 s | 7.26 s |
| Per value returned | 0.76 s | 0.67 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.3 credits | 6.3 credits |
| Per schema field (13) | 0.485 credits | 0.485 credits |
| Per value returned | 0.045 credits | 0.045 credits |

## Origin

`source/dc-water-fy2025-largest-customers.pdf` holds two exhibits from the statistical
section of the FY2025 Annual Comprehensive Financial Report of the District of Columbia
Water and Sewer Authority (DC Water): Exhibit 6, *Ten Largest Commercial Customers, Last
Ten Fiscal Years*, and Exhibit 7, *Ten Largest Government Customers, Last Ten Fiscal
Years*, both in thousands of dollars. It is **2 pages, landscape**, with a native text
layer. They are pages 11 and 12 of the 34-page statistical section (printed pages 88 and
89).

Each page is one ten-year grid: a customer column, ten fiscal-year columns (2025 back to
2016), a Total row and a `% of Total Operating Revenues` row. The commercial grid lists
16 customers and the government grid 11, because a customer that left the top ten still
has a row, with `-` in the years it did not qualify.

A public utility stands in for a diligence schedule here. A private company's customer
concentration schedule, with revenue and share by customer, is not something anyone
publishes; a utility's ACFR is the public document that carries the same table.

| | |
|---|---|
| Publisher | District of Columbia Water and Sewer Authority (DC Water) |
| Source | [dcwater.com/…/FY25 ACFR Statistical Section.pdf](https://www.dcwater.com/sites/default/files/finance/ACFR/2025/FY25%20ACFR%20Statistical%20Section.pdf), pages 11-12 of 34 |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

DC Water publishes its ACFR on its own website for bondholders and the public. The two
pages the operator chose were split out and the rest of the section dropped. There is no
personal data: every customer is a university, hospital, company or government agency.
Nothing was redacted. The split file's document metadata was cleared, and the committed
PDF carries none. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A customer concentration schedule shows how much of a business's revenue depends on a
few customers. Buyers, lenders and analysts ask for it whenever that dependence could
change the value of the business.

- **M&A and private equity due diligence:** deal teams use it to size the risk of losing
  a top customer.
- **Commercial lending:** credit analysts check whether one customer's loss would break
  the borrower's cash flow.
- **Municipal bond analysis:** analysts and rating agencies read the largest-customer
  exhibits in utility ACFRs to judge the stability of the revenue base.
- **Auditors and financial reporting:** concentration disclosures are checked against
  the revenue ledger.
- **Investors and equity research:** analysts track the trend in the top customers'
  share over time.

### What it contains

- **Wide multi-year grids,** with sixteen rows by ten fiscal-year columns on one page.
- **Dollar signs in their own column,** on the first and Total rows only.
- **Dash cells** that mark years a customer was not in the top ten, which make up much
  of each grid.
- **A total row and a percentage row** under each grid.
- **Multi-line exhibit titles** and a units note (thousands of dollars).
- **Landscape pages** with a native text layer.
- **Small rounding differences** between the rows and the printed totals, as published.
