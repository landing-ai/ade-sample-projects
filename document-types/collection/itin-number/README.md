# ITIN number

**On the website:** [landing.ai/document-type/itin-number](https://landing.ai/document-type/itin-number)

The IRS's own published sample of Notice CP565, the letter that confirms an Individual
Taxpayer Identification Number. It gives the notice number and date, a case reference,
the recipient's ITIN, name and date of birth, and IRS contact details, with a tear-off
stub that repeats the identifiers. Every value is IRS specimen data.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 14 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:12 | 2026-11-19 03:24 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 4,831 | 4,939 |
| Words under 0.95 confidence | 7 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.6 s | 6.8 s |
| Per page | 2.8 s | 3.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.8 credits | 2.3 credits |
| Per page | 0.40 credits | 1.15 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:13 | 2026-11-19 03:24 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 14 | 14 |
| Non-null fields returned | 14 | 14 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 103.6 s | 269.7 s |
| Per schema field (14) | 7.40 s | 19.27 s |
| Per value returned | 7.40 s | 19.27 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.5 credits | 1.5 credits |
| Per schema field (14) | 0.107 credits | 0.107 credits |
| Per value returned | 0.107 credits | 0.107 credits |

## Origin

`source/irs-cp565-specimen.pdf` is the IRS's own published sample of **Notice CP565**,
which confirms an Individual Taxpayer Identification Number. It is **2 pages, US Letter
portrait (612×792)**, with a full text layer and the IRS eagle logo on both the letter
and the tear-off stub.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [irs.gov/pub/notices/cp565_english.pdf](https://www.irs.gov/pub/notices/cp565_english.pdf) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

The notice is a work of the United States government, so it carries no copyright. It is
served from irs.gov and linked from the CP565 help page. Every value on it is specimen
data the IRS printed for illustration: the recipient is "JOHN SMITH" at "123 N HARRIS
ST, HARVARD, TX 12345", the case reference number is 99999, and **the ITIN itself is
printed as the placeholder `NNN-NN-NNNN`**. No real person's data appears, so no
redaction was needed.

The PDF's metadata named the IRS employee who produced the file. That dictionary and the
XML metadata were cleared before committing. Nothing on the page was altered.

This replaces an earlier sample: a letter presented as a CP565, downloaded from a Scribd
upload. It was probably not a genuine IRS notice, and it was a third party's personal
record, redacted but not consented to. The IRS's own sample replaced it, and the old
file was removed from the folder. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

The IRS issues an ITIN to people who must file US taxes but cannot get a Social Security
number, and the CP565 notice is their proof of the number.

- **Banking:** banks accept an ITIN in place of a Social Security number to open
  accounts, and check the notice as proof of the number.
- **Mortgage and consumer lending:** ITIN lending programs verify the borrower's number
  from the IRS notice.
- **Tax preparation:** preparers and Certifying Acceptance Agents record the number for
  returns and renewals.
- **Payroll and HR:** employers and payers collect ITINs for tax reporting.
- **Immigration and legal aid:** advisers keep the notice as part of a client's tax
  history.

### What it contains

- **A letter that is mostly table:** the header block, the ITIN and personal information
  table and the tear-off stub are all label-value grids.
- **Column headers printed below their values.** In the ITIN table, "First / Middle /
  Last" sits underneath the name it labels.
- **A tear-off stub** that repeats the identifiers and adds blank fields and a.m./p.m.
  checkboxes for the taxpayer to complete.
- **Identifiers that repeat:** the notice number, date and case reference print in the
  header block, on the stub and on the page 2 header.
- **The same name printed twice,** in the ITIN table and in the mailing block, in
  different case.
- **A headline in which the ITIN wraps** across two lines.
