---
name: vanilla-extract
description: Vanilla Extract zero-runtime CSS-in-JS — type-safe styles, Sprinkles, Recipes, themes
domain: content
tags:
- content-creation
- digital-content
- extract
- media
- vanilla
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

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The vanilla-extract workflow follows a standard pipeline pattern.

Core flow:
```
# vanilla-extract primary flow
input = prepare(raw_data)
result = process(input, config={extract, recipes, runtime, safe, sprinkles})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# vanilla-extract primary flow
input = prepare(raw_data)
result = process(input, config={extract, recipes, runtime, safe, sprinkles})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


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

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior
