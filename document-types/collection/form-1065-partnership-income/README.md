# Form 1065 - Partnership Income

**On the website:** [landing.ai/document-type/form-1065-partnership-income](https://landing.ai/document-type/form-1065-partnership-income)

Page 1 of the 2023 IRS Form 1065, U.S. Return of Partnership Income, filled with
synthetic data. It identifies the partnership and its business, reports income,
deductions and ordinary business income on 32 numbered lines, and closes with the
signature and paid preparer sections. Its header carries 13 checkboxes in rows G to K.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 75 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:03 | 2026-11-19 03:08 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 7,868 | 8,648 |
| Words under 0.95 confidence | 31 | n/a |
| Words under 0.80 confidence | 13 | n/a |
| Words under 0.50 confidence | 6 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 10.7 s | 11.0 s |
| Per page | 10.7 s | 11.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.0 credits | 2.7 credits |
| Per page | 1.00 credits | 2.70 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:03 | 2026-11-19 03:09 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 75 | 75 |
| Non-null fields returned | 74 | 74 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 141.2 s | 273.4 s |
| Per schema field (75) | 1.88 s | 3.64 s |
| Per value returned | 1.91 s | 3.69 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.8 credits | 4.0 credits |
| Per schema field (75) | 0.051 credits | 0.053 credits |
| Per value returned | 0.051 credits | 0.054 credits |

## Origin

`source/form-1065-2023-ocrolus-sample.pdf` is page 1 of the 2023 IRS Form 1065, U.S.
Return of Partnership Income, filled with synthetic data. It is **1 page, portrait**.

| | |
|---|---|
| Publisher | Ocrolus |
| Source | [Google Drive](https://drive.google.com/file/d/1PHpnyYjTsGCb4puiZJtKtZKu8Gu2ilsw/edit) |
| Linked from | [docs.ocrolus.com/docs/irs-form-1065-2023-us-return-of-partnership-income](https://docs.ocrolus.com/docs/irs-form-1065-2023-us-return-of-partnership-income) |
| Retrieved | 2026-10-02, by script (Drive's standard download link) |
| Clearance | **Public** |

The Drive link alone does not say who made the file. The Ocrolus documentation page for
this form links this exact file as its sample, which establishes the publisher. Ocrolus
sells document AI, so this is a competitor's published sample.

Every value is a placeholder: partnership "Sample Software Service" at "123 Fake
Memorial Ave.", EIN 12-3456789, preparer "John Sample" with PTIN P00001234, phone (800)
123-4567, and round-number line amounts. The signatures are drawn to match those
invented names. The PDF metadata holds only the print driver and Acrobat Distiller.
Nothing needed redacting. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Every US partnership, including most multi-member LLCs, files Form 1065 each year. Page 1
summarizes the business's income and deductions.

- **Commercial and small-business lending:** lenders read business returns to verify
  income and cash flow before approving a loan.
- **Mortgage lending:** underwriters review the partnership returns of self-employed
  borrowers who own a share of a business.
- **Accounting and tax preparation:** CPAs prepare the return and reconcile it with the
  partners' K-1s.
- **Investors and fund administrators:** they review partnership returns when
  evaluating or administering an investment.
- **Tax authorities and auditors:** examiners check reported income and deductions
  against the partnership's books.

### What it contains

- **A dense checkbox header,** with 13 checkboxes in rows G to K.
- **32 numbered amount lines** in a right-hand column.
- **Header boxes** for the partnership's name, address, EIN and business details.
- **Signature blocks** for the partner and the paid preparer, with drawn signatures.
- **A text layer** under the printed form and its filled-in values.
