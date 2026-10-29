# Letter of intent

Source assets for `landing.ai/document-type/letter-of-intent`.

## Sample document

`source/central-states-water-delaplain-loi.pdf`: Exhibit PSC 4-1(b) from Kentucky Public
Service Commission Case No. 2022-00432, as filed by Bluegrass Water. **49 pages, portrait
(612×792).** It is a raster scan with an OCR text layer, a PSC docket stamp on every page
and a CSWR letterhead bar on the letter pages. It contains:

| Pages | Content |
|---|---|
| 1–5 | Signed and countersigned non-binding letter of intent dated July 16, 2019, from Central States Water Resources (CSWR) to buy the assets of Delaplain Disposal Company, a sewer utility in Scott County, Kentucky, for $849,000 |
| 6–7 | Two image-only pages (no OCR layer) from a second CSWR letter of intent, to River Bluffs, Inc.: its exclusivity page and signature page |
| 8–28 | The Delaplain Purchase and Sale Agreement (August 2019, DocuSigned), with exhibits A–H, most of them placeholders |
| 29–49 | The River Bluffs Agreement for Sale of Utility System (June 2019, $240,000), with exhibits A–E |

| | |
|---|---|
| Publisher | Kentucky Public Service Commission (filed by Bluegrass Water Utility Operating Company) |
| Source | [psc.ky.gov/pscecf/2022-00432/…/Exhibit_PSC_4-1(b)_-_Purchase_Agreements.pdf](https://psc.ky.gov/pscecf/2022-00432/kerry.ingle@dinslaw.com/07272023081341/Exhibit_PSC_4-1(b)_-_Purchase_Agreements.pdf) |
| Case filings | [psc.ky.gov/Case/ViewCaseFilings/2022-00432/Post](https://psc.ky.gov/Case/ViewCaseFilings/2022-00432/Post) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

The file is a public regulatory filing on the PSC's official e-filing store. It is used
**exactly as filed, unredacted**, by the operator's decision of 2026-10-28. That departs
from the collection's usual rule that personal data is replaced before parsing. The pages
carry the following, all as they appear in the public record:

- signers' typed names, wet-ink signatures and DocuSign signatures
- a named executive's email address, and business phone, cell and fax numbers, on the
  letterhead
- names, email addresses and phone numbers of notice parties and counsel in the purchase
  agreements

The only change from the filed file: the PDF's document-information and XMP metadata were
cleared before parsing. The `author` field had held the name of the person who prepared
the filing, which is not part of the visible document.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

- **The real artifact, in context.** A letter of intent rarely travels alone. Here it
  sits in a regulatory exhibit with the definitive agreements that followed it, so the
  schema covers the letter's deal points and summarizes the related agreements.
- **Scanned, with handwriting.** The letter itself is a clean scan. The agreements carry
  handwritten dates ("23rd day of August", "10th day of June"), which extraction read
  correctly as `2019-08-23` and `2019-06-10`.
- **Pages without a text layer.** Pages 6–7 have no OCR layer at all, and ADE parsed
  them anyway.

## Featured fields: the deal

All on **page 1**:

| Field | Value |
|---|---|
| Buyer | Central States Water Resources, Inc. |
| Target | Delaplain Disposal Company |
| Target business | regulated sewer utility |
| Purchase price | 849000 |

Together they say who is buying what, and for how much. All four are organization names
or amounts, and no individual's name is featured. `target_name` is pinned to occurrence
0, the Re: line.

**What the request suggested and what shipped.** The request suggested the letter date,
buyer, target and price on page 1, plus the 90-day due diligence and exclusivity terms on
page 3, as suggestions only. Buyer, target and price shipped.

- `letter_date` comes back as `2019-07-16` and grounds to the printed "July 16, 2019".
  The value is right, but the overlay checker cannot match a spelled-out month, so it
  reads OFF.
- `due_diligence_period_days` (90) grounds correctly, but on page 3.
- `exclusivity_terms` is a paraphrase whose range spans the whole clause.

## What it surfaced

**The request misdescribed pages 6–7.** The request called them blank exhibit
placeholders. They are pages from a second letter of intent, to River Bluffs, scanned
without a text layer. ADE read them, and because the schema has a single
`letter_of_intent` object, the River Bluffs signatories and that letter's 90-day term
were merged into it. That gives `acceptance_signatories` four entries rather than two,
and `due_diligence_period_days` a second occurrence on page 6. A file that bundles
several letters needs an array of letters in the schema.

**Clauses ground line by line.** Narrative fields such as `conditions_of_sale`,
`confidentiality_terms` and `assets_included` come back with one range per line of the
clause. That is correct traceability, but no single crop shows the value, so these fields
read OFF.

**Booleans ground to their evidence.** `assumes_seller_debts: false` boxes the "No Debt
Assumption" clause, on page 3 and again on page 6.

**OCR noise is not inherited.** The filer's OCR layer garbles the letterhead email
differently on almost every page. ADE's parse reads the page image rather than the
embedded text, and gives the same, correct address on all seven letterhead pages.

## Schema

`schema.json` was written for this document: 28 leaf fields. There is a
`letter_of_intent` object covering date, parties, structure, price, assets, conditions,
debt, diligence, exclusivity, confidentiality, binding sections and signatories, and a
`related_agreements` array. Extraction returned no warnings.

## Cost

**76 credits** at standard tier for 49 pages: 51 to parse, 25 to extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py letter-of-intent                # 76 credits
.venv/bin/python document-types/scripts/run_ade.py letter-of-intent --extract-only # about 25, schema iteration
.venv/bin/python document-types/scripts/build_images.py letter-of-intent           # free
.venv/bin/python document-types/scripts/inspect_fields.py letter-of-intent --page 1 --good
```

`manifest.json` sets `preview_pages` to 1, 5, 8 and 29: the letter, its signature page,
and the first page of each purchase agreement.
