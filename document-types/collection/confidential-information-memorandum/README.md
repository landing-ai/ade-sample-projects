# Confidential Information Memorandum

A confidential information memorandum (CIM) for the sale of the PTL Group (PTL Holdings
Limited, PTL Services (Equipment) Limited, CSL Services (Industrial) Limited and 9263357
Canada Inc.), a site services, equipment rental and aggregate supply business in Southern
Harbour, Newfoundland and Labrador. It was prepared in May 2018 by BDO Canada Limited as
court-appointed receiver, to market the companies' assets to bidders. **19 pages,
portrait (612×792)**: a photo cover, a covering letter to prospective purchasers, a
disclaimer, contacts, an executive summary with investment highlights and charts, site
descriptions, a five-year historical income statement, a three-year forecast, a sale
process summary and the full sale process as Appendix A.

| | |
|---|---|
| Publisher | BDO Canada Limited, as court-appointed receiver of the PTL Group |
| Source | [bdo.ca/getmedia/c60b2304-857e-45ef-8825-cdc24ec12bbb/1st-App-H-PTL-Group-CIM.pdf](https://www.bdo.ca/getmedia/c60b2304-857e-45ef-8825-cdc24ec12bbb/1st-App-H-PTL-Group-CIM.pdf) |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | `redacted` |

## Clearance

The memorandum was filed publicly as Appendix H to the Receiver's First Report to the
Supreme Court of Newfoundland and Labrador, and BDO publishes it on bdo.ca with the
other receivership filings. Every page still carries the "Confidential Information
Memorandum" legend, and page 2 the notice that it is provided under a non-disclosure
agreement: that is its wording from the marketing stage, before it was filed. BDO's
engagement page for the PTL Group blocks scripted access, so the link from that page to
this file was not confirmed; the file itself is on BDO's own domain.

The companies, the receiver and the court are kept. The receiver's individual staff are
replaced:

| What | Replaced with | Occurrences |
|---|---|---|
| Receiver staff contacts' names | Jane Q Sample, John Q Sample | 5 |
| Their work email addresses | ja@example.com, jo@example.com | 7 |
| Staff direct lines, and office phone and fax numbers (area codes kept) | fiction-reserved 555-01xx numbers, one stand-in per number | 9 |

Text was replaced with `document-types/scripts/redact.py`, which removes the underlying
text rather than covering it. The emails' `mailto:` links went with the text. Kept as
printed: the firm names, the two BDO office addresses and the bid delivery address,
which are corporate.

Two leak paths beyond the page text were closed:

- **PDF metadata.** The `/Info` author field named a staff member. Cleared.
- **Image metadata.** One of the JPEG photographs carried XMP whose `dc:creator` named a
  staff member, in a different name order from the page text. The EXIF, XMP, IPTC and
  comment segments of every embedded JPEG were stripped without re-encoding, so the
  pixels are unchanged.

One name in the covering letter wraps across a line break. `redact.py` now splits a
replacement across the lines of a wrapped match ("Jane Q" / "Sample") instead of drawing
the whole stand-in on each line. The stand-ins are set in Helvetica, so they look
slightly different from the surrounding text.

**Verified:** no original value can be extracted from the committed PDF's page text,
metadata, objects or decoded streams, checked as literal strings and as bare digits, and
no original value appears anywhere in this folder. The rules file stays outside the repo.

## Why this document

A CIM is a long, mixed narrative: legal letter, disclaimers, marketing copy with a
side-by-side highlights panel, image-only charts and tables, and dense numbered
conditions. The facts a buyer needs are repeated in different words in different
sections. The receiver, the court order and the bid deadline appear in the covering
letter, again in the executive summary and again in Appendix A. That makes it a good
test of where extraction decides to ground a value that appears more than once. It is
also the first sale-side M&A document in the collection, and a distressed one.

## Featured fields

All on page 3, the receiver's covering letter, which states the whole deal in one
place:

- **Company for sale**: the "Re:" line, pinned to occurrence 1 (occurrence 0 is the
  cover).
- **Seller capacity**: "Court-appointed Receiver".
- **Court**: the Supreme Court of Newfoundland and Labrador.
- **Receivership order date**: May 11, 2018.
- **Binding offer deadline**: 2:00 p.m. (NDT) on Thursday, June 14, 2018.

None of them is a person.

The request suggested page 7, the executive summary, with the receiver, the order date,
the court, the offer deadline and the employee count. It was a suggestion, not a
requirement. Page 7 states all five, but grounding on this document is not stable from
run to run: across three extraction runs, the court and the order date grounded on page
7 in one run and on page 3 or page 15 in the others, and the deadline always grounded on
page 3, where it is printed in full with the weekday. The page 7 version is printed as
"June14, 2018". The committed run grounds only the receiver's name, the "over 40 years"
founding age and the "~70" employee count on page 7. Page 3 carries four of the five
suggested facts, all grounded correctly. The employee count appears only on page 7 and
is not featured.

## Grounding notes

- **Repeated facts move.** With the same parse, re-running extraction moved the grounding
  of the court and the order date between the covering letter, the executive summary and
  Appendix A. Each grounding was correct where it landed. A schema description pointing
  at the executive summary made it more likely but did not pin it.
- **Image-only tables are read.** The five-year historical income statement on page 10
  is an image with no text layer. DPT-3 read it into a table, and all 35 of its figures
  ground. 2016A and 2017E really do have the same COGS (12,401); it is not a parse
  repeat.
- **Charts are described.** The bar and pie charts on page 7 are images. The parse turns
  them into data tables. Extraction then put the pie chart's revenue categories into
  `business_overview.services`, grounded on the percentages (marked `OFF`), alongside
  the services listed in the text.
- **A field left null, then found.** The first schema asked for the "current year"
  secured revenue, and extraction returned null even though "$8.9 million" is printed on
  page 10. Renaming the field `revenue_secured_by_contracts` and describing it found and
  grounded it.
- **Boolean flags ground to supporting text.** `workforce_unionized` and
  `court_approval_required` ground to the sentences that imply them, which is correct
  but cannot be shown as a crop.

## Schema

48 leaf fields: the target companies, the seller and its capacity, the insolvency
proceeding, sale process terms (deadline, offer form, delivery address, deposit, closing,
sale basis), a business overview, investment highlights, the property sites, historical
performance, the income statement table (historical and forecast columns), the sale
timeline and the contacts.

## Credits

84.00 credits at standard tier: 37.80 for the first parse and extract, then three
extract-only runs at 15.40 each while refining the schema and checking grounding
stability.

## Regenerate

```bash
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/confidential-information-memorandum/source/ptl-group-cim-redacted.pdf \
    --rules <outside-the-repo>/rules.json
.venv/bin/python document-types/scripts/run_ade.py confidential-information-memorandum
.venv/bin/python document-types/scripts/run_ade.py confidential-information-memorandum --extract-only
.venv/bin/python document-types/scripts/build_images.py confidential-information-memorandum
```

A fresh extraction may ground the featured fields on a different page; check with
`inspect_fields.py confidential-information-memorandum --page 3` before rebuilding the
images.
