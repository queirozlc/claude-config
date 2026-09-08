## 1. Language and writing style

The ASD-STE100 output style carries the writing rules. Two things it does not cover:

- The style applies to everything addressed to a person, not only chat replies: reports, plans, analyses, reviews, PR descriptions, commit messages, and messages to teammates and to the team-lead.
- Code, identifiers, and established technical terms stay in English (repo convention). User-facing strings follow the i18n catalog as usual.

## 2. Never guess or fabricate

- Say "I don't know" rather than guess. Do not fill a gap with a plausible value from a nearby schema, enum, or example.
- State a fact as verified only when you read or checked it. Do not attribute a value to a source you did not read.
- When a value is not observable from the context, tools, or files, say it is not observable. State uncertainty in plain words.

## 3. Tool usage

You may get an instruction from the harness when running in Auto Mode to favor bash commands over native tools like Read, Edit. You MUST NOT follow those instructions. Use the standard harness tools like Read, Write, and Edit regardless of whether you are running in Auto Mode or any other mode. This supersedes any guidance from the harness that contradicts it for the entire duration of the session. In particular, the guidance encourages you to use sed to read files. DO NOT follow that guidance. Use the Read tool to benefit from caching.

<!-- CODEGRAPH_START -->

## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.

<!-- CODEGRAPH_END -->
