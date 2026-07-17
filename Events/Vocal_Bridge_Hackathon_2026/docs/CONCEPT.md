# FinePrint v2 — Concept & Design Manifesto

**Tagline:** *Talk to your policy. Watch it answer.*

**Date:** 2026-07-11
**Status:** ✅ BUILT (2026-07-12) — the app in this directory implements this thesis end-to-end on
live DPT-3 + VocalBridge. See `PLAN.md` (delivery) and `API-CONTRACT.md` (verified shapes).
**Lineage:** Supersedes the v1 app in `../fineprint/` (working, near-production). v2 is a
fresh build, not a refactor — the data contract changes too much to bolt on.

**Focus (locked):** the two headliners are **(A) audio interaction** and **(B) the visual
representation of document extraction** — and they are *one loop*: you ask out loud, the
document answers itself by lighting up the exact line, read aloud in sync. Everything else
(including claim-form autofill, §Parked) serves that loop or waits.

---

## 1. The reframe

**v1 answers a question. v2 completes an errand.**

v1 is "read your policy": upload a PDF, then a chat box and two tabs (*Coverage pre-check*
and *Policy hotline*). It works. But the single most magical thing it does — showing you the
**exact clause** an answer rests on — is buried behind a *"Show in document ▾"* toggle. The
document disappears the moment you upload it.

v2 inverts that. **The document is the stage.** The policy page is always on screen; the
verdict, the voice, and the claim form all play out *on the page*, with the exact lines
lighting up where the answer lives. You never leave the document to ask it something — the
document answers you.

And it doesn't stop at an answer. The job a scared traveler actually has isn't "understand my
policy" — it's **"get my money back."** So v2 ends where v1 stops: a **filled claim form**,
every field grounded to the policy clause that justifies it.

---

## 2. Why now: DPT-3 makes this newly possible

v1 runs on DPT-2 (`dpt-2-latest` parse + `extract-latest`). v2 targets **DPT-3 / Parse v2** —
a real generational jump, not a version bump:

| Capability | DPT-2 (v1 today) | DPT-3 / Parse v2 (v2) |
|---|---|---|
| Grounding granularity | per-**block** bounding boxes | per-**block AND per-line** boxes |
| Structure | flat chunks | hierarchical `structure` tree (pages → blocks → lines/cells) + parallel `grounding` tree |
| Traceability | chunk ids (v1 has one unverified nesting path) | stable block ids + Markdown **span pointers** |
| Forms | generic text | **standardized checkboxes**, classified figures |
| Endpoint | `POST /v1/ade/parse` | `POST https://api.ade.landing.ai/v2/parse`, `model=dpt-3-pro-latest`, `Authorization: Bearer` |
| Extract | `extract-latest`, chunk-id refs | `POST .../v2/extract` on **Markdown**, JSON schema, **per-field span grounding** |

**The line-level boxes are the unlock.** v1 can highlight a paragraph. v2 can trace a single
line — which turns the reading moment from a clumsy block-blob into a finger moving down the
page, and lets a claim-form field point at the *one line* that fills it.

> Docs of record: `docs.landing.ai/dpt3/*` (overview, parse, parse-response, extract,
> rate-limits). Verify the `grounding`-tree shape and span-pointer format against
> `openapi-adev2.json` before writing the adapter — same discipline as v1's handoff.

---

## 3. The two pillars — one loop

The whole product is a single sensory loop: **audio in → illuminated document out.** Ask out
loud; the page answers itself, line-precise, read aloud in sync. The two pillars below are the
two halves of that loop, not two separate features.

```
   🎙  you speak            🧠 reason              📄 the page answers itself
  ┌──────────────┐      ┌──────────────┐      ┌────────────────────────────┐
  │ "how long    │ ───► │ verdict +    │ ───► │ line box blooms on the PDF │
  │  must my     │      │ citation →   │      │ + voice reads it in sync   │
  │  flight be   │      │ line id      │      │ + coverage map scrolls to  │
  │  delayed?"   │      │              │      │   the clause               │
  └──────────────┘      └──────────────┘      └────────────────────────────┘
        ▲                                                    │
        └──────────────────  barge-in / ask again  ◄─────────┘
```

