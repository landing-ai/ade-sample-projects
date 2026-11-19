# Driver's license (US state)

**On the website:** [landing.ai/document-type/drivers-license-usa](https://landing.ai/document-type/drivers-license-usa)

The official specimen of Texas's 2025 driver license design, the front of the card. It
carries the license number, the holder's name, address and date of birth, issue and
expiry dates, class, restrictions and endorsements, a physical description, and the
portrait, all filled with specimen data.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 15 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:57 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 563 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 4.9 s |
| Per page | 4.9 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 0.7 credits |
| Per page | 0.70 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:57 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 15 |
| Non-null fields returned | 12 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 135.4 s |
| Per schema field (15) | 9.02 s |
| Per value returned | 11.28 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 0.5 credits |
| Per schema field (15) | 0.033 credits |
| Per value returned | 0.042 credits |

## Origin

`source/texas-dl-specimen-2025.png` is the official specimen of Texas's 2025 driver
license design, the front of the card. It is **1 image, landscape (600×385)**, cropped
from the Texas Department of Public Safety's news release image.

| | |
|---|---|
| Publisher | Texas Department of Public Safety |
| Source | [dps.texas.gov/news/dps-rolls-out-new-driver-license-design](https://www.dps.texas.gov/news/dps-rolls-out-new-driver-license-design) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

DPS published this card in its August 18, 2025 release announcing the new design. Every
field is specimen data: "SAMPLE JANE", DL 12345678, 123 Sample Street, Sample City, TX
12345, with "SAMPLE" printed across the portrait. The portrait is DPS's specimen model,
not a license holder, and the director's printed signature is part of the card design.
No redaction was needed.

The request gave a Google Images thumbnail (`encrypted-tbn0.gstatic.com`), which is
Google's cached copy of an image hosted elsewhere, not a publisher. Tracing it led to the
DPS release, whose banner image carries the identical card. The file here is that banner,
`8.18.2025-New-DL-Design-PR.jpg` (1080×742), cropped to the card at box (22, 300, 622,
685), so the banner's "LATEST NEWS" headline is not part of the image. The card in the
banner is slightly larger than the thumbnail, and it is the publisher's own file.

DPS publishes the card at about 600 pixels wide, the largest version found, so the text
is small. DPS's card designs page carries two other specimens ("SAMPLE JANICE SOFÍA" and
an under-21 "ZACHARY JOSÉ" card), both smaller still. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A driver's license is the most common proof of identity in the US, so it arrives as a
photo or scan in almost every onboarding flow.

- **Banking and fintech KYC:** banks, brokerages and payment apps read the license to
  verify a customer's name, date of birth and address when an account is opened.
- **Car rental and car sharing:** companies check the class, expiry date and
  restrictions before they release a vehicle.
- **Insurance:** auto insurers capture the license number and driver details for quotes
  and policies.
- **Healthcare and pharmacies:** patient intake and controlled-substance pickups record
  the ID presented.
- **Age-restricted retail, hospitality and HR:** staff verify age and identity, and
  employers record identity documents for employment eligibility.

### What it contains

- **A card, not a page.** About twenty fields, each a small AAMVA field code ("4d DL",
  "16 Hgt", "18 Eyes") followed by its value.
- **A patterned security background** with a guilloche, a seal, a ghost portrait and
  microtext behind the fields.
- **Security features among the fields:** a second, smaller portrait, a star and rotated
  ghost text.
- **A portrait photo** and a printed signature.
- **A low-resolution image** about 600 pixels wide, with very small text.
- **Dates in a fixed US format** for birth, issue and expiry.
