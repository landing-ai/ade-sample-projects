# Form 10-K

**On the website:** [landing.ai/document-type/form-10-k](https://landing.ai/document-type/form-10-k)

NVIDIA Corporation's annual report on Form 10-K for the fiscal year ended January 25,
2026. It has the SEC cover page, the business description and risk factors, MD&A, the
audited consolidated financial statements and notes, the signatures section, and the
exhibits filed with it, including the Section 302 and 906 certifications.

| | |
|---|---|
| Pages | 93 |
| Fields in the extraction schema | 49 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:00 | 2026-11-19 03:07 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 391,886 | 395,061 |
| Words under 0.95 confidence | 337 | n/a |
| Words under 0.80 confidence | 110 | n/a |
| Words under 0.50 confidence | 8 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 84.0 s | 73.8 s |
| Per page | 0.9 s | 0.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 53.2 credits | 145.3 credits |
| Per page | 0.57 credits | 1.56 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:02 | 2026-11-19 03:08 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 49 | 49 |
| Non-null fields returned | 49 | 49 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 170.4 s | 488.8 s |
| Per schema field (49) | 3.48 s | 9.98 s |
| Per value returned | 2.30 s | 6.61 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 80.9 credits | 81.5 credits |
| Per schema field (49) | 1.651 credits | 1.663 credits |
| Per value returned | 1.093 credits | 1.101 credits |

## Origin

`source/nvidia-form-10-k.pdf` is NVIDIA Corporation's annual report on Form 10-K for the
fiscal year ended January 25, 2026. It is **93 pages, all portrait**. The filing has the
full standard structure: the SEC cover page, Parts I to IV (business, risk factors, MD&A, the audited
consolidated financial statements and notes), the signatures section, and the exhibits
filed with it (insider trading policy, auditor consent, and the Section 302 and 906
certifications).

| | |
|---|---|
| Publisher | NVIDIA Corporation |
| Source | https://d18rn0p25nwr6d.cloudfront.net/CIK-0001045810/e361e58a-7483-44f5-bc62-a9080ae6ec72.pdf |
| Filed | 2026-02-25 (SEC accession 0001045810-26-000021) |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

A 10-K is a mandatory public SEC filing. This copy is the PDF that NVIDIA's investor
relations site serves, an EDGAR Online rendering of the filing. It is committed
unmodified, including its EDGAR Online metadata and an owner-only permissions flag that
needs no password to open.

The filing names the company's executive officers and directors in their official roles.
They appear in the executive officer table on page 11, in the conformed `/s/` signatures
on pages 84–85 and in the CEO and CFO certifications on pages 90–93. The operator
decided to keep these names as published. No private individual's personal data
appears: the only phone number is the corporate main line, and there are no emails, home
addresses or personal identifiers. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Every US public company files a 10-K each year. It is the most complete public record of
a company's business, risks and audited financial results.

- **Equity research and investment management:** analysts pull revenue, margins,
  earnings and segment data into models and compare them year over year.
- **Credit analysis and lending:** credit analysts and rating agencies read the balance
  sheet, cash flows and debt notes.
- **Financial data providers:** they extract the statements and cover-page facts from
  thousands of filings into standardized databases.
- **Audit, compliance and legal:** reviewers check disclosures, risk factors and
  certifications.
- **Corporate development and competitive intelligence:** teams track competitors'
  segments, headcount and strategy.

### What it contains

- **A long document:** 93 pages of dense prose broken up by about 60 financial tables.
- **Multi-year financial statements,** with three fiscal-year columns side by side in
  the income statement.
- **The same figures in several places,** such as cash flow totals in both the MD&A
  summary and the statement itself.
- **A cover page with checkboxes** for filer category, well-known seasoned issuer and
  shell company status.
- **Values stated in prose,** such as headcount, public float and shares outstanding.
- **Conformed `/s/` signatures** and signed certifications in the exhibits.
