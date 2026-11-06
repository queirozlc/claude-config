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
  re-recruiting. Record the exact role/agent names in the config.

**Ask the user** (only what detection could not resolve): tracker choice and
its workspace/team/project coordinates, ticket state names (in progress / in
review / done, or Jira transition names), seat model preferences, executor
constraint skills per surface, language rules for user-facing strings, and
where to write the config (repo `.agents/ship.md`, or the home fallback
`~/.agents/ship/<repo-name>/ship.md` for employer repos).

**Write the project rules file** `~/.agents/ship/<repo-name>/CLAUDE.md`,
always. Layout and the "one rule, one place" rule: `~/.agents/ship/README.md`
"Shared layer". It starts with the house import and the company import:

```markdown
@~/.agents/ship/CLAUDE.md
@~/.agents/ship/<company>-shared/ticket-artifacts.md

Open `~/.agents/ship/CLAUDE.md` and `~/.agents/ship/<company>-shared/ticket-artifacts.md` with your file tool and follow them. The first holds the ship house rules for every seat; its Part 2 (the ticket gate) wins over any other text here. The second holds the company's tracker fields, QA audience and evidence forms.
```

After the two lines, only rules true for this repo alone. A rule the
company's other projects share goes to the company file; a rule true at
every company goes to the house file. `AGENTS.md` beside it is a symlink.
Then link the checkout: `~/.agents/ship/link-local.sh` (it registers the
hooks and links `<repo>/CLAUDE.local.md`; never overwrites an existing one).

**Learn the company** when `~/.agents/ship/<company>-shared/ticket-artifacts.md`
does not exist. The company is the owner of the tracker (the Jira site,
the Linear workspace, the GitHub org). The file has four fixed headings.
Init fills them by looking, the same four steps for every company, and
writes the source beside every fact. "unknown" where nothing was found; the
first ticket that learns it fills it in.

1. `## Tracker fields`: list the issue fields of the project (Jira
   `getJiraIssue` with `view: full` on a recent ticket, Linear `linear api`
   schema, GitHub issue template). Find the field that holds test steps,
   the transitions and which one requires it, and any review-checks field.
   Record ids and names
2. `## Test steps format`: read the user's last five tickets in that
   tracker that have test steps (`assignee = currentUser()` or author).
   Copy the shape they use: headings, numbering, where Expected goes,
   where images go and how wide, whether the plan lives in the ticket or
   the PR. Name the tickets read
3. `## Who reads the test steps`: ask the user one question: who tests, and
   what can they open (UI, API client, databases, logs, VPN, test
   accounts). Write "has" and "has not" lists, and the writing rules that
   follow (a step names the screen, the button and the value; Expected is
   what the tester sees; a check that needs access the tester lacks is not
   a step, it goes under Notes as "I checked X")
4. `## Evidence`: which environments count (local stack, sandbox, a shared
   dev env, UAT after deploy), from the repo docs and CI config, plus the
   data rules that apply there (PHI, tokens, test-account passwords)

The company file never repeats Part 2 of the house file. It names the
tracker field, the audience and the environments, nothing else.

**Map the company sources** when `~/.agents/ship/<company>-shared/sources.md`
does not exist, also for a company that already has `ticket-artifacts.md`.
It is the table the context gate (cycle step 2) reads: question, source,
company ids and limits. Copy the layout of
`~/.agents/ship/enerflo-shared/sources.md`.

1. Explore: the MCP servers in this session and in the project config
   (`.mcp.json`, `~/.claude.json` project entries), the CLIs on PATH, and
   the skills that name the company (AWS, VPN, Datadog, Argo CD, database)
2. Ask the user one question: which tools the company uses for tickets,
   chat, calls, logs, errors, deploys and data, and which ones need the
   user (a login, the VPN)
3. Probe each source read-only and write only the ids the probe returned:
   log service and env names, error-tracker projects, database ids, deploy
   contexts. "unknown" where the probe failed
4. Write the "How to use the table" rules: which rows a prod bug always
   uses, and which access is one line to the user

Keep about ten rows. Add a row later only when a cycle lost time finding it.

**Set up the checkout** after the config and the rules file are written
(mandatory): `~/.agents/ship/link-local.sh`. It keeps `CLAUDE.local.md`
and the hook settings git-ignored through `.git/info/exclude`, and writes
the per-seat MCP deny lists from `~/.agents/ship/mcp/profiles.json` into
`~/.claude.json` (`mcp/apply.py`). When the company uses an MCP server
the profiles do not name, add it to `servers` and to the `keep` list of
each seat type that needs it, nothing else. See `~/.agents/ship/README.md`.

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

Reset cmd is the seat's restart: `maestri recruit "<Name>" --preset "<P>" --command '<seat command>' --replace "<Name>"`. Not `/clear`.
`<P>` has Maestro on for the floor Maestro only. Every other seat uses a preset with Maestro off (create one with `maestri preset create "<Name>" --command "<cli>" --maestro off --quick-start off`).

## Executor constraints

### <surface or path>

<skills to load, style rules, tooling — injected verbatim into executor prompts>

## Notes

<language rules, misc project conventions>
```

