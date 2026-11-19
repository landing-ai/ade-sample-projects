# Trust Income Document

**On the website:** [landing.ai/document-type/trust-income-document](https://landing.ai/document-type/trust-income-document)

A 2025 IRS Schedule K-1 (Form 1041), Beneficiary's Share of Income, Deductions,
Credits, etc., filled with IRS test data. It is the statement a trust or estate issues
to each beneficiary to report the income passed through to them. It identifies the
trust and the beneficiary and gives the beneficiary's share of each income line, with
coded boxes for deductions, credits and other information.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 38 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:40 | 2026-11-19 03:56 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,978 | 3,176 |
| Words under 0.95 confidence | 66 | n/a |
| Words under 0.80 confidence | 56 | n/a |
| Words under 0.50 confidence | 43 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.5 s | 6.9 s |
| Per page | 7.5 s | 6.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.3 credits |
| Per page | 0.50 credits | 1.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:40 | 2026-11-19 03:56 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 38 | 38 |
| Non-null fields returned | 13 | 17 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 180.7 s | 107.5 s |
| Per schema field (38) | 4.75 s | 2.83 s |
| Per value returned | 13.90 s | 6.32 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.6 credits | 1.7 credits |
| Per schema field (38) | 0.042 credits | 0.045 credits |
| Per value returned | 0.123 credits | 0.100 credits |

## Origin

`source/trust-income-k1-2025-irs-ats-1041-scenario-3.pdf` is the 2025 IRS Schedule K-1
(Form 1041), Beneficiary's Share of Income, Deductions, Credits, etc., filled with IRS
test data. This is the statement a trust or estate issues to each beneficiary to report
the income passed through to them. It is **1 page, portrait**.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [form-1041-ty2025-ats-scenario-3.pdf](https://www.irs.gov/pub/irs-efile/form-1041-ty2025-ats-scenario-3.pdf) |
| Linked from | IRS Tax Year 2025 Form 1041 MeF ATS page |
| Retrieved | 2026-10-03, by script |
| Clearance | Redacted (US government work, public domain; one identifier replaced as a precaution) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Scenario 3 for
tax year 2025 Form 1041, which software vendors use to test their e-file output. The
original PDF is 19 pages: the full trust return with Schedules D and I, Forms 3800,
4797, 8864 and 8960, and the beneficiaries' K-1s. This folder keeps **page 10 only**,
the first beneficiary's Schedule K-1.

Every value is IRS test data: a fictitious trust, Cyan Magenta Trust of Lanham MD, with
an EIN in the `00-` test range, and a test beneficiary. The beneficiary's identifying
number (item F) is an ATS test value, but it falls outside the standard specimen SSN
ranges, so as a precaution it was replaced with **987-65-4322**, from the reserved
987-65-4320 to 4329 range. The replacement removed the underlying text rather than
covering it. The original number is not recorded anywhere in this folder. The document
metadata was cleared. Verified: the original is not extractable from the committed PDF,
in hyphenated or digits-only form, and the folder sweep finds it nowhere.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A Schedule K-1 (Form 1041) is how a trust or estate reports to each beneficiary the
income it passed through. It is the main proof of trust income.

- **Mortgage and consumer lending:** underwriters verify trust distributions as income
  when a borrower lives partly on a trust.
- **Tax preparation:** preparers carry each K-1 amount onto the beneficiary's
  individual return.
- **Trust and estate administration:** fiduciaries and trust companies issue K-1s to
  every beneficiary each year.
- **Wealth management:** advisers track trust income across a client's accounts.
- **Tax software vendors:** they test e-file output against IRS scenarios such as this
  one.

### What it contains

- **A two-column form layout,** with the trust and beneficiary down the left (Parts I and
  II) and the beneficiary's share of each income line down the right (Part III).
- **Code-letter boxes** (11 to 14) that pair a code with an amount.
- **Mostly blank boxes.** Only two income lines, one credit and one item of other
  information are filled, so blank has to be told apart from zero.
- **Checkboxes** at the top of the K-1, such as Final K-1.
- **Ruled form cells** where a label and its value share one box.
