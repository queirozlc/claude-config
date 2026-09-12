# Architecture & Organization

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Cascade Layers
```css
@layer reset, design-system, components, utilities;

@import "open-props/colors" layer(design-system);
@import "components/nav/base.css" layer(components.nav);

@layer components.nav.primary {
  nav {
    position: sticky;
    inset-block-start: 0;
  }
}
```

Benefits:
- Import third-party CSS with lower specificity
- Organize styles by concern, not selector weight
- Nested layers create clear hierarchies

---
