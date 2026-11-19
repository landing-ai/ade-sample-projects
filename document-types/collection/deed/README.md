# Deed

**On the website:** [landing.ai/document-type/deed](https://landing.ai/document-type/deed)

A California grant deed by which the City of Los Angeles sold a surplus parcel in
Pacific Palisades to White Picket Fence, Inc. for $1,100,000 in 2011. It names the
grantor and grantee, the price and the transfer tax, the parcel and its legal
description, and carries the Mayor's signature, the City Clerk's attestation and a
notary acknowledgment.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 35 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:23 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 4,898 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 14.0 s |
| Per page | 2.8 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 3.8 credits |
| Per page | 0.76 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:23 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 35 |
| Non-null fields returned | 32 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 67.0 s |
| Per schema field (35) | 1.91 s |
| Per value returned | 1.72 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 3.9 credits |
| Per schema field (35) | 0.111 credits |
| Per value returned | 0.100 credits |

## Origin

`source/deed.pdf` is a California **grant deed** executed September 23, 2011, by which
the City of Los Angeles sold the surplus parcel at 15241 De Pauw Street, Pacific
Palisades (APN 4412-028-906), to White Picket Fence, Inc. It is **5 pages, portrait (US
Letter)**, a scan with a weak OCR layer: the deed, its Exhibit A legal description with
the surveyor's stamp, the signature cover with the departmental approvals, the execution
page signed by the Mayor and attested by the City Clerk, and the notary acknowledgment.

| | |
|---|---|
| Publisher | City of Los Angeles, Office of the City Clerk (Council File 10-2450), for the Department of General Services, Asset Management Division |
| Source | [cityclerk.lacity.org/onlinedocs/2010/10-2450_misc_9-23-11.pdf](https://cityclerk.lacity.org/onlinedocs/2010/10-2450_misc_9-23-11.pdf) |
| Retrieved | 2026-10-04 |
| Clearance | Public |

The file is the City Clerk's own copy in the Council File Management System, the
official public record of Council File 10-2450. It was downloaded by script. The filing
runs to 13 pages; only pages 1-5, the first deed, are kept. Pages 6-10 are a second deed
and 11-13 transmittal letters. Document metadata was cleared.

The parties are a city and a corporation. Everyone named appears in an official or
professional capacity: the Mayor, the City Clerk, a deputy city attorney, the General
Services general manager, the licensed surveyor who signed Exhibit A, and the notary. The
grantee's "When recorded mail to" block names a contact at the corporation's business
address; it was left in place as a corporate-capacity name. No redaction was needed.

This is the executed original filed with the City Clerk, not the recorded copy, so there
is no recorder's stamp. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A deed is the instrument that transfers ownership of real property, and every sale,
refinance and title search depends on reading one correctly.

- **Title insurance and escrow:** examiners trace the chain of title through each deed,
  checking grantor, grantee, legal description and any reservations.
- **Mortgage lending:** lenders confirm that the borrower holds title to the property
  being pledged.
- **County recorders and assessors:** recorded deeds are indexed by party and parcel,
  and the transfer tax and sale price feed property reassessment.
- **Real estate law and land records:** attorneys and abstractors read deeds for
  easements, mineral-rights exceptions and other conditions.
- **Government asset management:** cities, counties and agencies that buy and sell
  surplus land keep the deeds as the record of each transaction.

### What it contains

- **Prose, not a form.** The parties, the price and the conveyance are all in one
  granting sentence that runs across several lines.
- **A price in words and figures,** with the figures in bold mid-sentence.
- **A transfer tax declaration in the margin,** for two jurisdictions on two lines.
- **Handwritten dates** for the execution and on the notary acknowledgment.
- **An exhibit** with the legal description (lot, block, tract and map book) under a
  surveyor's stamp.
- **Signatures, an attestation and a notary seal** across the last three pages.
- **A scan with a weak OCR layer,** so the text has to be read from the page image.
