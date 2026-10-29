# Equity Incentive Plan

Source assets for `landing.ai/document-type/equity-incentive-plan`.

## Sample document

`source/alcoa-stock-and-incentive-compensation-plan-2026.pdf`: the **Alcoa Corporation
Stock and Incentive Compensation Plan (as Amended and Restated)**, dated May 6, 2026.
**18 pages, portrait**, native text, single column.

This is the plan document itself, the instrument stockholders approve and every equity
grant is made under: purpose and definitions, administration, the share reserve and
share-counting rules, eligibility, the terms of each award type (options, stock
appreciation rights, restricted shares, restricted share units, performance and cash
incentive awards), change-in-control treatment, performance goals, amendment, general
provisions and the plan term.

| | |
|---|---|
| Publisher | Alcoa Corporation |
| Source | [alcoa.com, plan PDF](https://www.alcoa.com/equity-plan/pdfs/alcoa-corporation-stock-and-incentive-compensation-plan-as-amended-and-restated-06-May-2026.pdf), linked from [alcoa.com/equity-plan](https://www.alcoa.com/equity-plan/) |
| Retrieved | 2026-10-28, by script |
| Clearance | **Public** |

Alcoa publishes the plan on its own equity-plan page for stockholders and participants.
It names no individual, carries no signatures, and its PDF metadata holds only Word's
placeholder author. Nothing was replaced and the file is unchanged from the download.

## Why this document

The other contracts in the collection are forms with values typed into blanks. This one
has no blanks: every number a reader wants is buried in running legal prose, often
several to a sentence, and qualified by the clauses around it. The share-counting rule
alone packs three ratios and six dates into four lines. It tests whether extraction can
pull clean figures out of dense drafting, and whether grounding can point at the exact
line within a long paragraph rather than at the paragraph.

## Schema

`schema.json` covers the plan's identity (name, former name, company, state of
incorporation, restatement date), eligibility and award types, the share reserve (total
reserve, incentive stock option limit, the full-value award counting ratios by period,
and the option/SAR counting rate), the director award cap, minimum vesting and its
carve-out, option and SAR terms and the 10% stockholder rules, par value, the Fair
Market Value exchange, the change-in-control ownership trigger, the clawback policy,
governing law, the last grant date and the approving meeting date.

**27 leaf fields** (counted from the schema). Every field came back populated.

## Featured fields: the share pool, from page 5

| Field | Value |
|---|---|
| Shares reserved | 38,000,000 |
| Incentive stock option limit | 38,000,000 |
| Full-value award counting ratio | 1.69 |
| Ratio effective from | May 6, 2026 |
| Director annual award cap | $750,000 |

Read together: how big the pool is, how much of it may go out as incentive stock
options, how fast restricted stock and other full-value awards draw it down under the
ratio this restatement introduced, and how much any one director can be granted a year.
These are the terms a proxy adviser or compensation analyst reads a plan for, and they
all sit in Section 4(a) and the paragraph just above it on one page.

The request suggested page 5 with the reserve, the ISO limit, the counting ratio and the
director cap. All four ground correctly on page 5 and shipped; the ratio's effective
date was added as a fifth. No person is featured.

## Grounding notes

- **Line-level grounding inside prose works well.** Each featured value boxes the
  single line of the paragraph that holds it, not the paragraph. All five crops contain
  their value and the OCR check passed on every one.
- **Pin the occurrence.** Several values ground twice, once on the line that holds them
  and once on a neighbouring line of the same sentence. The incentive stock option limit
  is pinned to occurrence 1 ("shall not exceed 38,000,000"); occurrence 0 boxes the line
  before, which does not contain the number. The ratio's start date is pinned to
  occurrence 1 ("May 6, 2026 and thereafter").
- **Numbers written as words ground off.** "One year", "ten years", "five years" and
  "one Share" were all extracted correctly as numbers, but their ranges land on the
  sentence around the word rather than containing a digit match, so `inspect_fields.py`
  marks them `OFF`. The plan name grounds `OFF` the same way, split across its two title
  lines. None of these is featured.
- **An open-ended period came back as the text "null".** The current ratio applies
  "from May 6, 2026 and thereafter", with no end date. Extraction returned `period_end`
  as the string `"null"` rather than a JSON null, even after the field description was
  rewritten to ask for a JSON null. The value is semantically right but a consumer
  should treat the string as empty.

## Credits

60.4 credits at the standard tier: 44.0 for the first parse and extract, then 16.4 for
one re-extraction after editing a field description (`--extract-only`, reusing the
parse).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py equity-incentive-plan           # parse + extract (spends credits)
.venv/bin/python document-types/scripts/run_ade.py equity-incentive-plan --extract-only
.venv/bin/python document-types/scripts/build_images.py equity-incentive-plan      # images, no API calls
.venv/bin/python document-types/scripts/inspect_fields.py equity-incentive-plan --page 5
```
