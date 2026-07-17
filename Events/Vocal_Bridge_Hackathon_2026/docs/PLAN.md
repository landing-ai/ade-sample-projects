# FinePrint v2 — Delivery Plan

**Date:** 2026-07-11
**Status:** ✅ BUILT (2026-07-12) — M0–M5 implemented and verified end-to-end against live DPT-3 +
VocalBridge. Planning by PM (John) + SM (Bob); follows `CONCEPT.md`.
**Product:** *Talk to your policy. Watch it answer.* Web-only voice + line-level document grounding.

> This plan turns the founding concept into a buildable sequence. Part I (PM) fixes
> scope, the journey, milestones, and what "done" means for the product. Part II (SM)
> breaks it into epics and stories with acceptance criteria and a build order.

---

## Part I — Product plan (PM)

### North star
A scared traveler asks a question **out loud**, and the **exact line** of their policy
lights up on the real page and is **read aloud in sync**. One loop, always grounded,
never a hallucinated coverage answer.

### Success criteria (demo-able v1-of-v2)
1. Drop the WA policy PDF → **"watch it read"** plays a brisk ~1s line-level sweep over the
   real page. *(Pillar B)*
2. Speak a coverage question in-browser → a spoken `{reply}` and the **cited line blooms**
   on the page within ~1s of the sentence, coverage map scrolling to the clause. *(Pillar A)*
3. **Grounding integrity:** every spoken policy claim maps to a real DPT-3 line box. The
   VocalBridge 60s-timeout path **never speaks an uncited clause** (proven by test).
4. Browser Web-Speech fallback works when VocalBridge/agent is unavailable.
5. Honors `prefers-reduced-motion`; the ever-present informational disclaimer is shown.

### Scope — in
- Single policy document (the WA travel policy) as the primary fixture.
- Three grounding engines: **Parse v2** (canvas), **Extract v2** (Benefits spine),
  **Claude** (conversation) — per `CONCEPT.md §6`.
- The **span bridge** (Extract span ∩ Parse span → line box).
- **Benefits** coverage map (default) + **Anatomy** x-ray (toggle).
- Voice: VocalBridge in-browser WebRTC + browser Web-Speech fallback, AI-Agent mode,
  `verbatim:true`, server-side token, concierge-only base prompt.
- Brand: "editorial instrument" — lime-is-the-highlighter, one highlight primitive/3 moods.

### Scope — out (parked, `CONCEPT.md §7b`)
- Claim-form autofill (the `ECLMFRTC` fields). Two-doc parse groundwork only.
- Multi-policy / IVR selection; horizontal-scale persistence.
- VocalBridge Client Actions (agent→app), post-call summary card — revisit if cheap.

### The loop (product journey)
```
open on "watch it read"  →  speak a question  →  reason (Claude → cited line id)
       │                          │                        │
       └── or drop a policy       └── barge-in / repeat     ▼
                                              line box blooms + read in sync
                                              + coverage map scrolls to clause
```

### Milestones (each ends demo-able)
| # | Milestone | Exit criteria | Depends on |
|---|---|---|---|
| **M0** | Scaffold + lift | v2 Next.js app runs; v1's VocalBridge wiring, PDF render, LLM layer, brand tokens ported; disclaimer present | — |
| **M1** | Parse v2 canvas | Real page renders with **line-level** boxes overlaid; "watch it read" brisk sweep plays | M0 |
| **M2** | Extract v2 + span bridge | Benefits/constraints extracted; each field resolves to a line box via the span bridge; Benefits coverage map renders | M1 |
| **M3** | Grounded conversation | Claude returns `{reply, assessment}`; a typed question lights the cited line + scrolls the map | M2 |
| **M4** | Voice drives the stage | In-browser VocalBridge answers aloud in sync; browser fallback works; **timeout-never-hallucinates test passes** | M3 |
| **M5** | Polish | Anatomy toggle, motion/reduced-motion, failure states from real SDK error codes, empty states | M4 |

