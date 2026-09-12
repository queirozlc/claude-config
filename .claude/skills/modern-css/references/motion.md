# Animations & Motion

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Scroll-Driven Animation
```css
/* Animate on scroll position */
.parallax {
  animation: slide-up linear both;
  animation-timeline: scroll();
}

/* Animate on viewport intersection */
.fade-in {
  animation: fade linear both;
  animation-timeline: view();
  animation-range: cover -75cqi contain 20cqi;
}
```

### View Transitions
**Support:** Verify current same-document and cross-document support separately for the target browsers.
Cross-document transitions are in Limited Availability (Chrome/Safari 18.2+).

```css
@view-transition {
  navigation: auto; /* Automatically animate page transitions (MPAs) */
}

nav {
  view-transition-name: --persist-nav; /* Persist specific elements */
  view-transition-class: --site-header; /* Group transitions with classes */
}

/* Style the active transition */
html:active-view-transition {
  overflow: hidden;
}
```

**Nested View Transition Groups:** Preserve 3D transforms and clipping during transitions.

### Advanced Easing with linear()
```css
.springy {
  --spring: linear(
    0, 0.14 4%, 0.94 17%, 1.15 24% 30%, 1.02 43%, 0.98 51%, 1 77%, 1
  );
  transition: transform 1s var(--spring);
}
```

### @starting-style
```css
.dialog {
  transition: opacity .5s, scale .5s;

  @starting-style {
    opacity: 0;
    scale: 1.1;
  }
}
```

---
