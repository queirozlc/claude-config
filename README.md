# Claude Code user config

Portable Claude Code setup. The git root is `$HOME`. Only `~/.claude` and `~/.agents` are tracked, through a whitelist in `~/.gitignore`.

This file is not loaded into Claude sessions. Only `CLAUDE.md`, `rules/`, `skills/`, `agents/`, `output-styles/` and the hooks in `settings.json` are.

## Install on a new machine

Using an agent: paste `~/PROMPT.md` into it. By hand:

```sh
cd ~
git init -b main
git remote add origin <repo-url>
git fetch origin
git reset --hard origin/main   # writes only the tracked files; existing untracked files stay
sh ~/.claude/install.sh
```

## Tracked

| Path | What |
|---|---|
| `.claude/CLAUDE.md` | Global instructions |
| `.claude/settings.json` | Permissions, hooks, env, enabled plugins, status line |
| `.claude/statusline.sh` | Status line (needs `git`, `jq`) |
| `.claude/rules/` | Always-on rules |
| `.claude/skills/` | Skills. Most are symlinks into `~/.agents/skills` |
| `.claude/agents/` | Custom subagents |
| `.claude/output-styles/` | Output styles |
| `.claude/hooks/` | Hook scripts referenced from `settings.json`. `no-bash-file-edits.sh` blocks file edits made through Bash so the agent uses Read, Edit and Write |
| `.agents/skills/` | Skill content shared by all agents (Claude Code, Codex, Cursor) |
| `.agents/ship/ledger-stop.py` | Stop hook for the ship workflow |
| `.agents/ship/state/` | Only `.gitkeep`. Ship state is never tracked |

Everything else under `$HOME` is ignored. Sessions, projects, memories, history, caches, credentials and backups must stay untracked.

## Dependencies

Installed by `install.sh`:

| Tool | Used by | Source |
|---|---|---|
| codegraph | MCP server `codegraph`, `UserPromptSubmit` hook `codegraph prompt-hook` | https://github.com/colbymchenry/codegraph |
| ai-memory | MCP server `ai-memory` (http://127.0.0.1:49374), hooks on most lifecycle events | https://github.com/akitaonrails/ai-memory |
| ponytail | Plugin `ponytail@ponytail` | https://github.com/DietrichGebert/ponytail |
| paper-desktop | Plugin `paper-desktop@paper` | https://github.com/paper-design/agent-plugins |
| atlassian, typescript-lsp | Plugins from `claude-plugins-official` | https://github.com/anthropics/claude-plugins-official |
| context7, mobbin | HTTP MCP servers (stored in `~/.claude.json`, not in this repo) | https://mcp.context7.com/mcp, https://api.mobbin.com/mcp |

## Notes

- `ai-memory install-hooks` rewrites the ai-memory hook commands in `settings.json` with absolute paths for the current machine. Commit that diff after running it on a new machine.
- `.claude/skills/elixir` is a link into a local project and is gitignored.
- `~/.agents/.skill-lock.json` records where each skill in `~/.agents/skills` came from, for `npx skills update`.
