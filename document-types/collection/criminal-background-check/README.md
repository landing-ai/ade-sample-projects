# Criminal background check

Source assets for `landing.ai/document-type/criminal-background-check`.

## Sample document

`source/accurate-sample-background-check-report-redacted.pdf` is an employment
**background screening report** from Accurate Background, a consumer reporting agency.
It is the publisher's own US sample report, cut to **3 pages, portrait**: a native PDF
with a text layer, rendered from HTML. Page 1 has the FCRA / California disclosure text
in English and Spanish, a header band with the overall result ("Does Not Meet
Requirements") and order dates, and the candidate information block. Page 2 has the
requested-by block, client and reviewer notes, the summary table of all 11 searches with
their status badges, and the SSN trace. Page 3 has the **county criminal search for
Placer County, CA**: one case file with two felony charges, each with a disposition and
a sentencing block (jail, prison, fines, fees, costs, restitution, classes).

| | |
|---|---|
| Publisher | Accurate Background |
| Source | [content.cdntwrk.com/…](https://content.cdntwrk.com/files/aT0xNTIyMDYzJnY9MSZpc3N1ZU5hbWU9c2FtcGxlLWJhY2tncm91bmRjaGVja3JlcG9ydC11cyZjbWQ9ZCZzaWc9ZGQzOWQxZWVlOTdhMTNjOGE3NTc4MjBiNGZkNWM1NDg%253D) |
| Linked from | [accurate.com/resources/abm/sample-backgroundcheckreport-us](https://www.accurate.com/resources/abm/sample-backgroundcheckreport-us) ("Download PDF") |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Redacted |

**Clearance.** This is the publisher's own sample, not a customer document. The subject
is fictitious, but shares a real actor's name, and the address used a real Chicago street
and ZIP code. We replaced both with obvious stand-ins before parsing:

- the subject's name, in all four places it is printed, became **Doe, Jane** (uppercase
  where the original was uppercase)
- the street became **100 Main St**, the city **Anytown**, and the ZIP code a randomly
  drawn 5-digit stand-in from `plausible.py`
- the requestor reference, which may be a staff surname, became **SAMPLE**

`redact.py` removes the underlying text rather than covering it. The pages were redacted
one at a time so each name kept the capitalisation it had, then merged. On the dark header
band, `redact.py`'s white fill would have hidden the white name, so we cleared that text
with `--remove-marks` and wrote a white Helvetica stand-in on the band. Document metadata
was cleared.

We kept **pages 1–3 only**. Pages 4–16 cover employment, education, references, a motor
vehicle report (which returns a different, real-looking driver's identity), a drug test,
credit and global watch, and add personal data without adding anything to the criminal
record.

The SSN shown is the well-known specimen 123-45-6789 and is kept. The email and phone
were already masked at source, and the date of birth is fictitious; both are kept.
Verified: no replaced string is extractable from the committed PDF, and none appears
anywhere in this folder. The redaction rules file stays outside the repo. Accurate's site
footer says All Rights Reserved and states no reuse terms for the sample.

## Why this document

The collection's first **criminal background check**, and its first report rendered from
a web application rather than designed for print:

- **Nested records:** search → case file → charges → sentencing, with a different set of
  sentencing items on each charge (charge #1 has fines, fees, costs and restitution; charge
  #2 has a prison term).
- **Status badges** (RECORD FOUND, COMPLETED - Discrepancy Found) as the main result of
  each search, set in coloured pills rather than table text.
- **Label/value grids** built from nested HTML tables, three levels deep in the
  sentencing block.

## Featured fields: one criminal record

All on page 3.

| Field | Value |
|---|---|
| Jurisdiction searched | CA / PLACER |
| Case number | GH56327 |
| Charge | ASSAULT WITH A DEADLY WEAPON |
| Disposition | GUILTY |
| Restitution ordered | $100,000.00 |

Where the search was run, what it found, the charge, how it ended, and what the court
ordered: one record from start to finish. No named individual is featured.

The request suggested fields in its notes but set no `fields` key. Every suggestion grounds
`ok` on page 3: jurisdiction, status, case number, filing date, charge #1 description,
level, disposition and all four amounts, and the charge #2 prison term. The five shown were
chosen for the story. The rest were left out only because of the five-field limit.

## Grounding

Clean throughout. 60 of the 67 extracted leaf values ground `ok`. The only misses:

- **The sentencing items that do not exist come back null and SYNTH**, which is the right
  answer: prison on charge #1, and fines, fees, costs and restitution on charge #2. The
  model did not borrow charge #1's amounts for charge #2, even though the two blocks sit
  side by side.
- **`candidate.address`** is joined from three printed lines, so each range covers only
  one line, and `inspect_fields.py` reads `OFF`.
- **The first search name** is right, but the parse encodes its ampersand as `&amp;`, so
  the literal match misses.

Label/value rows (`STATE/COUNTY: CA / PLACER`) ground to the whole row, label included,
which is why the jurisdiction box spans both columns. The table cells in the case file
ground to the exact cell.

## Credits

6.00 credits at standard tier: parse plus extract for 3 pages.

## Schema

`schema.json` has 34 leaf fields (67 extracted values once the arrays are filled): report header, candidate, the searches summary table,
and each criminal search with its cases, charges and sentencing. Dates and amounts are
kept as printed.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py criminal-background-check       # spends credits
.venv/bin/python document-types/scripts/run_ade.py criminal-background-check --extract-only
.venv/bin/python document-types/scripts/build_images.py criminal-background-check  # free
```

The source PDF is committed already redacted. Reproducing the redaction needs the original
from the source URL and a rules file kept outside the repo.
