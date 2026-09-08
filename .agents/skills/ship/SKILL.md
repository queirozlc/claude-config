---
name: ship
description: "Run the Maestri ticket cycle. Use for /ship, ship TICKET, run the cycle, the next ticket, or /ship init. Supports isolated floors; merge requires explicit permission."
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
   `.claude/ship.md` (legacy), then `~/.agents/ship/<repo-name>.md` (for
   repos where personal orchestration config cannot be committed).
   If none exists, run the [Init flow](references/setup.md) before doing anything else.

If the ticket does not exist yet (the user brings a raw idea), stop: that is
the triage phase, run `/grill-me` first and come back once issues exist.

## Scope and selection

Project-agnostic development cycle orchestrator for the Maestri canvas: read the project's ship config, fetch a ticket (Linear, GitHub issue, or Jira), gather codebase context, route to planner/design/executor teammates, fan reviews out by project surface (backend-only, web, mobile), gate with the project's CI command, then ship (commit, push, PR via gh, babysit, then merge only with the user's explicit permission). Keeps a per-ticket cycle state ledger so the cycle survives context clears. Use when the user says "ship TICKET-KEY" (e.g. "ship PRE-12", "ship #454", "ship SCH-603"), "run the cycle", "pick up the next ticket", or "/ship". The word "floor" anywhere in the request ("/ship HOB-66 floor", "ship HOB-66 on a new floor") runs the cycle on a fresh git-isolated Maestri floor. Also handles first-time project setup via "/ship init".

## Workflow references

Before any work, read [Cycle state ledger](references/state.md) and apply its resume rule. Resume the recorded next step instead of repeating completed phases.

Read each reference when its condition applies. References are parts of this skill. Project-relative commands still run from the selected checkout.

| Condition | Read |
| --- | --- |
| `/ship init`, or the project has no ship config | [Init flow](references/setup.md) |
| Select, connect, or recruit seats | [Seat matrix by surface](references/team.md) |
| The request contains the `floor` modifier | [Floor mode](references/floor.md) |
| Run or resume the normal ticket cycle | [The cycle](references/cycle.md) |
| Before any work dispatch or seat reset | [Worker context hygiene and background dispatch](references/dispatch.md) |
| Update state, resume work, or handle context overflow | [Cycle state ledger and handoffs](references/state.md) |

The cycle reference defines intake through merge. Floor mode replaces team assembly for the master. Its floor Maestro runs the normal cycle. Preserve the existing recruitment, CI, and per-PR merge boundaries.

