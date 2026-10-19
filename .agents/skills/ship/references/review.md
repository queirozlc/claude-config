## Review mode

Review mode reviews a pull request that someone else opened. Nobody on the
canvas writes the fix. The result is a set of review comments, one per real
problem, that read like a careful human review by the user. The user decides
when and how they are posted.

Trigger: `/ship review <ticket | PR number | PR URL>`, or "start a review
cycle for <ticket>", "review PR <n>". One request may name several PRs: run
one floor per PR, in parallel.

The ship config, its `CLAUDE.md`, the ledger, dispatch and seat-prep rules
all apply as in a ship cycle. This file replaces [The cycle](cycle.md) and
step 0 of [Floor mode](floor.md). A project that needs a review-only rule
puts it in an optional `## Review` section of its `ship.md`.

### The reviewer's stance (copy into every review brief)

The author most likely wrote this PR with a model as strong as yours. So
for every finding, ask: **why would the author's model have missed this?**
A good answer names something the author could not easily see: a caller in
another module, data that only exists in production, a runtime state the
diff does not show, a rule in a file the change never opened. Without a good
answer, look again before you keep the finding.

- Never invent a problem to look useful. Approve with no comments is a normal
  result, and it is the right one for a PR that is good enough to merge
- Be critical and independent. Do not soften a real problem, and do not
  inflate a nit into a should fix
- Every finding needs evidence that the seat produced: a real-app repro, a
  spec that fails, or a `file:line` read that shows the path. No evidence,
  no finding
- Nobody asks for a number of findings. Zero is an answer

### Hard limits (copy into every brief)

- Never commit, push, amend, or rebase on the PR branch. It belongs to the author
- Never post on the PR or change the ticket. Only the master posts, and only
  after the user says so for that PR
- Local edits only to try something out (a spec that proves a bug). Revert
  them before the report. `git status` at the end equals `git status` at the start
- Dev database: an additive migration to run the PR is allowed. Take a dump
  first when a migration deletes or rewrites rows. Never reset, drop, or seed.
  Log every migration applied so the user can roll it back
