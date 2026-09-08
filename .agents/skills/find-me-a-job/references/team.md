## Seat matrix

Every hunt gets these required seats:

| Seat             | Role               | When                                     |
| ---------------- | ------------------ | ---------------------------------------- |
| Resume Architect | `Resume Architect` | Every application. Writes, never grades. |
| ATS Analyzer     | `ATS Analyzer`     | Every application. Grades, never edits.  |

The Market Scout is a fallback seat. Recruit it only when the deterministic
source runner cannot parse a LinkedIn layout.

Optional, only when the user asks:

| Seat        | When                                                                                                       |
| ----------- | ---------------------------------------------------------------------------------------------------------- |
| Profile SEO | The LinkedIn profile itself needs work. Separate goal, separate portals, does not participate in the hunt. |

**The writer never grades its own output.** This is the load-bearing rule of
the whole system, the same way ship separates the executor from the reviewers.
An Architect that grades itself grades generously. Never collapse these seats.

**The Architect never fans out.** One dispatch carries one posting, or one
base-CV round. The Architect does not spawn subagents to tailor several
postings at once. The Maestro dispatches each posting and owns each handle.
Observed 2026-09-02: a fan-out of five subagents ran with no one polling the
leaves and produced five CVs nobody triaged.

**Ask before you recruit.** The two required hunt seats are approved by the
config and start fresh at every hunt without a further ask. The configured
Market Scout is approved only after a parser failure. Any seat outside the
matrix (Profile SEO, a new surface) needs a named yes from the user first; do
not recruit and then report it.

### Harnesses

Assign by task weight, not by habit. Claude for coordination and heavy
reasoning, Codex for light portal manipulation. The config's Seats table is
authoritative; this is the default it starts from.

| Seat             | Default harness                                                             | Why                                                                                              |
| ---------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Maestro          | `claude --model fable --effort high`                                        | Coordination, triage, judgement. Has a real background mechanism.                                |
| ATS Analyzer     | `claude --model fable --effort high`                                        | Routine delta review after deterministic gates. Use Opus only for unresolved semantic ambiguity. |
| Resume Architect | per config                                                                  | Writing quality, mid weight                                                                      |
| Market Scout     | `codex -m gpt-5.6-luna -c model_reasoning_effort=high -c service_tier=fast` | Portal driving and verbatim capture                                                              |

**The Maestro seat runs Claude Code.** Decision by Lucas, 2026-09-02, after a
Codex Maestro skipped triage and lost the dispatch handles. If Codex ever runs
the Maestro seat, it must follow the persistent exec-session form in
[Dispatch is always background](dispatch.md) for every dispatch, with no exception, and
it must still run triage itself.

Verified against the live CLIs on 2026-09-01. Do not guess these:

- `claude --model <fable|opus|sonnet|full-name>`,
  `claude --effort <low|medium|high|xhigh|max>`.
- `codex -m gpt-5.6-luna` and `codex -m gpt-5.6-sol` both confirmed.
- The reasoning key is `model_reasoning_effort`. `reasoning_model_effort` is
  **not** a key.
- `service_tier="fast"` is the correct key.
- `codex --strict-config` does not reject unknown `-c` overrides in 0.152.0,
  so it cannot validate a key name. Run the model to check.

Swap a live seat in place, never dismiss and re-recruit:

```
maestri recruit "<name>" --command "<launch command>" --replace "<name>"
```

`--replace` keeps the terminal node, its ropes and its canvas position. Chat
history does not survive, which costs nothing: roles are self-contained and
the ledger is the memory. Re-brief with `maestri ask` after a swap. A Codex
seat shows a directory-trust prompt on boot; answer it with
`maestri ask "<name>" --raw "1"` then `maestri ask "<name>" --raw "\x0d"` and
wait for the idle prompt. Two calls, see [Raw sends are two calls](dispatch.md).

