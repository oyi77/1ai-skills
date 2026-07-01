---
name: frontend-ui-design
description: Design and build production-grade UI components using React, Vue, or vanilla HTML/CSS. Create responsive layouts, design systems, and accessible interfaces. Use when designing and build production-grade ui components using react, vue, or.
domain: content
tags:
- design
- frontend
- ui
- react
- css
- components
- responsive
---

# Frontend Ui Design

## When to Use
**Trigger phrases:**
- "frontend ui design"
- "Design and build production-grade UI components using React, Vue, or vanilla HTM"


- When building UI components or pages from scratch
- When creating a design system or component library
- When implementing responsive layouts
- When improving accessibility of existing UI

## When NOT to Use

- For backend logic (use backend skills)
- For database design (use data skills)
- For mobile-native apps (use mobile development skills)

## Overview

Build production-quality frontend interfaces with modern frameworks. Covers component architecture, responsive design, accessibility (WCAG), and design system patterns.

## Workflow

1. **Define requirements** — User stories, wireframes, breakpoints
2. **Choose architecture** — Component hierarchy, state management
3. **Build components** — Atomic design (atoms, molecules, organisms)
4. **Apply styling** — CSS modules or Tailwind, responsive breakpoints
5. **Ensure accessibility** — ARIA labels, keyboard navigation, color contrast
6. **Test** — Visual regression, interaction testing, cross-browser

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Just use a UI library" | Libraries need customization; understanding CSS is non-negotiable |
| "Mobile-first is optional" | 60%+ traffic is mobile — responsive is not optional |
| "Accessibility is nice-to-have" | It is legally required in many jurisdictions and affects SEO |

## Code Example (React)

```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export function Button({ variant, size, children, onClick, disabled }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
}
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run frontend ui design workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] Renders correctly at all breakpoints (mobile, tablet, desktop)
- [ ] Passes WCAG 2.1 AA color contrast checks
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Screen reader compatible (ARIA labels)

