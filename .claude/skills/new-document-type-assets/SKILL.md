---
name: new-document-type-assets
description: Build a document-types/collection/<slug>/ asset folder from a public document. Pass the document type name, a URL to a public sample, optionally a path to an existing schema, and --file <path> when the document had to be downloaded by hand (Scribd and other sites that block scripts), e.g. /new-document-type-assets "Bill of Lading" https://example.com/bol.pdf ~/schemas/bol.json
---

# New Document Type Assets

Build the asset folder behind a `landing.ai/document-type/<slug>` page.

**Arguments:** `$ARGUMENTS`

Two forms. **A request file is preferred**, and is the only form that lets the user
specify a feature page or the fields to feature:

```
/new-document-type-assets document-types/requests/bill-of-lading.yaml
```

Or inline: `<document type name>` `<url>` `[path to a schema.json]` `[--file <local copy>]`

```
Bill of Lading https://example.com/sample-bol.pdf ~/schemas/bol.json
"SAT Score Report" https://www.scribd.com/... --file ~/Downloads/sat.pdf
```

The URL is required either way: it is the source of record, and it goes in the manifest
and on the page. `--file` only replaces the download, for sites that block scripts.

If the name or the URL is missing, stop and ask. Do not invent a document.

### Reading a request file

`document-types/requests/_template.yaml` documents every key. Only `name` and `url` are
required; an absent key means you decide that thing, exactly as you did before request
files existed.

| Key | Effect |
|---|---|
| `name`, `url` | Required. As the inline arguments. |
| `file` | A local copy to use instead of downloading. |
| `schema` | Use this schema unchanged. Skips writing one in Step 4. |
| `feature_page` | Feature this page, subject to the check in Step 6. |
| `fields` | Feature these, subject to the check in Step 6. |
| `notes` | Context the document does not carry. Read it before Step 6. |

**A request states intent, and Step 6 decides whether the run can honour it.** Never
silently substitute a field the user asked for. Copy the request file into the repo at
`document-types/requests/<slug>.yaml` if it is not already there, so the folder ships
with the ask that produced it.

---

## Step 0 — Load the rules you will be working under

Read these before anything else:

1. The **`ade-document-processing` skill**. Always use it when writing ADE code. If you
   find code written more than three months ago or using the v1 API, do not copy it.
   **Always v2** (`client.v2.parse`, `client.v2.extract`).
2. `document-types/README.md` and one finished folder —
   `document-types/collection/consolidated-1099/` is the richest example, including its
   `README.md`, `manifest.json` and `grounding-pro.json`.
3. `CLAUDE.md` in this repo.

Non-negotiables, all of them learned the hard way:

- **Standard service tier, always.** Synchronous calls always bill at priority; the jobs
  API is the only route to half credits. `run_ade.py` already does this. Nothing here is
  urgent enough to pay double.
- **Never a blank form.** A blank template demonstrates nothing. The sample must have
  real content in it.
- **No customer documents, ever.** Publisher-supplied, public-domain, or explicitly
  cleared. If you cannot establish where a document came from, do not use it.
- **Personal data never enters this repo.** See Step 3. It is a public repo.

---

## Step 1 — Set up

Derive the slug from the document type name: lowercase, hyphenated, singular, matching
the intended page URL. `Bill of Lading` → `bill-of-lading`.

Check `document-types/collection/<slug>/` does not already exist. If it does, stop and
ask whether to replace it.

**Branch and working directory.** Each document type gets its own git worktree, so
several builds can run at once:

```
.venv/bin/python document-types/scripts/ship.py start <slug>     # prints the worktree path
```

This creates `<repo>-worktrees/<slug>` on branch `document-type-<slug>`, links `.venv`
and `.env` into it, and copies the request file across. **Work inside that directory
from here on**, using paths relative to it. If you were started inside the slug's
worktree already, as the `/build-document-types` orchestrator does, skip this and stay
where you are. Never build in the main checkout while other builds are running.

Use `.venv/bin/python` for every script in this repo. In a worktree it is the linked one.

### Pausing

