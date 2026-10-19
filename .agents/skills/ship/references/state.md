## Cycle state ledger (mandatory)

Context is a cache. The ledger file is the memory. Path:
`~/.agents/ship/state/<repo-name>/<ticket-key>.md`.

The ledger is a journal with a materialized head, like a write-ahead log. The
head is a fixed set of short fields. The log is append-only.

```markdown
Master: <ground Maestro's agent name, from `You:` in `maestri list`>
--
# <ticket-key> — cycle state

Phase: <0-assemble | 1-intake | 2-context | 3-route | 4-execute | 5-review | 6-gate | 6-pr-open | 6-awaiting-merge-permission | done | paused (<phase before the pause>)>
Floor: <floor name · clone path, or "Ground">
Maestro: <floor Maestro's agent name, or "master">
Thread: <Maestri Chat thread color of this ticket, or none>
Branch: <branch> (base: <base branch> @ <sha>)
PR: <url, or none>
Ticket: <tracker state>
Next: <one concrete sentence>
Open: <one line per unresolved item, or "none">
Seats: <seat → last task, clean|dirty>

## Log

- 18:31 brief sent to Slughorn
- 19:02 executor reported, gate green, see <ticket-key>-executor-report.md
- 19:07 fix round 1, a2329a0 pushed, PR #17 open
```

**The head is a contract that tools read.** `~/.agents/ship/ledger.py` is the
one reader. The ledger Stop hook and the `ship-guard` and `context-handoff`
mods all use it, so a head that breaks the contract makes the cycle invisible
to them: no band, no context handoff, no stale-ledger check.

- **File.** `<ticket-key>.md`, directly in the state folder. Every key form is
  correct (`HOB-154`, `PB-A`, `537`). For a GitHub issue `#9` the file is
  `9.md`. Sibling files are `<ticket-key>-<name>`. Folders are permitted.
- **Title and Phase.** The head has the line `# <ticket-key> — cycle state`
  and a `Phase:` line, both above `## Log`. A file with only one of them is
  not a ledger, and the band shows that as a problem.
- **Floor.** `Ground` for a ground cycle. For a floor cycle, the floor name,
  then ` · `, then the clone path: the path ends with the floor folder. The
  floor Maestro finds its ledger by that folder.
- **Branch.** The line starts with the exact branch name. It is the second
  way a floor Maestro finds its ledger, and how the Stop hook assigns a
  commit to a ticket.
- **Who gets which ledger.** The ground Maestro gets every open ledger of the
  project: it runs the ground cycles and routes the floor cycles. A floor
  Maestro gets the ledger that names its floor folder or its branch. A seat
  gets none.
- **Review ledgers.** A review of someone else's PR uses the same file, head
  and Phase values, plus `Cycle: review of <author>'s PR (not ours)` above
  `Phase:`. See [Review mode](review.md).
