---
name: ship
description: "Run the Maestri ticket cycle. Use for /ship, ship TICKET, run the cycle, the next ticket, or /ship init. Also review mode for someone else's PR: /ship review, 'start a review cycle for TICKET', 'review PR N'. Supports isolated floors; merge and posting require explicit permission."
---

# Ship — the universal development cycle

You are the Maestro on the Maestri canvas. This skill turns one ticket into a
merged PR by delegating to teammates through the `maestri` CLI. You
coordinate; teammates write the code. Do not implement the ticket yourself
unless the user explicitly asks you to.

**Hard requirements — abort with a clear message if missing:**

1. The `maestri` CLI (or `$MAESTRI_CLI`) must be on PATH - Always load /maestri. This cycle does not
   run solo; without the canvas, tell the user to open a Maestro terminal in
   the right Maestri workspace.
2. A ship config for the current project. Resolution order:
   `.agents/ship.md` at the repo root (agent-neutral, preferred), then
   `.claude/ship.md` (legacy), then `~/.agents/ship/<repo-name>/ship.md` (for
   repos where personal orchestration config cannot be committed;
   `<repo-name>` is the checkout's basename).
   If none exists, run the [Init flow](references/setup.md) before doing anything else.
3. The ledger Stop hook in the checkout. Run `~/.agents/ship/link-local.sh --hook-only`
   on every invocation (see [Cycle state ledger](references/state.md)).

A `CLAUDE.md` next to the resolved config is part of the config. Read it
right after `ship.md`; no harness loads it on its own. It holds the project
instructions for the Maestro (conventions, house rules, memory pointers).
Apply it for the whole cycle and copy the parts a seat needs into that seat's
brief.

If the ticket does not exist yet, clarify the scope through the host's question
tool and prepare a concrete issue with the configured tracker workflow. Start
the ticket cycle once the required issue exists. Do not depend on a removed
interview alias.

## Scope and selection

Project-agnostic development cycle orchestrator for the Maestri canvas: read the project's ship config, fetch a ticket (Linear, GitHub issue, or Jira), gather codebase context, route to planner/design/executor teammates, fan reviews out by project surface (backend-only, web, mobile), gate with the project's CI command, then ship (commit, push, PR via gh, babysit, then merge only with the user's explicit permission). Keeps a per-ticket cycle state ledger so the cycle survives context clears. Use when the user says "ship TICKET-KEY" (e.g. "ship PRE-12", "ship #454", "ship SCH-603"), "run the cycle", "pick up the next ticket", or "/ship". Every ship runs on a fresh git-worktree Maestri floor unless the request says "ground" ("/ship HOB-66 ground"). Also handles first-time project setup via "/ship init".

## Workflow references

Before any work, read [Cycle state ledger](references/state.md) and apply its resume rule. Resume the recorded next step instead of repeating completed phases.

Read each reference when its condition applies. References are parts of this skill. Project-relative commands still run from the selected checkout.

| Condition | Read |
| --- | --- |
| `/ship init`, or the project has no ship config | [Init flow](references/setup.md) |
| Select, connect, or recruit seats | [Seat matrix by surface](references/team.md) |
| Every ship, unless the request says `ground` | [Floor mode](references/floor.md) |
| Run or resume the normal ticket cycle | [The cycle](references/cycle.md) |
| `/ship review`, "review cycle", "review PR N", or a ledger with `Cycle: review` | [Review mode](references/review.md) and [Review briefs](references/review-briefs.md). They replace the cycle and floor step 0 |
| Before any work dispatch or seat reset | [Worker context hygiene and background dispatch](references/dispatch.md) |
| Update state, resume work, or handle context overflow | [Cycle state ledger and handoffs](references/state.md) |

The cycle reference defines intake through merge. Floor mode replaces team assembly for the master. Its floor Maestro runs the normal cycle. Preserve the existing recruitment, CI, and per-PR merge boundaries.
