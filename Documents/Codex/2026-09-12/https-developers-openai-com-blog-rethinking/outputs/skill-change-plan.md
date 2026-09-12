# Skill change plan

Status: applied on 12 September 2026. See applied-changes.md for verification, recovery locations, and limitations.

## Selected decisions

| Skill or policy | User decision |
|---|---|
| gpt-taste | Keep optional GSAP guidance. Remove simulated execution and forced layouts. |
| typescript-magician | Remove the skill. This replaces the earlier decision to correct the example. Use compiler output, local types, and documentation. |
| growth-advisor | Select only for explicit validation or business advice. |
| argocd-cli-guide | Sync and promote only within the requested rollout scope. |
| dexcare-aws | Keep the highest-privilege role as the default. This differs from the audit recommendation. Select only for DexCare accounts, roles, or environments. Check supporting files, then use one canonical copy with links. |
| GitHub authentication and ship | Use separate GH_CONFIG_DIR directories per company. Configure terminal and agent environments. Resolve the existing Enerflo per-command-token rule as part of this change. Verify Git authentication separately. Use the directory/account mapping below. |
| kubectl-skill | Remove the skill. |
| spec-project | Remove the skill. |
| impeccable | Archive outside active skill directories. Preserve both host-specific packages. Do not delete the archived content. |
| make-interfaces-feel-better | Explicit user activation only. The model must not select or read it automatically. Verify enforcement for each host, including the Codex copy. Remove repetition and make review steps appropriate to the requested change. |
| high-end-visual-design | Remove the skill. |
| minimalist-ui | Remove the skill. |
| industrial-brutalist-ui | Remove the skill. |
| design-taste-frontend | Remove the skill. |
| image-to-code | Remove the skill. |
| taste | User is creating new guidelines in the Claude skill. Leave this work untouched. Do not apply findings from the old version without a new review. |
| revenue-centric-design | Retain for marketing-oriented UX. The current version was reread during the interview. Require its usability review for new or materially changed flows, not minor edits. Preserve source attribution and reuse conditions. |
| full-output-enforcement | Remove the skill. Keep completion requirements in global instructions. |
| brandkit | Keep the content unchanged. Require explicit user activation. |
| react-doctor | Run only when requested or required by the repository. |
| redesign-existing-projects | Remove the skill. Use the user's new taste guidelines. |
| modern-css | Keep the skill. Correct examples and organize references. |
| tailwindcss-performance | Remove the skill. Use current Tailwind documentation when needed. |
| context7-mcp | Leave unchanged. Record the selection concern only. Installer ownership was not established. |
| vpn | DexCare-only. Use for explicit requests or DexCare resources known to require VPN. Do not trigger on unrelated network failures. |
| elixir | Keep globally. Narrow selection and validation checks. Move ownership from the hobbi checkout to a stable shared location. |
| node | Keep as an explicitly activated specialist skill for application async and performance decisions. Reduce unrelated procedures. |
| nodejs-core | Keep as an explicitly activated specialist skill for Node runtime, libuv, V8, native addons, and core work. Reduce unrelated procedures. Preserve relevant technical checks. |
| dhh-rails-style | Keep active for all of the user's Rails projects. Keep its current workflow unchanged, including intake and reference procedures. |
| elysiajs | Remove the skill. Use current framework documentation when needed. |
| agent-browser | Shorten the description and remove universal priority over other web tools. User identifies skills.sh as its source. Record the customization and its update risk; do not assume upstream updates preserve it. |
| prosemirror | Remove the skill. Use current framework documentation when needed. |
| ship testing across roles | Apply the user's Ponytail intent to executors, testers, and reviewers. Add or run tests only when necessary for the changed behavior or a concrete risk. Prefer meaningful coverage over test count. Reuse existing coverage; do not add implementation-mirroring or redundant tests. Preserve required repository checks. The user did not explicitly remove mandatory reviewer roles. |
| Global CodeGraph policy | Create an index when repository navigation needs CodeGraph. Align both hosts. |
| Global file editing policy | Use each host's native editing tools. Claude uses available native file tools. Codex uses apply_patch. Do not substitute Python scripts or shell heredocs for edits. Shell reads remain appropriate for Codex. Do not claim local instructions outrank host instructions. |
| ai-memory-retrieval | Look up memory when the task depends on prior context or a standing rule. Apply through the managed source where appropriate. |
| ai-memory-durable-pages | Keep unchanged, including durable mutation boundaries. |
| ai-memory-handoff | Keep unchanged, including session continuity boundaries. |
| ai-memory-learning-maintenance | Keep unchanged as a managed operational skill. |
| ai-memory-routing-install | Keep unchanged as a managed operational skill. |
| ai-memory-usage | Keep unchanged as a managed operational skill. |
| babysit | Keep unchanged. Its existing practical polling interval does not need a separate host-specific rewrite. |
| find-me-a-job | Keep candidate evidence and user submission rules. Clarify the Maestri dependency and fallback. |
| handoff | Remove the file handoff skill. Use ai-memory-handoff for continuity. |
| grill-me | Remove the alias. |

