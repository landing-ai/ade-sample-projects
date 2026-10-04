# Court Order for Alimony

Source assets for `landing.ai/document-type/alimony-court-order`.

## Sample document

`source/alimony-court-order-fl-180-fl-343.pdf`: a California stipulated judgment of
dissolution (Judicial Council form **FL-180**, pages 1–2) and the **FL-343 Spousal,
Partner, or Family Support Order Attachment** it incorporates (pages 3–4). The order
has the respondent pay the petitioner $407 a month in spousal support from 8/1/2011,
on the 1st of each month, after a 15-year marriage. **4 pages, portrait, scanned.**

| | |
|---|---|
| Publisher | Superior Court of California, County of San Luis Obispo (Self-Help Center) |
| Source | [slo.courts.ca.gov/…/disso-3-uncontested-judgment-sample.pdf](https://www.slo.courts.ca.gov/system/files/disso-3-uncontested-judgment-sample.pdf), pages 7–8 and 18–19 of 33 |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** |

The court's Self-Help Center links this packet as "Sample Forms": a complete
uncontested-judgment filing, filled in by the court with specimen parties (Pat Sample,
Sam Sample, their children Chad and Cindy Sample) and a placeholder address, so
self-represented litigants can see what a finished one looks like. Nothing in it is a
real person's data, and nothing was redacted. Only the judgment and the support order
are used; the rest of the packet is instructions, custody and property attachments.

### Rotation

In the source, these pages are 1-bit raster scans stored sideways, with `/Rotate 270`
on the page to turn them upright, and slightly skewed. To keep the committed sample
free of page rotation, each page was rendered upright at 300 dpi with PyMuPDF and placed
as an image on a fresh, unrotated letter-size page. The scan itself is unchanged,
including its skew; the document metadata is empty.

## Why this document

Alimony is ordered on a checkbox form, not in prose. Who pays whom, whether support is
spousal, family or partner support, and whether it is temporary are all ticked boxes in
one sentence that runs across three lines, with the amount, the start date and the
payment day typed into blanks. It also tests the link between two forms:
the FL-180 judgment says spousal support is "as set forth in the attached" FL-343
(item 4l(3)), and the FL-343 says it is attached to the FL-180.

`schema.json`: **31 leaf fields** (counted from the schema), all populated except the
end date, which the sample leaves blank.

## Featured fields: the support order itself

All on page 3, the first page of the FL-343.

| Field | Value |
|---|---|
| Case number | FL110572 |
| Paid by | respondent |
| Support type | spousal support |
| Monthly amount | 407 |
| Length of marriage (years) | 15 |

`case_number` is pinned to occurrence 2, the FL-343 caption; occurrences 0 and 1 are on
the FL-180 pages.

**Different from the request.** The request's notes suggested the case number, the
spousal support checkbox, the monthly amount, the payment day and the marriage length.
The payment day ('1st') was dropped: `inspect_fields.py` marks it `ok`, but its crop
boxes the "Other (specify):" line beneath it. It was replaced by the payor.

## Grounding and extraction notes

- **One line-level box runs a line late.** The amount line reads "$ 407 per month,
  beginning (date): 8/1/2011 , payable through (specify end date):". The parse returns
  the "payable through" tail as a line of its own, and from there each line-level box
  in that block is one line late: the tail is boxed on the "payable on the 1st" line,
  and "payable on the 1st" on "Other (specify):". The match check passes because the
  range text is right; only looking at the crop shows it. This is why the payment day
  is not featured.
- **The checkbox sentence reads correctly.** Item 6a ticks "respondent" as payor,
  "petitioner" as payee and "spousal support" over "temporary", "family" and "partner"
  support; all three come back right and ground to their lines.
- **Income table.** Gross monthly and net disposable income for both parties ground to
  their cells, across a table with empty deduction columns.
- **Cross-form fields.** `judgment.spousal_support_by_fl343` (true) and
  `support_order.attached_to` ("Judgment (form FL-180)") both resolve.
- **Dates and booleans read `OFF`.** The start date (2011-08-01) is normalized from
  "8/1/2011"; booleans ground to their checkbox lines. The values are right.
- **Blank end date.** Extraction returns an empty string rather than null.

## Cost

**8.80 credits** at standard tier: 4-page parse and extraction.

## Regenerating

```bash
# Pages 7, 8, 18 and 19 of the source packet, re-rendered upright (see Rotation above).
python - <<'PY'
import fitz
src = fitz.open("disso-3-uncontested-judgment-sample.pdf")
out = fitz.open()
for n in [7, 8, 18, 19]:
    p = src[n - 1]
    pix = p.get_pixmap(dpi=300, colorspace=fitz.csGRAY)
    page = out.new_page(width=p.rect.width, height=p.rect.height)
    page.insert_image(page.rect, stream=pix.tobytes("png"))
out.set_metadata({}); out.del_xml_metadata()
out.save("source/alimony-court-order-fl-180-fl-343.pdf", garbage=4, deflate=True)
PY

.venv/bin/python document-types/scripts/run_ade.py alimony-court-order
.venv/bin/python document-types/scripts/build_images.py alimony-court-order
.venv/bin/python document-types/scripts/inspect_fields.py alimony-court-order --page 3
```
