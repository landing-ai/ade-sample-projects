# Elevation certificate (flood)

**On the website:** [landing.ai/document-type/elevation-certificate](https://landing.ai/document-type/elevation-certificate)

A FEMA Elevation Certificate for a Sarasota County fire station in Nokomis, Florida,
certified by a licensed surveyor in March 2024. It records the property and its flood
map data (community, map panel, flood zone and base flood elevation), the surveyed
elevations of the building, the surveyor's certification, and photographs of the
building.

| | |
|---|---|
| Pages | 7 |
| Fields in the extraction schema | 45 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:52 | 2026-11-19 02:57 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 20,152 | 22,138 |
| Words under 0.95 confidence | 52 | n/a |
| Words under 0.80 confidence | 17 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.3 s | 14.7 s |
| Per page | 1.2 s | 2.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.1 credits | 9.1 credits |
| Per page | 0.44 credits | 1.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:52 | 2026-11-19 02:58 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 45 | 45 |
| Non-null fields returned | 42 | 42 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 238.1 s | 199.8 s |
| Per schema field (45) | 5.29 s | 4.44 s |
| Per value returned | 5.18 s | 4.34 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.8 credits | 6.2 credits |
| Per schema field (45) | 0.129 credits | 0.138 credits |
| Per value returned | 0.126 credits | 0.135 credits |

## Origin

`source/elevation-certificate-sarasota-fire-station.pdf` is a **FEMA Elevation
Certificate** (Form FF-206-FY-22-152, the 2022 edition) for a Sarasota County fire
station at 1930 N. Tamiami Trail, Nokomis, Florida. A licensed surveyor at GeoSurv, LLC
certified it on March 11, 2024. It is **7 pages, portrait (US Letter)**, with a text
layer from the fillable form. The pages are Sections A and B (property and flood map
data), C and D (surveyed elevations and certification), E to I (blank on this
certificate), and two pages of building photographs.

| | |
|---|---|
| Publisher | Sarasota County, Florida (floodplain records); prepared by GeoSurv, LLC |
| Source | [ftp.scgov.net/GIS/ElevCerts/…Fire Station…pdf](https://ftp.scgov.net/GIS/ElevCerts/220021_EC_Fire%20Station%20FINAL_dsigned3-11-24_22%20115132%2000%20BC.pdf) |
| Retrieved | 2026-10-13 |
| Clearance | **Redacted**, see below |

The file is hosted on Sarasota County's own server. It sits in a public directory of
about 7,600 permit-linked elevation certificates that the county posts as an NFIP
Community Rating System community. The county's flood-maps page, which links to the
directory, returned 403 to scripts, so that link was not confirmed by script. The file
itself is on the county's domain and was downloaded by script.

The building owner is the county, and the building is a public fire station, so there is
no private owner data. The surveyor's printed name, license number, title and firm
contact details are professional information on a public record, and were kept.

The following were removed:

- **The surveyor's seal image.** The Section D seal box is now empty.
- **The digital signature.** This covers the signature form field and its visible
  appearance: the signature itself and the signer and timestamp line beside it. The
  Signature line is blank, and no stand-in was drawn.
- **12 pages.** These are page 1 and pages 9 to 19, which are FEMA's blank instructions
  and building diagrams. The footers still read "Page N of 19".
- **Document metadata.**

No text value was replaced. The output was verified: no image or text remains inside the
removed regions, and the metadata is empty. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

An elevation certificate records how high a building sits relative to the base flood
elevation on the flood map. It sets flood insurance rates and proves compliance with
floodplain rules.

- **Flood insurance:** NFIP and private flood insurers rate policies from the flood zone
  and the surveyed floor elevations.
- **Local floodplain management:** communities keep certificates for permitted
  buildings to show compliance, as Sarasota County does here.
- **Mortgage lending:** lenders and borrowers use it when flood insurance is required on
  a property in a special flood hazard area.
- **Real estate:** buyers and agents request it to estimate flood insurance cost before
  a sale.
- **Surveying and engineering:** surveyors prepare and certify it, and engineers use it
  for elevation and map amendment requests.

### What it contains

- **A dense federal form with numbered items.** Items A1 to A9, B1 to B13 and C2.a to h
  pack label and value pairs onto shared lines.
- **Numbers that only mean something together.** The flood zone and base flood
  elevation in Section B are compared with the surveyed floor and grade elevations in
  Section C.
- **Checkbox answers** for the datum, the BFE source, construction status and the units.
- **Blank items next to printed zeros,** which mean different things.
- **Photo pages** with captioned photographs and an empty fourth photo slot.
- **Whole sections left blank** (E to I) on this certificate.
