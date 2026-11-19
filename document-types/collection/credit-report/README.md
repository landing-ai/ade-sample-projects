# Credit report

**On the website:** [landing.ai/document-type/credit-report](https://landing.ai/document-type/credit-report)

A consumer credit report built on TransUnion data, with a VantageScore 3.0 of 766 and
a report date of January 30, 2022. It shows the score, the consumer's personal
information, an account summary, eleven credit card and charge accounts with 24-month
payment grids, a hard inquiry, a collection account, public records and a creditor
directory. Every identifying detail was replaced with stand-in data.

| | |
|---|---|
| Pages | 8 |
| Fields in the extraction schema | 46 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:45 | 2026-11-19 02:50 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 36,686 | 35,113 |
| Words under 0.95 confidence | 102 | n/a |
| Words under 0.80 confidence | 45 | n/a |
| Words under 0.50 confidence | 17 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 54.6 s | 58.5 s |
| Per page | 6.8 s | 7.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.9 credits | 12.8 credits |
| Per page | 0.61 credits | 1.60 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:46 | 2026-11-19 02:52 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 46 | 46 |
| Non-null fields returned | 43 | 46 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 266.2 s | 392.2 s |
| Per schema field (46) | 5.79 s | 8.53 s |
| Per value returned | 1.36 s | 1.97 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 12.9 credits | 12.5 credits |
| Per schema field (46) | 0.280 credits | 0.272 credits |
| Per value returned | 0.066 credits | 0.063 credits |

## Origin

`source/credit-report-redacted.pdf` is a consumer credit report built on TransUnion data,
with a VantageScore 3.0 of 766, report date January 30, 2022. It is **8 pages, portrait
(A4)**, rendered from a web page to PDF: a score gauge, personal information, an account
summary, eleven credit card and charge accounts with 24-month payment grids, a hard
inquiry, a collection account, public records and a creditor directory.

| | |
|---|---|
| Publisher | Unknown (a TransUnion-based report, saved from a web page) |
| Source | [scribd.com/document/978216898](https://www.scribd.com/document/978216898) |
| Retrieved | 2026-09-28, downloaded manually |
| Clearance | Redacted |

**Provenance is poor, and every identifying detail was replaced.** This is a real
individual's full credit report, uploaded to Scribd by a third party under a title
giving the person's name and a sequence number. A numbered upload of a named person's
report, complete with SSN, date of birth and fifteen years of addresses, is the pattern
of a leaked or fraud-traded identity record, not a document its subject chose to
publish. It was flagged as unusable; the document owner decided to use it on the
condition that nothing identifying survives.

The replacements were made with a tool that removes the underlying text rather than
covering it:

| What | With |
|---|---|
| Consumer's name | Jane Q Sample |
| Social Security number | 987-65-4323, from the reserved 987-65-4320–4329 range |
| Date of birth | 1957-01-16 |
| Employer and job title | Clerk (employer removed) |
| Six reported addresses | 100 Main St to 600 Maple Dr, Anytown, ZIP 000000000; states kept |
| Twelve account numbers | Plausible random stand-ins of the same length |

Kept as printed: the score, every balance, limit and payment, creditor names, dates,
payment histories, remarks, and the creditors' and collection agency's business
addresses and phone numbers. None of it identifies anyone once the identity is gone. The
PDF metadata was cleared (the original carried Chromium/Skia producer data). Verified:
no original value is extractable from the committed PDF, no other line of text changed,
and no original value, including as bare digits, appears in any file in this folder.

The URL is recorded without the listing's title slug, which contains the person's name.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A credit report is the record of a consumer's borrowing and repayment, and it sits
behind most consumer lending decisions in the US.

- **Mortgage lending:** underwriters read the score, tradelines, inquiries and
  collections to qualify a borrower and set the rate.
- **Auto, card and personal lending:** lenders use the report to approve credit and set
  limits.
- **Tenant screening and property management:** landlords review credit history before
  approving a lease.
- **Credit counseling and debt settlement:** counselors build repayment plans from the
  open accounts, balances and collections.
- **Consumers and their advocates:** they review reports for errors and file disputes
  with the bureau.

### What it contains

- **A dashboard printed to paper,** with big-number tiles for the account summary and
  the score drawn as a gauge chart.
- **The same figures twice,** in large tiles and again in a detail table beneath.
- **Many repeated records:** eleven tradelines with the same fifteen fields each, spread
  across six pages.
- **Colour-coded 24-month payment grids** on each account card.
- **Sections in different layouts** for the collection account, inquiries, public
  records and the creditor directory.
- **A web page rendered to PDF,** with a text layer.
