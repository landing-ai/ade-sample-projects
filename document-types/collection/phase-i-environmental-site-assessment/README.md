# Phase I Environmental Site Assessment

A Phase I Environmental Site Assessment (ESA) by Kimley-Horn and Associates, Inc. for
Norman Y. Mineta San José International Airport: **San Jose Airport Orange Lot, Martin
Avenue and De La Cruz Boulevard, Santa Clara, California** (Kimley-Horn project
097042828, issued June 30, 2025). The assessment covers a 3.6-acre parking lot and
taxiway strip at the northwest corner of the airport, performed under ASTM E1527-21 and
the EPA's All Appropriate Inquiries rule. It finds no RECs or HRECs, one CREC (residual
contamination from a nearby Unocal station that reached the property) and one business
environmental risk (a 2016 firefighting foam release at a neighbouring hangar).

**39 pages**, portrait, US Letter, with a text layer. The file is the report body only:
the appendices it lists (figures, photographs, EDR reports, closure documents, resumes)
were not posted, and all 39 pages are kept.

## Provenance

| | |
|---|---|
| Publisher | Kimley-Horn and Associates, Inc. (consultant); posted by Norman Y. Mineta San José International Airport |
| Source URL | https://www.flysanjose.com/sites/default/files/users/user143716/Orange%20Lot%20ESA%20Report.pdf |
| Context | Posted on the airport's own website; no linking page was found |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | `public` |

A consultant's report prepared for a city-owned airport and published by the airport on
its own domain. The PDF's pages are committed exactly as downloaded; only its document
metadata was cleared (see below).

**Personal data.** The report names the Environmental Professional who conducted it
(executive summary, reconnaissance table and declaration page, which also carries her
signature) and one airport staff member interviewed in her professional role. Both are
professional details in a public agency record, and by the operator's decision the
document is published unredacted, as the publisher filed it. The PDF's hidden /Info and
XMP metadata, which named the Environmental Professional as author, was cleared, also by
the operator's decision; the visible pages are unchanged. The assessor's parcel number is a public parcel
identifier. No person is featured on the page.

## Why this document

It is the long, narrative end of the real-estate due-diligence set. Most of the
collection is forms and tables; a Phase I ESA is 39 pages of prose in which the facts a
lender or buyer needs are scattered: the client and acreage sit in the first sentence of
the executive summary, the viability dates in a small table below it, the regulatory
database counts in a table that runs across three pages, and the opinion on each of 22
nearby release sites in a two-column table whose rows break across pages. The findings
are stated twice (executive summary and Section 7), so extraction also has to collapse
repeated statements into one answer. It also tests resistance to a source error: page 7
carries a paragraph pasted from another report, citing ASTM E1527-13 and a Mission Viejo
address.

## Featured fields

All five are on **page 6**, the executive summary (printed page 1):

| Field | Label | Value |
|---|---|---|
| `report.client` | Client | City of San Jose |
| `property.acreage` | Property size (acres) | 3.6 |
| `report.astm_standard` | ASTM standard | E 1527-21 |
| `component_dates.visual_inspection` | Site reconnaissance date | May 12, 2025 |
| `component_dates.ep_declaration` | EP declaration date | November 8, 2025 |

These are the fields the request suggested, and all five grounded on page 6. Together they
are the engagement and its clock: who commissioned the work, on how much land, under which
standard, and the component dates from which the report's 180-day viability runs. The
acreage is pinned to its fourth occurrence, the one in the executive summary sentence.
The EP declaration date is printed as November 8, 2025, the same as the viability date on
the cover and later than the issue date. That is the source's own figure, and the
extraction reports it as printed.

## Grounding notes

- **Prose fields box the sentence line, table fields box the cell.** Client, acreage and
  standard are values inside running text, so their crops are full-width line boxes with
  the value somewhere in the line. The two dates box their own table cells exactly.
- **The stray E1527-13 did not leak.** Extraction took the standard from the executive
  summary, not from the copy-pasted paragraph on page 7.
- **A half became a control character.** The parse reads "½ mile" correctly in the
  regulatory database table, but extraction returned `search_distance` as U+0095 followed
  by " mile" for all 8 such rows, so those rows ground OFF. The 22 rows themselves, spread
  across pages 20 to 22, all came back with the right counts.
- **The nearby-sites table mostly survived its page breaks.** The table prints 22
  facility entries over pages 23 to 31; extraction returned 21, each with address,
  distance, GeoTracker case number and contaminant, including entries whose name and
  notes are split across a page break, and only the Unocal station is marked as the
  REC/CREC. The miss: TTM Technologies (407 Mathew Street) and Sigma Circuits (393
  Mathew Street) are adjacent entries whose notes cross-reference each other, and they
  came back as one row carrying TTM's address and Sigma's LUST case number. A reviewer
  should check adjacent entries that share a case.
- **Summary judgements ground OFF, as expected.** Booleans (`recs_identified`, `is_rec`)
  and the CREC and BER summaries point at the paragraphs that support them rather than at
  a literal value.

The schema has **43 leaf fields**.

## Credits

Standard tier, jobs API, DPT-3 Pro: **74.70 credits** for one parse and one extract of
the 39 pages.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py phase-i-environmental-site-assessment        # spends credits
.venv/bin/python document-types/scripts/build_images.py phase-i-environmental-site-assessment   # free
.venv/bin/python document-types/scripts/inspect_fields.py phase-i-environmental-site-assessment --page 6
```
