# AIA G703 continuation sheet

Source assets for `landing.ai/document-type/aia-g703-continuation-sheet`.

## Sample document

`source/aia-g703-lake-elmo-pay-application-10-redacted.pdf`: pay application #10 on the
City of Lake Elmo, MN City Hall, Fire Department and Washington County Sheriff
Substation remodel, for the period ending October 31, 2022. Page 1 is the **G702-style
application and certificate for payment**; page 2 is the overall **G703-style
continuation sheet**, the schedule of values the G702 summarises. **2 pages,
landscape**, with a text layer. Prepared by the city's construction manager, Hoffmann +
Uhlhorn Construction, Inc.

| | |
|---|---|
| Publisher | City of Lake Elmo, MN (council packet); pay application by Hoffmann + Uhlhorn Construction, Inc. |
| Source | [miweblink.metro-inet.us … 03 - City Center Pay Request.pdf](https://miweblink.metro-inet.us/LakeElmoPublic/0/edoc/444946/03%20-%20City%20Center%20Pay%20Request.pdf) |
| Retrieved | 2026-10-14 |
| Clearance | Redacted |

The file is a consent item from the city council's November 15, 2022 packet, posted on
the city's public Laserfiche WebLink records portal, and was downloaded directly. The
90-page packet was trimmed to its pages 2–3: page 1 is a staff report, and pages 4–90
are a second G702/G703 pair, invoices, subcontractor pay applications, insurance
certificates and emails.

**Redaction.** The G703 carries no personal data. The G702 carried three signature
images (construction manager, architect, notary) and a notary stamp image bearing the
notary's name and commission expiry. All four images were deleted with
`document-types/scripts/redact.py`, which removes them from the file rather than
covering them, and the typed commission-expiry date was replaced with `30-Jun-25`.
Stand-in signatures in a handwriting font ("J. Sample", "A. Example", "N. Public") were
drawn where the three signatures were. Every page carried a `/Rotate 90` flag, which was
folded into the page content first, since `redact.py` mis-sizes boxes on rotated pages.
Document metadata was cleared. Verified: no removed image or original string remains in
the committed PDF, and the folder was swept for them.

**Licensing.** AIA's terms forbid posting completed AIA documents for marketing without
a licence. This sheet is the contractor's own spreadsheet edition of the G703 layout
("H+U CONSTRUCTION EDITION OF AIA DOCUMENT G703") with no AIA copyright notice. The
operator chose it knowing that, on 2026-10-14.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

The collection's first **construction pay application**, and one of its widest tables:

- **A 10-column schedule of values, 32 rows** keyed by CSI division codes (`#0330`,
  `#2300`) mixed with free-text item numbers (`Insurance`, `Reimburse`, `Contingency`).
- **Change orders and negatives.** A change orders column and a revised scheduled value
  per line, with deductions printed in parentheses.
- **Arithmetic that can be checked.** Revised value = scheduled + change orders; total
  completed = previous + this period; balance = revised − completed; 5% retainage per
  line; a totals row; and a G702 summary page whose lines must agree with the G703.
- **A non-standard edition.** Column letters A–H differ from AIA's own G703, and the
  header misnames the G702 as "G723", so a schema that relies on AIA lettering breaks.

## Featured fields: one line revised by a change order

All on page 2. The request named no page or fields; its notes suggested several, and
these were chosen from them:

| Field | Value |
|---|---|
| Period ending | 10/31/2022 |
| HVAC and Controls scheduled value | 962,000.00 |
| HVAC and Controls change orders | 154,703.00 |
| HVAC and Controls revised value | 1,116,703.00 |
| Total completed and stored to date | 6,849,725.77 |

The HVAC line is the largest change order on the job, and the three values show the
arithmetic the sheet exists for. The application number grounds only on the G702, so it
is not featured; on page 2 it shares a header box with the period ending date. The
this-period total, overall % complete and total retainage also ground correctly on
page 2 and were left out to keep to five.

## What it surfaced

**The table came back whole and consistent.** All 32 rows were extracted (the request
notes said 33; the sheet has 32). Every column sums to the extracted totals row, with
retainage within 3 cents, a rounding difference in the source itself. The G702's total
completed and total retainage match the G703 totals. Parenthesised change orders came
back negative.

**Amount and percentage grounding is exact.** These fields on page 2 ground to their
own cells. However, `schedule_of_values[12]` through `[17]` have incorrect `item_number`
ranges: each points to its scheduled-value cell rather than its item-number cell.

**Two text quirks.** Descriptions containing `&` are marked OFF by `inspect_fields.py`
only because the parse markdown escapes `&` as `&amp;`; the boxes are right. The
G702's three-line project name came back with its middle line, "& PUBLIC WORKS
FACILITIES REMODEL", missing.

## Extraction

**35 leaf fields** (counted from `schema.json`): the application header, the ten
numbered G702 lines, eleven fields per schedule-of-values row and the nine-column totals
row.

## Cost

**18.30 credits** at standard tier for 2 pages, parse and extract together.

## Regenerating

The redaction rules file is kept outside the repo. Image boxes are in PDF points on
page 1 after folding the rotation.

```bash
curl -sSL -o /tmp/pay-request.pdf "https://miweblink.metro-inet.us/LakeElmoPublic/0/edoc/444946/03%20-%20City%20Center%20Pay%20Request.pdf"
# keep pages 2-3 and fold the /Rotate 90 into the content
.venv/bin/python -c "import fitz;d=fitz.open('/tmp/pay-request.pdf');d.select([1,2]);[p.remove_rotation() for p in d];d.save('/tmp/pre.pdf',garbage=4,deflate=True)"
.venv/bin/python document-types/scripts/redact.py /tmp/pre.pdf \
    document-types/collection/aia-g703-continuation-sheet/source/aia-g703-lake-elmo-pay-application-10-redacted.pdf \
    --rules <outside-the-repo>/rules.json \
    --remove-images 1:50,469,147,511 1:478,485,544,498 1:752,440,791,544 1:405,548,603,612 \
    --draw-signature "1:60,478,140,506=J. Sample" "1:430,560,560,600=A. Example" "1:482,486,540,497=N. Public" \
    --handwriting-font document-types/scripts/fonts/IndieFlower-Regular.ttf
.venv/bin/python document-types/scripts/run_ade.py aia-g703-continuation-sheet                # 18.30 credits
.venv/bin/python document-types/scripts/run_ade.py aia-g703-continuation-sheet --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py aia-g703-continuation-sheet           # free
.venv/bin/python document-types/scripts/inspect_fields.py aia-g703-continuation-sheet --page 2
```
