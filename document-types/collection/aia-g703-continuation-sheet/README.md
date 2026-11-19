# AIA G703 continuation sheet

**On the website:** [landing.ai/document-type/aia-g703-continuation-sheet](https://landing.ai/document-type/aia-g703-continuation-sheet)

Pay application #10 for the remodel of the City of Lake Elmo, MN City Hall, Fire
Department and Washington County Sheriff Substation, for the period ending October 31,
2022. Page 1 is a G702-style application and certificate for payment. Page 2 is the
G703-style continuation sheet: a 32-line schedule of values with change orders, work
completed, balance to finish and retainage for each line.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 35 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:25 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 10,751 | 10,988 |
| Words under 0.95 confidence | 29 | n/a |
| Words under 0.80 confidence | 8 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 20.8 s | 30.0 s |
| Per page | 10.4 s | 15.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.4 credits | 3.8 credits |
| Per page | 0.70 credits | 1.90 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:26 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 35 | 35 |
| Non-null fields returned | 35 | 35 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 88.1 s | 59.3 s |
| Per schema field (35) | 2.52 s | 1.69 s |
| Per value returned | 0.23 s | 0.16 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 14.6 credits | 14.6 credits |
| Per schema field (35) | 0.417 credits | 0.417 credits |
| Per value returned | 0.039 credits | 0.039 credits |

## Origin

`source/aia-g703-lake-elmo-pay-application-10-redacted.pdf` is pay application #10 on
the City of Lake Elmo, MN City Hall, Fire Department and Washington County Sheriff
Substation remodel, for the period ending October 31, 2022. Page 1 is the **G702-style
application and certificate for payment**. Page 2 is the overall **G703-style
continuation sheet**, the schedule of values the G702 summarizes. It is **2 pages,
landscape**, with a text layer. The city's construction manager, Hoffmann + Uhlhorn
Construction, Inc., prepared it.

| | |
|---|---|
| Publisher | City of Lake Elmo, MN (council packet); pay application by Hoffmann + Uhlhorn Construction, Inc. |
| Source | [miweblink.metro-inet.us … 03 - City Center Pay Request.pdf](https://miweblink.metro-inet.us/LakeElmoPublic/0/edoc/444946/03%20-%20City%20Center%20Pay%20Request.pdf) |
| Retrieved | 2026-10-14 |
| Clearance | Redacted |

The file is a consent item from the city council's November 15, 2022 packet, posted on
the city's public Laserfiche WebLink records portal. It was downloaded directly. The
90-page packet was trimmed to its pages 2–3. Page 1 is a staff report, and pages 4–90
are a second G702/G703 pair, invoices, subcontractor pay applications, insurance
certificates and emails.

**Redaction.** The G703 carries no personal data. The G702 carried three signature
images (construction manager, architect, notary) and a notary stamp image bearing the
notary's name and commission expiry. All four images were deleted from the file rather
than covered, and the typed commission-expiry date was replaced with `30-Jun-25`.
Stand-in signatures in a handwriting font ("J. Sample", "A. Example", "N. Public") were
drawn where the three signatures were. Every page carried a `/Rotate 90` flag, which was
folded into the page content before redaction. Document metadata was cleared. No removed
image or original string remains in the committed PDF.

**Licensing.** AIA's terms forbid posting completed AIA documents for marketing without
a licence. This sheet is the contractor's own spreadsheet edition of the G703 layout
("H+U CONSTRUCTION EDITION OF AIA DOCUMENT G703") with no AIA copyright notice. The
operator chose it knowing that, on 2026-10-14.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A G702 and G703 pair is how a contractor bills for construction work each month. The
G703 lists every line of the contract's schedule of values, and the G702 totals it into
the amount due.

- **Project owners and public agencies:** they approve each pay application before
  paying it, as the Lake Elmo city council did here.
- **Architects and construction managers:** they certify that the work billed matches
  the work in place.
- **Construction lenders:** they fund loan draws against the percent complete on each
  line.
- **Sureties:** they track billing and retainage on bonded jobs.
- **General contractors and subcontractors:** they prepare the applications and
  reconcile them against change orders and payments received.

### What it contains

- **A 10-column, 32-row schedule of values** on a landscape page, keyed by CSI division
  codes (`#0330`, `#2300`) mixed with free-text item numbers (`Insurance`, `Reimburse`,
  `Contingency`).
- **Change orders and negative amounts,** with deductions printed in parentheses.
- **Arithmetic that can be checked.** Revised value, total completed, balance and 5%
  retainage per line, a totals row, and a summary page whose lines must agree with the
  schedule.
- **A non-standard edition.** The column letters differ from AIA's own G703, and the
  header misnames the G702 as "G723".
- **A certificate page with signature blocks** for the construction manager, the
  architect and a notary, here carrying stand-in signatures.
