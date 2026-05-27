---
name: responsive-design
description: Mobile-first responsive design — breakpoints, fluid typography, container queries, and touch optimization
---

## Overview

Responsive design that works across all devices. Covers mobile-first approach, breakpoint strategy, fluid typography, container queries, touch targets, and performance optimization.

## Capabilities

- Design mobile-first layouts that scale to desktop
- Implement fluid typography with clamp()
- Use container queries for component-level responsiveness
- Optimize touch targets for mobile (44px minimum)
- Handle responsive images and lazy loading

## When to Use

- Building a new responsive layout
- Existing layout breaks on certain screen sizes
- Mobile traffic is >50% but mobile experience is poor
- Need component-level responsive behavior

## Pseudo Code

### Mobile-First CSS
```css
/* Mobile first (default) */
.grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }

/* Tablet */
@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); gap: 2rem; }
}
```

### Fluid Typography
```css
h1 { font-size: clamp(1.75rem, 4vw, 3rem); }
body { font-size: clamp(1rem, 2vw, 1.125rem); }
```

### Container Queries
```css
.card-container { container-type: inline-size; }
@container (min-width: 400px) {
  .card { display: flex; gap: 1rem; }
}
```

## Common Patterns

- **Mobile first**: Write mobile styles by default, add `min-width` media queries
- **3 breakpoints**: Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)
- **44px touch targets**: All interactive elements minimum 44x44px on mobile
- **Fluid everything**: Use `clamp()` for font-size, spacing, and widths
