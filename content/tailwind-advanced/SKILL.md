---
name: tailwind-advanced
description: Advanced Tailwind CSS — custom plugins, JIT, container queries, animations, dark mode, design systems
---

## Overview

Advanced Tailwind CSS patterns for production applications — custom plugins, container queries, complex animations, design system integration, and performance optimization beyond basic utility classes.

## Capabilities

- Custom Tailwind plugins for project-specific utilities
- Container queries for component-level responsive design
- Complex animations with keyframes and transitions
- Dark mode with class strategy and system preference
- Design system tokens via CSS custom properties
- JIT compiler optimization and purge strategies

## When to Use

- Building a design system on top of Tailwind
- Need component-scoped responsive design (container queries)
- Complex animations beyond basic Tailwind utilities
- Custom utilities that repeat across the project

## Pseudo Code

### Custom Plugin
```js
// tailwind.config.js
const plugin = require("tailwindcss/plugin")

module.exports = {
  plugins: [
    plugin(function ({ addUtilities, addComponents, theme }) {
      addUtilities({
        ".text-gradient": {
          "background-clip": "text",
          "-webkit-text-fill-color": "transparent",
          "background-image": `linear-gradient(to right, ${theme("colors.blue.500")}, ${theme("colors.purple.500")})`,
        },
      })
      addComponents({
        ".card-elevated": {
          padding: theme("spacing.6"),
          "border-radius": theme("borderRadius.lg"),
          "box-shadow": theme("boxShadow.xl"),
          "background-color": theme("colors.white"),
        },
      })
    }),
  ],
}
```

### Container Queries
```html
<div class="@container">
  <div class="@lg:grid @lg:grid-cols-3 @sm:block">
    <!-- Responsive to container, not viewport -->
  </div>
</div>
```

### Custom Animations
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        "fade-in-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "fade-in-up": "fade-in-up 0.5s ease-out",
        shimmer: "shimmer 2s infinite linear",
      },
    },
  },
}
```

### Dark Mode with CSS Variables
```css
@layer base {
  :root {
    --bg-primary: 255 255 255;
    --text-primary: 15 23 42;
  }
  .dark {
    --bg-primary: 15 23 42;
    --text-primary: 248 250 252;
  }
}
```
```html
<div class="bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))]">
```

## Common Patterns

- **Arbitrary values**: `w-[342px]`, `bg-[#1da1f2]`, `grid-cols-[200px_1fr]`
- **Group/peer**: `group-hover:opacity-100`, `peer-checked:bg-blue-500`
- **Variant stacking**: `dark:md:hover:bg-gray-800`
- **@apply sparingly**: Only for repeated patterns in component CSS
- **Content config**: `content: ["./src/**/*.{ts,tsx}"]` for proper purging
