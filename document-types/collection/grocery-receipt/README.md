# Grocery Receipt

**On the website:** [landing.ai/document-type/grocery-receipt](https://landing.ai/document-type/grocery-receipt)

A phone photo of a Costco Wholesale receipt from the Greenville, SC warehouse, dated
March 31, 2019. It lists three items with their item numbers, prices and tax codes, a
$0.00 tax line, a $38.48 total and a chip-read card payment. The paper is creased and
unevenly lit, photographed on a granite counter.

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
| Processed (UTC) | 2026-11-19 03:13 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 768 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 6.0 s |
| Per page | 6.0 s |

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
| Processed (UTC) | 2026-11-19 03:14 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 19 |
| Non-null fields returned | 19 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 191.2 s |
| Per schema field (19) | 10.06 s |
| Per value returned | 5.79 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.0 credits |
| Per schema field (19) | 0.053 credits |
| Per value returned | 0.030 credits |

## Origin

`source/costco-grocery-receipt.pdf` is a Costco Wholesale receipt from the Greenville, SC
warehouse, dated March 31, 2019. It is a **phone photo, not a scan**: the paper is
creased and slightly curled, lit unevenly with a shadow across the top half, and
photographed on a granite counter. It is **1 page, portrait**, an image with no text
layer.

| | |
|---|---|
| Publisher | Apartment Therapy Media (The Kitchn), as an editorial image |
| Source | https://cdn.apartmenttherapy.info/image/upload/f_auto,q_auto:eco,c_fit,w_730,h_974/k%2Farchive%2Fadc09d0a4189a5d96ed835ac0633656decdcf991 |
| Retrieved | 2026-11-15 |
| Clearance | Redacted |

The image was downloaded by script from the publisher's CDN as a 730×973 JPEG and
wrapped in a one-page PDF, with no text layer and no metadata. The publisher printed the
photo but the receipt belongs to a shopper, so it was treated as a personal record.

| What | Replaced with |
|---|---|
| Costco membership number (12 digits) | A randomly generated 12-digit stand-in |
| Last four digits of the masked card number | A randomly generated 4-digit stand-in |

Both were replaced in the pixels before the document was parsed. Each was painted over
with paper colour blended from either side of it, so the patch follows the photo's
lighting rather than showing as a flat box. The stand-in was then redrawn in Arial
Narrow at the original's size and ink colour. The PDF is built from the edited image
alone. Tesseract OCR of the output finds neither original, as text or inside any run of
digits.

These were kept: the store address, item numbers and transaction references (sequence,
approval code, transaction and merchant IDs). They belong to the retailer and the
transaction, not to the shopper. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Receipts are the proof of purchase behind expense claims, rebates and loyalty programs.
Most arrive as phone photos of thermal paper.

- **Expense management:** employees photograph receipts, and finance teams match the
  merchant, date and total to card transactions.
- **Consumer rewards and loyalty apps:** apps read the items and totals on uploaded
  receipts to award points and verify purchases.
- **Consumer packaged goods and market research:** brands and panels collect item-level
  purchase data from shopper receipts.
- **Accounting and bookkeeping:** small businesses and accountants record purchases and
  sales tax from receipts.
- **Rebate and warranty processing:** claims teams check the store, date and item
  against the offer.

### What it contains

- **A phone photo of thermal paper** with creases, curl and a shadow across the top
  half, and no text layer.
- **Item numbers fused to descriptions** on one line.
- **A tax-code letter printed twice,** beside the price and again in the left margin.
- **A total printed inside an inverted black bar,** white digits on black.
- **No quantity or unit price** on single-unit item lines.
- **A card payment block** with a masked card number and transaction references.
