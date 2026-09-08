## Cycle state ledger (mandatory)

Context is a cache. The ledger file is the memory. Path:
`~/.agents/ship/state/<repo-name>/<ticket-key>.md`.

The ledger is a journal with a materialized head, like a write-ahead log. The
head is a fixed set of short fields. The log is append-only.

```markdown
# <ticket-key> — cycle state

Phase: <0-assemble | 1-intake | 2-context | 3-route | 4-execute | 5-review | 6-gate | 6-pr-open | 6-awaiting-merge-permission | done>
Floor: <floor name · clone path, or "Ground">
Maestro: <floor Maestro's agent name, or "master">
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

Write it for a reader with zero context. The head plus the ship config must be
enough to resume after a full context loss; the log is the audit trail.

Append after each of these, without being asked: ticket moved, brief sent, plan
approved, executor reported, findings triaged, fix round sent, gate run, commit
pushed, PR opened, merge permission requested, merged.

**Resume rule.** On every `/ship` invocation, before anything else, list
`~/.agents/ship/state/<repo-name>/`. A ledger with Phase != done means you
are mid-cycle: resume from its **Next** field. Do not redo finished
phases. Delete the ledger only after the PR merged and the ticket closed.

## Context overflow and handoffs

- **Your own overflow:** the ledger IS the handoff. Update it, tell the
  user to `/clear`, resume via the resume rule. No Maestri note needed.
- **Teammate overflow:** record its unfinished work in the ledger's
  **Seat sessions** and **Open items**, reset the seat with its Reset
  cmd, re-send one self-contained prompt that includes the remaining work.
- **Mid/long term:** durable decisions and multi-ticket knowledge go to
  ai-memory wiki pages (shared across all agents), never the ledger. See
  `/ai-memory-usage`.

Record a decision in ai-memory only when it will matter beyond this ticket.
