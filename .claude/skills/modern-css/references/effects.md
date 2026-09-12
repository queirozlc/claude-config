# Visual Effects

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Scrollbar Styling
```css
.custom-scrollbar {
  scrollbar-color: hotpink transparent;
  scrollbar-width: thin;
}
```

### Shape Function
```css
.complex-clip {
  clip-path: shape(
    from 0% 0%,
    curve by 50% 25% via 25% 50%,
    line to 100% 100%
  );
}
```

### Corner Shapes
```css
.fancy-corners {
  corner-shape: squircle;
  corner-shape: notch;
  corner-shape: scoop;
  corner-shape: superellipse(0.7);
}
```

---
