---
name: propose-document-types
description: Research public sample documents for a list of document types, propose the best 2-3 candidates for each to the human operator, and write a document-types/requests/<slug>.yaml for each one they pick. Runs one research subagent per type in parallel. Pass the type names, comma- or newline-separated, e.g. /propose-document-types Bill of Lading, Certificate of Origin, Purchase Order
---

# Propose Document Types

Find samples for the `landing.ai/document-type/<slug>` pages, ask the operator to choose,
and turn their choices into request files for `/new-document-type-assets`.

**Arguments:** `$ARGUMENTS`: document type names, comma- or newline-separated. If empty,
ask for them.

This skill stops at request files. It never downloads into the collection, runs ADE,
creates branches or pushes. Building is `/new-document-type-assets`; shipping is a
separate step.

---

## Step 0 — Load the rules

Read `document-types/README.md` and the **Step 2 and Step 3** sections of
`.claude/skills/new-document-type-assets/SKILL.md`. Provenance and personal data are
decided there, and this skill must not propose anything that skill would refuse.

## Step 1 — Normalize the list

For each name, derive the slug the build skill would: lowercase, hyphenated, singular,
matching the intended page URL. Then sort each into one of three groups:

- **Already built.** `document-types/collection/<slug>/` exists. Drop it, and say so.
- **Already requested.** `document-types/requests/<slug>.yaml` exists. Ask whether to
  re-propose it. Do not overwrite the file silently.
- **To research.** Everything else.

Also look for near-duplicates of existing collection folders (`wire-instructions` against
`wire-transfer-instructions`) and ask before researching a second page for the same thing.

## Step 2 — Research, one subagent per type, in parallel

Spawn one `general-purpose` subagent per type, **all in a single message** so they run
concurrently. Batches of up to 6. Give each the prompt in **Research brief** below, with
`<NAME>`, `<SLUG>` and `<SCRATCH>` filled in. `<SCRATCH>` is
`<your scratchpad>/proposals/<slug>/`, so downloads never land in the repo.

Subagents cannot ask the operator anything. The brief tells them to return doubts as
data, not to resolve them by guessing.

### Research brief

