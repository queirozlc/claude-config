# Decisions for all audited skills

Snapshot: 12 September 2026, 00:54:15, America/Sao_Paulo.

These are proposed changes. No installed skill was changed. Read the main audit for evidence, priority, and limitations. Compare the inventory SHA-256 with the live file before implementation.

Each entry includes the proposed disposition and a shorter description. The descriptions are drafts, not measured improvements. Confirm selection behavior on the acceptance cases in the main audit. Preserve explicit invocation settings where intentional. Frontmatter support depends on the host.

Locations: Agents means `/Users/lucasqueiroz/.agents/skills`. Claude means `/Users/lucasqueiroz/.claude/skills`. Most Claude entries link to Agents. Exact paths and link targets are in `skill-inventory.json`. Root word counts describe file size, not automatic context usage.

## agent-browser

Location: Agents (483 words); Claude (483 words, linked).

Decision: Keep; narrow description.

Keep the installed CLI as the source of version-matched instructions. Move service examples out of the description. Remove the universal preference over more direct connectors.

Proposed description:

> Automate browser and supported Electron interfaces with agent-browser. Use for website interaction, extraction, and browser testing.

## ai-memory-durable-pages

Location: Agents (803 words); Claude (803 words, linked).

Decision: Keep.

Preserve explicit mutation scope, project identity, and ownership checks. Move advanced page examples into references.

Proposed description:

> Create, update, or delete ai-memory wiki pages when the user requests a durable knowledge change. Routine session capture is outside this scope.

## ai-memory-handoff

Location: Agents (578 words); Claude (578 words, linked).

Decision: Keep.

Preserve session continuity and pending-handoff handling. Distinguish this from a portable handoff document and Orca task transfer.

Proposed description:

> Save, find, resume, or discard ai-memory session handoffs for continuity between sessions or agents.

## ai-memory-learning-maintenance

Location: Agents (678 words); Claude (678 words, linked).

Decision: Keep; reduce root.

Keep maintenance as a separate operation. Load the selected maintenance procedure instead of all procedures.

Proposed description:

> Maintain ai-memory knowledge: consolidate observations, review lessons, find contradictions, audit pages, or prune stale content.

## ai-memory-retrieval

Location: Agents (1,078 words); Claude (1,078 words, linked).

Decision: Keep; narrow body scope.

Remove the general prerequisite for nearly all non-trivial tasks unless a standing user rule requires it. Preserve read-only access and untrusted-data handling.

Proposed description:

> Retrieve prior project context, decisions, rules, or activity from ai-memory when the task depends on stored knowledge.

## ai-memory-routing-install

Location: Agents (434 words); Claude (434 words, linked).

Decision: Keep.

Preserve managed markers, ownership boundaries, and host selection. This has a specific operational scope.

Proposed description:

> Install, inspect, repair, refresh, or remove ai-memory routing in agent instruction files and skill directories.

## ai-memory-usage

Location: Agents (772 words); Claude (772 words, linked).

Decision: Keep; clarify boundary.

Use this for operation and diagnosis. Route page changes and retrieval to the dedicated skills.

Proposed description:

> Configure or troubleshoot ai-memory capture hooks, MCP access, storage, upgrades, and integration across agent hosts.

## argocd-cli-guide

Location: Agents (765 words); Claude (765 words, linked).

Decision: Correct scope before reuse.

Remove unconditional full promotion and image-only safety assumptions. Preserve context and diff checks. See audit finding 11.

Proposed description:

> Inspect, sync, or troubleshoot ArgoCD applications through the argocd CLI within the requested environment and rollout stage.

## babysit

Location: Agents (474 words); Claude (474 words, linked).

Decision: Keep.

Preserve review pagination, current-head verification, actionable feedback handling, and completion conditions. Adapt waiting to the host's available mechanism.

Proposed description:

> Monitor a pull request when asked to babysit it. Resolve actionable review and CI issues until the agreed readiness condition is met.

## brandkit

Location: Agents (2,600 words); Claude (2,600 words, linked).

Decision: Keep; split references.

Retain brand inputs and one useful initial board. Move visual modes and long aesthetic catalogs into selected references.

Proposed description:

> Create brand-guideline boards and identity presentations when the user requests a brand kit or visual identity system.

## caveman-commit

Location: Agents (358 words); Claude (358 words, linked).

Decision: Explicit use only.

Allow repository commit conventions to take priority. Do not impose Conventional Commits on every project.

Proposed description:

