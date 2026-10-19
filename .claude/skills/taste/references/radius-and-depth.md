# Radius and depth

Radius tells the register of the product without saying it. Depth tells what is in front without shadows.

## 1. Radius families

| Family | Base | Controls | Cards and panels | Register | Seen in |
|---|---|---|---|---|---|
| sharp | 0 to 2 px | 2 px | 2 to 4 px | enterprise, finance, data, serious tooling | trading terminals, older enterprise suites |
| crisp | 4 px | 4 to 6 px | 6 to 8 px | professional tools, developer products | Linear, Vercel, Stripe |
| soft | 8 px | 8 px | 12 px | modern SaaS, productivity, AI products | Notion, Figma, Claude, ChatGPT |
| round | 12 px | 12 px, pills common | 16 to 24 px | consumer, mobile-first, friendly | Airbnb, Spotify, consumer fintech |

Pick one family in setup. The family gives two values: `radius` for controls and `radius-lg` for containers. Plus `full` for pills, avatars, toggles. Three utilities. Nothing else on the screen.

Rules:
- Nested radius: inner radius equals outer radius minus the padding between them. A 12 px card with 8 px padding holds 4 px children. Otherwise corners look misaligned.
- Pills only on things that are pill-shaped by nature: tags, toggles, avatars, segmented controls in soft and round families. Pill buttons are a brand decision, not a default.
- The radius family does not change between marketing and app. It is the identity.
- Inputs and buttons in the same row share one radius.
- Mobile can go one step rounder than desktop in the same family. Not two.

## 2. Depth without shadows

Three surface levels, by lightness:

| Level | Light mode | Dark mode | Border |
|---|---|---|---|
| canvas | L 0.99 | L 0.14 | none |
| raised | L 0.975 or 1.0 | L 0.18 | hairline `line` |
| overlay | L 1.0 | L 0.22 | hairline `line` plus shadow |

In light mode, raised can be lighter or darker than canvas. Pick one direction per product. Notion darkens the sidebar. Linear lightens the settings card. Do not mix.

Borders: a hairline at one or two lightness steps. That is the depth cue for everything at rest. Shadows are reserved for floating layers: popover, dropdown, modal, toast, drag preview. A card at rest has no shadow.

Shadow scale, two values only:
- `shadow-overlay`: `0 4px 16px -4px oklch(0 0 0 / 0.12), 0 0 0 1px oklch(0 0 0 / 0.04)` for popovers and menus.
- `shadow-modal`: `0 16px 48px -12px oklch(0 0 0 / 0.24)` for dialogs and sheets.

In dark mode shadows nearly vanish. Raise the surface lightness one more step instead, and use a lighter hairline.

## 3. Rings and focus

- Focus ring: 2 px brand, 2 px offset, on every interactive element. Same everywhere.
- Hover on rows and list items: raised surface one step lighter or darker, fast transition. No border change.
- Selected: `brand-soft` background, primary text. No brand border.
- Inset ring `0 0 0 1px` for inputs at rest in the crisp and sharp families. Border for soft and round.

## 4. What this replaces

- Cards with `shadow-lg` on white. Replace with hairline plus one lightness step.
- Three radii on one screen. Replace with the family's two plus full.
- Glass, blur, and glow on surfaces at rest. Replace with nothing.
- A colored left border on a card as an accent. Replace with a status dot or colored text in the row.
