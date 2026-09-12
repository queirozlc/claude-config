# Progressive Enhancement Patterns

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Feature Detection
```css
@supports (animation-timeline: view()) {
  .fade-in {
    animation: fade linear both;
    animation-timeline: view();
  }
}

@supports (container-type: inline-size) {
  .responsive-card {
    container-type: inline-size;
  }
}
```

### Respect User Preferences
```css
@media (prefers-reduced-motion: no-preference) {
  .animated {
    animation: slide 1s ease;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface: #222;
  }
}

@media (prefers-contrast: more) {
  .text {
    font-weight: 600;
  }
}
```

---
