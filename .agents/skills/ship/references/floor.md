## Floor mode (the default)

Every `/ship TICKET` runs on a new floor. A floor is a git worktree of the
project: a branch in the same repository. The word `ground` in the request
(`/ship HOB-66 ground`) opts out and runs the cycle on the ground floor.
Position does not matter. The word `floor` is still accepted and changes
nothing. Requires Maestro Mode. If the project is not a git repository, or
Maestro Mode is off, tell the user and ask before you fall back to ground.

**One master, one Maestro per floor.** In floor mode you do not run the ticket
cycle. You are the master: you create the floor, staff it, hand the ticket to a
floor Maestro, and step back. The floor Maestro runs steps 1 to 6 inside its own
clone with its own seats. Several floors can run at once; the master holds none
of their context.

**The ground floor rule.** The master stays on the ground floor and writes no
code, so the ground checkout sits on the base branch for the whole cycle. A
floor is a worktree cut from the ground checkout, so a floor created from a
ground on `main` gets a branch based on `main`. That is how the base stays correct; the
CLI has no `--base` flag. Two duties follow. Pull the base branch **before**
every `floor create`, or the floor starts stale and the PR needs a rebase. And
never `git checkout` a ticket branch on the ground floor, not even to look at
it; read the floor's clone instead.

**A floor Maestro is a Maestro.** It has the full `maestri` toolset. Two rules
split the work, and they are rules, not missing capabilities:

- The master creates floors and recruits the floor Maestro and the first
  seats, because adding a seat needs the user's yes (see
  [Seat matrix by surface](team.md)).
- A floor Maestro restarts its own seats with `recruit ... --replace` (see
  [seat prep](dispatch.md)). It does not add or dismiss seats. It asks the
  master for that. The master restarts the floor Maestro.

Replace step 0 with this:

1. Pull the base branch on the ground floor.
2. `maestri floor create "<floor name>" --branch <the ticket branch>`. The name
   follows the config's floor naming convention; default to the ticket key plus
   a short slug. Never pass `--copy-ground`. The floor must come up **empty**.
3. Wait for the command to return. That is the entire step. Creating a floor
   staffs nothing. Then run
   `~/.agents/ship/link-local.sh "<floor path>"` before any recruit. `CLAUDE.local.md`
   and `.claude/settings.local.json` are git-ignored, so a worktree does not carry
   them. The script gives the floor the same `CLAUDE.local.md` link as the ground
   (it reuses the ground's link target) and the ledger Stop hooks. Check with
   `ls -l "<floor path>/CLAUDE.local.md"`. If the link is missing, stop and fix it;
   a floor without it has no house rules. If a terminal you did not recruit appears there, ignore it;
   never adopt it as a seat.
4. Recruit the floor Maestro onto the floor, naming it from the config's floor
   Maestro pool and giving it the config's Maestro role. Omit `--dir`: the
   floor's own checkout is the point.
5. Pick the seats from the ticket's surfaces, ask the user to confirm the
   missing ones (see [Seat matrix by surface](team.md)), then recruit each approved
   seat with `--floor "<floor name>"`. Every recruit boots inside the clone,
   already on the branch.
6. `maestri band create "<floor name>" --floor "<floor name>" --without-me`.
   Recruits are wired to you, not to each other. The band puts the floor
   Maestro and every seat on that floor in one band, so the floor Maestro can
   `ask` its own team, and the canvas shows the team as one node. You stay
   outside the band and keep your own rope to each member. Check with
   `maestri list` that every seat is in the band before the handoff.
7. Create the ledger (head filled, first log line) before you hand over.
8. `maestri ask "<Floor Maestro>" "<handoff>"`. The handoff carries: the ticket
   key, the floor name and clone path, the branch and its base, the seat roster
   by name, the ledger path, the ship config path, and these standing orders:
   run the cycle from the clone, own the ledger, make every seat log
   its seat-to-seat messages (see below), dispatch every seat in the background, run the seat prep before every dispatch, tell `<master name>`
   at 30% context so it can restart you, report to `<master name>` by name, ask the master to add or dismiss seats,
   and **never merge**. The handoff `ask` itself is a dispatch:
   fire it in the background too.

**Seats may talk to each other, on the record.** In a band every member can
reach every other member. A seat may `maestri ask` another seat directly, for
a question or a finding. The ledger must show every such message:

- The seat that sends the ask appends one line to the ledger's `## Log`
  before it sends: `- HH:MM <from> → <to>: <why>`. Seats only append to the
  Log. The head stays the floor Maestro's.
- The seat names the exchange in its own report to the floor Maestro.
- The floor Maestro still dispatches the work packages through `dispatch.py`,
  triages the review findings, and has the final say on a fix.
- The floor Maestro talks to the master. Seats do not.

After the handoff you are a router. Answer the floor Maestro's requests, recruit
what it asks for with `--floor "<floor name>" --band "<floor name>"` so the new
seat joins the band and gets its connections, relay the user's merge permission, and keep the ledgers'
directory as your index of what is in flight. Do not re-derive a floor's
context; ask its Maestro.

The code lives in the clone, not the ground checkout. The floor Maestro runs the
gate, the commit, the push and the PR from that path. `maestri floor list`
prints it. Running the gate on the ground checkout gates the wrong tree.

The floor already carries the branch, so step 6 commits on it instead of
creating one. Everything else in the cycle is unchanged: same brief, same review
fan-out, same gate, same merge permission from the user. Landing the branch is a
merge of the PR, as usual; the floor itself is deleted by the user in the UI.

