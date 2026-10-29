# Master Services Agreement

Source assets for `landing.ai/document-type/master-services-agreement`.

## Sample document

`source/msa-williamson-county-powerdms.pdf`: a **Master Services Agreement** between
Williamson County, Texas and Power DMS by NEOGOV, with the vendor's order form attached
as Exhibit A. **7 pages, portrait.**

- **Pages 1-5** are the county's standard master agreement: recitals, services, a
  12-month term with up to five automatic one-year renewals, a not-to-exceed amount of
  $7,564.33, Texas prompt-payment terms, indemnification, venue, a three-year audit
  right, no assignment, and the signature page.
- **Page 5**, the signature page, is a scan, not a text page. The vendor's block carries
  a DocuSign signature, printed name and date, with a legal-review initials stamp beside
  it. The county's block is blank.
- **Pages 6-7** are Exhibit A, the vendor's two-page order form: contract records,
  billing and shipping contacts, Net 60 payment terms, two subscription pricing tables
  (a prorated October-November 2024 period and a December 2024-November 2025 year),
  special conditions, and side-by-side signature columns for the two parties.

| | |
|---|---|
| Publisher | Williamson County, Texas (Commissioners Court) |
| Source | [Commissioners Court agenda attachment, February 11, 2025](https://public.destinyhosted.com/wilcodocs/2025/COM/20250211_1884/36121%5FMSA%5FPower%5FDMS%5F%2D%5F02%2E05%2E2025%5FGC%5FStamp%5F%2D%5FRedacted%2Epdf) |
| Linked from | [The court's public agenda](https://public.destinyhosted.com/94526/agenda/agenda.cfm?seq=1872) |
| Retrieved | 2026-10-28, by script |
| Clearance | **Public** |

The county published this contract as an attachment to a public Commissioners Court
agenda. **It is published here as the county filed it: nothing was replaced.** That was
the document owner's explicit decision. The county had already blacked out the order
form's account and order numbers, and no text sits under those boxes. The parties are a
county and a software company. The vendor's signer appears in a professional capacity on
pages 5 and 7, with two DocuSign signatures. The contact details on the order form are
a county department's accounts-payable mailbox and office phone. The PDF carried no
metadata.

## Why this document

The collection's other contracts are leases and loan documents. This is a services
agreement in the form public bodies actually use: the buyer's own legal terms with the
vendor's order form stapled on as an exhibit. One file therefore holds two documents
with different authors and layouts: numbered prose clauses in Times on pages 1-5, and a
vendor-branded order form with label/value grids and ruled pricing tables on pages 6-7.
It also mixes layers: page 5 is a scan in the middle of a born-digital PDF. It tests
whether extraction can pull contract terms out of legal prose (a not-to-exceed amount
written out in words and figures, a renewal count, an audit window) and structured
pricing out of the order form in the same pass.

## Schema

`schema.json` covers the agreement title and e-signature envelope ID; the county and
the service provider; the initial term, renewal count, not-to-exceed amount and
late-payment statute; venue, governing law, the audit window and notice, and whether
assignment is allowed; both signature blocks on the master agreement; and the order
form (customer, employee count, the redacted account and order numbers, valid-until
date, billing address, email and phone, payment term, notes, the pricing tables as an
array of periods with line items and a period total, whether tax is included, and the
vendor signer's title and signature date).

**39 leaf fields** (counted from the schema; 75 once the signature blocks, the two
periods and their six line items are expanded).

Every value matches the page except one: `county.name` returns "Williamson" rather
than "Williamson County, Texas", the name the opening paragraph defines; see the
grounding notes for why the description was not reworded. The blacked-out account and
order numbers come back as empty strings, although the schema asks for null.

## Featured fields: one subscription line, from page 6

| Field | Value |
|---|---|
| Payment term | Net 60 |
| Subscription | PowerPolicy Professional Subscription |
| Users | 89 |
| Prorated period end | 2024-11-30 |
| Prorated total | $1,260.69 |

Read together: what was bought, for how many users, through when, on what terms, inside
what prorated total. The request suggested page 6 with the customer, the payment term, a
subscription line item with dates and quantity, and the prorated total, as suggestions
only. Page 6 ships with all of them except the customer and the line's start date, both
of which ground `OFF`. No person is featured.

## Grounding notes

- **Table grounding depended on the wording of an unrelated field.** The first
  extraction grounded every pricing cell to its own cell. Rewording the description of
  `county.name`, a page-1 field, to ask for "Williamson County, Texas" fixed that value,
  but in two runs in a row every value in the prorated table, its total included, then
  grounded to the table's heading "Prorated to Shift Dates" instead of its cell. Values
  were still right; the boxes were useless. Restoring the original description restored
  cell-level grounding, and that run is the one committed. Table grounding on this
  document is not stable across small schema changes, and is worth rechecking with
  `inspect_fields.py` after any edit.
- **Order-form cells ground cell by cell** in the committed run: item, type, end date,
  quantity and total for all six line items, and the first period's total. Each value
  also has a second range pointing at the table heading.
- **Start dates read `OFF` although their boxes are right.** The form prints `10/1/2024`
  without zero padding; the ISO value does not match it literally.
- **The customer reads `OFF`.** "Williamson County Emergency Communications (TX)" wraps
  across two lines of its cell.
- **The scanned signature page parses cleanly.** Page 5's two signature blocks come back
  as attestation blocks, the vendor's labelled `[E-SIGNED]` with the printed name and
  DocuSign timestamp read off the scan, and the legal-review stamp as a logo block
  reading "NEOGOV LEGAL [HANDWRITTEN INITIALS]".
- **Side-by-side signature columns on page 7 stay separate.** Each party's column is its
  own attestation block, so the vendor's title and date do not bleed into the county's
  empty column.
- **The second period's total is on page 7**, where the table breaks across the page.

## Cost

**15.50 credits** at standard tier for one 7-page parse and one extraction (parse 8.90,
extraction 6.60). The schema experiment above added three more extractions, so the
build spent **35.30 credits** in all.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py master-services-agreement
.venv/bin/python document-types/scripts/build_images.py master-services-agreement
.venv/bin/python document-types/scripts/inspect_fields.py master-services-agreement --page 6
```

A fresh extraction may ground the prorated table differently; check page 6 with
`inspect_fields.py` before rebuilding the images.
