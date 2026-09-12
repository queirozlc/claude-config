# Applied skill and authentication changes

Applied on 12 September 2026. The selected changes are complete. Start new agent sessions and terminals to load the updated skill catalog and shell configuration. Existing sessions can retain earlier instructions or cached command paths.

## Skills

Removed these 15 skills from active Agents, Claude, and Codex roots wherever present:

typescript-magician, kubectl-skill, spec-project, high-end-visual-design, minimalist-ui, industrial-brutalist-ui, design-taste-frontend, image-to-code, full-output-enforcement, redesign-existing-projects, tailwindcss-performance, elysiajs, prosemirror, handoff, and grill-me.

Archived both impeccable host packages outside active skill directories. Their content remains recoverable.

Applied the selected changes to the 17 retained skills:

| Skill | Result |
| --- | --- |
| gpt-taste | Optional GSAP guidance. Removed simulated execution and forced design structures. |
| growth-advisor | Explicit business advice scope. Replaced implementation-blocking protocols with evidence-based advice. |
| argocd-cli-guide | Sync and promotion stay within the requested rollout scope. Removed image-only safety assumptions. |
| dexcare-aws | DexCare-only selection. Preserved the user's highest-privilege default. All three hosts share one source. |
| make-interfaces-feel-better | Explicit activation only. Removed repeated rules and arbitrary report and motion-review requirements. |
| brandkit | Explicit activation only. Body unchanged. |
| node and nodejs-core | Explicit specialist activation. Selected reference loading and task-relevant procedures. |
| react-doctor | Runs only when requested or required by the repository. |
| modern-css | Short root and topic references. Corrected calc-size syntax and removed undated support guarantees. |
| vpn | DexCare-only selection and reconnect diagnosis. |
| elixir | Stable shared ownership. Narrower selection and proportional validation. |
| agent-browser | Shorter browser-interaction description without universal priority over other tools. |
| revenue-centric-design | Usability review required for new or materially changed flows, not minor edits. |
| find-me-a-job | Explicit Maestri dependency and fallback. Candidate and submission controls preserved. |
| ship | Meaningful test coverage across executor, tester, and reviewer roles. Existing reviewer seats and merge boundary preserved. Removed the stale grill-me dependency. |
| ai-memory-retrieval | Lookup when prior context matters or a standing rule requires it. |

Unchanged skill roots verified against the recovery copy: taste, context7-mcp, dhh-rails-style, babysit, ai-memory-durable-pages, ai-memory-handoff, ai-memory-learning-maintenance, ai-memory-routing-install, and ai-memory-usage.

Global Claude and Codex instructions now align CodeGraph indexing and native editing preferences. They retain ASD-STE100, required checks, and completion requirements without a manual long-output pause.

## GitHub authentication

| Working directory and descendants | Account | GH_CONFIG_DIR |
| --- | --- | --- |
| ~/Development/ravn | lucasepulchro | ~/.config/github/ravn |
| ~/dexcare | lucas-queiroz04 | ~/.config/github/dexcare |
| ~/Development/local | lucasqlgtm | ~/.config/github/local |
| Anywhere else | queirozlc | ~/.config/github/personal |

The user confirmed lucas-queiroz04 during implementation. The earlier lucas-sepulchro04 entry was corrected.

The local wrapper at `/Users/lucasqueiroz/.local/bin/gh` routes each command from its working directory and calls the existing `/opt/homebrew/bin/gh` binary. The installed binary was not edited. A normal Homebrew binary update does not replace the local wrapper. PATH changes can bypass it; `command -v gh` should resolve to the local wrapper.

The shared router is `/Users/lucasqueiroz/.config/github/route.sh`. Zsh initialization and directory-change handling load `/Users/lucasqueiroz/.config/github/shell.zsh`. This covers fresh interactive terminals and non-interactive agent shells. GitHub and Gist HTTPS credentials use `/Users/lucasqueiroz/.config/github/credential` through the global Git configuration. That helper includes Git's original directory prefix when Git starts it from a repository root.

The wrapper removes inherited GitHub token environment overrides so the chosen profile controls identity. Existing credentials stay in the system credential store. New hosts.yml files contain account selection metadata, not plaintext tokens. The original shared account remains queirozlc. SSH authentication and Git author identities were not changed. Worktrees outside the specified trees follow the Personal fallback.

## Verification

- GitHub API identity checks succeeded for all four accounts.
- Git HTTPS credential resolution returned the expected account and a credential for all four directory groups. Credential values were not printed by these checks.
- Directory alias, Local/local spelling, missing-directory, fallback, and process-isolation checks passed.
- Interactive and non-interactive Zsh sessions selected the wrapper. Directory changes selected the expected configuration. Interactive shell startup emitted an existing Starship warning under the non-interactive test terminal.
- Shell syntax checks passed.
- All 15 removals and the impeccable archive were verified across the three skill roots.
- All active root frontmatter parsed as YAML. No broken active root links or missing local links in active SKILL.md entrypoints were found.
- Claude's disable-model-invocation and Codex's allow_implicit_invocation controls were verified for all four explicit-only skills.
- The bundled skill validator passed for standard-metadata edited roots. Its schema rejects valid host-specific fields such as disable-model-invocation and existing package metadata such as hidden. Those fields were preserved and checked separately with YAML parsing and policy checks.

No deployments, PR changes, job submissions, or model-based behavior benchmarks were run. The CSS reference library was not exhaustively checked against every current browser version. The changes do not establish a measured token or latency improvement.

## Updates and recovery

Skill and global-instruction recovery copies are under `/Users/lucasqueiroz/.local/share/skill-audit/2026-09-12-before`. Removed skill packages and archived impeccable packages are under `/Users/lucasqueiroz/.local/share/skill-audit/2026-09-12-removed`, grouped by host. Preserve both impeccable packages when restoring; they have host-specific contents. Archived relative links may need their original root layout when restored.

The agent-browser description is a local skills.sh customization. Upstream updates can replace it. The companion agent-browser-customization.patch records the selected description; review an upstream update before reapplying it.

The retrieval skill is now user-owned. Its ai-memory managed marker was removed so the documented installer behavior preserves it unless forced. The other five ai-memory skills remain managed. An installer can report the skipped user-owned file as an actionable error; review upstream retrieval changes before choosing to replace this customization.

Elixir's original hobbi skill was left intact. The global Claude link now targets the stable Agents copy.

## Sensitive output incident

An early shell-configuration inspection printed existing values for NODE_AUTH_TOKEN, GITHUB_PAT_ENERFLO, GITHUB_PERSONAL_ACCESS_TOKEN, and DEXCARE_TOKEN in task tool output. No values are included in these reports or the new routing files. Rotate any of those tokens that remain active. No tokens were revoked or rotated by this task.
