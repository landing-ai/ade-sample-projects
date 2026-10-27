# Vehicle Title

Source assets for `landing.ai/document-type/vehicle-title`.

## Sample document

`source/vehicle-title.pdf`: a completed Commonwealth of Virginia *Certificate of Title
for a Vehicle* (DMV form VSA3L, rev. 6/15) for a 2017 Ford pickup, front and back.
**2 pages, portrait, raster scan.**

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
| Clearance | **Redacted**, see below |

## Provenance caveat

This request was **rejected on 2026-10-03** because the file then looked digitally
fabricated: a vector-only "Print To PDF" file, with an edited control number and
misspelled form text. The operator lifted the rejection and downloaded the file again on
2026-10-26.

**The file received on 2026-10-26 does not match that description.** It is a raster scan
of both sides of a paper title, with an invisible OCR text layer and Kodak Alaris
scanner software in its metadata. It carries handwriting, ink signatures, rubber stamps
and a dealer's barcode label. No misspelled form text was found. Whether Scribd now
serves a different file, or the earlier description was wrong, could not be established.

Even so, nothing in a scan proves a title is genuine. **This is not presented as a
verified real title.** It is used as a realistic sample of the form, after redaction.

## Redaction

Scribd is a user-upload site, not the publisher, so the document was treated as a real
record. Before anything was parsed, these were replaced:

| What | Replaced with | Count |
|---|---|---|
| VIN (VIN box, and its last eight characters on the barcode label) | `1FTEW1E86HFB56934`. The original's make, model, engine, year and plant characters were kept, a random serial was drawn, and the check digit was recomputed, so the stand-in is a valid VIN. | 2 |
| Title number | `9440212714`, drawn by `plausible.py` | 1 |
| Security control number ("This is not a title number") | `G18063942`, `plausible.py` | 1 |
| Other Pertinent Data value | `755630`, `plausible.py` | 1 |
| Dealer stock number (handwritten at the top, printed on the label) | `726772`, `plausible.py` | 2 |
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

The redaction used `document-types/scripts/redact_scan.py`, unmodified, in two passes.
The first pass replaced the typed VIN, title number and Other Pertinent Data in Courier
New Bold, to match the title printer. The second replaced everything else in Arial or
the handwriting font. OCR could not read the VIN, the title number, the red control
number, the printed agent name or the label, so those were placed with `--place`.
Signatures, handwriting and barcodes were erased with `--erase`, and the rule lines the
erasing cut were redrawn. Both pages were rebuilt from 300 dpi renders of the edited
images, so neither the original rasters nor the original OCR layer is in the output.
The PDF's metadata is empty.

The redaction shows on close inspection. The erased PDF417 barcode leaves a plain
rectangle in the security background, and the stand-in signatures sit on white patches.
A few unidentifiable fragments of the original scrawls remain, such as a loop across the
"Dealer(s) Signature" caption on page 2.

The output was verified by `redact_scan.py`'s OCR check of every original, by eye on 110
to 300 dpi renders, and by `ship.py check --rules` over every file in this folder.

## Why this document

A title is the core document in auto lending, insurance, dealer floor-plan and export
work, and real ones are almost never published. This one tests things that the clean
forms in the collection do not:

- **A security-printed background.** Guilloche borders, a patterned field and repeated
  "VOID" lettering sit behind every value.
- **Typed, handwritten and stamped values on one page.** The face is printed by the DMV
  in a monospaced face. The transfer sections are handwritten. A dealer's diagonal
  rubber stamp crosses the lien release and, on the back, the reassignment and
  application sections.
- **Two numbers that look alike.** The title number and the red control number labelled
  "This is not a title number" are both long identifiers near the top right.
- **A chain of transfers.** The owner assigns to a dealer on the face, and the dealer
  reassigns on the back, with blank reassignments below.

## Featured fields

Page 1 features the vehicle-identity row and the title record: **VIN, model year, make,
title number and date issued.** These are what a lender, insurer or buyer checks first.
All are in typed print in one ruled band, and each grounds to its own cell. Extraction
kept the title number and the control number apart. The handwritten transfer fields
were not featured, because several came back wrong (see below).

## Grounding and extraction notes

- **The typed face is extracted correctly.** All nine vehicle fields, the title and
  control numbers, the dates, the sales tax, the owner, the lienholder and the odometer
  brand are right, and the featured fields ground to their own cells.
- **Handwriting is where it slips.** The section A odometer reading, written `17126`
  with a stroke between the digits, came back as `171126` in both transfers. The
  section A date of sale `1-7-25` came back as `1-7-2`. The ZIP `78521` came back as
  `785.21`, and Matamoros as "Matamurus". The handwritten lien release date is hard to
  read even by eye, and came back as `11/26/14`.
- **Section B's dealer is missed.** The dealer's printed name ("Toasty Motor Company")
  and dealer number, both handwritten in their boxes, came back empty.
- **The stamp misleads the checkboxes.** In blank reassignment C, the parse marks "IN
  EXCESS of Mechanical Limits" as checked where the stamp crosses the box.
- **One hallucination.** In the row under the section A buyer's printed name, the
  parse emits a short Arabic-script string and `[ILLEGIBLE_TEXT]`, where the page has
  only faint fragments left from the original handwriting. It does not reach the
  extraction.
- `build_images.py` warned that OCR could not read the year, make and date issued in
  their boxes, probably because of the patterned background. All three crops were
  checked by eye, and each box sits on its value.
- The schema has 37 leaf fields. Extraction populated all 18 top-level fields.

## Credits

8.70 credits for parse and extract, at standard tier.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py vehicle-title     # spends credits
.venv/bin/python document-types/scripts/build_images.py vehicle-title
.venv/bin/python document-types/scripts/inspect_fields.py vehicle-title
```

The redaction is not reproducible from this folder by design, because its rules file
holds the originals.
