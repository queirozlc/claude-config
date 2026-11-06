## The cycle

### 0. Assemble the team

Floor mode (the default, unless the request says `ground`) replaces this step. See [Floor mode](floor.md).

`maestri list`. Fill the config's seat table: connect disconnected
teammates, recruit missing ones.

### 1. Ticket intake

Fetch the issue with the config's tracker tooling. Move it to the config's
**in progress** state before any code is written, unless the config says a
status move needs the user's OK: then ask for it in the intake report. Keep
the state accurate for the whole cycle; a stale state is a bug. Create the cycle state ledger
now (see [Cycle state ledger](state.md)), with `Thread:` set to the Maestri
Chat color the ticket started in ([Thread per ticket](state.md#thread-per-ticket)).

### 2. Context gate (you, the Maestro)

Work alone until you can explain the problem. Do not ask the user for
context you can get yourself.

1. Read the company sources file, `~/.agents/ship/<company>-shared/sources.md`
   (setup writes it, see [Init flow](setup.md)). Use every source that fits
   the ticket: the full ticket with comments, attachments, epic and links,
   then chat threads, calls, logs, error trackers, real data and the real
   screen. Read again on every blocker
2. Explore the code with CodeGraph first. If CodeGraph cannot run or answer
   the question, use targeted reads and `rg`
3. Bug: reproduce it on base-branch code (local stack, or prod read-only)
   and save the evidence. Other tickets: run the current behavior the
   ticket changes. If you cannot reproduce, write what you tried
4. Write `<KEY>-context.md` beside the ledger: what the ticket asks, the
   root cause or the change point (`file:line`), the files and symbols it
   touches, constraints from the project rules, prior decisions, one line
   per source (what it showed, or why you skipped it), and open questions

Exit only when the root cause or change point has a trace or evidence and
every open question is one that only the user can answer. Then start the
cycle. This file travels with every prompt you send.

### 3. Route

- **Simple ticket** (most are: clear scope, known pattern, few files):
  straight to the Executor. Go to step 4.
- **Frontend screen/flow planning** (a web or mobile ticket that needs a
  screen designed or reshaped, not just implemented): send it to the Design
  planner seat. The Design planner
  reports the screen plan back via ask-back; you approve or iterate, then
  forward it to the frontend executor as part of the brief.
- **Complex ticket** (cross-cutting, ambiguous, or the brief exposed
  unknowns): send it to the Planner first, in its harness plan mode, with
  the report-back instruction (`maestri ask "<your name>" "<plan>"`), in the
  background like every other dispatch.
  Review, iterate until sound, then forward the approved plan plus the
  brief to the Executor.

### 4. Execute

Run the [seat prep](dispatch.md) on the Executor first. Then send the Executor
one self-contained prompt for one work package: ticket key and description,
your context brief, the approved plan if there is one, the config's
**Executor constraints** block for the touched surface(s), and the
report-back instruction (`maestri ask "<your name>" "<summary>"` when
done). Dispatch it in the background — see [Dispatch is always background](dispatch.md).

Universal constraints for every executor prompt, on top of the config's:
use the repository's required checks and meaningful coverage for the changed behavior. Reuse existing tests. Add a test only for an uncovered behavior or concrete risk; do not mirror implementation details or increase test count for its own sake. Apply this rule to executors, testers, and reviewers. Follow global CodeGraph and documentation rules.

### 5. Review fan-out

Run the [seat prep](dispatch.md) on every review seat before each dispatch,
and on the Executor before each fix round. Read a report's `## Summary`
first, not the whole file.

When the Executor reports back, fan out in one parallel batch with
`maestri ask --batch`, in the background, one entry per active review seat (Static + Security
always; QA seat when a frontend surface was touched). Each prompt: the
brief, the changed files, and that seat's review ask from the seat matrix. Tell each reviewer to identify actual coverage gaps, not demand a new test by default. Run only relevant checks plus required repository gates; retain the existing reviewer seats.

Triage the findings yourself: drop noise, send real issues back to the
Executor as a fix list, re-run only the reviews that flagged them. Loop
until clean. Two clean passes maximum on nitpicks; do not ping-pong style
opinions forever.

### 6. Gate and ship

1. Pass the config's CI command from the repo root. Red gate means no
   commit. Out-of-scope failures get reported to the user, never committed
   around.
   **Done means validated.** A green gate and a clean
   review are not the end of the cycle. Before the commit request, the
   executor runs every Test Plan case end to end on the local stack (real
   API, real UI), and records visual evidence for each case: screenshot or
   recorded request and response as an image, plus the UI before/after
   when a screen changed. A spec run, a log or a `file:line` alone does not
   count here. The commit request shows the evidence inline, case by case,
   with pass or fail. A busy local stack is not a reason to skip: free it.
   A case that truly cannot run gets a `waived: <reason>` proof row, and
   the request names it. Never ask for commit while the ledger or a report
   has a "not proven" item that can still run. The same holds under a
   standing permission to commit. The full gate is Part 2 of
   `~/.agents/ship/CLAUDE.md`. A company file names the environments, the
   QA audience and the tracker field (`~/.agents/ship/<company>-shared/ticket-artifacts.md`).
2. Use the directory-routed `~/.local/bin/gh`. Verify identity with
   `gh api user --jq .login` when authentication needs checking. Each company
   has its own `GH_CONFIG_DIR`; never change a shared active account. Follow
   the global directory/account mapping. If the project config disagrees,
   resolve the mismatch before authenticated work.
3. Commit, push, open the PR against the config's base branch, title in the
   config's format (ticket key first so the tracker links it).
4. Move the ticket to the config's **in review** state.
5. Run `/babysit` on the PR until it is mergeable: CI green, conflicts
   resolved, review comments triaged. Babysit never merges.
6. When mergeable, set Phase = `6-awaiting-merge-permission` in the
   ledger, report the PR state to the user, and STOP. Merge only after
   the user gives explicit permission for THIS PR. Permission for a
   previous PR does not carry over. No exceptions.
7. After the user approves and the merge lands, confirm the ticket closed
   (config's **done** state), ask the user to clear the ticket's thread
   color, delete the ledger, then pick up the next ticket or report the
   cycle done.
