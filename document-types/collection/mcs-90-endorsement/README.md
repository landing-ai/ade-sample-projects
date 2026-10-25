# MCS-90 endorsement

Source assets for `landing.ai/document-type/mcs-90-endorsement`.

## Sample document

`source/mcs-90-endorsement.pdf` is a completed FMCSA **Form MCS-90**, *Endorsement for
Motor Carrier Policies of Insurance for Public Liability under Sections 29 and 30 of the
Motor Carrier Act of 1980* (Rev 5/26/2023). Northland Insurance Company issued it to
BCT, Inc., the for-hire motor carrier subsidiary of Boise Paper (Packaging Corporation of
America), dated 21 November 2024 with an effective date of 11/01/2024. It has **3 pages,
portrait (US Letter)**, with a text layer:

1. The endorsement: carrier and state, where and when it was dated, the amending policy
   number and effective date, the insurer, the countersignature, the primary/excess
   checkbox with its limit, and the FMCSA verification phone number.
2. Definitions and the operative wording of the endorsement.
3. The Schedule of Limits for public liability, by type of carriage.

| | |
|---|---|
| Publisher | Boise Paper (Packaging Corporation of America), for BCT, Inc.; issued by Northland Insurance Company |
| Source | https://www.boisepaper.com/wp-content/uploads/2025/09/BCT-Owner-Oper-MCS-90.pdf |
| Retrieved | 2026-10-25, downloaded by script from the publisher's site |
| Clearance | Public |

Boise Paper links this PDF as "MCS-90" on its BCT, Inc. company page
(https://www.boisepaper.com/our-company/bct-inc-2/), beside BCT's operating authority,
W-9 and SmartWay certificate: a carrier packet published for shippers and brokers. It is
used as published, with no redaction. It carries business data only: the carrier, the
insurer, a policy number and the insurer's verification line. The countersignature is a
handwritten mark by an unnamed insurer representative and was kept, by the operator's
decision. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

The collection's first **motor carrier insurance filing**, and a different shape from
the policies and certificates already here:

- **A federal form whose values are typed onto underlines**, not into ruled boxes. The
  labels and values sit inline in running text.
- **Two label/value pairs share a line twice**: "Dated at ... on this ... day of ..., ..."
  and "Amending Policy Number ... Effective Date ...". That is the classic place for a
  value to pair with the wrong label.
- **The coverage answer is a checkbox choice between two sentences**, each with its own
  amount blanks.
- **Empty boxes at source**: the USDOT Number and Date Received boxes are blank.

## Featured fields: who is covered, by whom, for how much

All on page 1.

| Field | Value |
|---|---|
| Motor carrier | BCT, INC. |
| Motor carrier state | Idaho |
| Amending policy number | WF011842 |
| Insurance company | Northland Insurance Company |
| Primary limit per accident | 750,000 |

A shipper or broker opens an MCS-90 to check one thing: that this carrier has public
liability cover, from which insurer, under which policy, and up to what amount. These five
answer it. Every featured field is impersonal.

The request suggested six fields in its notes. The **effective date** was left out: it
extracts correctly and grounds `ok`, but it shares one line box with the policy number,
so the two would be one highlight.

## What it surfaced

**The two-pairs-per-line risk did not bite.** The parse wrote each line as
`Amending Policy Number: WF011842  Effective Date: 11/01/2024` and
`Dated at: Greenwood Village, CO on this 21st day of November, 2024`, and extraction
paired every value with the right label. The cost is in grounding granularity, not
accuracy: each of those lines is one box, so its values cannot be highlighted
separately.

**The checkbox reads correctly.** The parse renders the choice as `[x]` on the primary
line and `[ ]` on the excess line, and `coverage.basis` comes back `primary`. The primary
limit's box is the whole checked line, so its crop shows the `[X]` and the amount
together, which suits the field.

**The signature is tagged, not transcribed.** The countersignature comes back as
`[SIGNED]` and `[ILLEGIBLE_SIGNATURE]`. The `countersigned` boolean is right but grounds
`OFF`, since `true` never appears on the page.

**Blanks become empty strings.** The empty USDOT Number and Date Received boxes, and the
unused excess and underlying limits, come back as `""` although the schema allows null.
Their ranges point at the surrounding labels, so they read `OFF`.

**The page 3 schedule grounds cleanly.** All twelve cells of the four-row Schedule of
Limits ground `ok`, cell by cell.

## Extraction

**26 leaf fields** in the schema (35 extracted values with the four schedule rows): form
number, revision and OMB data, USDOT Number and Date Received, the motor carrier and its
state, the dated-at place and date, the amending policy number, the effective date, the
insurer, whether it is countersigned, the primary/excess choice and its three limits, the
FMCSA verification phone, the two cancellation notice periods, and the Schedule of Limits.

## Credits

**8.7 credits at standard tier**, for one parse and one extraction.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py mcs-90-endorsement            # parse + extract (spends credits)
.venv/bin/python document-types/scripts/run_ade.py mcs-90-endorsement --extract-only
.venv/bin/python document-types/scripts/build_images.py mcs-90-endorsement       # images, no API calls
.venv/bin/python document-types/scripts/inspect_fields.py mcs-90-endorsement
```
