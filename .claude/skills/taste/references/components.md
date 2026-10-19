# Components that earn their place

The UI serves a UX job. This file joins the vocabulary in the other references with the revenue-centric-design spine and the friction pass, so a component is built because a job needs it, not because it is pretty.

## 0. The brief

Intent, references, no-gos, confirmed by the user. Pull the referenced screens from Mobbin and look at them before writing the three sentences below. A component built without a brief is decoration by definition.

## 1. Before building: three sentences

Write these three lines at the top of the work. If any is empty, do not build.

1. Job: who is doing what, to get what. From the user's brief, not invented.
2. Primary action: the one thing this screen exists to make happen. Neutrality is omission. A screen that does not direct hurts conversion.
3. Proof: what the user must see before they commit. Value first, ask later. The proof sits above or beside the action, never below it.

Then the attention hierarchy in order: proof, primary action, the data needed to decide, secondary actions, navigation, everything else. The visual hierarchy follows this order exactly. Size, weight, color and position are spent top-down on this list.

## 2. The mall rule

On mobile, space is the budget. Each component pays rent with a job. On web, attention is the budget. Each component pays rent with a place in the hierarchy. A component with no line in the hierarchy list is decoration. Delete it.

## 3. Defaults are decisions

The initial state of every control is a decision made for the user. Pick the default that serves the job and the business, state it in the component notes, and make the alternative reachable in one action.

## 4. Component recipes on the vocabulary

Each recipe lists the tokens it may use. Nothing else.

Button
- Sizes: one height per tier, body size text, `px-4`, radius from family. Primary: `bg-brand text-on-brand`. Secondary: `bg-raised border-line text-primary`. Tertiary: text only, secondary color. Danger only on confirm steps.
- One primary per screen. Press scale 0.98 fast.

Input
- Height equals button height. Label primary at 500 above, caption help below in secondary. Error: caption in danger, border danger, no icon needed. Focus ring brand.
- Placeholder tertiary, never used as the label.

Row and list
- One line unit plus `py-3`. Leading icon 16 px secondary, label primary, trailing meta caption tertiary or control. Hover raised. Divider hairline. No card per row.

Card
- Only for grouping rows or a single dominant object. Raised surface, hairline, `radius-lg`, `p-4` or `p-6`. No shadow at rest. Title row inside uses title size, then rows or content.

Metric
- Caption label in secondary above, display number in primary with tabular figures, caption delta below in success or danger. Aligned to one baseline across siblings. Stripe puts four in a row on spans of 3.

Table
- Header caption in secondary, uppercase is allowed here and nowhere else. Rows one line unit plus padding, hairline dividers, hover raised. Numeric columns right-aligned tabular. Actions in the last column on hover only.

Empty state
- Centered inside the canvas, the one exception to top-left. Title, one line of body in secondary, one primary action. No illustration unless the brand has a system for them.

Modal
- Overlay at layer tier, panel `max-w-md` for confirm, `max-w-2xl` for forms, `radius-lg`, `shadow-modal`. Title, body, actions right-aligned with primary last. Never stack modals.

Navigation rail
- Section labels in caption tertiary, items one line unit each, active item `brand-soft` background with primary text, icon 16 px. Footer slot for the business message: trial days, upgrade, invite. The upgrade prompt lives here at the moment of a limit, never as an interruption.

Onboarding step
- Centered column of 480 px, progress as a thin bar not dots, one question per screen, options as full-width rows with radio semantics, primary action fixed at the bottom. Third-party logos here are the only saturated color on the screen and that is the point.

Pricing
- Three columns on spans of 4, the recommended one raised one surface step and labeled. Feature rows in one line unit, tabular check marks in secondary, not green. Price display size tabular. One primary per column.

Toast
- Bottom right, `max-w-sm`, raised surface, hairline, `shadow-overlay`, icon in semantic color, body text, optional single action. Enter normal, exit fast, auto-dismiss 5 s, hover pauses.

## 5. Ready-made component libraries

shadcn/ui, Radix, Base UI, Headless UI and similar are the right starting point. They own behavior, accessibility, keyboard handling and edge cases. Do not rewrite that.

Customize means: the component reads our tokens and drops its default look. It does not mean redesigning the component.

Do:
- Map every library token to `theme.css`: colors to canvas, raised, line, primary, secondary, brand; radius to the family; shadows to overlay and modal only; font to ours. In shadcn, edit the CSS variables block once, in oklch, and delete the palette it shipped with.
- Remove the defaults that mark a site as "shadcn out of the box": the stock gray-zinc palette, `shadow-sm` on cards at rest, the default ring color, `rounded-md` everywhere, the sample `Button` variant set with `destructive` styled louder than `default`.
- Keep the component API and DOM. Change class names and variables only.
- Heights, paddings and gaps come from the vocabulary, not from the library defaults.

Do not:
- Fork the component to add visual flourish.
- Keep the demo look because it "already looks clean". Clean and cliché are the same thing here.
- Mix library defaults and our tokens on one screen. The audit counts raw palette classes.

## 6. After building: the friction pass

Run the friction pass from the revenue-centric-design skill, `references/friction-and-usability.md`, or delegate a full screen or flow to the `friction-auditor` agent. It checks Krug's rules: no question marks, no mindless choices, words cut in half, clear hierarchy, the trunk test, the goodwill reservoir. Fix its findings in one round. Do not build a second version.

## 7. Where UX rules come from

- Landing pages, CTAs, proof, awareness levels: revenue-centric-design `references/conversion-and-landing-pages.md`.
- First run, empty states, activation: `references/onboarding-and-activation.md`.
- Pricing tables, decoys, upgrade paths: `references/pricing-and-monetization.md`.
- Attention hierarchy, feature discipline: `references/product-strategy-and-features.md`.

Load the one that matches the surface. This file only says how the UI must express the answer.
