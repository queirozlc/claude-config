---
name: modern-css
description: Use modern CSS features or refactor CSS when the task benefits from them. Check the project's target browsers before selecting newer APIs.
---

# Modern CSS

Preserve the project's styling system, tokens, and browser targets. Prefer native CSS when it meets the requested behavior and support requirements. Do not replace working JavaScript with an unsupported CSS feature merely because it is newer.

Read only the relevant topic:
- [Layout & Responsive Design](references/layout.md)
- [Color & Theming](references/color.md)
- [Typography](references/typography.md)
- [Animations & Motion](references/motion.md)
- [Custom Properties & Advanced Features](references/advanced.md)
- [Architecture & Organization](references/architecture.md)
- [Interactive Components](references/components.md)
- [Form Enhancements](references/forms.md)
- [Visual Effects](references/effects.md)
- [Progressive Enhancement Patterns](references/progressive-enhancement.md)

Verify current support through MDN or the Web Platform Baseline data. Record the source and verification date when support determines the implementation. Use progressive enhancement and a working fallback for unsupported features. Respect reduced motion, contrast preferences, keyboard access, and readable states.

For intrinsic-size calculations, `calc-size()` needs a basis and calculation, for example `calc-size(auto, size)`. For a simple transition to an intrinsic size, consider `interpolate-size: allow-keywords` and verify support. See [MDN calc-size](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/calc-size).

Examples are reference material, not a production checklist. Do not apply every feature to one component. Verify the changed behavior in relevant browsers.

Historical conference material is not a current browser-support reference. Check current syntax and support before reusing older examples.