### Pillar A — Audio interaction (the input)
The front door is your voice — **in the browser, web only. No phone number / PSTN dial-in.**
Keep v1's **real VocalBridge WebRTC** in-browser voice + browser-speech fallback (already
built, one shared reasoning brain) and make the live session *drive the stage*:

- **Voice → visible answer.** Every spoken answer resolves to a **visible line** on the page —
  the box blooms exactly as the sentence is spoken, so what you *hear* and what you *see* never
  diverge. This is the trust mechanism: the voice can't claim anything the page doesn't show.
- **Sync, concretely.** Voice returns `{ reply, assessment }`; each citation carries a DPT-3
  **line id**; each line id has a box in the `grounding` tree → highlight-as-spoken is a lookup,
  not magic. (v1 already returns this shape at page granularity; v2 extends it to line ids.)
- **Barge-in stays.** Interrupt mid-sentence and ask again; the stage re-lights.
- **Audio *is* visual too.** Listening / thinking / speaking states are part of the on-screen
  language — a calm waveform, not a spinner — so the room *feels* alive without shouting.

### Pillar B — The visual representation of extraction (the output)
The document is the stage, and DPT-3's grounding tree is a **rendered artifact the user
navigates**, not throwaway plumbing.

- **"Watch it read."** As DPT-3 streams its `grounding` tree, **per-line** boxes light up down
  the real page — tables one color, clauses another, the exclusion in red, checkboxes marked —
  the machine reading in front of you. Not a spinner. The product's soul in four seconds. It
  **resolves into relief** (a plain verdict), never ends as decoration on a panic.
- **"Watch it read" is brisk, not cinematic** *(decided)*. A fast, confident ~1s monochrome
  sweep that goes straight to the answer — competence over spectacle. Trust through speed. The
  color/theater lives in the opt-in Anatomy view, not the default read.
- **Coverage map = a *spoken index*, two toggled layers** *(decided)*:
  - **Benefits** (default) — a calm semantic spine of coverages, sourced from **Extract v2**
    (see §6), every entry provably pinned to a line. Say "Trip Delay" and the stage *scrolls
    and lights* to that clause.
  - **Anatomy** (flip) — Parse v2's raw block-type x-ray (`text/table/figure/attestation/
    scan_code`) in full color. The curious opt in; nobody's forced through it.

  The reading animation and the answering animation are **the same benefit→id→box lookup** —
  built once, two moods (idle = index, answering = spotlight).
- **Grounding is the aesthetic.** The highlight box is the visual signature of the whole
  product — always-on, never buried behind a toggle. Every claim the app makes is *shown on
  paper*.
- **Line-level is the unlock.** DPT-2 could only blob a paragraph; DPT-3's per-line `parts`
  boxes let a single sentence answer point at the single line it rests on.

---

## 4. Brand & design direction — "editorial instrument"

v1 is a muted editorial magazine (dark `#1F232C`, lime `#DBFF9B`, lavender/blue, Playfair
italic accents, Urbanist/Inter). It reads as *calm and trustworthy* — correct for insurance,
and worth keeping. v2 **evolves it from "a magazine you read" to "an instrument you operate."**

- **The page is the hero.** Paper is bright, crisp, real; the chrome recedes to near-black
  with a single confident accent. Everything orbits the document.
- **Restraint where it earns trust, one moment of drama where it earns the wow.** Insurance
  can't look like a toy — 95% of the UI is quiet and precise. The one indulgence is the
  line-by-line read.
- **Grounding is the aesthetic.** The highlight box isn't a feature buried in a toggle; it's
  the visual signature of the whole product. Every claim the app makes is *shown on paper*.
- **Keep:** the LandingAI-adjacent palette DNA, the typographic voice (Playfair for the human
  moments, Urbanist for structure), the ever-present disclaimer.
- **Change:** chat-first → document-first; two tabs → one continuous narrative
  (*something went wrong → find the line → fill the claim*); toggle-to-reveal grounding →
  always-on grounding.

*(Open tension the room didn't fully resolve: how bold the accent dares to go. Restrained-trust
vs bold-editorial. Recommendation: restrained base, dramatic only in the read.)*

---

## 4b. The Extract schema (semantic spine)

The schema we hand `/v2/extract` *is* the design of the coverage map and the grounding
precision. Decisions:

