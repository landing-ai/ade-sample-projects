# Build process

The paper trail for how this application was specified and built with an AI coding agent.
None of it is needed to run the app — see the [main README](../README.md) for that. It's
here because the sequence is reusable.

## The files, in order

| File | Stage |
|---|---|
| [`instructions.md`](instructions.md) | The original brief. One page, written before any code. |
| [`BUILD_SPEC.md`](BUILD_SPEC.md) | The consolidated spec, after the agent interviewed the requester about what the brief left open. This is what got implemented. |
| [`Feedback on the application.md`](Feedback%20on%20the%20application.md) | Review notes from actually using the running app, which drove a second round of changes. |

## The workflow

```
brief  ─▶  interview  ─▶  written spec  ─▶  build + verify  ─▶  use it  ─▶  feedback  ─▶  revise
```

**Brief → interview.** The brief was clear about intent but silent on decisions that
change the build: which stack, how to handle nested and array fields, whether to re-run
or reuse cached results, whether reviewers confirm every field or only correct the wrong
ones. Those got asked before anything was written, and the answers are recorded as
settled decisions in `BUILD_SPEC.md` §3 so they weren't relitigated mid-build.

**Interview → spec.** Writing the spec first surfaced the hard part early: mapping an
extracted value back to the exact line or table cell it came from. That got its own
section with an explicit algorithm (§6) rather than being discovered during coding.

**Spec → build.** The spec was treated as revisable, not sacred. Where reality disagreed,
the spec was corrected and the reason recorded — see the implementation note in §6.2 about
using a local range-overlap join instead of the server-side `client.v2.ground()` endpoint.

**Build → verify.** The acceptance checklist (§14) includes *visually* confirming a
highlight lands on the right words, not just asserting it in a test. That requirement
caught a real bug: line-level refinement was silently falling back to whole-block
highlights, which looked plausible and would have shipped.

**Use it → feedback → revise.** The feedback file is short and blunt, which is what makes
it useful. One item ("the UI only shows the `[0]` element of arrays") turned out to be a
misdiagnosis — every element *was* rendering, but repeated identical labels with the index
buried in small grey text made it unreadable. The fix was presentation, not data. Worth
checking a reported cause before acting on it.

## On ADE specifically

The ADE API details came from LandingAI's agent skills, not from the model's memory. ADE's
v1 and v2 (DPT-3) APIs differ substantially — response shapes, page indexing, how schemas
are passed — and an agent working from recall tends to produce v1 code. Install the skills
before extending this project:

```bash
/plugin marketplace add landing-ai/ade-document-processing-skills
/plugin install ade-document-processing@ade-document-processing-skills
/reload-plugins
```

Details and non-Claude-Code options: <https://docs.landing.ai/ade/build-with-ai-agents>

Even with the skills loaded, two gaps against the shipped SDK turned up during the build:
`client.v2.parse()` accepts a `password` parameter the skill says was removed, and
`client.v2` also exposes `ground`, `ground_jobs`, and `files.upload`, which the skill's API
table omits. Verify against the installed SDK when something looks off.
