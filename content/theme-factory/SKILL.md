---
name: theme-factory
description: Generate and apply professional color themes, typography systems, and design tokens for applications. Create consistent visual identities across platforms.
domain: content
tags:
- design
- themes
- colors
- typography
- design-tokens
- branding
---

# Theme Factory

## When to Use

- When creating a new visual theme or color palette
- When defining design tokens for a design system
- When rebranding an application
- When ensuring visual consistency across platforms

## When NOT to Use

- For implementing existing designs (use `frontend-ui-design`)
- For logo design (use image generation skills)
- For content creation (use content skills)

## Overview

Generate professional design systems including color palettes, typography scales, spacing systems, and design tokens. Supports CSS custom properties, Tailwind config, and design token JSON.

## Workflow

1. **Define brand** — Primary color, mood, audience
2. **Generate palette** — Primary, secondary, accent, neutral, semantic colors
3. **Define typography** — Font stack, scale, line heights, weights
4. **Create tokens** — Design token JSON for cross-platform use
5. **Export** — CSS variables, Tailwind config, Figma tokens

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will pick colors by eye" | Systematic color theory ensures accessibility and harmony |
| "One font is enough" | A type scale (headings, body, caption) creates visual hierarchy |
| "Hardcode colors in components" | Design tokens enable theme switching and dark mode |

## Code Example (CSS Custom Properties)

```css
:root {
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-base: 1rem;
  --font-size-2xl: 1.5rem;
  --space-1: 0.25rem;
  --space-4: 1rem;
  --space-8: 2rem;

  [data-theme="dark"] {
    --color-primary-500: #60a5fa;
    --color-bg: #0f172a;
    --color-text: #f8fafc;
  }
}
```

## Verification

- [ ] Color palette passes WCAG contrast checks
- [ ] Typography scale is harmonious (1.25 ratio)
- [ ] Design tokens work in both light and dark mode
- [ ] Tokens export correctly to CSS/Tailwind/JSON

