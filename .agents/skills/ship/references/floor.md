## Floor mode (the `floor` modifier)

`floor` is a modifier on a normal ship, not a subcommand. Position does not
matter: `/ship HOB-66 floor`, `/ship floor HOB-66` and "ship HOB-66 on a new
floor" are one request. Without it the cycle runs on the ground floor, as
before. Requires Maestro Mode.

**One master, one Maestro per floor.** In floor mode you do not run the ticket
cycle. You are the master: you create the floor, staff it, hand the ticket to a
floor Maestro, and step back. The floor Maestro runs steps 1 to 6 inside its own
clone with its own seats. Several floors can run at once; the master holds none
of their context.

**The ground floor rule.** The master stays on the ground floor and writes no
code, so the ground checkout sits on the base branch for the whole cycle. A
floor is a copy of the ground directory, so a floor created from a ground on
`main` gets a branch based on `main`. That is how the base stays correct; the
CLI has no `--base` flag. Two duties follow. Pull the base branch **before**
every `floor create`, or the floor starts stale and the PR needs a rebase. And
never `git checkout` a ticket branch on the ground floor, not even to look at
it; read the floor's clone instead.

**A recruit is not a Maestro.** `recruit`, `connect`, `dismiss`, `floor create`,
`notify`, `role *` and `preset list` are all Maestro-only. A floor Maestro has
`ask`, `check`, `note *` and `portal *` and nothing else. It asks the master for
the rest. Do not tell it to recruit its own seats.

Replace step 0 with this:

1. Pull the base branch on the ground floor.
2. `maestri floor create "<floor name>" --branch <the ticket branch>`. The name
   follows the config's floor naming convention; default to the ticket key plus
   a short slug. Never pass `--copy-ground`. The floor must come up **empty**.
3. Wait for the command to return. That is the entire step. Creating a floor
   staffs nothing. If a terminal you did not recruit appears there, ignore it;
   never adopt it as a seat.
4. Recruit the floor Maestro onto the floor, naming it from the config's floor
   Maestro pool and giving it the config's Maestro role. Omit `--dir`: the
   floor's own checkout is the point.
5. Pick the seats from the ticket's surfaces, ask the user to confirm the
   missing ones (see [Seat matrix by surface](team.md)), then recruit each approved
   seat with `--floor "<floor name>"`. Every recruit boots inside the clone,
   already on the branch.
6. `maestri connect "<Floor Maestro>" "<seat>"` for every seat. Recruits are
   wired to you, not to each other, so without this the floor Maestro cannot
   `ask` its own team.
7. Create the ledger (head filled, first log line) before you hand over.
8. `maestri ask "<Floor Maestro>" "<handoff>"`. The handoff carries: the ticket
   key, the floor name and clone path, the branch and its base, the seat roster
   by name, the ledger path, the ship config path, and these standing orders:
   run the cycle from the clone, own the ledger, dispatch every seat in the
   background, report to `<master name>` by name, ask the master for anything
   Maestro-only, and **never merge**. The handoff `ask` itself is a dispatch:
   fire it in the background too.

After the handoff you are a router. Answer the floor Maestro's requests, recruit
what it asks for, relay the user's merge permission, and keep the ledgers'
directory as your index of what is in flight. Do not re-derive a floor's
context; ask its Maestro.

The code lives in the clone, not the ground checkout. The floor Maestro runs the
gate, the commit, the push and the PR from that path. `maestri floor list`
prints it. Running the gate on the ground checkout gates the wrong tree.

The floor already carries the branch, so step 6 commits on it instead of
creating one. Everything else in the cycle is unchanged: same brief, same review
fan-out, same gate, same merge permission from the user. Landing the branch is a
merge of the PR, as usual; the floor itself is deleted by the user in the UI.

