# Client Risk Profile (Handwritten)

Wells Fargo Advisors' **Client Profile/Risk Assessment** questionnaire, **filled in by hand** and
scanned. It has two parts:

- **Client contact details:** name, phone, address and email.
- **Twelve risk-tolerance questions:** age band, time horizon, investment purpose, risk
  acceptance, preferred portfolio, tolerable drawdown, hypothetical return table, income needs,
  experience, share of assets, total assets and income stability.

Most answers are ticked checkboxes, with handwritten write-ins beside a few. The source is 4
portrait pages, raster scans with no text layer.

## Provenance

| | |
|---|---|
| Publisher | LandingAI; the form itself is Wells Fargo Advisors' questionnaire |
| Source | Not published online. A specimen filled in by hand by LandingAI staff, from LandingAI's internal marketing document library (doc38) |
| Retrieved | 2026-11-16 |
| Clearance | `public` |

A LandingAI staff member filled in the blank questionnaire by hand with **invented data**, in
blue pen, and scanned it. The client's name, address, phone number (the 555 range), email address
and every answer are fictitious. No real client's data is present, so nothing was redacted. The
PDF metadata was cleared. The Wells Fargo Advisors name and logo appear because they are printed
on the form; Wells Fargo did not produce or endorse this specimen.

## Why this document

It is a long checkbox questionnaire filled in by hand. Each answer is a pen tick against one of
four or five printed options. Free-text write-ins sit beside some answers ("Secondary:",
"Years of Experience:", "Assets:"). One question (7) is answered by ticking a row of a table of
hypothetical returns. Reading it means finding *which* option carries the tick, not just reading
text.

## Schema

The schema was supplied with the request and used unchanged. It has 26 leaf fields: the contact
details, plus each question's answer with its write-in and a normalized value where there is one
(e.g. `q10_normalized`).

It contains one property with an **empty name** (`""`). That key extracts as `null`, but it
carries about 38 grounding ranges scattered over pages 1–2: the logo, the contact lines,
unticked options and question stems. It reads like an editing slip in the schema and was left as
supplied. A consumer would want it named or removed.

## Featured fields (page 1)

| Field | Value |
|---|---|
| Age band | Between 46 and 55 |
| Time horizon | Long Term (10+ years) |
| Primary purpose | Build Long-Term Wealth |
| Secondary purpose | preservation of wealth (handwritten) |
| Risk acceptance | More accepting of risk – Long Term |

These are page 1's risk profile in one column: four hand-ticked options and the handwritten
write-in between them. No personal field is featured.

## Grounding on this document

**Ticks ground to the chosen option, line for line.** Every checkbox answer grounds `ok` to the
ticked option ("[x] Between 46 and 55", "[x] > 50%", "[x] Very Stable"). The boxes sit exactly
on that option, and none drifts onto a neighbouring line. Compare the handwritten Chase mortgage
assistance form in this collection, whose lower checkboxes landed one and two rows low.

**Write-ins ground to their lines.** The handwritten write-ins ("preservation of wealth", "20",
"3.5M") and the contact details each ground to their own line.

**Normalized values ground `OFF`, and that is correct.** "Texas" is extracted as "TX", and
"3.5M" as 3500000. Neither normalized value is printed on the page.

**The tick in the returns table grounds `OFF`.** For question 7, the tick marks the fourth row of
the hypothetical-returns table. The answer is right ("row 4"), but it grounds to the whole table
and the next question, not to the ticked row.

## Credits

6.70 credits at standard tier: parse plus extract, 4 pages.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py client-risk-profile-handwritten
.venv/bin/python document-types/scripts/inspect_fields.py client-risk-profile-handwritten --page 1
.venv/bin/python document-types/scripts/build_images.py client-risk-profile-handwritten
```
