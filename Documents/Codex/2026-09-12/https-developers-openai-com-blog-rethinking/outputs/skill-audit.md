# Skill audit for GPT-6 Astra

Audit date: 12 September 2026. Inventory snapshot: 00:54:15, America/Sao_Paulo.

Your setup needs clearer selection rules and fewer conflicting instructions. Keep the operational knowledge. Reduce the instructions that force a method, add work, or stop an authorized task.

The highest priority changes are to remove simulated execution, correct unsafe examples, narrow business-advice triggers, and make visual styles explicit choices. File length alone is not a sufficient reason to remove a skill.

## Basis and coverage

OpenAI recommends short descriptions with precise selection conditions, supporting files that load only when needed, and fewer fixed procedures. It also recommends reviewing repeated preparation and testing requirements. Completion conditions should state how far the agent must continue. Approval rules should identify the actual action boundary. Shared skills must also work for the other models that use them. These are the audit criteria, not a claim that shorter instructions always perform better. [OpenAI guide](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

I inspected the skill roots, resolved symbolic links, read the root instructions, and checked local reference links. I also read selected supporting files for the findings below. I parsed the frontmatter with Ruby YAML and recorded SHA-256 values. The inventory covers both requested global directories. It includes the Elixir skill reached through a link to a project directory. It does not cover every project-local skill on the computer or all installed plugin packages.

This is a static instruction audit. I did not run deployment, memory mutation, job-hunt, browser, or orchestration workflows. I did not inspect every supporting document or execute bundled scripts. I ran one isolated check of the TypeScript guard and verified two reference errors against current documentation. No skill, global instruction, or application setting was changed by this audit.

The directories changed while I read them. The final inventory is a fixed snapshot, not a guarantee that the live files remain unchanged. Changes observed during inspection included new tool and writing skills, a longer browser description, updated interview aliases, and replacement of the separate revenue-centric-design copy with a link. I have assessed these later versions where observed. The temporary orca-linear entry disappeared before the snapshot and is excluded.

| Measure | Snapshot result |
|---|---:|
| Entries in `.agents/skills` | 41 |
| Entries in `.claude/skills` | 51 |
| Claude entries that are symbolic links | 40 |
| Skill names across both roots | 51 |
| Distinct resolved `SKILL.md` paths | 53 |
| Words across distinct root files | 65,963 |
| Bytes across distinct root files | 468,784 |
| Description characters in the Agents root | 11,570 |
| Description characters in the Claude root | 15,253 |
| Frontmatter parse errors | 0 |

These are file measurements, not model token measurements. The full 65,963 words are not automatically loaded into each task. Description cost and loaded-body cost are separate. A symbolic link is not evidence that a host loads the same body twice. I did not measure host deduplication, selection accuracy, latency, or billing.

The companion inventory contains every path, description, line count, word count, link target, and SHA-256 value. The companion skill decisions file gives an action and a proposed description for every skill name.

## Priority findings

### 1. Remove simulated tool execution from gpt-taste

Evidence: `/Users/lucasqueiroz/.agents/skills/gpt-taste/SKILL.md:14` requires simulated Python execution. Lines 15-20 force the result of that simulation. Line 69 requires mock output under an execution label.

This makes invented execution part of the workflow. The same file forces AIDA on every page and prohibits static interfaces at line 47. A settings form can acquire a marketing layout and a GSAP dependency through this skill.

Action: retire this skill from automatic selection. Preserve useful motion examples in an optional GSAP reference. If you retain a variation mode, choose from the brief. Run a real generator only when random selection is requested. Never describe a simulated result as executed.

Priority: P1. This is a truthfulness and scope problem, not a formatting preference.

### 2. Correct the TypeScript validation example

Evidence: `/Users/lucasqueiroz/.agents/skills/typescript-magician/SKILL.md:74` checks only whether `id` and `name` exist. It claims a `User` with a numeric ID and string name.

The isolated check returned `true` for `{id: 'wrong', name: 42}`. The example teaches an invalid trust-boundary check. Correct it to validate both field types. Also check the HTTP response before treating its body as successful data.

Lines 19-23 prescribe two compiler runs for every invocation. Lines 34-39 require type theory and comprehensive type tests for every challenge. Apply compiler checks to code changes. Answer conceptual questions directly. Limit removal of `any` to the requested scope.

Priority: P1 for the example. P2 for workflow scope.

### 3. Restrict growth-advisor to evaluation requests

Evidence: `/Users/lucasqueiroz/.agents/skills/growth-advisor/SKILL.md:3` includes ordinary feature requests. Lines 99-110 prohibit code, copy, pages, and plans until a decision passes. The live-product protocol requires six business metrics and blocks when they are absent.

This can turn an implementation request into a product-validation interview. The protocol even states that this block takes priority over the user's request. That is unsuitable for an automatically selected skill.

Action: keep the evidence framework for explicit validation and growth advice. Exclude implementation of an already selected feature. In advice mode, explain missing evidence and propose a test. Preserve a deliberate strict interview mode if you still want it. Do not require the word `override` to carry out a clear implementation request.

Priority: P1 for unintended task blocking.

### 4. Separate visual styles from the general frontend workflow

Evidence comes from the root files for gpt-taste, high-end-visual-design, minimalist-ui, industrial-brutalist-ui, design-taste-frontend, image-to-code, impeccable, and make-interfaces-feel-better.

| Decision | One instruction | Conflicting instruction |
|---|---|---|
| Card shape | high-end requires nested enclosures and large radii | industrial requires square corners; image-to-code rejects nested boxes |
| Buttons | high-end requires pills | minimalist prohibits pill primary buttons |
| Type | high-end prohibits Inter and Roboto | industrial recommends both |
| Motion | gpt-taste prohibits static interfaces | make-interfaces-feel-better prohibits custom motion on frequent interactions |
| Color | minimalist prohibits gradients | its own lines 67 and 74 suggest gradients |
| Theme | design-taste requires both color modes | industrial requires one substrate palette |
| Transitions | high-end suggests `transition-all` | make-interfaces-feel-better prohibits it |
| Composition | shadcn requires full Card composition | image-to-code pushes away from nested containers |

Some of these rules can be valid within a specific design brief. They become defects when several skills claim the same task.

Action: select one general frontend workflow. Use style references only when the user or project brief selects them. Keep component-library guidance for APIs and accessibility. Do not let an aesthetic replace the project's tokens, font family, or installed components during a small fix.

Suggested division: impeccable for general frontend work; make-interfaces-feel-better for explicit detail review; taste for its named SaaS token system; design-taste-frontend for explicit marketing art direction after reduction. This is my proposed organization, not a requirement from OpenAI.

Priority: P1 for scope conflicts. P2 for organization.

### 5. Reduce image-to-code generation requirements

Evidence: `/Users/lucasqueiroz/.agents/skills/image-to-code/SKILL.md` has 1,228 lines and 5,815 words. Sections 2-7, 10, 18, 28, 35-38 repeat image generation and regeneration requirements. It defaults to one image per section, requires fresh generation instead of closer inspection, and permits more images whenever they might improve clarity.

These instructions add a generation step to nearly every visual task. They have no practical completion limit. A new image can also change the detail that the agent is trying to inspect.

Action: select this skill only for a requested design-image workflow or implementation from an image reference. Preserve supplied references. Create additional views only for a named unresolved design decision. State the required screens and acceptance conditions before generation. Keep the verification of the implemented result against the reference.

Priority: P2. Potential latency and cost impact is inferred, not measured.

### 6. Remove routine approval requests from taste

Evidence: `/Users/lucasqueiroz/.claude/skills/taste/SKILL.md:18` stops on hex, RGB, or HSL input. Lines 22-28 require a brief and another confirmation before work. The conversion restriction repeats in `references/color.md`.

The no-guessing rule is useful. Requiring the user to perform a deterministic color conversion is unnecessary. Asking for a brief again is also unnecessary when the request already contains one.

Action: use an available deterministic conversion method. Reuse the supplied brief. Ask only for a missing choice that materially changes the result. Keep the closed token vocabulary when this specific design system is requested.

Line 85 also limits corrections to one pass. Keep a limit on optional polishing. Continue through confirmed functional or accessibility defects in scope.

Priority: P2.

### 7. Make descriptions precise before reducing body size

Examples of broad selection include these files:

| Skill | Current selection problem | Required boundary |
|---|---|---|
| dexcare-aws | Generic AWS requests and words such as `dev` and `staging` | A DexCare account, role, or environment |
| context7-mcp | Any library mention | A need for current or version-specific API documentation |
| react-doctor | Finishing any feature or fixing any bug | React diagnostics or an established React validation workflow |
| kubectl-skill | Containers and deployments in general | Kubernetes operations through kubectl |
| elixir | Also includes unqualified migration and N+1 requests | Elixir, Phoenix, or Ecto context |
| caveman-review | Any PR or diff review | An explicit request for its compressed review format |
| scrooge | Generic requests to be terse | Explicit Scrooge activation |
| spec-project | A rough idea with intent to build | A request to create a ticket specification |
| orca-cli | Generic handoff and worktree phrases | Orca state or an explicit Orca operation |

The final browser description is 925 characters. The root file is a useful CLI router, but its description includes many examples and a universal preference over other web tools. Retain browser interaction as the selection condition. Keep Slack and cloud details in the selected guide.

Priority: P2. The companion decisions file contains proposed replacement descriptions for all 51 names.

### 8. Move reference material out of large root files

| Skill | Lines | Words | Recommended root content |
|---|---:|---:|---|
| design-taste-frontend | 1,206 | 12,853 | Scope, brief interpretation, preservation rules, reference table |
| image-to-code | 1,228 | 5,815 | Reference selection, unresolved details, implementation acceptance |
| brandkit | 798 | 2,600 | Deliverable, brand inputs, one board default, reference table |
| growth-advisor | 259 | 2,535 | Explicit advice scope, evidence source, protocol selection |
| shadcn | 277 | 2,430 | Project discovery, local components, selected API reference |
| redesign-existing-projects | 178 | 2,210 | Requested scope and preservation rules |
| modern-css | 756 | 1,900 | Feature selection and browser-support policy |

Keep the useful material in supporting files. Do not load the whole pattern catalog to fix one component. Remove repetition before moving it. Splitting repeated text into more files does not improve its quality.

A useful trial target is 200-500 words for a multi-workflow root. This is an audit proposal, not a platform limit. Single-purpose references can be longer when each part is required.

Priority: P2.

### 9. Repair missing dependencies and distinguish them from unavailable tools

Confirmed missing local paths:

- `/Users/lucasqueiroz/.agents/skills/kubectl-skill/references/REFERENCE.md`
- `/Users/lucasqueiroz/.agents/skills/kubectl-skill/scripts/`
- `/Users/lucasqueiroz/.claude/skills/orchestrate-project/references/project-config.md`
- `/Users/lucasqueiroz/.claude/skills/orchestrate-project/references/ticket-spec.md`

The first two are linked from kubectl-skill lines 191-192. The second pair is required by spec-project lines 28 and 59. Restore the required source or remove the reference and provide the necessary contract locally.

The interview aliases now call a `Skill` tool for `grilling` and `domain-modeling`. Those target skills were not found in the three local roots searched. spec-project also names ui-ux-pro-max and orchestrate-project. ship and find-me-a-job name maestri. Their absence from these roots does not prove they are unavailable through every plugin or host. Declare the provider and fallback for each dependency. The Maestri CLI itself was present.

The `orca` executable did not resolve on this shell PATH. Other runtime mechanisms can still provide it. Do not label the installation broken without checking the configured executable in its actual host.

Priority: P1 for required missing files. P2 for dependency declarations.

### 10. Correct two technical reference errors

`/Users/lucasqueiroz/.agents/skills/tailwindcss-performance/SKILL.md:205` says `theme(static)` inlines values instead of using CSS variables. Current Tailwind documentation says the static option generates all theme variables. The inline option controls value inlining. Correct the distinction before reusing this example. [Tailwind theme documentation](https://tailwindcss.com/docs/theme)

`/Users/lucasqueiroz/.claude/skills/modern-css/SKILL.md:253` uses `calc-size(auto)` with one argument. The documented function requires a basis and a calculation, such as `calc-size(auto, size)`. For simple intrinsic-size animation, the documentation prefers `interpolate-size`. Correct the example and check support for the target browsers. [MDN calc-size documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/calc-size)

The modern-css file mixes stable features, proposed features, and undated availability labels. Retain its support-checking instructions. Move examples into topic files with a verification date. I did not validate every CSS, Node, ProseMirror, or Elysia example in the library.

Priority: P2.

### 11. Keep deployment boundaries precise

Evidence: `/Users/lucasqueiroz/.agents/skills/argocd-cli-guide/SKILL.md:134` requires `promote-full` after an Argo Rollouts sync. Lines 87 and 146 treat image-only changes as safe to sync.

A generic skill cannot establish the deployment policy for every application. An image-only change can still be a material release. A synchronization request does not by itself establish that every promotion step is intended.

Action: preserve context verification and diff inspection. State the authorized environment and rollout stage. Continue within that scope. Promote only when the requested rollout and project policy require it. Preserve explicit restrictions on force and prune.

The DexCare skill already has useful same-scope authorization reuse at lines 101-103. Keep it. Replace line 60's highest-privilege wording with the least privilege that supports the task.

Priority: P1 for deployment scope.

### 12. Remove broad testing repetition without removing real checks

Examples:

- redesign-existing-projects line 174 says to test after every change.
- Elixir lines 104-120 require a broad loop after any edit and a second full gate before commit.
- TypeScript requires compiler runs even for conceptual questions.
- React Doctor requires a latest-version scan after every React change.
- ship's cycle reference requires regression tests for everything and always dispatches Static and Security reviewers.

Action: retain each repository's actual required checks. For iterative work, rerun affected checks after relevant changes. Broaden the run when the change, a failure, or the project contract requires it. Do not add a new test for a prose-only edit merely because a generic skill says every change needs one.

Keep Node core's warning about testing a stale embedded build. That is specific technical knowledge. Move its detailed build and commit workflow behind the Node-core contribution condition. Inspect existing build configuration before asking the user to restate it.

Priority: P2.

### 13. Resolve global instruction drift

`/Users/lucasqueiroz/.claude/CLAUDE.md:27` says to skip CodeGraph when no index exists. `/Users/lucasqueiroz/.codex/AGENTS.md` requires index creation. This is verified cross-host drift. The current task's supplied instructions take precedence here.

Keep your CodeGraph preference. Decide whether the difference between hosts is deliberate. If automatic indexing is required, retain it explicitly. If you want a lighter policy, allow direct inspection for a known, small file and reserve index creation for repository navigation. Do not silently change this preference during cleanup.

The Claude file at line 16 claims authority over contrary host instructions and assumes Read/Write/Edit tools. Replace that claim with a preference for native file tools when available, plus an available-tool fallback.

The Codex file's file-editing sentence ends with `unless you're asked for`. Complete the sentence so the exception is clear.

The ship cycle at line 73 calls `gh auth switch`. This conflicts with your Enerflo instruction to set a token per command and preserve the default account. Add an explicit project-authentication condition to the cycle. Keep the Enerflo account, credential handling, and token non-disclosure rules.

Priority: P1 for authentication scope. P2 for the other drift.

### 14. Do not use full-output-enforcement as a general persistence policy

Evidence: `/Users/lucasqueiroz/.agents/skills/full-output-enforcement/SKILL.md:10` treats every task as production-critical. Lines 28-41 require a pause and a user `continue` response when output is long.

The useful requirement is to finish the requested deliverable. The pause protocol can stop work even when an output file would solve the response-length problem.

Action: retire automatic selection. Preserve one completion rule in global instructions: finish the requested scope, verify the result, and save large deliverables as files. Keep a manual full-file output option for requests that specifically require inline complete code.

Priority: P2.

### 15. Keep one writing policy active by default

The newly added caveman-review can select on any PR review. caveman-commit forces Conventional Commits. scrooge describes fragment-style output and persistent global activation. These can conflict with ASD-STE100 or a repository's commit format. Scrooge's generic terse trigger is broader than the named activation described for its hook.

Action: keep ASD-STE100 as the default. Make other writing modes explicit choices. Let repository commit rules take priority over a generic Conventional Commits format. Keep expanded explanations for findings that need evidence. Verify hook behavior separately before changing persistent activation; this audit did not inspect or modify hooks.

Priority: P2.

### 16. Preserve host-specific packaging

At the snapshot, dexcare-aws still exists as two identical root files. It can use one canonical copy if both hosts need the same instructions.

Impeccable has two different packages at version 4.1.1. The Agents package has additional agent TOML files and OpenAI metadata. Many differences also adapt paths and command syntax. Do not replace one package with a link to the other merely because the skill name matches. Preserve host adapters. Compare workflow policy separately from packaging.

The separate revenue-centric-design copy was replaced by a shared link during inspection. Do not apply the earlier duplicate-copy finding to that final state. Its later root has a broader description and no longer mandates the friction-auditor pass. Assess the saved SHA-256 before any follow-up edit.

The Elixir link points into the hobbi checkout. It resolved successfully. Moving or deleting that checkout could remove the global skill. If it is a personal global standard, move ownership to a stable shared location in a separate change. If it is a hobbi policy, keep it project-local.

Priority: P2.

## What to preserve

Preserve explicit user preferences and proven workflow facts. The cleanup should retain these controls:

- ASD-STE100 and repository i18n rules.
- Enerflo per-command authentication and protection of credentials.
- Existing project stack, tokens, content, routes, and behavior during scoped changes.
- Memory project identity, explicit durable writes, ownership markers, and untrusted-content handling.
- Job-application truth checks and the rule that the user submits applications.
- The explicit per-PR merge boundary in ship.
- PR review pagination, current-head verification, and completion conditions in babysit.
- CLI-provided version-matched instructions where the CLI is the real execution interface.
- Actual repository CI requirements and checks that prevent stale or invalid test results.
- Source licensing and reuse conditions when retaining third-party content.

The memory family has useful separation between retrieval, durable writes, handoff, maintenance, and installation. Keep those operation boundaries. Reduce generic trigger text and move advanced details into selected references. In particular, ai-memory-retrieval line 33 expands a read-only retrieval skill into a prerequisite for nearly all non-trivial work. Keep automatic lookup only where prior project knowledge is relevant or where an explicit standing rule requires it.

## Proposed change order

1. Correct factual and scope defects. Remove simulated execution. Fix the TypeScript guard, missing required paths, authentication conflict, and unconditional rollout promotion.
2. Narrow selection. Start with growth-advisor, gpt-taste, image-to-code, DexCare, browser, review style, and ticket planning.
3. Choose one default frontend workflow. Convert aesthetic packages into optional references or explicit modes.
4. Reduce large roots. Move required examples behind task-specific references. Remove repeated instructions and repeated approval requests.
5. Reconcile host policy. Preserve package adapters and intentional host differences. Update managed sources through their owner so an installer does not restore old text.
6. Compare behavior on the tasks below before broad rollout.

No deletion list should be applied without preserving the useful source material. An archive outside discovered skill roots is sufficient for retired personal skills. There is no need to build a new skill-management framework for this work.

## Behavior checks for the revised setup

These are proposed acceptance cases. They have not been run as model evaluations.

| Request | Expected selection and completion |
|---|---|
| Fix a typo in a React button | Inspect and edit the target. No growth interview, image generation, or design-system replacement. |
| Implement an approved SaaS settings form | Use the existing system and relevant component APIs. Complete required states and affected checks. |
| Use this hex brand color with taste | Convert deterministically. Do not require the user to supply a second color format. |
| Build a static accessible page | Do not force GSAP, random selection, or a second color mode without a relevant requirement. |
| Implement this supplied screenshot | Preserve the supplied reference. Generate another image only for an explicit design need. |
| Validate whether a product idea is worth building | Select growth-advisor. State evidence gaps and a test that resolves them. |
| Explain `Partial<T>` | Give the explanation. Do not run a repository compiler or remove unrelated `any` types. |
| Validate an unknown User response | Reject wrong field types, null, missing fields, and failed HTTP responses. |
| Inspect staging in an unrelated company | Do not select DexCare from the word `staging` alone. |
| Sync an app to its canary stage | Verify context and diff. Stop at the authorized rollout stage. |
| Write a Node core commit message | Use the repository's format and sign-off rules. Do not force Conventional Commits. |
| Review this PR in detail | Preserve required evidence. Do not force a one-line style. |
| Save permanent project knowledge | Select durable memory writing with the correct scope. Do not create a transient handoff instead. |
| Create a file for the next agent | Use the file handoff path. Do not consume a memory handoff or create an Orca worktree by default. |
| Prepare one job application | Use the candidate evidence and required workflow. Deliver the package. Do not submit it. |
| Complete a ship cycle for an Enerflo issue | Preserve per-command authentication. Reach the concrete per-PR merge boundary. |

Run the same representative requests before and after each small change group. Record selected skills, unnecessary questions, unnecessary tools, completion, and regressions. Measure tokens and latency only if the host exposes reliable values. Keep Astra and any other model you still use in the comparison. A reduction in text is acceptable only when task quality and required controls remain intact.

## Limits

This report identifies instruction defects and likely selection conflicts. It does not prove how often a model follows each instruction. Frontmatter parsed successfully, but that does not prove every host supports every key. Claude-style `disable-model-invocation`, `allowed-tools`, dynamic shell injection, and model fields need host-specific verification. File presence also does not prove a skill is available in the current task catalog.

Before changing a cited file, compare its SHA-256 with the inventory and read the current version. The directory was being updated concurrently. Any new or changed file after the snapshot needs a separate check.
