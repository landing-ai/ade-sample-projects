# FinePrint v2 — *Talk to your policy. Watch it answer.*

Web-only voice + **line-level** document grounding for travel-insurance policies. Ask out loud
(or type); the exact clause blooms on the real page and is read back in sync. Every spoken answer
resolves to a real DPT-3 line box — the voice cannot claim anything the page doesn't show.

Built on **LandingAI DPT-3** (Parse v2 + Extract v2) and **VocalBridge** WebRTC voice, with Claude
doing the clause-level reasoning. Supersedes the v1 app in `../fineprint/`.

## Demo

[![Watch the demo](https://img.youtube.com/vi/lzkpyK5B7VI/maxresdefault.jpg)](https://youtu.be/lzkpyK5B7VI)

See `docs/CONCEPT.md` (thesis + design), `docs/PLAN.md` (PM/SM delivery plan), and
`docs/API-CONTRACT.md` (the verified DPT-3 v2 response shapes).

---

## Quick start

```bash
# 0. Prereqs (macOS): Node 20+ and poppler for PDF rendering
brew install node poppler

# 1. Install deps
npm install

# 2. Configure secrets — copy the template and fill it in (see "Getting your keys" below)
cp .env.example .env
$EDITOR .env

# 3. Create the local SQLite database
npx prisma db push

# 4. Run it
npm run dev            # → http://localhost:3000
```

Open http://localhost:3000, upload a travel-insurance policy PDF, and ask a question by voice or
text. A sample policy — **`sample-travel-policy.pdf`** (bundled at the project root) — is
included so you can try the full loop without your own document.

**Minimum to see it work:** you only need `VISION_AGENT_API_KEY` (LandingAI, for reading the PDF)
and one LLM key (`ANTHROPIC_API_KEY` by default). VocalBridge is optional — leave those vars blank
and the app falls back to the browser's built-in speech (Web Speech API).

---

## Prerequisites (macOS)

| Requirement | Why | Install |
| --- | --- | --- |
| **Node.js 20+** (22 recommended) + npm | runs the Next.js app | `brew install node` |
| **poppler** (`pdftoppm`) | renders PDF pages to images for the grounding canvas | `brew install poppler` |
| **Python 3.9+** *(optional)* | only for the `vb` VocalBridge CLI (agent config) | ships with macOS / `brew install python` |

On Linux, install `poppler-utils` from your package manager instead of `brew install poppler`.

---

## Getting your keys

All secrets live in `.env` (git-ignored — **never commit real keys**). `.env.example` lists every
variable; here is where each one comes from.

### 1. LandingAI ADE — `VISION_AGENT_API_KEY` *(required)*

Powers DPT-3 Parse v2 + Extract v2 (reading and structuring the policy).

1. Sign in at **https://va.landing.ai** (LandingAI Agentic Document Extraction).
2. Open **Settings → API Keys** and create a key.
3. Paste it into `.env` as `VISION_AGENT_API_KEY=...`.

### 2. LLM brain — `ANTHROPIC_API_KEY` *(required, default provider)*

Claude does the clause-level reasoning and produces the spoken reply + citations.

1. Create a key at **https://console.anthropic.com** → **API Keys**.
2. In `.env`, keep the defaults and set the key:
   ```dotenv
   LLM_PROVIDER=anthropic
   LLM_MODEL=claude-haiku-4-5
   ANTHROPIC_API_KEY=sk-ant-...
   ```

The client is provider-pluggable. To use something else, set `LLM_PROVIDER` to `openai`, `gemini`,
or `ollama` and fill the matching vars (`OPENAI_API_KEY`, `GEMINI_API_KEY`, or the generic
`LLM_BASE_URL` + `LLM_API_KEY`). Ollama needs no key and is handy for fully-local runs.

### 3. VocalBridge (live voice) — *optional but recommended*

Gives you the real-time WebRTC voice experience (mic in, agent speaks back). **Skip this and the app
still runs** — it falls back to the browser's Web Speech API for typed/spoken questions.

You need two values in `.env`:

```dotenv
VOCAL_BRIDGE_API_KEY=...      # account key (server-side only; never shipped to the browser)
VOCAL_BRIDGE_AGENT_ID=...     # the agent this app delegates to
```

How the app uses them: the browser never sees your key. `app/api/voice-token/route.ts` exchanges
`VOCAL_BRIDGE_API_KEY` (+ `VOCAL_BRIDGE_AGENT_ID`) for a short-lived room token at
`POST https://vocalbridgeai.com/api/v1/token`, and the client (`components/VoiceRail.tsx`) connects
with that token via `@vocalbridgeai/react`.

#### 3a. On the VocalBridge site

1. Sign up / sign in at **https://vocalbridgeai.com** and open the **Dashboard**.
2. **Get your API key:** Dashboard → **API Keys** (or **Settings → API**) → create a key →
   copy it into `.env` as `VOCAL_BRIDGE_API_KEY`.
3. **Create an agent.** You can do this in the dashboard UI, or with the CLI (below). Creating an
   agent requires an active paid subscription. Deploy target **web** is what this app uses.
4. **Copy the agent's ID** into `.env` as `VOCAL_BRIDGE_AGENT_ID`.

#### 3b. Using the `vb` CLI (agent create + config)

The CLI is the fastest way to create and tune the agent. It's a Python package:

```bash
# one-time: isolate it in a venv (don't pollute system Python)
python3 -m venv ~/.venvs/vocalbridge
~/.venvs/vocalbridge/bin/pip install vocal-bridge
alias vb="~/.venvs/vocalbridge/bin/vb"      # optional convenience

vb auth login "$VOCAL_BRIDGE_API_KEY"       # authenticate (or run `vb auth login` to be prompted)
vb auth status                               # confirm you're logged in
vb agent list                                # see existing agents + their IDs
```

Create the FinePrint agent (deploy on web) and select it:

```bash
vb agent create \
  --name "FinePrint Hotline" \
  --style Focused \
  --deploy-targets web \
  --ai-agent-enabled true \
  --ai-agent-verbatim true \
  --prompt-file agent/concierge-prompt.txt   # your concierge-only prompt (see guardrail below)

vb agent use            # pick the agent you just made → its ID goes in VOCAL_BRIDGE_AGENT_ID
```

Inspect or adjust an existing agent:

```bash
vb config show                                   # all current settings
vb config get model-settings > model.json        # export a section to round-trip
vb config options "<setting>"                     # list valid values for a setting
vb config set --ai-agent-verbatim true            # flip a single setting
vb config set --model-settings-file model.json --merge   # apply a tuned model-settings block
vb prompt show                                     # view the current system prompt
vb prompt set --file agent/concierge-prompt.txt    # replace the prompt from a file
```

---

## ⚠ Required VocalBridge agent config — the grounding-integrity guardrail (R1)

VocalBridge's AI-Agent mode has a **60-second delegation timeout**; if our `onQuery` doesn't answer
in time, the base voice agent *"answers from its own knowledge."* On an insurance tool that is the
one failure that voids the whole thesis — a confident, ungrounded coverage answer. Configure the
agent (the one whose ID is in `VOCAL_BRIDGE_AGENT_ID`) so that can't happen:

1. **Verbatim on** — `vb config set --ai-agent-verbatim true` (or the dashboard's *verbatim* toggle).
   The agent speaks our returned `reply` **exactly**, so the highlighted line and the heard sentence
   cannot drift.
2. **Concierge-only prompt** — the base agent may greet, acknowledge, and delegate, and is
   **forbidden to answer policy specifics itself.** With no policy knowledge to fall back to, a
   timeout produces a stall ("let me pull that up again"), never an invented clause. Set it with
   `vb prompt set --file <your-concierge-prompt>`.
3. **Turn-taking** *(recommended)* — set the agent's turn detection to `semantic_vad` with
   `semantic_eagerness: low` (via `vb config set --model-settings-file ... --merge`). Under the
   default `server_vad` with a short silence window the agent barges in on the caller and cuts its
   own follow-ups. (`continuous_mode` should stay `false`.)

App-side we hold the same line: `/api/hotline/turn` returns a stall + `assessment: null` on any
error (never a fabricated answer), and citations can only reference refs that exist. Covered by
`lib/policy/grounded.test.ts` ("IGNORES an invented ref").

---

## Verify your setup

```bash
npm test                  # vitest — span bridge, anti-hallucination, llm, pdf, rate-limit
npm run build             # production build (should complete cleanly)
npm run accept:extraction # end-to-end DPT-3 extraction check against the sample policy
npm run accept:precheck   # end-to-end grounded-precheck check
npm run e2e               # Playwright browser test of the full loop
```

`accept:*` scripts need `VISION_AGENT_API_KEY` (and your LLM key) set — they call the live APIs.

---

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

Pipeline: `lib/ade/pipeline.ts`. Grounded model: `lib/policy/grounded.ts`. Voice glue:
`components/VoiceRail.tsx` + `app/api/voice-token/route.ts` + `app/api/hotline/turn`.

---

## Troubleshooting

| Symptom | Likely cause / fix |
| --- | --- |
| PDF pages don't render / upload errors | `poppler` missing — `brew install poppler`, confirm `pdftoppm -v`. |
| "VocalBridge not configured" / voice won't start | `VOCAL_BRIDGE_API_KEY` unset — voice falls back to browser speech; that's expected without a key. |
| "Voice agent isn't active" | `VOCAL_BRIDGE_AGENT_ID` wrong, or the agent isn't deployed to **web**. Check `vb agent list`. |
| Prisma "table does not exist" | run `npx prisma db push` to create the local `dev.db`. |
| LLM calls fail / 401 | wrong `LLM_PROVIDER` vs key, or missing `ANTHROPIC_API_KEY`. |

---

## What's parked (deliberately, per CONCEPT §7b)

Claim-form autofill; multi-policy/IVR selection; VocalBridge Client Actions & post-call summary.
The two-document parse groundwork is laid; the loop is the focus.

**Disclaimer:** informational pre-check only, not insurance advice or a claims decision. Personal
documents only — never customer data.
