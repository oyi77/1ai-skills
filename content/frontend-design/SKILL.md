---
name: frontend-design
description: Use when designing frontend systems — component architecture, Tailwind mastery, visual hierarchy, and responsive layouts. Covers design-system patterns, component composition, and responsive implementation.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- design
- digital-content
- frontend
- media
version: 1.1.0
triggers:
- "frontend-design"
- "ui design"
- "component design"
- "redesign page"
- "revamp design"
- "design task"
- "ui design work"
category: content
---
## Overview

Frontend design skill for building beautiful, consistent UIs. Covers design systems, Tailwind CSS, component patterns, spacing, typography, color theory, and responsive design. This skill bridges visual design and engineering: component architecture and design tokens through CSS implementation, accessibility auditing, and design system distribution.

## Capabilities

- Build design systems with reusable component patterns
- Master Tailwind CSS utilities and custom configurations
- Apply visual hierarchy, spacing, and typography principles
- Create responsive layouts with mobile-first approach
- Implement dark mode and theme switching

## When to Use

**Trigger phrases:**
- "frontend design"
- "Design system patterns — component architecture, Tailwind mastery, visual hierarchy"
- "build a UI", "create a component", "design a page"
- "Tailwind classes", "shadcn setup", "Radix primitives"

**Use when:**
- Starting a new frontend project and need a design system
- Existing UI looks inconsistent or unprofessional
- Need to implement responsive design across devices
- Building a component library for team reuse
- Auditing WCAG compliance in interactive elements
- Implementing dark/light theme switching

## When NOT to Use

- Backend API design or database modeling (use `api-design` / `database-migration`)
- Mobile-native app development outside WebView wrappers (use platform SDKs)
- Pure CSS animation timing (use `motion-dev`)
- Static HTML pages without runtime interactivity (use Astro/Eleventy guides)

## Design Token System

Single source of truth for visual decisions. Map every visual property to a semantic token so themes swap atomically.

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

## Component Pattern

Compose from primitives. Prefer composition over inheritance; each component owns one responsibility.

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
- **Token-driven styling**: Never hardcode hex or px; map every visual property to a semantic token

## Setup & Configuration

```bash
# Create React + TypeScript project with Vite
npm create vite@latest my-app -- --template react-ts
cd my-app

# Install Tailwind CSS v4 with Vite plugin
npm install tailwindcss @tailwindcss/vite

# Install Storybook for component workbench
npx storybook@latest init

# Chromatic for visual regression in CI
npm install -D chromatic
```

For Vue projects:
```bash
npm create vue@latest my-vue-app
cd my-vue-app
npm install unocss
```

## Process

1. **Prepare** — Gather brand assets, wireframes, and content strategy. Set up toolchain (Vite, Tailwind, Storybook). Document component hierarchy with a tree diagram before writing code.
2. **Design tokens** — Establish color palette, typography scale, spacing units, and shadows as CSS custom properties or Tailwind config. Verify contrast ratios meet WCAG AA.
3. **Component build** — Layer components via atomic design (atoms → molecules → organisms). Implement responsive variants and dark mode.
4. **Quality check** — Run Lighthouse, AXE DevTools, keyboard navigation audit, and cross-browser visual diff.
5. **Deliver and document** — Export component library with usage documentation, Storybook preview, and live demo URL.

## Common Issues & Troubleshooting

| Problem | Root Cause | Solution |
|---|---|---|
| CSS specificity conflicts | Nested selectors and !important overrides | Use BEM naming, CSS Modules, or Tailwind utility classes |
| Layout breaks on mobile | Fixed px widths or missing viewport meta | Use relative units (rem, %, vw) and mobile-first media queries |
| Components re-render unexpectedly | Missing React keys or unstable callback references | Add stable keys to lists, memoize callbacks with useCallback |
| Color contrast fails WCAG AA | Insufficient luminance difference against background | Use WCAG contrast calculators; maintain minimum 4.5:1 ratio for normal text |
| Screen reader skips interactive element | Missing or incorrect ARIA role or attribute | Use semantic HTML where possible; add aria-label for visual-only labels |
| Hover styles don't work on touch devices | :hover-dependent interactions without touch fallback | Use @media (hover: hover) to separate pointer and touch interactions |

## Verification

- [ ] All components render correctly at breakpoints: 320px, 768px, 1024px, 1440px
- [ ] Color contrast passes WCAG 2.1 AA minimum (4.5:1 for normal text, 3:1 for large)
- [ ] Keyboard navigation covers Tab order, visible focus indicators, Enter/Space activation, Escape close
- [ ] Screen reader announces dynamic content changes via ARIA live regions
- [ ] CSS architecture has no !important overrides or specificity battles
- [ ] Design tokens defined in a single source of truth (CSS custom properties or Tailwind config)
- [ ] Components maintain consistent spacing using the established scale (4px/8px base)
- [ ] Lighthouse performance score >= 90 for the rendered page

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Just use a UI library like MUI or Chakra" | Libraries need deep customization for brand identity; CSS architecture and component composition skills remain essential |
| "Mobile-first is optional for our audience" | 60%+ of global traffic is mobile — responsive design is table stakes, not optional |
| "Accessibility is a nice-to-have add-on" | WCAG compliance is legally required in many jurisdictions and directly affects SEO rankings |
| "CSS is easy, I will just write what works" | Poor CSS architecture leads to specificity wars, !important overrides, and unmaintainable stylesheets |
| "We don't need a design system for a small project" | Even small projects benefit from consistent spacing, typography, and color tokens — prevents tech debt from day one |
| "State management libraries solve everything" | Poor component architecture causes prop-drilling and re-render issues that no state library can fix |

## Video / Motion Graphics

Typography hierarchy, spacing rhythm, and visual hierarchy apply directly to [Remotion](../video/remotion/SKILL.md) video frames. Key difference: video has fixed dimensions (1920×1080), no responsive design. Text must be larger — main headline ≥84px, supporting ≥44px at 1080p.

## Sub-Skills & Specialized Playbooks

| Sub-Skill | Trigger / Kasus Penggunaan | Berkas Referensi |
| :--- | :--- | :--- |
| `storybook-ui` | Developing, testing, and documenting isolated UI components with stories, controls, accessibility, and visual regression | [SKILL.md](../storybook-ui/SKILL.md) |
| `frontend-ui-design` | Production-grade UI component architecture, responsive grids, WCAG accessibility, cross-browser compat, CSS specificity battles | [SKILL.md](../../_demoted/frontend-ui-design/SKILL.md) |
