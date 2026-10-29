# Trademark registration certificate

Source assets for `landing.ai/document-type/trademark-registration-certificate`.

## Sample document

`source/uspto-reg-5886375-registration-certificate.pdf` — the USPTO registration
certificate for U.S. Reg. No. 5,886,375, the AMERICAN NINJA WARRIOR shield design mark,
registered October 15, 2019 in International Class 21. **2 pages, portrait, A4.** Page 1
is the certificate; page 2 is the USPTO's standard statement of the filings needed to
keep the registration alive. Both are kept, as the request asked.

The page is a mixed layer: the text is a real text layer, while the blackletter "United
States of America" banner, the mark itself, the USPTO seal and the Director's signature
are images.

| | |
|---|---|
| Publisher | United States Patent and Trademark Office |
| Source | [tmng-al.uspto.gov/…/5886375_87981735_101519_ORC.pdf](https://tmng-al.uspto.gov/resting2/api/casedoc/cms/case/87981735/registration-certificate/5886375_87981735_101519_ORC.pdf) |
| File record | [TSDR, serial 87981735](https://tsdr.uspto.gov/#caseNumber=87981735&caseType=SERIAL_NO&searchType=documentSearch) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

Trademark registrations and their file histories are public records, published by the
USPTO in TSDR; this is the "Registration Certificate" document in that file. The owner is
a corporation, Tokyo Broadcasting System Television, Inc. The only personal element is
the facsimile signature of the USPTO Director, a public official, which appears on every
certificate of the period; it is kept, and **no redaction was made**. The PDF metadata
holds only the PD4ML creator and producer and a creation date. The mark is a well-known
third-party television brand logo, shown here as part of the public record.

## Why this document

The collection's first **trademark registration certificate**, and a different layout from
the forms around it:

- **Two columns that are not a table.** Bold left-column labels ("Reg. No.", "Int. Cl.",
  "Principal Register") sit beside a right column of prose, with no rules between them.
  Each left-column line came back as its own block, so the identifiers ground tightly.
- **Values inside prose.** The serial number and filing date share one line; the first-use
  dates share another; the disclaimer is a quoted word at the end of a sentence.
- **The mark is an image.** Whether it is a design mark, and what its words are, has to be
  read from the description paragraph and the drawing.
- **A second page of boilerplate** whose deadlines are relative to a date on page 1.

## Featured fields: the registration's identity

All on page 1. The request named no fields; its notes suggested registration number,
registration date, international class, owner, serial number and filing date.

| Field | Value |
|---|---|
| Registration number | 5,886,375 |
| International class | 21 |
| Register | Principal Register |
| Owner | Tokyo Broadcasting System Television, Inc. |
| Serial number | 87-981,735 |

Which registration, in which class, on which register, held by whom, and from which
application.

**Registration date and filing date were not featured,** though both were suggested and
both extract correctly. The schema normalizes dates to ISO (`2019-10-15` from "Registered
Oct. 15, 2019", `2017-07-18` from "FILED 07-18-2017"), so the range check reads them OFF
and a crop would print a value that does not match the text inside it. Register takes the
fifth place.

The owner crop takes in "(JAPAN CORPORATION)" on the same line, which is extracted
separately as the entity type. The serial number crop takes in the filing date beside it.

## What it surfaced

**The left column grounds cleanly.** Each label-and-value line in the bold column is a
block of its own, so every crop is a tight box around exactly one identifier.

**The goods-and-services class number grounds twice,** to "Int. Cl.: 21" and to the "CLASS 21:" prefix of the
goods paragraph. Both are right.

**First-use dates are kept as printed.** The USPTO writes `7-00-2017`, with `00` for an
unknown day; the schema asks for the printed form rather than inventing a day.

**The parse names the signatory.** The signature is an image with only the title printed
beneath it, yet the parse writes the Director's name under a `[SIGNED]` tag, read from the
signature itself. The schema extracts only the printed title.

**The seal is described, not dropped.** It appears in the markdown as a bracketed
description of the USPTO / Department of Commerce seal.

**Page 2 values read OFF as paraphrase.** The maintenance windows are extracted as phrases
("between the 5th and 6th years after the registration date") from longer sentences, and
the blocks span several lines, so the range check marks most of them OFF. The values are
right.

**`color_claimed` is null with no range,** as it should be: this certificate has no color
claim.

## Extraction

**25 leaf fields**: issuing office, registration number and date, international classes,
mark type, register, serial number and filing date; the owner (name, entity type, address,
country); goods and services per class (class, description, first use, first use in
commerce); the mark (literal element, design-mark flag, description, color claim); the
disclaimer; the signatory's title; and the three maintenance windows from page 2. All 14
top-level fields populate.

## Cost

**4.70 credits** at standard tier for 2 pages, parse and extract together.

## Regenerating

```bash
curl -sSL -o document-types/collection/trademark-registration-certificate/source/uspto-reg-5886375-registration-certificate.pdf \
  "https://tmng-al.uspto.gov/resting2/api/casedoc/cms/case/87981735/registration-certificate/5886375_87981735_101519_ORC.pdf"
.venv/bin/python document-types/scripts/run_ade.py trademark-registration-certificate                # 4.70 credits
.venv/bin/python document-types/scripts/run_ade.py trademark-registration-certificate --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py trademark-registration-certificate           # free
.venv/bin/python document-types/scripts/inspect_fields.py trademark-registration-certificate --page 1
```