> Use the Caveman commit format when explicitly requested, subject to the repository's commit requirements.

## caveman-help

Location: Agents (309 words); Claude (309 words, linked).

Decision: Keep explicit scope.

A help command is narrow. Keep it separate from activation of persistent writing modes.

Proposed description:

> Explain available Caveman commands and modes when the user asks for Caveman help.

## caveman-review

Location: Agents (412 words); Claude (412 words, linked).

Decision: Explicit use only.

Remove automatic selection for any diff review. Preserve the evidence needed to understand a defect.

Proposed description:

> Use the compressed Caveman review format when explicitly requested for a code review.

## computer-use

Location: Agents (283 words); Claude (283 words, linked).

Decision: Keep.

Keep this as a tool guide router. Verify that the selected host provides the required runtime before following host-specific commands.

Proposed description:

> Operate supported desktop interfaces through the computer-use runtime when the task requires desktop interaction.

## context7-mcp

Location: Claude (313 words).

Decision: Narrow selection; add fallback.

Do not query for every library mention. State what to do when Context7 is unavailable or lacks the requested version.

Proposed description:

> Find current or version-specific library documentation through Context7 when local sources do not answer the API question.

## design-taste-frontend

Location: Agents (12,853 words); Claude (12,853 words, linked).

Decision: Reduce substantially; explicit art direction.

Move the large pattern catalog out of the root. Remove mandatory image generation, dual themes, repeated confirmations, and fixed layout metrics from general work.

Proposed description:

> Design marketing pages with deliberate art direction when requested. Preserve the existing design system during changes to an established site.

## dexcare-aws

Location: Agents (792 words); Claude (792 words).

Decision: Narrow selection; correct privilege wording.

Select only for DexCare context. Use the least privilege that supports the task. Two identical root copies can share a source if host requirements match.

Proposed description:

> Access DexCare AWS accounts and environments through the configured toolbox and AWS CLI profiles.

## dhh-rails-style

Location: Claude (889 words).

Decision: Keep as a selected style.

Do not turn every Rails question into a style migration. Remove the mandatory intake menu when the request is clear. Read only relevant references.

Proposed description:

> Apply DHH and 37signals Rails conventions when requested or when the repository already uses them.

## elixir

Location: Claude (997 words, linked).

Decision: Narrow selection; clarify ownership.

Qualify migrations and N+1 queries with Elixir or Ecto. Avoid repeating full gates after every edit. The global link depends on the hobbi checkout.

Proposed description:

> Develop or review Elixir, Phoenix, and Ecto code. Use repository conventions and checks appropriate to the change.

## elysiajs

Location: Agents (1,830 words); Claude (1,830 words, linked).

Decision: Keep; split examples.

Keep framework-specific knowledge. Move long examples into references. Do not make classes or abstract classes a default requirement.

Proposed description:

> Build or modify ElysiaJS services using the installed framework version and existing application structure.

## find-me-a-job

Location: Agents (1,008 words); Claude (1,008 words, linked).

Decision: Keep.

Preserve candidate evidence and user submission. Declare how the Maestri skill dependency is provided and how to proceed if it is unavailable.

Proposed description:

> Run the Maestri job search or prepare an application package for a selected posting. The user submits applications.

## full-output-enforcement

Location: Agents (412 words); Claude (412 words, linked).

Decision: Retire automatic selection.

Keep completion in global policy. Save large deliverables as files instead of forcing a manual continue loop.

Proposed description:

> Provide complete inline file contents when the user explicitly requests unabridged code output.

## gpt-taste

Location: Agents (1,134 words); Claude (1,134 words, linked).

Decision: Retire automatic selection; correct first.

Remove simulated execution. Preserve useful GSAP examples as optional references. Do not require animation or AIDA for every interface.

Proposed description:

> Create GSAP motion treatments when explicitly requested for a suitable interface.

## grill-me

Location: Agents (22 words); Claude (22 words, linked).

Decision: Repair dependency declaration.

The alias is short, but its target was not found in the searched roots. Declare its provider and an available-host fallback.

Proposed description:

> Run the grilling interview when explicitly invoked and the grilling skill is available.

## grill-with-docs

Location: Agents (35 words); Claude (35 words, linked).

Decision: Repair dependency declaration.

Both target skills need a declared provider. Do not assume a Claude Skill tool exists in every host.

Proposed description:

> Run the requested grilling and domain-modeling interview when both target skills are available.

## growth-advisor

Location: Agents (2,535 words); Claude (2,535 words, linked).

