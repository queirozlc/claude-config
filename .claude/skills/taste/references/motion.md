# Motion

Motion is hard to brief because the vocabulary is loose. This file fixes the vocabulary, then gives a template for describing an animation you saw so it can be rebuilt.

Mobbin serves static screenshots through the MCP. It cannot show motion. Describe what you saw with the template below instead.

## 1. Transition vs animation

Transition: a property moves from state A to state B because state changed. Two keyframes, implicit. Defined by property, duration, easing. Hover, press, open, close, focus, toggle.

Animation: a sequence over time, with its own keyframes or physics, that may run without a state change. Defined by keyframes or a spring, duration or stiffness, iteration, direction. Spinner, shimmer, pulse, count-up, enter choreography, morph.

Rule: default to transitions. Use an animation only when the motion has more than two keyframes, loops, or is physics-driven.

## 2. Easing vocabulary

| Name | Curve | Use |
|---|---|---|
| ease-out | `cubic-bezier(0.2, 0, 0, 1)` | Entering. Things appearing, opening, expanding. Fast start, soft landing. |
| ease-in | `cubic-bezier(0.4, 0, 1, 1)` | Exiting. Things leaving, closing. Soft start, fast away. |
| ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` | Moving between two on-screen positions or sizes. Sidebar collapse, tab indicator slide, reorder. |
| linear | `linear` | Continuous motion only. Marquee, progress, spinner rotation, shimmer. Never for UI state changes. |
| spring | physics: stiffness, damping, mass | Gesture-driven or physical. Drag release, sheet snap, toggle knob, playful brands. |

Browser `ease` and `ease-in-out` keywords are fine for prototypes but the named curves above are more decisive. Register them as `--ease-out`, `--ease-in`, `--ease-in-out` in `@theme`. Never bounce or overshoot on UI chrome. Overshoot is a brand decision, made once in DESIGN.md.

## 3. Durations

| Tier | ms | Use |
|---|---|---|
| instant | 0 | Focus ring. Text color on hover of links. |
| fast | 120 to 150 | Hover, press, toggle, checkbox, tooltip appear. |
| normal | 200 to 250 | Dropdown, popover, small enter or exit, accordion. |
| layer | 300 to 350 | Modal, sheet, drawer, sidebar collapse. |
| page | 400 to 500 | Route transition, shared-element morph. |

Rules:
- Exit is 20 to 30 percent faster than enter.
- Larger distance, longer duration. Same tier table, pick the upper value.
- Stagger 30 to 50 ms per item, cap at 6 items. Beyond 6 items animate the container only.
- Tooltip: 100 ms fade, 300 to 500 ms delay before showing, no delay on the next tooltip while one is open.

## 4. Animation types

| Type | What moves | Default recipe |
|---|---|---|
| fade | opacity | 0 to 1, ease-out, fast or normal |
| scale | transform scale | 0.96 to 1 plus fade, `transform-origin` at the trigger, normal |
| slide | transform translate | 8 to 16 px along the entry edge plus fade, normal. Not 100 px. |
| morph | size, position, radius of one element across two states | View Transitions API or a layout animation in a motion library. Page tier. |
| spring | transform via physics | stiffness 300 to 500, damping 30 to 40 for chrome. Lower damping only for playful brands. |
| glow or pulse | opacity or box-shadow loop | 1.5 to 2 s, ease-in-out, alternate. Only for live or recording states. |
| shimmer | background-position | 1.5 s linear loop. Skeletons only. |
| count-up | number | 600 to 800 ms ease-out, tabular figures so width is stable. |

Animate only `transform` and `opacity` unless there is no other way. `height: auto` transitions need `interpolate-size: allow-keywords` or a grid-rows trick or a motion library.

## 5. Micro-interaction catalog

The ones that make an app feel alive, with defaults.

- Button press: scale 0.98, fast, ease-out. Release returns at the same tier.
- Toggle: knob translate with a spring or ease-in-out at fast. Track color transitions at fast.
- Checkbox: check path draws over fast with ease-out, box background at fast.
- Dropdown and popover: scale 0.96 to 1 plus fade, origin at the trigger corner, normal in, fast out.
- Tooltip: fade only. No scale.
- Toast: slide 16 px from its edge plus fade, normal in, fast out. Stack pushes with ease-in-out.
- Modal: overlay fade at layer tier, panel scale 0.98 to 1 plus fade. Never slide a centered modal.
- Sheet or drawer: translate from its edge with ease-out at layer tier. Spring if gesture-dismissible.
- Sidebar collapse: width with ease-in-out at layer tier. Labels fade out at fast before the width moves.
- Tab indicator: the underline or pill morphs between tabs. Layout animation or width plus translate with ease-in-out at normal.
- List add or remove: item fades and slides 8 px, siblings shift with ease-in-out. Removal must move siblings, not leave a hole.
- Optimistic update: apply the state instantly, show a subtle pulse if it takes over 300 ms, revert with a fast shake of 4 px if it fails.
- Skeleton: shimmer, then crossfade to content at normal. No layout shift.
- Accordion: content height with ease-in-out at normal, chevron rotates 90 or 180 degrees at the same tier.
- Number change: count-up on metrics, crossfade on prices.
- Scroll reveal: fade plus 8 px slide on first entry, once, never on every scroll. On marketing pages only.

## 6. Describing an animation you saw

Fill this, one line per field. It turns a memory into a spec.

```
Trigger:   what starts it (hover, click, route change, data arrival, scroll into view)
Element:   what moves (the whole card, the icon, the background)
Property:  opacity, scale, translate, size, color, path
From, to:  numbers, not adjectives (0.96 to 1, 16 px up to 0)
Duration:  tier from the table
Easing:    name from the table
Origin:    where it grows from (top-left of trigger, center)
Exit:      same in reverse, faster, or none
Choreo:    what else moves at the same time, and the stagger
Type:      transition or animation. If animation: fade, scale, slide, morph, spring, glow, shimmer.
```

Example: "the Linear command palette". Trigger cmd-k. Element the panel. Property scale and opacity. From 0.98 and 0 to 1 and 1. Duration normal. Easing ease-out. Origin center top. Exit reverse at fast. Choreo the overlay fades at the same time, no stagger. Type transition.

## 7. CSS or library

Start CSS. Escalate to a motion library (Motion for React, or Motion One for vanilla) when the spec needs: a spring, a layout or shared-element morph, gesture tracking, exit animations on unmount in React, or orchestration of more than 3 elements. Do not escalate for a fade.

Easings are registered in `@theme` as `--ease-out`, `--ease-in`, `--ease-in-out`, so `ease-out` and friends are utilities. Durations are plain variables on `:root` because Tailwind v4 has no `--duration-*` namespace. Use `transition-[transform,opacity] duration-(--duration-fast) ease-out` so the audit can count them.

## 8. Reduced motion

`@media (prefers-reduced-motion: reduce)`: keep opacity fades, remove translate and scale, set durations to instant, stop loops. Do this in the base layer once, not per component.
