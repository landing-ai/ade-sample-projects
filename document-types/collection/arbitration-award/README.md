# Arbitration award

Source assets for `landing.ai/document-type/arbitration-award`.

## Sample document

`source/25-01517.pdf` — a FINRA arbitration award, case 25-01517: a customer's claim
against a broker-dealer and three of its associated persons, heard in Providence, Rhode
Island. **5 pages, portrait (612×792).** Produced from Word, so it has a full text layer.

| | |
|---|---|
| Publisher | FINRA Dispute Resolution Services |
| Source | [finra.org/…/aao_documents/25-01517.pdf](https://www.finra.org/sites/default/files/aao_documents/25-01517.pdf) |
| Retrieved | 2026-09-26 |
| Clearance | Public |

FINRA publishes every arbitration award in its public Arbitration Awards Online
database. This one is used **exactly as published, unredacted**. That was a deliberate
decision by the document owner, not an oversight. The award names the claimant, who is a
private individual, three individual respondents, the respondent member firm, counsel
and their firms, and the three arbitrators, all as they appear in the public record. The
PDF metadata `author` field, the FINRA staff member who prepared it, is also left as
published.

It is recent: the award was served on 2026-09-25, the day before it was retrieved.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first legal document, and the first whose value is mostly in prose:

- **Structured caption, narrative body.** Page 1 is a labelled caption: case number,
  parties, hearing site, nature of dispute. Pages 2 to 4 are paragraphs: causes of
  action, relief requested, the award itself and the fee allocation.
- **A real team schema.** `schema.json` is the team's arbitration-awards schema from
  `Applications/UI for Rapid Human View of Extracted Fields/schemas/`, used unchanged:
  10 top-level groups, 59 leaf fields. It is written to cover expungement awards as well
  as customer cases.
- **Clean input.** A born-digital Word export, the opposite of the engineering drawing,
  so any grounding trouble here comes from the schema and the prose rather than from
  reading the page.

## Featured fields: the case caption

All on **page 1**:

| Field | Value |
|---|---|
| Case number | 25-01517 |
| Claimant | Steven Damiani |
| Respondent firm | Janney Montgomery Scott LLC |
| Nature of dispute | Customer vs. Member and Associated Persons |
| Hearing site | Providence |

Each grounds to its own line in the caption, so the overlay reads as the case at a
glance. `hearing_site_state` is not featured because it shares a line with the city and
would render the identical crop. The claimant is pinned to occurrence 0, the caption;
the name also appears twice in the representation paragraph below it.

**Why not page 2, where the money is.** Page 2 carries the outcome, and
`compensatory_damages` grounds correctly to the $642,000.00 line. Almost everything else
on the page is a long narrative string or a boolean, and those crop badly, for the reason
below.

## What it surfaced

**Short labelled values ground precisely; long prose grounds line by line.** Every
caption field boxes exactly its line. A narrative field such as
`relief_requested.claimant_requested_relief` comes back with eight ranges, one per line
of the paragraph. That is correct, but no single crop shows the value, and the
consistency check flags each line as a partial match. Fields like these can be
extracted but not illustrated.

**Booleans ground to their evidence.** `respondent_cost_assessment_request: true` boxes
the sentence asking for forum fees to be assessed against the claimant. That is useful
traceability, but the crop shows a sentence next to the word "True", so booleans are not
featured.

**Normalized dates no longer match the page.** The schema asks for ISO dates, so
`October 27, 2025` comes back as `2025-10-27` and gets flagged, like `revision_date` on
the engineering drawing. The values are right.

**A single-value field with several answers.** `respondent_submission_agreement_signed_date`
is one string, but four respondents signed on three dates. Extraction joined them into
`2025-10-23, 2025-10-23, 2025-10-24, 2025-10-28` without saying which respondent signed
when. That is a schema limitation, not an extraction error.

**Three values to read with care:**
- `claimant_injunction_denied` came back `true` although no injunction was requested.
  It grounds to the catch-all "any and all claims for relief … are denied".
- `filing_fee_retained_by_finra` came back `0` although the award does not state one.
  It grounds to the filing fee footnote.
- The monetary fields for relief that was not awarded come back as `0` rather than null.

**Expungement fields are null, with a warning.** This is a customer case, so all five
`decision.expungement` fields are null. The schema marks `affirmative_finding_of_fact`
non-null, so extraction returns a `nonconformant_output` warning. The null is correct,
and the team's schema is kept unchanged.

## Cost

**10.40 credits** at standard tier for 5 pages: 4.50 to parse, 5.90 to extract. The
extract share is high for so few pages because the schema is 13.5 KB.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py arbitration-award                # 10.40 credits
.venv/bin/python document-types/scripts/run_ade.py arbitration-award --extract-only # 5.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py arbitration-award           # free
.venv/bin/python document-types/scripts/inspect_fields.py arbitration-award --page 1 --good
```

`manifest.json` sets `preview_pages` to 1, 2, 3 and 5, skipping page 4, which is mostly
blank, in favour of the arbitration panel and signatures.
