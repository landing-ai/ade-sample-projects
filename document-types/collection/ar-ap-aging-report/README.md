# Accounts Receivable and Payable Aging Report

Source assets for `landing.ai/document-type/ar-ap-aging-report`.

## Sample document

`source/CDFI-RFP-Attachment2.pdf`: one portrait page, "Attachment 2: Sample Accounts
Receivable Aging Report", published by Empire State Development (ESD), New York State's
economic development agency. It shows applicants to ESD's CDFI lending program what an
aging schedule should look like. It is a single ruled table for a fictitious "NYS CDFI" as
of June 30, 2016: eight customer rows and a Total row. The columns are an MWBE status,
"ESD Funds Used", the total receivable, and four aging buckets: Current, 1-30, 31-60 and
Over 60 Days Past Due. A short tip about accounting software follows the table.

This sample is **receivables only**. The page covers AR and AP aging, and the two have
the same layout with customers swapped for vendors, so the schema handles both through
`report_info.report_type`.

## Provenance

| | |
|---|---|
| Publisher | Empire State Development (New York State) |
| Source URL | https://esd.ny.gov/sites/default/files/rfp/CDFI-RFP-Attachment2.pdf |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | `public` |

ESD publishes the PDF on its own domain as an attachment to a public RFP. The data is
specimen data, so it names no real customers or amounts. The page text is unchanged. The
only edit was clearing the PDF's document-information metadata, because its author field
named a state staff member. No page text needed redaction.

## Why this document

It is a clean, standalone aging table, the form a lender actually asks a borrower for,
not a screenshot of an accounting package. The table also checks itself: each row's
buckets sum to its total, and the columns sum to the Total row. That makes it easy to
verify the extraction cell by cell. Two details are less common. The oldest bucket is
"Over 60 Days" rather than the usual "Over 90", and two program-specific columns (MWBE
status and ESD funds used) sit before the aging buckets.

## Featured fields

All five are in the Total row on page 1, so the overlay reads as one statement: $11,200
of receivables, of which $7,000 is current, $3,000 is 1-30 days past due, $900 is 31-60
and $300 is over 60.

| Field | Label | Value |
|---|---|---|
| `totals.total_balance` | Total accounts receivable | 11200 |
| `totals.current` | Current | 7000 |
| `totals.days_1_30` | 1-30 days past due | 3000 |
| `totals.days_31_60` | 31-60 days past due | 900 |
| `totals.over_oldest_bucket` | Over 60 days past due | 300 |

These are the four figures the request suggested, plus the 31-60 day total to complete
the row. The as-of date is not featured, as the request asked. No customer row is
featured: the totals are what a lender reads first.

## Extraction

`schema.json` has 22 leaf fields: report header, the aging bucket headings, a per-account
array, and the Total row. Bucket fields have generic names (`days_1_30`, `days_31_60`,
`days_61_90`, `over_oldest_bucket`), so one schema covers reports whose buckets end at 60,
90 or 120 days.

Every value is correct. All eight rows extract, each row's buckets sum to its total, and
the column sums match the printed totals. `days_61_90` is null everywhere because this
report has no such bucket, which is the correct result.

Two things did not follow the schema's descriptions:

- Cells printed as `----` came back as `0.0` rather than null. The amount is the same,
  but a consumer cannot tell "zero" from "not printed".
- Blank MWBE and ESD-funds cells came back as `""` and `0.0` rather than null.

## Grounding

The Total row grounds cleanly, one cell per value, and every crop shows exactly the
figure it claims.

`inspect_fields.py` flags most customer-row amounts as `OFF`, but the boxes are on the
right cells (`1600.0` is boxed on `$1,600`). The customer rows came back as floats, and
the match check does not treat `1600.0` as `1,600`. The Total row came back as integers
and matches. So the flag here comes from the number format, not from the grounding.
Cells that read `----` ground to the dash, which is also correct.

The header grounds as one block: title, entity and date share a single range, so
`report_info.as_of_date` cannot be cropped on its own.

## Credits

3.40 credits for parse and extract at the **standard** service tier, through the jobs
API.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py ar-ap-aging-report      # spends credits
.venv/bin/python document-types/scripts/build_images.py ar-ap-aging-report # free
```
