# Document Types

Source assets for the document type pages on landing.ai — one folder per page, each
holding a sample document, its extraction schema, real ADE output, and the images that
appear on the page.

Everything here is also usable on its own: each folder is a worked example of parsing and
extracting a particular kind of document with ADE v2.

```
document-types/
  scripts/                  tooling, shared across every document type
    run_ade.py              calls Parse and Extract, writes their output
    build_images.py         reads that output, writes images/. Never calls the API.
  collection/
    <slug>/                 one folder per page, named for its URL slug
```

## Folder names are page slugs

A folder is named for the page it feeds: `collection/consolidated-1099/` becomes
`landing.ai/document-type/consolidated-1099`. Lowercase, hyphenated, no exceptions —
the authoring tooling derives the path from the slug.

This differs from `Use_Cases/`, which uses `Title_Case`. That is deliberate, not an
oversight.

## What a folder contains

| Path | Required | Written by |
|---|---|---|
| `source/<doc>.pdf` | ● | you |
| `schema.json` | ● | you |
| `manifest.json` | ● | you |
| `README.md` | ● | you (title, description, Origin, Why); `build_readme.py` (the rest) |
| `runs/<parse>/parse.json`, `parse.md` | ● | `run_ade.py` |
| `runs/<parse>/<extract>/extract.json` | ● | `run_ade.py` |
| `runs/<parse>/<extract>/grounding.json`, `images/` | ● | `build_images.py` |
| `cost.md` | — | you |
| `accuracy.md`, `ground-truth.json` | — | you |

A folder with all the required pieces produces a full page. A folder missing the
generated output produces a reduced page — the website treats the presence of a valid
`manifest.json` as the signal.

## Why two scripts

`run_ade.py` spends credits. `build_images.py` does not, and never calls the API — it
reads the committed parse and extract output.

Image generation gets re-run often: adjusting crop padding, box weight, resolution, or
which fields are featured. Tying that to the API would mean paying to change a stroke
colour, and would make the images non-deterministic, since a re-parse can return subtly
different output. Keeping them apart makes the committed output the fixed record and the
images a pure function of it.

## Adding a document type

```bash
mkdir -p collection/<slug>/source
# add the document, write schema.json and manifest.json

.venv/bin/python document-types/scripts/run_ade.py <slug>
.venv/bin/python document-types/scripts/build_images.py <slug>
# write README.md: title, description, ## Origin, ## Why this document
.venv/bin/python document-types/scripts/build_readme.py <slug>
```

Then check `collection/<slug>/runs/<parse>/<extract>/images/` by eye before committing.
A bad crop is not obvious from a file listing.

`build_readme.py` writes the README's website link, page and schema-field counts, and
its Parse performance and Extract performance sections from the runs on the pinned
snapshots, Verity first where it ran. `ship.py check` fails when they are out of date.

## Samples must be publishable

These documents and their extracted values go on a public website.

- **Never a customer document.** No exceptions.
- **Never a blank form.** A blank form has nothing to extract and demonstrates nothing.
- Synthetic, vendor-supplied, or explicitly cleared documents only.
- Realistic samples will contain personal data, which is replaced before anything is
  parsed. Names and addresses become obviously fake ("Jane Q Sample", "100 Main St").
  Numeric identifiers such as account, invoice and meter numbers become plausible,
  randomly drawn stand-ins of the same shape (`scripts/plausible.py`), using reserved
  ranges where they exist (SSNs 987-65-4320–4329, phone numbers 555-0100–0199), so the
  sample still reads as a real document.

Provenance lives in `manifest.json` under `source.origin`, so the authoring tooling can
read it and put an attribution on the page without anyone retyping it:

```json
"origin": {
  "url": "https://…",
  "publisher": "Park National Corporation",
  "title": "Q4 2025 Investor Slides",
  "retrieved": "2026-09-25",
  "clearance": "public",
  "clearance_note": "Investor relations material published for general distribution."
}
```

`clearance` is `public`, `synthetic`, `cleared`, or `PLACEHOLDER` for a sample still
awaiting a proper one — greppable across the collection, so outstanding work is visible
rather than buried in prose. Each folder's `README.md` carries the human-readable version.

## Highlight style

A translucent yellow fill with an amber border, not an outline. The fill marks the
*region* a value came from; an outline only marks its boundary, which at page scale
makes the eye find a line and then work out what it encloses. Amber rather than red,
because red reads as "something is wrong" and the message is that the value was found
correctly.

Stroke width is a fraction of the image's short side rather than a pixel count, so a
240px crop and a 1200px page render carry the same visual weight.

The constants sit at the top of `build_images.py`. Changing them changes every page,
which is the point — these images sit side by side in a library and must not drift.

> **Untested on dark documents.** Translucent yellow over a white page is obvious;
> over a dark slide it may be invisible or ugly. The pitch deck sample will be the
> first real test, and may need a second treatment.

## Service tier and models

Everything runs through the **jobs APIs at the `standard` service tier**, which costs half
of priority. Synchronous calls always bill at priority whatever tier is requested, so the
jobs API is the only route to the cheaper rate. Nothing here is urgent.

Every run is filed under the exact snapshots that produced it, as reported in each
response's `metadata.model_version`:

```
collection/<slug>/runs/dpt-3-pro-20261111/parse.json, parse.md
                                         extract-20261111/extract.json, grounding.json, images/
                  runs/dpt-3-verity-20261111/...
```

The extraction sits inside the parse it came from, because it only means anything against
that markdown. A folder can hold DPT-3 Pro and DPT-3 Verity runs side by side, and
`manifest.json` lists each one under `"runs"` with its page count and credits, which is
what the website compares. Every run features the same fields, from the manifest.

**Snapshots are pinned, never `-latest`.** They are set in `scripts/runs.py`. When the
collection used `extract-latest`, its extractions ended up split between
`extract-20260819` and `extract-20260903` with nothing in the file names to say so.

`run_ade.py --parse verity` runs DPT-3 Verity. It reads digitally created, Latin-script
documents only: no scans, handwriting or non-Latin scripts. `build_images.py`,
`inspect_fields.py` and `ship.py check` take `--parse` / `--extract` to pick a run when a
folder holds more than one. `migrate_runs.py` moves a folder from the old
`parse-pro.json` / `images/pro/` layout.

## API version

ADE **v2** (DPT-3) throughout: `client.v2.parse`, `client.v2.extract`. Pages are
1-indexed and boxes are normalized 0–1. Older v1 code elsewhere in this repo is not a
model for anything here.
