---
name: orca-team
description: >-
  Standing multi-agent delegation policy for sessions running inside Orca. Use
  whenever this session is Orca-managed (ORCA_WORKTREE_ID is set, or the
  SessionStart hook announced "Orca session detected") and the work is more than
  a single-file edit: it defines which agent owns implementation, review,
  research, and docs, and how to dispatch to them without the user writing the
  worker prompts. Load before spawning any agent, creating an Orca worktree or
  terminal, or writing a delegation prompt. Delegates the mechanics to the
  `orca-cli` and `orchestration` skills; this file decides who does what.
---

# Orca team policy

This file answers "who does what, and when do I delegate". It deliberately does
not restate the `orca` command grammar. Mechanics live in two places that are
version-matched to the installed binary:

- `orca skills get orca-cli` — worktrees, terminals, prompts, artifacts.
- `orca skills get orchestration` — tasks, dispatch, `worker_done`, decision
  gates, coordinator loops.

Read the relevant one before running commands. Never improvise `orca` flags.

## Roster

| Slice | Owner | Launch command | Notes |
| --- | --- | --- | --- |
| Coordination, planning, decomposition | this Claude session | n/a | Owns the ticket, the decomposition, and the final report. |
| Implementation of a bounded slice | Codex | `codex` | Default executor. One worktree per independent slice. |
| Code review of a diff or branch | Cursor | `cursor-agent` | Review-only. Reports findings; does not push fixes unless told. |
| Wide read-only research across the repo | Codex | `codex` | Cheaper than doing a repo sweep in the coordinator context. |

This is the machine-wide default roster. A repo overrides it via
`worker.commands`, `worker.default`, and `reviewer` in its
`.claude/orchestrate.json` — when those keys exist, they win.

Verify the launch command once per machine before relying on it
(`command -v codex`, `command -v cursor-agent`). If a command is missing, say so
and fall back to Codex rather than silently doing the work inline.

## Routing rules

0. **A whole Linear project, or a project URL pasted with intent to build it** —
   do not hand-roll a plan. Load `orchestrate-project`: it reads the project,
   builds the `blockedBy` graph, and runs merge-gated waves of child worktrees.
   If the project does not exist yet, or its tickets are too thin to be prompts,
   load `spec-project` first.
1. **Single file, obvious change, under ~20 lines** — do it inline. Delegation
   overhead is not worth it.
2. **A ticket-sized feature or fix** — decompose into slices, dispatch each to
   Codex, then route the resulting diff to Cursor for review before opening the
   PR.
3. **"Review this" / "audit this branch"** — dispatch to Cursor directly. Do not
   review inline; the point of the roster is a second model on the diff.
4. **Slices that touch the same files** — run them sequentially in one worktree.
   Parallel worktrees are only for slices with disjoint file sets.
5. **The user says "hand off" / "give this to another agent"** — that is an
   ownership transfer, not supervised orchestration. Use `orca-cli`, spawn the
   agent with the prompt, and stop. Do not create tasks, dispatches, or waits.
6. **The user says supervise / monitor / wait / coordinate** — use the
   `orchestration` skill: create the Run and Task, dispatch with `--inject`, and
   wait for `worker_done`.

## Writing the worker prompt

The user does not author these. Build each prompt yourself and include, in this
order:

1. The goal in one sentence, framed as the finished state.
2. The Linear ticket key and its acceptance criteria, if there is one.
3. The exact files or directories in scope, and what is explicitly out of scope.
4. The repo's quality gate verbatim, and the rule that a red gate is never
   committed around. Take it from `gate` in `.claude/orchestrate.json`, or detect
   it per `orchestrate-project/references/project-config.md`.
5. The house style pointer relevant to the slice: the `styleNotes` lines from
   that same config, or a path reference to the repo's `CLAUDE.md` / `AGENTS.md`.
6. What to report back: files changed, gate result, anything left undone.

Nothing repo-specific belongs in this file. If a rule only applies to one repo,
it goes in that repo's `.claude/orchestrate.json`.

A review prompt is the same shape with a different payload: the base ref, the
head ref, what the change is supposed to do, and an instruction to report
findings as `file:line — severity — problem — fix` without editing anything.

## Reporting back

The coordinator's final message names each agent, its slice, and where the
output landed (worktree name, terminal handle, PR URL). If a worker failed or
was skipped, say so plainly instead of absorbing the work back inline without
mentioning it.

## Tuning this file

The roster table is the knob. Change an owner, a launch command, or a routing
rule here and every future Orca session picks it up with no prompting.
