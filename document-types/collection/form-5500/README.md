# Form 5500

**On the website:** [landing.ai/document-type/form-5500](https://landing.ai/document-type/form-5500)

The Form 5500 Annual Return/Report of Employee Benefit Plan for the St. Olaf College
403(b) Retirement Plan, plan year 2023, with its attached schedules. The main form
identifies the plan and sponsor and reports participant counts and plan
characteristics. Schedules A, C, D, H and R add the insurance contract, service
providers, investment entities, financial statements and retirement plan details.

| | |
|---|---|
| Pages | 24 |
| Fields in the extraction schema | 79 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:03 | 2026-11-19 03:10 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 80,792 | 80,831 |
| Words under 0.95 confidence | 397 | n/a |
| Words under 0.80 confidence | 159 | n/a |
| Words under 0.50 confidence | 30 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 48.6 s | 23.5 s |
| Per page | 2.0 s | 1.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 11.7 credits | 32.3 credits |
| Per page | 0.49 credits | 1.35 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:04 | 2026-11-19 03:10 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 79 | 79 |
| Non-null fields returned | 79 | 79 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 309.2 s | 408.5 s |
| Per schema field (79) | 3.91 s | 5.17 s |
| Per value returned | 2.76 s | 3.61 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 19.4 credits | 19.5 credits |
| Per schema field (79) | 0.246 credits | 0.247 credits |
| Per value returned | 0.173 credits | 0.173 credits |

## Origin

`source/form-5500-st-olaf-403b-2023-redacted.pdf` is the Form 5500 Annual Return/Report
of Employee Benefit Plan for the St. Olaf College 403(b) Retirement Plan, plan year
2023, with its attached schedules. It is **24 pages, portrait**. Every filled-in value is
drawn as vector glyph outlines, not text (the producer was Microsoft Print To PDF).

| Pages | Content |
|---|---|
| 1–3 | Form 5500: plan and sponsor identification, signatures, participant counts, plan characteristics, attached schedules |
| 4–7 | Schedule A, Insurance Information (TIAA-CREF contract) |
| 8–13 | Schedule C, Service Provider Information |
| 14–16 | Schedule D, DFE/Participating Plan Information |
| 17–21 | Schedule H, Financial Information |
| 22–24 | Schedule R, Retirement Plan Information |

| | |
|---|---|
| Publisher | St. Olaf College (the plan sponsor) |
| Source | [2023-403b-5500-Website.pdf](https://wp.stolaf.edu/finance/files/2024/10/2023-403b-5500-Website.pdf), on the college's finance site; no linking page was found |
| Retrieved | 2026-10-28, by script |
| Clearance | Redacted: a public ERISA filing, with the one individual's name replaced |

Form 5500 filings are open to public inspection under ERISA, and the college posts this
one itself. The filing names one individual: the person who signed it, printed twice on
page 1, as plan administrator and as plan sponsor. That name was replaced with
**JANE Q. SAMPLE** in both places; the electronic-signature notice and the signature
dates beside it were kept. The college's own name, EIN, address and telephone, and the
organizations in the schedules (an insurance carrier, an investment consultant and an
audit firm), are institutional and were kept. Schedules A and C name no individual
broker or agent. The PDF's metadata, which named a person as author, was cleared.

**How the redaction was done.** Each line of values is one compound vector path: the
e-signature notice, the date and the name are a single path. The name was found by OCR,
just its glyph subpaths were cut out of the page content stream, and the replacement was
drawn in Helvetica. Verified by OCR, and by text and content-stream search: the original
name survives nowhere in the committed PDF or in this folder.

**A hidden text layer.** Under every field sits invisible white text holding EFAST
placeholder strings (`ABCDEFGHI`, `123456789`, `YYYY-MM-DD`) rather than the values. It
carries no personal data and was left in place.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Most US employee benefit plans file a Form 5500 every year, and the filings are public.
They are the main record of a plan's size, costs, service providers and finances.

- **Plan sponsors and administrators:** they prepare and file the return each year and
  reconcile it against the plan audit.
- **Retirement plan advisers and recordkeepers:** they mine 5500 data to benchmark fees
  and prospect for plans.
- **Auditors:** plan auditors tie Schedule H to the audited financial statements.
- **Regulators:** the Department of Labor, IRS and PBGC review filings for compliance.
- **Benefits researchers and journalists:** they compare plans on participation,
  assets and fees.

### What it contains

- **A main form plus five schedules,** each with its own header and line numbering.
- **No usable text layer for the values.** The filled-in values are vector outlines, and
  a hidden layer underneath holds placeholder strings, not the values.
- **Participant headcounts and plan-characteristic codes** on numbered lines.
- **Checkbox grids** for attached schedules, funding and benefit arrangements.
- **A repeating service-provider block** in Schedule C, with several service codes packed
  into one narrow cell.
- **A two-column balance sheet and income statement** in Schedule H.
- **Electronic-signature notices** in the signature rows.
