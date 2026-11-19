# Immigration Visa (Historical)

**On the website:** [landing.ai/document-type/immigration-visa-historical](https://landing.ai/document-type/immigration-visa-historical)

A United States Quota Immigration Visa, No. 840, issued by the American Consular
Service at Riga, Latvia on February 2, 1927, under the Immigration Act of 1924. It is a
printed government form filled in on a typewriter, with the bearer's photograph and
signature, quota and nationality, passport details, a fee stamp and the vice consul's
signature.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 19 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:16 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 2,003 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 10.9 s |
| Per page | 10.9 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.1 credits |
| Per page | 1.10 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:17 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 19 |
| Non-null fields returned | 18 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 161.2 s |
| Per schema field (19) | 8.48 s |
| Per value returned | 8.95 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.0 credits |
| Per schema field (19) | 0.053 credits |
| Per value returned | 0.056 credits |

## Origin

`source/quota-immigration-visa-riga-1927.pdf` is a **United States Quota Immigration
Visa**, No. 840, issued by the American Consular Service at Riga, Latvia on February 2,
1927, under the Immigration Act of 1924. The bearer is classed as a Preference immigrant
on the Russian quota, traveling on a Soviet passport issued at Kiev. It is a printed
Government Printing Office form, filled in on a typewriter. It is **1 page, portrait**,
a 600×820 grayscale image wrapped in a PDF, with no text layer.

| | |
|---|---|
| Issued by | U.S. Department of State, American Consular Service, Riga |
| Source | [wiki.rootsweb.com/wiki/images/e/e5/ImmigrationVisa-lores.jpg](https://wiki.rootsweb.com/wiki/images/e/e5/ImmigrationVisa-lores.jpg) |
| Hosted at | RootsWeb wiki (Ancestry) |
| Retrieved | 2026-11-16, downloaded manually |
| Clearance | Public |

This is a record of the US federal government. It is the kind of document held in the
USCIS **Visa Files** series (July 1, 1924 to March 31, 1944), the arrival records created
when the 1924 act required immigrants to obtain a visa abroad.

RootsWeb blocks scripted access, so the operator downloaded the image by hand. Its
RootsWeb file-description page refused scripted access (HTTP 403), so the uploader and
any further attribution could not be checked. RootsWeb is therefore recorded as the
host, not the publisher. The image was wrapped in a one-page PDF with no metadata.

It is published as printed, including the bearer's name and photograph, under the
historical-record exemption. The visa is dated February 2nd, 1927 on its face, more than
72 years ago. The bearer is photographed as an elderly woman at that date, so she is long
deceased. The vice consul signs in an official role. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Historical immigration visas are primary records of how and when a person entered the
US. They are read today mostly by people tracing families and proving lineage.

- **Genealogy and family history services:** researchers and platforms index visas to
  link immigrants to arrival records and family trees.
- **Archives and libraries:** archivists digitize and catalog Visa Files and similar
  series so they can be searched by name, date and place.
- **Citizenship by descent:** applicants and their lawyers use an ancestor's visa and
  passport details to prove nationality for a second citizenship.
- **Immigration history research:** historians study quota classes, nationalities and
  ports of departure across many records.
- **Government records requests:** USCIS genealogy requests return copies of visa files
  that families then need to read and transcribe.

### What it contains

- **A printed form filled in on a typewriter,** with two columns of typed blanks inside
  printed legal sentences.
- **Checkboxes** for Preference or Nonpreference.
- **Paired blanks with captions underneath,** such as "(Quota.)" and "(Nationality.)".
- **A photograph and stamps overlapping the text,** with the bearer's handwritten
  signature across the photo.
- **A handwritten file number** at the top and the vice consul's signature.
- **A two-line passport number.**
- **The ribbon and seal** of the visa packet.
- **A low-resolution grayscale image** with no text layer, as many genealogy-site copies
  are.
