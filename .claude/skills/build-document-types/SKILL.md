---
name: build-document-types
description: Build several document-type folders at once from their request files, each in its own git worktree, run by parallel subagents that use /new-document-type-assets. Relays their pause points to the operator, reviews the results, and, only when the operator approves, pushes the branches and opens the PRs. Pass the slugs, e.g. /build-document-types form-1040 form-6251-amt power-of-attorney
---

# Build Document Types

Turn a batch of request files into document-type folders, branches and, once the
operator approves, pull requests.

**Arguments:** `$ARGUMENTS`: slugs with a request file at
`document-types/requests/<slug>.yaml`. With no arguments, list the request files that
have no collection folder yet, and ask which to build.

You are the orchestrator. The operator talks only to you. Subagents build, and you
relay. Nothing is pushed without the operator saying so in this session.

The pipeline's tooling:

| | |
|---|---|
| `/propose-document-types` | research → request files (runs before this) |
| `/new-document-type-assets` | builds one folder; each subagent runs it |
| `document-types/scripts/ship.py` | `start` worktree · `check` gates · `ship` commit/push/PR · `cleanup` |

---

## Step 1 — Plan the batch

For each slug, read its request file and confirm `document-types/collection/<slug>/` does
not exist on the base branch. Then put it in a lane:

- **Parallel lane.** The request's notes say no redaction tool is needed (clean
  specimen or public data), so the build will not touch shared scripts.
- **Serial lane.** Redaction is expected, or the notes are unsure. Redaction work has
  changed the shared scripts before (`redact_scan.py` changed on four consecutive
  builds), and two builds changing one script in parallel cannot both merge cleanly. Run
  this lane one at a time. Each build's branch stacks on the previous one's
  (`--base <previous branch> --local`).

Decide the **base**. Use `main`, unless the batch needs tooling that is committed locally
but not merged. Then use that local branch with `--local`, and tell the operator the
batch is stacked on it.

Show the plan, slug by lane with its base, in a few lines, and go on. The operator can
interrupt.

## Step 2 — Start the worktrees

From the main checkout, for each slug:

```
.venv/bin/python document-types/scripts/ship.py start <slug> [--base <branch> --local]
```

It prints the worktree path, `<repo>-worktrees/<slug>`. Request files only need to exist
in the main checkout; `start` copies each one across.

## Step 3 — Launch the builders

For the parallel lane, spawn one `general-purpose` subagent per slug, **all in one
message**. For the serial lane, spawn one at a time, the next after the previous one
returns. Give each this brief, filled in:

> You are building the document-type folder `<SLUG>` in the git worktree `<WORKTREE>`.
> Run `cd <WORKTREE>` before anything else, and keep every file you write inside it.
> Never touch the main checkout at `<MAIN>`.
>
> Invoke the `new-document-type-assets` skill with the argument
> `document-types/requests/<SLUG>.yaml`, and follow it exactly, with these overrides:
> - You are already in the slug's worktree, on branch `document-type-<SLUG>`. Skip
>   `ship.py start`.
> - Wherever the skill would stop and ask the operator, end your turn with the skill's
>   `PAUSE` block instead. You will be resumed with the answer.
> - Use the scratchpad `<SCRATCH>/<SLUG>/` for anything outside the repo. Keep redaction
>   rules files there, never in the worktree.
> - At the end, commit with `ship.py ship <SLUG>`, plus `--rules`, `--verify-also` and
>   `--include` as the skill directs, and `--trailer "<TRAILER>"`. **Do not pass
>   `--push` or `--pr`.**
>
> Finish with the skill's Step 10 report. Add one line naming the rules file path, if
> you used one.

`<TRAILER>` is the commit attribution line this session's instructions give, if any.

## Step 4 — Relay pauses

When a subagent ends with a `PAUSE <slug>` block, ask the operator with
`AskUserQuestion`. Use the block's `question` and `options`, and put `context` in the
option descriptions. Batch pauses from several subagents into one call, up to 4. Send
each answer back to its subagent with `SendMessage`, and it resumes where it stopped.

Never answer a pause yourself, even when the answer seems obvious. The pauses exist
because the operator's choice is the record.

## Step 5 — Review what came back

A subagent's report is not evidence. For each finished slug, in its worktree:

1. Run `ship.py check <slug>`, with `--rules` from the report if it gave one. It must
   pass.
2. Open the page overlay `images/pro/page-<n>.png` and look at it. Are the boxes on the
   values they claim? Open any crop that looks doubtful.
3. **Redacted documents:** open the first page of the source PDF and confirm no original
   is visible.
4. Read the README's grounding notes for anything surprising.

Then report to the operator, one row per slug:

| Slug | Branch | Pages | Featured (page) | Credits | Clearance | Notes |
|---|---|---|---|---|---|---|

Add every part of a request that did not survive the run, with the reason. Then ask:
**push the branches and open the PRs?** Offer *all*, *some* or *none*.

## Step 6 — Ship, on approval only

For each approved slug, in dependency order (a stacked branch after its base):

```
.venv/bin/python document-types/scripts/ship.py ship <slug> --push --pr --base <base> \
    [--rules ...] --pr-footer "<PR footer line from this session's instructions>"
```

- **Local base:** if the base is an unpushed local branch, it has to be pushed and
  opened as a PR first. Ask before pushing it. It is outward-facing in its own right.
- **Stacked PRs:** say in the report which PR each one stacks on, and the merge order.

## Step 7 — Clean up after merge

When the operator says the PRs have merged:

```
.venv/bin/python document-types/scripts/ship.py cleanup <slug> --delete-branch
```

Leave the worktrees in place until then. They are the only copy of unpushed work.
