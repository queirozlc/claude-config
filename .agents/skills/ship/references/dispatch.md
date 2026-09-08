## Worker context hygiene

You manage every seat's context window, not only your own.

- Before you send a seat a task unrelated to its last one (new ticket,
  different surface, review of code it never saw), reset its session:
  `maestri ask "<name>" --raw "<reset cmd>\n"` with the config's Reset cmd.
- Never reset a seat mid-task or mid-ticket while it holds useful state
  (the executor working the current ticket's fix list).
- Every prompt stays self-contained (brief included), so a reset never
  loses required information.
- Track each seat's last task in the ledger's **Seat sessions** field.
  Dirty context + unrelated next task = reset first.
- Older configs lack the Reset cmd column. Detect each seat's harness,
  confirm the command with the user once, add the column to the config.

## Dispatch is always background (mandatory)

`maestri ask` blocks until the target goes idle. A blocking ask in your
foreground makes the human Ctrl+B you out of your own wait. So **every
dispatch that carries work runs through your harness's background
mechanism** — single ask, `--batch` fan-out, planner, design planner,
executor, fix round, floor handoff. No exceptions.

| Coordinator harness | Background mechanism |
| ------------------- | -------------------- |
| Claude Code | Bash tool with `run_in_background: true`, then `Monitor` / `TaskOutput` |
| Codex | `exec_command` with `yield_time_ms: 1000`, then `write_stdin` on its returned `session_id`. Follow the procedure below. |
| Other harness without tracked background tools | `maestri ask ... > <ledger-dir>/<ticket>-<seat>.out 2>&1 &`, then poll the file |

### Codex coordinator procedure

Use this procedure when Codex is the coordinator or Maestro, regardless of
which harness runs the worker. It applies to every work dispatch, including
review batches and floor handoffs. The detached fallback does not apply.

1. Write a self-contained prompt file next to the ledger. Use a unique task ID
   for each seat and review or fix round. Specify the scope, inputs, expected
   output, and report path. Do not overwrite an earlier report. Give each seat
   at most one active task.
2. Tell the worker to write its full report to that path and finish its turn.
   Do not require a `maestri ask` back to this Codex coordinator. This replaces
   the ask-back examples elsewhere in this skill. The coordinator tracks the
   original dispatch until it returns. A floor Maestro still dispatches its
   own team through its own harness's background mechanism.
3. Run the command through `exec_command`, with `workdir` set to the task's
   checkout and `yield_time_ms: 1000`. Redirect output next to the ledger:

   ```sh
   maestri ask "<seat>" "$(cat <ledger-dir>/<task-id>.prompt.md)" > <ledger-dir>/<task-id>.out 2>&1
   ```

   Substitute real paths and quote them if needed. Use the same tracked tool
   session for `maestri ask --batch`. Do not append `&`, use `nohup`, or launch
   a detached subprocess. The tool yields while the command stays tracked.
4. If the tool returns a `session_id`, immediately record it in the ledger's
   Seats field with the task ID, output path, report path, and next action.
   Append the dispatch event to the log. If it exits immediately, inspect the
   exit status and report. Do not invent a session ID.
5. Poll the same session with `write_stdin`:

   ```json
   {"session_id":12345,"chars":"","yield_time_ms":20000,"max_output_tokens":1000}
   ```

   Replace `12345` with the returned ID. Continue useful independent work
   between polls. If `functions.exec` returns a running cell ID, resume it
   with `functions.wait` first to get the nested `exec_command` result. A
   functions cell ID is not an exec session ID.
6. After a user interruption, resume the same session. Do not resend the task.
   Do not end the cycle after announcing a dispatch. Wait for completion,
   read the output and report, and then continue the next cycle step. If a
   saved session is no longer available after a restart, inspect the output,
   report, and `maestri check` before deciding whether work needs resumption.

### Shared dispatch rules

- Redirect the output to a file next to the ledger. The reply is the seat's
  report; it must survive your context clear.
- Poll, do not re-send. On timeout or an empty file, `maestri check "<name>"`.
  A re-sent prompt gives the seat two tasks.
- Log the dispatch in the ledger the moment you fire it, not when it returns.
  A dispatch nobody logged is a dispatch nobody can resume.
- `maestri check`, `maestri list` and `--raw` resets return at once. Those run
  in the foreground.
- Do not dismiss a seat you just dispatched to. Background means you keep
  working while it works, not that you drop it.

