# Bid tabulation

Source assets for `landing.ai/document-type/bid-tabulation`.

## Sample document

`source/S18018-Div-B-Bid-Tab.pdf` — the bid tabulation for **Jackson Township Regional
Sewer District, Wastewater System Improvements, Division "B" - Collection System
Improvements** (Indiana), for bids received June 12, 2026. Prepared and certified by
Commonwealth Engineers, Inc., the consulting engineer of record. **4 pages, landscape**,
with a text layer: it is an Excel workbook printed to PDF.

A bid tabulation is the engineer's record of a public bid opening: every bidder's price
for every line item, set beside the Engineer's Estimate, with a checklist of the documents
each bidder submitted. Owners use it to identify the apparent low bidder and to check the
bids for irregularities before recommending an award.

| | |
|---|---|
| Publisher | Commonwealth Engineers, Inc., for the Jackson Township Regional Sewer District |
| Source | [commonwealthengineers.com/…/S18018-Div-B-Bid-Tab.pdf](https://commonwealthengineers.com/wp-content/uploads/2026/06/S18018-Div-B-Bid-Tab.pdf) |
| Retrieved | 2026-10-14, downloaded directly by script |
| Clearance | Public |

The engineer posts the tabulation on its own website, as public bid results usually are.
The bidders are companies. The only people named act in an official capacity: the staff
member who prepared the tabulation (page 1), and the certifying professional engineer,
with his Indiana P.E. registration number, signature and seal (page 4). P.E.
registrations are public record. None of them is featured. No redaction was needed. The
PDF's metadata named a staff username as author, so it was cleared. Each page footer
prints the engineer's internal file-server path, which is kept as printed.

The engineer's projects-for-bid page now lists this project as a rebid, so these bids
were probably rejected. That makes no difference to the document as a sample.

## Why this document

The collection's first **bid tabulation**, and one of its widest tables:

- **Eleven columns per row.** Item, description, quantity and unit, then a Unit Price and
  Total pair for the Engineer's Estimate and for each of three bidders, with the bidder
  name in a merged header cell over each pair and blank spacer columns between them. Every
  price has to be paired with the right bidder and the right half of the pair.
- **A checklist grid** of eight submittal rows ("Bid Bond", "E-Verify" and so on) where
  every cell reads "Yes". Only the cell's position says which bidder and which document it
  belongs to.
- **Five schedules over three pages**: the base bid and four mandatory alternates
  (MA-1 to MA-4). Each alternate repeats the bidder header and the column layout.
- **Deduct lines**, with negative quantities and negative totals.
- **Totals that reconcile** both down the columns (line items to schedule totals) and
  across pages (base bid plus the four alternates to the grand total on page 4).

## Featured fields: the base bid result

All on page 1.

| Field | Value |
|---|---|
| Engineer's Estimate total base bid | $1,186,195.00 |
| Low bidder | Yarberry Companies, Inc. |
| Low bidder total base bid | $1,117,809.00 |
| Low bidder bid bond received | Yes |
| Engineer's unit price for item 3 (railroad casing pipe) | $623.00 |

Together they show the result of the opening: what the engineer expected, who came in
lowest and by how much, and that the low bid came with a bid bond. The bid bond crop is
one "Yes" out of 24 identical ones in the grid, so it shows that the row and column were
read correctly. Item 3's unit price ($623.00) differs from its total ($87,220.00), so its
crop shows which of the pair was read. The lump-sum items print the same figure in both
columns and would not show that.

The request suggested six fields. The bid opening date was left out: the schema returns it
in ISO form (2026-06-12), so the grounding check cannot find that value in the printed
"June 12, 2026" and marks it OFF. A page also features at most five fields.

## What it surfaced

**Every value is right.** The extraction returned all 1,298 values: 83 line items across
five schedules, each with an estimate and three bids. Every line's quantity times unit
price equals its total, for the estimate and for all three bidders. Every schedule's line
totals sum to its printed total, and the five Engineer's Estimate totals sum to the
$2,666,583.00 grand total on page 4. The spacer columns caused no pairing errors.

**The bidder irregularity is visible in the data.** The engineer's note on page 4 says
Yarberry's unit price for item 8a on MA-1 does not match its base bid price. The
extraction shows it: $30.00 in the base bid, $40.00 on MA-1. The source highlights those
cells in yellow. The notes about each bidder were extracted to `engineer_comments`.

**Grounding is tight in the base bid table.** Each price grounds to its own cell, so every
crop holds exactly one figure. A bidder's name grounds to the whole merged header cell,
address included, which is why the "Low bidder" crop shows three lines.

**Two rows on page 3 ground one row out.** On MA-3, items 14 and 15 extracted correctly,
but their ranges point at the following row (item 14's number grounds to "15"). This was
the only drift found among the line items.

**Each alternate's values carry a second, empty range.** Every value in MA-1 to MA-4 has
a zero-length second range at the start of its table. The grounding check lists these as
OFF occurrence 1 with no page. They are harmless, but a consumer joining ranges to blocks
should skip empty ones.

**The checker misreads one name.** "S&S Directional Boring, Ltd." reads OFF only because
the parse escapes the ampersand as `&amp;` in its HTML table. The box is on the right
cell.

## Extraction

**32 leaf fields**: owner, project, division, bid opening date and preparer; the
Engineer's Estimate base bid and grand total; for each bidder, the name, address, six
checklist entries, base bid, grand total and the engineer's comments; for each schedule,
its name, its estimate total and its line items (item number, description, quantity,
unit, estimate unit price and total, and each bidder's unit price and total); and the
certification (engineer, registration line, date). All 9 top-level fields populate.

## Cost

**48.70 credits** at standard tier for 4 pages, parse and extract together.

## Regenerating

The committed PDF has its document metadata cleared. A fresh download carries it again;
clear it with PyMuPDF before parsing.

```bash
curl -sSL -o document-types/collection/bid-tabulation/source/S18018-Div-B-Bid-Tab.pdf \
  "https://commonwealthengineers.com/wp-content/uploads/2026/06/S18018-Div-B-Bid-Tab.pdf"
.venv/bin/python document-types/scripts/run_ade.py bid-tabulation                # 48.70 credits
.venv/bin/python document-types/scripts/run_ade.py bid-tabulation --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py bid-tabulation           # free
.venv/bin/python document-types/scripts/inspect_fields.py bid-tabulation --page 1
```
