# EKG report

**On the website:** [landing.ai/document-type/ekg-report](https://landing.ai/document-type/ekg-report)

A resting 12-lead EKG report from VectraCor's PC-based Universal ECG system, with the
patient's name replaced. A header carries the patient and recording details, the
machine's measurements (rate and intervals) and coded interpretation statements. Below
it, the tracing shows twelve leads in a 3x4 layout over a lead II rhythm strip.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 26 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:51 | 2026-11-19 02:23 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,430 | 1,919 |
| Words under 0.95 confidence | 1 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 14.4 s | 16.9 s |
| Per page | 14.4 s | 16.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.4 credits | 1.0 credits |
| Per page | 0.40 credits | 1.00 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:51 | 2026-11-19 02:23 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 26 | 26 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 166.2 s | 76.6 s |
| Per schema field (26) | 6.39 s | 2.95 s |
| Per value returned | 4.15 s | 1.92 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.4 credits | 1.3 credits |
| Per schema field (26) | 0.054 credits | 0.050 credits |
| Per value returned | 0.035 credits | 0.033 credits |

## Origin

`source/vectracor-universal-ecg-sample-report.pdf` is a resting **12-lead EKG report**
(a "3x4 Simultaneous ECG Report") from VectraCor's PC-based Universal ECG system. It is
**1 page, landscape**, a native PDF with a text layer. A header carries four blocks
(patient details, recording details, machine measurements and interpretation
statements). Below it, the tracing grid shows twelve leads in a 3x4 layout over a lead II
rhythm strip, with paper speed, gain and filter settings along the bottom.

| | |
|---|---|
| Publisher | VectraCor (formerly QRS Diagnostic) |
| Source | [vectracor.com/…/ECG-Sample-Report-1.pdf](https://www.vectracor.com/wp-content/uploads/2020/03/ECG-Sample-Report-1.pdf) |
| Linked from | [vectracor.com/universal-ecg](https://www.vectracor.com/universal-ecg/) |
| Retrieved | 2026-10-13, downloaded directly by script |
| Clearance | Redacted |

VectraCor links the PDF as "Universal ECG Sample Report" from its Universal ECG product
page. A byte-identical copy is also at `.../ECG-Sample-Report.pdf`.

**A caveat on terms, accepted by the operator.** The footer reads "Copyright QRS
Diagnostic", and the PDF carries no reuse licence. Clearance therefore rests on the file
being a sample the manufacturer publishes for its own product. The operator accepted it
on that basis on 2026-10-13.

What was changed:

- **Kept page 1 of 9.** Pages 2-9 show the same recording in other lead layouts.
- **Turned the page upright.** Page 1's content was drawn sideways under a `/Rotate` of
  180. The rotation was built into the content stream, so the page is now upright
  landscape (840 × 660 pt) with `/Rotate` 0. The fix was made before redaction, because
  replacement text is written horizontally.
- **Replaced the patient's name** (1 occurrence on the kept page) with **John Sample**.
  The demo name could not be shown to be fictitious. The redaction removes the
  underlying text rather than covering it. The other eight printings of the name went
  with the dropped pages. The other patient details were left as printed, as the request
  asked.
- **Cleared the document metadata.**

The output was then checked: the original name cannot be extracted from the committed
PDF, and it appears nowhere in this folder. The redaction rules file stays outside the
repo. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

The EKG is one of the most common tests in medicine, and its printout travels well
beyond the clinic that recorded it.

- **Life insurance underwriting:** underwriters read the rate, intervals and
  interpretation statements when an applicant's coverage calls for an EKG.
- **Cardiology and primary care:** clinicians compare a new tracing's measurements with
  earlier ones in the patient's record.
- **Health records and data teams:** they move EKG results from device printouts into
  structured fields in the record.
- **Clinical research:** trials collect interval measurements such as QTc as safety
  data.
- **Occupational health and pre-employment screening:** examiners file EKGs for
  commercial drivers, pilots and other screened roles.

### What it contains

- **A waveform that fills most of the page,** about 100,000 vector paths of grid and
  trace under a few lines of header text.
- **Measurements printed with their units,** such as "80 bpm" and "186 ms".
- **Coded interpretation statements,** each a numeric code followed by its text.
- **Label-and-value blocks** for patient and recording details, some left empty.
- **Text inside the tracing:** lead labels, scale and filter settings, and a review
  notice printed along the tracing's edges.
- **A landscape page** with a native text layer.
