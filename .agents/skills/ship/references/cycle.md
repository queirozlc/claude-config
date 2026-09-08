## The cycle

### 0. Assemble the team

Floor mode (`floor` in the request) replaces this step. See [Floor mode](floor.md).

`maestri list`. Fill the config's seat table: connect disconnected
teammates, recruit missing ones. If the canvas is empty and the config names
a partitura, ask the user to load it instead of recruiting from scratch.

### 1. Ticket intake

Fetch the issue with the config's tracker tooling. Move it to the config's
**in progress** state before any code is written. Keep the state accurate
for the whole cycle; a stale state is a bug. Create the cycle state ledger
now (see [Cycle state ledger](state.md)).

### 2. Context pass (you, the Maestro)

Explore with CodeGraph when the repo has a `.codegraph/` index
(`codegraph explore "..."` or the MCP tool) before any grep/find/Read;
otherwise explore conventionally. Produce a short context brief: what the
ticket asks, which files/symbols it touches, relevant constraints from the
project's AGENTS.md/CLAUDE.md, and prior decisions (check ai-memory if the
ticket references past work). This brief travels with every prompt you send.

### 3. Route

- **Simple ticket** (most are: clear scope, known pattern, few files):
  straight to the Executor. Go to step 4.
- **Frontend screen/flow planning** (a web or mobile ticket that needs a
  screen designed or reshaped, not just implemented): send it to the Design
  planner seat, not the Planner and not `/grill-me`. The Design planner
  reports the screen plan back via ask-back; you approve or iterate, then
  forward it to the frontend executor as part of the brief.
- **Complex ticket** (cross-cutting, ambiguous, or the brief exposed
  unknowns): send it to the Planner first, in its harness plan mode, with
  the report-back instruction (`maestri ask "<your name>" "<plan>"`), in the
  background like every other dispatch.
  Review, iterate until sound, then forward the approved plan plus the
  brief to the Executor.

### 4. Execute

Send the Executor one self-contained prompt: ticket key and description,
your context brief, the approved plan if there is one, the config's
**Executor constraints** block for the touched surface(s), and the
report-back instruction (`maestri ask "<your name>" "<summary>"` when
done). Dispatch it in the background — see [Dispatch is always background](dispatch.md).

Universal constraints for every executor prompt, on top of the config's:
tests are mandatory (nothing ships without regression tests and passing
lint), CodeGraph before grep where indexed, context7 for library APIs.

### 5. Review fan-out

When the Executor reports back, fan out in one parallel batch with
`maestri ask --batch`, in the background, one entry per active review seat (Static + Security
always; QA seat when a frontend surface was touched). Each prompt: the
brief, the changed files, and that seat's review ask from the seat matrix.

Triage the findings yourself: drop noise, send real issues back to the
Executor as a fix list, re-run only the reviews that flagged them. Loop
until clean. Two clean passes maximum on nitpicks; do not ping-pong style
opinions forever.

### 6. Gate and ship

1. Pass the config's CI command from the repo root. Red gate means no
   commit. Out-of-scope failures get reported to the user, never committed
   around.
2. Verify the active gh account matches the config
   (`gh auth status`); `gh auth switch -u <account>` if not.
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
   (config's **done** state), delete the ledger, then pick up the next
   ticket or report the cycle done.

