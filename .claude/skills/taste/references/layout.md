# Layout

The special sauce of the best SaaS apps is not a composition. It is a measure and a shell that never move. This file gives both, plus the construction order from the book.

## 1. Shell anatomy (app UI)

Three zones. Widths are constants.

| Zone | Width | Content |
|---|---|---|
| Rail | 220 to 260 px, collapsible to 56 px icon rail | Workspace switcher, primary nav grouped by section labels, footer slot for trial, upgrade, whats-new. |
| Canvas | Fills the rest. Content inside is clamped to a measure. | Page title band, then sections. |
| Inspector | 280 to 360 px, optional, toggleable | Properties of the selected item. Never permanent on small screens. |

Observed: Linear settings put a 640 px column inside a 1440 px window. Notion pages use about 700 px. Stripe dashboard uses a 12-track canvas about 1100 px wide. In every case more than a third of the viewport is margin. Slop fills the viewport. The experts spend space on margins.

Rules:
- Canvas content width comes from the body type, not from the viewport. 60 to 75ch for prose, 640 to 720 px for settings and forms, up to 1200 px for dashboards.
- Everything anchors top-left to the column edge. Centering is for onboarding, empty states, auth, modals. Never for app content.
- The page title sits in a reserved band at the top of the canvas. Keep the band even when the title is short.
- Zone widths do not change at breakpoints. The rail collapses, the inspector becomes a sheet, the canvas keeps its measure.

## 2. Inside the canvas: the field grid

The book's model, translated.

- 12 tracks. Allowed spans: 3, 4, 6, 8, 12. A dashboard card is 4 or 6. A hero card is 12 or 8 plus 4. Never 5, never 7, never a percentage.
- One gutter value for `gap`. Do not add margins on children.
- Vertical rhythm in whole line units. Section spacing: title, one-line description, then the block. Between sections: 2 line units. Between blocks inside a section: 1 line unit.
- Rows inside a card are one line unit tall plus padding, stacked with hairline dividers, no gaps. Grouping by surface, not by gap.
- Empty cells are legal. Leave a cell empty rather than stretch a card or add filler.
- One dominant element per screen: a large title, a large number, one hero card. Many equal cards read as dull.
- Discipline: two or three distinct card sizes per screen. Not eight.

Section skeleton:

```html
<section class="grid grid-cols-12 gap-6">
  <header class="col-span-12">
    <h2 class="text-title">Billing</h2>
    <p class="text-body text-secondary">Invoices, plan and payment method.</p>
  </header>
  <div class="col-span-6 rounded-lg border border-line bg-raised divide-y divide-line">
    <div class="flex items-center justify-between px-4 py-3">…row…</div>
    <div class="flex items-center justify-between px-4 py-3">…row…</div>
  </div>
  <div class="col-span-6 …">…</div>
</section>
```

## 3. Marketing and content pages

Different rules from app UI.

- One column of measure for text, 60 to 75ch. Full-bleed only for images and colored bands, and rarely.
- Asymmetric page frame. Bottom padding larger than top. Book ratio inner 1 : head 1.5 : outer 2 : foot 3, or 3 : 5 : 5 : 8.
- Hierarchy by whitespace first, then weight, then size. Whitespace is the cheapest signal and the one slop forgets.
- Max two consecutive image-plus-text split sections. The third breaks the pattern with a full-width, a stack, or a grid.
- A feature grid has exactly as many cells as features. Cells are on allowed spans and at least two of them differ in size or fill.

## 4. Mobile

Space is expensive. Each component pays rent.

- One column. The rail becomes a bottom tab bar with 3 to 5 items, or a sheet.
- The measure rule still holds: body 16 px, 16 to 20 px side padding, which lands near 40ch.
- Primary action in the thumb zone. Not at the very top, not below a long scroll.
- Dense rows become full-width list rows, one line unit plus padding each.
- Cards lose their borders and become sections separated by whitespace. Cards inside cards do not survive on mobile.

## 5. Construction order for a new screen

From the book, in sequence.

1. Inventory: what text, what data, what images, how many of each, which are large.
2. Priority list: the one primary action, the proof before it, then the rest.
3. Pick the shell zone and the measure.
4. Pick the spans for each block from the allowed set.
5. Lay the vertical rhythm: sections, blocks, rows in whole line units.
6. Place the dominant element.
7. Sketch small at the final proportion. Cut to one candidate. Build once.

## 6. Breakpoints

Keep the module, change the count. Tracks go 4 on mobile, 8 on tablet, 12 on desktop. The gutter and the line unit stay constant. Component widths are never set at breakpoints, only spans.
