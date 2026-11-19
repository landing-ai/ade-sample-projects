# Medical Imaging Report

**On the website:** [landing.ai/document-type/medical-imaging-report](https://landing.ai/document-type/medical-imaging-report)

A real radiology report as it arrives at a provider's office: by fax. It is a shoulder
MRI read for an orthopedic practice and faxed to a physical therapy clinic in March
2019. Page 1 is the practice's fax cover sheet, and page 2 is the report, with the
study details, history, comparison, technique, findings, impression and signature lines.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 22 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:37 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 4,825 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 19.5 s |
| Per page | 9.7 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 2.3 credits |
| Per page | 1.15 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:37 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 22 |
| Non-null fields returned | 25 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 109.8 s |
| Per schema field (22) | 4.99 s |
| Per value returned | 4.39 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 3.4 credits |
| Per schema field (22) | 0.155 credits |
| Per value returned | 0.136 credits |

## Origin

`source/mri-report-fax.pdf` is a shoulder MRI report read for an orthopedic practice and
faxed to a physical therapy clinic in March 2019. It is **2 pages, portrait**, a raster
scan with no text layer. Every page carries the fax machine's transmission header.

| Page | Content |
|---|---|
| 1 | The practice's fax cover sheet: letterhead, a staff roster down the left margin, To/From/Date/Subject blocks, and a confidentiality notice |
| 2 | The report: patient block, study details, history, comparison, technique, findings, impression, and signature lines |

| | |
|---|---|
| Sender | Rebound Orthopedics & Neurosurgery (Northwest Surgical Specialists, P.C.), Vancouver, WA |
| Source | Contributed by the patient. Not published online, so there is no source URL |
| Received | 2026-11-15 |
| Clearance | Redacted |

This replaces the collection's earlier medical-imaging-report folder, a 3-page sample
report published by New York State DOCCS, at the operator's direction.

The patient this report describes contributed it and gave explicit permission to
publish it, on one condition: their name must not appear. The patient chose to remove
their name only. Everything else is as faxed: the clinic's staff roster, the referring,
reading and sending staff, the medical record and accession numbers, the dates, and the
clinical content.

The scan arrived with the patient's name and date of birth covered by black marks. These
were **stamp annotations drawn over an intact scan**, so removing the annotations in any
PDF editor would reveal the original text underneath.

Three regions were burned into the page images: the patient name on both pages and the
date of birth on page 2. The image pixels in each region were blanked and a solid black
box drawn in their place, and the stamp annotations were deleted. The boxes are fitted
to each text line, so the neighbouring labels (PATIENT NAME, MRN, DOB, SEX) stay
legible. Checks on the output: the raw embedded image pixels under every box read pure
white, no annotations remain, and the PDF metadata is empty.

The usual text sweep for the original strings was not run, because the patient chose
not to supply them. The burn happened before the document was parsed, so the originals
never left the source file. There is no text layer and no metadata in which they could
survive. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Imaging reports move between providers, insurers and patients, and much of that traffic
still runs over fax.

- **Physical therapy and specialty clinics:** staff file incoming reports into the
  patient's chart and match them to a referral.
- **Health insurers:** utilization review teams read the findings and impression to
  approve surgery or therapy.
- **Workers' compensation and personal injury claims:** adjusters and attorneys use
  imaging findings as evidence of injury.
- **Health information management:** release-of-information and records teams index
  faxed reports by patient, study and date.
- **Clinical research and registries:** abstractors pull study details and impressions
  into research databases.

### What it contains

- **A fax of a scan,** with no text layer and a transmission header on every page.
- **A cover sheet that is mostly noise,** including a roster of about 60 staff names
  down the margin.
- **A report body in all capitals,** as exported from a radiology information system.
- **Multi-line findings and impression sections** in free text.
- **Burned-in black redaction boxes,** as real records arriving from outside often
  carry.
- **A value that wraps onto its own line** below its label, the accession number.
