---
name: frontend-design
description: Design system patterns — component architecture, Tailwind mastery, visual hierarchy, and responsive layouts
---

## Overview

Frontend design skill for building beautiful, consistent UIs. Covers design systems, Tailwind CSS, component patterns, spacing, typography, color theory, and responsive design.

## Capabilities

- Build design systems with reusable component patterns
- Master Tailwind CSS utilities and custom configurations
- Apply visual hierarchy, spacing, and typography principles
- Create responsive layouts with mobile-first approach
- Implement dark mode and theme switching

## When to Use

- Starting a new frontend project and need design system
- Existing UI looks inconsistent or unprofessional
- Need to implement responsive design across devices
- Building component library for team reuse

## Pseudo Code

### Design Token System
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a8a' },
        neutral: { 50: '#fafafa', 500: '#737373', 900: '#171717' }
      },
      spacing: { '18': '4.5rem', '88': '22rem' },
      fontSize: { 'display': ['3rem', { lineHeight: '1.2', fontWeight: '700' }] }
    }
  }
}
```

### Component Pattern
```jsx
// Button with variants
const Button = ({ variant = 'primary', size = 'md', children, ...props }) => {
  const styles = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600',
    secondary: 'bg-neutral-100 text-neutral-900 hover:bg-neutral-200',
    ghost: 'bg-transparent hover:bg-neutral-100'
  }
  const sizes = { sm: 'px-3 py-1.5 text-sm', md: 'px-4 py-2', lg: 'px-6 py-3 text-lg' }
  return <button className={`${styles[variant]} ${sizes[size]} rounded-lg transition`} {...props}>{children}</button>
}
```

## Common Patterns

- **8px grid**: All spacing multiples of 8px for visual consistency
- **3 font sizes max**: Display, body, caption — don't exceed 3 sizes
- **Color scale**: 50-900 scale for each color (50 = lightest, 900 = darkest)
- **Mobile-first**: Write mobile styles by default, add breakpoints for larger screens
