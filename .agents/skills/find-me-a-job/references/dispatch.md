## Dispatch is always background (mandatory)

`maestri ask` blocks until the target goes idle. A blocking ask in your
foreground makes the human interrupt your own wait. So **every dispatch that
carries work runs through your harness's background mechanism** — single ask,
`--batch` fan-out, fallback Scout run, tailor, review, fix round. No exceptions.

| Harness                          | Background mechanism                                                                                                                                                                                                              |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code                      | Bash tool with `run_in_background: true`, then `Monitor` / `TaskOutput`                                                                                                                                                           |
| Codex with unified exec sessions | Run `maestri ask "<seat>" "<prompt>" > ~/career/state/<slug>-<seat>.out 2>&1` through `exec_command` with a short yield and **no `&`**. Record the returned session ID, then poll that session with `write_stdin` until it exits. |

Rules:

- Redirect the output to a file next to the ledger. The reply is diagnostic
  transport evidence and must survive a context clear.
- In Codex, set `yield_time_ms` to about 1000 so `exec_command` returns a live
  session ID while `maestri ask` remains attached. Write that session ID to
  the ledger immediately. Poll it with empty `write_stdin` calls every 20 to
  30 seconds. A user message can interrupt the active poll, but the exec
  session remains alive; resume the same session ID.
- **Never append `&` inside the Codex exec command.** Observed 2026-09-04: the
  parent shell exited, the recorded process disappeared, the `.out` file
  stayed empty, and Kestrel continued remotely with no result channel.
- Completion requires the exec session to exit, the task sentinel to verify,
  and every artifact named in the sentinel to exist. The `.out` reply is
  diagnostic transport evidence. It is not the completion signal.
- Maestri can return only the visible terminal screen for a long reply. If the
  final report can exceed one screen, give the worker a separate
  `~/career/state/<slug>-<seat>.report.md` path in the original prompt. The
  worker writes the complete report there and returns only a short status and
  that path. Completion then requires the exec session to exit, the task
  sentinel to verify, and the complete `.report.md` artifact. Read the report
  artifact before making the next decision. Do not use `maestri ask`
  from the worker to report back; the project rules prohibit it.
- Poll, do not re-send. On timeout or an empty file, `maestri check "<name>"`
  is a progress view only. Never paste its screen into the `.out` file; the
  `.out` file holds the seat's reply and nothing else.
- If an older dispatch already lost its exec session while the seat is still
  working, do not resend the work. Open one persistent exec session that
  polls `maestri check` until the seat is idle. Then send one report-only ask
  through the correct persistent exec-session form and capture that reply in
  the original `.out` path. If that reply is truncated, send one final
  report-save ask that writes the complete report artifact and returns only
  its path. Do not repeat the underlying work.
- Log the dispatch in the ledger the moment you fire it, not when it returns.
  A dispatch nobody logged is a dispatch nobody can resume.
- `maestri check`, `maestri list`, `maestri note *` and `--raw` resets return
  at once. Those run in the foreground.

## Worker context hygiene

You manage every seat's context window, not only your own.

- Before you send a seat a task unrelated to its last one (a different
  posting, a different segment), reset its session:
  two raw calls: `maestri ask "<name>" --raw "<reset cmd>"` then
  `maestri ask "<name>" --raw "\x0d"`, with the config's Reset cmd.
  **Raw sends are two calls: text first, Enter alone second.** Verified
  2026-09-02 on a Codex seat: text and terminator in one call (`"/new\n"`
  or `"/new\x0d"`) arrive as one burst, the TUI treats it as a paste, and
  the terminator becomes a line break; the command sits unsent under a
  blank line. A lone `"\x0d"` in a second call submits it. Send only to an
  idle seat, then confirm with `maestri check` that the composer is empty
  and context shows 0% used. If a stray line is in the composer, clear it
  with backspaces (`--raw "\x7f\x7f\x7f\x7f\x7f\x7f"`) before the next send.
- Never reset a seat mid-task while it holds useful state.
- After a Codex `/new` reset, wait until `maestri check` shows the idle
  prompt again before you send the next ask. A prompt sent during the restart
  is swallowed and the seat sits idle at 0% context (seen 2026-09-01).
- Every prompt stays self-contained, so a reset never loses information.
- Track each seat's last task in the ledger's **Seats** field. Dirty context
  plus an unrelated next task means reset first.

