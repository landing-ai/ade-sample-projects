# Utility bill

**On the website:** [landing.ai/document-type/utility-bill](https://landing.ai/document-type/utility-bill)

A PSE&G residential electric and gas bill for May 19 to June 17, 2020, with the
customer's details replaced. It has a summary with a payment stub, a charges overview,
and a detail page for each service with the meter, readings, usage, delivery and supply
charges, a total and a usage chart.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 24 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:41 | 2026-11-19 03:57 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 13,135 | 12,273 |
| Words under 0.95 confidence | 58 | n/a |
| Words under 0.80 confidence | 21 | n/a |
| Words under 0.50 confidence | 10 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.3 s | 16.5 s |
| Per page | 1.8 s | 4.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.0 credits | 5.1 credits |
| Per page | 0.50 credits | 1.27 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:41 | 2026-11-19 03:57 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 119.2 s | 124.4 s |
| Per schema field (24) | 4.97 s | 5.18 s |
| Per value returned | 4.97 s | 5.18 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.5 credits | 3.3 credits |
| Per schema field (24) | 0.146 credits | 0.137 credits |
| Per value returned | 0.146 credits | 0.137 credits |

## Origin

`source/pseg-electric-gas-bill-redacted.pdf` is a PSE&G residential electric and gas
bill for May 19 to June 17, 2020, redacted. It is **4 pages, portrait (612×792)**, with a
full text layer: a summary with a payment stub on page 1, a charges overview on page 2,
gas details on page 3 and electric details on page 4, each detail page with a usage
chart.

| | |
|---|---|
| Publisher | PSE&G (Public Service Electric and Gas Company) |
| Source | [scribd.com/document/500641462/PSEG-Sample-Electric-Bill](https://www.scribd.com/document/500641462/PSEG-Sample-Electric-Bill) |
| Retrieved | 2026-09-27 |
| Clearance | Redacted |

Despite "Sample" in its Scribd title, this is a real customer's bill, uploaded to Scribd
by a third party. Scribd is a user-upload site, so the uploader is not the publisher,
and the bill is treated as a personal record. The local copy used is
`Use_Cases/Utility_Bills/input_folder/electric2.pdf`, **where the same bill is already
committed to this repo unredacted.** That copy is outside this folder and is not changed
here.

Nine identifiers were replaced using `document-types/scripts/redact.py`, which removes
the underlying text rather than covering it, 21 replacements across the four pages:

| What | Replaced with | Occurrences |
|---|---|---|
| Customer's name | JANE SAMPLE | 5 |
| Service address, street | 100 MAIN ST APT A | 2 |
| Service address, town, state and ZIP | ANYTOWN NJ 00000-0000 | 2 |
| Account number, spaced | 68 736 306 51 | 1 |
| Account number | 6873630651 | 5 |
| Invoice number | 183722332744 | 3 |
| Point-of-delivery ID | PE975560397498155489 | 1 |
| Electric meter number | 245603755 | 1 |
| Gas meter number | 7651211 | 1 |

**The numbers are plausible stand-ins, not zeros.** The account, invoice,
point-of-delivery and meter numbers are random numbers of the same shape from
`document-types/scripts/plausible.py`, so the bill still reads as a bill. The account
number is one stand-in printed in both its forms, spaced and unspaced. None is derived
from the original.

The PDF metadata was also cleared. PSE&G's name, logo, phone numbers and PO box, and the
bill's amounts, dates and usage, are left as printed. Some replacements are visibly
edited: the name in the page headers came out in regular weight rather than bold, and
the account number in the payment stub's scan line is Helvetica rather than the original
OCR font.

No original identifier is extractable from the committed PDF, and none appears anywhere
in this folder. The original values are deliberately not recorded here or in
`manifest.json`. The rules file used by `redact.py` stays outside the repo. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A utility bill records a household's energy use and charges, and it is one of the most
widely accepted proofs of address.

- **Banking and identity verification:** banks and fintechs accept a recent utility bill
  as proof of address when opening accounts.
- **Mortgage and consumer lending:** lenders use utility bills to confirm residence and
  recurring obligations.
- **Energy management and sustainability reporting:** companies track usage and cost
  across sites from monthly bills.
- **Utility bill auditing and payment services:** they check charges, rates and meter
  readings and pay bills on behalf of customers.
- **Government assistance programs:** energy assistance caseworkers verify the account,
  the service address and the amount owed.

### What it contains

- **Two services on one bill,** each with its own detail page, meter, readings, usage,
  delivery and supply charges, and total.
- **The same identifier everywhere.** The account number is printed six times in two
  formats across all four pages.
- **Charges in a dotted leader list,** with each amount at the right end of a dotted
  line and subtotals in bold.
- **A total printed on a shaded bar** directly above a usage bar chart.
- **Usage bar charts** on each detail page.
- **A payment stub** with a machine-readable scan line.
