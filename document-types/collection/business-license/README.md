# Business license

**On the website:** [landing.ai/document-type/business-license](https://landing.ai/document-type/business-license)

A specimen Broward County Local Business Tax Receipt, the form a Florida business shows
as its business license, valid October 1, 2019 through September 30, 2020. It gives the
business name, owner, location and type, the receipt number, a row of counts such as
employees, and the tax and total paid.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 32 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:44 | 2026-11-19 02:34 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 1,680 | 1,847 |
| Words under 0.95 confidence | 21 | n/a |
| Words under 0.80 confidence | 9 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.1 s | 5.6 s |
| Per page | 4.1 s | 5.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.4 credits | 1.0 credits |
| Per page | 0.40 credits | 1.00 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:44 | 2026-11-19 02:34 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 32 | 32 |
| Non-null fields returned | 26 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 130.8 s | 309.5 s |
| Per schema field (32) | 4.09 s | 9.67 s |
| Per value returned | 5.03 s | 11.91 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.4 credits | 1.4 credits |
| Per schema field (32) | 0.044 credits | 0.044 credits |
| Per value returned | 0.054 credits | 0.054 credits |

## Origin

`source/broward-county-local-business-tax-receipt-sample.pdf` is a specimen Broward
County Local Business Tax Receipt, valid October 1, 2019 through September 30, 2020. It
is **1 page, landscape**, a single raster image. The only text layer is the red "This is
a sample of a local business tax receipt" banner added by the publisher.

Florida has no general business license. Its counties and cities issue a Local Business
Tax Receipt instead, which is what a Florida business shows when asked for its business
license. The receipt says so itself: the tax "is non-regulatory in nature" and the
receipt "does not indicate that the business is legal".

| | |
|---|---|
| Publisher | Broward County (receipt format); published as a sample by the Florida State Minority Supplier Development Council |
| Source | [fsmsdc.org/…/8-Broward-county-Generic.pdf](https://fsmsdc.org/wp-content/uploads/2023/02/8-Broward-county-Generic.pdf) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

The Florida State Minority Supplier Development Council publishes this file in the
sample documents library on its certification pages, which carries a disclaimer for its
sample documents. It is a specimen filled with placeholder data (Generic Business LLC,
owner Juan B Generic, 123 Fourth St), not a real business, and the publisher's banner
crosses the page. The business phone is the well-known 867-5309 placeholder. No
redaction was needed. The PDF metadata holds only the Acrobat creator, producer and
dates. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A business license or local business tax receipt shows that a business is registered
to operate in a city or county. It is a routine item in any request to verify a
business.

- **Banking and KYB onboarding:** banks and payment processors collect it to confirm a
  business's name, location and that it operates locally.
- **Small-business and SBA lending:** lenders ask for it to show how long the business
  has operated and where.
- **Supplier certification and procurement:** minority and small-business certification
  programs, like the publisher's here, and government buyers require it from vendors.
- **Commercial insurance:** underwriters use it to confirm the business type and
  location.
- **Landlords and property managers:** commercial tenants show it when they lease space.

### What it contains

- **A raster image with no text layer** under the receipt, so everything is read from
  the page image.
- **Labels and values in different typefaces.** Bold sans-serif labels, monospaced typed
  values, sometimes on a different baseline from their label.
- **A sparse row of counts:** Rooms, Seats, Employees, Machines and Professionals, with
  only Employees filled.
- **A fee table** with a "For Vending Business Only" header spanning five columns.
- **A disclaimer paragraph** that says the receipt is not a regulatory license.
- **A red SAMPLE banner** printed across the page.
