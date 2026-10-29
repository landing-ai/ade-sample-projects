# Disclosure Schedules

Source assets for `landing.ai/document-type/disclosure-schedule`.

## Sample document

`source/finch-ferring-apa-disclosure-schedules-redacted.pdf`: the Disclosure Schedules
(Execution Version) to the Asset Purchase Agreement between the four Finch Therapeutics
sellers and Ferring Asset Holding LLC, as filed in the Finch Therapeutics chapter 11
cases. **13 pages, portrait**, trimmed from a 66-page filing.

| | |
|---|---|
| Publisher | Omni Agent Solutions, the court-appointed claims agent, for the debtors in *In re Finch Therapeutics Group, Inc., et al.*, Case No. 26-10409 (LSS) (Bankr. D. Del.) |
| Source | [D.I. 296](https://casedocs.omniagentsolutions.com/cmsvol2/pub_47593/93712212-0d24-4754-86aa-56f478514c33_296.pdf), Notice of Filing of Schedules to Asset Purchase Agreement, filed July 24, 2026; case page [omniagentsolutions.com/FinchTherapeutics](https://omniagentsolutions.com/FinchTherapeutics) |
| Retrieved | 2026-10-28, by script |
| Clearance | **Redacted**: a public court filing, trimmed, with three individuals' names replaced |

| Page | Content |
|---|---|
| 1 | Cover page |
| 2 | Preamble (agreement, parties, interpretation) |
| 3 | Schedule 1.1(b) Assigned Agreements |
| 4–5 | Schedule 1.1(e) Intellectual Property: first page of the pending patent applications table; trademarks, domain names, software |
| 6 | Schedule 1.2(c) Excluded Insurance Policies |
| 7–8 | Schedules 1.2(f) Excluded Causes of Action, 1.2(m) Additional Excluded Assets |
| 9–13 | Schedules 4.1(a), (f), (g), (h), (i): seller jurisdictions, IP, litigation, no violation, assigned agreements |

**What was removed.** The filing's first two pages are the court notice, which carries
the debtors' attorneys' names, emails, bar numbers and an `/s/` signature; they were
dropped. Original pages 7–57 continue the Schedule 1.1(e) patent table, whose narrow
columns wrap words mid-token; they were dropped to keep the sample short, leaving the
table's first page (four complete rows). The court-stamped header still shows the
original page numbers (`Page N of 64`).

**What was replaced.** Schedule 1.1(b) names three individual contacts in its notice
addresses. Each was replaced with an obviously fake name: **Jane Sample** (an Attn line
in a University of Minnesota address), **John Sample** and **Alex Q. Sample** (in the
Skysong Innovations address); the job titles beside them were kept. The replacements were
made with `redact.py`, which removes the original text rather than covering it, and set
in Helvetica, so they look slightly different from the surrounding Times. Every other
party (sellers, purchaser, universities, insurers) is an organization and was kept, as
were the debtors' partial federal tax-ID digits, which are corporate. The PDF's metadata
was cleared. Verified by text search on the committed PDF and this folder: no original
name survives.

## Why this document

It is the collection's first set of M&A disclosure schedules: not a form, but a legal
deliverable built from many short, independently numbered schedules, each with its own
heading and its own shape. Some are tables (assigned contracts with multi-address notice
blocks, patents, trademarks, a 19-row insurance schedule), some are numbered lists, and
several are just "None." The test is whether extraction keeps each schedule's contents
under the right schedule number.

`schema.json` covers the cover page and preamble (agreement, date, sellers, purchaser)
and one object per schedule, each with its schedule number and title. **57 leaf fields**
(counted from the schema); all 16 top-level fields were populated.

## Featured fields: the excluded insurance schedule

All on page 6.

| Field | Value |
|---|---|
| Schedule title | Excluded Insurance Policies |
| Primary D&O policy number | 06-584-17-94 |
| Primary D&O policy term | 3/19/2026 - 3/19/2028 |
| Automobile policy number | 73595419 |

The request's notes suggested this page with these four fields plus the primary D&O
insurer. The insurer was left out: its value wraps across three lines of its cell, and
`inspect_fields.py` reads its range as off. The crops and the page overlay were checked by eye. No person is
featured.

## Grounding and extraction notes

- **The insurance table is clean.** All 19 rows extract correctly, and every policy
  number and policy term grounds to its own cell, including `HN-0303-7264-031925`, which
  wraps across two lines. Insurer and coverage cells are less even: eight of the 38
  read as off (both cells of the Global Package Policy, primary D&O and first excess
  D&O rows, plus two more insurers), while other wrapped insurers (Hudson, XL) read
  ok and no pattern by line count holds. The policy number and term columns are the
  reliable ones to feature.
- **Schedule numbers and titles** ground to their own headings on every schedule.
- **The patent table** extracts all four rows correctly despite its mid-word wraps
  (`Countr`/`y`, `0100833.004`/`10`). One quirk: the Algeria row's co-ownership note,
  which sits in the Application No. cell, was folded into `application_number`.
  Application dates are normalized to ISO, so their ranges read as off by text match
  though they point at the right cell.
- **Long numbered items** (the excluded cause of action, the No Violation item) ground
  as several line ranges each, as expected for multi-line prose.
- **The redacted contacts** extracted as the fake names, inside the notice-address
  strings, confirming the parse saw only the replacements.

## Credits

20.90 credits at standard tier (parse and extract, 13 pages).

## Regenerate

```bash
# trimming and redaction (rules file kept outside the repo)
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/disclosure-schedule/source/finch-ferring-apa-disclosure-schedules-redacted.pdf \
    --rules <outside-the-repo>/rules.json --drop-pages 1 2 $(seq 7 57)

.venv/bin/python document-types/scripts/run_ade.py disclosure-schedule
.venv/bin/python document-types/scripts/build_images.py disclosure-schedule
```
