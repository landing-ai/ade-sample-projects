# EKG report

Source assets for `landing.ai/document-type/ekg-report`.

## Sample document

`source/vectracor-universal-ecg-sample-report.pdf` is a resting **12-lead EKG report**
(a "3x4 Simultaneous ECG Report") from VectraCor's PC-based Universal ECG system. It is
**1 page, landscape**, a native PDF with a text layer. A header carries four blocks
(patient details, recording details, machine measurements and interpretation statements).
Below it, the tracing grid shows twelve leads in a 3x4 layout over a lead II rhythm strip,
with paper speed, gain and filter settings along the bottom.

| | |
|---|---|
| Publisher | VectraCor (formerly QRS Diagnostic) |
| Source | [vectracor.com/…/ECG-Sample-Report-1.pdf](https://www.vectracor.com/wp-content/uploads/2020/03/ECG-Sample-Report-1.pdf) |
| Retrieved | 2026-10-13, downloaded directly by script |
| Clearance | Redacted |

VectraCor links the PDF as "Universal ECG Sample Report" from its
[Universal ECG product page](https://www.vectracor.com/universal-ecg/). A byte-identical
copy is also at `.../ECG-Sample-Report.pdf`.

**A caveat on terms, accepted by the operator.** The footer reads "Copyright QRS
Diagnostic", and the PDF carries no reuse licence. Clearance therefore rests on the file
being a sample the manufacturer publishes for its own product. The operator accepted it on
that basis on 2026-10-13.

### What was changed

- **Kept page 1 of 9.** Pages 2–9 show the same recording in other lead layouts.
- **Turned the page upright.** Page 1's content was drawn sideways under a `/Rotate` of
  180. The rotation was built into the content stream, so the page is now upright
  landscape (840 × 660 pt) with `/Rotate` 0. The fix was made before redaction, because
  replacement text is written horizontally.
- **Replaced the patient's name** (1 occurrence on the kept page) with **John Sample**.
  The demo name could not be shown to be fictitious. The replacement was made with
  `scripts/redact.py`, which removes the underlying text rather than covering it. The
  other eight printings of the name went with the dropped pages. The other patient
  details were left as printed, as the request asked.
- **Cleared the document metadata.**

The output was then checked: the original name cannot be extracted from the committed
PDF, and it appears nowhere in this folder. The rules file stays outside the repo.

## Why this document

This is the collection's first **medical device printout**, and its first document that is
mostly a **waveform**:

- **About 100,000 vector paths of grid and trace** sit under a few lines of header text.
  The parse treats the whole tracing as one `<figure type="CHART">` and writes its own
  description of it, with a small table of the lead labels.
- **Measurements printed with their units** ("80 bpm", "186 ms") are extracted as plain
  integers.
- **Coded interpretation statements** ("193 Anteroseptal infarction, probably old") are
  split into a code and its text.
- **A source drawn sideways**, which had to be turned upright before it could be redacted
  or parsed cleanly.

## Featured fields: the machine's read of the recording

All on page 1.

| Field | Value |
|---|---|
| Heart rate (bpm) | 80 |
| PR interval (ms) | 186 |
| QRS duration (ms) | 100 |
| QTc interval (ms) | 416 |
| Interpretation statement | Anteroseptal infarction, probably old |

These are the rate, the three intervals a reader checks first, and the finding that
matters clinically. They are the numbers an underwriter or a cardiology data pipeline
takes from an EKG.

**Differences from the request.** The request suggested heart rate, PR and QRS, QT/QTc,
the interpretation statements and the filter/scale settings.

- **QT was left out in favour of QTc**, to keep to five fields. It grounds correctly too.
- **The filter and scale settings could not be featured.** They are extracted correctly,
  but they are printed along the bottom edge of the tracing. The parse folds that text
  into the description it writes for the chart, so the settings' ranges point at the
  description and their box would cover the whole tracing.

No named individual is featured.

## What it surfaced

- **Header text grounds exactly.** Every measurement, the interpretation status, each
  statement's code and text, and every patient and recording field reads `ok`. Each box
  is the label-and-value line it came from.
- **Text inside the tracing becomes part of the chart.** The lead labels, the scale, the
  filters and the "Data must be reviewed by a qualified physician" notice all end up in
  the figure's model-written description and table. The lead labels still ground to
  their cells in that table. The settings ground only to the description, which is why
  they cannot be shown as crops.
- **Empty fields came back as the string `"null"`**, not JSON null. This happened for
  Location and Comments, and both ground `OFF` to their bare labels.
- **The parse ignored the waveform's size.** About 100k paths parsed in about 8 seconds
  as a single block, with no failed pages.

## Schema

`schema.json` has 26 leaf fields: the report title; patient details; recording details
(timestamp, device and location); the seven measurements; interpretation status, coded
statements and comments; paper speed, gain and filters; and the lead labels. The
waveform itself is not extracted.

## Credits

**2.10 credits** at the standard tier (parse 0.9 plus extract), through the jobs API.
The parse model was `dpt-3-pro-20260710`.

## Regenerate

```bash
# from the repo root; the source PDF is already redacted and upright
.venv/bin/python document-types/scripts/run_ade.py ekg-report        # spends credits
.venv/bin/python document-types/scripts/build_images.py ekg-report   # free
.venv/bin/python document-types/scripts/inspect_fields.py ekg-report
```
