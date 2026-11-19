# Letter (Historical)

**On the website:** [landing.ai/document-type/letter-historical](https://landing.ai/document-type/letter-historical)

A 19th-century lithographed facsimile of William Penn's 1682 letter to the Lenape,
written in England before he sailed to Pennsylvania. In it Penn promises fair dealing
and signs "Your Loving Freind, Wm Penn". Below the letter, his surveyor general Thomas
Holme notes its delivery beside the Pennsylvania seal, and above it is an engraving
after Benjamin West's painting Penn's Treaty with the Indians.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 12 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:30 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 2,805 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 14.3 s |
| Per page | 14.3 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.3 credits |
| Per page | 1.30 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:30 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 12 |
| Non-null fields returned | 11 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 176.2 s |
| Per schema field (12) | 14.69 s |
| Per value returned | 11.75 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.8 credits |
| Per schema field (12) | 0.150 credits |
| Per value returned | 0.120 credits |

## Origin

`source/penn-letter-to-the-indians-1682.pdf` is a 19th-century lithographed facsimile of
**William Penn's letter to the Lenape**. Penn wrote it in England in 1682, before
sailing to Pennsylvania, and his surveyor general, Thomas Holme, delivered it and read
it aloud. It begins "The Great God who is the power and wisdom that made you and me…".
Holme's delivery note sits below, beside the Pennsylvania seal, and an engraving after
Benjamin West's painting *Penn's Treaty with the Indians* sits above. It is **1 page,
portrait**, a 704×1024 JPEG wrapped in a one-page PDF, with no text layer.

| | |
|---|---|
| Publisher | Library of Congress, Prints and Photographs Division (`pga.08522`) |
| Source | https://tile.loc.gov/storage-services/service/pnp/pga/08500/08522v.jpg |
| Retrieved | 2026-11-16, downloaded manually (the file is dated 2026-11-15) |
| Clearance | Public |

loc.gov refuses scripted access, so the operator downloaded the JPEG by hand. The LOC
handle `hdl.loc.gov/loc.pnp/pga.08522` is embedded in the file's comment field. The
item's catalogue record and rights statement **could not be read by script**. Library of
Congress Prints and Photographs items of this age are normally "no known restrictions on
publication". The image was wrapped in a one-page PDF with no metadata.

It is published as printed under the historical-record exemption:

- **The record is far past the 72-year line.** The letter is dated 1682, and the print
  is 19th century.
- **William Penn**, the founder of Pennsylvania, died in 1718.
- **Thomas Holme**, who signs the delivery note, died in 1695. Source: Irma Corcoran,
  *Thomas Holme, 1624–1695: Surveyor General of Pennsylvania*, American Philosophical
  Society, 1992.

**Requested as "Treaty (Historical)".** The document is not a treaty: it has no parties
agreeing terms, no articles and no ratification. The treaty is only the subject of the
engraving above the letter. The operator renamed the type to Letter (Historical).

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Historical letters survive mostly as manuscripts and printed facsimiles in archives.
Reading them at scale means transcribing old handwriting that few people can read
quickly.

- **Archives and special collections:** they catalog and transcribe correspondence so
  it can be searched.
- **Historians and genealogists:** they read letters for dates, names and events.
- **Digital humanities projects:** they turn manuscript collections into searchable,
  citable text.
- **Museums and educators:** they present transcriptions beside the original images.
- **Libraries:** digitization programs add transcriptions to scanned prints and
  manuscripts.

### What it contains

- **17th-century handwriting,** reproduced as a lithograph, with long s, "ye" and "yt"
  abbreviations, and spellings such as "freind" and "Rumme" (rum).
- **An old-style dateline** ("25: 2: 1682", meaning the 25th of the second month).
- **A flourished signature.**
- **A second hand** writing the delivery note.
- **A seal** beside the delivery note.
- **A large engraving** above the text.
- **An image-only page** with no text layer, and a tiny printer's imprint under the
  letter.
