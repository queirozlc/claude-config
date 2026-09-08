# Setup prompt

Copy the text below into your coding agent (Claude Code, Codex, Cursor) on the new machine.

---

Set up this Claude Code config on my machine. The repo root is `$HOME`. Follow these steps in order and stop at the first failure you cannot fix.

1. Read `~/.claude/README.md`. It lists what is tracked and every external dependency with its source URL.
2. If the repo is not cloned yet, run the "Install on a new machine" block from the README. Before `git reset --hard origin/main`, tell me which existing files in `~/.claude` and `~/.agents` it will overwrite, and wait for my confirmation.
3. Run `sh ~/.claude/install.sh`. It is idempotent. Read its full output.
4. For every line that says `MISSING` or `failed`, install that tool with the simplest method for this OS, using the source URL from the README. Do not guess install commands. Read the tool's own README first.
5. Verify:
   - `codegraph --version` and `ai-memory --version` print a version.
   - `claude mcp list` shows `codegraph`, `ai-memory`, `context7`.
   - `claude plugin list` shows `ponytail`, `paper-desktop`, `atlassian`, `typescript-lsp`.
   - `find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print` prints only `elixir` or nothing.
6. If `ai-memory install-hooks` changed `~/.claude/settings.json`, show me the diff and commit it with the message `Rewrite ai-memory hook paths for <hostname>`.
7. Do not add, commit or push any file that is not already tracked. `~/.gitignore` is a whitelist. Never track sessions, transcripts, memories, history, caches, credentials or backups.

Report what was installed, what was skipped, and what still needs my action (logins, tokens, optional tools).
