## Two ledgers

Context is a cache. The ledger file is the memory. Both ledgers are a journal
with a materialized head, like a write-ahead log. The head is a fixed set of
short fields. The log is append-only.

### Hunt ledger — `~/career/state/hunt-<YYYY-MM-DD>.md`

One per hunt. Fans out into application ledgers.

```markdown
# hunt <YYYY-MM-DD> — hunt state

Phase: <0-assemble | 1-source | 2-triage | 3-shortlist | done>
Surfaces: <jobs-tab, posts — which are done>
Recency cut: <e.g. past-24h>
Found: <N raw>
Dropped at triage: <N, one line of reasons>
Shortlist: <N approved by the user, or "pending">
Next: <one concrete sentence>
Open: <one line per unresolved item, or "none">
Seats: <seat -> last task, clean|dirty>
Spawned: <app ledger slugs, one per line>

## Log

- 09:12 source runner started, jobs-tab and posts, past-24h
- 09:13 first preflight record triaged from state/source-hunt-2026-09-01/preflight.jsonl
- 09:15 source runner completed: 14 raw, see state/source-hunt-2026-09-01/events.jsonl
- 09:40 triaged to 5, dropped 9 (3 hybrid, 4 agency dup, 2 PHP), sent to user
```

### Application ledger — `~/career/state/app-<company>-<role-slug>.md`

One per posting the user approved. Independent. Resumable. Abandonable.

```markdown
# <company> — <role> — application state

Phase: <0-intake | 1-context | 2-tailor | 3-review | 4-package | 5-delivered | 6-applied | abandoned>
Segment: <us-direct | br-pj | agency>
Language: <en | pt | es>, decided at intake from the posting
Posting: <url, or "posts-only, no link">
Posted: <YYYY-MM-DD HH:MM, and age at intake>
Recruiter: <name · profile url · contact channel, or "none">
CV: <path to the tailored file, or "not started">
Review: <not run | BLOCKED: <check name>, because <exact reason> | PASS>
Note: <Maestri note name, or "none">
Next: <one concrete sentence>
Open: <one line per unresolved item, or "none">

## Log

- 10:02 intake, posting 6h old, 4 comments, language en
- 10:14 Quill dispatched to tailor from base-en.tex
- 10:41 Sieve review: BLOCKED by Role Eligibility, posting requires four hours of PST overlap and no approved source confirms it; LUCAS CONFIRMATION
- 10:52 Quill fix round 1
- 11:03 Sieve review: PASS. Resume Evidence 74/100, Recruiter Readability 81/100
- 11:05 note "apply-acme-senior-node" written, user notified
```

### Ledger rules

In force because a ledger that is expensive to write is a ledger that does not
get written.

- **Append, never rewrite the log.** One line per event: `- HH:MM <what
happened>`. Take the time from `date +%H:%M`. Never edit or reflow a line
  that is already there.
- **Rewrite the head only when a field changes.**
- **The ledger holds no narrative.** Raw search results, keyword corpora,
  analyzer reports and fix lists go in sibling files next to the ledger, or in
  their owning directory under `~/career/`. The log line names the file; it
  does not repeat it. A ledger past ~60 lines means narrative leaked in.
- **Phase values come from the lists above.** Do not invent one.

### The guard hook

`~/career/.agent/hooks/job-ledger-guard.py` is the shared script. Claude Code
registers it in `~/career/.claude/settings.json`. Codex registers it as a
`Stop` hook in `~/career/.codex/hooks.json`. Keep both local registrations in
sync. Run the Maestro from `~/career`. The script arms only when the hook
payload cwd is exactly `~/career`; nested Maestri workers do not own the
cross-seat ledger and must not be continued by this guard.

For Codex, the hook must be synchronous. It returns `decision: "block"` with
a continuation reason when an active ledger is stale. The `stop_hook_active`
input and the script's `.fired-*` files prevent a continuation loop. After a
change, review and trust the project hook with `/hooks`; Codex binds trust to
the exact hook definition.

It does not write the ledger. A hook is a shell command with no view of what
happened, so it guards the discipline instead: it blocks the turn when
a matching hunt or application artifact changed but its active ledger did not
move. Unrelated work from another concurrent seat does not stale every ledger.
That is the failure mode worth catching, the hunt advanced and nobody logged
it. It blocks at most once per ledger per session, so it cannot loop.

Its runtime files in `~/career/state/` are dotfiles: `.hookstamp` and
`.fired-*`. Leave them alone.

Write it for a reader with zero context. The head plus the config must be
enough to resume after a full context loss.

Append after each of these, without being asked: seat dispatched, seat
reported, triage done, shortlist approved, application ledger spawned, CV
drafted, review run, review result, fix round sent, package note written, user
notified, user confirmed applied, application abandoned.

**Resume rule.** On every `/find-me-a-job` invocation, before anything else,
list `~/career/state/`. Any ledger with Phase != done, applied, or abandoned
means you are mid-hunt: resume from its **Next** field. Do not redo finished
phases. Report every open application to the user before starting a new hunt;
a second hunt while three applications sit half-tailored is how work gets
lost. The user may dismiss an open hunt; then mark every open ledger
`abandoned` with a one-line reason, archive its PDFs under
`~/career/resumes/archive/<date>/`, and start the new hunt.

Delete a ledger only after the user confirms they applied, or explicitly
abandons it.

## Context overflow and handoffs

- **Your own overflow:** the ledger IS the handoff. Update it, tell the user
  to `/clear`, resume via the resume rule. No Maestri note needed.
- **Teammate overflow:** record its unfinished work in the ledger's **Seats**
  and **Open** fields, reset the seat with its Reset cmd, re-send one
  self-contained prompt covering the remaining work.
- **Mid and long term:** durable knowledge that outlives one posting goes to
  `~/career/ATS-KNOWLEDGE.md` with an evidence tag, or to an ai-memory wiki
  page. Never the ledger.

