# Vehicle Title

**On the website:** [landing.ai/document-type/vehicle-title](https://landing.ai/document-type/vehicle-title)

A completed Commonwealth of Virginia Certificate of Title for a Vehicle (DMV form VSA3L)
for a 2017 Ford pickup, front and back. The face gives the vehicle description, title
number and issue date, the owner, the lienholder with a signed lien release, and the
owner's assignment of title to a buying dealer. The back records the dealer's
reassignment to a buyer in Mexico, with blank reassignment and application sections
below.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 37 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:59 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 12,822 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 21.1 s |
| Per page | 10.5 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 4.3 credits |
| Per page | 2.15 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 04:00 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 37 |
| Non-null fields returned | 37 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 89.3 s |
| Per schema field (37) | 2.41 s |
| Per value returned | 2.03 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 4.1 credits |
| Per schema field (37) | 0.111 credits |
| Per value returned | 0.093 credits |

## Origin

`source/vehicle-title.pdf` is a completed Commonwealth of Virginia *Certificate of Title
for a Vehicle* (DMV form VSA3L, rev. 6/15) for a 2017 Ford pickup, front and back. It is
**2 pages, portrait**, a raster scan.

- **Page 1, the face.** Vehicle description, title number and issue date, owner (a
  dealership), lienholder (a bank) with a signed lien release, a FOR EXPORT ONLY dealer
  stamp, and section A, the owner's assignment of title to a buying dealer.
- **Page 2, the back.** Dealer reassignment B, completed to an individual buyer in
  Mexico, blank reassignments C and D, and the blank application sections E to H. The
  export stamp is repeated across the page.

| | |
|---|---|
| Publisher | Virginia Department of Motor Vehicles (the form). The completed copy was uploaded to Scribd by an unknown account. |
| Source | https://www.scribd.com/document/939332148/TITLE |
| Retrieved | 2026-10-26. The operator downloaded it by hand, because Scribd blocks scripted downloads. |
| Clearance | Redacted |

**Provenance caveat.** This request was **rejected on 2026-10-03** because the file then
looked digitally fabricated: a vector-only "Print To PDF" file, with an edited control
number and misspelled form text. The operator lifted the rejection and downloaded the
file again on 2026-10-26.

**The file received on 2026-10-26 does not match that description.** It is a raster scan
of both sides of a paper title, with an invisible OCR text layer and Kodak Alaris
scanner software in its metadata. It carries handwriting, ink signatures, rubber stamps
and a dealer's barcode label. No misspelled form text was found. Whether Scribd now
serves a different file, or the earlier description was wrong, could not be established.

Even so, nothing in a scan proves a title is genuine. **This is not presented as a
verified real title.** It is used as a realistic sample of the form, after redaction.

**Redaction.** Scribd is a user-upload site, not the publisher, so the document was
treated as a real record. These were replaced:

| What | Replaced with | Count |
|---|---|---|
| VIN (VIN box, and its last eight characters on the barcode label) | `1FTEW1E86HFB56934`. The original's make, model, engine, year and plant characters were kept, a random serial was drawn, and the check digit was recomputed, so the stand-in is a valid VIN. | 2 |
| Title number | `9440212714`, randomly drawn | 1 |
| Security control number ("This is not a title number") | `G18063942`, randomly drawn | 1 |
| Other Pertinent Data value | `755630`, randomly drawn | 1 |
| Dealer stock number (handwritten at the top, printed on the label) | `726772`, randomly drawn | 2 |
| Name of the bank's attorney in fact under the lien release | `Jane Doe` | 1 |
| Name of the selling dealership's agent, section A | `JANE Q SAMPLE` | 1 |
| Handwritten printed name of the buyer's signer in section A, and of the individual buyer in section B | `John Sample`, `John Q Sample`, in a handwriting font | 2 |
| Section B buyer's handwritten street address and postal code | `100 Main St` and `51607`, in a handwriting font. The city and country were kept. | 2 |
| Five signatures (lien release, seller and buyer in A, buyer and dealer in B) | Initials or `J Doe` in a handwriting font | 5 |
| PDF417 barcode on the face, linear barcode on the label, vertical barcode at the edge | Erased to blank paper. They encode title and vehicle data. | 3 |

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. The businesses were kept: the two dealerships, the bank lienholder and their
addresses, and the dealer licence number on the export stamp. Dates, weights, odometer
readings and sales tax were kept as well.

Typed values were replaced in Courier New Bold, to match the title printer, and the rest
in Arial or the handwriting font. Signatures, handwriting and barcodes were erased, and
the rule lines the erasing cut were redrawn. Both pages were rebuilt from 300 dpi renders
of the edited images, so neither the original rasters nor the original OCR layer is in
the output. The PDF's metadata is empty.

The redaction shows on close inspection. The erased PDF417 barcode leaves a plain
rectangle in the security background, and the stand-in signatures sit on white patches.
A few unidentifiable fragments of the original scrawls remain, such as a loop across the
"Dealer(s) Signature" caption on page 2. The output was verified by OCR of every
original, by eye on 110 to 300 dpi renders, and by a sweep of every file in this folder.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A vehicle title is the legal record of who owns a vehicle and who holds a lien on it.
Real ones are almost never published, but they pass through many hands at each sale.

- **Auto lenders:** they record their lien on the title and release it when the loan is
  paid off.
- **Dealers and floor-plan lenders:** dealers take titles in on trade and reassign
  them, and floor-plan lenders hold them as collateral.
- **State motor vehicle agencies:** they issue new titles from assigned ones.
- **Auto insurers:** total-loss and salvage claims require the title to transfer
  ownership.
- **Vehicle exporters and customs brokers:** export shipments need the title, as the
  FOR EXPORT ONLY stamp here shows.

### What it contains

- **A security-printed background,** with guilloche borders, a patterned field and
  repeated "VOID" lettering behind every value.
- **Typed, handwritten and stamped values on one page.** The face is printed in a
  monospaced face, the transfer sections are handwritten, and a diagonal rubber stamp
  crosses the lien release and the back's sections.
- **Two identifiers that look alike:** the title number and a red control number
  labeled "This is not a title number".
- **A chain of transfers,** from owner to dealer on the face and dealer to buyer on the
  back, with blank reassignments below.
- **Signatures and checkboxes** in the assignment and reassignment sections.
- **A raster scan** with an invisible OCR text layer.
