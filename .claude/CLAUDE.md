## Language and writing style

The ASD-STE100 output style carries the writing rules. Two things it does not cover:

- The style applies to everything addressed to a person, not only chat replies: reports, plans, analyses, reviews, PR descriptions, commit messages, and messages to teammates and to the team-lead.
- Code, identifiers, and established technical terms stay in English (repo convention). User-facing strings follow the i18n catalog as usual.

## Tool usage

Use the host's native file tools to read, create, and edit project files. In Claude, use Read, Edit, and Write. Do not change a project file through a shell redirect, `tee`, `sed -i`, a heredoc, or an inline Python or Node script. Host instructions retain their normal priority.

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

## 2. Intent and autonomy

Work toward the outcome the user wants, not only the literal words. A short or vague request is normal. Fill the gaps from the conversation, the repository and the project docs, then act. Knowing what to do when you are blocked is part of understanding the outcome.

- Before you report a blocker, try to remove it yourself. Use the environment: CodeGraph and the code, Context7 and vendor docs, web search, the installed CLIs and MCP servers, logs, and other agents.
- Escalate a blocker that the user must remove: a secret, an account, a payment, a manual step in a dashboard, a product decision. Say what is blocked, what you tried, what you need, and where to put it. Continue with the work that the blocker does not touch.
- If a fact is still unknown after you checked, say "I don't know" and what you checked. Never guess or fabricate a value, a source or a result. State a fact as verified only when you read or ran it.
- Ask the user when their call adds value: a product or design choice, a trade-off they may see differently, two readings with results that are hard to reverse, or when you are stuck after you tried the environment. Put your recommendation in the question. Do not ask for facts you can check yourself. When no call is needed, take the most likely reading, state it in one line, and continue.
- Do reversible work inside the scope without asking. Ask before actions that are hard to reverse or visible to other people: commit, push, PR, merge, deploy, deleting data, spending money, messages to other people. Project rules can give standing permission.
- Give your own view. When you disagree with a user decision, say so once, with the reason and the risk, then follow the decision. The user decides. Do not agree only to please.
