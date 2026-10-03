# IRS CP 575

Source assets for `landing.ai/document-type/irs-cp-575`.

## Sample document

`source/irs-cp-575-sample.pdf` — a specimen CP 575 A notice, the letter the IRS sends
when it assigns an Employer Identification Number. **3 pages, US Letter portrait
(612×792)**, with a full text layer: the letter on page 1, reminders on page 2, and a
mostly blank page 3 ending in the tear-off stub.

| | |
|---|---|
| Publisher | MetroPlusHealth |
| Source | [metroplus.org/…/Sample-IRS-Letter.pdf](https://metroplus.org/wp-content/uploads/2024/09/Sample-IRS-Letter.pdf) |
| Retrieved | 2026-10-03 (downloaded by script) |
| Clearance | Public |

MetroPlusHealth publishes it on its provider forms page as a credentialing example, to
show providers which IRS letter to submit. Every value is placeholder data: EIN
88-8888888, the entity "ABC Behavioral LCSW PC" at "123 OLD Road TPKE, ANY VALLEY, NY
10111", name control ABCD, an IRS-use reference of 9999999999, and dates in the year 2525.
No real person's or business's data appears, so nothing was redacted. The PDF metadata
names only "IRS" as author, and the file is committed exactly as downloaded.

**The publisher marked it up.** A red "EXAMPLE ONLY" header, two yellow callout boxes
("Name must match contracted entity and the W9", "EIN must match W9") with arrows, and
yellow highlights over the name and EIN. They are in the text layer, and the parse keeps
them as their own text blocks.

**The dates are deliberately invalid.** Page 1 dates the notice 01-35-2525; the stub on
page 3 and the IRS-use line on pages 2 and 3 print 01-25-2525. The notice date is not
featured for that reason.

## Why this document

The collection's first **EIN assignment notice**, and a contrast with the CP565 in
`itin-number/`: where that letter is mostly table, this one is almost entirely prose.

- **33 parse blocks over three pages, none of them tables**: 27 text blocks and 6
  marginalia. The header block is a run of `label: value` lines, not a grid.
- **Key values live in sentences.** The required filing and its due date sit on a line
  of their own after "you must file the following forms by the dates shown", and the
  name control is stated only in a page 2 sentence.
- **Third-party markup over an official form**, which a real credentialing workflow sees
  constantly: annotated copies passed between organizations.
- **Identifiers repeat** across the header, the body, the IRS-use line and the stub.

## Featured fields: the assignment, in one page

All on **page 1**. The request suggested five fields, as suggestions only; all five
ground `ok` there and all five ship:

| Field | Value |
|---|---|
| Employer Identification Number | 88-8888888 |
| Legal name | ABC Behavioral LCSW PC |
| Notice number | CP 575 A |
| Application form | SS-4 |
| Required filing | Form 1120 |

Together they read as one thing: which notice this is, which application it answers,
which business received which number, and what that business must now file. The legal
name is a fictitious business's, not a person's. The EIN uses occurrence 0, the header
block, rather than its repeat in the first paragraph.

## What it surfaced

**Everything extracts.** All 13 leaf fields populate, with no warnings and no schema
violation.

**The page 1 address grounds line by line.** `entity.address` comes back with one range
per printed line, so `inspect_fields.py` marks both page 1 ranges `OFF`: each holds half
the value. The stub's copy on page 3 is `ok`. Not featured.

**The tear-off stub parses as one block.** The stub copies of the legal name, the agency
and the office address all ground to a single block that spans the whole stub, so they
are `ok` but their box is the stub, not the line. Page 1 copies are used instead.

**Callouts did not leak into fields.** "EIN must match W9" sits directly beside the EIN
and was parsed as a separate block; the EIN's range starts at the IRS's own label.

**Extraction followed the page 1 date.** The schema asks for the date as printed in the
page 1 header, and it returned 01-35-2525 rather than the stub's 01-25-2525. It does not
flag the mismatch; nothing in the schema asks it to.

## Extraction

`schema.json` has **13 leaf fields**: the EIN; the notice (number, date, form, revision);
the entity (legal name, address, name control); the required filings, as an array of
form and due date; and the issuer (agency, office address, assistance phone).

## Cost

**4.80 credits** at standard tier for 3 pages: 3.10 to parse, 1.70 to extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py irs-cp-575                # 4.80 credits
.venv/bin/python document-types/scripts/run_ade.py irs-cp-575 --extract-only # 1.70, schema iteration
.venv/bin/python document-types/scripts/build_images.py irs-cp-575           # free
.venv/bin/python document-types/scripts/inspect_fields.py irs-cp-575 --page 1
```
