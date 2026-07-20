# FinePrint v2 — *Talk to your policy. Watch it answer.*

Web-only voice + **line-level** document grounding for travel-insurance policies. Ask out loud
(or type); the exact clause blooms on the real page and is read back in sync. Every spoken answer
resolves to a real DPT-3 line box — the voice cannot claim anything the page doesn't show.

Built on **LandingAI DPT-3** (Parse v2 + Extract v2) and **VocalBridge** WebRTC voice, with Claude
doing the clause-level reasoning. Supersedes the v1 app in `../fineprint/`.

See `docs/CONCEPT.md` (thesis + design), `docs/PLAN.md` (PM/SM delivery plan), and
`docs/API-CONTRACT.md` (the verified DPT-3 v2 response shapes).

## The architecture — three grounding engines + one bridge

- **Parse v2** (`api.ade.landing.ai/v2/parse`, `dpt-3-pro-latest`) → the canvas: page render +
  `structure`/`grounding` trees with **per-line `parts` boxes** + one global markdown string.
  Adapter: `lib/ade/parse.ts`.
- **Extract v2** (`.../v2/extract`, JSON schema over the parsed markdown) → the typed benefits/
  constraints spine, each leaf carrying `spans` into the same markdown. Adapter: `lib/ade/extract.ts`;
  schemas: `lib/ade/schemas.ts`.
- **The span bridge** (`lib/ade/span-bridge.ts`) — `field span ∩ parse part span → line box`. One
  interval-overlap lookup ties a typed field to a pixel rectangle. This is v1's `chunk_ids` made
  first-party and **un-hallucinatable**: Claude cites stable `ref`s from a fixed list and the server
  resolves each ref → box. An invented ref resolves to *no* box (tested).
- **Claude** (`lib/llm/*`, pluggable) → the conversation: `{ reply, assessment }`, cites refs only.

Pipeline: `lib/ade/pipeline.ts`. Grounded model: `lib/policy/grounded.ts`.

## Prerequisites (macOS)

- **Node.js 20+** (22 recommended) and npm — `brew install node`.
- **poppler** for PDF page rendering — `brew install poppler` (provides `pdftoppm`).
- API keys (see *Environment* below). The `.env` file is **shared separately** — it is intentionally
  not in this zip. Drop it into the project root next to `.env.example` before running.

## Run it

```bash
npm install
cp .env.example .env      # OR use the .env shared with you separately
npx prisma db push        # create the local SQLite dev.db
npm run dev               # http://localhost:3000

npm test                  # vitest (span bridge, anti-hallucination, llm, pdf, rate-limit)
npm run build             # production build
```

Then open http://localhost:3000, upload a travel-insurance policy PDF, and ask a question by
voice or text. A sample policy — **`sample-travel-policy.pdf`** (World Travel Holdings LeisureCare
Classic, bundled at the project root) — is included so you can try the full loop without your own document.

### Environment (`.env`) — never commit real keys
- `VISION_AGENT_API_KEY` — LandingAI ADE (DPT-3 Parse v2 + Extract v2).
- `LLM_PROVIDER=anthropic`, `LLM_MODEL=claude-haiku-4-5`, `ANTHROPIC_API_KEY` — reasoning/voice brain.
- `VOCAL_BRIDGE_API_KEY`, `VOCAL_BRIDGE_AGENT_ID` — live WebRTC voice (optional; the app falls back
  to browser Web Speech when absent).

## ⚠ Required VocalBridge agent config — the grounding-integrity guardrail (R1)

VocalBridge's AI-Agent mode has a **60-second delegation timeout**; if our `onQuery` doesn't answer
in time, the base voice agent *"answers from its own knowledge."* On an insurance tool that is the
one failure that voids the whole thesis — a confident, ungrounded coverage answer. Two settings on
the agent (`VOCAL_BRIDGE_AGENT_ID`, in the VocalBridge dashboard) close it:

1. **`verbatim: true`** — the agent speaks our returned `reply` exactly, so the highlighted line and
   the heard sentence cannot drift.
2. **Concierge-only `custom_prompt`** — the base agent may greet, acknowledge, and delegate, and is
   **forbidden to answer policy specifics itself.** With no policy knowledge to fall back to, a
   timeout produces a stall ("let me pull that up again"), never an invented clause.

App-side we hold the same line: `/api/hotline/turn` returns a stall + `assessment: null` on any
error (never a fabricated answer), and citations can only reference refs that exist. Covered by
`lib/policy/grounded.test.ts` ("IGNORES an invented ref").

## What's parked (deliberately, per CONCEPT §7b)
Claim-form autofill; multi-policy/IVR selection; VocalBridge Client Actions & post-call summary.
The two-document parse groundwork is laid; the loop is the focus.

**Disclaimer:** informational pre-check only, not insurance advice or a claims decision. Personal
documents only — never customer data.
