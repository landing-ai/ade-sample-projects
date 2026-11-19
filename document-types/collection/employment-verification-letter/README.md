# Employment verification letter

**On the website:** [landing.ai/document-type/employment-verification-letter](https://landing.ai/document-type/employment-verification-letter)

An employment certificate issued by Deloitte Consulting India on April 25, 2022. It
confirms an employee's start date, designation and residential address "as per our
records" on company letterhead, and carries a signatory's handwritten signature with a
time-stamped signing date. The employee's details were replaced with stand-in data.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 16 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:54 | 2026-11-19 02:59 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 1,435 | 1,519 |
| Words under 0.95 confidence | 0 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.7 s | 6.7 s |
| Per page | 4.7 s | 6.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.3 credits | 0.9 credits |
| Per page | 0.30 credits | 0.90 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:54 | 2026-11-19 02:59 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 16 | 16 |
| Non-null fields returned | 15 | 15 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 70.6 s | 235.7 s |
| Per schema field (16) | 4.41 s | 14.73 s |
| Per value returned | 4.71 s | 15.71 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.1 credits | 1.1 credits |
| Per schema field (16) | 0.069 credits | 0.069 credits |
| Per value returned | 0.073 credits | 0.073 credits |

## Origin

`source/employment-verification-letter-redacted.pdf` is an employment certificate issued
by Deloitte Consulting India on April 25, 2022, confirming an employee's start date,
designation and residential address "as per our records", redacted. It is **1 page,
portrait (612×792)**, produced from Adobe LiveCycle, with a full text layer and the
Deloitte logo.

| | |
|---|---|
| Publisher | Deloitte Consulting India Private Limited (employer) |
| Source | [scribd.com/document/571883179/Employment-Letter](https://www.scribd.com/document/571883179/Employment-Letter) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

This is a real certificate, uploaded to Scribd by a third party. Scribd is a user-upload
site, so the uploader is not the publisher, and the letter is treated as a personal
record. Scribd also blocks scripted requests, so the file was downloaded by hand. This
sample replaces an earlier one for the same slug, a small contractor's letter.

Personal data was replaced with a tool that removes the underlying text rather than
covering it:

| What | Replaced with |
|---|---|
| Employee's full name | Johnathon Q Samplewood |
| Employee ID | 00000000 |
| Residential address, first line | Plot no:000, Sample Green Park, |
| Residential address, locality | Anytown, |
| Residential address, city and PIN code | Hyderabad, Telangana, 000000, IN |

The city is kept: the office is in Hyderabad too. The replacement name was chosen to
match the original's width in the same Helvetica Bold, so the justified sentence still
reads without a gap. **The signatory's handwritten signature is kept**, at the document
owner's request, so the page can show signature detection. It is illegible, and the
signatory is not named anywhere on the page; their title and the team mailbox beneath
the signature stay. The company's letterhead, office address, phone, GST and CIN numbers
stay, as do the start date and the designation. The PDF metadata was cleared.

**Verified:** no original identifier is extractable from the committed PDF, and none
appears anywhere in this folder. The original values are deliberately not recorded here
or in `manifest.json`. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An employment verification letter is an employer's written confirmation that a person
works there, in what role and since when. It is asked for whenever someone needs to
prove a job.

- **Mortgage and consumer lending:** lenders confirm employment and tenure before
  approving a loan.
- **Background screening:** screening firms verify employment history for new
  employers.
- **Immigration and visas:** consulates and immigration lawyers ask for letters that
  confirm the applicant's role and start date.
- **Rental applications:** landlords and property managers check that applicants are
  employed.
- **HR and shared services:** employers issue these letters on request, often from a
  central team as in this case.

### What it contains

- **Values inside justified prose,** with the start date and designation in one
  sentence.
- **Company letterhead** with a logo, office address, phone and registration numbers.
- **A multi-line residential address block.**
- **A handwritten signature** that is illegible and has no printed name beneath it.
- **A small time-stamped signing date** under the signature, separate from the letter
  date.
- **A born-digital text layer.**
