# Confidential Information Memorandum

**On the website:** [landing.ai/document-type/confidential-information-memorandum](https://landing.ai/document-type/confidential-information-memorandum)

A confidential information memorandum (CIM) prepared in May 2018 by BDO Canada Limited,
as court-appointed receiver, to sell the assets of the PTL Group, a site services,
equipment rental and aggregate supply business in Newfoundland and Labrador. It has a
covering letter to bidders, an executive summary with investment highlights and charts,
site descriptions, historical and forecast income statements, and the sale process.

| | |
|---|---|
| Pages | 19 |
| Fields in the extraction schema | 48 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:43 | 2026-11-19 02:47 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 51,677 | 50,859 |
| Words under 0.95 confidence | 68 | n/a |
| Words under 0.80 confidence | 34 | n/a |
| Words under 0.50 confidence | 10 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.2 s | 17.8 s |
| Per page | 0.8 s | 0.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.1 credits | 22.3 credits |
| Per page | 0.43 credits | 1.17 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:43 | 2026-11-19 02:47 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 48 | 48 |
| Non-null fields returned | 48 | 48 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 140.7 s | 453.7 s |
| Per schema field (48) | 2.93 s | 9.45 s |
| Per value returned | 1.26 s | 4.05 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 14.0 credits | 13.8 credits |
| Per schema field (48) | 0.292 credits | 0.288 credits |
| Per value returned | 0.125 credits | 0.123 credits |

## Origin

`source/ptl-group-cim-redacted.pdf` is a **confidential information memorandum** for the
sale of the PTL Group (PTL Holdings Limited, PTL Services (Equipment) Limited, CSL
Services (Industrial) Limited and 9263357 Canada Inc.), a site services, equipment
rental and aggregate supply business in Southern Harbour, Newfoundland and Labrador. BDO
Canada Limited prepared it in May 2018 as court-appointed receiver, to market the
companies' assets to bidders. It is **19 pages, portrait (612×792)**, created digitally
with a text layer: a photo cover, a covering letter to prospective purchasers, a
disclaimer, contacts, an executive summary with investment highlights and charts, site
descriptions, a five-year historical income statement, a three-year forecast, a sale
process summary and the full sale process as Appendix A.

| | |
|---|---|
| Publisher | BDO Canada Limited, as court-appointed receiver of the PTL Group |
| Source | [bdo.ca/getmedia/c60b2304-857e-45ef-8825-cdc24ec12bbb/1st-App-H-PTL-Group-CIM.pdf](https://www.bdo.ca/getmedia/c60b2304-857e-45ef-8825-cdc24ec12bbb/1st-App-H-PTL-Group-CIM.pdf) |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | **Redacted**, see below |

The memorandum was filed publicly as Appendix H to the Receiver's First Report to the
Supreme Court of Newfoundland and Labrador, and BDO publishes it on bdo.ca with the
other receivership filings. Every page still carries the "Confidential Information
Memorandum" legend, and page 2 the notice that it is provided under a non-disclosure
agreement. That is its wording from the marketing stage, before it was filed. BDO's
engagement page for the PTL Group blocks scripted access, so the link from that page to
this file was not confirmed. The file itself is on BDO's own domain.

The companies, the receiver and the court are kept. The receiver's individual staff are
replaced:

| What | Replaced with | Occurrences |
|---|---|---|
| Receiver staff contacts' names | Jane Q Sample, John Q Sample | 5 |
| Their work email addresses | ja@example.com, jo@example.com | 7 |
| Staff direct lines, and office phone and fax numbers (area codes kept) | fiction-reserved 555-01xx numbers, one stand-in per number | 9 |

The redaction removed the underlying text rather than covering it, and the emails'
`mailto:` links went with the text. The firm names, the two BDO office addresses and the
bid delivery address are corporate and kept as printed. One name in the covering letter
wraps across a line break, so its stand-in is split across the two lines. The stand-ins
are set in Helvetica, so they look slightly different from the surrounding text.

Two leak paths beyond the page text were closed. The PDF's author field named a staff
member and was cleared. One embedded JPEG photograph carried XMP metadata naming a staff
member as its creator, so the metadata segments of every embedded JPEG were stripped
without re-encoding, which leaves the pixels unchanged. No original value can be
extracted from the committed PDF's page text, metadata, objects or decoded streams,
checked as literal strings and as bare digits, and none appears anywhere in this folder.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A CIM is the document a seller sends to qualified bidders to market a business. This one
is a distressed sale run by a court-appointed receiver.

- **Private equity and corporate development:** deal teams screen CIMs to decide which
  businesses to bid on, and pull the financials into their models.
- **Investment banks and M&A advisors:** sell-side advisors write CIMs, and buy-side
  advisors summarize them for clients.
- **Insolvency and restructuring:** receivers, trustees and their counsel market
  distressed assets through CIMs under court-approved sale processes.
- **Lenders and credit funds:** acquisition lenders read the CIM's financials and
  forecasts when sizing a loan.
- **Due diligence and data rooms:** analysts index CIMs alongside the rest of a deal's
  documents.

### What it contains

- **A long mixed narrative:** a legal letter, disclaimers, marketing copy, site
  descriptions and dense numbered sale conditions.
- **A side-by-side highlights panel** next to running text.
- **Image-only charts and tables,** including a five-year income statement with no text
  layer behind it.
- **Financial tables** with historical, trailing-average and forecast columns.
- **Facts repeated in different words** across the covering letter, executive summary
  and appendix, such as the receiver, the court order and the bid deadline.
- **Photographs** on the cover and in the site descriptions.