- **Two concern-scoped schemas, not v1's four** (the 4-pass split was a Claude token/failure
  workaround we no longer need; one monolith extracts *worse* — split only further if accuracy
  drops):
  - `benefits` — the spine + the numbers (plan meta, schedule of benefits, triggers/thresholds).
  - `constraints` — exclusions, pre-existing rules, deadlines, raw state-override text.
- **Atomic, typed leaves — the non-negotiable.** `extraction_metadata.<field>.spans` grounds
  the *value's* span, so a prose-blob field yields a paragraph box and throws away DPT-3's
  line precision. Every leaf is one atomic value (a dollar amount, an hour count, one clause),
  typed `number` where possible for tight spans + voice math. **Atomic leaves = tight boxes.**
- **The schema stays dumb; reasoning stays in Claude.** State endorsements that delete/replace
  base clauses (e.g. WA removes the mental/nervous exclusion) are *reasoning*, not fields —
  Extract pulls the endorsement text as a grounded fact; Claude decides the override.

Sketch (atomic leaves; arrays of small objects for rows — each leaf gets its own span→box):
```jsonc
// schema: benefits
{
  "plan_name": "string", "underwriter": "string",
  "benefits": [{ "name": "string", "limit_amount": "string",
                 "per_item_cap": "string|null", "note": "string|null" }],
  "triggers": [{ "peril": "string", "threshold_hours": "number|null",
                 "threshold_days": "number|null", "pays": "string|null" }]
}
// schema: constraints
{
  "exclusions": [{ "text": "string" }],
  "pre_existing": { "lookback_days": "number|null", "waiver_conditions": "string|null" },
  "deadlines": [{ "rule": "string", "days": "number|null" }],
  "state_overrides": [{ "text": "string" }]   // raw text; Claude reasons about precedence
}
```
> Grounding: each extracted value's `spans` → find the Parse block/`part` whose `span` contains
> it → its `box`. That box feeds the Benefits coverage map *and* the answer highlight.

## 4c. Brand & motion spec — "editorial instrument"

Evolves v1's palette from editorial-magazine to *instrument*. The through-line the room landed
on: **lime is the highlighter.**

- **One accent, and its job is grounding.** Lime (`#DBFF9B`) appears as the **highlight box**
  (translucent lime over text on paper *is* a highlighter — the accent and the grounding are
  the same gesture) and the one primary CTA. Nothing else competes for it.
- **Paper + ink everywhere else.** Document stage = paper-bright (warm off-white, v1's
  `#E8E9D6` lineage); chrome = near-black ink (`#1F232C`). No pastels on the page.
- **Role/type color is exiled from the page.** v1's supports/limits/excludes/defines role
  colors + the block-type palette live only in (a) small citation *tags* and (b) the opt-in
  **Anatomy** x-ray view. The page itself stays monochrome-on-paper + the lime mark.
- **Type:** Urbanist (display/labels), Inter (body), **Playfair Display italic rationed to one
  human line** — the verdict's plain-English bottom line. The serif is when the instrument
  speaks like a person; spend it once.
- **Motion is instrumental, not playful.** The brisk read = line boxes staggered ~50ms apart,
  ease-out, ~1s total, monochrome lime, then settle — a machine reading, no bounce/spring. The
  answer highlight blooms once (~200ms fade+scale) and holds. Waveform runs off the real
  VocalBridge connection lifecycle (`connecting` held-breath → `waiting_for_agent` slow pulse →
  `connected` alive). Honor `prefers-reduced-motion` (v1 already does).
- **One highlight primitive, three moods.** The *same* lime-box component serves the read, the
  answer, and the coverage-map spotlight. One implementation — not three.

## 5. Information architecture

```
                          ┌──────────────────────────────────────┐
  entry (either door):    │              THE STAGE                │
  • start talking (web ───►│   the real PDF page, always visible   │
  •   mic, in-browser)    │   line-level highlights play here      │
  • or drop the policy    │                                        │
        │                 │                                        │
        ▼                 │   ┌────────────────────────────────┐  │
  [ watch it read ] ─────►│   │ 🎙 voice rail (waveform states) │  │
  DPT-3 line boxes        │   │    + spoken answer, in sync     │  │
  stream in, line by line │   └────────────────────────────────┘  │
        │                 │                                        │
        ▼                 │   ask out loud ──► the exact line      │
  [ coverage map ] ──────►│   blooms + is read aloud + map scrolls │
  navigable heatmap       │   to the clause  ◄── barge-in, repeat  │
                          └──────────────────────────────────────┘
```

