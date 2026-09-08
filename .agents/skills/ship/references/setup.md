## Init flow (`/ship init`, or auto-triggered when no config exists)

One-time per project. Detect what is detectable, ask the user only what is
ambiguous, write the config, done. Never re-detect on normal runs — the
config is the cache. When init was auto-triggered by a ship request (e.g.
"ship SCH-603" with no config yet), continue straight into the cycle with
that ticket once the config is written — do not stop after init.

**Detect:**

- **Repo identity:** `git remote get-url origin` → org/owner. Match against
  `gh auth status` accounts and suggest the gh account. The GitHub MCP
  servers (github-personal / github-ravn / github-dexcare) are fallback
  tooling only; `gh` is the default.
- **CI gate:** look for `bin/ci`, root `Makefile`/`justfile` targets, and
  `package.json` scripts (`test`, `lint`, `typecheck`). Propose one command
  that gates commits.
- **Tracker hints:** ticket key patterns in recent branch names and commit
  subjects (`PRE-\d+`, `SCH-\d+`, `#\d+`), `linctl` configured workspaces,
  available Jira (Atlassian MCP) or GitHub issue tooling.
- **Surfaces** (drives seats and review focus):
  - `mobile` — Expo / React Native present (an `app.json` with expo, or
    `expo`/`react-native` in a package.json).
  - `web` — a web frontend (Next.js, Vite, Rails + Hotwire views, etc.).
  - `backend` — API/services code. A project with ONLY this is
    **backend-only**.
    A project can have several surfaces (e.g. Rails backend + Expo mobile).
- **Maestri seats:** run `maestri list`. Compare the workspace's existing
  agents/roles against the [seat matrix](team.md) for the detected surfaces.
  Recruit what is missing (`maestri recruit "Name" --preset "..." --role
"..."`); connect existing-but-disconnected teammates instead of
  re-recruiting. Record the exact role/agent names in the config. Ask the
  user for the partitura name if one exists (partituras are UI-only and
  invisible to the CLI).

**Ask the user** (only what detection could not resolve): tracker choice and
its workspace/team/project coordinates, ticket state names (in progress / in
review / done, or Jira transition names), seat model preferences, executor
constraint skills per surface, language rules for user-facing strings, and
where to write the config (repo `.agents/ship.md`, or the home fallback
`~/.agents/ship/<repo-name>.md` for employer repos).

**Write the config** using this template:

```markdown
# Ship config — <project name>

## Tickets

- Tracker: <linear | github-issues | jira>
- Tooling: <e.g. LinearMCP (workspace X, team Y, project Z) | gh issue / github-ravn MCP | Atlassian MCP (site, project key)>
- Ticket pattern: <regex, e.g. PRE-\d+ | #\d+ | SCH-\d+>
- States: in progress = <...>, in review = <...>, done = <...>

## Repo

- gh account: <account> (run `gh auth switch -u <account>` before gh operations)
- Base branch: <main | develop | ...>
- PR title format: <e.g. "PRE-XX: <summary>">

## Gate

- CI: `<command>` from the repo root. Red gate = no commit, no exceptions.

## Surfaces

- <backend | web | mobile>: <paths, e.g. backend/, app/>

## Seats

| Seat | Role / agent name in Maestri | When | Preferred agents | Reset cmd |
| ---- | ---------------------------- | ---- | ---------------- | --------- |
| ...  | ...                          | ...  | ...              | ...       |

## Executor constraints

### <surface or path>

<skills to load, style rules, tooling — injected verbatim into executor prompts>

## Notes

<language rules, misc project conventions>
```

