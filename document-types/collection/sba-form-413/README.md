# SBA Form 413

**On the website:** [landing.ai/document-type/sba-form-413](https://landing.ai/document-type/sba-form-413)

A completed SBA Form 413, the Personal Financial Statement that an SBA loan applicant,
owner or guarantor fills in. It has program checkboxes, the applicant's details, a
balance sheet of assets and liabilities with net worth, income and contingent
liabilities, supporting schedules, a certification block and statutory notices. This
one is unsigned, and only the balance sheet page carries real figures.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 53 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:34 | 2026-11-19 03:51 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 22,653 | 22,754 |
| Words under 0.95 confidence | 59 | n/a |
| Words under 0.80 confidence | 33 | n/a |
| Words under 0.50 confidence | 20 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.1 s | 12.9 s |
| Per page | 1.5 s | 2.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.2 credits | 8.7 credits |
| Per page | 0.53 credits | 1.45 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:34 | 2026-11-19 03:52 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 53 | 53 |
| Non-null fields returned | 51 | 51 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 103.3 s | 101.7 s |
| Per schema field (53) | 1.95 s | 1.92 s |
| Per value returned | 2.03 s | 1.99 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.2 credits | 6.2 credits |
| Per schema field (53) | 0.117 credits | 0.117 credits |
| Per value returned | 0.122 credits | 0.122 credits |

## Origin

`source/sba-form-413.pdf` is a completed **SBA Form 413, Personal Financial Statement**
(05-21 edition). This is the form an SBA loan applicant, owner or guarantor fills in for
a 7(a), 504, disaster or surety bond application, or for the WOSB or 8(a) programs. It
is **6 pages, portrait**, a fillable form whose values are stored in form fields:

- Page 1: program checkboxes and instructions
- Page 2: applicant details, the assets and liabilities balance sheet, income and
  contingent liabilities
- Page 3: supporting schedules (notes payable, stocks, real estate, other property)
- Page 4: more schedules and the certification
- Pages 5–6: statutory notices

| | |
|---|---|
| Publisher | U.S. Small Business Administration (the form). It was completed by an unidentified filer |
| Source | scribd.com/document/567494949/completed-sba-form-413 (shown as plain text, not linked) |
| Retrieved | 2026-10-03, downloaded manually by the operator (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

Scribd is a user-upload site, not a publisher, so this was treated as a personal record.
Some of the values look illustrative rather than real, but the business name and address
could belong to a real business, so every identifying field was replaced before the
document was parsed.

The values lived only in the form's fillable fields, not in the page text, so each
field's stored value and its appearance were replaced. The PDF metadata was then
cleared.

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Applicant's name | 2 | `Jane Q Sample` |
| Business name | 1 | `Sample Bookstore` |
| Home street address | 1 | `100 Main St.` |
| Home city, state and ZIP | 1 | `Anytown, SD 57000` |
| Business address | 1 | `200 MAIN ST, Anytown, SD 57000` |
| Business and home phones | 2 | reserved `555-01xx` numbers |
| Social security number | 1 | `987-65-4324` (reserved range) |
| PDF metadata (`/Info`, XMP) | — | removed |

The page text, the form fields, every decompressed PDF object and the raw file bytes
were searched, and none contains an original value. No original value appears anywhere
in this folder, checked as literal text and as runs of digits. The rules file that maps
originals to replacements is kept outside the repo.

There was nothing else to replace. Both signature fields are empty, so the form is
unsigned. There is no spouse, no account or loan number, and no real estate (Section 4
reads N/A). Dollar amounts, checkboxes and dates were left unchanged.

A previous Scribd candidate for this type was an altered document, so this one was
checked before use, and nothing suggests editing. The asset lines sum to total assets,
and total liabilities plus net worth equals total assets. The as-of date matches the
signature-block date, and both fall within the form's OMB expiry date. The file is the
SBA's own Word-to-Acrobat form, saved once, with every value in a form field whose
appearance matches its stored value. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

SBA lenders collect Form 413 from every owner and guarantor of a business applying for
most SBA loans, and the SBA uses it in several contracting programs.

- **SBA and small-business lending:** lenders read each guarantor's assets, liabilities
  and net worth to judge the strength of a personal guarantee.
- **Community banks and credit unions:** the same personal financial statement is often
  used for conventional business loans.
- **Disaster loan processing:** applicants for SBA disaster loans file it with their
  application.
- **SBA contracting programs:** WOSB and 8(a) applicants use it to show they meet the
  economic disadvantage limits.
- **Surety bonding:** surety companies review contractors' personal finances before
  issuing bonds under the SBA program.

### What it contains

- **Values stored in fillable form fields,** not in the page text.
- **A balance sheet in two columns** with dotted leaders between labels and amounts.
- **Checkbox groups** for the loan program and the business type.
- **Supporting schedules that are mostly blank,** so many cells must come back empty.
- **Printed "SIGN" flag tabs** beside empty signature fields on an unsigned form.
- **Two pages of statutory notices** in dense prose.
