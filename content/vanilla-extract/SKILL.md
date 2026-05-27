---
name: vanilla-extract
description: Vanilla Extract zero-runtime CSS-in-JS — type-safe styles, Sprinkles, Recipes, themes
---

## Overview

Vanilla Extract is a zero-runtime CSS-in-JS library. Styles are written in TypeScript and compiled to static CSS at build time — no runtime overhead, full type safety, and excellent performance.

## Capabilities

- Zero-runtime CSS (compiled at build time)
- Type-safe style definitions in TypeScript
- Sprinkles for utility-first responsive styles
- Recipes for component variants
- Theme contracts for type-safe theming
- Works with Vite, Webpack, esbuild, Next.js

## When to Use

- Want CSS-in-JS without runtime performance cost
- Need type-safe styles in TypeScript projects
- Building design systems with variant-heavy components
- Migrating from styled-components to zero-runtime

## Pseudo Code

### Basic Styles
```ts
// styles.css.ts
import { style } from "@vanilla-extract/css"

export const container = style({
  padding: "24px",
  borderRadius: "8px",
  backgroundColor: "#f8fafc",
  ":hover": { backgroundColor: "#f1f5f9" },
  "@media": {
    "(max-width: 768px)": { padding: "16px" },
  },
})
```

### Theme
```ts
// theme.css.ts
import { createTheme, createThemeContract } from "@vanilla-extract/css"

export const vars = createThemeContract({
  color: { primary: null, background: null, text: null },
  space: { sm: null, md: null, lg: null },
})

export const lightTheme = createTheme(vars, {
  color: { primary: "#3b82f6", background: "#ffffff", text: "#1f2937" },
  space: { sm: "8px", md: "16px", lg: "24px" },
})

export const darkTheme = createTheme(vars, {
  color: { primary: "#60a5fa", background: "#111827", text: "#f9fafb" },
  space: { sm: "8px", md: "16px", lg: "24px" },
})
```

### Recipes (Variants)
```ts
// button.css.ts
import { recipe } from "@vanilla-extract/recipes"

export const button = recipe({
  base: {
    padding: "8px 16px",
    borderRadius: "6px",
    fontWeight: 600,
  },
  variants: {
    variant: {
      primary: { backgroundColor: "#3b82f6", color: "white" },
      outline: { border: "1px solid #3b82f6", color: "#3b82f6" },
    },
    size: {
      sm: { fontSize: "14px", padding: "4px 8px" },
      md: { fontSize: "16px" },
      lg: { fontSize: "18px", padding: "12px 24px" },
    },
  },
  defaultVariants: { variant: "primary", size: "md" },
})
```

### Sprinkles (Utility Props)
```ts
// sprinkles.css.ts
import { defineProperties, createSprinkles } from "@vanilla-extract/sprinkles"

const responsiveProperties = defineProperties({
  conditions: {
    mobile: {},
    tablet: { "@media": "(min-width: 768px)" },
    desktop: { "@media": "(min-width: 1024px)" },
  },
  defaultCondition: "mobile",
  properties: {
    display: ["none", "flex", "block"],
    padding: { sm: "8px", md: "16px", lg: "24px" },
    gap: { sm: "8px", md: "16px", lg: "24px" },
  },
})

export const sprinkles = createSprinkles(responsiveProperties)
```

## Common Patterns

- **Composition**: `className={clsx(container, isActive && active)}`
- **Global styles**: `globalStyle("body", { margin: 0 })`
- **Keyframes**: `const fadeIn = keyframes({ from: { opacity: 0 }, to: { opacity: 1 } })`
- **Theme vars**: Always use theme contract — type-safe, enforced consistency
- **Recipes over variants**: Use `recipe()` for multi-variant components
