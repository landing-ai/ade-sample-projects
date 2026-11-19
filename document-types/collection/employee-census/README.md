# Employee Census

**On the website:** [landing.ai/document-type/employee-census](https://landing.ai/document-type/employee-census)

An Employee Census Report from AdvanStaff HR's demo company, listing 34 active employees
one row each. Every row gives the employee's name, ID, status, birth date, age, marital
status, state, gender, last and original hire dates, term date and annual pay. All the
employees are fictional demo records.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 18 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:52 | 2026-11-19 02:58 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 7,097 | 7,103 |
| Words under 0.95 confidence | 2 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.1 s | 10.7 s |
| Per page | 6.1 s | 10.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.9 credits | 2.3 credits |
| Per page | 0.90 credits | 2.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:52 | 2026-11-19 02:59 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 18 | 18 |
| Non-null fields returned | 17 | 17 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 225.9 s | 116.5 s |
| Per schema field (18) | 12.55 s | 6.47 s |
| Per value returned | 0.63 s | 0.33 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 11.0 credits | 11.0 credits |
| Per schema field (18) | 0.611 credits | 0.611 credits |
| Per value returned | 0.031 credits | 0.031 credits |

## Origin

`source/advanstaff-employee-census-report.pdf` is an **Employee Census Report with Status
Class "Active"** for AdvanStaff HR's demo company `*ASI DEMO - GENERAL COMPANY`, run on
23 May 2025. It is **1 page, landscape**, with a native text layer. It lists 34 active
employees, one row each: name, employee ID, status, birth date, age, marital status,
state, gender, last and original hire dates, term date and annual pay.

| | |
|---|---|
| Publisher | AdvanStaff HR |
| Source | [advanstaff.com/wp-content/uploads/2025/05/reporting_sales-final.pdf](https://advanstaff.com/wp-content/uploads/2025/05/reporting_sales-final.pdf) |
| Linked from | [advanstaff.com/help/introduction-to-reporting/](https://advanstaff.com/help/introduction-to-reporting/) |
| Retrieved | 2026-10-28 (downloaded by script) |
| Clearance | Public |

The source is AdvanStaff HR's own "Reporting Options" sales PDF, which shows example
output from its HR and payroll system. The original is six pages: a cover page, a
dashboard, and four demo reports. **Only page 4, the census report, was kept**; the
other pages were dropped.

**No redaction was needed.** Every employee is a fictional demo record with an
alliterative name (Abagail Aarons, Beth Baker, Chloe Cook), and 32 of the 34 carry a
`DEMO` suffix. The two without one follow the same alliterative pattern and appear as
new hires of the same demo company in the PDF's other demo reports, beside suffixed demo
hires, so they were treated as fictional too. The PDF's document metadata, which named
the person who produced the sales PDF, was cleared. The page is otherwise unchanged.

The footer reads "Page 1 of 2". The second page of the census is not in the publisher's
PDF, so the sample stops at the 34th row. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

An employee census is what an employer hands a benefits broker, insurer or PEO to get a
group quote: one row per employee with the attributes coverage is rated on. This one is
an HR and payroll-style census, without the coverage-tier or ZIP columns a carrier's
template would carry.

- **Benefits brokers:** they collect a census from each client to shop group health,
  life and disability coverage.
- **Group insurance carriers:** underwriters rate a group on its ages, genders, states
  and salaries.
- **PEOs and payroll providers:** they take in a census when onboarding a new client
  company.
- **Retirement plan administrators:** they use census data for eligibility and annual
  compliance testing.
- **M&A and HR due diligence:** acquirers review headcount, tenure and pay across the
  workforce.

### What it contains

- **A single wide table** of 34 rows and 12 columns, with nothing else on the page.
- **Sparse columns:** marital status is filled on 12 rows and term date on none, so
  values can drift into neighbouring cells.
- **Two hire-date columns** that are often the same and differ for rehires.
- **Amounts overprinted at a small offset** to fake bold on every other row, so the text
  layer carries two copies of each.
- **A right-aligned date column** under a wide header.
- **A report header and footer** with the company, filter, run timestamp and page label.
