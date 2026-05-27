---
name: pandacss-styling
description: Panda CSS zero-runtime styling — token system, patterns, recipes, conditions, JSX styles
---

## Overview

Panda CSS is a zero-runtime CSS-in-JS framework with a token system, patterns, recipes, and JSX style props. Generates static CSS at build time with full TypeScript support.

## Capabilities

- Zero-runtime CSS generation
- Design token system with semantic tokens
- Patterns for common layout primitives
- Recipes for component variants
- Conditions for responsive and state styles
- JSX style props for inline styling
- Works with React, Vue, Solid, Qwik

## When to Use

- Want type-safe styling with design tokens
- Need component variants without runtime cost
- Building design systems with consistent tokens
- Using JSX style props for rapid development

## Pseudo Code

### Configuration
```ts
// panda.config.ts
import { defineConfig } from "@pandacss/dev"

export default defineConfig({
  preflight: true,
  include: ["./src/**/*.{ts,tsx}"],
  exclude: [],
  theme: {
    extend: {
      tokens: {
        colors: {
          primary: { value: "#3b82f6" },
          secondary: { value: "#8b5cf6" },
        },
      },
    },
  },
  outdir: "styled-system",
})
```

### Token Usage
```tsx
import { css } from "styled-system/css"

const styles = css({
  color: "primary",
  bg: "gray.100",
  p: "4",
  borderRadius: "md",
  _hover: { bg: "gray.200" },
})
```

### Recipes (Variants)
```ts
// styled-system/recipes/button.ts
import { cva } from "styled-system/css"

export const button = cva({
  base: {
    display: "inline-flex",
    alignItems: "center",
    fontWeight: "semibold",
    borderRadius: "md",
  },
  variants: {
    variant: {
      primary: { bg: "primary", color: "white" },
      outline: { border: "1px solid", borderColor: "primary", color: "primary" },
    },
    size: {
      sm: { px: "3", py: "1.5", fontSize: "sm" },
      md: { px: "4", py: "2" },
      lg: { px: "6", py: "3", fontSize: "lg" },
    },
  },
  defaultVariants: { variant: "primary", size: "md" },
})
```

### JSX Style Props
```tsx
import { styled } from "styled-system/jsx"

export function Card({ children }) {
  return (
    <styled.div
      p="6"
      bg="white"
      rounded="lg"
      shadow="md"
      _dark={{ bg: "gray.800" }}
    >
      {children}
    </styled.div>
  )
}
```

### Patterns (Layout Primitives)
```tsx
import { Stack, HStack, Grid } from "styled-system/jsx"

<Stack gap="4">
  <HStack justify="space-between">
    <styled.span>Title</styled.span>
    <styled.button>Action</styled.button>
  </HStack>
  <Grid columns={3} gap="4">{items}</Grid>
</Stack>
```

## Common Patterns

- **Conditions**: `_hover`, `_focus`, `_dark`, `_motionReduce`, `_sm`, `_md`, `_lg`
- **Semantic tokens**: `colors.primary` → `colors.primary.default`, `colors.primary.subtle`
- **Pattern library**: Stack, HStack, VStack, Grid, Flex, Box, Container
- **Recipe composition**: `cx(button({ variant: "primary" }), extraClass)`
- **Static extraction**: Run `panda codegen` to generate styled-system types
