# Attending Physician Statement

**On the website:** [landing.ai/document-type/attending-physician-statement](https://landing.ai/document-type/attending-physician-statement)

Part B of California EDD form DE 2501, the Physician or Practitioner's Certificate
for a State Disability Insurance claim, filled with specimen data. The treating
physician certifies the patient's treatment period, when the disability began, the ICD
diagnosis codes, findings and treatment, prior treatment and surgery, and whether the
condition is work-related.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 35 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:27 | 2026-11-19 02:27 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 9,271 | 16,742 |
| Words under 0.95 confidence | 187 | n/a |
| Words under 0.80 confidence | 140 | n/a |
| Words under 0.50 confidence | 95 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.9 s | 21.4 s |
| Per page | 3.3 s | 7.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.4 credits | 5.7 credits |
| Per page | 0.47 credits | 1.90 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:27 | 2026-11-19 02:27 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 35 | 35 |
| Non-null fields returned | 25 | 28 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 147.0 s | 160.4 s |
| Per schema field (35) | 4.20 s | 4.58 s |
| Per value returned | 5.88 s | 5.73 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.0 credits | 4.5 credits |
| Per schema field (35) | 0.086 credits | 0.129 credits |
| Per value returned | 0.120 credits | 0.161 credits |

## Origin

`source/de2501-physician-certificate-sample.pdf` is Part B, the Physician or
Practitioner's Certificate, of California EDD form DE 2501, Application for Disability
Insurance Benefits (Rev. 82, 10-24). The EDD fills it with specimen data. It is
**3 pages, portrait**, with a text layer:

- Page 1 (printed page 11): patient, the practitioner and their license, the treatment
  period, and when the disability began
- Page 2 (printed page 12): ICD diagnosis codes, diagnosis, findings and treatment
- Page 3 (printed page 13): prior treatment, surgery, work-relatedness, and the signed
  certification

**This is a state disability-insurance physician certificate, not an insurance
carrier's Attending Physician Statement (APS).** California's State Disability
Insurance program requires one from the treating physician for every claim. A carrier
APS for a life, disability or long-term-care policy asks for the same core information:
who treated the patient, since when, the diagnosis and ICD codes, the treatment, and when
the patient is expected back at work. Publishers rarely release a filled-in carrier APS,
and this is the closest public specimen.

| | |
|---|---|
| Publisher | State of California Employment Development Department (EDD), State Disability Insurance program |
| Source | https://edd.ca.gov/siteassets/files/pdf_pub_ctr/de2501.pdf |
| Retrieved | 2026-10-04, downloaded by script |
| Clearance | Public |

The EDD's Forms and Publications page links this file as "DE 2501 - Sample claim
form", and the same filled pages appear in its paper-claim tutorial. Every page carries a
red "SAMPLE, this page for reference only" banner. The patient is "Sample Claimant", the
SSN is all zeros, and the physician's address is in "Anywhere, CA", so there is no
personal data and nothing was redacted.

The original has 13 pages. Pages 1-10 are instructions, the claimant's authorization
and Part A (the claimant's own statement), so only pages 11-13 were kept. The PDF
metadata was cleared. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A physician's statement is the medical evidence behind a disability, life or long-term
care claim. Insurers and benefit programs ask the treating doctor for the same core
facts: diagnosis, treatment, and how long the patient cannot work.

- **State disability insurance programs:** California's SDI requires this certificate
  from the treating physician for every claim.
- **Disability and long-term-care insurers:** claims examiners use an APS to approve
  benefits and set the expected return-to-work date.
- **Life insurance underwriting:** underwriters order an APS to review an applicant's
  medical history.
- **Employers and leave administrators:** they use physician certifications to manage
  leave and return to work.
- **Workers' compensation:** the work-relatedness answers decide which program pays.

### What it contains

- **Comb boxes.** Almost every value is printed one character per box, and dates are
  eight digits with no separators (`01252025`).
- **A red form.** White entry boxes sit on a red ground, and every page carries a red
  SAMPLE banner.
- **Checkbox groups** for treatment interval and yes/no questions, some left unanswered.
- **ICD-10 diagnosis codes** in their own boxes, one of them misprinted by the publisher
  with the digit 5 in place of the letter S.
- **Free-text diagnosis, findings and treatment** written across rows of character
  boxes.
- **A signed certification** on the last page.
