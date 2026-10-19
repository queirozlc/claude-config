## The cycle

### 0. Assemble the team

Floor mode (the default, unless the request says `ground`) replaces this step. See [Floor mode](floor.md).

`maestri list`. Fill the config's seat table: connect disconnected
teammates, recruit missing ones. If the canvas is empty and the config names
a partitura, ask the user to load it instead of recruiting from scratch.

### 1. Ticket intake

Fetch the issue with the config's tracker tooling. Move it to the config's
**in progress** state before any code is written. Keep the state accurate
for the whole cycle; a stale state is a bug. Create the cycle state ledger
now (see [Cycle state ledger](state.md)), with `Thread:` set to the Maestri
Chat color the ticket started in ([Thread per ticket](state.md#thread-per-ticket)).

### 2. Context pass (you, the Maestro)

Use CodeGraph first when repository navigation needs it. Create or repair the index according to the global instructions. If CodeGraph cannot run or answer the question, use targeted reads and `rg`. Produce a short context brief: what the
ticket asks, which files/symbols it touches, relevant constraints from the
project's AGENTS.md/CLAUDE.md, and prior decisions (check ai-memory if the
ticket references past work). This brief travels with every prompt you send.

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
