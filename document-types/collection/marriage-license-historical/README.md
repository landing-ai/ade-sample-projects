# Marriage License (Historical)

**On the website:** [landing.ai/document-type/marriage-license-historical](https://landing.ai/document-type/marriage-license-historical)

The 1886 Hamilton County, Ohio marriage license of William Howard Taft and Helen Louise
Herron, issued June 19, 1886 and returned the same day. It has a printed probate-court
affidavit completed in ink, naming the applicant, the intended spouse and the judge, and
a marriage return at the foot with the officiant's certification. The image is a
photograph of the ledger page taken around 1910–15.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 14 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:34 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 1,123 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 46.2 s |
| Per page | 46.2 s |

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
| Processed (UTC) | 2026-11-19 03:35 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 14 |
| Non-null fields returned | 12 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 115.1 s |
| Per schema field (14) | 8.22 s |
| Per value returned | 9.59 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 0.7 credits |
| Per schema field (14) | 0.050 credits |
| Per value returned | 0.058 credits |

## Origin

`source/taft-marriage-license-1886.pdf` is the 1886 Hamilton County, Ohio marriage
license of **William Howard Taft and Helen Louise Herron**, issued June 19, 1886 and
returned the same day. It has two parts:

- a printed probate-court affidavit, completed in ink
- the marriage return at the foot, with the officiant's certification

The image is a Bain News Service glass-plate photograph of the license, taken around
1910–15 while Taft was President. It is **1 page, landscape**, in greyscale: a photo of a
ledger page, with the negative's handwritten caption ("TAFT MARRIAGE LICENSE") running up
the left margin. It has no text layer.

| | |
|---|---|
| Publisher | Library of Congress, Prints and Photographs Division (Bain News Service collection), via Wikimedia Commons |
| Source | https://upload.wikimedia.org/wikipedia/commons/b/bd/Taft_Marriage_License%2C_Ohio_LOC_2162683291.jpg |
| Retrieved | 2026-11-15 |
| Clearance | Public |

The Library of Congress lists the image with "no known restrictions on publication"
(Flickr ID 2162683291). It was downloaded by script from Commons as a 1024×751 greyscale
JPEG and wrapped in a one-page PDF with no metadata.

It is published as printed, with no redaction, under the historical-record and
public-figure exemptions:

- **The record is more than 72 years old.** It is dated June 19, 1886 on its face.
- **Both people named in it are deceased public figures.** William Howard Taft, 27th
  President of the United States, died March 8, 1930. Helen Herron Taft died May 22,
  1943. Source: Encyclopaedia Britannica's biographies of each.
- **The other names appear in official roles.** These are the probate judge, the deputy
  clerk and the officiant.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Marriage records are among the most requested vital records. Older ones survive as
handwritten ledger pages, often only as photographs or microfilm.

- **Genealogy services:** they index historical marriage records by name, date and
  county.
- **County probate courts and recorders:** they digitize old ledgers and issue
  certified copies.
- **Historians and biographers:** they use marriage records to date and verify events
  in people's lives.
- **Archives and libraries:** they catalog photographs of records like this one.
- **Legal and estate research:** heir searches and probate cases trace marriages to
  establish relationships.

### What it contains

- **19th-century handwriting** for every value, some faded and some smudged.
- **Handwritten values inside printed legal prose,** on fill-in lines mid-sentence ("And
  that ___ is more than eighteen years of age …").
- **A photograph of a bound ledger page,** not a flat scan, in greyscale.
- **A hand-ruled box** holding the license number.
- **Handwritten dates** in the form "19 day of June 1886".
- **A handwritten caption** running up the left margin of the negative.
- **Flourished capitals** that make some names hard to read.
