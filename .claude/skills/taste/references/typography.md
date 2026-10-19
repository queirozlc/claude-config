# Typography

The book's rule: the body size and its leading define everything. The line-height becomes the vertical unit of the whole layout.

## 1. Family

- One grotesque with a full weight range (400, 500, 600 minimum). Or one sans body plus one serif display, the pairing Claude uses. Never two sans. Never two serifs.
- Medium width for body. Condensed and expanded only for display.
- Tabular figures on anything numeric: tables, metrics, timers, prices. `font-variant-numeric: tabular-nums`.
- Pick a face engineered for screens. Check it has real 500 and 600 weights, not synthetic bold.

## 2. Sizes: four, no more

| Role | App UI | Marketing | Weight | Line-height |
|---|---|---|---|---|
| display | 24 to 32 px | 40 to 64 px | 600 | 1.1 to 1.2, snapped to a whole or half line unit |
| title | 16 to 20 px | 24 to 32 px | 600 | 1.25 to 1.5, whole units |
| body | 14 or 16 px | 16 to 18 px | 400, 500 for labels | 1.5, this is the line unit |
| caption | 12 or 13 px | 13 to 14 px | 400 | 1.33 to 1.5, so two captions equal a whole number of body lines |

Size jumps must be unmistakable. 14 next to 16 reads as a mistake. 14 next to 20 reads as hierarchy.

Hierarchy ladder, cheapest first: whitespace, then weight, then color, then size, then a rule. Reach for space before reaching for a bigger size. Linear settings use one body size with medium weight labels and secondary-color descriptions. Roto C magazine in the book used one size for body and subheads, separated by an empty line.

## 3. Measure and leading

- 7 to 10 words per line. 60 to 75ch for prose, 45 to 55ch for narrow columns and captions.
- Narrower column, smaller face. Use container queries on the column, not viewport queries.
- Body line-height 1.5. Never lower than 1.4 for paragraphs. Display 1.1 to 1.2.
- Loose leading breaks cohesion as badly as tight leading. Cap body at 1.7.
- Reversed text on dark surfaces: keep it short, raise line-height one step.
- Letter-spacing: none on body. Negative tracking, minus 0.01 to minus 0.02em, only at 28 px and above. Positive tracking only on uppercase labels, and uppercase labels are rare.

## 4. The line unit in Tailwind

Body 16 px at 1.5 gives 24 px. Tailwind spacing is 4 px, so whole lines are `6`, `12`, `18`, `24`. Half line `3` is allowed only inside dense rows. Body 14 px at 1.5 gives 21 px, which does not sit on 4 px. Either set body line-height to 20 px (`leading-5`) and use `5`, `10`, `20`, or use 16 px body. Decide once in DESIGN.md.

## 5. Text colors

Three: primary, secondary, tertiary. Labels primary at 500 weight. Descriptions secondary. Metadata and placeholders tertiary. Disabled reuses tertiary plus 50 percent opacity. Never a fourth gray.

## 6. Setting up

`--text-*` and `--leading-*` in `@theme` register the four sizes as utilities: `text-display`, `text-title`, `text-body`, `text-caption`. Delete the temptation to use `text-lg`, `text-xl`, `text-2xl`, `text-3xl` on the same screen. The audit counts distinct sizes.
