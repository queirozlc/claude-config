# Editing ship config

Applies before any change to a file under `~/.agents/ship/` (except
`state/`, `feedback/`, `backup/`) or `~/.claude/skills/ship/`.

1. Find the rule first. Search every layer (house `CLAUDE.md` and `house/`,
   `<company>-shared/`, the project folders, the ship skill) for the topic.
   If a rule exists, rewrite that line. Never add a second one beside it
2. One rule, one layer: the highest layer where it is true (house, then
   company, then project). A rule two projects of one company share goes to
   `<company>-shared/`. Lower layers link to it, they never copy it
3. No history in config: no "(Lucas, <date>, <ticket>)" tags, no "was X",
   no "verified on <date>", no status snapshots (open PRs, names in use,
   what is installed today). Keep the reason only as one short clause when
   it stops a repeat mistake. History goes in the ledger log or `feedback/`
4. Check every fact on the real system before you write it: the path
   exists, the command runs, the preset or permission is what you say
5. After you move or rename a section, search the ship files and the memory
   folders (`~/.claude/projects/*/memory/`) for links to it and fix them
6. Read, Edit and Write only. Never change these files from Bash
