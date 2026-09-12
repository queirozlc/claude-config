---
name: gpt-taste
description: Optional GSAP guidance for requested scroll or interaction animation. Use when the design brief calls for GSAP motion.
---

# GSAP motion

Use motion to support the requested interaction or narrative. Preserve the project's layout, typography, tokens, and installed animation stack. A static interface is a valid result. Do not require a new dependency for a simple transition.

Choose a pattern only when it helps the brief:
- Pin a title while related content scrolls, if the content remains accessible on small screens.
- Scrub a reveal or image transform when scroll progress conveys useful sequence.
- Stack cards when the overlap preserves reading order and interaction.
- Use a small hover or press transition when feedback needs it.

Use the installed GSAP version's documentation for APIs. In React, follow the project's animation lifecycle and clean up timelines and ScrollTriggers on unmount or dependency changes. Respect reduced-motion preferences and keep a readable static state. Do not make animation the only state cue.

Verify the changed interaction at relevant viewport sizes. Check scrolling, focus, content visibility, and reduced motion. Continue through confirmed defects within scope. Do not require a particular hero, grid, page structure, font, or number of effects.

Report only tools actually run and results actually observed. Never invent execution or mock tool output.