- One serving floor at a time (see the config's Notes). Ask the master for the
  slot. When done, stop the servers and check the ports, because a child
  process can outlive its parent

### Floor and seats (the master)

1. Pull the base branch on the ground floor
2. `maestri floor create "<#PR KEY short title>" --pull-request <N>`. Wait
   for it to list (floor create is slow; never retry), then run
   `~/.agents/ship/link-local.sh "<floor path>"` and check `CLAUDE.local.md`
3. Recruit onto the floor, with the config's commands: a floor Maestro, a
   Static Code Reviewer, a Security Auditor, and a Web QA seat only when the
   PR touches the web surface or the bug shows in the UI. No Planner, no
   executor, no Design Planner
4. Connect the floor Maestro to each seat. Create the ledger (shape below)
5. Fill the handoff template from [Review briefs](review-briefs.md) and
   dispatch it in the background

### Phases

The floor Maestro runs R1 to R5. Each phase writes one file beside the ledger
and reports to the master.

| Phase value | Step | Who | Output |
| --- | --- | --- | --- |
| `1-intake` | R1. Read the ticket (description, acceptance criteria, Test Plan, attachments, every comment, links) and the PR (body, every comment and review thread, bots included) | floor Maestro | `<KEY>-intake.md` |
| `2-context` | R2. Explore the codebase with CodeGraph until you can explain the change, the old behavior on the base branch and the blast radius in your own words. Do not move on until you are proud of it | floor Maestro | `<KEY>-context.md` |
| `3-route` | R3. Turn the steps to reproduce and the Test Plan into concrete cases. When there are none, write them from the acceptance criteria | floor Maestro | `<KEY>-cases.md` |
| `4-execute` | R4. Run the PR. Reproduce the bug on base-branch code first when you can, then run every case on the PR. Run the PR's own specs. Mark each case pass, fail, or blocked with the reason | QA seat, or the floor Maestro when there is no web surface | `<KEY>-qa-report.md`, `<KEY>-evidence/` |
| `5-review` | R5. Static and security reviews in one background batch, while R4 runs or after it. Then triage every finding against the code and the R4 results | reviewers, then floor Maestro | `<KEY>-review-*.md`, `<KEY>-review-comments.md` |
| `6-awaiting-merge-permission` | R6. The master puts the comments file in a canvas note named `<repo> PR <N> review` and shows the user the verdict | master | canvas note |
| `done` | The review is posted, or the user dropped it | master | |

### Review scope (every reviewer brief carries it)

1. Useless comments: run `ponytail:ponytail-review` on the diff, then apply
   the house Comments rule. Judge each comment yourself, not from what anyone
   said about the PR
2. Useless tests: a test that checks a library, a mock, the framework, a
   constant or a trivial getter instead of the logic the PR changed. Also a
   changed branch that no test would catch if it broke
3. Performance: N+1 queries, missing indexes for new queries or columns,
   queries in loops, extra round trips, heavy re-renders, unbounded lists.
   Run the review skills the config's Seats section names first
4. Security: auth on every new entry point, tenant or org scoping, injection,
   data exposure, raw SQL in migrations and triggers. Run `/security-review` first
5. Correctness, the seat role's own checklist, and fit with the project's
   rules for the touched paths

### Triage (floor Maestro)

For each finding: check the evidence yourself, ask the stance question,
then keep it, downgrade it, or cut it. Write the cut findings with a one-line
reason in a `## Cut` section at the end of the comments file. The user reads
that section to see whether a seat invents problems; it is never posted.

Verdict, from what is left:

| Left after triage | Verdict | GitHub event |
| --- | --- | --- |
| nothing | approve | `APPROVE`, short body |
| nits only | approve with nits | `APPROVE` with the comments |
| a should fix or a blocker | request changes | `REQUEST_CHANGES` |

### Comments file: `<KEY>-review-comments.md`

Start with `## Summary`, 15 lines or less: the verdict, a case results table,
the count by severity, and anything for the user only (an out-of-scope bug,
a possible new ticket). Then one entry per finding:

````markdown
### <n>. <short title> · <blocker | should fix | nit>
`path/from/repo/root.ts:<start>-<end>` (lines on the PR head, right side of the diff)

```text
<the comment the user posts>
```
````

How a comment reads:

- Point at the exact line range and say what is wrong and why it matters.
  1 to 3 sentences. A nit is one sentence
- No suggestion blocks and no code. The author's agent writes the fix
- No proof in text. Proof is visual only, a screenshot or a before/after
  composite, and only when it helps. Give its path above the block
- When a screenshot cannot show the bug, add `To reproduce:` with 3 to 5
  steps, the last one being the wrong result. Every step is something a seat
  ran or read in code. Not for test gaps or plain nits
- The user's voice: first person singular, plain words, short sentences, no
  em dashes, sound like a teammate. Never mention agents, seats, tools, or
  review rounds. Never claim an impact nobody proved
- Comments about the Test Plan or a missing follow-up ticket go in the review
  body, not on a line

### Posting (master, after the user says so for this PR)

1. Check the PR head still equals the reviewed commit. If not, tell the user
2. Check each commented line on the head: it exists, it says what the
   comment claims, and it is inside a diff hunk
3. Build one JSON payload (`commit_id`, `event`, `body`, `comments[]` with
   `path`, `line`, optional `start_line`, `side: "RIGHT"`) in the scratchpad
   and post it with `gh api -X POST repos/<owner>/<repo>/pulls/<N>/reviews --input <file>`
4. Send the user the review link. Set the ledger to `done`

### Ledger

Same folder and head as a ship ledger, so the hooks and mods read it. Two
fields mark it as a review:

```markdown
Cycle: review of <author>'s PR (not ours)
PR: <url> (author <login>, head <short sha>)
```

`Open:` lists what the review left behind (migrations applied, test data,
parked files). Clockify follows the config, with one entry per review kind
for each PR: static review, security review, QA. Switch the timer when the
work changes kind.
