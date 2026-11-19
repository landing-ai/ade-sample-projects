# Business registration

**On the website:** [landing.ai/document-type/business-registration](https://landing.ai/document-type/business-registration)

An Idaho Certificate of Organization for a limited liability company, filed with the
Idaho Secretary of State in April 2018. The state's preprinted form is filled in with
typed values for the LLC's name, office address, registered agent and organizers, and
carries handwritten signatures, the office's filing stamp, a cashier's register imprint
and a handwritten filing number.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 36 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:34 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 1,837 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 7.9 s |
| Per page | 7.9 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.0 credits |
| Per page | 1.00 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:35 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 36 |
| Non-null fields returned | 27 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 302.6 s |
| Per schema field (36) | 8.41 s |
| Per value returned | 10.09 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.8 credits |
| Per schema field (36) | 0.050 credits |
| Per value returned | 0.060 credits |

## Origin

`source/business-registration.pdf` is an Idaho **Certificate of Organization, Limited
Liability Company**, filed with the Idaho Secretary of State in April 2018. It is **1
page, portrait**, a single raster scan with no text layer: the state's preprinted form
filled in by typewriter-style type, two handwritten signatures, the Secretary of State's
"FILED EFFECTIVE" rubber stamp, the cashier's register imprint, and a handwritten filing
number.

| | |
|---|---|
| Publisher | Idaho Secretary of State |
| Source | [sosbiz.idaho.gov/api/report/GetImageByNum/…](https://sosbiz.idaho.gov/api/report/GetImageByNum/097182066095252009134168051025113046056061167000) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

The Secretary of State serves this filing from its public business-entity search. The
scanned image is byte-identical to the copy the marketing team kept in the ADE Documents
shared drive (doc36), so the drive copy and the public record are the same document.

**Used as published, unredacted, by explicit decision of the operator.** The filing
carries what Idaho's public register carries: the names of the LLC's two organizers (who
are also its governors, one of them its registered agent), the street address they gave,
a PO box, and their handwritten signatures. The collection usually redacts public records
that name private people. Here the operator chose to keep the record as published, as
with the FINRA arbitration award. The PDF metadata holds only the state's imaging
software (GdPicture) and a timestamp. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A certificate of organization is the state's record that a business entity exists, so
anyone who has to verify a business before dealing with it asks for one.

- **Banking and payments:** know-your-business checks confirm the legal name, entity
  type, state and filing number before an account is opened.
- **Commercial lending:** lenders confirm that the borrowing entity exists and who
  formed and manages it.
- **Vendor onboarding and procurement:** buyers check a supplier's registration before
  setting it up for payment.
- **Registered agents and corporate services firms:** they file and track formation
  documents for their clients.
- **Legal and compliance teams:** they confirm entity details during contracts, due
  diligence and litigation.

### What it contains

- **Typed values on a preprinted form,** each on a rule under its numbered question.
- **A rubber stamp** ("FILED EFFECTIVE … SECRETARY OF STATE, STATE OF IDAHO"), faint and
  partly broken, that carries the filing date and time.
- **A cashier's register imprint** in a dot-matrix face, with date and time, check, batch
  and fee lines.
- **Handwriting:** two signatures and the filing number written in the state-use box.
- **Dates in two formats,** one on the stamp and one in the register imprint.
- **A raster scan with no text layer,** so every value has to be read from the page
  image.
