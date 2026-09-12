---
name: make-interfaces-feel-better
description: Review or refine interface details only when the user explicitly activates this skill.
disable-model-invocation: true
---

# Interface detail review

Do not select or read this skill automatically. Use it only after explicit user activation.

Preserve the project's styling system, tokens, components, and intended behavior. Inspect the requested surface and choose only relevant guidance.

| Subject | Reference |
| --- | --- |
| Text wrapping, font rendering, changing numbers | [Typography](typography.md) |
| Nested corners, optical alignment, shadows, image edges, hit areas | [Surfaces](surfaces.md) |
| Interruptible transitions, entry and exit, motion restraint | [Animations](animations.md) |
| Stroke weight, currentColor, state, sizing, RTL | [Icons](icons.md) |
| Transition properties and measured rendering issues | [Performance](performance.md) |

Treat example values as starting points, not universal requirements. Existing design tokens and the requested behavior determine the change. Keep visible focus and static state cues. Respect reduced motion and avoid adding an animation dependency for a small detail.

For a quick review, inspect the primary path and significant states. For a full review, cover the requested scope, not unrelated screens. Check motion at normal speed; slow playback only when timing or sequencing needs diagnosis.

Report actionable findings with location, observed behavior, proposed change, and user impact. Combine repeated causes. Do not impose a finding count or invent rejected candidates. State actual coverage and verification limits. Confirm changes with relevant interactions and checks. Optional polish can stop; confirmed functional or accessibility defects in scope still need resolution.
