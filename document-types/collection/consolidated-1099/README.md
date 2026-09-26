# Consolidated 1099

Source assets for `landing.ai/document-type/consolidated-1099`.

## Sample document

`source/consolidated-1099-edward-jones-redacted.pdf` — a 2024 Edward Jones Consolidated
1099 Statement. **13 pages, landscape.**

| | |
|---|---|
| Publisher | Edward Jones |
| Source | [scribd.com/document/868128892](https://www.scribd.com/document/868128892/XXXX8634-Consolidated-1099-Statement-Figures-Are-Final-01-23-2025) |
| Retrieved | 2026-09-25 |
| Clearance | **Redacted** — see below |

## This document was redacted before it entered the repo

> **The original was not redacted at source, despite the Scribd listing being titled
> `XXXX8634`.** It carried a named individual's complete tax records.

What it contained, and what replaced it:

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Recipient's full name | 11 | `JANE DOE` |
| Full brokerage account number | 10 | `000-00000-0-0` |
| Financial advisor's name | 1 | `PAT EXAMPLE` |
| Advisor's direct line | 2 | `(000) 000-0000` |
| Real last four of the TIN | 1 | `***-**-0000` |
| Home address | page 1 | page dropped |

Done with `document-types/scripts/redact.py`, which uses PyMuPDF redaction annotations —
these **remove the underlying text** rather than drawing a box over it. Text hidden under
a filled rectangle is still in the file and still extractable, which is the usual way a
"redacted" PDF leaks. The script re-extracts afterwards and fails if any original string
survives. It verified clean, and a separate sweep over every file in this folder — the
PDF, the parse output, the extraction and the manifest — confirmed that none of the
original identifiers appear anywhere.

**The account number was also in the PDF metadata.** `/Info` carried
`author: 04822863413` — the account number from the page with its separators stripped,
which is why every search for the hyphenated form missed it. Producers commonly stash
customer and account ids there, and it survives any amount of page-level redaction.
`redact.py` now clears the metadata dictionary and XMP outright, and its verification
compares digits as well as literal strings, so an identifier stored without punctuation
cannot slip through.

**Page 1 was dropped rather than redacted.** It is a mailing panel: its text is rotated
90°, so replacement text either wrapped into fragments or failed to render at all, and it
carried the home address while adding nothing to the demonstration. Removing it deletes
that data outright instead of relying on substitution.

A useful side effect: with the cover gone, PDF page numbers now match the printed ones.
Page 4 of the file is "Page 4 of 10" on the page.

## Why this document

The pilot's medium-length case with a long schema — and the one where the schema is
someone else's, not written for this exercise. `schema.json` is the marketing team's
existing consolidated-1099 schema, used unchanged: 17 top-level groups covering 1099-INT,
1099-B, 1099-OID, 1099-DIV and 1099-MISC, resolving to **316 leaf fields**.

All 17 populate.

## Featured fields: one complete transaction

Page 4 carries the long-term 1099-B detail — six sale rows across five securities. The
featured fields follow a single row end to end, so the overlay reads as one story rather
than five unrelated values:

| Field | Value |
|---|---|
| Security sold | AMERICAN CAP INC BUILDER A / 140193103 / CAIBX |
| Date acquired | 09/02/2023 |
| Gross proceeds | 3,071.56 |
| Cost basis | 2,982.67 |
| Gain | 88.89 |

## Grounding here is good

Worth recording as a contrast. On the investor presentation, array elements in charts and
dense tables ground one cell adrift. On this document the `form_1099_b.details` array
grounds **correctly** throughout — `details[1].proceeds` boxes `3,071.56`, `cost_basis`
boxes `2,982.67`, and so on.

The difference appears to be the source: a ruled financial table in a real form grounds
well, while values a model reads off a chart do not.

Two fields on this page are flagged by the consistency check and are correct anyway:
`holding_period` and `covered_security` ground to the section header
`Long Term (Box 2) / Covered (Box 12)`, which is genuinely where those values come from
even though the literal text differs. Neither is featured.

## Cost

**38.90 credits** at standard tier: 13 pages with a 19 KB schema.

## Regenerating

```bash
# Redaction, from the original in the Marketing shared drive:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    source/consolidated-1099-edward-jones-redacted.pdf \
    --rules rules.json --drop-pages 1

.venv/bin/python document-types/scripts/run_ade.py consolidated-1099
.venv/bin/python document-types/scripts/build_images.py consolidated-1099
.venv/bin/python document-types/scripts/inspect_fields.py consolidated-1099 --page 4 --good
```

`manifest.json` records **what** was replaced and with what, under
`source.origin.redactions` — deliberately not the original values.

> **The rules file stays out of the repo.** `rules.json` maps each original string to its
> replacement, so it is a verbatim copy of the personal data this exercise removed.
> Committing it, or pasting the originals into a README or manifest "for provenance",
> republishes exactly what the redaction took out. Keep it alongside the original PDF in
> the Marketing shared drive.

An earlier draft of this folder made that mistake in both files, and the first sweep
checked only the PDF's page text — missing both the manifest copy and the account number
sitting in the PDF metadata. Hence the rule: **sweep every file in the folder, and compare
digits as well as literal strings.**
