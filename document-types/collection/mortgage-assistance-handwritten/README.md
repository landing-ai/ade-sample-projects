# Mortgage Assistance (Handwritten)

**On the website:** [landing.ai/document-type/mortgage-assistance-handwritten](https://landing.ai/document-type/mortgage-assistance-handwritten)

Page 1 of Chase's Request for Mortgage Assistance Form, filled in by hand with invented
data and scanned. It covers the borrower and co-borrower, servicemember status, the
property and its occupancy, assistance history, listing and counseling details, and
real estate taxes and insurance, with handwritten values and hand-ticked checkboxes.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 27 |

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
| Characters returned | 4,858 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 14.8 s |
| Per page | 14.8 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.8 credits |
| Per page | 1.80 credits |

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
| Fields requested | 27 |
| Non-null fields returned | 18 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 229.2 s |
| Per schema field (27) | 8.49 s |
| Per value returned | 12.73 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 2.2 credits |
| Per schema field (27) | 0.081 credits |
| Per value returned | 0.122 credits |

## Origin

`source/chase-request-for-mortgage-assistance-handwritten.pdf` is page 1 of Chase's
**Request for Mortgage Assistance Form** (D19693 RMA 09/13): the borrower and
co-borrower section, servicemember status, property and occupancy, assistance history,
listing and counseling details, and taxes and insurance. It has been **filled in by
hand** and scanned. It is **1 page, portrait**, a raster scan with no text layer.

| | |
|---|---|
| Publisher | LandingAI; the form itself is JPMorgan Chase's published form |
| Source | Not published online. A specimen filled in by hand by LandingAI staff, from LandingAI's internal marketing document library (doc35) |
| Retrieved | 2026-11-16 |
| Clearance | Public |

A LandingAI staff member printed the blank form, filled it in by hand with **invented
data**, and scanned it. Everything handwritten on the page is fictitious, written for
this specimen:

- names, Social Security numbers and dates of birth
- phone numbers (the 555 range) and email addresses
- the mailing address and loan number
- the credit counselor's details

No real borrower's data is present, so nothing was redacted. The PDF metadata was
cleared. The Chase name and logo appear because they are printed on the form; Chase did
not produce or endorse this specimen. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Homeowners who are struggling to pay their mortgage fill in a request for mortgage
assistance to apply for a loan modification, forbearance or other relief. Some arrive
handwritten, by mail or fax, or as scans.

- **Mortgage servicing and loss mitigation:** servicers read the application to open a
  case and decide which relief options the borrower qualifies for.
- **Housing counseling agencies:** HUD-approved counselors help borrowers complete the
  form and submit it on their behalf.
- **Default management vendors:** outsourcers process assistance packages for servicers
  at volume.
- **Compliance and quality control:** teams check that applications were handled on
  time and that servicemember protections were applied.
- **Legal aid and foreclosure defense:** attorneys review what the borrower submitted
  and when.

### What it contains

- **Handwritten values,** in print and cursive, written into labeled boxes.
- **Hand-drawn ticks** in checkboxes, often overrunning the box and the label beside
  it.
- **Yes/no questions answered only by a tick,** such as whether the property is listed
  for sale.
- **A dense, faint, small-print bank form** with many fields per section.
- **Blank boxes** that the filer left empty, such as the co-borrower's home phone.
- **A raster scan with no text layer,** so everything is read from the page image.
