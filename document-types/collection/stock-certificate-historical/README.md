# Stock Certificate (Historical)

**On the website:** [landing.ai/document-type/stock-certificate-historical](https://landing.ai/document-type/stock-certificate-historical)

Stock Certificate No. 95 of The Ford Motor Company of Canada, Limited, for ten $100
shares, issued at Walkerville, Ontario in November 1908 to James Couzens of Detroit. It
is an engraved form completed by hand, signed by G. M. McGregor as Secretary and Henry
Ford as President, with a red foil seal and a red-ink "Cancelled" across the middle.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 13 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:55 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 1,365 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 24.7 s |
| Per page | 24.7 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 0.9 credits |
| Per page | 0.90 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:55 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 13 |
| Non-null fields returned | 11 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 34.9 s |
| Per schema field (13) | 2.68 s |
| Per value returned | 2.91 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 0.8 credits |
| Per schema field (13) | 0.062 credits |
| Per value returned | 0.067 credits |

## Origin

`source/ford-motor-company-of-canada-1908.pdf` is **Stock Certificate No. 95** of The
Ford Motor Company of Canada, Limited, for ten $100 shares, issued at Walkerville,
Ontario in November 1908. The holder is James Couzens, of Detroit. It is signed by G. M.
McGregor as Secretary and by Henry Ford as President. It is **1 page, landscape**, a
high-resolution photograph with no text layer. The certificate is an engraved form
completed by hand, with a guilloche border, blackletter headings and a red foil seal. A
red-ink "Cancelled" is scrawled diagonally across the middle, and the back shows through
faintly.

| | |
|---|---|
| Publisher | Wikimedia Commons; photograph by Julie Ceccaldi, certificate from the Sammlung Commodore (Rüdiger K. Weng) |
| Source | https://upload.wikimedia.org/wikipedia/commons/1/1c/Ford_Motor_Company_of_Canada_1908.jpg |
| Retrieved | 2026-11-15 |
| Clearance | Public |

The photograph is released under **CC0**. It was downloaded by script as a 4080×3308
JPEG and wrapped in a one-page PDF with no metadata.

It is published as printed under the historical-record exemption. The evidence:

- **The record's date.** It is dated 1908 on its face, and the Commons record gives
  1908-11-10.
- **Everyone named is a deceased public figure acting in a corporate role.** James
  Couzens, Ford co-founder and later US Senator, died in 1936. Henry Ford died in 1947.
  Gordon M. McGregor, founder of Ford of Canada, died in 1922. Sources: the Detroit
  Historical Society's *Encyclopedia of Detroit* entry for Couzens, the Windsor Public
  Library's history of McGregor, and Henry Ford's biographies.

The Commons description names the holder as "Henry Couzens". The certificate clearly
reads **James** Couzens.

**This is not the document the request named.** The request named a photograph of Henry
Ford's own 1903 Ford Motor Company certificate, hosted by Investopedia. That image is a
licensed Getty Images photo (GettyImages-515176734), not released for reuse. The
operator chose this CC0 certificate instead. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Old paper stock certificates still turn up in estates, archives and collections, and
someone has to work out what they record and whether they still have value.

- **Estate settlement and probate:** executors and attorneys identify certificates found
  among a decedent's papers.
- **Transfer agents and unclaimed property:** they trace old certificates to current
  share registers or determine that they were cancelled.
- **Archives, museums and libraries:** curators catalogue the issuer, holder, date and
  signatories of historical financial documents.
- **Scripophily dealers and auction houses:** they describe and value certificates by
  issuer, number, signatures and condition.
- **Historical and genealogical research:** researchers read the names, places and dates
  on company records.

### What it contains

- **Handwriting in printed sentences.** The holder, residence, share count in words and
  date are filled into blanks in Edwardian copperplate.
- **Engraved type and ornament:** a guilloche border and blackletter headings.
- **Handwritten signatures** of the Secretary and the President.
- **A red-ink "Cancelled"** scrawled diagonally across the text.
- **A red foil seal** and show-through from the back of the paper.
- **A photograph, not a scan,** with no text layer.
