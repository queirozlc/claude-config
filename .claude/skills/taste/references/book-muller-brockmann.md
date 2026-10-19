# Müller-Brockmann, Grid Systems in Graphic Design. Core spec for web use

Distilled 2026-09-11 from the full 162-page scan (8 slices, see part-01..08.md).
Paraphrased rules and the book's own numbers. Not a summary of the prose.

## 1. Construction order (the book's method, in sequence)

1. Inventory the content first: how much text, how many images, how many large vs small, captions, notes, tables. Write the priority list before any layout.
2. Fix the format and the margins. Margins define the type area. Margins are unequal. Book ratios: inner 1 : head 1.5 : outer 2 : foot 3, or Golden Section 3 : 5 : 5 : 8 (inner : head : outer : foot). Foot always deeper than head. Equal margins are called dull and indecisive.
3. Choose the body type size and leading for the reading distance (30 to 35 cm for print). Body 8 to 12 pt. Normal letterspacing, medium width.
4. Derive the column width from the type size: 7 words per line minimum, 7 to 10 the range, 10 the comfortable average. Wider column needs a bigger face. If a title and body share a column, size the column for the body.
5. Choose column count from content variety: 1 column too rigid for images. 2 subdivides to 4. 3 subdivides to 6. 4 subdivides to 8 and 16 (good for data). More columns means smaller type.
6. Fix the vertical module from the leading. Every other type size must land on the same module. Book example: 7/8, 10/12 and 20/24 all resolve on a 24-pt rule (3 lines, 2 lines, 1 line). Captions 6 pt solid: two caption lines equal one 10/12 body line.
7. Cut the columns into fields. Field depth is a whole number of text lines. Gap between fields is 1 whole empty line (2 or 3 if captions live there). Never half lines.
   Formula: column depth in lines = fields x lines per field + (fields - 1) x gap lines.
   Worked example: 57 lines drafted, 4 fields, 1-line gaps: (57-3)/4 = 13.5, no half lines, so 13 x 4 + 3 = 55 lines. Redraw the column to 55 lines.
8. Enumerate the allowed image formats: column spans x field depths. 4 x 8 = 32 fields gives 32 formats. Use the corner diagonal to keep them proportional. Then discipline yourself: 2 or 3 sizes per page, not 8.
9. Sketch small at the final proportion, cut to 2 or 3 candidates, enlarge to 1:1, keep one. Expect to restart.

## 2. Hard rules (the constraints agents should never break)

- Every vertical gap is a whole number of lines or whole grid units. Half steps break cross-column alignment.
- Every image, table, chart and tint fills whole fields. Smallest image is one field. Width equals column width or a combination of columns.
- Image top edge sits on the cap line, bottom edge on the descender line of the adjacent text.
- The gutter is one value, set once. Side offsets for marginal items (folio, notes) reuse the gutter measure.
- Fewer picture-size differences means a quieter page. But one dominant picture is needed or the page goes dull.
- Text on a tint: inset the text from the tint edge, or bleed the tint past the text. Never share an edge. Better: colour the text, drop the panel.
- Light tints under text, not dark. Screen a dark colour rather than print it solid behind type.
- Cut-out images need a backing field (light tint, rule box, or top and bottom rules) or they float.
- Reversed (light-on-dark) text stays short and gets wider leading.
- Same leading for every instance of a type size. Same size and position for every title, subtitle, caption.
- Hold format, grid, face and sizes constant across a series. Vary one thing (cover colour or image).
- Cover and inside share one grid and one type scale, designed together.

## 3. Type scale in the book's own practice

- Sizes used per publication: 1 to 4, never more. Roto C uses one size for body and subheads, separated only by an empty line before and after.
- Hierarchy ladder, cheapest first: whitespace, then weight, then size, then a rule. Colour is a hierarchy level too (captions in red, titles black or blue by importance).
- Size jumps must be unmistakable. 9 pt vs 6 pt is the benchmark. Adjacent sizes read as errors.
- Weights as grey values: medium light, semi-bold medium, bold deep. Three weights cover a full hierarchy.
- One family with a full weight range. Never pair two faces of the same genre.
- Light weight for captions and marginalia. Bold, semi-bold, italic for display only.
- The book's own spec: A4, 32 fields, 2 text columns, 4 caption columns, titles 12 pt semi-bold, text 9/12, captions 7/8.
- The size ladder shown: 6 8 9 10 12 14 18 24 30 36 48 60. Leading demo at 20 pt: 4 8 16 32, a doubling scale.

## 4. Whitespace

- Empty fields are designed output, not leftover. Miletus left grid fields empty for temples. Leave a cell empty rather than shrink a gap.
- Ragged column bottoms are fine. Do not force equal heights.
- Titles get a rest zone: a reserved empty band above the type area, kept even when there is no title.
- Generous margins are part of the image treatment on dark grounds.

## 5. Colour (all the book says; it has no colour theory chapter)

- One accent, flat, functional. Same colour for the same kind of content everywhere.
- Colour carries hierarchy (red captions, blue vs black titles) at the same size.
- Solid tint under a photo is the cheap substitute for 4-colour. Lighter red is more legible than dark.
- Monochrome ground throws the content forward.

## 6. Direct CSS translations

| Book | CSS |
|---|---|
| Type area | one wrapper: max-width plus asymmetric padding, bottom larger than top |
| Columns 2/3/4 subdividing to 4/6/8/16 | 12 tracks (or 4/8), children only span tracks |
| Combination pages, band with a different field count | same tracks, subgrid for the band |
| Gutter, one value | gap from one token, never per-component margins |
| Vertical module = leading | --lh from body line-height; every margin-block and block height an integer multiple; lh and rlh units |
| Captions 2 lines = 1 body line; title 1 line = 2 body lines | every line-height is a divisor or multiple of --lh |
| Image on cap line / descender line | aspect-ratio chosen so height is n x --lh; text-box-trim cap alphabetic where supported |
| Images fill whole fields | grid-column: span n, closed set of allowed spans, no free widths |
| 7 to 10 words per line | max-width 45ch to 75ch on prose; measure in ch or em, never px |
| Narrower column, smaller face | container queries on the column, not viewport media queries |
| Margins 3:5:5:8 | spacing scale 3 5 8 13 21 x base; page bottom padding larger than top |
| Empty field | leave the cell empty; grid-column-start skips, no filler tile |
| Same grid across breakpoints | change track count and gap, never the module |
| Tint vs text edge | padding inside the band, or full-bleed band past the container |
| Coloured text over coloured panel | color: var(--accent) before background highlights |
| Reversed text short, more leading | dark surfaces: raise line-height, cap paragraph length |
| Series with one variable | one stylesheet plus one --accent per section |
| Design manual binding on staff | tokens in code plus a lint or pre-flight check |

## 7. What the book does not give (gaps to fill from other sources)

- Colour theory beyond a functional accent.
- Interaction, motion, states.
- Screen-specific measure: the 30 to 35 cm rule needs re-basing per device.
- Breakpoints. The nearest rule is "same module, more or fewer tracks" (Crystal Palace dense vs Expo 70 open).