Decision: Restrict to explicit advice.

Remove ordinary implementation requests from selection. Remove the claim that the protocol overrides user intent. Keep strict interviewing as an explicit mode.

Proposed description:

> Evaluate product ideas, feature value, positioning, or growth strategy when the user asks for validation or business advice.

## handoff

Location: Claude (119 words).

Decision: Keep; distinguish output type.

This small skill has a useful document purpose. Do not select it for ai-memory operations or Orca transfer by default.

Proposed description:

> Create a portable handoff document when the user requests written context for the next agent or session.

## high-end-visual-design

Location: Agents (1,456 words); Claude (1,456 words, linked).

Decision: Explicit style only.

Treat font, radius, nesting, and button rules as style choices. Correct conflicts with accessibility, performance, and existing design tokens.

Proposed description:

> Apply the high-end visual style when explicitly selected in the design brief.

## image-to-code

Location: Agents (5,815 words); Claude (5,815 words, linked).

Decision: Narrow selection; remove repeated generation.

Preserve supplied references. Generate only to resolve named design needs. Define acceptance conditions and move examples into references.

Proposed description:

> Implement an interface from a design image, or create a design image first when the user requests that workflow.

## impeccable

Location: Agents (1,461 words); Claude (1,489 words).

Decision: Keep as proposed general frontend workflow.

Preserve separate host packages. Read relevant references only. Limit optional polish, but continue through confirmed defects in scope.

Proposed description:

> Design or improve frontend interfaces, including usability, accessibility, performance, and visual consistency with the project.

## industrial-brutalist-ui

Location: Agents (1,075 words); Claude (1,075 words, linked).

Decision: Explicit style only.

Keep its coherent aesthetic as an option. Do not let it override the existing design system on unrelated frontend changes.

Proposed description:

> Apply the industrial brutalist visual style when selected by the user or project brief.

## kubectl-skill

Location: Agents (907 words); Claude (907 words, linked).

Decision: Repair references; narrow selection.

Restore or remove the missing reference and scripts links. Select for Kubernetes, not generic containers. Preserve cluster context verification.

Proposed description:

> Inspect, deploy, or troubleshoot Kubernetes resources through kubectl within the requested cluster and namespace.

## make-interfaces-feel-better

Location: Agents (1,865 words); Claude (1,865 words, linked).

Decision: Keep for focused review; reduce repetition.

Preserve specific interaction guidance. Remove duplicated principles and arbitrary report caps. Apply motion measurements only when relevant.

Proposed description:

> Review or refine interface details such as typography, spacing, controls, and motion when a focused interface improvement is requested.

## minimalist-ui

Location: Agents (1,089 words); Claude (1,089 words, linked).

Decision: Explicit style only; resolve contradiction.

Choose whether gradients are allowed in this style. Keep its token choices separate from other aesthetic packages.

Proposed description:

> Apply the minimalist editorial visual style when selected by the user or project brief.

## modern-css

Location: Claude (1,900 words).

Decision: Correct examples; split references.

Fix calc-size syntax. Date support claims and distinguish experimental features. Keep target-browser verification.

Proposed description:

> Use or evaluate modern CSS features for the target browsers, or refactor CSS when the requested change benefits from them.

## node

Location: Agents (766 words); Claude (766 words, linked).

Decision: Keep; reduce universal prescriptions.

Keep the topic router. Use native TypeScript, caching, or async generators only where the runtime and task justify them. Preserve explicit invocation settings if intentional.

Proposed description:

> Develop or troubleshoot Node.js and TypeScript runtime behavior using the project's supported Node version.

## nodejs-core

Location: Agents (1,413 words); Claude (1,413 words, linked).

Decision: Keep specialist knowledge; scope gates.

Preserve stale-build warnings and contribution conventions. Load detailed build and commit procedures only for the matching task.

Proposed description:

> Contribute to Node.js core or diagnose native addon, V8, node-gyp, N-API, and libuv problems.

## orca-cli

Location: Agents (339 words); Claude (339 words, linked).

Decision: Keep; narrow selection.

Use explicit Orca context. Verify the configured executable because it did not resolve on this shell PATH. Avoid overlap with memory and document handoffs.

Proposed description:

> Operate Orca agents, tasks, and worktrees when the user requests an Orca workflow.

## orchestration

Location: Agents (563 words); Claude (563 words, linked).

Decision: Keep as Orca supervision mode.

