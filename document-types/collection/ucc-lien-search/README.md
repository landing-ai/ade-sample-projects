# UCC lien search

Source assets for `landing.ai/document-type/ucc-lien-search`.

## Sample document

`source/microbilt-ucc-report-2024.pdf`: MicroBilt's sample UCC Search Report. **2 pages,
portrait (US Letter)**, born-digital. Page 1 and the top of page 2 hold a results table of
five UCC financing statements filed in Washington, each with its debtor, filing state and
date, creditor, document numbers and filing, debtor and secured-party counts. The rest of
page 2 is the detail record for one of those filings: original document number and date,
filing state, four debtor parties, the secured party, and the filing event with its type
code.

| | |
|---|---|
| Publisher | MicroBilt Corporation |
| Source | [microbilt.com/.../UCC-Report-2024.pdf](https://www.microbilt.com/Cms_Data/Contents/Microbilt/Media/Docs/SampleReports/UCC-Report-2024.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

**A vendor's own published specimen, and nothing was redacted.** MicroBilt links this PDF
from its UCC product page, and a reseller (lsiservices.net) links it from its samples page.
It is filled with specimen data: names such as ANY COMPANY and WALLY WORLD MEGA VISION
CINEMA, ANYSTREET addresses with ZIP 12345, and document numbers masked as XXXX. The only
phone number is MicroBilt's toll-free sales line in the footer. The PDF metadata carries
only InDesign producer data. Full provenance is in `manifest.json` under `source.origin`;
this section is the human-readable version.

## Why this document

The collection's first **UCC lien search**, and the first search-result report. It has
two layouts on two pages:

- **A results grid built from free-floating text.** Each result is a block of loose text
  in three shaded columns, with label and value pairs such as `DOC NUMBER:` and
  `FILING COUNT [ 1]`. One block breaks across the page, so its counts sit on page 2.
- **The same filing, twice.** Document 98-168-XXXX appears as results 2 and 5, under
  different debtor names, and again in the detail record. Extraction has to keep the two
  results apart instead of merging them.
- **A labelled detail record** with key and value pairs set side by side in two columns.

It is a thin sample: every `COLLATERAL:` label is blank, and there are no lapse dates and
no search through-date. The schema does not ask for those.

## Featured fields: the filing detail record

All on page 2. The request named no fields. It offered four as suggestions and pointed at
page 2's detail block, which is what is featured:

| Field | Value |
|---|---|
| Original document number | 98-168-XXXX |
| Original date filed | 1998-06-17 (printed 06/17/1998) |
| Filing state | Washington |
| Filing type code | 0801 |
| Secured party | ANY COMPANY |

Together these describe one financing statement: what it is, when and where it was filed,
and who holds the lien. The suggested **type of filing** (UCC FINANCE STATEMENT FILED)
was not featured, because it grounds OFF: the value wraps over two lines and each of its
two ranges covers only part of it. The filing type code from the same Events row is
featured in its place. The secured party is a specimen organization name, not a person.

## What it surfaced

**The word "null" in a description backfired.** In the first extraction, three results
with no bold debtor name came back with the string `"null"` instead of an actual null.
A description telling the model to "return JSON null, never the text 'null'" made it
worse: every blank debtor name and collateral came back as `"null"`. It also merged
result 5 into result 2, because they share a document number, so only four of the five
results came back. Rewording to "leave it empty when…", and saying that the array should
match the count in the heading and must not merge repeated document numbers, fixed both.
The blank collaterals still come back as a mix of null and `""`.

**Grounding is clean on the labelled pairs.** Every key and value pair in the detail
block grounds `ok`, and each box takes in the label with its value. Values that wrap over
two lines, such as the type of filing and the debtor addresses in the results grid, ground
OFF, because each range covers one line.

**Repeated values ground to every copy.** Result 2's document number and counts have
ranges on page 2 as well, where result 5 repeats the same filing. The fields are right,
but they are not unique to one block.

## Extraction

**27 leaf fields**: the report provider, the result count, an array of search results
(13 fields each) and the filing detail with arrays of debtor parties, secured parties and
events. Every value matches the page, with the collateral caveat above.

## Cost

**12.80 credits** at standard tier for 2 pages: 5.70 for the first parse and extract,
then 3.30 and 3.80 for two extract-only schema revisions. The committed output is the
first parse with the last extraction, which cost 3.80 credits.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py ucc-lien-search                # parse + extract
.venv/bin/python document-types/scripts/run_ade.py ucc-lien-search --extract-only # 3.80, schema iteration
.venv/bin/python document-types/scripts/build_images.py ucc-lien-search           # free
.venv/bin/python document-types/scripts/inspect_fields.py ucc-lien-search --page 2
```
