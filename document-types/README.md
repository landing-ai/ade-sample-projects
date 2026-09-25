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
| `README.md` | ● | you |
| `parse.json`, `parse.md` | ● | `run_ade.py` |
| `extract.json` | ● | `run_ade.py` |
| `images/` | ● | `build_images.py` |
| `cost.md` | — | you |
| `accuracy.md`, `ground-truth.json` | — | you |

A folder with all the required pieces produces a full page. A folder missing the
generated output produces a reduced page — the website treats the presence of a valid
`manifest.json` as the signal.

## Why two scripts

`run_ade.py` spends credits. `build_images.py` does not, and never calls the API — it
reads the committed `parse.json` and `extract.json`.

Image generation gets re-run often: adjusting crop padding, box weight, resolution, or
which fields are featured. Tying that to the API would mean paying to change a stroke
colour, and would make the images non-deterministic, since a re-parse can return subtly
different output. Keeping them apart makes the committed output the fixed record and the
images a pure function of it.

## Adding a document type

```bash
mkdir -p collection/<slug>/source
# add the document, write schema.json, manifest.json and README.md

.venv/bin/python document-types/scripts/run_ade.py <slug>
.venv/bin/python document-types/scripts/build_images.py <slug>
```

Then check `collection/<slug>/images/` by eye before committing. A bad crop is not
obvious from a file listing.

## Samples must be publishable

These documents and their extracted values go on a public website.

- **Never a customer document.** No exceptions.
- **Never a blank form.** A blank form has nothing to extract and demonstrates nothing.
- Synthetic, vendor-supplied, or explicitly cleared documents only.
- Realistic samples will contain plausible personal data. It must be obviously
  non-real on inspection and must not collide with a real identifier.

Each folder's `README.md` records where its document came from and that it is cleared.
That record travels with the document rather than living in a separate tracker.

## API version

ADE **v2** (DPT-3) throughout: `client.v2.parse`, `client.v2.extract`. Pages are
1-indexed and boxes are normalized 0–1. Older v1 code elsewhere in this repo is not a
model for anything here.
