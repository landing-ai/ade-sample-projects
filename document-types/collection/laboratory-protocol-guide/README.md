# Laboratory Protocol Guide

**On the website:** [landing.ai/document-type/laboratory-protocol-guide](https://landing.ai/document-type/laboratory-protocol-guide)

ibidi's application guide Immunofluorescence Assays (FL_AG_039, V 1.0, September 2019).
It walks through an indirect immunofluorescence staining protocol step by step, from
fixation and blocking through antibody incubation to mounting and microscopy. It ends
with two troubleshooting tables, a comparison of ibidi's culture vessels and example
micrographs.

| | |
|---|---|
| Pages | 16 |
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
| Processed (UTC) | 2026-11-19 03:14 | 2026-11-19 03:28 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 53,863 | 52,595 |
| Words under 0.95 confidence | 103 | n/a |
| Words under 0.80 confidence | 57 | n/a |
| Words under 0.50 confidence | 25 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 19.2 s | 23.3 s |
| Per page | 1.2 s | 1.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.8 credits | 21.2 credits |
| Per page | 0.49 credits | 1.32 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:15 | 2026-11-19 03:28 |
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
| Total | 241.4 s | 141.4 s |
| Per schema field (19) | 12.71 s | 7.44 s |
| Per value returned | 2.30 s | 1.33 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 17.8 credits | 17.7 credits |
| Per schema field (19) | 0.937 credits | 0.932 credits |
| Per value returned | 0.170 credits | 0.167 credits |

## Origin

`source/ibidi-immunofluorescence-application-guide.pdf` is ibidi's application guide
*Immunofluorescence Assays* (FL_AG_039, V 1.0, September 2019). It walks through an
indirect immunofluorescence staining protocol, one step at a time: fixation,
permeabilization and blocking; primary and secondary antibody incubation; counterstain
and mounting, then microscopy. It then gives two troubleshooting tables, a comparison
table of ibidi's culture vessels, and example micrographs. It is **16 pages, portrait
A4**, with a text layer.

| | |
|---|---|
| Publisher | ibidi GmbH |
| Source | https://ibidi.com/img/cms/resources/AG/FL_AG_039_Immunofluorescence_150dpi.pdf |
| Retrieved | 2026-11-15 |
| Clearance | Public |

This is a vendor's own application guide, published free on its website. It was
downloaded by script directly from the publisher's domain, and the PDF metadata was
cleared.

The example pages credit the scientists who supplied each micrograph, by name and
institution. Those are professional attributions in the publisher's own document. They
are kept as printed. The back page carries ibidi's corporate addresses and phone lines.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Protocol guides tell a lab what to use, for how long, at what temperature, and what to
do when a step fails. Vendors publish them alongside their products.

- **Research and academic labs:** scientists adapt vendor protocols into their own
  standard operating procedures.
- **Biotech and pharmaceutical R&D:** teams standardize assay steps and reagent
  conditions across sites.
- **Lab informatics and electronic lab notebooks:** protocol steps and parameters are
  captured as structured methods.
- **Life science vendors:** application scientists and support teams answer customer
  questions from their own guides.
- **Quality and compliance teams:** they review documented methods for consistency and
  audit readiness.

### What it contains

- **Procedural prose** with parameters such as "4% formalin", "10 minutes" and "3x for
  5 minutes" inside sentences.
- **A two-column layout** with cell diagrams beside the text.
- **Ruled reference tables** for troubleshooting and the vessel comparison.
- **Micrographs** with credit lines naming their sources.
- **A photo cover** and a heavily designed page layout.
- **A born-digital text layer.**
