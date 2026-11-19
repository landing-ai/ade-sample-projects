# Food sensitivity report

**On the website:** [landing.ai/document-type/food-sensitivity-report](https://landing.ai/document-type/food-sensitivity-report)

Genova Diagnostics' sample IgG Food Antibodies profile, a clinical lab report for a
specimen patient. Page 1 is a grid of 87 foods in seven categories, each with an IgG
reactivity code and a color-coded box, plus a Total IgE result. Page 2 groups the foods
by reactivity level, and pages 3 and 4 explain the elimination diet.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 13 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:00 | 2026-11-19 03:05 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 11,577 | 12,530 |
| Words under 0.95 confidence | 52 | n/a |
| Words under 0.80 confidence | 28 | n/a |
| Words under 0.50 confidence | 10 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 12.1 s | 21.3 s |
| Per page | 3.0 s | 5.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.8 credits | 5.2 credits |
| Per page | 0.45 credits | 1.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:00 | 2026-11-19 03:05 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 13 | 13 |
| Non-null fields returned | 13 | 13 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 152.4 s | 328.2 s |
| Per schema field (13) | 11.72 s | 25.24 s |
| Per value returned | 0.55 s | 1.19 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 7.7 credits | 7.9 credits |
| Per schema field (13) | 0.592 credits | 0.608 credits |
| Per value returned | 0.028 credits | 0.029 credits |

## Origin

`source/1001-IgG-Food-Antibodies-Sample-Report.pdf` is Genova Diagnostics' sample IgG
Food Antibodies profile, a clinical lab report. It is **4 pages, portrait (612×792)**,
with a full text layer. Page 1 is a grid of 87 foods in seven categories, each with an
IgG reactivity code and a color-coded box, plus a Total IgE panel. Page 2 groups the
foods by reactivity level, and pages 3 and 4 are commentary on the elimination diet.

| | |
|---|---|
| Publisher | Genova Diagnostics |
| Source | [gdx.net/core/sample-reports/1001-IgG-Food-Antibodies-Sample-Report.pdf](https://www.gdx.net/core/sample-reports/1001-IgG-Food-Antibodies-Sample-Report.pdf) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

Genova publishes this among its sample reports for clinicians. The patient is "SAMPLE
PATIENT", with date of birth, sex, MRN and ID left blank. The only person named is the
laboratory director, in the page footer, in a professional capacity, and the CLIA and
Medicare license numbers are the laboratory's. No redaction was needed.

**Why "sensitivity", not "allergy".** The folder was first named `food-allergy-report`.
The report itself says IgG responses are "in a class distinct from Immunoglobulin E (IgE)
food allergy reactions", and that its elimination diet is "specific to food sensitivities
… not those defined as classic (IgE-mediated) food allergy reactions". The slug names
what the document is. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Food antibody panels come back from specialty labs as multi-page reports, and the
results have to be read into a care plan or a patient record.

- **Functional and integrative medicine practices:** clinicians use the reactivity
  levels to build an elimination diet.
- **Dietitians and nutritionists:** they turn the high and moderate results into meal
  plans and reintroduction schedules.
- **Specialty laboratories:** they produce and quality-check the reports and send
  results to ordering clinicians.
- **Health records and patient portals:** teams move lab results from PDF reports into
  structured fields.
- **Research:** studies of diet and immune response collect results across many
  patients.

### What it contains

- **A results grid without ruling.** 87 foods sit in four columns, grouped under
  category headings that break each column at different heights.
- **Meaning carried by color.** Each result has a code (0, VL, 1+, 2+, 3+) and a colored
  box beside it.
- **An in-range indicator,** where the Total IgE result sits in an "Inside" or "Outside"
  box.
- **A color legend bar** below the grid.
- **The same data twice.** Page 2 restates the grid as lists by reactivity level.
- **Narrative commentary** on pages 3 and 4.
- **A full text layer** on portrait pages.