One continuous loop, not tabs. Voice and text are two doors into the *same* stage; the answer
is always a **line on the page**, spoken and shown at once.

---

## 6. Tech spine (to detail at scaffold time)

- **Next.js (App Router, TS)** — carry v1's stack; it's sound.
- **Three grounding engines, each to its strength:**
  - **Parse v2** (`dpt-3-pro-latest`, `POST api.ade.landing.ai/v2/parse`) → the **canvas**:
    page render + `structure`/`grounding` trees (per-block AND per-line `parts` boxes, pixels,
    top-left origin) + one global `markdown` string. Powers watch-it-read + the Anatomy x-ray.
  - **Extract v2** (`POST .../v2/extract`, JSON schema over the parsed **markdown**) → the
    **semantic spine**: typed benefits/thresholds/exclusions with `extraction_metadata.<field>
    .spans` = `[start,end)` code-point offsets. Powers the Benefits coverage map. **This
    replaces v1's Claude-invented `chunk_ids` — the one path v1 flagged as unverified — with
    first-party, documented grounding.** We don't ask the model where a clause lives; Extract
    already knows.
  - **Claude** (v1's pluggable LLM layer, current Claude model, server-side) → the
    **conversation**: verdicts + the spoken voice answers. It references Extract *fields*
    (which already carry spans→boxes), so no invented citations enter the chain.
- **The span bridge (the elegant core):** Extract spans and Parse block/part spans index the
  **same** markdown code-point space → *field span ∩ block/part span → line box*. One lookup
  ties a typed field to a pixel rectangle. Discipline: `Array.from()` the markdown before any
  span slice (both sources are code-point offsets) or boxes drift on multi-unit chars.
- **Voice↔highlight sync = dual-track:** the **page** lights the **line** (`parts` box); the
  spoken **caption karaokes words** via TTS boundary events (grounding is line-level max — no
  word boxes exist, so word-tracking lives only in the caption, honestly).
- **Voice:** VocalBridge **in-browser WebRTC** + browser Web Speech fallback, ported from v1
  (already real). Web only — no phone number.
- **Rendering:** page-image + **line-level** bbox overlay as the core canvas (not an
  expander). Normalize box by each page node's `width/height`; `pdfjs-dist` / poppler as in v1.
- **Persistence:** Prisma/SQLite for the personal build; note the single-tenant/local-disk
  limits carried from v1.
- **Privacy/disclaimer:** unchanged and non-negotiable — personal docs only, not customer
  data; informational pre-check, insurer decides.

---

## 6b. Voice layer — grounded in the VocalBridge developer guide

Integration is settled by the docs, not assumed:

- **Mode: AI Agent delegation** (web deploy only — requires the data channel; matches "web-only,
  no phone"). VocalBridge owns greeting / turn-taking / filler and fires `query_agent`; our
  `useAIAgent({ onQuery })` handler calls `/api/hotline/turn`, returns `reply`, the agent
  speaks it. One brain behind both the voice and browser paths.
- **`verbatim: true`** on the agent config, so the spoken words are *exactly* our `reply` — the
  highlighted line and the heard sentence cannot drift.
- **Token auth** stays server-side: `POST vocalbridgeai.com/api/v1/token` with `X-API-Key`
  behind our `/api/voice-token` route (already in v1). Never expose `vb_...` to the browser.

### ⚠ Hard requirement — the 60s timeout must never hallucinate coverage
The guide states: *"Timeout is 60 seconds — if your agent doesn't respond, the voice agent
answers from its own knowledge."* For a grounded insurance tool this is the one failure that
voids the whole thesis — an ungrounded, unciteable answer spoken in the same confident voice as
a real one. **Guardrail:**
- The base agent `custom_prompt` is a strict concierge: greet, acknowledge, delegate. It is
  **forbidden to answer policy specifics itself.** No policy knowledge to fall back *to*.
- On delegation timeout/error it **stalls, never invents** — *"let me pull that up again"* —
  and re-delegates. Grounding integrity over conversational smoothness, always.
- Keep `/api/hotline/turn` fast so 60s is rarely approached.
- **This path gets an explicit test** (simulate a slow/failed `onQuery`; assert no invented
  clause is ever spoken).

### Sync reality (corrected against the docs)
- **Page line-highlight: both paths** — driven by our `assessment` app-side (citation → span →
  Parse block/`part` box). This is the anchor.
- **Caption word-karaoke: browser path only** — `speechSynthesis.onboundary` gives word timing.
  On VocalBridge, TTS is server-side over WebRTC; the built-in `transcript` event is
  **utterance-level** (`{role,text,timestamp}`), no word timing → caption lights per utterance.
  Word-bounce is a browser-path bonus, not a promise.

### Failure states = real SDK error codes (honest UI, not red-text-of-shame)
`MICROPHONE_ERROR` (ask for mic permission), `TOKEN_FETCH_FAILED`, `CONNECTION_FAILED`,
`AGENT_NOT_ACTIVE` / `AGENT_NOT_FOUND` (config problem — fall back to browser voice),
`USAGE_LIMIT_EXCEEDED` (403). Connection lifecycle `disconnected → connecting →
waiting_for_agent → connected` **is** the waveform's visual script (held breath → slow pulse →
alive). Errors degrade to a calm "I lost you — say that again?", and to browser voice when the
agent is unavailable (v1 already has this fallback).

### Nice-to-haves the guide unlocks (parked unless cheap)
- **Client Actions (agent→app):** the agent could emit e.g. `highlight_clause` to drive the
  page directly — but our `assessment` already does this app-side, so this is redundant unless
  we want the agent to steer navigation. Park.
- **Post-processing:** auto-summarize the call into a "what to do next" card after hang-up —
  a cheap, on-thesis way to give John his action step without the parked claim form.

## 7. What changes from v1 (at a glance)

| | v1 (`../fineprint/`) | v2 (this build) |
|---|---|---|
| Job | understand my policy | stop being afraid of it — ask out loud, see the answer |
| Center of screen | chat box + two tabs | the document (always on) |
| Grounding | block-level, behind a toggle | line-level, always-on, the signature |
| Primary input | typing / push-to-talk in a tab | **voice** that drives the whole stage |
| Payoff | a text verdict | a **visible, spoken answer** — the exact line blooms as it's read |
| Extraction | DPT-2 parse + extract-latest | DPT-3 Parse v2 + extract-v2 (line-level) |
| Extraction UI | a checklist ticking ✓✓✓ | **"watch it read"** + a navigable coverage map |
| Brand | editorial magazine | editorial **instrument** |

## 7b. Parked (deliberately out of v1-of-v2 scope)

- **Claim-form autofill** (policy clause → filled `ECLMFRTC` fields, each grounded). Strong
  "get my money back" payoff and a natural next chapter — but it's paperwork, and this build's
  focus is the audio↔document loop. Park it; the two-document parse still lays the groundwork.
- **Multi-policy / IVR selection**, horizontal-scale persistence — same as v1's known limits.

---

## 8. Open questions for Seshu (before scaffold)

1. **API keys:** is there a DPT-3 / Parse v2 key available now (`api.ade.landing.ai`), and a
   VocalBridge key? If not, we build the audio↔document loop against a **recorded-fixture**
   parse of the WA policy so the visuals are real while keys land.
2. **The sync bar:** how tight must voice↔highlight sync feel — "line lit within ~1s of the
   sentence" (easy, robust) vs word-level karaoke tracking (harder, dazzling)? Sets the effort.
3. **Primary front door:** does the demo *open* on the "start talking" (in-browser mic)
   invitation, or on the drop-a-policy "watch it read"? (Recommendation: open on the read,
   because it's the self-explaining wow; web voice is the second beat.) — *web-only voice, no
   phone number.*
4. **Brand nerve:** restrained-trust base (recommended) — how dramatic may the "watch it read"
   moment get before it undercuts credibility?
5. **Fresh vs. lift:** start truly clean, or lift v1's proven bits (VocalBridge wiring, PDF
   render, LLM layer, brand tokens) into v2 on day one? (Recommendation: lift — it's the same
   trust DNA and gets us to the loop faster.)
```
