# Typography

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Text Wrapping
```css
h1 {
  text-wrap: balance; /* Balanced multi-line headings */
  max-inline-size: 25ch;
}

p {
  text-wrap: pretty; /* No orphans */
  max-inline-size: 50ch;
}
```

### Text Box Trim
```css
h1, p, button {
  text-box: trim-both cap alphabetic; /* Optical vertical centering */
}
```

### Fluid Typography
```css
.heading {
  font-size: clamp(1rem, 1rem + 0.5vw, 2rem); /* Respects user preferences */
}
```

### Dynamic Viewport Units
- `dvh` / `dvw` - Dynamic (accounts for mobile browser UI)
- `svh` / `svw` - Small (smallest possible viewport)
- `lvh` / `lvw` - Large (largest possible viewport)

---
