---
name: taste
description: Start and grow SaaS UI from foundations. Derives a design system from one oklch brand hue on Tailwind v4, then builds screens and components that serve a stated intent. Use for /taste, design system setup, new UI surfaces, motion specs, slop audits.
argument-hint: "[setup | component <what> | motion <what you saw> | audit [path]]"
user-invocable: true
---

# taste

Nothing is chosen per element. Every value comes from a small closed vocabulary. Design starts from intent and references, never from a blank prompt.

Framework-agnostic. Tailwind v4. Icons, fonts and motion library are decided per project in the brief.

Component libraries such as shadcn are welcome. Keep their behavior and DOM, remap their tokens to ours, strip the stock look. Rules in [references/components.md](references/components.md), section 5.

## Colors: oklch only

All colors are written in oklch. If the user gives hex, rgb or hsl, stop and ask them for the oklch value. Do not convert by eye or from memory. The only exception is a conversion done by a tool in the project that the user has approved.

## Brief first

Before `setup` and before `component`, ask for the brief. Do not build without it.

1. Intent: what this product or screen must do, for whom, and what it should feel like. One or two sentences.
2. References: two or three apps, screens or flows. Pull them from Mobbin by name or description and look at them. A gallery link or a screenshot also counts.
3. No-gos: what the user does not want.

Restate the brief in three lines and get a yes. Then work.

## Subcommands

| Call | Does |
|---|---|
| `setup` | Brief, then derive the system. Writes `theme.css` and `DESIGN.md`. |
| `component <what>` | Brief, then one component or screen that earns its place. |
| `motion <what you saw>` | Turns a description into a motion spec and code. |
| `audit [path]` | Slop scan, vocabulary count, friction pass. |
| no args | Reads `DESIGN.md` if present, else runs `setup`. |

Load only the reference the subcommand names.

### setup
Inputs from the user: brand color in oklch, font family, the brief. Everything else is derived.
1. Register from the brief (tool, consumer, enterprise) picks the radius family and neutral warmth. [references/radius-and-depth.md](references/radius-and-depth.md)
2. Copy [templates/theme.css](templates/theme.css) next to `@import "tailwindcss"` and fill the placeholders. Derivation rules in [references/color.md](references/color.md). Type rules in [references/typography.md](references/typography.md).
3. Write `DESIGN.md`, under 40 lines: brief, hue, chroma, warmth, the four sizes, line unit, gutter, spans, radius family, font, icon set, motion tier and library, references used.
4. Stop when the tokens compile. No demo pages.

### component
Read `DESIGN.md`. Then [references/components.md](references/components.md): job, primary action, proof, hierarchy. Layout from [references/layout.md](references/layout.md). Build with the vocabulary. Run the friction pass once, fix, stop.

### motion
[references/motion.md](references/motion.md). Fill the spec template, classify transition or animation, choose CSS or library by the escalation rule, deliver spec and code.

### audit
[references/slop-smells.md](references/slop-smells.md). One line per finding: file, line, severity, fix. Then count sizes, text colors, radii, vertical spacing values, gap values against the vocabulary. Then the friction pass.

## The closed vocabulary

- Line unit: body line-height. 16/24 gives 24 px. Vertical spacing in whole units: `6`, `12`, `24`. Half unit `3` only inside dense rows.
- Gutter: one value. `gap-4` dense, `gap-6` normal.
- Tracks: 12. Spans 3, 4, 6, 8, 12. No percentages, no arbitrary widths.
- Measure: prose 60 to 75ch. Forms and settings 640 to 720 px. Content never stretches to the viewport.
- Text: display, title, body, caption. Colors: primary, secondary, tertiary.
- Surfaces: canvas, raised, overlay. One hairline token. Shadows only on floating layers.
- Radius: two values from one family plus full.
- Brand color: primary action, focus, active, selected, links, progress. Under 10 percent of an app screen.
- Motion: `duration-(--duration-fast)` 140 ms for hover and press, normal 220 ms, layer 320 ms. Ease-out in, ease-in out, ease-in-out between states, linear only for loops.

## Pre-flight

1. Brief restated and confirmed.
2. Vertical gaps are whole line units.
3. Blocks on allowed spans.
4. One gutter.
5. Four sizes or fewer.
6. Prose inside a measure.
7. Bottom padding larger than top.
8. One dominant element.
9. Brand color only on action and state.
10. No tint sharing an edge with text.
11. Exits faster than entries, reduced motion respected.
12. Zero slop smells.

Fail, fix, stop. One pass.

## Sources

Müller-Brockmann, Grid Systems in Graphic Design: [references/book-muller-brockmann.md](references/book-muller-brockmann.md). Mobbin screens of Linear, Stripe, Notion and peers. revenue-centric-design skill for UX and the friction pass. Lucas's notes in ai-memory `design/saas-ui-foundations`.
