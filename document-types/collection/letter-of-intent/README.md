# Letter of intent

**On the website:** [landing.ai/document-type/letter-of-intent](https://landing.ai/document-type/letter-of-intent)

A regulatory exhibit filed with the Kentucky Public Service Commission that holds a
signed, non-binding letter of intent from Central States Water Resources to buy a sewer
utility in Scott County, Kentucky, for $849,000. The letter is followed by pages from a
second letter of intent and the two definitive purchase agreements that came after,
with their exhibits.

| | |
|---|---|
| Pages | 49 |
| Fields in the extraction schema | 28 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:31 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 104,721 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 39.8 s |
| Per page | 0.8 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 50.7 credits |
| Per page | 1.03 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:32 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 28 |
| Non-null fields returned | 28 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 315.1 s |
| Per schema field (28) | 11.25 s |
| Per value returned | 6.56 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 24.8 credits |
| Per schema field (28) | 0.886 credits |
| Per value returned | 0.517 credits |

## Origin

`source/central-states-water-delaplain-loi.pdf` is Exhibit PSC 4-1(b) from Kentucky
Public Service Commission Case No. 2022-00432, as filed by Bluegrass Water. It is **49
pages, portrait (612×792)**, a raster scan with an OCR text layer, a PSC docket stamp on
every page and a CSWR letterhead bar on the letter pages. It contains:

| Pages | Content |
|---|---|
| 1-5 | Signed and countersigned non-binding letter of intent dated July 16, 2019, from Central States Water Resources (CSWR) to buy the assets of Delaplain Disposal Company, a sewer utility in Scott County, Kentucky, for $849,000 |
| 6-7 | Two image-only pages (no OCR layer) from a second CSWR letter of intent, to River Bluffs, Inc.: its exclusivity page and signature page |
| 8-28 | The Delaplain Purchase and Sale Agreement (August 2019, DocuSigned), with exhibits A-H, most of them placeholders |
| 29-49 | The River Bluffs Agreement for Sale of Utility System (June 2019, $240,000), with exhibits A-E |

| | |
|---|---|
| Publisher | Kentucky Public Service Commission (filed by Bluegrass Water Utility Operating Company) |
| Source | [psc.ky.gov/pscecf/2022-00432/…/Exhibit_PSC_4-1(b)_-_Purchase_Agreements.pdf](https://psc.ky.gov/pscecf/2022-00432/kerry.ingle@dinslaw.com/07272023081341/Exhibit_PSC_4-1(b)_-_Purchase_Agreements.pdf) |
| Linked from | [psc.ky.gov/Case/ViewCaseFilings/2022-00432/Post](https://psc.ky.gov/Case/ViewCaseFilings/2022-00432/Post) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

The file is a public regulatory filing on the PSC's official e-filing store. It is used
**exactly as filed, unredacted**, by the operator's decision of 2026-10-28. That departs
from the collection's usual rule that personal data is replaced before parsing. The pages
carry the following, all as they appear in the public record:

- signers' typed names, wet-ink signatures and DocuSign signatures
- a named executive's email address, and business phone, cell and fax numbers, on the
  letterhead
- names, email addresses and phone numbers of notice parties and counsel in the purchase
  agreements

The only change from the filed file: the PDF's document-information and XMP metadata
were cleared. The `author` field had held the name of the person who prepared the
filing, which is not part of the visible document. Full provenance is in `manifest.json`
under `source.origin`.

## Why this document

### Who processes it

A letter of intent sets out the main terms of a deal before the definitive agreement is
drafted. It is read again later, as here, when a regulator or a buyer reviews how the
deal came about.

- **M&A and corporate development:** deal teams track price, structure, exclusivity and
  due diligence periods across letters of intent in the pipeline.
- **Utility and infrastructure acquirers:** buyers of regulated utilities file letters
  and purchase agreements with state commissions when they seek approval.
- **Public utility commissions:** staff review acquisition filings to confirm the price
  and terms of the deal.
- **Law firms:** attorneys compare the letter's terms with the definitive agreement that
  followed.
- **Lenders and investors:** they review deal terms before committing financing.

### What it contains

- **Several documents in one file.** Two letters of intent and two purchase agreements,
  each with exhibits, sit in one regulatory exhibit.
- **Dense legal prose** where the price, the assets, the conditions and the binding
  sections are all in numbered clauses.
- **A raster scan with an OCR layer** that garbles some text, such as the letterhead
  email, differently from page to page.
- **Pages with no text layer at all** (pages 6-7).
- **Handwritten dates** in the purchase agreements, such as "23rd day of August".
- **Wet-ink and DocuSign signatures,** with signature and acceptance blocks.
- **A docket stamp on every page** and a letterhead bar on the letter pages.
