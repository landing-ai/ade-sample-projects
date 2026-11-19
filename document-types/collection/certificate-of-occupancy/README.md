# Certificate of occupancy

**On the website:** [landing.ai/document-type/certificate-of-occupancy](https://landing.ai/document-type/certificate-of-occupancy)

A New York City Department of Buildings Temporary Certificate of Occupancy for a school
building at 192 East 151st Street in the Bronx, effective April 16, 2019. It identifies
the property and the building's classification, lists the outstanding requirements, and
tabulates the permitted use, occupancy and capacity of each floor.

| | |
|---|---|
| Pages | 4 |
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
| Processed (UTC) | 2026-11-19 02:39 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 6,780 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 11.8 s |
| Per page | 3.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 3.7 credits |
| Per page | 0.93 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:39 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 27 |
| Non-null fields returned | 27 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 435.1 s |
| Per schema field (27) | 16.11 s |
| Per value returned | 2.23 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 6.5 credits |
| Per schema field (27) | 0.241 credits |
| Per value returned | 0.033 credits |

## Origin

`source/certificate-of-occupancy.pdf` is a New York City Department of Buildings
Temporary Certificate of Occupancy, No. 220152652T005, for the school building at 192
East 151st Street in the Bronx, effective April 16, 2019. It is **4 pages, portrait (US
Letter)**, a scan with no text layer: the certificate itself, two pages of the
Permissible Use and Occupancy table, and a closing page.

| | |
|---|---|
| Publisher | NYC Department of Buildings; posted by Public Prep, the charter school network occupying the building |
| Source | [resources.finalsite.net/…/CertificateOfOccupancy.pdf](https://resources.finalsite.net/images/v1582305033/publicprep/w9uf0livvpbwada6gzn2/CertificateOfOccupancy.pdf) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

Certificates of occupancy are public records, available through the Department of
Buildings' BIS system. This one is posted on the website of the school network that
occupies the building, hosted on Finalsite, a school website platform. It names no
private individual: it describes the building, its permitted uses and capacities, and
carries the signatures of the Borough Commissioner and the Commissioner in their
official capacity. No redaction was needed. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A certificate of occupancy states that a building may legally be occupied, and for what
uses and how many people. A temporary certificate also has an expiration date and a list
of conditions still to be met.

- **Commercial real estate:** buyers and their attorneys confirm during due diligence
  that the building's legal use matches how it is used.
- **Mortgage lending:** lenders ask for the certificate before closing on new
  construction or a change of use.
- **Insurance underwriting:** underwriters check occupancy classification and
  capacities when pricing property and liability cover.
- **Leasing and tenants:** landlords and tenants confirm that the space is approved for
  the tenant's planned use.
- **Schools, permitting and compliance:** operators, expediters and inspectors track
  temporary certificates and their outstanding requirements until a final one issues.

### What it contains

- **A scan with no text layer,** so everything has to be read from the page image.
- **A dense ruled form** with lettered sections A to E and label and value pairs packed
  into cells.
- **A use table whose columns run together.** The Floor To value sits against Maximum
  persons permitted ("001 234" is floor 001, 234 persons), so the columns have to be
  separated by position.
- **A table across two pages,** with the header repeated.
- **Blank cells** for Maximum persons and Floor To on some rows.
- **Signatures and an agency logo** on the certificate.
