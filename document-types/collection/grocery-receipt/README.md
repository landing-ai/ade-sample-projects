# Grocery Receipt

A Costco Wholesale receipt from the Greenville, SC warehouse, dated March 31, 2019. It covers three
items, a $0.00 tax line, a $38.48 total and a chip-read card payment. It is a **phone photo, not a
scan**: the paper is creased and slightly curled, lit unevenly with a shadow across the top half,
and photographed on a granite counter. The source is one portrait page.

## Provenance

| | |
|---|---|
| Publisher | Apartment Therapy Media (The Kitchn), as an editorial image |
| Source URL | https://cdn.apartmenttherapy.info/image/upload/f_auto,q_auto:eco,c_fit,w_730,h_974/k%2Farchive%2Fadc09d0a4189a5d96ed835ac0633656decdcf991 |
| Retrieved | 2026-11-15 |
| Clearance | `redacted` |

The image was downloaded by script from the publisher's CDN as a 730×973 JPEG and wrapped in a
one-page PDF, with no text layer and no metadata. The publisher printed the photo but the receipt
belongs to a shopper, so it was treated as a personal record.

### What was replaced

| What | Replaced with |
|---|---|
| Costco membership number (12 digits) | A randomly generated 12-digit stand-in |
| Last four digits of the masked card number | A randomly generated 4-digit stand-in |

Both were replaced in the pixels before the document was parsed. Each was painted over with
paper colour blended from either side of it, so the patch follows the photo's lighting rather
than showing as a flat box. The stand-in was then redrawn in Arial Narrow at the original's size
and ink colour. The PDF is built from the edited image alone.

Tesseract OCR of the output finds neither original, as text or inside any run of digits.

These were kept: the store address, item numbers and transaction references (sequence,
approval code, transaction and merchant IDs). They belong to the retailer and the transaction,
not to the shopper.

## Why this document

Every other document in the collection is a born-digital PDF or a flat scan. This one is a photo
of thermal paper, the way receipts actually reach expense and loyalty systems. It also has some
receipt-specific notation:

- item numbers fused to descriptions
- a tax-code letter printed twice, beside the price and again in the left margin
- a total printed inside an inverted black bar

## Schema

The request asked for a list of every item purchased, with name, quantity, unit price, total
price and taxable status. The `items` array has all five, plus the item number and the printed
tax-code letter. The rest of the schema covers the store, the date and time, the totals and the
card payment. It has 33 leaf fields.

**Quantity and unit price are not printed on this receipt.** Each item is a single unit.
Extraction fills `quantity` as 1 and `unit_price` as the line total, as the schema instructs,
and both ground to the item's line.

**`taxable` is derived from the "E" flag, not read from the page.** It comes back `false` for all
three items, consistent with the $0.00 tax line. Because it is an inference, its range points at
the "E" that supports it, and it grounds `OFF`.

## Featured fields (page 1)

| Field | Value |
|---|---|
| Item | GRAPE TOMATO |
| Item price | 5.99 |
| Tax flag | E |
| Tax | 0.00 |
| Total | 38.48 |

The fields follow one item line across the receipt: its description, its price, and the "E" in
the left margin. Then the 0.00 tax line the flag explains, and the total.

## Grounding on this document

Grounding is better than the photo would suggest. Every printed value grounds `ok` to its own
line, even in the shadowed top half. That includes the item, payment and date lines, and the
replaced card digits ("XXXXXXXXXXXX2398").

- **Item number and description share a box.** "77053 GRAPE TOMATO" is one line of type, so they
  share one box.
- **The price and its trailing flag share a box.** The "E" after the price is in the same box as
  the price ("5.99 E"). The margin "E" gets a box of its own.
- **The inverted total is still found.** The total grounds to the inverted black bar, and the
  crop shows the white digits inside it. `build_images.py` warns that OCR cannot read 5.99 and
  38.48 in their boxes. That is the photo's lighting and the inverted bar, not a misplaced box;
  every crop was opened and checked.
- **The address grounds `OFF`.** It spans two lines, and neither line contains the whole value.

## Credits

1.70 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py grocery-receipt
.venv/bin/python document-types/scripts/inspect_fields.py grocery-receipt --page 1
.venv/bin/python document-types/scripts/build_images.py grocery-receipt
```
