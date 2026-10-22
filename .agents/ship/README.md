# Ship directory

Files that the `/ship` cycle uses across every project. The cycle itself lives in the `ship` skill.

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Shared house rules for every project. Every project file imports it (see "Shared layer") |
| `<project>/CLAUDE.md` | House rules for one project. Required. It starts with the shared import. `AGENTS.md` next to it is a symlink to it |
| `<project>/ship.md` | Cycle config for one project: seats, gates, Jira and PR rules |
| `state/<project>/` | Cycle state. One ledger per ticket (`EN-5382.md`) plus briefs, reports and screenshots with a suffix (`EN-5382-*.md`) |
| `feedback/<project>.md` | Problem reports about the cycle itself, one `## <time> · <keys>` entry per report with the ledger context. The `ship-feedback` mod writes it (`/ship-feedback <text>`) |
| `ledger.py` | The one reader of ledgers: which files are ledgers, which project a folder belongs to, which ledgers an agent owns. `ledger-stop.py` imports it. The `ship-guard` and `context-handoff` mods run it. `test-ledger.py` checks it |
| `dispatch.py` | Runs a `maestri ask` dispatch and returns when the report files are written, because the ask does not always return. Exit 2 on a timeout. `test-dispatch.py` checks it |
| `ledger-stop.py` | Stop hook that blocks a turn when a ledger is stale |
| `floor-status-stop.py` | Stop hook that blocks a floor Maestro turn that did work with no `maestri floor status` post. Seats are exempt: one writer per floor. `test-floor-status-stop.py` checks it |
| `thread-guard.py` | PreToolUse and UserPromptSubmit hook: one Maestri Chat thread per ticket. Denies a `maestri say` for a ticket when the user is in another thread and points to the `<key>-outbox.md`, then hands the outbox back when the user writes in the ticket's thread. `test-thread-guard.py` checks it |
| `link-local.sh` | Sets up a checkout: `CLAUDE.local.md` link to the project house rules, plus the ledger and floor status Stop hooks and the thread guard |

`<project>` is the folder that the checkout's `CLAUDE.local.md` link points into. With no link, it is the folder name of the repo's main checkout. For a Maestri floor made as a clone (`.maestri/floors/<ground folder>--<branch>`), it is the part before `--`. Examples: `enerflo-next`, `localpay-api`.

## ledger.py

```sh
~/.agents/ship/ledger.py [dir]    # default: current dir
```

It prints JSON for the agent in that folder: `project`, `seat`, `floor`, `branch`, `ledgers` (the open ledgers that are its own) and `problems`. Change a ledger rule here only. Then run `python3 test-ledger.py`.

- A ledger is a `.md` file directly in `state/<project>/` whose head (the text above `## Log`) has a `# <key> — cycle state` title and a `Phase:` line. The file name is not checked, so `EN-5382.md`, `PB-B.md` and `9.md` are all ledgers. A file with only the title or only the Phase is a problem
- A ledger is open until its Phase starts with `done`, `closed` or `merged` (a step number before it is permitted)
- A ledger whose Phase starts with `paused` (for example `Phase: paused (6-gate)`) is not open. The ship-guard and context-handoff mods and the Stop hook ignore it. `ledger.py` lists its key in `paused`. To resume, put the Phase in the brackets back
- The ground agent owns every open ledger. An agent on a floor owns the ledger whose `Floor:` contains the floor folder or whose `Branch:` starts with the floor's branch. A seat (a role folder whose role name has no "maestro") owns none

## How seats load the house rules

Claude Code, Codex and Cursor all read `<repo>/CLAUDE.local.md`. Each checkout has it as a symlink:

```
<repo>/CLAUDE.local.md -> ~/.agents/ship/<project>/CLAUDE.md
```

- The file must stay git-ignored. The global gitignore (`~/.gitignore_global`) already has it
- The target is an absolute path, so an edit reaches every checkout at once
- Codex reads `CLAUDE.local.md` only when the repo root has no `AGENTS.md`

## link-local.sh

Sets up a checkout for the cycle: the `CLAUDE.local.md` symlink and the ledger Stop hook. It works for any project.

```sh
git wta ../my-wt -b EN-1234-thing                # git worktree add + link (global alias)
~/.agents/ship/link-local.sh [dir]               # hook + link an existing checkout (default: current dir)
~/.agents/ship/link-local.sh --hook-only [dir]   # hook only, no CLAUDE.local.md
```

`/ship init` runs it once the config is written: the full form when you agree to the link in the questionnaire, else `--hook-only`. Every `/ship` run calls `--hook-only` first, so the Stop hook is always registered.

