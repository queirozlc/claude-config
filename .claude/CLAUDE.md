## 1. Language and writing style

The ASD-STE100 output style carries the writing rules. Two things it does not cover:

- The style applies to everything addressed to a person, not only chat replies: reports, plans, analyses, reviews, PR descriptions, commit messages, and messages to teammates and to the team-lead.
- Code, identifiers, and established technical terms stay in English (repo convention). User-facing strings follow the i18n catalog as usual.

## 2. Never guess or fabricate

- Say "I don't know" rather than guess. Do not fill a gap with a plausible value from a nearby schema, enum, or example.
- State a fact as verified only when you read or checked it. Do not attribute a value to a source you did not read.
- When a value is not observable from the context, tools, or files, say it is not observable. State uncertainty in plain words.

## 3. Tool usage

Use the host's native file tools for reading and editing when available. In Claude, use the available Read, Edit, and Write tools. Do not replace native edits with Python scripts or shell heredocs. If a host has no native reading tool, use targeted shell reads. Host instructions retain their normal priority.

<!-- CODEGRAPH_START -->

## CodeGraph

Use CodeGraph first when repository navigation requires locating or understanding code.

- If the repository has no `.codegraph/`, run `codegraph init -i` at its root.
- If the index is unusable, check `codegraph status "<repo-root>"` and rebuild with `codegraph index "<repo-root>"`.
- Use the `codegraph_explore` MCP tool or `codegraph explore "<symbol names or question>"`. Load the tool if it is deferred.
- Create or repair the index without asking again. If CodeGraph cannot run or answer the question, state the limitation and use targeted reads and `rg`.

<!-- CODEGRAPH_END -->

## GitHub authentication by directory

Use the directory-routed `/Users/lucasqueiroz/.local/bin/gh` and the configured Git HTTPS credential helper. They select a separate `GH_CONFIG_DIR` for each company without switching a shared active account.

| Directory and descendants | Account | Configuration |
| --- | --- | --- |
| `~/Development/ravn` | `lucasepulchro` | `~/.config/github/ravn` |
| `~/dexcare` | `lucas-queiroz04` | `~/.config/github/dexcare` |
| `~/Development/local` | `lucasqlgtm` | `~/.config/github/local` |
| Anywhere else, Personal | `queirozlc` | `~/.config/github/personal` |

The Development symlink and actual Local directory capitalization resolve to the same mapped directories. Run commands from the intended project directory. Worktrees outside these trees use Personal unless the user changes the rule.

Do not run shared `gh auth switch` or inject a token from another company. The wrapper removes inherited GitHub token overrides so the selected profile supplies authentication. Do not bypass it through an absolute system gh path for normal project work. For HTTPS Git operations, retain the directory-routed credential helper. Never print credentials or save them in project files, remote URLs, reports, or memory.

## Completion and validation

Finish the requested scope and verify the result. Save large deliverables as files when needed; do not require a manual continue response merely because output is long.

Executors, testers, and reviewers must prioritize meaningful behavior coverage over test count. Reuse existing coverage. Add tests only for an uncovered changed behavior or concrete risk. Do not create redundant tests or tests that mirror implementation details. Run affected checks and required repository gates. Repeat checks after relevant changes or failures, not after every intermediate edit.
