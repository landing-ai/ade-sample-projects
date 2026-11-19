# CIA Daily Bulletin (Historical)

**On the website:** [landing.ai/document-type/cia-daily-bulletin-historical](https://landing.ai/document-type/cia-daily-bulletin-historical)

The CIA's Current Intelligence Bulletin of 25 January 1957, the Office of Current
Intelligence's daily summary for senior policymakers, declassified and released in 2019.
It has a cover, a contents page listing ten items and an annex, and a typewritten page
or so per item, on subjects from Nasser and the Suez Canal to a possible Soviet
air-to-surface nuclear missile.

| | |
|---|---|
| Pages | 14 |
| Fields in the extraction schema | 16 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:40 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 19,682 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 21.2 s |
| Per page | 1.5 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 12.0 credits |
| Per page | 0.86 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:40 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 16 |
| Non-null fields returned | 16 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 610.7 s |
| Per schema field (16) | 38.17 s |
| Per value returned | 4.85 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 8.9 credits |
| Per schema field (16) | 0.556 credits |
| Per value returned | 0.071 credits |

## Origin

`source/cia-current-intelligence-bulletin-1957-01-25.pdf` is the **Current Intelligence
Bulletin** of 25 January 1957: the CIA Office of Current Intelligence's daily summary for
senior policymakers. It is copy 131 of a numbered Top Secret distribution. The document
is **14 pages, portrait**, of typewritten text:

- a cover
- a contents page listing ten items and an annex
- one page or so per item, covering Nasser and the Suez Canal, Soviet gold loans to
  Egypt, British defence economies, a possible Soviet air-to-surface nuclear missile,
  Laos, Afghanistan and others

It is a scan of the declassified release, with a rough OCR text layer. Blank boxes
throughout mark the CIA's own declassification redactions.

| | |
|---|---|
| Publisher | Central Intelligence Agency, released through the CIA FOIA Electronic Reading Room |
| Source | https://www.cia.gov/readingroom/docs/CURRENT%20INTELLIGENCE%20BULL%5B15755607%5D.pdf |
| Retrieved | 2026-11-15, downloaded manually |
| Clearance | Public |

The CIA released the bulletin itself: every page is stamped "Approved for Release:
2019/12/04 C03161983". It is a work of the US federal government. cia.gov serves a
bot-check page to a scripted download, so the operator downloaded the PDF by hand. The
PDF metadata was cleared.

The bulletin is dated 1957, so it is still inside the 72-year line. Its clearance rests
on the publisher's own release, not the historical exemption. Every person named acts in
an official role: heads of government, ministers, diplomats and military officers, among
them Nasser, Chou En-lai, Prime Minister Daud, Harold Macmillan, Duncan Sandys and Air
Chief Marshal Sir William Dickson. No private individual appears. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Declassified government records are released in large volumes, mostly as scans of
typewritten pages. Making them searchable and citable means reading them page by page.

- **Archives and records agencies:** they index released documents by date, subject and
  release identifier.
- **Historians and academic researchers:** they search bulletins like this one for
  what policymakers were told on a given day.
- **Journalists and FOIA researchers:** they track what was released, when, and what
  remains withheld.
- **Libraries and digital humanities projects:** they turn scanned collections into
  searchable text.
- **Government declassification offices:** they review and release records and track
  the exemptions applied.

### What it contains

- **Typewritten text on a scan,** with an OCR layer that is badly garbled ("BRI A
  OUTLINES", "Current Intelli.gence").
- **Release stamps** at the head and foot of every page.
- **A crossed-out "TOP SECRET" classification** on the cover.
- **A handwritten declassification review block.**
- **Exemption codes** (3.5(c), 3.3(h)(2)) beside the withheld passages.
- **Blank redaction boxes,** some in the middle of headlines.
- **A contents page** with item numbers and page references, and headlines that wrap
  onto a second line.
