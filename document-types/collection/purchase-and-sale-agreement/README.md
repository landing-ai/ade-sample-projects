# Purchase and Sale Agreement

Source assets for `landing.ai/document-type/purchase-and-sale-agreement`.

## Sample document

`source/purchase-and-sale-agreement-az-realtors.pdf`: a fully executed Arizona
Association of REALTORS **Residential Resale Real Estate Purchase Contract** (form dated
February 2020). **10 pages, portrait.**

An LLC buys a single-family home in Tucson from another LLC for $845,000, all cash. The
form is the standard Arizona resale contract: property and price (Section 1), financing
(not used here), title and escrow, disclosures, warranties, due diligence, remedies,
typed additional terms, and the buyer's offer and seller's acceptance with DocuSign
signatures and initials on every page.

| | |
|---|---|
| Publisher | Here Collection LLC, as filed with the SEC; pre-printed form by the Arizona Association of REALTORS |
| Source | [SEC EDGAR, here_ex6z17.pdf](https://www.sec.gov/Archives/edgar/data/1876769/000109690622001941/here_ex6z17.pdf) |
| Filing | Exhibit EX1A-6 (material contract) to Form 1-A POS, accession 0001096906-22-001941, filed 2022-08-18 |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** |

Here Collection filed this contract publicly on EDGAR as a material contract of its
Regulation A offering; the filing index lists `here_ex6z17.pdf`. Buyer and seller are
both LLCs. Everyone else named acts in a professional capacity: the seller's listing
agent and brokerage with their license numbers, the escrow officer at the title company,
and the LLC signers whose e-signatures and initials are on the form. No private
individual's personal data is present, so nothing was replaced.

Two changes from the filed PDF:

- **Page 1 was dropped.** It is the one-page Buyer Attachment, an advisory checklist that
  says on its face it is not part of the contract's terms. The sample is the ten-page
  contract alone, so page numbers here are the filed PDF's minus one.
- **PDF metadata was cleared** (PDFium creator/producer and a creation date). The pages
  are otherwise unchanged.

## Why this document

It is a real, signed, filled-in contract rather than a blank form, and every core term
of the deal sits on one clean page. Two things make it a useful test:

- **The typed values have no text layer.** The pre-printed form is text, but every
  filled-in value (names, address, amounts, dates) is drawn without one, so the parse has
  to read them from the image while reading the form around them from text.
- **Values are threaded through numbered form lines**, with checkboxes, split date
  blanks (month, day and year in separate blanks) and printed defaults that a typed value
  overrides. That is the shape of most real-estate forms.

## Schema

`schema.json` covers the form identity, the parties, the premises (address, parcel
number, legal description), price and payment (purchase price, earnest money and its
form and holder, cash at closing, all-cash flag), close of escrow, addenda, the escrow
company, inspection period, home-warranty election, the typed additional terms, offer
expiration, the seller's broker, and both signature blocks.

**43 leaf fields** (counted from the schema).

## Featured fields: the deal, from page 1

| Field | Value |
|---|---|
| Full purchase price | 845,000 |
| Earnest money | 10,000 |
| Cash due at closing | 835,000 |
| Assessor's parcel number | 114-18-0490 |
| Legal description | Rockcliff Lot 37 |

Read together: which parcel is being sold, for how much, and how the price is paid
($10,000 earnest money + $835,000 at closing = $845,000). The request suggested the
first four plus the seller. The seller could not be featured (see below), nor could the
buyer, so the legal description took its place. No person is featured.

## Grounding notes

- **Section 1 grounds line by line, and the money lines are clean.** Each amount boxes
  exactly its numbered line (10, 11, 12), with the value inside.
- **The seller's range is far too wide.** `seller_name` is right, but its extraction
  range runs from the "1. PROPERTY" heading through the city line, about seven lines.
  The first block it touches is the heading, so the crop boxed "1. PROPERTY".
  `inspect_fields.py` still marks it `ok`, because the over-wide range does contain the
  value. Only opening the crop showed the problem.
- **The buyer's line box is one line low.** `buyer_name` has a tight range, but the
  parse's line-level box for "1a. 1. BUYER: HCO 1, LLC" covers the printed
  "BUYER'S NAME(S)" caption under the value. The real line's box is attached to a
  zero-length entry just before it. Also marked `ok`, also wrong by eye.
- **The close-of-escrow date is assembled correctly** ("October / 3rd / 2022" becomes
  2022-10-03) but grounds `OFF`, because the ISO date is not printed. As the request
  warned, it is not featured.
- **The typed additional terms (Section 8a) come back synthesized.** All five are
  verbatim and correct, but none has ranges, even though the parse reads them as table
  cells.
- **One parse error: an a.m./p.m. checkbox.** The offer expires "August 5, 2022 at
  11:00" with the **a.m.** box checked. The parse wrote `[ ] a.m./ [x] p.m.`, so
  `offer_expiration.time` reads "11:00 p.m.".
- **One extraction error: the inspection period.** The form prints "ten (10) days or
  ___ days" and the blank is filled with 7. The parse reads "ten (10) days or 7 days"
  correctly, but extraction returned the printed default, 10, even after the field
  description was rewritten to say a filled blank overrides the default.
- **`is_all_cash_sale` needed a better description.** The first extraction returned
  `false`, apparently reading line 19's "IF THIS IS AN ALL CASH SALE" literally. A
  description saying earnest money plus cash at closing equals the full price fixed it.
- Booleans and signature flags ground `OFF` to `[SIGNED]` tags and checkbox lines, as
  usual.

## Cost

**59.20 credits** at standard tier: one 10-page parse and extraction (32.60), plus two
extraction-only reruns (13.30 each) while tuning field descriptions.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py purchase-and-sale-agreement
.venv/bin/python document-types/scripts/build_images.py purchase-and-sale-agreement
.venv/bin/python document-types/scripts/inspect_fields.py purchase-and-sale-agreement --page 1
```
