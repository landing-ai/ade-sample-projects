# Stock Purchase Agreement

Source assets for `landing.ai/document-type/stock-purchase-agreement`.

## Sample document

`source/stock-purchase-agreement-hydro-star-nuon.pdf`: a joint application to the
Kentucky Public Service Commission (Case No. 2005-00323) asking for approval of a
transfer of stock. Exhibit 3 is the executed **Stock Purchase Agreement** dated as of
May 14, 2005, under which Hydro Star, LLC buys all 1,000 shares of Nuon Global Solutions
USA Inc., the parent of the water and wastewater utility holding company Utilities,
Inc., from Nuon Global Solutions USA B.V. for $192,500,000. **78 pages, portrait.**

The filing is in three parts: the cover letter, application and verifications (pages
1–30), the SPA (pages 31–75: cover, 42 numbered pages of terms, signature pages 74–75)
and later exhibits (76–78).

| | |
|---|---|
| Publisher | Kentucky Public Service Commission (filed by Nuon Global Solutions USA B.V. and Hydro Star, LLC as joint applicants) |
| Source | [psc.ky.gov, NHW_App_080205.pdf](https://psc.ky.gov/PSCSCF/2005%20cases/2005-00323/NHW_App_080205.pdf) |
| Case | Kentucky PSC Case No. 2005-00323 |
| Retrieved | 2026-10-28, by script |
| Clearance | **Public** |

This is a public regulatory filing, downloaded from the Commission's official case-file
server. **The operator decided explicitly to publish it as filed, without redaction.**
That departs from the collection's usual rule that personal data is replaced before
parsing. The filing names corporate officers, attorneys and company contacts, and carries
their wet signatures, phone and fax numbers, notary seals and a personnel table. Every
one of them appears in a professional or corporate capacity in a document the Commission
publishes. None of it was replaced.

The one change from the filed PDF: **the hidden /Info and XMP metadata was cleared**
(Acrobat Paper Capture creator and the 2005 creation and modification dates). Every page's
content stream is byte-identical to the filed file.

## Why this document

- **It is a raster scan.** The file is an Acrobat Paper Capture scan, and only page 1
  has any text layer. Every value has to be read from the image.
- **It is long legal prose.** Most other samples are forms or statements, with a value
  next to a label. Here every value sits mid-sentence in a defined-term paragraph:
  `("Seller")`, `(the "Purchase Price")`. Extraction has to resolve those definitions.
- **The contract is wrapped in a filing.** The SPA is an exhibit inside a 78-page
  application, so the document also tests whether extraction picks the contract's own
  terms over the application's summary of them.

## Schema

`schema.json` covers the agreement date, the seller, buyer and target company (name,
entity type, jurisdiction, operating subsidiary), the stock (shares, class, par value,
percentage of the company), the purchase price and currency, payment method, earnest
money, closing location, time and timing, both parent guarantors, the termination fee,
the outside-date terms, the governing law, and the signature blocks.

**31 leaf fields** (counted from the schema).

## Featured fields: the deal, from page 32

| Field | Value |
|---|---|
| Seller | Nuon Global Solutions USA B.V. |
| Buyer | Hydro Star, LLC |
| Company whose stock is sold | Nuon Global Solutions USA Inc. |
| Shares sold | 1,000 |
| Purchase price | $192,500,000 |

Page 32, the SPA's first page of terms, holds the whole deal: who sells, who buys, which
company, how many shares and for how much. It carries no personal data. The request
suggested page 32 and five fields: agreement date, seller, buyer, purchase price and
closing location. Seller, buyer and purchase price ship. The other two ground `OFF`
(see below), so the company and the share count took their place. No person is featured.

The purchase price is pinned to occurrence 1, the Section 1.02 sentence on page 32.
Occurrence 0 is the application's summary of the same figure on page 6.

## Grounding notes

- **The scan grounds cleanly at line level.** Every featured value's box is the exact
  printed line that holds it, though the page has no text layer.
- **The agreement date grounds `OFF`.** Extraction normalises it to 2005-05-14, and the
  page prints "this 14th day of May, 2005", so the crop would not match the value shown
  beside it.
- **The closing location grounds `OFF`.** The value (the law firm's name, then its
  Pennsylvania Avenue address) runs across two printed lines, and neither line box holds
  the whole value. Its neighbour, the 10:00 a.m. closing time, is `ok`. The buyer's
  parent guarantor (American International Group, Inc.) also breaks across a line and
  grounds `OFF`.
- **Contract terms win over the application's summary.** Extraction took the parties,
  price and stock from the SPA rather than from the application pages that restate them.
- **The outside date is not a date.** The first schema asked for a calendar outside
  date and got null. Section 10.01(b) defines the deadline as twelve months after the
  last regulatory filing. The field was redefined as `outside_date_terms`, a string
  quoted as written, and now extracts. The run that returned null is in the credit
  total below.
- **A third signature block was found.** Besides the two parties on page 74, extraction
  picked up a block on page 75 signed for the company itself, Nuon Global Solutions USA
  Inc. It grounds `ok`.
- Signature flags ground `OFF` to `[SIGNED]` / `[HANDWRITTEN SIGNATURE]` tags, as usual.

## Cost

**167.00 credits** at standard tier: the 78-page parse (86.90) and its first
extraction (39.90), plus one extraction-only rerun (40.20) after the outside-date field
was redefined.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py stock-purchase-agreement
.venv/bin/python document-types/scripts/build_images.py stock-purchase-agreement
.venv/bin/python document-types/scripts/inspect_fields.py stock-purchase-agreement --page 32
```