## Already removed before this interview

The live check found these audited skills absent from both requested roots: caveman-commit, caveman-help, caveman-review, computer-use, grill-with-docs, orca-cli, orchestration, scrooge, and shadcn.

Correction: the earlier progress message said 10 removed skills. The check listed nine. The audit had 51 names, leaving 42 present at that check.

## Implementation conditions

### GitHub account mapping

The user supplied these directory rules. Each rule applies to the directory and its descendants. Match directory boundaries, not arbitrary text prefixes. All other directories use the Personal account.

| Directory | Account |
|---|---|
| /Users/lucasqueiroz/Development/ravn | lucasepulchro |
| /Users/lucasqueiroz/dexcare | lucas-queiroz04 |
| /Users/lucasqueiroz/Development/local | lucasqlgtm |
| All other directories, Personal | queirozlc |

These rules replace earlier assumed company/account mappings for the planned authentication setup. Choose separate configuration directories during implementation. Ensure terminal and agent commands receive the selected GH_CONFIG_DIR. Verify how worktrees outside these directory trees should behave before adding any exception to the Personal fallback.

P1, P2, and remaining per-skill decisions are complete. Implementation is complete. The user corrected the DexCare account to the saved lucas-queiroz04 account during implementation.

- Recheck live files before edits. The setup changed during the audit and interview.
- Keep the user's new taste work untouched. The old taste findings do not authorize edits to its replacement.
- Archive impeccable outside discovered skill roots. Preserve both host packages and supporting files.
- Implement explicit activation through controls the actual host supports. Do not assume a frontmatter field prevents automatic reading on every host.
- Apply managed-source changes through their owner where appropriate. Record the agent-browser customization because skills.sh updates can replace it. Leave Context7 unchanged.
- Use the supplied directory/account mapping. Inspect terminal and agent launch configuration before implementing authentication isolation. Verify Git transport separately. Do not copy credentials into reports or project files.
- Preserve ASD-STE100, repository i18n rules, source reuse conditions, user submission of applications, memory ownership controls, and the explicit per-PR merge boundary.
- Preserve required validation while removing redundant test creation. Use the audit's representative behavior cases to verify selection, unnecessary questions, tool use, and completion. Do not claim performance gains without measurement.

## Order of work

1. Remove the selected skills and archive impeccable with recoverable contents.
2. Correct retained P1 scope rules in gpt-taste, growth-advisor, and argocd-cli-guide.
3. Configure company-specific GitHub authentication after the remaining environment mapping is known.
4. Apply the selected activation, reference, and workflow changes to retained skills.
5. Align global CodeGraph and native-editing preferences. Preserve intentional user choices that differ from the audit.
6. Verify links, managed-source behavior, activation controls, and representative tasks.
