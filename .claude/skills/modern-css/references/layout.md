# Layout & Responsive Design

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Container Queries
```css
.card {
  container: --my-card / inline-size;
}

@container --my-card (width < 40ch) {
  /* Component-based responsive design */
}

@container (20ch < width < 50ch) {
  /* Range syntax */
}
```

**Container units:** `cqi`, `cqb`, `cqw`, `cqh` - size relative to container dimensions

**Anchored container queries:** Style positioned elements based on anchor fallback state
```css
.tooltip {
  container-type: anchored;
}

@container anchored(top) {
  /* Styles when positioned at top */
}
```

### Media Query Range Syntax
```css
@media (width <= 1024px) { }
@media (360px < width < 1024px) { }
```


### Grid Enhancements
- **Subgrid:** Inherit parent grid lines for nested layouts
- **Masonry:** `display: grid-lanes` for Pinterest-style layouts with logical tab order. (Previously proposed as `grid-template-rows: masonry`).

---