### Risks
- **R1 — Grounding integrity (highest).** The 60s VocalBridge timeout can speak an
  ungrounded answer. Mitigation: concierge-only base prompt + stall-not-invent + explicit
  test (M4 exit gate). *(Grumbal's rule: "believe it when it's tested.")*
- **R2 — API keys.** No confirmed DPT-3 / VocalBridge keys yet. Mitigation: build M1–M3
  against a **recorded-fixture** parse of the WA policy so visuals are real while keys land.
- **R3 — Span drift.** Multi-unit chars misalign boxes. Mitigation: `Array.from()` before
  every span slice — a hard rule in the adapter, covered by a unit test.
- **R4 — Sync tightness.** Word-karaoke is browser-path only (utterance-level on VocalBridge).
  Mitigation: line-within-~1s is the promise; word-bounce is a browser bonus, stated honestly.

### Decisions still needed from Seshu (from `CONCEPT.md §8`)
1. **Keys now, or fixtures first?** (Sets whether M1 hits the live API or a recorded parse.)
2. **Sync bar:** line-within-~1s (robust) vs word-level tracking (dazzling)? (Sizes M4.)
3. **Front door:** open on "watch it read" (recommended) or on "start talking"?
4. **Brand nerve:** how dramatic may the read get? (Recommended: restrained base.)
5. **Fresh vs lift:** lift v1's proven bits (recommended) — assumed *lift* in this plan.

---

## Part II — Implementation plan (SM)

Assumes **lift** (Decision 5) and **fixtures-first** for M1–M3 with a live-key swap at M4
(Decision 1 pending; safe default that unblocks the build). Sizes: **S** ≤ half-day,
**M** ~1 day, **L** ~2–3 days.

### Epic A — Scaffold & lift (M0)
- **A1 (M)** Create `fineprint-v2/` Next.js (App Router, TS) app; port `AGENTS.md` Next-version rule.
- **A2 (M)** Lift brand tokens → `lib/brand.ts` (paper/ink/lime, type scale); apply base layout.
- **A3 (M)** Lift the pluggable LLM layer (`chat`/`chatJSON`, providers) from v1.
- **A4 (S)** Lift VocalBridge token route (`/api/voice-token`, `X-API-Key` server-side).
- **A5 (S)** Port PDF page-render (poppler/`pdfjs-dist`) + the informational disclaimer.
- **AC:** app boots, renders a page image, disclaimer visible, LLM layer callable.

### Epic B — Parse v2 canvas & "watch it read" (M1)
- **B1 (L)** Parse v2 adapter: `POST api.ade.landing.ai/v2/parse`, `dpt-3-pro-latest`; parse
  `structure` + `grounding` trees; keep the one global `markdown` string. **`Array.from()`
  before any span slice** (unit test for multi-unit chars — R3).
- **B2 (M)** Recorded-fixture mode: cache one real parse of the WA policy behind the adapter
  interface so B/C/D build without live keys (R2).
- **B3 (M)** Canvas overlay: normalize per-line `parts` boxes by each page node's `width/height`;
  render as the core canvas (not an expander).
- **B4 (M)** "Watch it read" motion: staggered ~50ms line boxes, ease-out, ~1s, monochrome
  lime, then settle. Honor `prefers-reduced-motion`.
- **AC:** WA page renders with line boxes; brisk sweep plays and resolves cleanly.

### Epic C — Extract v2 + the span bridge (M2)
- **C1 (M)** Extract schemas (`benefits`, `constraints`) as `CONCEPT.md §4b` — atomic typed leaves.
- **C2 (M)** Extract v2 adapter: `POST .../v2/extract` over the parsed markdown; capture
  `extraction` + `extraction_metadata.<field>.spans`.
- **C3 (L)** **Span bridge**: field span ∩ Parse block/`part` span → line box. Unit-tested against
  the fixture; this retires v1's unverified `chunk_ids`.
- **C4 (M)** Benefits coverage map: render the spine, each entry pinned to its line box.
- **AC:** say/click "Trip Delay" → map scrolls and the clause line lights, sourced from Extract.

### Epic D — Grounded conversation (M3)
- **D1 (M)** `/api/hotline/turn` returns `{reply, assessment}`; `assessment` cites **line ids**
  resolved through the span bridge (extends v1's page-granularity contract to line ids).
- **D2 (M)** Prompt build: verdict + spoken rules reference **Extract fields only** (no invented
  citations). Reuse the `HotlineReplySchema` shape from v1's hotline spec.
- **D3 (M)** One highlight primitive, three moods (read / answer / map-spotlight) — built once.
- **D4 (S)** Typed-question path: answer bubble + cited line blooms + map scrolls.
- **AC:** typed coverage question lights the correct line; greeting returns `assessment:null`.

### Epic E — Voice drives the stage (M4) — the integrity gate
- **E1 (M)** Port VocalBridge `useAIAgent({onQuery})`; `onQuery` → `/api/hotline/turn` → speak `reply`.
- **E2 (S)** Agent config: `verbatim:true`; concierge-only `custom_prompt` (forbidden to answer
  policy specifics — no knowledge to fall back to).
- **E3 (M)** Sync: spoken `reply` → `assessment` → line box (both paths). Waveform states from the
  real connection lifecycle (`connecting → waiting_for_agent → connected`).
- **E4 (M)** **Guardrail test (gate):** simulate slow/failed `onQuery`; assert the 60s timeout
  **never speaks an uncited clause** — it stalls ("let me pull that up again") and re-delegates.
- **E5 (S)** Browser Web-Speech fallback when agent unavailable (`AGENT_NOT_ACTIVE/NOT_FOUND`);
  `speechSynthesis.onboundary` word-karaoke on this path only.
- **AC:** spoken question answered aloud + line in sync; E4 test green; fallback works.

### Epic F — Polish & honest edges (M5)
- **F1 (S)** Anatomy x-ray toggle (Parse block-type palette, opt-in) — Caravaggio's color, contained.
- **F2 (S)** Failure UI from real SDK error codes (`MICROPHONE_ERROR`, `TOKEN_FETCH_FAILED`,
  `CONNECTION_FAILED`, `USAGE_LIMIT_EXCEEDED`) → calm "I lost you — say that again?".
- **F3 (S)** Empty/loading states; final `prefers-reduced-motion` and disclaimer pass.
- **AC:** toggle works; errors degrade calmly; motion respects the setting.

### Build order & sequencing
```
A (M0) ─► B (M1) ─► C (M2) ─► D (M3) ─► E (M4) ─► F (M5)
             └ B2 fixture unblocks C/D before live keys (R2)
Gate: E4 (integrity test) must pass before M4 is "done" (R1)
```
Critical path: **B1 → C3 (span bridge) → D1 → E4.** The span bridge is the single
architectural keystone; the integrity test is the single non-negotiable gate.

### Definition of Done (every story)
- Grounding claims trace to a real line box (no invented citations).
- `Array.from()` discipline held on any span slice.
- Reduced-motion honored where motion is added; disclaimer intact.
- For voice work: no path can speak an uncited coverage clause.