- **Thread.** The Maestri Chat color that belongs to this ticket, one color
  per open ticket. See [Thread per ticket](#thread-per-ticket).
- **Check it.** After you create a ledger or change its Floor, Branch or
  Phase, run `~/.agents/ship/ledger.py` from your folder. It prints, as JSON,
  the open ledgers that are yours and each problem. Your ledger must be in
  `ledgers` and `problems` must be empty. If not, correct the head.

Rules, in force because a ledger that is expensive to write is a ledger that
does not get written:

- **Append, never rewrite the log.** One line per event: `- HH:MM <what
happened>`. Take the time from `date +%H:%M`. Never edit or reflow a line
  that is already there.
- **Rewrite the head only when a field changes.** Phase, PR and Ticket move a
  handful of times per cycle. That is the whole cost.
- **The ledger holds no narrative.** Briefs, plans, executor reports, review
  findings and fix lists go in sibling files
  (`<ticket-key>-brief.md`, `-fixlist-r2.md`, `-review-security.md`). The log
  line names the file; it does not repeat it. A ledger past ~60 lines means
  narrative leaked in.
- **Phase values come from the list above.** Do not invent one.
- **`Master:` is the first line of every ledger.** The context-handoff mod
  reads it, so a floor Maestro at its context ceiling knows who restarts it.
- **The head of a floor ledger has one writer: its floor Maestro.** The
  ground Maestro appends log lines to it and does not change its head. One
  exception: `Thread:` belongs to the Maestro that talks to the user, so the
  master writes it.

## Thread per ticket

Every ticket has its own Maestri Chat thread color. Never mix tickets in one
thread.

- **Assign.** At intake, write `Thread: <color>` with the color of the header
  that started the ticket. If an open ledger already owns that color, ask the
  user to start the ticket in a free color (`maestri recall list` shows the
  empty ones). A ticket that starts from the terminal gets `Thread: none`
  until the user picks one.
- **Reply in it.** `maestri say` posts to the thread the user is in, and the
  CLI cannot pick another one. Tag every `maestri say` with the ticket:
  `SHIP_TICKET=<key> maestri say ...`, or `SHIP_TICKET=none` for a reply that
  is about no ticket. The `thread-guard.py` hook denies a tagged reply when
  the user is in another thread, and an untagged reply in a thread that a
  ticket owns.
- **Outbox.** When the guard denies a reply, append it to
  `<key>-outbox.md` beside the ledger (`## HH:MM` then the text). The guard
  gives the outbox back as context when the user next writes in the ticket's
  thread. Send it first, then delete the file. In the other thread you may
  send one line with no detail: "<key> update is waiting in <color>".
- **A blocking question** goes in the ticket's thread. Say that the work waits
  on it. Ask again in the same thread after 30 minutes with no answer.
- **Close.** When the ledger reaches `done`, ask the user in the ticket's
  thread to clear that color in Maestri (the CLI has no clear command). The
  color is free again.

Write it for a reader with zero context. The head plus the ship config must be
enough to resume after a full context loss; the log is the audit trail.

Append after each of these, without being asked: ticket moved, brief sent, plan
approved, executor reported, findings triaged, fix round sent, gate run, commit
pushed, PR opened, merge permission requested, merged.

**Stop hook (mandatory).** `~/.agents/ship/ledger-stop.py` blocks a turn
that ran a cycle event (`maestri ask`, `git commit`, `git push`, `gh pr`)
after a ledger's last write. On every `/ship` invocation, run
`~/.agents/ship/link-local.sh --hook-only` in the checkout first. It is a
no-op when the hook is registered. If it cannot register the hook, stop and
tell the user. When the hook blocks, append the log line it asks for and
stop. Log `- HH:MM no change to this ticket, stop hook check during the
<ticket-key> cycle` on open ledgers with no news.

**Resume rule.** On every `/ship` invocation, before anything else, list
`~/.agents/ship/state/<repo-name>/`. A ledger with Phase != done means you
are mid-cycle: resume from its **Next** field. Do not redo finished
phases. Delete the ledger only after the PR merged and the ticket closed.

**Pause.** The word is "pause", not "snooze". When the user pauses a cycle,
set `Phase: paused (<current phase>)` and append `- HH:MM cycle PAUSED by
the user`. A paused ledger is not open: the ship-guard and context-handoff
mods and the Stop hook ignore it, and `ledger.py` lists its key in
`paused`. Do no cycle work on it, and do not resume it by yourself. On
`/ship` with only paused ledgers, tell the user which cycles are paused and
stop. When the user says resume, put the Phase in the brackets back, append
`- HH:MM cycle RESUMED by the user`, and continue from **Next**.

## Context overflow and handoffs

- **Your own overflow** (35%, see [budget](dispatch.md)): the ledger IS the
  handoff. Update it, tell the user to `/clear`, resume via the resume rule.
  No Maestri note needed.
- **Teammate overflow:** record its unfinished work in the ledger's
  **Seats** and **Open** fields (or its `-progress-<seat>.md` file), restart
  the seat with its Reset cmd (see [seat prep](dispatch.md)), re-send one
  self-contained prompt that includes the remaining work.
- **Floor Maestro overflow:** the master restarts it and re-sends the
  handoff from the ledger.
- **Mid/long term:** durable decisions and multi-ticket knowledge go to
  ai-memory wiki pages (shared across all agents), never the ledger. See
  `/ai-memory-usage`.

Record a decision in ai-memory only when it will matter beyond this ticket.
