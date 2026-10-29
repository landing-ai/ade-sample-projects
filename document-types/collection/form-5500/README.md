# Form 5500

Source assets for `landing.ai/document-type/form-5500`.

## Sample document

`source/form-5500-st-olaf-403b-2023-redacted.pdf`: the Form 5500 Annual Return/Report of
Employee Benefit Plan for the St. Olaf College 403(b) Retirement Plan, plan year 2023,
with its attached schedules. **24 pages, portrait.**

| | |
|---|---|
| Publisher | St. Olaf College (the plan sponsor) |
| Source | [2023-403b-5500-Website.pdf](https://wp.stolaf.edu/finance/files/2024/10/2023-403b-5500-Website.pdf), on the college's finance site; no linking page was found |
| Retrieved | 2026-10-28, by script |
| Clearance | **Redacted**: a public ERISA filing, with the one individual's name replaced |

| Pages | Content |
|---|---|
| 1–3 | Form 5500: plan and sponsor identification, signatures, participant counts, plan characteristics, attached schedules |
| 4–7 | Schedule A, Insurance Information (TIAA-CREF contract) |
| 8–13 | Schedule C, Service Provider Information |
| 14–16 | Schedule D, DFE/Participating Plan Information |
| 17–21 | Schedule H, Financial Information |
| 22–24 | Schedule R, Retirement Plan Information |

Form 5500 filings are open to public inspection under ERISA, and the college posts this
one itself. The filing names one individual: the person who signed it, printed twice on
page 1, as plan administrator and as plan sponsor. That name was replaced with
**JANE Q. SAMPLE** in both places; the electronic-signature notice and the signature
dates beside it were kept. The college's own name, EIN, address and telephone, and the
organizations in the schedules (an insurance carrier, an investment consultant and an
audit firm), are institutional and were kept. Schedules A and C name no individual
broker or agent. The PDF's metadata, which named a person as author, was cleared.

**How the redaction was done.** Every filled-in value in this PDF is drawn as vector
glyph outlines, not text (the producer was Microsoft Print To PDF), and each line of
values is one compound path: the e-signature notice, the date and the name are a single
path. `redact_outlined.py` gained a `--split-compound` option for this. It finds the
name by OCR and cuts just that name's glyph subpaths out of the page content stream,
then draws the replacement in Helvetica. Verified by OCR, and by text and content-stream
search: the original name survives nowhere in the committed PDF or in this folder.

**A hidden text layer.** Under every field sits invisible white text holding EFAST
placeholder strings (`ABCDEFGHI`, `123456789`, `YYYY-MM-DD`) rather than the values. It
carries no personal data and was left in place. Parse ignored it completely: no
placeholder appears in `parse-pro.md`.

## Why this document

It is the collection's first ERISA benefit-plan filing. Other tax forms in the collection
are a single return; this one is a main form plus five schedules, each with its own
header, and it mixes participant headcounts, plan-characteristic codes, checkbox grids,
a repeating service-provider block (Schedule C), and a two-column balance sheet and
income statement (Schedule H). It also tests a document whose visible values have no
text layer at all.

`schema.json` covers the plan year and filer type, plan and sponsor identification, the
signature rows, the line 5–6 participant counts, plan characteristic codes, funding and
benefit arrangements, attached schedules, and key lines of Schedules A, C, D, H and R.
**79 leaf fields** (counted from the schema), all 18 top-level fields populated.

## Featured fields: the plan's headcount

All on page 2.

| Field | Value |
|---|---|
| Participants at start of year (line 5) | 2080 |
| Active participants at year end (6a(2)) | 798 |
| Total participants (6f) | 2096 |
| Participants with account balances (6g(2)) | 2094 |
| Schedule H attached (10b) | H |

These are the fields the request's notes suggested; the request named none outright.
Each count grounds to its own cell and the checkbox grounds to the Schedule H row of
line 10b. The crops and the page overlay were checked by eye. No person is featured.

## Grounding and extraction notes

- **Every participant count on page 2 grounds to its own cell**, including the zeros on
  6b and 6h.
- **Line 10's attached-schedule checkboxes ground well** (each to its own row), but the
  same kind of checkbox on line 9a grounds once to a bare `[x]` and once to the label,
  and the line 3a "Same as Plan Sponsor" and line D "Form 5558" checkboxes ground to the
  line caption rather than the box.
- **Schedule C is the weak spot.** TIAA's ten service codes are printed packed into one
  narrow cell; extraction lists all ten correctly but only the first has a range, the
  rest are synthesized. The same happens to every provider's second code ("27 50"
  grounds only 27). For the second provider, the compensation, relationship and service
  code ranges resolve to no page at all, although the values are right; the third
  provider grounds cleanly.
- **Schedule H** reads cleanly across both columns, from total assets to net income, and
  the Disclaimer opinion checkbox, the auditor and its EIN extract correctly.
- Extraction is correct throughout as far as checked against the page, including the
  Schedule A unallocated-contract rollforward and the Schedule R opinion letter.

## Credits

50.60 credits at standard tier (parse and extract, 24 pages).

## Regenerate

```bash
# redaction (rules file kept outside the repo)
.venv/bin/python document-types/scripts/redact_outlined.py <original>.pdf \
    document-types/collection/form-5500/source/form-5500-st-olaf-403b-2023-redacted.pdf \
    --rules <outside-the-repo>/rules.json --split-compound

.venv/bin/python document-types/scripts/run_ade.py form-5500
.venv/bin/python document-types/scripts/build_images.py form-5500
```
