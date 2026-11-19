# Death Certificate

**On the website:** [landing.ai/document-type/death-certificate](https://landing.ai/document-type/death-certificate)

A certified copy of a Missouri Certification of Death, issued January 17, 2017 by the
Missouri Department of Health and Senior Services. It records where and when the death
occurred, the cause and manner of death, the informant and the funeral home, and carries
the state registrar's printed signature and the department's seal.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 23 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:55 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 1,180 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 8.3 s |
| Per page | 8.3 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 0.8 credits |
| Per page | 0.80 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:55 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 23 |
| Non-null fields returned | 20 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 70.5 s |
| Per schema field (23) | 3.07 s |
| Per value returned | 2.82 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.2 credits |
| Per schema field (23) | 0.052 credits |
| Per value returned | 0.048 credits |

## Origin

`source/missouri-certification-of-death.pdf` is a certified copy of a Missouri
**Certification of Death**, issued January 17, 2017 by the Missouri Department of Health
and Senior Services. It is **1 page, landscape**, an image with no text layer: a
photocopy of the state's green security-bordered certificate. Preprinted labels are in
sans-serif type and the values are typed in a monospace typewriter face.

| | |
|---|---|
| Publisher | KCUR 89.3, Kansas City's NPR member station, as an image in a 2017 news story |
| Issued by | Missouri Department of Health and Senior Services, Bureau of Vital Records |
| Source | [npr.brightspotcdn.com/…/DeathCertificate_white_out_2.png](https://npr.brightspotcdn.com/dims4/default/5dd4623/2147483647/strip/true/crop/2544x2120+0+0/resize/880x733!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fkcur%2Ffiles%2F201712%2FDeathCertificate_white_out_2.png) |
| Retrieved | 2026-11-15 |
| Clearance | Public |

The URL above is an 880-pixel resize. The source PDF was built from the full-size
2544×2120 original behind it, flattened onto white, with no metadata.

KCUR had already whited out the Social Security number and the residence address before
publishing. The PNG has a transparency channel, so it was checked: those boxes are blank
in the pixels themselves, not hidden by transparency.

The document is otherwise published exactly as KCUR printed it, at the operator's
decision:

- The decedent is deceased.
- The state registrar and his signature appear in an official capacity.
- The funeral home is a business.
- The surviving spouse's name is the only living private individual on the page. It was
  kept because the operator chose to use the image as published.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A certified death certificate is the legal proof of a death, and almost every account,
policy or estate that a person leaves behind needs one to close or transfer.

- **Life insurance:** claims teams need it before they pay a death benefit, and check
  the cause and manner of death against policy exclusions.
- **Banks and brokerages:** estate services teams close or retitle accounts and release
  funds to survivors.
- **Estate attorneys and probate courts:** a certified copy starts the probate process
  and the transfer of property.
- **Pension, annuity and benefits administrators:** they stop payments to the decedent
  and start survivor benefits.
- **Public health and vital statistics:** cause-of-death entries are coded for mortality
  statistics.

### What it contains

- **A fixed government form filled in on a typewriter,** with each value beside its
  label rather than in a cell.
- **Labels that wrap onto two lines,** such as "DATE OF / DEATH:".
- **A short free-text cause-of-death list** that mixes underlying causes, with
  intervals, and a contributing condition marked "SIG COND".
- **Boxes whited out** by the publisher, which must come back empty.
- **A heavy guilloche security border,** a seal and a printed signature.
- **A photocopy with no text layer,** so every value has to be read from the image.
