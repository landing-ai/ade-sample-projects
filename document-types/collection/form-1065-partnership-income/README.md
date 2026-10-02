# Form 1065 - Partnership Income

Source assets for `landing.ai/document-type/form-1065-partnership-income`.

## Sample document

`source/form-1065-2023-ocrolus-sample.pdf`: page 1 of the 2023 IRS Form 1065, U.S.
Return of Partnership Income, filled with synthetic data. **1 page, portrait.**

| | |
|---|---|
| Publisher | Ocrolus |
| Source | [Google Drive](https://drive.google.com/file/d/1PHpnyYjTsGCb4puiZJtKtZKu8Gu2ilsw/edit), linked as the sample from [docs.ocrolus.com/docs/irs-form-1065-2023-us-return-of-partnership-income](https://docs.ocrolus.com/docs/irs-form-1065-2023-us-return-of-partnership-income) |
| Retrieved | 2026-10-02, by script (Drive's standard download link) |
| Clearance | **Public** |

The Drive link alone does not say who made the file. The Ocrolus documentation page for
this form links this exact file as its sample, which establishes the publisher.

Every value is a placeholder:
- partnership "Sample Software Service" at "123 Fake Memorial Ave."
- EIN 12-3456789
- preparer "John Sample" with PTIN P00001234
- phone (800) 123-4567
- round-number line amounts

The signatures are drawn to match those invented names. The PDF metadata holds only the
print driver and Acrobat Distiller. Nothing needed redacting.

> Ocrolus sells document AI, so this is a competitor's published sample. The same is
> true of the bailee letter.

## Why this document

It is the collection's first tax return, and the densest checkbox form in it. Rows G–K
carry 13 checkboxes in a few lines of the header, beside 32 numbered amount lines. It
tests reading a checkbox's state and grounding it to the right box.

`schema.json` follows Ocrolus's field list for this form, with each checkbox as its own
boolean. **75 leaf fields** (counted from the schema), all populated. All 13 checkboxes
extract correctly as checked or unchecked.

## Featured fields: the return's headline, plus a checkbox

| Field | Value |
|---|---|
| Partnership name | Sample Software Service |
| EIN | 12-3456789 |
| Schedules C and M-3 attached (row J) | true |
| Total income (line 8) | 15000.0 |
| Ordinary business income (line 23) | -76000.0 |

The other four fields say who is filing and its bottom line. No person is featured.

## The requested checkbox could not be shown

The request asked for the **cash accounting method checkbox in row H**. Extraction got
it right: `accounting_method.cash` is `true`, and its range is exactly `[x] (1) Cash`.
The highlight did not: **it lands on row I**, the Schedules K-1 count, one row below.

The cause is the parse's line-level boxes (`atomic_grounding`) for the rows G–K block:

| Line | Text it carries | Its box is on row |
|---|---|---|
| 0 | `G Check applicable boxes:` | G |
| 1 | G's checkboxes, then `H Check accounting method:` | H (one row low) |
| 2 | H's checkboxes (`[x] (1) Cash` …) and all of row I | I (one row low) |
| 3 | Row J | J |
| 4 | Row K | K |

The parse writes each row's label on a line of its own, separate from that row's
checkboxes. So for rows G–I its lines fall one row behind the boxes, and they line up
again at row J.

ADE's grounding API (`client.v2.ground`) returns the same shifted line, at 0 credits.
So `build_images.py`'s own range-to-box join is not the cause. The API also returns
that one line for Cash, Accrual, Other and the row I count alike, because a line is the
smallest unit it grounds to.

At the requester's choice, the row J checkbox replaces it. It is the only checkbox on
its line, so the line's box is effectively that box, and it lands on the right row. Row
K's checkboxes also land correctly, but that line holds two of them, so its box would
cover both.

Row J reads `OFF` in `inspect_fields.py` only because "true" is not printed, as for
every boolean. The crop was checked by eye. These findings are written up for the
product team, with job IDs.

## Other notes

- **The sample's arithmetic is invented.** Line 1c reads 2,000 although 1a − 1b = 0.
  Extraction copies the printed values rather than recomputing them, which is the right
  behaviour.
- **Every amount line, 1a through 32, grounds to the box holding its own value**: all 36 read `ok`.

## Cost

**6.00 credits** at standard tier: one-page parse and extraction. The grounding API
check cost 0 credits.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py form-1065-partnership-income
.venv/bin/python document-types/scripts/build_images.py form-1065-partnership-income
.venv/bin/python document-types/scripts/inspect_fields.py form-1065-partnership-income --page 1
```