Distinguish supervised coordination from general agent work and ordinary Orca commands. Preserve the wrong-binary guard.

Proposed description:

> Coordinate a supervised Orca workflow with tracked tasks, messages, and results when that workflow is requested.

## prosemirror

Location: Claude (1,479 words).

Decision: Keep; split long API examples.

The manual specialist scope is useful. Move API examples to references and verify them against the installed version before use.

Proposed description:

> Implement or troubleshoot ProseMirror schemas, transactions, plugins, selections, and editor behavior.

## react-doctor

Location: Claude (308 words).

Decision: Narrow selection; make scan scope explicit.

Do not fetch and run the latest scanner after every small React edit by default. Preserve a required repository scan when configured.

Proposed description:

> Run React Doctor diagnostics when requested or required by the repository, then resolve findings within the agreed scope.

## redesign-existing-projects

Location: Agents (2,210 words); Claude (2,210 words, linked).

Decision: Keep for redesign requests; remove invented content.

Preserve real product facts. Remove instructions to invent organic statistics or dates. Test affected behavior instead of every intermediate edit.

Proposed description:

> Audit and redesign an existing interface when requested while preserving its functionality, content accuracy, and project constraints.

## revenue-centric-design

Location: Agents (753 words); Claude (753 words, linked).

Decision: Keep for product advice.

Use the final shared version. Keep licensing and domain exclusions. Do not apply an obsolete duplicate-copy or mandatory-friction finding.

Proposed description:

> Advise on SaaS conversion, pricing, retention, growth, and product UX when requested. Excludes gambling, betting, and casinos.

## scrooge

Location: Agents (914 words); Claude (914 words, linked).

Decision: Explicit use only.

Do not select from generic brevity requests. Keep ASD-STE100 as the default. Audit persistent hooks separately before changing them.

Proposed description:

> Use Scrooge mode only when the user explicitly activates or configures it.

## shadcn

Location: Agents (2,430 words); Claude (2,430 words, linked).

Decision: Keep; reduce root and repeated intake.

Inspect local components first. Read only relevant documentation. Reuse known registry choices. Preserve confirmation for actual overwrite risk when authorization is absent.

Proposed description:

> Build or modify shadcn/ui components using the project's installed components, registry, and version.

## ship

Location: Agents (557 words); Claude (557 words, linked).

Decision: Keep workflow; fix authentication conflict.

Preserve the explicit per-PR merge boundary and simple-ticket path. Replace global account switching with project authentication policy. Declare external skill dependencies.

Proposed description:

> Run the Maestri ticket cycle when the user invokes ship or requests that cycle. Continue to the explicit per-PR merge boundary.

## spec-project

Location: Claude (655 words).

Decision: Repair dependencies; explicit planning scope.

The required sibling references are missing. Provide the ticket contract locally or restore the package. Do not convert every rough idea into ticket planning.

Proposed description:

> Create a project ticket specification when the user requests structured project planning or ticket decomposition.

## tailwindcss-performance

Location: Agents (1,107 words); Claude (1,107 words, linked).

Decision: Correct reference; keep focused scope.

Correct static versus inline. Use measured build or CSS issues to select optimizations. Avoid applying version-specific configuration to another version.

Proposed description:

> Diagnose and improve Tailwind CSS build time, generated CSS size, or content detection for the installed version.

## taste

Location: Claude (766 words).

Decision: Keep named system; remove routine stops.

Convert supplied colors deterministically. Reuse an adequate brief. Preserve its token system when selected. Continue through functional defects.

Proposed description:

> Build or refine an interface with the taste SaaS design system when that system is explicitly selected.

## typescript-magician

Location: Agents (562 words); Claude (562 words, linked).

Decision: Correct guard; narrow required procedure.

Validate actual property types and HTTP status. Do not run compiler workflows for explanations. Keep type changes within the requested scope.

Proposed description:

> Design or troubleshoot advanced TypeScript types, generic inference, type guards, and compiler type errors.

## vpn

Location: Claude (326 words).

Decision: Keep; narrow automatic diagnosis.

A generic timeout does not establish a VPN failure. Check the known VPN-dependent destination and configured connection before taking action.

Proposed description:

> Manage the configured macOS VPN when requested, or diagnose connectivity to a known VPN-dependent destination.

## Implementation boundary

Start with the factual errors and action-scope conflicts identified in the main audit. Then change descriptions in small groups. Recheck skill selection before moving large bodies into references. Keep useful examples and host adapters. Do not merge packages solely because they have the same name.