This skill stops and waits in several places: a download blocked by a bot check,
provenance you cannot establish, a requested field or feature page the run cannot
honour, and an existing folder. When you run as a subagent, you cannot ask the operator
yourself. End your turn with exactly this block and nothing after it, and the
orchestrator will put the question to the operator and resume you with the answer:

```
PAUSE <slug>
step: <step number and name>
question: <one sentence the operator can answer>
options:
  - <option, with its consequence>
  - <option, with its consequence>
context: <the facts the operator needs, with no personal-data values>
```

Leave the worktree as it is when you pause. Do not commit partial work.

---

## Step 2 — Fetch the document and establish provenance

Get the document into `document-types/collection/<slug>/source/<filename>`:

- **With `--file`:** copy the local file there. Do not try the URL as well. Check it is
  a real document of the expected kind with `file` or PyMuPDF, not a saved web page.
- **Without `--file`:** download the URL. Some sites return a bot check or a login page
  with a `200` status instead of the document. Scribd returns a 3 KB HTML page titled
  "Client Challenge", and its downloads need a logged-in account anyway. So check what
  arrived: if it is HTML, or anything other than the document, **stop and ask the user
  to download it by hand** and re-run with `--file`. Do not try to get round the block.

A manual download changes how the document was obtained, not where it came from. The
source URL is still the one given, and the retrieved date is the day the user downloaded
it. Ask if it was not today. Say in `clearance_note` that the file was downloaded
manually.

Then establish, and be able to state:

| | |
|---|---|
| Publisher | Who produced it |
| Source URL | Where you got it |
| Retrieved | Today's date |
| Clearance | `public`, `redacted`, or stop |

**`public`** means the publisher distributes it for general use: an investor relations
PDF, a government form filled with specimen data, a vendor's own sample.

**If you cannot establish this, stop and ask the user.** A document you found without a
clear provenance story is not usable, however good a sample it is.

**User-upload sites are not publishers.** On Scribd and similar sites, the account that
uploaded a document is rarely the one that produced it, so the site's publicness does
not make the document `public`. Treat such documents as personal records until Step 3
shows otherwise, and expect the clearance to be `redacted`. The consolidated 1099 came
from Scribd, was titled as redacted, and was not.

Open the first page and look at it. Confirm it is a real, populated document of the type
requested and not a blank template.

**Sources that are not PDFs.** An SEC EDGAR exhibit is HTML, and some publishers post SVG.
Render them to PDF with headless Chrome, as a local renderer only:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
    --user-data-dir=<scratch>/chrome-profile --no-pdf-header-footer \
    --print-to-pdf=<out>.pdf file:///<cleaned>.html
```

- **Use a throwaway profile** in the scratchpad, so Chrome never touches the operator's
  own browser session.
- **Clean EDGAR HTML first.** Strip the `<DOCUMENT>`/`<TYPE>`/`<SEQUENCE>`/`<FILENAME>`/
  `<DESCRIPTION>`/`<TEXT>` wrapper lines. Also remove EDGAR's injected `<script
  src="/...">` tag: with it in place, Chrome hangs on a `file://` load.
- **Wrap an SVG** in a small HTML page whose `@page` size matches the SVG, with no
  margins. PyMuPDF renders CSS-styled SVGs as solid black.
- **Chrome does not exit by itself** after writing the PDF. Once the file appears, stop
  only the Chrome processes that use your scratch profile. Never stop anything else.
- **Look at the result** before parsing: render page 1 with PyMuPDF. Then clear its
  metadata, and keep the original URL as the source of record.

---

## Step 3 — Check for personal data, and redact before anything else

**Do this before the ADE run, not after.** Once a document is parsed, the personal data
is in the parse output too.

Read enough of the document to answer: does it contain a real person's name, address,
account number, government identifier, phone number, or signature?

A listing title claiming a document is redacted **is not evidence that it is**. The
consolidated 1099 in this collection was titled `XXXX8634` and carried the recipient's
full name, full account number, home address, advisor's name and direct line, and the
real last four of their TIN.

If it contains personal data:

