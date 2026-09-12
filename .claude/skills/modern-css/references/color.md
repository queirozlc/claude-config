# Color & Theming

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Color Scheme & Light-Dark Function
```css
:root {
  color-scheme: light dark;
  --surface-1: light-dark(white, #222);
  --text-1: light-dark(#222, #fff);
}
```

### Modern Color Spaces
```css
/* OKLCH: uniform brightness, P3+ colors */
.vibrant {
  background: oklch(72% 75% 330);
}

/* Display-P3 for HDR displays */
@media (dynamic-range: high) {
  .neon {
    --neon-red: color(display-p3 1 0 0);
  }
}

/* Better gradients with in oklch */
.gradient {
  background: linear-gradient(
    to right in oklch,
    color(display-p3 1 0 .5),
    color(display-p3 0 1 1)
  );
}
```

### Color Manipulation
```css
/* color-mix() */
.lighten {
  background: color-mix(in oklab, var(--brand), white);
}

/* Relative color syntax */
.lighter {
  background: oklch(from blue calc(l + .25) c h);
  background: oklch(from blue 75% c h); /* Set to specific lightness */
}

.semi-transparent {
  background: oklch(from var(--color) l c h / 50%);
}

.complementary {
  background: hsl(from blue calc(h + 180) s l);
}
```

### Accent Color
```css
:root {
  accent-color: hotpink; /* Tints checkboxes, radios, range inputs */
}
```

---
