# Sanctions screening

Source assets for `landing.ai/document-type/sanctions-screening`.

## Sample document

`source/sanctions-screening-bout-sdn-8279.pdf` — a sanctions-record report from Lursoft's
sanctions search for OFAC SDN entry 8279, Viktor Anatolijevitch BOUT. **2 pages, portrait
(A4)**, generated on 2026-09-29: the listing (list, programme, date of publication,
remark), six names and aliases with their quality, birth data, and the lists the service
checks with the date each was last updated.

| | |
|---|---|
| Publisher | Lursoft IT (report); listing data from the US Treasury's Office of Foreign Assets Control (OFAC) |
| Source | [sanctions.lursoft.lv/person/boutov/SDN-8279](https://sanctions.lursoft.lv/person/boutov/SDN-8279?pdf=1) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted (one value, not the subject's) |

Viktor Bout is a convicted arms dealer on the US sanctions list. Every listed value is
public US government data, also published by OFAC as
[SDN entry 8279](https://sanctionssearch.ofac.treas.gov/Details.aspx?id=8279), and several
sanctions-screening vendors use this same listing as their example report. The listing is
kept as printed, at the document owner's decision. The site answers scripted requests with
a Cloudflare challenge, so the PDF was downloaded by hand.

**One value was replaced, and it was not the subject's.** Lursoft prints the requester's IP
address in the header of every generated report, so the downloaded file identified
whoever downloaded it. It was replaced with `198.51.100.245`, from the RFC 5737 range
reserved for documentation, the same length as the original so the right-aligned header
still lines up, and in the header's grey. `redact.py` removes the underlying text rather
than covering it, and the PDF metadata was cleared. Verified: the original IP is not
extractable from the committed PDF and appears nowhere in this folder.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **compliance screening result**:

- **Label and value tables, repeated.** Six name blocks with the same labels and a
  different set of rows in each (the primary name has no quality; two aliases have first
  and last names, four do not).
- **A record split by a page break.** The last alias's quality is printed alone at the top
  of page 2, separated from its other rows.
- **Status in prose.** The lists the service checks, and when each last changed, are one
  run-on paragraph rather than a table.

## Featured fields: the listing

All on page 1, as requested:

| Field | Value |
|---|---|
| Sanctioned subject | Viktor Anatolijevitch BOUT |
| Sanctions list | SDN (OFAC) |
| Sanctions program | DRCONGO |
| Date of publication | 2019-12-31 |
| Listing remark | Dealer and transporter of weapons and minerals; Owner, Great Lakes Business Company and Compagnie Aerienne des Grands |

The listing a screening hit returns: who, on which list, under which programme, since
when and why. The subject's name is featured because a sanctions screen is a name match,
so the document type cannot be shown without one. The subject is a publicly sanctioned
individual. The name box is the report heading (occurrence 1); occurrence 0 is the Full
name row of the Names table.

The remark ends mid-name because Lursoft's report truncates it; extraction returns it as
printed.

## What it surfaced

**Extraction varied between runs on the same parse.** Three extractions were run. One
returned null for Vitali SERGITOV's alias quality, "Strong", which sits alone at the top
of page 2; the parse keeps it, as `Quality: Strong` after the page break, but that run did
not join it back to its alias. Another run grounded the remark to its "Remark" label
rather than to the text, which would have made its crop read as a mistake. The committed
extraction has both right. One run of each is not enough to trust either failure mode
gone.

**The page 2 dates are right and flagged.** The list update dates are normalized to ISO
dates, so `inspect_fields.py` marks them `OFF` against the printed `22.09.2026.` style. The
lists checked are pulled out of a run-on paragraph correctly, all seven with their dates.

**The primary name's quality is null, correctly.** The primary name has no Quality row,
and extraction returns null rather than inventing one.

## Extraction

**18 leaf fields**: report time, subject, the listing, names and aliases, birth data, the
historical-records flag, data freshness dates and the lists checked. Everything extracts
correctly in the committed run.

## Cost

**4.00 credits** at standard tier for 2 pages: 1.80 to parse, 2.20 to extract. The PDF was
parsed twice, because the IP replacement was redone to match the header's colour, and
extraction was re-run once, for 10.10 in all.

## Regenerating

```bash
# The source is a manual download from the url, with the requester's IP replaced by
# redact.py using a rules file kept outside the repo. The committed PDF is the replaced one.
.venv/bin/python document-types/scripts/run_ade.py sanctions-screening                # 4.00 credits
.venv/bin/python document-types/scripts/run_ade.py sanctions-screening --extract-only # 2.20, schema iteration
.venv/bin/python document-types/scripts/build_images.py sanctions-screening           # free
.venv/bin/python document-types/scripts/inspect_fields.py sanctions-screening --page 1
```