1. Write a rules file mapping each original string to a replacement of similar shape.
   **Keep it outside this repo** — it is the personal data in plain text.

   - **Names and addresses: obviously fake.** Jane Q Sample, 100 Main St, Anytown. A
     realistic-looking fake name can belong to a real person.
   - **Numeric identifiers: plausible, not zeros.** Account, invoice, order, meter,
     licence, policy and reference numbers get a realistic stand-in of the same shape
     from `plausible.py`. A page showing account number 0000000000 reads as a redaction,
     not as a document.

     ```
     .venv/bin/python document-types/scripts/plausible.py <original> [<original> ...]
     ```

     It keeps length, separators and letter prefixes, draws every digit at random (never
     from the original, which a short number could be brute-forced back from), and uses
     reserved ranges where they exist: SSNs from 987-65-4320–4329, phone numbers in
     555-0100–0199.
   - **One stand-in per identifier.** When the same number is printed in several formats
     (`70 023 651 18` and `7002365118`), generate it once and use `reformat()` for the
     other forms, or the document stops agreeing with itself.
2. Run `redact.py`, which uses PyMuPDF redaction annotations. These *remove* the
   underlying text rather than drawing a box over it; text hidden under a filled
   rectangle is still extractable, and that is the usual way a "redacted" PDF leaks.

   ```
   .venv/bin/python document-types/scripts/redact.py <in>.pdf <out>.pdf \
       --rules <outside-the-repo>.json [--drop-pages N]
   ```

3. Replacements must be **no longer than what they replace**, or PyMuPDF wraps them into
   fragments and the field stops extracting.
4. A page that is mostly personal data and adds nothing — a mailing panel, a cover sheet
   — is better dropped with `--drop-pages` than replaced. Rotated text cannot be replaced
   cleanly anyway.

Then sweep. **The PDF's page text is only one of four leak paths:**

- **Document metadata.** `/Info` and XMP. The 1099 carried the account number in `author`
  as `04822863413` — the same digits without separators, so every search for the
  hyphenated form missed it. `redact.py` now clears metadata and verifies on digits as
  well as literal strings.
- **The provenance record.** Recording the before/after map in `manifest.json`
  republishes exactly what you removed. Record *what* was replaced and with what, never
  the original values.
- **The rules file**, if it lands in the repo.
- **Anything you write while documenting the removal** — a README sentence listing the
  strings you took out puts them straight back.

Sweep every file in the folder, on digits as well as literals, before you commit.

---

## Step 4 — Schema

If the request file names a `schema`, or a schema path was passed inline, copy it to
`document-types/collection/<slug>/schema.json` and use it unchanged. Do not improve it,
reorder it or add fields to it. An existing schema from the team is better than a new
one: it is what they actually run, and the page is evidence about their workflow rather
than about a schema written for the occasion.

If it fails against this document — a required field absent, a type that does not fit —
report that in Step 10 and leave the schema alone. That failure is a finding about the
schema, and quietly patching it hides the thing worth knowing.

Otherwise write one. Aim for the fields a real consumer of this document needs, not every
field on the page. Nested objects and arrays are fine. Give every field a `description`.

**Iterate extraction without re-parsing.** `run_ade.py --extract-only` reuses the
committed parse and re-runs extraction alone. On a 43-page deck that was 21 credits
instead of 65.

---

## Step 5 — Run ADE

```
.venv/bin/python document-types/scripts/run_ade.py <slug>
```

Standard tier, jobs API, DPT-3 Pro. Writes `parse-pro.json`, `parse-pro.md` and
`extract-pro.json`, and reports the credits used. Note that figure; it goes in the README.

If extraction returns a partial result, read the warning. A `nonconformant_output` warning
usually means a required field was absent from the document — decide whether to relax the
schema or accept the null.

---

## Step 6 — Choose the featured fields

This is the step that most affects whether the page is any good, and it cannot be done by
reading `extract-pro.json`.

```
.venv/bin/python document-types/scripts/inspect_fields.py <slug> --good
.venv/bin/python document-types/scripts/inspect_fields.py <slug> --page N
```

Each row gives the field, the occurrence, the page, and a match column reading `ok`,
`OFF` or `SYNTH`. Only `ok` can be featured. Run it **without** `--good` when checking a
request: `--good` hides exactly the rows you need to see, which are the failures.

### If the request named a feature page or fields

