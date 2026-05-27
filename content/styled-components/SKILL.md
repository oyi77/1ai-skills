---
name: styled-components
description: styled-components CSS-in-JS — tagged templates, theming, props, animations, SSR, performance
---

## Overview

styled-components enables CSS-in-JS with tagged template literals. Components are styled directly in JavaScript with access to props, themes, and dynamic values. Supports SSR and tree-shaking.

## Capabilities

- Tagged template literal syntax for styling
- Dynamic styles via props
- ThemeProvider for global theming
- Server-side rendering with ServerStyleSheet
- Keyframe animations
- Extending and composing components
- Transient props ($prefix) to avoid DOM forwarding

## When to Use

- React projects needing scoped, dynamic CSS
- Component libraries with prop-driven styles
- Server-side rendered React apps (Next.js)
- Theming with runtime color/mode switching

## Pseudo Code

### Basic Usage
```tsx
import styled from "styled-components"

const Button = styled.button`
  background: ${(props) => props.$primary ? "#3b82f6" : "#e5e7eb"};
  color: ${(props) => props.$primary ? "white" : "#374151"};
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  &:hover { opacity: 0.9; }
`

// Usage: <Button $primary>Click</Button>
```

### Theme Provider
```tsx
import { ThemeProvider } from "styled-components"

const theme = {
  colors: {
    primary: "#3b82f6",
    background: "#ffffff",
    text: "#1f2937",
  },
  spacing: { sm: "8px", md: "16px", lg: "24px" },
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <MyApp />
    </ThemeProvider>
  )
}
```

### Theme Access
```tsx
const Card = styled.div`
  background: ${({ theme }) => theme.colors.background};
  padding: ${({ theme }) => theme.spacing.md};
  color: ${({ theme }) => theme.colors.text};
`
```

### Extending Components
```tsx
const PrimaryButton = styled(Button)`
  background: #3b82f6;
  color: white;
  font-weight: 600;
`
```

### Keyframes
```tsx
import { keyframes } from "styled-components"

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`

const AnimatedDiv = styled.div`
  animation: ${fadeIn} 0.3s ease-out;
`
```

## Common Patterns

- **Transient props**: Use `$` prefix (`$primary`, `$size`) to prevent DOM forwarding
- **attrs**: `styled.input.attrs({ type: "text" })` for default attributes
- **Global styles**: `createGlobalStyle` for CSS reset and global rules
- **Composition**: `const StyledLink = styled(Link)` for React Router links
- **Performance**: Use `.attrs()` for static values, memoize expensive computations
