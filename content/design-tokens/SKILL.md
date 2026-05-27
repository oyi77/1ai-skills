---
name: design-tokens
description: Design token systems — color, typography, spacing, and theme architecture for consistent design
---

## Overview

Design tokens are the single source of truth for design decisions. This skill covers token taxonomy, color scales, typography, spacing systems, dark mode, and implementation via CSS custom properties and Tailwind.

## Capabilities

- Define color scales with semantic naming (primary, success, error)
- Build typography scales with consistent line heights and weights
- Create spacing systems based on a base unit (4px or 8px)
- Implement dark mode via token swapping
- Export tokens to CSS custom properties, Tailwind, and Figma

## When to Use

- Starting a new design system from scratch
- Inconsistencies in colors, fonts, or spacing across the app
- Need to support dark mode or multiple themes
- Syncing design decisions between Figma and code

## Pseudo Code

### Token Definition
```json
{
  "color": {
    "primary": { "50": "#eff6ff", "500": "#3b82f6", "900": "#1e3a8a" },
    "success": { "500": "#22c55e" },
    "error": { "500": "#ef4444" }
  },
  "spacing": { "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px" },
  "fontSize": { "xs": "12px", "sm": "14px", "base": "16px", "lg": "18px", "xl": "24px" }
}
```

### CSS Custom Properties
```css
:root {
  --color-primary: var(--color-primary-500);
  --color-bg: #ffffff;
  --color-text: #171717;
}
[data-theme="dark"] {
  --color-bg: #0a0a0a;
  --color-text: #fafafa;
}
```

## Common Patterns

- **Semantic naming**: Use `primary`, `success`, `error` — not `blue-500`, `green-500`
- **Scale by 100s**: Color shades: 50, 100, 200, ..., 900
- **4px base unit**: All spacing multiples of 4px for rhythm
- **Dark mode swap**: Swap 50↔900, 100↔800, etc.
