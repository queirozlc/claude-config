# Slop smells

Patterns that appear because the training data is GitHub demos, component libraries and Tailwind tutorials. Each is a finding in `/taste audit`. Each has a fix.

Root cause of most of them: values chosen per element. Nothing derived. The fix is always the same, the closed vocabulary in SKILL.md.

## Layout

- Body text or forms stretching the full viewport width. Fix: measure.
- Symmetric equal margins, same padding top and bottom, everything centered. Fix: asymmetric frame, top-left anchoring in app UI.
- Three identical feature cards, then three more. Fix: as many cells as features, two different sizes or fills, on allowed spans.
- Alternating image-left, image-right sections as the only rhythm. Fix: max two in a row.
- Alternating section background colors as the only rhythm. Fix: whitespace in whole line units.
- Every item in its own card. Cards inside cards. Fix: group rows in one surface with dividers.
- A filler tile to complete a grid. Fix: leave the cell empty.
- Hero with two CTAs, the second a ghost outline. Fix: one primary, the secondary is a text link.
- Widths like `w-[347px]`, `w-[calc(33%-1rem)]`, `col-span-5`. Fix: allowed spans.

## Typography

- Six or more font sizes on one screen. Fix: four.
- Eyebrow labels above every heading, often monospace uppercase, on content and marketing pages. Fix: delete. A section title with whitespace above it is the hierarchy.
- Monospace for anything that is not code or a key.
- Negative tracking on body text. Fix: tracking only at 28 px and up.
- Emoji in headings. Fix: delete.
- Green checkmark bullet lists as the feature section. Fix: prose or a real comparison.
- Uppercase small labels everywhere. Fix: sentence case, secondary color.

## Color and depth

- Pure gray neutrals, `#808080`, `zinc` next to a warm brand. Fix: neutrals on the brand hue.
- Gradient text. Glow blobs behind the hero. Purple-to-blue gradient accent. Fix: one flat brand color.
- `shadow-lg` cards on white. Fix: hairline plus one lightness step.
- Tinted rounded pill or bar on the left border of a card as an accent. Fix: status dot or colored text.
- Icon in a tinted circle before every feature title. Fix: icon at 16 or 20 px in secondary color, or no icon.
- Brand color on icons, borders, badges and backgrounds at once. Fix: under 10 percent, primary action and state only.
- Text sharing an edge with its tinted background. Fix: padding or bleed.
- Glass, backdrop blur, and glow on surfaces at rest. Fix: nothing.

## Radius and shape

- Three radii on one screen. `rounded-2xl` cards with `rounded-md` buttons inside. Fix: one family, two values plus full.
- Inner radius equal to outer radius with padding between. Fix: inner = outer minus padding.
- Pill buttons in a product whose family is crisp. Fix: family radius.

## Motion

- Bounce or overshoot on UI chrome. Fix: ease-out.
- Hover transitions over 200 ms. Fix: fast tier.
- Everything animates on scroll, every time. Fix: once, marketing only, or not at all.
- Slide-in from 100 px. Fix: 8 to 16 px.
- Spinners where a skeleton belongs. Fix: skeleton with shimmer.
- No exit animation. Elements pop out. Fix: exit at fast tier.
- Transition on `all`. Fix: name the properties.

## Content

- Fake stat walls. "Trusted by 10,000+ teams". Logo rows of companies that are not customers. Fix: real proof or none.
- Placeholder names like Acme, John Doe, lorem ipsum in a deliverable. Fix: realistic data from the domain.
- Badge soup: New, Beta, Pro, AI on the same screen. Fix: one badge type, used rarely.
- "Powered by AI" sparkle icons. Fix: delete.

## Library defaults

- shadcn or similar with its shipped palette, ring color, `shadow-sm` cards and `rounded-md` untouched. Fix: remap tokens to `theme.css`, strip defaults, keep behavior.

## Consistency

- A component that does not use the tokens. `text-gray-500` next to `text-secondary`. Fix: tokens only, audit counts raw palette classes.
- Spacing values chosen per element: `mt-3`, `mt-5`, `mt-7` in one component. Fix: whole line units.
- Different gaps in sibling grids. Fix: one gutter.
- A screen that ignores DESIGN.md. Fix: read it first, every call.