The global alias is `alias.wta = !~/.agents/ship/link-local.sh --add` in `~/.gitconfig`.

What it does:

1. Finds the main checkout with `git worktree list`
2. Picks the target, first match wins:
   - the checkout's own `CLAUDE.local.md` link
   - the main checkout's `CLAUDE.local.md` link. This lets a repo use another project's rules (`frontend-pb-a` uses `localpay-api`)
   - `.agents/CLAUDE.md` in the repo, as a relative link, so worktrees resolve it too
   - `~/.agents/ship/<main folder name>/CLAUDE.md`
3. Skips everything when the repo has no ship config (`.agents/ship.md`, `.claude/ship.md`, `~/.agents/ship/<main folder name>/ship.md`) and no rules, so repos without a cycle stay untouched
4. Adds the ledger Stop hook to `.claude/settings.local.json`. It merges with the settings already there, and skips when the hook is already registered
5. Creates the link, unless `--hook-only` or there are no rules. Skips when `CLAUDE.local.md` already exists. It never overwrites
6. If git does not ignore `CLAUDE.local.md` or `.claude/settings.local.json`, adds it to `.git/info/exclude`. That file is in the common git dir, so all worktrees share it, and it is never committed

It is safe to run again on any checkout.

When to run it:

- New worktree: use `git wta`
- A worktree that another tool created (Codex app in `~/.codex/worktrees`, Claude Code `--worktree`): run `link-local.sh <dir>` once
- APFS floor (a copy-on-write clone): nothing to do. A clone copies the symlink as a symlink with the same absolute target

## ledger-stop.py

A Stop hook. It stops Claude from ending a turn while a ticket ledger is out of date.

It blocks only when all of these are true:

1. The session cwd is in a git repo, and `state/<project>/` exists. So a worktree or a clone with any folder name finds the right ledgers
2. `ledger.py` finds an open ledger in that folder. Files like `EN-5382-context.md` do not count
3. The transcript has a Bash call after the ledger's last write (mtime) that runs `maestri ask`, `git commit`, `git push` or `gh pr` at a command boundary (start, `&&`, `||`, `;`, `|`). A newline is not a boundary, so a heredoc that only mentions these words does not count

When it blocks, it lists the stale ledgers. The fix: append one `- HH:MM <what happened>` line to `## Log`, change the head only if a field changed, then stop. It blocks once per stop (`stop_hook_active`). Any error exits 0, so it never wedges a session.

Every open ledger of the repo counts, not only the ticket you work on. For a ledger with no news, log `- HH:MM no change to this ticket, stop hook check during the <TICKET> cycle`. To stop the checks for a closed ticket, set `Phase: done`.

Registration, per checkout, in the git-ignored `.claude/settings.local.json`. `link-local.sh` adds it:

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command", "command": "python3 /Users/lucasqueiroz/.agents/ship/ledger-stop.py" } ] } ] } }
```

Registered today in `enerflo-next` (main and the 3 Codex worktrees), `localpay-api` and `frontend-pb-a`.

## Ledger format

```
# EN-5382 — cycle state

Phase: 6-pr-open
Branch: ...
PR: ...
Next: ...

## Log

- 16:02 cycle started
```

`ledger.py` reads the head only: the text above `## Log`, 4000 characters at most. The full contract is in the ship skill, `references/state.md`.

## Shared layer

`CLAUDE.md` in this folder holds the rules that every project shares. Two limits:

- A Claude Code `@` import of a file outside the project needs an approval, which is stored once per project path. Every new role folder, worktree and floor is a new path
- Codex and Cursor do not expand `@` imports

Every project under this folder must import it. A new project gets this before its first cycle. A project with no rules of its own still gets the file with only the two lines below.

```markdown
@~/.agents/ship/CLAUDE.md

Open `~/.agents/ship/CLAUDE.md` with your file tool and follow it. It holds the ship house rules for every seat.
```

How a project wires it in:

1. The project `CLAUDE.md` starts with the two lines above. Project rules come after them and add to the shared rules. Do not copy shared sections into the project file. `AGENTS.md` is a symlink to `CLAUDE.md`, so Codex and Cursor see the line.
2. Every seat command in the project's `ship.md` starts with `trust-cwd &&`. It sets `hasClaudeMdExternalIncludesApproved` for the seat's own directory, so Claude seats do not stop on the import prompt.
3. The Maestro still copies Tools and Comments into every brief, for seats that skip the file.

The ground Maestro, launched by hand, shows the import prompt once per checkout unless `trust-cwd` runs there first.
