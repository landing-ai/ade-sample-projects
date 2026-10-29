# Litigation complaint

Source assets for `landing.ai/document-type/litigation-complaint`.

## Sample document

`source/us-v-hpe-juniper-complaint.pdf` — the complaint in *United States of America v.
Hewlett Packard Enterprise Co. and Juniper Networks, Inc.*, No. 3:25-cv-00951 (N.D. Cal.),
the Justice Department's suit to block HPE's $14 billion acquisition of Juniper.
**21 pages, portrait (612×792).** Produced from Word, with a full text layer, on
28-line numbered pleading paper, with the court's ECF filing stamp across the top of
every page.

| | |
|---|---|
| Publisher | U.S. Department of Justice, Antitrust Division |
| Source | [justice.gov/atr/media/1406591/dl](https://www.justice.gov/atr/media/1406591/dl?inline) |
| Case page | [US v. Hewlett Packard Enterprise Co. and Juniper Networks, Inc.](https://www.justice.gov/atr/case/us-v-hewlett-packard-enterprise-co-and-juniper-networks-inc), linked as "Complaint (January 30, 2025)" |
| Filed | 2025-01-30 |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

A U.S. government work, published by the DOJ on its case page. It is used **exactly as
published, all 21 pages, unredacted**, by decision of the document owner. The only
individuals it names are the government attorneys of record, in their official
capacity: counsel and their bar numbers, an office email, telephone and fax on page 1,
and the signature block with an `/s/` e-signature on page 21. The body was screened for
named company executives: they are referred to by title only ("Senior Vice President of
Worldwide Sales"), never by name. The PDF metadata is left as published.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

- **Pleading paper.** Line numbers down the left margin, a ruled border, a footer
  title on every page, and an ECF stamp above it all. Every one of those is text the
  parser has to keep apart from the pleading itself.
- **A side-by-side caption.** The parties sit in a ruled box on the left, the case
  number and title on the right. The caption's case-number box is **blank**, as it is
  on any complaint at the moment of filing: the number exists only in the court's
  stamp, so the schema has to send the model there.
- **Mostly prose.** After page 1 the facts are numbered paragraphs. Statutes, markets
  and relief have to be found in sentences, not read off labels.

## Featured fields: the caption

All on **page 1**:

| Field | Value |
|---|---|
| Court | NORTHERN DISTRICT OF CALIFORNIA |
| Case number | 3:25-cv-00951 |
| Plaintiff | UNITED STATES OF AMERICA |
| First defendant | HEWLETT PACKARD ENTERPRISE CO. |
| Second defendant | JUNIPER NETWORKS, INC. |

Which court, which case, who is suing whom. The case number comes from the ECF stamp,
and grounds to just that word span (`Case 3:25-cv-00951`), not the whole stamp line. The
request also suggested the filed date; with two defendants that is six fields against a
cap of five, so it was left out. It extracts and grounds correctly (`01/30/25`, from the
same stamp line). The court is featured through its second caption line, since the first
(`IN THE UNITED STATES DISTRICT COURT`) names no particular court. No individual's name
is featured.

## Grounding notes

- **Values copied as printed ground; normalized values do not.** The first extraction
  asked for the court as a tidied name and the filed date as `YYYY-MM-DD`. Both values
  were right and both grounded OFF: the boxed text (`Filed 01/30/25`, two caption lines in
  capitals) no longer contained them. Asking for them as printed, and splitting the
  court's two caption lines into `court` and `court_district`, made both ground `ok`.
- **Duplicates and a garbled character.** The first run also listed Section 7 of the
  Clayton Act twice under `claims`, once with its `§` turned into a control character
  (U+0016). The parse markdown has a clean `§` in all 12 places, so this came from
  extraction. Asking for each distinct provision once gave one clean entry.
- **Long prose values ground loosely.** Each request-for-relief item, the jurisdiction
  and venue bases and the one-sentence `nature_of_action` ground to the paragraph they
  came from rather than to text that contains them verbatim, so they read `OFF`. Short
  values in prose — the statute name, its citation, the paragraph count of 63, the
  `$14 billion` deal value — ground to their sentences cleanly.
- **The second defendant's box includes the `and`** that begins its caption line
  (`and JUNIPER NETWORKS, INC.`). The value itself is right.

## Schema

`schema.json` was written for this sample: 19 top-level fields, **23 leaf fields** —
the caption and filing stamp, counsel's office, the challenged transaction, the alleged
product and geographic markets, the claims with citations, jurisdiction and venue, the
lettered requests for relief, the paragraph count and the signature date. It asks for
no individual's name.

## Credits

At standard tier: **34.90** for the first parse and extraction, plus **12.00** for one
extract-only re-run after the schema changes, **46.90** in all.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py litigation-complaint                 # parse + extract
.venv/bin/python document-types/scripts/run_ade.py litigation-complaint --extract-only  # extract only
.venv/bin/python document-types/scripts/build_images.py litigation-complaint            # images, no API
```