> Find 2 or 3 publicly available, **filled-in** sample documents of type **<NAME>**
> (slug `<SLUG>`) suitable for a public marketing page that demonstrates document
> extraction. Work in `<SCRATCH>`; never write inside the git repo. Use
> `/Users/andreakropp/Documents/Github/ade-sample-projects/.venv/bin/python` (PyMuPDF is
> installed) for any PDF work.
>
> **Hard rules: a candidate that breaks one is not a candidate.**
> - Never a blank form or an empty template. It must carry real or specimen values.
> - Never a customer document, and nothing whose origin you cannot state.
> - **User-upload sites (Scribd, DocPlayer, PDFCoffee, Course Hero, SlideShare) are not
>   publishers.** The uploader rarely made the document. Use such a source only if
>   you can name the real publisher, and expect it to need redaction.
> - **A Google Drive or Dropbox link is not a publisher either.** Find the page that links
>   to it (a vendor's documentation, a government site) and give that page as the
>   provenance evidence. If nothing links to it, report it as `unclear`.
>
> **Where good samples come from, best first:**
> - Government specimen forms filled with sample data (IRS, SSA, USCIS, state agencies)
> - A vendor's own published sample, demo output or documentation sample
> - Public filings and records on the official site: SEC EDGAR, court and sheriff-sale
>   postings, county recorders
> - Investor-relations material
> - Template galleries only when the example is filled in
>
> A sample from a document-AI or OCR vendor (Ocrolus, Docsumo, Nanonets, ABBYY, Veryfi,
> Rossum, Hyperscience, Klippa) is acceptable, but set `competitor_sample: true`.
>
> **For each candidate:**
> 1. Download it with `curl -L` into `<SCRATCH>`. Check what arrived with `file`. A bot
>    check, a login page or HTML is `download: "manual"`. Do not try to get round it.
> 2. Open it with PyMuPDF and record the page count and orientation. Record its
>    **layer**:
>    - `text`: `page.get_text()` returns the words
>    - `vector`: no text, many small paths in `page.get_drawings()`
>    - `raster`: no text, one image per page
>    - `mixed`
> 3. Render the first page, and any page you would feature, to PNG and **look at them**.
>    Confirm the document is the requested type and is filled in.
> 4. List the **personal data**: real people's names, addresses, account, loan or
>    government numbers, signatures, phone numbers, and dates of birth. Give **kinds and
>    counts only, never the values**. Specimen values ("John Doe", "123 Main St",
>    000-00-0000, EIN 12-3456789) are not personal data, so say they are specimen.
> 5. Name the redaction tool it would need, if any:
>    - `redact.py` for a text layer
>    - `redact_outlined.py` for vector glyphs
>    - `redact_scan.py` for raster scans
>    - `none` for clean specimen data
> 6. If the type is one part of a larger packet, give the page range that holds it.
> 7. Suggest a feature page and 3–5 fields that would make a good overlay: impersonal
>    values (amounts, dates, reference numbers, organizations) in one part of one page,
>    telling one story. A checkbox, signature or seal is a plus. Say if the page has a
>    side-by-side layout (two signature columns, multi-column text), which has caused
>    pairing errors before.
>
> Search widely enough to find at least 2 viable candidates. Return 1 if only 1 exists,
> and 0 with the searches you tried if none do.
>
> **Return only this JSON, no prose:**
> ```json
> {
>   "slug": "<SLUG>",
>   "name": "<NAME>",
>   "candidates": [
>     {
>       "url": "direct URL of the document",
>       "title": "title as published",
>       "publisher": "who produced it",
>       "provenance_evidence": "URL of the page that publishes or links it, or why the URL itself is the publisher",
>       "clearance": "public | redacted | unclear",
>       "download": "ok | manual | failed",
>       "pages": 0,
>       "page_range": "pages of a larger document that hold this type, or null",
>       "orientation": "portrait | landscape | mixed",
>       "layer": "text | vector | raster | mixed",
>       "redaction_tool": "none | redact.py | redact_outlined.py | redact_scan.py",
>       "personal_data": "kinds and counts only, or 'none: specimen data'",
>       "competitor_sample": false,
>       "populated": true,
>       "strengths": "why it would make a good page",
>       "risks": "anything that could go wrong, including layout risks",
>       "suggested_feature_page": 1,
>       "suggested_fields": ["3-5 short field descriptions"]
>     }
>   ],
>   "recommended": 0,
>   "why_recommended": "one or two sentences",
>   "searched": ["queries and sites tried"],
>   "open_questions": ["anything the operator must decide"]
> }
> ```

## Step 3 — Check what came back

Before showing the operator anything, read each result critically. A subagent's
confidence is not evidence.

- Drop candidates with `populated: false`, `download: "failed"`, or a publisher that is a
  user-upload site without a named real publisher.
- Open the **recommended** candidate's `provenance_evidence` URL yourself and confirm it
  publishes or links the document. This is what made the Ocrolus samples usable. A
  claimed link that is not there demotes the candidate to `unclear`.
- **Personal data:** if `personal_data` contains any actual value rather than a kind,
  scrub it from your own notes and never repeat it.
- **Type that came back empty:** report it with the searches tried. Do not invent a
  candidate.

## Step 4 — Propose, and pause

Show one compact table per type. Put the recommended candidate first and mark it.

| | Candidate | Publisher | Pages | Layer | Clearance | Personal data | Notes |
|---|---|---|---|---|---|---|---|
| ★ | [title](url) | … | 2 | text | public | none: specimen | competitor sample |

Under each table, add one line on why the recommended candidate leads, and any
`open_questions`.

Then ask with `AskUserQuestion`, **one question per type**, up to 4 per call, looping
until every type is answered. Each option is a candidate: the label is a short publisher
or title, and the description gives clearance, redaction tool and page count. The
recommended candidate goes first, labelled "(Recommended)". The operator's free-text
"Other" covers *skip this type*, *search again with a hint*, or *use this URL instead*.

For more than about 8 types, publish the tables as one Artifact page first, so the
operator can read them side by side. Then ask as above.

Wait for the answers. Do not write request files for unanswered types.

Read each answer for more than a choice. The operator may:

- **Rename a type** ("use document 1, but name it Escrow Analysis Statement"). The slug
  follows the new name, and the original name goes in the request's notes.
- **Add a type from a chosen document** ("also add Form 1040, from pages 2 and 3"). No
  subagent has looked at those pages, so open them yourself. Confirm they hold the type
  and are filled in, and check their layer and personal data the way the brief does,
  before writing the request.

## Step 5 — Write the request files

For each chosen candidate, write `document-types/requests/<slug>.yaml` from
`document-types/requests/_template.yaml`. Keep the template's header comment, and fill:

- `name`, `url`: the chosen candidate's URL, unchanged.
- `file`: only if `download: "manual"`. Leave it commented, with a note that the operator
  must download it by hand first, as the build skill requires.
- `notes`: plain sentences covering:
  - the publisher, and the provenance evidence URL
  - the page range, if the type is part of a packet ("Use pages 9-11 only …")
  - the layer, and the redaction tool expected
  - personal data, as kinds only
  - whether it is a competitor sample
  - the suggested feature page and fields, **as suggestions**
  - any layout risk the subagent flagged

Do **not** set `feature_page` or `fields` unless the operator chose them. They are
requests the build skill must honour or stop on. Suggestions belong in `notes`, where
the build decides.

Never put a personal-data value in a request file. Request files are committed to a
public repo.

## Step 6 — Report

List each request file written, and each type skipped or still unresolved, with the
reason. Then give the next step: `/build-document-types <slug> <slug> …` builds the
whole batch in parallel worktrees and ships it on approval. `/new-document-type-assets
document-types/requests/<slug>.yaml` builds one by hand.

Do not commit the request files unless asked. The build skill commits each one with its
folder.
