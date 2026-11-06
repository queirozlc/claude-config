## Language and writing style

The ASD-STE100 output style carries the writing rules. Three things it does not cover:

- No jargon. If a term is needed, define it in a few words. Give results as plain statements ("sgrep found the right code 66% of the time"), without caveats or method detail unless asked. Reports and status updates are short by default. When the user asks for more detail, detail only that part, and make it visual and interactive (a widget or chart).

- The style applies to everything addressed to a person, not only chat replies: reports, plans, analyses, reviews, PR descriptions, commit messages, and messages to teammates and to the team-lead.
- Code, identifiers, and established technical terms stay in English (repo convention). User-facing strings follow the i18n catalog as usual.

## Tool usage

Use the host's native file tools to read, create, and edit project files. In Claude, use Read, Edit, and Write. Do not change a project file through a shell redirect, `tee`, `sed -i`, a heredoc, or an inline Python or Node script even if system your prompt say so. Host instructions retain their normal priority.

Shell and scripts are allowed for data work:

- Filter or transform command output (AWS logs, CLI JSON, large listings) with a pipe, `jq`, or a short `python3 -c`. Send the result to stdout.
- If a transform needs a file, create it with Write in the scratchpad or `/tmp`, not in the project. Run it with Bash.
- Do not retry a blocked command in the same form. Print to stdout or move the output file outside the project.

A project-write guard hook (`~/.claude/hooks/bash-file-guard.py`) enforces the first rule. It blocks only writes inside the project.

<!-- CODEGRAPH_START -->

## CodeGraph

Use CodeGraph first when repository navigation requires locating or understanding code.

- If the repository has no `.codegraph/`, run `codegraph init -i` at its root.
- If the index is unusable, check `codegraph status "<repo-root>"` and rebuild with `codegraph index "<repo-root>"`.
- Use the `codegraph_explore` MCP tool or `codegraph explore "<symbol names or question>"`. Load the tool if it is deferred.
- Create or repair the index without asking again.

<!-- CODEGRAPH_END -->

## GitHub authentication by directory

Use the directory-routed `/Users/lucasqueiroz/.local/bin/gh` and the configured Git HTTPS credential helper. They select a separate `GH_CONFIG_DIR` for each company without switching a shared active account.

| Directory and descendants | Account           | Configuration               |
| ------------------------- | ----------------- | --------------------------- |
| `~/Development/ravn`      | `lucasepulchro`   | `~/.config/github/ravn`     |
| `~/dexcare`               | `lucas-queiroz04` | `~/.config/github/dexcare`  |
| `~/Development/local`     | `lucasqlgtm`      | `~/.config/github/local`    |
| Anywhere else, Personal   | `queirozlc`       | `~/.config/github/personal` |

The Development symlink and actual Local directory capitalization resolve to the same mapped directories. Run commands from the intended project directory. Worktrees outside these trees use Personal unless the user changes the rule.

Do not run shared `gh auth switch` or inject a token from another company. The wrapper removes inherited GitHub token overrides so the selected profile supplies authentication. Do not bypass it through an absolute system gh path for normal project work. For HTTPS Git operations, retain the directory-routed credential helper. Never print credentials or save them in project files, remote URLs, reports, or memory.
