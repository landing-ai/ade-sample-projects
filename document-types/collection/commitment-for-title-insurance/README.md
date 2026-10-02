# Commitment for Title Insurance

Source assets for `landing.ai/document-type/commitment-for-title-insurance`.

## Sample document

`source/commitment-for-title-insurance-redacted.pdf`: a 2016 ALTA Commitment for Title
Insurance issued by First Integrity Title Company as agent for Westcor Land Title
Insurance Company, with the agent's lender notes and both companies' privacy notices.
**11 pages, portrait** (12 in the original; see below).

| | |
|---|---|
| Publisher | First Integrity Title Company, as agent for Westcor Land Title Insurance Company |
| Source | [adc-tenbox-prod.imgix.net/…/PRELIMINARY_TITLE_REPORT/…pdf](https://adc-tenbox-prod.imgix.net/resi/propertyDocuments/1300098/PRELIMINARY_TITLE_REPORT/40C02EC5FCCE4D3BBF40A5C6B9BEF65F.v1.pdf) |
| Retrieved | 2026-10-02, by script (no manual download needed) |
| Clearance | **Redacted**, see below |

It is posted as the preliminary title report on a residential property-auction listing,
for prospective bidders. That makes the file public, but not the people in it.

## This document was redacted before it entered the repo

**It is a foreclosure file.** Schedule B-II records a notice of default and a notice of
trustee's sale against the first deed of trust. It named three private homeowners as
vested owners and trustors, and a named debtor under a child-support judgment. The
property could be found from its street address, its assessor's parcel number, the
legal description, or any of the county recording numbers.

| Personal or locating data | Occurrences | Replaced with |
|---|---|---|
| Vested owners' and trustors' names (three people) | 9 | `Jonah Q Sample`, `Robert James Q Sample`, `Jane Q Sample` |
| Judgment debtor's full name | 1 | `Jonah Quinn Sample` |
| Street address, city, ZIP, county | 10 | `100 SAMPLE RD`, `Anytown`, `90000`, `Sample` |
| Assessor's parcel number | 3 | Random stand-in, same shape |
| Section, township, range, parcel map number, map page | 6 | Different numbers |
| Recording instrument numbers (8 distinct) | 9 | Year prefix kept, other digits random |
| MERS MIN, court case number | 2 | Random stand-ins, same shape |
| Commitment / order number, including the recorded-documents link | 10 | `FIN-78796415` |
| Wire instructions (title company's real trust account and routing numbers) | page 11 | page dropped |
| PDF metadata (a title-company employee's name) | — | cleared |

Amounts, dates, tax figures, and lender and trustee company names are kept. Once the
identifiers above are gone, they no longer point to a property.

Corporate officers' names and facsimile signatures are kept. That covers Westcor's
President and Secretary on the jacket, and the agent's COO on Schedule A. They sign in
a corporate capacity and appear on every commitment these companies issue. None of them
is featured.

### Why `redact.py` could not do it

The PDF was produced by *Microsoft: Print To PDF*. That driver writes every glyph as a
filled vector path, so the file has **no text layer**. `redact.py` finds strings through
the text layer, which here returns nothing for every page, so every rule would have
missed without an error.

`document-types/scripts/redact_outlined.py` handles this case:

1. It OCRs each page with Tesseract to locate each string.
2. It snaps each hit to the glyph paths underneath it.
3. It deletes those paths from the content stream with a redaction annotation (line art
   removed if covered), rather than covering them.
4. It draws the replacement in Helvetica at the original size and baseline, compressed
   horizontally to the source font's narrower set width.

Strings that wrap onto the next line ("Debtor: …" / "…;") are matched across the break.
Bold is detected from ink density, because the bold and regular digits are the same
width. The bold-italic link was forced with a per-rule font.

Verification is OCR of every page of the output, on literals and on bare digits. It
passed, and a separate sweep of every file in this folder found none of the originals.
That sweep also caught the redaction script itself: its comments had used the real
debtor's name and commitment number as examples. They were replaced before commit.

Visible artefact: a replacement shorter than its original leaves a gap before the next
word (`100 SAMPLE RD , Anytown , CA`), because outlined text cannot reflow. The parse
reads the gap as a space, so the extracted address carries it too.

## Why this document

This is the first sample in the collection that is **vector outlines with no text
layer**. The page looks like a digital PDF, but nothing can be copied out of it, so the
parse is reading what is drawn, much as it would a scan. It is also the first real-estate
title product. It is a long legal form with a two-page Schedule B of encumbrances
(deeds of trust, assignments, foreclosure notices, a judgment), and those make a hard,
structured extraction.

`schema.json` was written for this sample: 15 top-level groups, **49 leaf fields**
(counted from the schema). All 15 populate. Extraction found 18 Schedule B-II
exceptions and both deeds of trust. It also inferred `in_foreclosure: true` for the
first deed of trust and `false` for the second, from the notices recorded under each.

## Featured fields: the jacket, and its attestation

The request asked for page 1 and for two booleans: whether the commitment is signed,
and whether it carries a seal or stamp. Both are on page 1, the commitment jacket.
Three identifying fields join them there.

| Field | Value |
|---|---|
| Commitment number | FIN-78796415 |
| Underwriter | Westcor Land Title Insurance Company |
| Form edition | ALTA Commitment for Title Insurance (Adapted 08-1-2016) |
| Signed | true |
| Seal or stamp | true |

The booleans ground to the parse's attestation labels. `is_signed` grounds to `[SIGNED]`,
whose box is the President's signature line. `has_seal_or_stamp` grounds to `[SEALED]`,
whose box is exactly the corporate seal, and the parse transcribed the seal's ring text.
Both tools flag them `OFF` because the word "true" is not on the page. That is expected
for a boolean, and both crops were checked by eye.

## Grounding notes

- **The page 1 booleans each have several ranges.** Besides the attestation label, the
  model also cites the "IN WITNESS WHEREOF" paragraph. Occurrence 0 is the label in both
  cases, which is the crop that makes the point.
- **`issuing_agent.name` cannot be featured.** The name wraps over two lines in the
  "Issued By" block, so each of its two ranges holds half the value and both read `OFF`.
- **`signatory_titles` picked up the COO** from Schedule A as well as the jacket's two
  officers, although the description scoped it to the jacket.
- **`property.legal_description` stops at the line break before the parcel map
  number.** The schema asked for the first paragraph only, and the model cut it at a
  line break instead.

## Cost

**26.4 credits** at standard tier for the committed output: 13.4 for the 11-page parse
and 13.0 for the extraction.

Getting there cost more. The first two extraction jobs failed with `Internal Server
Error`, and bisecting the schema (five partial extractions) traced it to the top-level
property name: **a property named `exceptions` makes v2 Extract fail.** Renamed to
`schedule_b_exceptions`, the identical sub-schema extracts normally.

## Regenerating

```bash
# Redaction, from the original download; the rules file stays outside the repo.
.venv/bin/python document-types/scripts/redact_outlined.py <original>.pdf \
    source/commitment-for-title-insurance-redacted.pdf \
    --rules <outside-the-repo>/rules.json --drop-pages 11 \
    --verify-also <each surname and the bare commitment number>

.venv/bin/python document-types/scripts/run_ade.py commitment-for-title-insurance
.venv/bin/python document-types/scripts/build_images.py commitment-for-title-insurance
.venv/bin/python document-types/scripts/inspect_fields.py commitment-for-title-insurance --page 1
```

Requires `tesseract` on the PATH (`brew install tesseract`).
