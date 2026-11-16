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
> - **Search only with the WebSearch tool, and fetch with curl or WebFetch.** Do not drive a browser
>   (the Chrome extension) to run searches, and do not route around a search or rate limit. If
>   WebSearch is unavailable, work from the leads you have and report it in `searched` and
>   `open_questions`.
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
> - Historical records released into the public domain: the Library of Congress, the
>   National Archives, state and county archives, university digital collections, and
>   Wikimedia Commons files with a public-domain tag. Records more than 72 years old, or
>   about people who have died, need no redaction. They are often the best way to get a
>   real, filled-in personal document such as a marriage license or a deed.
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
> 4. List the **personal data**: a **living private individual's** name, home address,
>    date of birth, personal phone or email, account, card, loan, policy or membership
>    number, government identifier, or photograph. Give **kinds and counts only, never
>    the values**. These are **not** personal data, and need no redaction:
>    - specimen values ("John Doe", "123 Main St", 000-00-0000, EIN 12-3456789): say they
>      are specimen
>    - people who are deceased, and records more than 72 years old, **with evidence**:
>      - for the 72-year rule, the record's date as printed or in the archive's catalogue
>        entry
>      - for a death, the document itself (a death certificate), an archive or government
>        record, or a reliable published source such as an obituary or a news report
>
>      Put the evidence in `exemption_evidence`. Without it, treat the person as living.
>    - public figures in the record of their public life
>    - officials and professionals named in that role: clerks, judges, notaries,
>      officiants, physicians, attorneys, company officers
>    - organizations and their contact details
>    - signatures, which are never altered
>    - the document owner's own data, **only** when the operator tells you the owner
>      consented. Record the consent and its limits in `exemption_evidence`. You cannot
>      infer consent from a document being online.
>
>    Clearance follows **all** the data, not just the names. A candidate is
>    `clearance: "public"` only when nothing on it is a living private individual's
>    personal data (name, home address, date of birth, personal contact, account or
>    government number, photograph), apart from consented owner data. One private home
>    address or identifier makes it `redacted`, whoever else is named.
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
>       "personal_data": "kinds and counts only, or 'none: specimen data' / 'none: historical' / 'none: officials and organizations only'",
>       "exemption_evidence": "for each exemption relied on (historical date, death, owner consent): the evidence and its source, or null if none is relied on",
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
- **Exemptions need evidence.** A `public` candidate that relies on the historical, death
  or owner-consent exemption must carry `exemption_evidence` that names a source. Without
  one, demote it to `redacted`. With one, check the source for the recommended candidate,
  as you do its provenance.
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
`.claude/skills/new-document-type-assets/request-template.yaml`. Keep the template's header comment, and fill:

- `name`, `url`: the chosen candidate's URL, unchanged.
- `file`: only if `download: "manual"`. Leave it commented, with a note that the operator
  must download it by hand first, as the build skill requires.
- `notes`: plain sentences covering:
  - the publisher, and the provenance evidence URL
  - the page range, if the type is part of a packet ("Use pages 9-11 only …")
  - the layer, and the redaction tool expected
  - personal data, as kinds only
  - the exemption evidence, if the clearance relies on one, so the build can carry it into
    `clearance_note`
  - whether it is a competitor sample
  - the suggested feature page and fields, **as suggestions**
  - any layout risk the subagent flagged

Do **not** set `feature_page` or `fields` unless the operator chose them. They are
requests the build skill must honour or stop on. Suggestions belong in `notes`, where
the build decides.

Never put a personal-data value in a request file. Request files are gitignored and stay
on this machine, but they are shared working papers, and their notes are copied into
manifests that are published.

## Step 6 — Report

List each request file written, and each type skipped or still unresolved, with the
reason. Then give the next step: `/build-document-types <slug> <slug> …` builds the
whole batch in parallel worktrees and ships it on approval. `/new-document-type-assets
document-types/requests/<slug>.yaml` builds one by hand.

Request files are never committed: `document-types/requests/` is gitignored. When a
folder merges, `ship.py cleanup` moves its request to `document-types/requests/published/`.
