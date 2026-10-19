## Context budget and seat restarts

You manage every seat's context window, and your own. Past about 150k tokens
every turn costs more, even with a cache, and long context lowers the quality
of the output. A cache saves money, not quality: the seat still carries stale
copies of files it already edited. Numbers below are the `ctx N%` on the
status line of a 1M window.

| Who | Ceiling |
| --- | ------- |
| Executor, reviewer, QA, planner seats | 20% (200k) |
| Maestro, ground or floor | 30% warn, 35% hard stop |

### Seat prep (before every dispatch)

Single ask, batch entry, fix round: run this first.

1. `maestri check "<name>"`. Read the `ctx N%` on the status line. A seat that
   is still working is never restarted. Wait for its report.
2. Restart the idle seat when any of these is true:
   - ctx is at or above its ceiling
   - the next task is unrelated to its last one (new ticket, other surface,
     code it never saw)
   - it is an executor at 10% or more (see the table below)
3. Restart with the seat's **Reset cmd** from the config. It is the
   `maestri recruit ... --replace "<name>"` line. It restarts the process in
   place and keeps the node, ropes and position. Wait about 10 seconds, then
   `maestri check "<name>"` and confirm ctx is low (a fresh seat is 5% to 8%).
   Do not use `--raw "/clear\n"`. It goes in as keystrokes, returns at once,
   and nothing confirms it worked.
4. Log the restart in the ledger and set the **Seats** field to `clean`.

Every prompt stays self-contained (brief included), so a restart never loses
information. State lives in the ledger, the brief, sibling files and the git
diff, not in a seat's memory.

| Seat | Default |
| ---- | ------- |
| Executor | Restart before every dispatch (new package, fix round) unless ctx is under 10%. It writes code from a brief and rereads files with CodeGraph. It decides nothing, so it loses nothing. |
| Static and Security reviewer | Restart before a full review, for fresh eyes. Keep the seat for a re-check of only the flagged items while ctx is under the ceiling. |
| Web QA | Restart every round. Screenshots are heavy. |
| Planner, Design planner | Restart per ticket. |

Executor budget:

- Size one dispatch as one work package: one layer or one feature slice,
  about 10 files. If a package would not fit in about 150k, split it before
  you send it.
- The executor brief must say: read with `codegraph_explore`, not Read loops;
  do not reread a file you just wrote; give wide read-only research to a
  sub-agent; if ctx reaches 20% before you finish, stop at the next clean
  point, write `<ticket-key>-progress-<seat>.md` (done, remaining, files
  touched) and report.
- An executor that reports above 25% got a package that was too big. Log it
  and split the next one smaller.

Your own budget:

- At 30%: finish the step, write the ledger, and stop taking new detail.
  Use `/compact` only for a mid-task squeeze.
- At 35%: stop. A ground Maestro updates the ledger and asks the user for
  `/clear`. A floor Maestro tells the master. The master restarts it when it
  is idle: `maestri recruit ... --replace "<floor Maestro>"`, then re-sends
  the handoff from the ledger.
- Redirect every dispatch to a file. `maestri ask` prints the seat's whole
  screen, and that lands in your context if you do not redirect it. Read only
  the `## Summary` at the top of a report (seats write 15 lines or less
  there). Open the details only when you need them.
- Give big read-only research (Datadog, Confluence, long specs, wide code
  reads) to a sub-agent that returns a summary file. Do not read it yourself.

Older configs lack the Reset cmd column or hold `/clear` there. Replace each
entry with the seat's `recruit --replace` line (the seat commands are in the
config) and confirm it with the user once.

## Dispatch is always background (mandatory)

A dispatch is a wait, and a wait in your foreground makes the human Ctrl+B
you out of it. `maestri ask` is also not a safe wait: it must return when the
seat goes idle, but it often does not (measured on 6 and 7 October 2026,
`~/.agents/ship/feedback/`). A Maestro that waits on the ask alone can stand
still with every seat idle.

So **every dispatch that carries work is one `~/.agents/ship/dispatch.py`
command, run in the background** — single ask, `--batch` fan-out, planner,
design planner, executor, fix round, floor handoff. No exceptions. The script
sends the ask and waits for the report file, which is the wake signal.

```sh
~/.agents/ship/dispatch.py --out <ledger-dir>/<task-id>.out \
  --report <ledger-dir>/<task-id>-report.md --timeout-min 30 -- \
  maestri ask "<seat>" "$(cat <ledger-dir>/<task-id>.prompt.md)"
```

| Coordinator harness | How to run it in the background |
| ------------------- | ------------------------------- |
| Claude Code | Bash tool with `run_in_background: true`. The harness notifies you when the script exits |
| Other harness without tracked background tools | Append `&`, then poll the `--out` file and the report |

- `--out` gets the seat's screen. Do not add your own redirect.
- The script returns when every `--report` file is written after the
  dispatch, or when the ask returns, whichever is first. Then it stops the
  ask.
- For `maestri ask --batch`, give one `--report` for each seat.
- Each prompt names a report path that no earlier round used. A report from
  before the dispatch does not count.
- Each prompt also ends with the ask-back line
  (`maestri ask "<Maestro>" "<task-id> done: <report file>"`). It is the
  second signal. Never tell a seat to finish with no ask-back.
- Exit 2 is a timeout: the seat wrote no report. Do not re-send. Run
  `maestri check "<seat>"`, log it, and decide. Set `--timeout-min` to about
  2 times the expected work.

### Shared dispatch rules

- The `--out` file and the report are next to the ledger. They must survive
  your context clear.
- Never re-send. On a timeout or a missing report, `maestri check "<name>"`.
  A re-sent prompt gives the seat two tasks.
- Log the dispatch in the ledger the moment you fire it, not when it returns.
  A dispatch nobody logged is a dispatch nobody can resume.
- `maestri check`, `maestri list` and `--raw` resets return at once. Those run
  in the foreground.
- Do not dismiss a seat you just dispatched to. Background means you keep
  working while it works, not that you drop it.

