# Executive employment agreement

**On the website:** [landing.ai/document-type/executive-employment-agreement](https://landing.ai/document-type/executive-employment-agreement)

The employment agreement between the Bethlehem Central School District in Delmar, New
York, and its Superintendent of Schools, for a term from July 1, 2025 to June 30, 2030.
It sets out the term, salary and annual increases, longevity payments, benefits, leave,
renewal and termination in 18 numbered sections, and ends with the parties' signatures
and two notary acknowledgments.

| | |
|---|---|
| Pages | 13 |
| Fields in the extraction schema | 27 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:01 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 34,135 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 24.5 s |
| Per page | 1.9 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 15.1 credits |
| Per page | 1.16 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:02 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 27 |
| Non-null fields returned | 27 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 146.7 s |
| Per schema field (27) | 5.44 s |
| Per value returned | 4.73 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 8.2 credits |
| Per schema field (27) | 0.304 credits |
| Per value returned | 0.265 credits |

## Origin

`source/executive-employment-agreement.pdf` is the superintendent employment agreement
between the Bethlehem Central School District (Delmar, NY) and its Superintendent of
Schools, approved July 1, 2025, for a term running from July 1, 2025 to June 30, 2030.
It is **13 pages, portrait (612×792)**, a wet-ink executed scan: every page is one image,
with an invisible OCR text layer over it. Pages 1 to 12 hold the recitals and 18
numbered sections (term, compensation, duties, benefits, leave, renewal, termination and
so on). Page 12 ends with a side-by-side signature block, and page 13 holds two notary
acknowledgments with stamps and seals.

| | |
|---|---|
| Publisher | Bethlehem Central School District |
| Source | [bethlehemschools.org](https://www.bethlehemschools.org/wp-content/uploads/2025/09/J-Monroe-Employment-Contract-Approved-7-1-2025-with-signatures-accessible.pdf) |
| Linked from | The district's [Employment Contracts](https://www.bethlehemschools.org/employment-contracts/) page |
| Retrieved | 2026-10-28, by script |
| Clearance | Public |

The district posts this agreement for public access, and in New York a public employee's
contract is a public record. **The operator chose not to redact it.** All 13 pages are
committed as the district filed them, including the parties' names, their signatures and
the notaries' details on pages 12 and 13. This is a deliberate exception to the
collection's usual rule that personal data is replaced before parsing. The decision was
made explicitly on 2026-10-28.

Only the PDF's document metadata was cleared: the `/Info` dictionary, the XMP and the
tagged-PDF structure tree. The page images and the OCR text layer are untouched. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An executive employment agreement fixes an executive's term, pay, benefits and exit
terms. Public employers publish them, and private companies file them as exhibits to
their SEC reports.

- **HR and compensation teams:** they track term dates, salary increases, leave and
  renewal notice deadlines across executive contracts.
- **Employment law practices:** attorneys review compensation, termination and notice
  provisions when negotiating or disputing a contract.
- **Public sector oversight:** school boards, auditors and journalists compare
  superintendent and administrator pay across districts.
- **Compensation consultants:** they benchmark salary, increases and benefits against
  peer agreements.
- **M&A due diligence:** acquirers review executive agreements for change-of-control and
  severance obligations.

### What it contains

- **Terms stated in prose.** No value sits in a labelled box, and amounts are written
  in words and then in figures, such as a salary and a percentage increase.
- **Schedules inside sentences,** such as three longevity payments, each with its own
  trigger, in one paragraph.
- **A scan with an OCR layer** added by the scanner.
- **A side-by-side signature block** with two signers, their captions and "Dated"
  lines.
- **Handwritten dates, wet-ink signatures and two notary stamps and seals.**