Check the request against that output before anything else. This is a verification step,
not a selection step: the user has already chosen, and your job is to find out whether
the run supports the choice.

For every requested field, find its row:

- **`ok` on the requested page** — honour it. Use the label the user gave.
- **`OFF`** — the range points at text that supports the value without containing it. The
  crop will read as a mistake. Cannot be featured.
- **`SYNTH`** — no coordinates at all. Cannot be illustrated.
- **`ok` on a different page** — cannot appear on this overlay, which embeds one page.

If any requested field fails, or the requested `feature_page` leaves fewer than three
usable fields, **stop and report to the user before writing the manifest.** Give them:

1. Which requested fields survived and which did not, with the reason for each.
2. The nearest usable alternatives, from the same page and preferably from the same part
   of the document, so the overlay still tells one story.
3. If the requested page is the problem, which page their fields do resolve on.

Then wait. Do not substitute a field the user did not choose, and do not quietly move the
feature page. A page featuring values nobody picked is worse than a page that took an
extra round trip, because nothing about it announces that a choice was made.

Record the outcome in the manifest's `notes`: what was asked for, what shipped, and why
they differ. The request file says what was wanted; the manifest says what happened.

### If the request named neither, choose them yourself

Three failure modes are invisible in the extraction JSON:

- **Synthesized** — the value is correct but has no `ranges` at all. The model read it
  off a chart without being able to point at it. It cannot be illustrated.
- **Grounded off** — the range points at text that supports the value without containing
  it. `$9.8 billion` grounded to a cell reading `$ 9,805`. Both right; the crop reads as
  a mistake.
- **Grounded elsewhere** — on a different page from the one you are featuring.

Rules for the selection:

- **3 to 5 fields, all on one page.** A web page embeds one page overlay. Declare that
  page as `feature_page` in the manifest; `build_images.py` warns if a field resolves
  elsewhere.
- **Prefer fields that tell one story.** The 1099 features one complete transaction —
  security, date acquired, proceeds, cost basis, gain — so the overlay reads as a single
  thing rather than five unrelated values. That page is better than the others because of
  this choice, not because of the document.
- **Pin the occurrence** when a value appears more than once. `company_name` appears 49
  times in the sample deck; first-occurrence is arbitrary.
- **Watch grounding quality by source.** Ruled tables in real forms ground reliably.
  Array elements read off charts and dense slide tables often ground one cell adrift —
  values right, ranges shifted.
- **Prefer an impersonal field when one carries the same point.** These values are
  published on a marketing page and indexed, which is a wider audience than the source
  record has, even when the source is a public one. A date, a case number, an amount, a
  reference or an organization name demonstrates grounding exactly as well as a person's
  name does. Feature a named individual only when the document type cannot be shown
  without one, and say so in `notes` when you do. The arbitration award features a
  private claimant by the document owner's explicit decision; that is the exception, and
  the filing and signature dates on the same page would have made the same point.
- **Count the schema leaves, do not estimate them.** Two READMEs shipped with invented
  figures: 59 leaf fields against an actual 50, and 316 against an actual 66. The website
  prints this number on the page. Read it from the sync output, or count it:

  ```bash
  python3 -c "import json;d=json.load(open('document-types/collection/<slug>/schema.json'))
  f=lambda n: sum(map(f,n['properties'].values())) if n.get('type')=='object' and 'properties' in n else (f(n['items']) if n.get('type')=='array' and 'items' in n else 1)
  print(f(d))"
  ```

---

## Step 7 — Manifest

Write `document-types/collection/<slug>/manifest.json`:

```json
{
  "slug": "<slug>",
  "title": "<Document Type Name>",
  "source": {
    "file": "<filename>",
    "pages": 0,
    "orientation": "portrait | landscape",
    "origin": {
      "url": "...",
      "publisher": "...",
      "title": "...",
      "retrieved": "YYYY-MM-DD",
      "clearance": "public | redacted",
      "clearance_note": "..."
    }
  },
  "feature_page": 1,
  "fields": [
    { "path": "a.b[0].c", "label": "Human label", "occurrence": 0 }
  ],
  "notes": "Why these fields, and anything a reader of this folder should know."
}
```

