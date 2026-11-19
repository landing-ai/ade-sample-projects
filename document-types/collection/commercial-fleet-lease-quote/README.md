# Commercial Fleet Lease Quote

**On the website:** [landing.ai/document-type/commercial-fleet-lease-quote](https://landing.ai/document-type/commercial-fleet-lease-quote)

Seven Enterprise Fleet Management open-end lease rate quotes prepared for Hidalgo
County, Texas, in May 2019, one per vehicle for the county's fleet. Each prices a
60-month lease: capitalized cost, depreciation reserve, monthly lease charge,
maintenance program, total monthly rental and the reduced book value at the end of the
term, followed by the vehicle's pricing summary, options and configured features.

| | |
|---|---|
| Pages | 32 |
| Fields in the extraction schema | 33 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:41 | 2026-11-19 02:43 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 97,065 | 104,826 |
| Words under 0.95 confidence | 210 | n/a |
| Words under 0.80 confidence | 57 | n/a |
| Words under 0.50 confidence | 10 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 25.1 s | 44.4 s |
| Per page | 0.8 s | 1.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 14.6 credits | 42.3 credits |
| Per page | 0.46 credits | 1.32 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:41 | 2026-11-19 02:44 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 33 | 33 |
| Non-null fields returned | 35 | 33 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 235.7 s | 548.6 s |
| Per schema field (33) | 7.14 s | 16.62 s |
| Per value returned | 1.05 s | 2.58 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 26.9 credits | 28.0 credits |
| Per schema field (33) | 0.815 credits | 0.848 credits |
| Per value returned | 0.120 credits | 0.131 credits |

## Origin

`source/enterprise-fleet-lease-rate-quotes-redacted.pdf` is a set of **Open-End (Equity)
Lease Rate Quotes** from **Enterprise Fleet Management**, with Enterprise FM Trust as
the lessor, prepared for **Hidalgo County, Texas** in May 2019. It is **32 pages,
portrait, with a text layer**. Seven quotes run back to back, of 4 to 6 pages each:

- A **rate page** (pages 1, 5, 9, 13, 17, 23, 28): a header block (vehicle, term, state,
  customer number), a long dollar column with its labels to the right, an Order
  Information box in the right-hand column, notes and an unsigned lessee line.
- Sometimes an **Other Totals** or **Aftermarket Equipment** page (24, 29).
- A **Vehicle Information** page: invoice and MSRP pricing summary, colors and a
  selected-options table.
- Two pages of **configured features**, as label/value lists.

The vehicles are two Ford F-250s, three Ford F-150s, a Chevrolet Colorado and a
Chevrolet Express 2500. Page 19 is blank apart from its footer, as in the original.

| | |
|---|---|
| Publisher | Enterprise Fleet Management / Enterprise FM Trust (lessor); posted by the Hidalgo County, Texas Commissioners Court |
| Source | [public.destinyhosted.com/hidaldocs/2019/CC/20190604_3330/70466_Quotes.pdf](https://public.destinyhosted.com/hidaldocs/2019/CC/20190604_3330/70466_Quotes.pdf) |
| Retrieved | 2026-10-25, by script |
| Clearance | Redacted |

The county published the quotes as an attachment to agenda item 70466 of its
Commissioners Court meeting of June 4, 2019, on its public agenda-publishing host. They
are part of the public meeting record.

The quotes carry no signatures (the lessee line is blank), phone numbers or addresses.
Three identifiers were replaced with `document-types/scripts/redact.py`, which removes
the underlying text rather than drawing a box over it:

| What | Replaced with | Count |
|---|---|---|
| County employee's name under Prepared For | `Sample, Jane` | 7 |
| Enterprise account representatives' initials (AE/AM) | `0AB/CD0` | 7 |
| The county's Enterprise customer number (Customer#) | A random 6-digit stand-in | 7 |

The PDF metadata, which carried an Enterprise user ID, was cleared. Quote numbers,
prices, dates and vehicle details are kept. The original values are not recorded
anywhere in this folder, and the rules file stays outside the repo. The redaction was
verified by the script's text check, by eye on renders, and by a rules check over every
file in this folder. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A fleet lease quote prices a vehicle for a business or public fleet before the lease is
signed. Fleet managers compare quotes across vehicles and lessors, and public bodies
attach them to approval records like this one.

- **Fleet management companies and lessors:** they issue quotes like these and
  reconcile them against the signed lease schedules.
- **Government procurement:** counties, cities and school districts review quotes
  before a governing body approves the lease.
- **Corporate fleet and procurement teams:** they compare monthly rental, maintenance
  and end-of-term value across vehicles and vendors.
- **Finance and accounting:** teams book lease obligations and track the reduced book
  value each vehicle carries at term.
- **Equipment and vehicle finance:** lenders and lessors use quote data to price and
  document open-end leases.

### What it contains

- **A two-column form whose values sit to the left of their labels,** so a value can
  pair with the wrong label.
- **A boxed Order Information panel** in the right-hand column, beside the dollar
  column.
- **One layout repeated seven times** with different numbers, so each quote's values
  have to stay with their own quote.
- **Subtotal and total rows** within the dollar column.
- **Pricing summary and selected-options tables** on the vehicle information pages.
- **Long label/value lists** of configured features, over two pages per quote.
- **A blank page** and an unsigned lessee line, as in the original.
