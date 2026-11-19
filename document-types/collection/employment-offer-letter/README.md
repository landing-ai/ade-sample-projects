# Employment offer letter

**On the website:** [landing.ai/document-type/employment-offer-letter](https://landing.ai/document-type/employment-offer-letter)

An offer letter from Aerial Telecom Solutions Pvt. Ltd., an Indian telecom services
company, for a Technical Manager post, dated 20-Mar-2025. It states the designation,
place of posting, joining date, annual cost to company, probation, notice period and
retirement age, and closes with an annexure that breaks the salary into monthly and
annual earnings, deductions and employer contributions.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 19 |

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
| Characters returned | 10,973 | 11,162 |
| Words under 0.95 confidence | 49 | n/a |
| Words under 0.80 confidence | 25 | n/a |
| Words under 0.50 confidence | 6 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.9 s | 10.8 s |
| Per page | 1.4 s | 2.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.9 credits | 5.3 credits |
| Per page | 0.38 credits | 1.06 credits |

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
| Fields requested | 19 | 19 |
| Non-null fields returned | 19 | 19 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 363.9 s | 58.9 s |
| Per schema field (19) | 19.15 s | 3.10 s |
| Per value returned | 4.85 s | 0.79 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 4.0 credits | 3.9 credits |
| Per schema field (19) | 0.211 credits | 0.205 credits |
| Per value returned | 0.053 credits | 0.052 credits |

## Origin

`source/employment-offer-letter-redacted.pdf` is an offer letter from Aerial Telecom
Solutions Pvt. Ltd., an Indian telecom services company, for a Technical Manager post,
dated 20-Mar-2025, redacted. It is **5 pages, portrait (612×792)**, exported from Word,
with a full text layer, a logo, a watermark and a branded footer on every page. Pages 1
to 4 are the letter and its terms; page 5 is Annexure I, the salary breakdown table.

| | |
|---|---|
| Publisher | Aerial Telecom Solutions Pvt. Ltd. (employer) |
| Source | [scribd.com/document/850511200](https://www.scribd.com/document/850511200) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

This is a real letter, uploaded to Scribd by a third party. Scribd is a user-upload
site, so the uploader is not the publisher, and the letter is treated as a personal
record. Scribd also blocks scripted requests, so the file was downloaded by hand. **The
source URL is recorded in its id-only form**: Scribd's full URL adds a title slug, and
this one was the candidate's full name.

Personal data was removed using `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it:

| What | Replaced with | Occurrences |
|---|---|---|
| Candidate's full name | Jonny Doe | 2 (page 1, annexure) |
| First name in the salutation | Dear Jonny | 1 |
| Care-of line with a relative's name and house number | C/O Sample Relative, H.No-000, Example Colony, | 1 |
| Locality, city and PIN code | Sample Nagar, Jalandhar, Punjab-000000 | 1 |

The city is kept: Jalandhar is also the place of posting in the body of the letter.

**The signature was an image.** The authorized signatory's handwritten signature on page
4 was deleted. It sat over a corner of the full-page watermark, so only images lying
entirely inside the signature area were removed, and the watermark was left intact.

The PDF metadata was also cleared; its `author` field named a person. The company's
name, logo, address, phone number, website and CIN are business details, and the terms
and salary figures are left as printed. The replacements are set in Helvetica Bold, so
they are visibly a different typeface from the Calibri around them.

No original identifier is extractable from the committed PDF, no image remains in the
signature area, and no original identifier appears anywhere in this folder. The original
values are deliberately not recorded here or in `manifest.json`, and the rules file
stays outside the repo. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An offer letter sets out the job, pay and terms an employer offers a candidate. Once
signed, it becomes the reference for the employment terms and is often used as proof of
income and employment.

- **HR and recruiting:** teams generate offers and load the accepted terms into HR and
  payroll systems.
- **Background verification and onboarding:** verification firms and new employers check
  designation, joining date and compensation against the letter.
- **Banks and lenders:** in India, lenders accept an offer letter with the salary
  annexure as income proof for personal loans and home loans.
- **Immigration and visa processing:** employers and applicants submit offer letters to
  show the role and salary.
- **Payroll and compliance:** payroll teams map the salary structure to statutory
  deductions such as EPF, ESIC and professional tax.

### What it contains

- **Terms in sentences.** The designation, posting, joining date and pay are each stated
  in a sentence ("Your Date of Joining will be 07-Apr-2025."), not in labeled fields.
- **Rupee amounts in figures and in words,** such as "Rs. 565008/- (Rupees Five Lakh
  Sixty Five Thousand Eight Only/-)", and numbers written only as words ("Six months").
- **An Indian salary structure** with HRA, EPF, ESIC, LWF and professional tax.
- **A salary table with repeated line names.** The annexure lists EPF, ESIC and LWF
  twice, once under the employee's deductions and once under the employer's
  contributions.
- **A logo, a full-page watermark and a branded footer** on every page.
- **Replaced text in a different typeface** and a removed signature on page 4.
