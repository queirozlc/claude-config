---
name: spec-project
description: |
  Turn a raw product idea into a Linear project whose tickets are agent-executable
  prompts: PM and design pass first, then a decomposition into tickets that each
  carry context, scope, expected behavior, files, acceptance criteria, test
  scenarios, rollout, and an explicit blockedBy dependency graph. Repo-agnostic —
  tracker scope, language, and house style come from .claude/orchestrate.json or
  are detected. This is the front half of the wave-orchestration workflow; its
  output is what `orchestrate-project` consumes. Use when: "turn this idea into
  tickets", "spec this feature", "create a Linear project for X", "break this
  down into tickets", or when handed a rough feature description with intent to
  build it.
---

# Spec a project into agent-executable tickets

You are the PM and the tech lead here, not the implementer. The output is a
Linear project whose tickets can each be handed to an autonomous agent with no
further conversation. Downstream, `orchestrate-project` reads exactly this graph.

## Phase 0 — Resolve the repo contract

Read `.claude/orchestrate.json` at the repo root, plus `CLAUDE.md` / `AGENTS.md`.
The keys that matter here are `linear.workspace`, `linear.team`,
`linear.defaultProject`, `language`, and `styleNotes`. For anything unset, follow
the detection ladder in
`../orchestrate-project/references/project-config.md` — in particular, infer the
team key from the current branch name or recent commit subjects before asking.

Tracker access, in order: the Linear MCP (`mcp__*_Linear__*` or
`mcp__linear-server__*`, whichever this session exposes), then `orca linear`,
then `linctl`.

## Phase 1 — Product pass

Interrogate the idea before decomposing it. Resolve, with the human:

- Who it is for and what they cannot do today.
- The smallest version that delivers the value, and what is deliberately
  deferred.
- How success is observed — the event or metric that proves it works.
- Risk: does this need a flag, a rollback path, or a staged rollout?

Batch open questions into ONE `AskUserQuestion`. Do not ask what the codebase can
answer — check what already exists before proposing to build it, using the repo's
own index (CodeGraph when a `.codegraph/` directory exists) rather than guessing.

## Phase 2 — Design pass

For anything user-facing, settle the surface before writing tickets: the screens
or endpoints touched, the states (empty, loading, error, success), and the copy
language (from `language` in the config; ask once if unset). Consult the
`make-interfaces-feel-better` and `ui-ux-pro-max` skills when the work is visual.

## Phase 3 — Decompose

Split into tickets that obey the rules in
`../orchestrate-project/references/ticket-spec.md`:

- Never a separate ticket for tests; tests ship with their code.
- Migration and schema live with the code that uses them.
- No "foundation" ticket of unused helpers.
- One reviewable PR per ticket; split anything above 5 points.
- Target non-trivial PRs under roughly 400 lines.
- Risky features are born with rollback and observability.

Write each ticket using the template in that same reference file. Every section
is mandatory: an agent reading only the ticket must know exactly what to build,
which files to touch, and when it is done. File paths must be real paths in this
repo, not invented ones.

## Phase 4 — Wire the graph

Dependencies go in Linear's `blockedBy` relations, never in prose. Set them
explicitly — the orchestrator refuses to infer them from titles.

Then print the wave preview the orchestrator will compute:
`| Wave | Tickets | Unblocks after |`. If everything lands in one wave, say so —
that is a good sign, not a mistake. If one ticket blocks everything, question
whether it is really one ticket.

## Phase 5 — Hand off

Create the project and its issues in Linear, then report:

1. The project URL.
2. The wave preview table.
3. The exact next command: `/orchestrate-project <project-url>`, plus the worker
   modes this repo defines (`--agent codex`, `--agent sol`, `--agent sonnet`, or
   whatever `worker.commands` declares).

Do not start implementing. Speccing and building are separate sessions on
purpose — the human reads the graph before agents burn tokens against it.
