# Interactive Components

Examples retained from the local skill. Availability labels are not a browser-support guarantee. Verify the installed browser targets and current documentation before use. The calc-size syntax was corrected on 12 September 2026; other examples have not received a complete standards audit.


### Dialog
```html
<dialog id="modal">
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="confirm">Confirm</button>
  </form>
</dialog>

<button commandfor="modal" command="showModal">Open</button>
<button commandfor="modal" command="close">Close</button>
```

**Check target-browser support:** `closedby` attribute enables light-dismiss behavior

### Popover
```html
<button popovertarget="menu">Show Menu</button>
<div popover id="menu">...</div>
```

**popover=hint:** Ephemeral tooltips that don't dismiss other popovers

```css
[popover] {
  transition:
    display .5s allow-discrete,
    overlay .5s allow-discrete,
    opacity .5s;

  @starting-style {
    &:popover-open {
      opacity: 0;
    }
  }
}
```

### Anchor Positioning
```css
.tooltip-anchor {
  anchor-name: --tooltip;
}

.tooltip[popover] {
  position-anchor: --tooltip;
  position-area: block-start;
  position-try-fallbacks: flip-block;
  position-try-order: most-height;
}
```

**Related APIs:** `anchor()` is a function; `::scroll-button()` and `::scroll-marker()` are pseudo-elements.

### Exclusive Accordion
```html
<details name="accordion">...</details>
<details name="accordion">...</details>
<!-- Only one can be open at a time -->
```

### Customizable Select
```css
select {
  appearance: base-select; /* Full CSS control */
}

/* Style options with rich HTML */
select option::before {
  content: ""; /* Can include images, icons */
}
```

### Search Element
```html
<search>
  <form>
    <input type="search" name="q">
    <button type="submit">Search</button>
  </form>
</search>
```

---
