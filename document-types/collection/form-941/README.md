# Form 941

**On the website:** [landing.ai/document-type/form-941](https://landing.ai/document-type/form-941)

IRS Form 941, the Employer's Quarterly Federal Tax Return, for the first quarter of
2023, filled with specimen data. It reports the wages an employer paid in the quarter,
the federal income, social security and Medicare tax due on them, the deposits made,
and the balance owed.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 69 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:05 | 2026-11-19 03:12 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 9,395 | 10,177 |
| Words under 0.95 confidence | 63 | n/a |
| Words under 0.80 confidence | 32 | n/a |
| Words under 0.50 confidence | 10 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.8 s | 20.3 s |
| Per page | 2.6 s | 6.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.4 credits | 4.1 credits |
| Per page | 0.47 credits | 1.37 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:05 | 2026-11-19 03:12 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 69 | 69 |
| Non-null fields returned | 60 | 61 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 403.0 s | 151.2 s |
| Per schema field (69) | 5.84 s | 2.19 s |
| Per value returned | 6.72 s | 2.48 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 4.2 credits | 4.3 credits |
| Per schema field (69) | 0.061 credits | 0.062 credits |
| Per value returned | 0.070 credits | 0.070 credits |

## Origin

`source/form-941-2023-ocrolus-sample.pdf` is IRS Form 941 for 2023 (Rev. March 2023),
filled with specimen data for the first quarter. It is **3 pages, portrait**.

| | |
|---|---|
| Publisher | Ocrolus (document-AI vendor sample) |
| Source | [drive.google.com/file/d/1gD_JCWFhLjuJKIoE_EDzTqv4IbcGZ1_M](https://drive.google.com/file/d/1gD_JCWFhLjuJKIoE_EDzTqv4IbcGZ1_M/view?usp=sharing) |
| Linked from | [docs.ocrolus.com: 941 Employer's Quarterly Federal Tax Return](https://docs.ocrolus.com/docs/941-employers-quarterly-federal-tax-return) |
| Retrieved | 2026-10-28 |
| Clearance | Public: vendor-published specimen |

Ocrolus publishes this sample in its public developer documentation for Form 941,
alongside its own extraction of it. Google Drive is only the host. The file was downloaded
by script from Drive's direct-download URL and checked to be a 3-page PDF, not Drive's
HTML viewer page.

Every value is specimen data: `SAMPLE NAME`, `SAMPLE TRADE LLC`, `123 ANY STREET`,
`FAKE CITY`, EIN `12-3456789`, designee `JOHN SAMPLE`, preparer `SAMPLE SMITH` of
`SAMPLE FIRM LLC`, placeholder phone numbers and PTIN, and script-font "Sample Name" and
"Sample Smith" signatures. No real person or business appears, so nothing was redacted.
The PDF metadata was reset to a title naming the sample and Ocrolus as author, and the XMP
packet was removed. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Every US employer that withholds tax from wages files Form 941 each quarter, so it is
one of the most common records of a business's payroll.

- **Commercial and small-business lending:** lenders read recent 941s to confirm payroll
  and headcount before approving a loan, and SBA lenders ask for them by default.
- **Tax credits and recovery claims:** amended 941s carry claims such as the Employee
  Retention Credit, and reviewers check them line by line.
- **Accounting and tax preparation:** CPAs reconcile each quarter's 941 against the W-2s
  and the payroll register at year end.
- **Payroll providers and PEOs:** they file 941s for their clients and reconcile them
  against deposits.
- **Insurance and audit:** workers' compensation premium audits and financial auditors
  use it to verify reported wages.

### What it contains

- **Single-digit boxes for the EIN**, one digit per box.
- **A checkbox panel** for the quarter being reported.
- **A two-column computation** on lines 5a to 5d: each wage line is multiplied by a tax
  rate printed on the form, with the result in a second column.
- **Line-numbered amounts** split into dollars and cents, from line 1 to line 15.
- **Deposit schedule checkboxes** and a third-party designee section.
- **Signature blocks** for the employer and the paid preparer.
- **A hard text layer.** Pages 1 and 2 use a garbled font encoding, and page 3 is
  mostly vector art and images, so the text has to be read from the page image.
