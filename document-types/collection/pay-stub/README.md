# Pay stub

Source assets for `landing.ai/document-type/pay-stub`.

## Sample document

`source/lenovo-pay-stub-2026-02-redacted.pdf` — a Lenovo direct deposit earnings
statement for the pay period January 19 to February 1, 2026, redacted. **1 page, portrait
(612×792)**: earnings, taxes, payroll deductions, direct deposit, totals, and a
miscellaneous block, in a ruled form set largely in Courier.

| | |
|---|---|
| Publisher | Lenovo (employer) |
| Source | [scribd.com/document/993398120/…](https://www.scribd.com/document/993398120/Lenovo-PayStub-2026-03) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

## Redaction

This is a real employee's pay statement, uploaded to Scribd by a third party. Scribd is a
user-upload site, so the uploader is not the publisher, and the statement is treated as a
personal record. Scribd also blocks scripted requests, so the file was downloaded by hand.

Six identifiers were replaced using `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it:

| What | Replaced with |
|---|---|
| Employee's name | Jane Q Sample |
| Employee's street address | 100 Main St |
| Employee's city, state and ZIP | Anytown, NC 00000 |
| Last four of the employee's SSN | XXX-XX-0000 |
| Employee ID | 0000 |
| Direct deposit advice number | DD00000000 |

The PDF metadata was also cleared; its title carried an internal file identifier. The pay
amounts are left as printed: with the identifiers gone, nothing on the page identifies the
employee. Lenovo's name, address, phone number and EIN are the employer's published details
and are left as printed. The bank and account numbers were already masked in the original.

**Verified:** no original identifier is extractable from the committed PDF, and none
appears anywhere in this folder. The original values are deliberately not recorded here
or in `manifest.json`. The rules file used by `redact.py` stays outside the repo.

**This sample improved `redact.py`.** The identifiers are set in Courier and Courier Bold,
and the script wrote replacements in Helvetica, which stands out among fixed-width text.
It now writes monospace replacements in Courier. The regular Courier spans here do not set
PyMuPDF's monospace flag, so the script checks the font name as well.

## Why this document

The collection's first **payroll document**, and a layout with two traps:

- **Amounts printed off their labels.** In the Taxes table, each amount sits about half a
  line below its code, so "FICA" appears to have no amount and every amount falls between
  two codes. Pairing them by position alone gets every tax wrong.
- **A scrambled text layer.** The labels use a font whose encoding is shifted, so
  "Amount" copies out of the PDF as "$PRXQW" and "Earnings" as "(DUQLQJV". Only the values
  and the address block carry usable text.

## Featured fields: one paycheck

All on **page 1**. The request named no feature page or fields, so these were chosen:

| Field | Value |
|---|---|
| Gross pay | $5,361.60 |
| Medicare tax | $77.74 |
| Total taxes | $1,387.30 |
| 401(k) deduction | $268.08 |
| Net pay | $3,706.22 |

They tell one story: gross pay, less taxes and the 401(k) deduction, is net pay.
$5,361.60 − $1,387.30 − $268.08 = $3,706.22. The Medicare line is included because it is
the hardest value on the page, the first of the offset tax amounts, and the rate confirms
its pairing: 1.45% of $5,361.60 is $77.74. No person is featured.

`$5,361.60` is printed twice, in the earnings line and the Totals row. `totals.gross_pay`
boxes the Totals row, which is the one the schema asks for.

The 401(k) box is tall. The deductions table is drawn with one cell per column running
from its single entry down to the Total row, and grounding returns that whole cell. The
value is at the top of the box.

## What it surfaced

**The offset tax rows were resolved in the parse.** The parse returns the Taxes table with
an empty FICA row and each amount on its own code's row, so extraction gets every tax
right. Medicare and Social Security check against their rates (1.45% and 6.2% of gross).

**The scrambled labels are read correctly.** Every label comes back as printed, including
"Amount", "Year To Date" and "Payroll Deductions", so the parse reads the page rather than
trusting the broken text layer.

**Everything grounds.** All 33 extracted values are `ok`, each boxing text that contains
its value. That puts this with the SAT score report as the collection's cleanest results.

## Extraction

`schema.json` was written for this statement, with **24 leaf fields**: employer, employee,
pay period, `earnings[]`, `taxes[]` and `deductions[]` lines, totals, hours worked and PTO.
The taxes description warns that amounts are printed below their codes. Everything
populates, with no warnings.

## Cost

**2.30 credits** at standard tier for 1 page: 1.10 to parse, 1.20 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/pay-stub/source/lenovo-pay-stub-2026-02-redacted.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py pay-stub                # 2.30 credits
.venv/bin/python document-types/scripts/run_ade.py pay-stub --extract-only # 1.20, schema iteration
.venv/bin/python document-types/scripts/build_images.py pay-stub           # free
.venv/bin/python document-types/scripts/inspect_fields.py pay-stub --page 1
```
