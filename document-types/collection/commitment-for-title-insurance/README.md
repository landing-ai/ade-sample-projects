# Commitment for Title Insurance

**On the website:** [landing.ai/document-type/commitment-for-title-insurance](https://landing.ai/document-type/commitment-for-title-insurance)

A 2016 ALTA Commitment for Title Insurance issued by First Integrity Title Company as
agent for Westcor Land Title Insurance Company on a residential property in foreclosure.
It sets out the proposed policy and insured, the vested owners, the property's legal
description, the requirements to be met before closing, and a Schedule B of exceptions
that lists deeds of trust, assignments, foreclosure notices and a judgment. The agent's
lender notes and both companies' privacy notices follow.

| | |
|---|---|
| Pages | 11 |
| Fields in the extraction schema | 49 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:42 | 2026-11-19 02:46 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 30,712 | 31,706 |
| Words under 0.95 confidence | 96 | n/a |
| Words under 0.80 confidence | 40 | n/a |
| Words under 0.50 confidence | 19 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.3 s | 32.6 s |
| Per page | 1.4 s | 3.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.8 credits | 13.5 credits |
| Per page | 0.44 credits | 1.23 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:43 | 2026-11-19 02:46 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 49 | 49 |
| Non-null fields returned | 48 | 48 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 152.1 s | 141.7 s |
| Per schema field (49) | 3.11 s | 2.89 s |
| Per value returned | 1.44 s | 1.32 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 12.4 credits | 12.1 credits |
| Per schema field (49) | 0.253 credits | 0.247 credits |
| Per value returned | 0.117 credits | 0.113 credits |

## Origin

`source/commitment-for-title-insurance-redacted.pdf` is a 2016 ALTA Commitment for Title
Insurance issued by First Integrity Title Company as agent for Westcor Land Title
Insurance Company, with the agent's lender notes and both companies' privacy notices. It
is **11 pages, portrait** (12 in the original). It has **no text layer**: the PDF was
produced by *Microsoft: Print To PDF*, which writes every glyph as a filled vector path.

| | |
|---|---|
| Publisher | First Integrity Title Company, as agent for Westcor Land Title Insurance Company |
| Source | [adc-tenbox-prod.imgix.net/…/PRELIMINARY_TITLE_REPORT/…pdf](https://adc-tenbox-prod.imgix.net/resi/propertyDocuments/1300098/PRELIMINARY_TITLE_REPORT/40C02EC5FCCE4D3BBF40A5C6B9BEF65F.v1.pdf) |
| Retrieved | 2026-10-02, by script |
| Clearance | Redacted |

It is posted as the preliminary title report on a residential property-auction listing,
for prospective bidders. That makes the file public, but not the people in it.

**It is a foreclosure file.** Schedule B-II records a notice of default and a notice of
trustee's sale against the first deed of trust. It named three private homeowners as
vested owners and trustors, and a named debtor under a child-support judgment. The
property could be found from its street address, its assessor's parcel number, the
legal description, or any of the county recording numbers. All of these were replaced
before the file entered the repo:

| Personal or locating data | Occurrences | Replaced with |
|---|---|---|
| Vested owners' and trustors' names (three people) | 9 | `Jonah Q Sample`, `Robert James Q Sample`, `Jane Q Sample` |
| Judgment debtor's full name | 1 | `Jonah Quinn Sample` |
| Street address, city, ZIP, county | 10 | `100 SAMPLE RD`, `Anytown`, `90000`, `Sample` |
| Assessor's parcel number | 3 | Random stand-in, same shape |
| Section, township, range, parcel map number, map page | 6 | Different numbers |
| Recording instrument numbers (8 distinct) | 9 | Year prefix kept, other digits random |
| MERS MIN, court case number | 2 | Random stand-ins, same shape |
| Commitment / order number, including the recorded-documents link | 10 | `FIN-78796415` |
| Wire instructions (title company's real trust account and routing numbers) | page 11 | page dropped |
| PDF metadata (a title-company employee's name) | — | cleared |

Amounts, dates, tax figures, and lender and trustee company names are kept. Once the
identifiers above are gone, they no longer point to a property. Corporate officers' names
and facsimile signatures are kept: Westcor's President and Secretary on the jacket, and
the agent's COO on Schedule A. They sign in a corporate capacity and appear on every
commitment these companies issue.

Because the file has no text layer, each string was located by OCR and the glyph paths
underneath it were deleted from the content stream, not covered. The replacement was
drawn in Helvetica at the original size and baseline. OCR of every page of the output,
on literals and on bare digits, found none of the originals, and a separate sweep of
every file in this folder found none either. One visible artifact remains: a replacement
shorter than its original leaves a gap before the next word (`100 SAMPLE RD , Anytown ,
CA`), because outlined text cannot reflow.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A title commitment is the title insurer's promise to issue a policy once listed
requirements are met. Every closing with title insurance starts from one, and every
party to the deal reads its exceptions.

- **Title and escrow companies:** they issue the commitment and clear its requirements
  before closing.
- **Mortgage lenders:** they review the exceptions to make sure their lien will have
  the priority they expect.
- **Real estate attorneys:** they examine the exceptions for liens, easements and
  judgments that affect the buyer.
- **Property auction platforms and investors:** they post or read the preliminary title
  report so bidders can see the encumbrances, as here.
- **Default servicing and foreclosure trustees:** they track notices of default and
  sale recorded against a property.

### What it contains

- **No text layer.** Every glyph is a vector outline, so the text has to be read from the
  page image, much as with a scan.
- **A long legal form** with a jacket, Schedule A, and Schedules B-I and B-II.
- **A two-page list of exceptions** (deeds of trust, assignments, foreclosure notices, a
  judgment), each with recording dates, instrument numbers and amounts.
- **A corporate seal and facsimile officer signatures** on the jacket.
- **Values that wrap** across lines, such as the issuing agent's name.
- **Privacy notices and lender notes** in dense small print.
