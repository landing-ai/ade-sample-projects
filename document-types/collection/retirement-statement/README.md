# Retirement statement

Source assets for `landing.ai/document-type/retirement-statement`.

## Sample document

`source/tiaa-participant-statement-sample.pdf` — TIAA's sample quarterly retirement
savings portfolio statement, January 1 to March 31, 2021. **15 pages, portrait (US
Letter)**: a cover with the balance and a projected retirement income chart, a portfolio
summary and asset allocation, then five workplace plans (a retirement plan, a voluntary
employee plan, a matching plan, a basic plan and a Roth supplemental annuity plan), each
with holdings, changes in value, transactions and vesting, followed by disclosures.

| | |
|---|---|
| Publisher | TIAA |
| Source | [tiaa.org/…/PDF_Participant-statement-sample2.PDF](https://www.tiaa.org/public/pdf/p/PDF_Participant-statement-sample2.PDF) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted (hidden data removed) |

TIAA's own sample, published on its public site, marked SAMPLE on every page, with the
account holder's name and plan numbers left blank. The site does not answer scripted
requests, so the file was downloaded by hand.

**The published sample was not fully scrubbed.** Page 1 carried invisible mail-merge
control data, hidden under the grey balance panel and near the footer, that included what
appears to be a real participant's name, personal email address and PIN, along with
delivery, package and routing IDs built from the PIN. It does not show on the page, but
any text extraction, including ADE's parse, reads it. The spans were deleted outright
rather than replaced, since they are delivery data rather than statement content, so
nothing visible changed. They were removed with PyMuPDF redaction annotations, which
delete the underlying text, and the PDF metadata and XMP were cleared. Verified: none of
the values is in the page text or the raw PDF bytes, no other line of text changed, and
none appears anywhere in this folder.

This is the same lesson as the consolidated 1099: a document published as a sample, or
titled as redacted, is not evidence that it is clean. The hidden layer is the leak path
a visual check misses.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **workplace retirement plan statement**, and different from the
brokerage statement at `investment-statement`:

- **Employee and employer money, side by side.** Contributions are split between the
  participant's and the employer's, per plan and in total.
- **Five plans in one statement,** each repeating the same sections with different lines
  present: one plan has only employer contributions, another only the participant's.
- **Vesting.** Two plans print a vested percent; three say it is not displayed because the
  employer holds it. Telling "not displayed" from "0%" matters.
- **A projection, not a fact.** The cover estimates monthly lifetime income at retirement,
  with a bar chart of what higher contributions would give.

## Featured fields: the quarter's portfolio activity

All on page 2. The request named no page or fields, so these were chosen:

| Field | Value |
|---|---|
| Beginning balance | $460,806.88 |
| Your contributions | $8,250.02 |
| Employer contributions | $7,425.03 |
| Gains and losses | $25,492.73 |
| Ending balance | $501,974.66 |

The quarter as one story that reconciles: $460,806.88 plus $8,250.02 and $7,425.03 in
contributions and $25,492.73 in gains is $501,974.66. Every box sits in the "This quarter"
column, not the identical "This year" column beside it.

## What it surfaced

**Missing is not zero, and the model had to be told how.** The first extraction returned
0 as the vested percent for the three plans whose statement says vesting is not currently
displayed, although the schema asked for null in that case. Reporting someone as 0%
vested is materially wrong. A second run with a firmer description still returned 0.
Making the field text (`vested_status`: "100%" or "Not displayed") fixed it.

**The watermark read as a name.** The account holder line is blank, and the first run
returned the SAMPLE watermark beside it as the account holder.

**Run-to-run drift in a label.** The second run named the first plan "TIAA CREF", after
its contract labels, instead of its heading, RETIREMENT PLAN. Anchoring the description
to the numbered plan heading fixed it.

**The allocation table grounds one cell adrift.** On page 2 each asset class, value and
percent grounds to the cell after it: Equities to "$351,832.90", 70.09 to "Fixed
Income". The values are right, the boxes are not, so none of it is featured.

**Every plan balance adds up.** The five plans' ending balances sum to the $501,974.66
total, and the participant's contributions to two plans sum to the $8,250.02 on page 2.

## Extraction

**24 leaf fields**: provider, holder, period, total balance and rate of return, the
income projection, the portfolio summary, the asset allocation, and per plan its
balances, contributions, gains, vesting and tax treatment. Everything extracts correctly
in the committed run.

## Cost

**29.50 credits** at standard tier for 15 pages: 18.70 to parse, 10.80 to extract. Two
earlier extractions during schema revision cost 21.60 more, for 51.10 in all.

## Regenerating

```bash
# The source is a manual download from the url, with the hidden page 1 control data
# deleted by a script kept outside the repo. The committed PDF is the cleaned one.
.venv/bin/python document-types/scripts/run_ade.py retirement-statement                # 29.50 credits
.venv/bin/python document-types/scripts/run_ade.py retirement-statement --extract-only # 10.80, schema iteration
.venv/bin/python document-types/scripts/build_images.py retirement-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py retirement-statement --page 2
```
