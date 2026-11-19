# Certified Payroll Report

**On the website:** [landing.ai/document-type/certified-payroll-report](https://landing.ai/document-type/certified-payroll-report)

A filled specimen of Oregon's form WH-38, Payroll/Certified Statement, the certified
payroll a contractor on a public works project files each pay period. The first page is
the payroll grid, with daily hours, rates, fringe benefits, gross pay, deductions and net
pay for four workers. The second is the signed statement that certifies it.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 51 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:38 | 2026-11-19 02:39 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 10,682 | 11,343 |
| Words under 0.95 confidence | 42 | n/a |
| Words under 0.80 confidence | 12 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.3 s | 12.8 s |
| Per page | 2.6 s | 6.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.4 credits | 3.9 credits |
| Per page | 0.70 credits | 1.95 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:39 | 2026-11-19 02:40 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 51 | 51 |
| Non-null fields returned | 48 | 48 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 215.8 s | 248.6 s |
| Per schema field (51) | 4.23 s | 4.87 s |
| Per value returned | 1.93 s | 2.20 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.4 credits | 6.5 credits |
| Per schema field (51) | 0.125 credits | 0.127 credits |
| Per value returned | 0.057 credits | 0.058 credits |

## Origin

`source/boli-wh-38-certified-payroll-sample.pdf` is a filled specimen of Oregon's form
WH-38, *Payroll/Certified Statement*. A contractor on a public works project files this
certified payroll with the public agency each pay period under Oregon's prevailing wage
law (ORS 279C.845), and the form is also designed to meet the federal Davis-Bacon Act.
It is **2 pages, landscape**, with a text layer.

| Page | Content |
|---|---|
| 1 | The WH-38 payroll grid: contractor and project header, prime and subcontractor sections, and four worker blocks with daily OT/ST hours, rates, fringe benefits, gross, deductions and net |
| 2 | The certified statement on the reverse: signatory, contractor, project and period, deductions, and the Davis-Bacon fringe benefit section |

| | |
|---|---|
| Publisher | Oregon Bureau of Labor and Industries (BOLI), Prevailing Wage Rate unit |
| Source | [oregonlegislature.gov handout, 2019-10-23 PWR work group](https://www.oregonlegislature.gov/committees/slb/WorkgroupDocuments/Susan%20Wooley,%20BOLI%20(handout)%20-%2010-23-19%20meeting.pdf) |
| Retrieved | 2026-10-14, downloaded by script |
| Clearance | **Redacted** |

BOLI's Prevailing Wage Rate unit handed this sample to the Oregon Legislature's Senate
Labor and Business committee PWR work group on October 23, 2019, and the handout is
posted on oregonlegislature.gov. The same filled sample appears on slides 9 and 10 of
BOLI's 2024 certified payroll training deck. The handout has 6 pages. Pages 1 to 4 are
presentation slides and were dropped, and pages 5 and 6 are kept. The certified
statement was printed upside down in the handout. It was turned upright, and both pages
had their page rotation folded into the content, so the text runs left to right on an
unrotated page. Nothing else on either page was moved.

The workers are specimen joke names with no ID numbers, and the contractor is fictional.
The specimen does borrow the presenter's own name for the contractor's owner, signatory
and business name, carries two real-looking phone numbers, and gives the workers
plausible Portland street addresses, one of them a state office building. These were
replaced before anything was parsed:

| What | Replaced with | Count |
|---|---|---|
| Presenter's name, as the contractor owner and signatory (page 2) | `Jane Sample` | 2 |
| Contractor business name, which carried the presenter's surname (pages 1 and 2) | `Sample Construction` / `SAMPLE CONSTRUCTION` | 3 |
| Contractor phone, in a BOLI telephone exchange | `(971) 555-0136` | 1 |
| Public agency phone, of unknown origin | `(503) 555-0127` | 1 |
| Contractor street address and PO box number (city, state and ZIP kept) | `500 Pine St`, `PO Box 3569` | 2 |
| Four worker street addresses (city, state and ZIP kept) | `100 Main St`, `200 Oak St`, `300 Elm St`, `400 Ash St.` | 4 |

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. Worker names, the specimen CCB registration number, the public agency, the
project name, number and location, every date and every amount were left as published.
The public agency and project are a real public project.

The replacement used `document-types/scripts/redact.py`, which removes the underlying
text rather than covering it. Each page was redacted separately with its own rules, after
its rotation was folded into the content, and the two pages were then joined. The output
was checked by the script's own re-extraction, by eye on renders of both pages, and by a
sweep of every file in this folder. The PDF's metadata is empty. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Contractors on prevailing-wage public works jobs file a certified payroll every week or
pay period. It is the record that each worker was paid at least the required rate for
their trade.

- **Public agencies and owners:** state, county and city agencies collect and review
  certified payrolls on every public works contract they fund.
- **Labor regulators:** state labor departments and the federal Department of Labor
  audit them for prevailing wage and Davis-Bacon compliance.
- **General contractors:** they collect payrolls from every subcontractor and are liable
  for their compliance.
- **Construction compliance and payroll software providers:** they prepare, file and
  check certified payrolls for contractors.
- **Unions and fringe benefit trusts:** they check reported hours and contributions
  against what was paid into the plans.

### What it contains

- **A dense ruled grid with stacked rows.** Each worker is a five-row block: an OT row
  and an ST row of daily hours, rates and totals, then a schedule line, all sharing the
  worker's name, classification, gross, deductions and net cells.
- **Diagonally split cells.** Column (7) holds two values in one cell, divided by a
  diagonal rule: gross on this project in the upper left, gross for all work in the
  lower right.
- **A sub-table beside each block.** Columns (10) and (11) list each worker's fringe
  benefit plans, one per row, with a different count per worker.
- **Landscape pages** with small print and many numbered columns.
- **A two-part document.** The payroll and the certified statement on its reverse must
  agree on contractor, project and period.
- **A signature block and checkboxes** on the certified statement.
