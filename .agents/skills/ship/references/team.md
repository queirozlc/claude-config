## Seat matrix by surface

Every project gets, at minimum:

| Seat                 | When                                                                                                              |
| -------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Planner              | Complex tickets only (cross-cutting, ambiguous). Frontier model in its harness plan mode.                         |
| Executor             | Always. Frontier-but-fast tier (Codex Luna xhigh fast, Cursor Grok high fast, Cursor Composer fast, Claude Opus). |
| Static Code Reviewer | Always. Frontier model.                                                                                           |
| Security Auditor     | Always. Frontier model.                                                                                           |

Surface additions:

- **mobile** → add a **Design planner** (screen/flow planning seat), a
  **Mobile UI Executor**, and a **Mobile QA** that opens the change in a
  Maestri **device portal** (`maestri portal devices`) and walks every
  affected screen. Reuse an existing free portal/simulator; never spawn new
  simulators when one already runs.
- **web** → add a **Design planner** and a **Web QA** that opens the change
  in a Maestri **browser portal** and walks every affected page and flow,
  stressing edge cases with concrete repro steps.
- **backend-only** → NO QA or design seats. Compensate by deepening the two
  reviewers: the Static reviewer's prompt must emphasize performance (N+1
  queries, missing indexes, allocation hot paths, query plans) and the
  Security auditor gets the full attack-surface brief (auth, injection, data
  exposure, abuse).

**Activation is per ticket, not per project.** The matrix says what a project
_can_ staff. The files the ticket touches say what it _does_ staff. A
backend-only ticket in a project that also has a web or mobile surface gets no
QA seat, no design planner and no portal. Never open a device portal for a
ticket that does not touch the mobile surface.

**Ask before you recruit.** A seat already on the canvas needs no ask. Before
you spawn a seat that is missing, name it and wait for a yes: "This ticket
touches `assets/`. Recruit Ginny (frontend executor) and Dobby (Web QA)? y/n".
Recruit what the user approves, nothing more. This is a real question to the
user, not a rhetorical one; do not recruit and then report it.

