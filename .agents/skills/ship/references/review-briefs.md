## Review briefs

Fill the `<placeholders>` and send the text as it is. Do not rewrite a
template per review: the same words every time keep the reviews consistent.
Write each filled brief to `<state dir>/<KEY>-<name>.prompt.md` and dispatch
it with `dispatch.py` in the background. Every brief also gets the Tools,
Comments and Context sections of the project's house rules, and the line
"Do not post `maestri floor status`. Report to your Maestro." for seats.

### Handoff (master → floor Maestro)

```markdown
## Summary

You are <name>, floor Maestro for a PR REVIEW cycle: <KEY>, PR #<N> "<title>" by <author> (`<login>`). It is not our PR. Master: <master>. Report to <master> by name. Never talk to the user directly.

- Floor: <floor name> · <floor path>
- Branch: <branch>, head <sha> (base <base> @ <base sha>)
- Ledger: <state dir>/<KEY>.md (you own the head now, except `Thread:`)
- Cycle rules (READ FIRST): the ship skill's references/review.md, sections "The reviewer's stance", "Hard limits", "Phases", "Review scope", "Triage", "Comments file"
- Ship config: <ship.md path> and its CLAUDE.md
- Seats, already connected to you: <static> (Code Reviewer), <security> (Security Auditor)<, <qa> (Web QA)>
- Surfaces in the diff: <surfaces>. <files> files, +<add>/-<del>

## Standing orders

- Run R1 to R5 from the clone. R1 to R3 are yours (CodeGraph first, wide reading goes to a sub-agent). Do not start R4 until you can explain the change and its blast radius
- R4: ask <master> for the serving slot before any server starts. Brief the QA seat with the QA template, or run the cases yourself when there is no QA seat
- R5: one background `--batch` to the reviewers with the reviewer template. It may run while R4 runs
- Triage every finding yourself with the stance question. Cut what has no evidence, and list it under `## Cut`
- Own the ledger. Post `maestri floor status` with every ledger update
- Seat prep before every dispatch. Never re-send; on a timeout, `maestri check`
- Never commit, push, or post. Never run `clockify`
- Tell <master> at 30% context. Ask <master> to add or dismiss seats
- Report to <master> after R1, R3, R4 and when the comments file is final: `maestri ask "<master>" "<KEY> <phase> done: <file>"`

## First step

Read the cycle rules, then start R1.
```

### QA (floor Maestro → QA seat)

```markdown
Task <KEY>-qa-<round>. Run PR #<N> in the real app and report what you see. Do not judge the code.

- Cases: <state dir>/<KEY>-cases.md. Run every case, in order
- Before: when the cases say so, the API runs on base-branch code first. Reproduce the bug there and capture it
- After: run every case on the PR code
- Browser: follow the config's browser rule (skill, profile). Real routes, seed or test data
- Evidence in <state dir>/<KEY>-evidence/: one screenshot per changed state, at desktop and at 390 px, plus a before/after composite for the main state (the config's evidence style). Name files after the case id
- Mark each case pass, fail, or blocked, with one line of reason. A failing step names what you saw and what the case expected
- Never change account permissions or data you did not create for this run

Report: <state dir>/<KEY>-qa-<round>-report.md, starting with `## Summary` (a table: case, result, evidence file). Then `maestri ask "<floor Maestro>" "<KEY>-qa-<round> done: <report file>"`.
```

### Reviewer (floor Maestro → Static Code Reviewer and Security Auditor)

```markdown
Task <KEY>-review-<kind>-<round>. Review PR #<N> (<base>...<sha>) as a <Static Code Reviewer | Security Auditor>. Read-only: do not edit, commit, or post.

Context: <state dir>/<KEY>-context.md. Cases and their results so far: <state dir>/<KEY>-cases.md<, <KEY>-qa-report.md>.

<paste "The reviewer's stance" from references/review.md>

<paste "Review scope" from references/review.md. Static owns items 1, 2, 3 and 5. Security owns item 4, and items 3 and 5 in its area>

For each finding give: title, severity (blocker, should fix, nit), `path:start-end` on the PR head, what is wrong and why, and the evidence you produced (a spec that fails, a repro, or the `file:line` path you read). A finding without evidence is not a finding. If you find nothing real, say "no findings" and stop.

Report: <state dir>/<KEY>-review-<kind>-<round>-report.md, starting with `## Summary` (verdict and findings by severity). Then `maestri ask "<floor Maestro>" "<KEY>-review-<kind>-<round> done: <report file>"`.
```
