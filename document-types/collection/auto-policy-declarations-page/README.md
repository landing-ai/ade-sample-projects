# Auto Policy Declarations Page

**On the website:** [landing.ai/document-type/auto-policy-declarations-page](https://landing.ai/document-type/auto-policy-declarations-page)

National Indemnity Company's Business Auto Coverage Declarations for a limousine and
party-bus operator in Aliquippa, Pennsylvania, for the policy period 10/01/2019 to
10/01/2020. It names the insured, the insurer and the agencies, and schedules each
coverage with its covered-auto symbols, limit and premium, followed by the premium
totals and the forms and endorsements that apply.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 24 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:30 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 3,861 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 7.0 s |
| Per page | 7.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.5 credits |
| Per page | 1.50 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:31 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 24 |
| Non-null fields returned | 22 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 309.4 s |
| Per schema field (24) | 12.89 s |
| Per value returned | 5.95 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 3.2 credits |
| Per schema field (24) | 0.133 credits |
| Per value returned | 0.062 credits |

## Origin

`source/national-indemnity-business-auto-declarations.pdf` is National Indemnity
Company's **Business Auto Coverage Declarations** for an LLC limousine and party-bus
operator in Aliquippa, Pennsylvania, policy period 10/01/2019 to 10/01/2020. It is
**1 page, portrait**, a slightly skewed scan with an OCR text layer.

| | |
|---|---|
| Publisher | Pennsylvania Public Utility Commission public filings repository; the declarations were issued by National Indemnity Company |
| Source | [puc.pa.gov/pcdocs/1644171.pdf](https://www.puc.pa.gov/pcdocs/1644171.pdf) |
| Retrieved | 2026-10-25, downloaded by script |
| Clearance | Public |

The filing is a motor carrier's proof of insurance, posted by the PA PUC in its public
document repository. The original is four pages: the filer's cover letter, this
declarations page, a Form E certificate of insurance and a date-stamped mailing
envelope. **Only the declarations page was kept.** Pages 1, 3 and 4 were dropped without
being reviewed for individual names.

**No page text was redacted.** The kept page names only organizations: the insured LLC at
its business address, the insurer, the producing agency and the countersigning agency.
The two signatures at the foot are the insurer's pre-printed facsimile officer signatures
(Secretary and President). They carry no printed name and appear on every policy of this
form, so they were left in place, as on the other insurer forms in this collection. The
authorized-signature line is blank. The PDF's metadata (format and dates) was cleared.

This is a **commercial** (business auto) declarations page, not a personal auto one. No
plain, specimen-filled personal auto declarations page could be found; the candidates
were annotated consumer-guide specimens, which were rejected. The layout and vocabulary
(covered-auto symbols, CSL limits, UM/UIM, comprehensive and collision) are the same ones
a personal auto declarations page uses. Item Three, the schedule of covered autos, reads
**AS ATTACHED** and is not in the filing, so the sample has no vehicle rows.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

The declarations page is the one page of an auto policy that every downstream process
reads: who is insured, by whom, for how long, and which coverages were bought at what
limit and price.

- **Transportation regulators:** state utility commissions and other regulators check
  that motor carriers hold the required liability limits, as the PA PUC filing here
  shows.
- **Insurance carriers and brokers:** underwriters and account managers read prior
  declarations at renewal and when quoting a competing policy.
- **Fleet operators and their customers:** shippers, venues and contracting parties
  confirm a carrier's coverage before hiring it.
- **Auto lenders and lessors:** they confirm that financed vehicles carry the required
  physical-damage coverage.
- **Claims departments:** adjusters check which coverages and limits were in force on
  the date of loss.

### What it contains

- **A dense ruled coverage schedule** with columns for coverage, covered-auto symbols,
  limit and premium.
- **Mostly empty rows.** Many coverage rows are blank or carry a preprinted `$` with no
  amount.
- **Limits that are references,** such as "See M 3912b (08/2001)" or `INCL`, in place of
  a number.
- **Coverage names that wrap** onto a second line inside their cells.
- **An unlabeled policy number** that sits beside a CROSS REFERENCE NUMBER caption.
- **Facsimile officer signatures** at the foot of the page.
- **A skewed scan** with an OCR text layer.
