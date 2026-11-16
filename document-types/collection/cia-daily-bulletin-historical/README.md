# CIA Daily Bulletin (Historical)

The **Current Intelligence Bulletin** of 25 January 1957: the CIA Office of Current
Intelligence's daily summary for senior policymakers. It is copy 131 of a numbered Top Secret
distribution. The document is 14 portrait pages of typewritten text:

- a cover
- a contents page listing ten items and an annex
- one page or so per item, covering Nasser and the Suez Canal, Soviet gold loans to Egypt,
  British defence economies, a possible Soviet air-to-surface nuclear missile, Laos,
  Afghanistan and others

It is a scan of the declassified release, with a rough OCR text layer. Blank boxes throughout
mark the CIA's own declassification redactions.

## Provenance

| | |
|---|---|
| Publisher | Central Intelligence Agency, released through the CIA FOIA Electronic Reading Room |
| Source URL | https://www.cia.gov/readingroom/docs/CURRENT%20INTELLIGENCE%20BULL%5B15755607%5D.pdf |
| Retrieved | 2026-11-15, downloaded manually |
| Clearance | `public` |

The CIA released the bulletin itself: every page is stamped "Approved for Release: 2019/12/04
C03161983". It is a work of the US federal government. cia.gov serves a bot-check page to a
scripted download, so the operator downloaded the PDF by hand. The PDF metadata was cleared.

The bulletin is dated 1957, so it is still inside the 72-year line. Its clearance rests on the
publisher's own release, not the historical exemption. Every person named acts in an official
role: heads of government, ministers, diplomats and military officers, among them Nasser, Chou
En-lai, Prime Minister Daud, Harold Macmillan, Duncan Sandys and Air Chief Marshal Sir William
Dickson. No private individual appears.

## Why this document

It is a typewritten 1950s government scan, with the clutter real archives carry:

- release stamps at the head and foot of every page
- a crossed-out "TOP SECRET" classification
- a handwritten declassification review block
- exemption codes (3.5(c), 3.3(h)(2))
- blank redaction boxes in the middle of headlines

The OCR layer is badly garbled ("BRI A OUTLINES", "Current Intelli.gence"). DPT-3 reads the
page image instead, and its markdown is clean.

## Featured fields (page 1, the cover)

| Field | Value |
|---|---|
| Bulletin date | 25 January 1957 |
| Classification | TOP SECRET |
| Copy number | Copy No. 131 |
| Approved for release | 2019-12-04 |

The cover tells the document's whole life: a Top Secret daily bulletin of January 1957, one
numbered copy, declassified and released 62 years later. The release stamp's document ID
(C03161983) shares the release date's line, so only the date is featured. The classification
grounds to the struck-through "TOP SECRET" at the foot of the page, which is the declassification
mark itself.

## Grounding on this document

**Single-line values ground tightly through the noise.** That includes the cover fields, the
contents page's item numbers and page references, and figures quoted in the article bodies
("$50,000,000").

**Stacked or wrapped values ground `OFF`.**

- **On the cover:** the title is stacked over three lines and the issuing office over two, so
  no single line contains either whole value.
- **In the contents and articles:** headlines that wrap onto a second line come back `OFF` the
  same way.

**The `redacted` flag is unreliable.** The schema asks whether each contents line has a
declassification box beside it. Eight of the ten headlines do, plus the annex. The extraction
marked only item 4 `true`. The boxes are blank white rectangles, so the parse has no text to
see, and the model mostly reported nothing.

**DPT-3 ignores the OCR layer.** The scan's own OCR layer is unusable: page 1 begins with a run
of backslashes. DPT-3's own reading of the page image is clean throughout.

## Credits

21.00 credits at standard tier: parse plus extract, 14 pages.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py cia-daily-bulletin-historical
.venv/bin/python document-types/scripts/inspect_fields.py cia-daily-bulletin-historical --page 1
.venv/bin/python document-types/scripts/build_images.py cia-daily-bulletin-historical
```

The schema has 16 leaf fields.
