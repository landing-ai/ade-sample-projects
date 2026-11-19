# Negotiable certificate of deposit

**On the website:** [landing.ai/document-type/negotiable-certificate-of-deposit](https://landing.ai/document-type/negotiable-certificate-of-deposit)

A Barclays Bank D.C.O. negotiable certificate of deposit, No. 301, issued in
Johannesburg on 25 July 1964 for R100,000 at 3.65% for 180 days, due 21 January 1965.
The printed certificate is completed by hand and typewriter, payable to the bearer, and
carries three South African revenue stamps and two bank officers' signatures.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 16 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:38 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 1,796 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 8.7 s |
| Per page | 8.7 s |

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
| Processed (UTC) | 2026-11-19 03:38 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 16 |
| Non-null fields returned | 15 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 219.1 s |
| Per schema field (16) | 13.69 s |
| Per value returned | 12.17 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.0 credits |
| Per schema field (16) | 0.062 credits |
| Per value returned | 0.056 credits |

## Origin

`source/occ-first-negotiable-cd.jpg` is a Barclays Bank D.C.O. negotiable certificate of
deposit, No. 301, issued in Johannesburg on 25 July 1964 for R100,000 at 3.65% for 180
days, due 21 January 1965. It is **1 image, landscape (600×461)**, a black-and-white
reproduction of the printed certificate, completed by hand and typewriter, with three
South African revenue stamps and two signatures.

| | |
|---|---|
| Publisher | Office of the Comptroller of the Currency (image credited to A. P. Faure / South African Financial Markets Journal) |
| Source | [occ.gov/images/history/img-barclays-cd-600px.jpg](https://www.occ.gov/images/history/img-barclays-cd-600px.jpg) |
| Linked from | [The Negotiable CD: National Bank Innovation in the 1960s](https://www.occ.gov/about/who-we-are/history/history-of-the-occ/1936-1966/1936-1966-negotiable-cd.html) |
| Retrieved | 2026-09-30 |
| Clearance | Public |

The OCC publishes the image on its history page with the caption "In July 1964 the
British bank Barclays, in amalgamation with the National Bank of South Africa, issued a
negotiable CD (above) at 100,000 Rand" and the credit **A. P. Faure / South African
Financial Markets Journal**. It is therefore a third-party image the OCC republishes,
not a US government work, and the credit line should go with it. The manifest carries
it in `origin.credit`.

The certificate is payable to the bearer and names no individual. The two signatures are
the bank's General Manager and Chief Accountant, signing in their official capacity. No
redaction was needed.

The request described this as the first negotiable CD ever issued. The OCC page says
First National City Bank of New York issued the first, in February 1961, and presents
this 1964 certificate as an early international one. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A negotiable certificate of deposit is a large time deposit that the holder can sell
before it matures. Old certificates like this one survive in archives and in the
records of banks and collectors.

- **Banks and trust departments:** they verify the issuer, amount, rate and maturity of
  deposit instruments they hold or redeem.
- **Custodians and money market funds:** they record the terms of CDs held for clients
  and track maturity dates.
- **Archives, museums and financial historians:** they catalog historical instruments
  like this one by issuer, date and terms.
- **Bank examiners and auditors:** they check deposit instruments against the bank's
  records.
- **Collectors and auction houses:** they describe and authenticate old financial
  documents from their printed and handwritten details.

### What it contains

- **Handwriting and typewriting over print.** The dates, amount, term and rate are
  written or typed into blanks on an engraved form.
- **A small, old reproduction,** 600 pixels wide, black and white.
- **A decorative border and ornamented type.**
- **A choice left in the form.** "payable to *the Bearer of this Certificate *the Order
  of", with a footnote to delete whichever does not apply.
- **Revenue stamps** stacked down the right edge, each with its value.
- **Two handwritten signatures** of bank officers.
