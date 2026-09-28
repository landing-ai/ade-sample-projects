# Document type requests

One file per document you want turned into an asset folder. Written before the
run, committed alongside the folder it produced.

```
/new-document-type-assets document-types/requests/bill-of-lading.yaml
```

`_template.yaml` has every field and what it means.

## Why these are committed

Six months later the question about any page is "why these fields, on this
page?" The manifest records what was chosen. The request records what was
asked for, which is a different thing and is the one that explains the
decision.

Where the two disagree, the manifest's `notes` says why the request could not
be honoured.

## What a request can and cannot decide

It decides the inputs: the document, the schema, and what you would like
featured.

It cannot decide that a value will ground cleanly. Whether a field can be
illustrated is a property of the ADE run, not of the request, and it is
invisible until the run finishes. A field can come back synthesized with no
coordinates, grounded to neighbouring text, or grounded on another page.

So a requested field is honoured when it holds up and reported when it does
not. The skill stops rather than substituting, because a silent substitution
is how a page ends up featuring a value nobody chose.

## Preparing several at once

Write one request per document, then run the skill once per request. Land them
in a single merge: the website's `sync --check` compares every slug against
this repo's HEAD, so one merge of five documents costs one provenance update
over there instead of five.
