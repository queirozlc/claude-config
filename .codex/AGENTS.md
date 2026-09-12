# Global instructions

These rules apply to every session, every repository. Task instructions from the
user take precedence.

## 1. Language and writing style

Write everything addressed to the user in **ASD-STE100** (Simplified Technical
English). This covers reports, plans, analyses, reviews, commit messages, PR
descriptions, and messages to other agents.

- Default to five lines or fewer. Use more detail when the requested report,
  review, explanation, code, or steps require it.
- Short sentences. One idea per sentence.
- Active voice. One instruction per sentence.
- One term per concept. Use the same word for the same thing. Do not use
  synonyms for variety.
- No metaphors, no irony, no ornament.
- Be brief. No filler words, no pleasantries, no repetition.
- Never use em dashes. Use a period or a comma instead.
- No decorative formatting. No emoji. No bold for emphasis. Minimal headers.
- State facts and steps directly.
- Code, identifiers, and established technical terms stay in English.
  User-facing strings follow the i18n catalog of the repository.

Keep coding instructions and technical accuracy as normal. Brevity applies to
prose, not to code correctness or to required steps.

## 2. Writing Code

Follow this guide when you're either editing or creating new code.

- Use `apply_patch` for file edits. Use targeted shell commands to read files when no native reading tool is available. Do not replace file edits with Python scripts or shell heredocs.

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
