# Service Manual

**On the website:** [landing.ai/document-type/service-manual](https://landing.ai/document-type/service-manual)

Five pages from Goodman's service instructions for its APG/GPG 14 SEER gas/electric
package units with R-410A refrigerant. They are the cover, the Cooling and Gas Heating
Analysis Charts that match each cause of a fault to its symptoms and remedy, the
servicing table of contents, and the first procedure, Checking Voltage.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 25 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:36 | 2026-11-19 03:52 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 26,559 | 26,354 |
| Words under 0.95 confidence | 314 | n/a |
| Words under 0.80 confidence | 156 | n/a |
| Words under 0.50 confidence | 88 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.9 s | 15.6 s |
| Per page | 1.8 s | 3.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.5 credits | 9.1 credits |
| Per page | 0.70 credits | 1.82 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:36 | 2026-11-19 03:53 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 25 | 25 |
| Non-null fields returned | 25 | 25 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 191.2 s | 123.6 s |
| Per schema field (25) | 7.65 s | 4.94 s |
| Per value returned | 0.34 s | 0.22 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 24.8 credits | 25.1 credits |
| Per schema field (25) | 0.992 credits | 1.004 credits |
| Per value returned | 0.045 credits | 0.044 credits |

## Origin

`source/goodman-gpg14-service-manual-excerpt.pdf` is five pages from Goodman's service
instructions for its APG/GPG 14 SEER gas/electric package units with R-410A refrigerant
(publication RS6300012r4, July 2017). It is **5 pages, portrait (612×792)**, with a text
layer throughout (Acrobat Distiller). The cover drawing and the chart grids are vector
paths.

| | |
|---|---|
| Publisher | Goodman Manufacturing Company, L.P. (hosted by HVACDirect) |
| Source | [hvacdirect.com/…/GPG14-Service.pdf](https://hvacdirect.com/media/hvac/pdf/GPG14-Service.pdf) |
| Title | Service Instructions: APG/GPG 14 SEER Gas Electric Package Units with R-410A Refrigerant & Accessories (RS6300012r4, July 2017) |
| Retrieved | 2026-10-14 |
| Clearance | Public |

This is a manufacturer's service manual, written for HVAC technicians and distributed
freely for use with Goodman equipment. This copy is hosted by HVACDirect, an online HVAC
retailer that posts manufacturers' manuals for the products it sells. Other dealers and
distributors carry Goodman's manuals for this unit the same way (an earlier RS6300012
revision is on Alpine Home Air's document server). No page on goodmanmfg.com was found
linking this exact revision, so the retailer's URL is the source of record. The manual
carries "Copyright © 2014-2017 Goodman Manufacturing Company, L.P.", so it is publicly
distributed material rather than copyright-free material. It was downloaded by script.

The full manual is 67 pages. This file keeps five of them, in this order, split out with
PyMuPDF at the operator's choice:

| Page here | Manual page | Content |
|---|---|---|
| 1 | 1 | Cover |
| 2 | 32 | Cooling Analysis Chart |
| 3 | 33 | Gas Heating Analysis Chart |
| 4 | 34 | Servicing table of contents (S-1 to S-314) |
| 5 | 35 | S-1 Checking Voltage |

There is no personal data on the kept pages: no names, phone numbers or email addresses.
Nothing was redacted. The document metadata was cleared when the pages were split out.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A service manual tells technicians how to diagnose and repair a specific piece of
equipment. Manufacturers publish thousands of them, and the troubleshooting charts are
the pages technicians use most.

- **HVAC contractors and field technicians:** they look up symptoms, causes and service
  procedures on the job.
- **Equipment manufacturers:** they maintain manuals across models and revisions and
  feed them into support and training tools.
- **Field service management and support platforms:** they turn manuals into searchable
  knowledge bases and guided troubleshooting.
- **Distributors and retailers:** they host manuals for the products they sell, as
  HVACDirect does here.
- **Facilities and property maintenance teams:** they keep manuals for the equipment in
  their buildings.

### What it contains

- **Troubleshooting matrices** that map each cause to the symptoms it produces.
- **Rotated column headers.** Sixteen symptom columns on page 2 (nine on page 3) are
  labeled with text turned 90 degrees, under merged group headers.
- **Dot-only cells.** The data is a bullet in a cell, so which symptom a dot belongs to
  can only be read from its position under a rotated label.
- **A sparse reference column.** Many rows have no service procedure reference.
- **A two-column table of contents** of servicing procedures.
- **A short procedure with a small limits table,** and a vector line drawing on the
  cover.
- **Broken word spacing** in the text layer, such as "Pow er Failure".