**Labels render in an inline comma-separated list on the website, so a label must not
contain a comma.** "Ratio, from the overview bullet" read as two fields; it became
"Non-interest income ratio (bullet)".

Add `"name"` to a field only when two featured fields share a `path` — the image filename
derives from the path and would otherwise collide.

If the document was redacted, add `origin.redactions` recording **what** was replaced and
with what, plus counts. Never the original values.

---

## Step 8 — Build the images

```
.venv/bin/python document-types/scripts/build_images.py <slug>
```

Writes per-field crops, the annotated page overlay, clean page previews, and
`grounding-pro.json`.

Read every warning:

- **"value is NOT in the boxed text"** means the range points at text that does not
  contain the value. The crop will show something that does not match the value printed
  beside it.
- **"OCR could not read these values inside their boxes"** means the range is right but
  the box may not be. Line boxes are sometimes one line adrift, so a box can land on a
  caption ("BUYER'S NAME(S)"), on a label alone ("Business Name:") or on the next line
  ("Other (specify):"), while `inspect_fields.py` still reads `ok`. Open every crop it
  names, and do not feature one whose box misses its value. OCR also misreads, so a
  warning is a prompt to look, not a verdict.

**Then open the images and look at them.** Not a file listing — the actual images.

- The page overlay: are the boxes on the right rows?
- Each crop: does it contain the value it claims to?
- The previews: are they the pages you expected? A document of four pages or fewer
  previews every page, with no manifest entry needed. `preview_pages` is for longer
  documents where the default sampling picks a dull page over an interesting one.

**A wrong crop is invisible from a listing, and no test catches it.** This step is not
optional and has caught real errors every time it has been done.

---

## Step 9 — README

Write `document-types/collection/<slug>/README.md` covering:

- What the document is, publisher, page count, orientation
- Provenance table and the clearance story, including whether the file was downloaded
  manually. If redacted, say what was replaced and with
  what — **never the originals** — and that the output was verified
- Why this document was chosen — what it tests that the others do not
- The featured fields and why
- Anything surprising about grounding on this document, good or bad. The contrast between
  documents is worth recording; it is how we learn what these pages can show
- Credits used, at standard tier
- The commands to regenerate everything

---

## Step 10 — Verify and report

Before committing, run the mechanical gates:

```
.venv/bin/python document-types/scripts/ship.py check <slug> \
    [--rules <outside-the-repo>/rules.json] [--verify-also <terms>] [--include <paths>]
```

It checks:
- the folder is complete and the request file is present
- clearance is `public` or `redacted`, never a placeholder
- a redacted document records its redactions, and its source PDF carries no metadata
- 1–5 featured fields, all on `feature_page`, with no comma in any label
- no credential- or rules-shaped path is in the change set
- the personal-data sweep, literals **and** runs of digits

A redacted folder needs `--rules` to be swept at all. Pass `--include` for anything else
this document changed, such as a redaction script. Fix every failure.

Then, by eye, since no script can:

- [ ] Every crop and the page overlay opened and read
- [ ] Every difference between the request and the manifest is explained in `notes`

Commit with `ship.py ship <slug>` and the same flags. It re-runs the check, refuses
files outside this document type, and commits on `document-type-<slug>`. It pushes and
opens the PR only with `--push --pr`, and only when the user has asked. Report:

- The folder path and what is in it
- Credits used
- The featured fields and the page they are on
- **Every part of the request that did not survive the run**, with the reason: a field
  that came back `SYNTH` or `OFF`, a feature page that had too few usable fields, a
  supplied schema that did not fit the document. Say this even when they already agreed
  to the substitution mid-run, because the report is what gets read later.
- Anything you could not establish — especially provenance or clearance doubts
- Whatever the grounding did that was unexpected

Then tell them the next step: run `/new-document-type <slug>` in the **website** repo,
which reads this folder and builds the page.

Do not push or open a PR unless asked. When asked, it is
`ship.py ship <slug> --push --pr [--base <branch>]`. Pass `--base` when this document's
branch is stacked on another unmerged one, such as a redaction script change. After the
PR merges, `ship.py cleanup <slug> --delete-branch` removes the worktree.
