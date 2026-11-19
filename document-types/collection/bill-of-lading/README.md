# Bill of Lading

**On the website:** [landing.ai/document-type/bill-of-lading](https://landing.ai/document-type/bill-of-lading)

A COSCO Container Lines bill of lading issued at Beihai, China on 23 May 2011 for one
40-foot container of optical drives shipped to New York, with Buffalo as the place of
delivery. It names the shipper, consignee and notify party, the vessel and voyage, the
ports, the container and seal, and the cargo's packages and weight. A rider page carries
the totals and the freight terms.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 34 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:33 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 4,467 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 8.4 s |
| Per page | 4.2 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 2.2 credits |
| Per page | 1.10 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:33 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 34 |
| Non-null fields returned | 27 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 221.1 s |
| Per schema field (34) | 6.50 s |
| Per value returned | 8.19 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 2.2 credits |
| Per schema field (34) | 0.065 credits |
| Per value returned | 0.081 credits |

## Origin

`source/bill-of-lading.pdf` is a COSCO Container Lines port to port or combined
transport bill of lading, B/L COSU6030603280, issued at Beihai on 23 May 2011 for one
40-foot container of optical drives (802 cartons, 7,304.59 kg) shipped from Beihai,
China to New York, with Buffalo as the place of delivery. It is **2 pages, portrait,
scanned**: the B/L face and its rider ("PAGE: 2 OF 2"), which carries the totals and
"OCEAN FREIGHT PREPAID". It is an office-copier scan with no text layer.

| | |
|---|---|
| Publisher | U.S. District Court for the Southern District of New York case record (*Fubon Ins. Co. Ltd. v. OHL International*), served by the CourtListener RECAP archive. The B/L was issued by COSCO Container Lines Co., Ltd. |
| Source | [storage.courtlistener.com/…/gov.uscourts.nysd.398603.46.7.pdf](https://storage.courtlistener.com/recap/gov.uscourts.nysd.398603/gov.uscourts.nysd.398603.46.7.pdf), pages 2–3 of 21 |
| Retrieved | 2026-10-03, by script |
| Clearance | **Redacted**, see below |

The filing is ECF 46-7, an exhibit to a Rule 56.1 statement, where the B/L appears as
deposition Exhibit 8. Page 1 of the filing is an exhibit slip sheet; pages 4 onward are
COSCO's printed B/L terms and an unrelated service contract. Only the B/L is kept.

This replaces an earlier candidate that was rejected as fabricated. Checks on this one:
container CBHU1842324 passes the ISO 6346 check digit, CBHU is COSCO's own owner prefix,
and the file was produced by a Canon copier as part of a court filing.

Every party on the B/L (shipper, consignee, notify party, carrier) is a company, and the
telephone and fax numbers are business lines. **The bill of lading itself was not
altered.** The one change is the court reporter's deposition exhibit sticker, stamped
into the empty Freight & Charges Payable box. It carried a witness's handwritten
surname, the exhibit number, the deposition date and the reporter's initials. It was
painted out with the page's own background, and nothing was drawn in its place: the box
is blank, as it was when COSCO issued the B/L. Because the page was changed, clearance
is `redacted`, with the sticker recorded as the only redaction.

Each page was rebuilt from a 300 dpi render of the edited image, so the original raster
is not carried into the output. The PDF's metadata (the copier's and iText's producer
strings and the filing dates) was cleared. OCR of the output and a sweep of every file
in this folder found no trace of the sticker's surname. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A bill of lading is the carrier's receipt for cargo, the contract of carriage and, in
its negotiable form, the title document for the goods. It travels with every ocean
shipment.

- **Freight forwarders and NVOCCs:** they match B/Ls to bookings and invoices and pass
  the details to the next party in the chain.
- **Customs brokers:** they use the B/L number, ports, container and cargo description
  to file import entries.
- **Banks and trade finance:** under letters of credit, banks check the B/L against the
  credit's terms before they pay.
- **Cargo insurers and claims handlers:** they rely on the B/L to establish what was
  shipped, by whom and in what condition, as in the court case this copy comes from.
- **Importers and logistics teams:** they track containers and plan delivery from the
  vessel, voyage and place of delivery.

### What it contains

- **A dense ruled form** with numbered boxes whose labels sit in the same cells as their
  values.
- **Monospaced typed entries,** including a free-text marks column.
- **A continuation rider** that repeats the header values on page 2.
- **Boxes left blank on purpose,** such as the booking number, declared value and
  freight amounts.
- **A seal number that runs over a column rule** into the next column.
- **A copier scan with no text layer,** so every value has to be read from the page
  image.
