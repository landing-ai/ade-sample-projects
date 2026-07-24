# Prompt — full-stack grounding viewer app

A full-stack app that shows a document next to its ADE responses and uses
**grounding** to link them: hover over the Markdown (or an extracted field) and
the matching region lights up on the page. This is the demo that makes ADE's
span/grounding data tangible.

Run the minimal sequence in
[`quickstart_with_parse_buildSchema_extract.md`](quickstart_with_parse_buildSchema_extract.md)
first so you (and the agent) have real parse/schema/extract responses to build
against.

---

I checked the conversation and updated `ADE.md`. Now can you create a full-stack app that does the following:

- Show a side-by-side UI where I can upload a doc, see the doc on the left side, and on the right side I can switch between **parse markdown / schema / extract** response views.
- The markdown should be rendered as a markdown view (e.g. with HTML tables).
- For all the spans in the parse response, when I hover over the markdown I want to highlight the corresponding grounding location on the doc page.
- For extract as well: when I hover on an extracted field, I want to highlight all the grounding locations that overlap with the extracted spans.

---

**Notes**
- The hover-to-highlight behavior relies on ADE's **grounding** data — each parse
  chunk and extracted field carries the span/box location it came from on the
  page. That span ↔ box mapping is what you're visualizing.
- Ask for a specific stack if you have a preference (e.g. "Next.js + FastAPI");
  otherwise the agent will choose one.
- Related in-repo example of grounding-driven UI:
  [`Applications`](../Applications) and the Word-Level Grounding workflow under
  [`Workflows`](../Workflows).
