# Color

Think in oklch. One brand hue. Everything else is lightness.

## 1. The structure the best SaaS apps share

- Monochromatic palette. One hue, chroma near zero for surfaces and text, lightness stepped.
- The neutrals are not neutral. They carry the brand hue at chroma 0.004 to 0.012. Cool brands lean blue, warm brands lean orange or yellow. Pure gray is a smell.
- Depth comes from lightness steps, not shadows. Surfaces: canvas, raised, overlay. Borders are hairlines one or two steps away.
- Text is three lightness steps on the same hue: primary, secondary, tertiary.
- The brand color is under 10 percent of an app screen: primary action, focus ring, active nav, selected row, links, progress. Marketing pages may use more.
- Semantic colors (danger, success, warning, info) are the only other hues, desaturated to sit inside the palette. Lightness matched to the brand color.
- Saturation arrives from content: third-party logos, avatars, charts, images. The palette is flat because it expects color from outside.
- Dark mode inverts lightness and keeps hue and chroma. Only possible when the scale is generated.

Observed: Notion white canvas, gray-light sidebar. Linear cool grays, indigo brand. Claude warm off-white canvas, orange brand. Stripe white canvas, indigo links, muted semantic dots.

## 2. Recipe: derive the scale from one hue

Input: brand color in oklch, `L C H`. Hex, rgb and hsl are not inputs. If that is what you have, ask the user for the oklch value. No mental conversion.

Neutral scale, hue `H`, chroma by warmth:

| Step | Light L | Dark L | Chroma |
|---|---|---|---|
| canvas | 0.99 | 0.14 | 0.002 to 0.006 |
| raised | 0.975 | 0.18 | 0.004 to 0.008 |
| overlay | 1.0 | 0.22 | 0.004 to 0.008 |
| line | 0.92 | 0.27 | 0.006 to 0.012 |
| line-strong | 0.87 | 0.32 | 0.008 to 0.014 |
| text-tertiary | 0.62 | 0.55 | 0.010 to 0.020 |
| text-secondary | 0.47 | 0.72 | 0.012 to 0.024 |
| text-primary | 0.21 | 0.95 | 0.010 to 0.020 |

Warm brands (hue 40 to 110) can take chroma at the top of each range. Cool brands (hue 220 to 300) stay at the bottom.

Brand:
- `brand`: the given color. If L is above 0.7 or below 0.45, it will fail contrast as a button fill. Adjust L to 0.5 to 0.65 for the fill and keep the original as `brand-vivid` for icons and marketing.
- `brand-hover`: L minus 0.05.
- `brand-soft`: L 0.95 light, 0.25 dark, chroma 0.03. Selected rows, tinted badges.
- `on-brand`: white or canvas, whichever passes 4.5:1.

Semantic, chroma 0.12 to 0.16, L matched to brand fill:
- danger hue 25, success hue 150, warning hue 80, info hue 240 or the brand hue.
- Each gets a `-soft` at L 0.95 chroma 0.04 for backgrounds.

## 3. Rules of use

- Text on a tint: inset the text from the tint edge or bleed the tint past the container. Never share an edge.
- Prefer colored text to a colored panel behind text. Cheaper, more legible, more accessible.
- Light tints under text. Never a solid dark brand panel with body copy on it.
- One accent color per screen. A second accent needs a written reason in DESIGN.md.
- Same color for the same kind of content everywhere. Captions, links, status dots do not change meaning by page.
- Icons take `text-secondary`. Brand on an icon means active state only.
- Focus ring: brand at 2 px offset 2 px. Same everywhere.
- Contrast: body text 4.5:1, large text and UI borders 3:1. Check the derived values, do not assume.

## 4. Tailwind v4 wiring

`@theme` cannot be nested under a media query, so the light and dark values live on `:root` and `[data-theme=dark]` as plain variables, and `@theme inline` maps them to Tailwind namespaces. See `templates/theme.css`. Utilities then read `bg-canvas`, `text-secondary`, `border-line`, `bg-brand`.
