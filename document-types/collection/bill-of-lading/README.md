# Bill of Lading

Source assets for `landing.ai/document-type/bill-of-lading`.

## Sample document

`source/bill-of-lading.pdf`: a COSCO Container Lines port to port or combined transport
bill of lading, B/L COSU6030603280, issued at Beihai on 23 May 2011 for one 40-foot
container of optical drives (802 cartons, 7,304.59 kg) shipped from Beihai, China to New
York, with Buffalo as the place of delivery. **2 pages, portrait, scanned**: the B/L face
and its rider ("PAGE: 2 OF 2"), which carries the totals and "OCEAN FREIGHT PREPAID". It
is an office-copier scan with no text layer.

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

## Redaction

Every party on the B/L (shipper, consignee, notify party, carrier) is a company, and
the telephone and fax numbers are business lines. **The bill of lading itself was not
altered.**

The one change is the court reporter's deposition exhibit sticker, stamped into the
empty Freight & Charges Payable box. It carried a witness's handwritten surname, the
exhibit number, the deposition date and the reporter's initials. It was painted out
with the page's own background using `document-types/scripts/redact_scan.py --erase`,
and nothing was drawn in its place: the box is blank, as it was when COSCO issued the
B/L. Because the page was changed, clearance is `redacted`, with the sticker recorded as
the only redaction.

`redact_scan.py` rebuilds each page from a 300 dpi render of the edited image, so the
original raster is not carried into the output. The PDF's metadata (the copier's and
iText's producer strings and the filing dates) was cleared with
`document-types/scripts/pdfmeta.py`. Verified by OCR of the output; a sweep of every file
in this folder found no trace of the sticker's surname.

## Why this document

A genuine carrier-issued B/L, not a template or a mock-up: a dense ruled form with
monospaced typed entries, numbered boxes whose labels sit inside the same cells as their
values, a free-text marks column, a continuation rider that repeats the header values,
and copier noise. It also has the fields a real B/L leaves blank (booking number,
declared value, freight amounts), which tests whether extraction leaves them blank too.

`schema.json` is the team's ocean bill of lading schema, used unchanged: **34 leaf
fields** (counted from the schema).

## Featured fields: which box, on which ship, from where to where

All on page 1.

| Field | Value |
|---|---|
| B/L number | COSU6030603280 |
| Vessel | HUI JIN QIAO 181 |
| Port of loading | BEIHAI, CHINA |
| Port of discharge | NEW YORK, NY |
| Container number | CBHU1842324 |

The B/L number and vessel are pinned to occurrence 0, the B/L face; both repeat in the
rider's header on page 2. The voyage (008S) is correct but shares the vessel's cell, so
it would repeat that crop. Gross weight (7304.590KGS) is correct and grounds cleanly; it
was left out to keep to five.

## Grounding and extraction on this document

- **Clean on the ruled boxes.** Every numbered box grounds to its own cell, and every
  crop above contains its value.
- **The overstruck seal number splits.** The seal's last digits run over the column
  rule, and the parse cut it there: `W9300` in the marks column, `05` in the packages
  column. The container crop shows the full container number followed by the seal cut
  at the rule. `containers[0].marks_and_numbers` begins with `W9300`, so the seal fragment
  ended up in the marks.
- **Booking number is wrong.** The Booking No. box is blank, but `booking_number` came
  back `SHE11328`, the Export References and Service Contract number from the
  neighbouring boxes.
- **Dates are correct but read OFF**, as expected: `2011-05-23` against a page that
  prints `23 MAY 2011`.
- **OCR slip in the parse**: "Date Laden on Board" is read as "Dale Laden on Board". The
  extraction still found the on-board date.

### Where the team schema does not fit this B/L

- `shipper.address` is required, but the shipper box carries a name only. Null.
- `port_of_loading.country` and `port_of_discharge.country` are required. The model put
  the country into `city` (`BEIHAI, CHINA`) and returned null for both countries, with a
  `nonconformant_output` warning on the discharge country. The page prints no country
  for New York at all.
- `freight_charges` is empty: the charge rows are blank on the face, and the rider's
  "OCEAN FREIGHT PREPAID" was not captured as a charge.
- `declared_value` and `freight_payable_at` are empty strings, as they are on the page.

## Credits

4.60 credits for parse and extract, at the standard tier.

## Regenerate

```bash
# From a copy of the source filing (pages 2-3), outside the repo:
.venv/bin/python document-types/scripts/redact_scan.py original.pdf \
    document-types/collection/bill-of-lading/source/bill-of-lading.pdf \
    --rules <outside-the-repo>/rules.json --pages 2 3 --erase "2:471,537,590,614"

.venv/bin/python document-types/scripts/run_ade.py bill-of-lading
.venv/bin/python document-types/scripts/build_images.py bill-of-lading
```

`run_ade.py --extract-only` re-runs extraction against the committed parse.
