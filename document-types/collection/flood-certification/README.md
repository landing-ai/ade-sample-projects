# Flood certification

**On the website:** [landing.ai/document-type/flood-certification](https://landing.ai/document-type/flood-certification)

A completed FEMA Standard Flood Hazard Determination Form, prepared in September 2023
for a residential mortgage on a property in Jackson Township, New Jersey. It records the
NFIP community, the flood map panel, the flood zone, whether the building is in a
Special Flood Hazard Area, and whether flood insurance is available. A fee slip and the
borrower's flood hazard notice follow.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 41 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:58 | 2026-11-19 03:03 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 9,683 | 10,135 |
| Words under 0.95 confidence | 19 | n/a |
| Words under 0.80 confidence | 6 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.2 s | 50.0 s |
| Per page | 2.4 s | 16.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.5 credits | 4.1 credits |
| Per page | 0.50 credits | 1.37 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:58 | 2026-11-19 03:04 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 41 | 41 |
| Non-null fields returned | 37 | 37 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 190.9 s | 139.6 s |
| Per schema field (41) | 4.66 s | 3.40 s |
| Per value returned | 5.16 s | 3.77 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.4 credits | 3.5 credits |
| Per schema field (41) | 0.083 credits | 0.085 credits |
| Per value returned | 0.092 credits | 0.095 credits |

## Origin

`source/flood-certification.pdf` is a completed FEMA **Standard Flood Hazard
Determination Form** (SFHDF, form FF-206-FY-21-116). ServiceLink National Flood prepared
it in September 2023 for a residential mortgage from a bank lender, for a property in
Jackson Township, Ocean County, New Jersey. It is **3 pages, portrait (US Letter)**, with
a text layer:

1. The determination form: loan information, the NFIP community, the map panel, the
   flood zone, insurance availability, the Special Flood Hazard Area answer, HMDA codes
   and the preparer.
2. A short fee slip with the order number, loan number and fee.
3. The borrower notice, *Notice of Special Flood Hazards and Availability of Federal
   Disaster Relief Assistance*, with "Property NOT IN SFHA" checked.

| | |
|---|---|
| Publisher | ServiceLink National Flood, on FEMA's Standard Flood Hazard Determination Form |
| Source | [scribd.com/document/671333520/Flood-Certificate](https://www.scribd.com/document/671333520/Flood-Certificate) |
| Retrieved | 2026-10-03, downloaded manually because Scribd blocks scripted downloads |
| Clearance | Redacted |

Scribd is a user-upload site, not a publisher, so this was treated as a personal record.
Redaction happened before anything was parsed. It used
`document-types/scripts/redact.py`, which removes the underlying text rather than
covering it. The rules file was kept outside the repo. What was replaced:

| What | Replaced with | Occurrences |
|---|---|---|
| Borrower's name | SAMPLE, JANE Q | 2 |
| Property street address | 100 MAIN ST | 2 |
| ZIP+4 add-on of the property address | a random 4-digit add-on (the 5-digit ZIP is kept) | 2 |
| Lender's customer number with the preparer | a plausible random 10-digit number | 1 |
| Loan identifier | a plausible random 11-digit number | 3 |
| Flood order number | a plausible random 10-digit number | 3 |

Kept: the lender (a bank) and its address, ServiceLink, FEMA, the NFIP community and map
data, the town, state and 5-digit ZIP, and the HMDA census tract codes. These describe
organizations, a FEMA map and a neighborhood, not a person. The form has no signatures
(the signature lines on page 3 are blank) and no barcodes. Its only image is the
preparer's logo. Document metadata was cleared. No original value is extractable from
the committed PDF, and none appears anywhere in this folder. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Federal rules require a flood determination for almost every US mortgage. It tells the
lender whether the building is in a Special Flood Hazard Area and so whether flood
insurance is mandatory.

- **Mortgage lenders and servicers:** they order a determination at origination and
  enforce flood insurance when the property is in an SFHA.
- **Flood zone determination companies:** vendors like the preparer here produce the
  forms and track life-of-loan changes to the flood maps.
- **Flood insurance agents and carriers:** they rate NFIP and private flood policies
  from the zone, community and map panel.
- **Bank regulators and compliance teams:** examiners check that loan files carry a
  valid determination and that borrowers received the notice.
- **Mortgage due diligence and loan purchasers:** reviewers check the form in each loan
  file when loans are sold or securitized.

### What it contains

- **A federally standardized ruled form** with lettered sections and numbered boxes.
- **Checkboxes and radio buttons as the answers.** Program type, insurance availability,
  LOMC and the YES/NO SFHA determination are marks, not text.
- **A notice chosen by a checked box.** On page 3 the borrower notice that applies is
  selected by a check mark.
- **The same facts on more than one page.** The loan and order numbers appear on all
  three pages, and the community and map panel are repeated on the notice.
- **Coded values** such as the flood zone, community number, map panel and HMDA census
  tract.
- **Blank signature lines** on the borrower notice.
