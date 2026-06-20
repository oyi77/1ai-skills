---
name: css-frameworks
description: CSS framework patterns — Tailwind CSS, Bootstrap, PostCSS, Sass, CSS Modules, CSS-in-JS
domain: development
tags:
- coding
- css
- frameworks
- software-engineering
- testing
---


## Overview

CSS frameworks and methodologies provide structured approaches to styling web applications. This skill covers the most popular frameworks and patterns: Tailwind CSS (utility-first), Bootstrap (component-based), PostCSS (transformation), Sass (preprocessing), CSS Modules (scoped), and CSS-in-JS (styled-components, Emotion).

## Capabilities

- Tailwind CSS utility-first styling with JIT compilation
- Bootstrap responsive grid and component library
- PostCSS plugin pipeline for CSS transformation
- Sass/SCSS variables, mixins, and nesting
- CSS Modules for scoped component styles
- CSS-in-JS with styled-components and Emotion
- CSS custom properties (variables) for theming
- Responsive design patterns (mobile-first)
- Dark mode support
- CSS animations and transitions

## When to Use

- **Tailwind**: Rapid prototyping, design systems, utility-first teams
- **Bootstrap**: Quick admin panels, legacy projects, grid-heavy layouts
- **PostCSS**: CSS transformation pipeline, autoprefixer, custom plugins
- **Sass**: Complex stylesheets, variables, mixins, partials
- **CSS Modules**: Component-scoped styles, avoiding naming conflicts
- **CSS-in-JS**: Dynamic styles, runtime theming, component libraries

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The css-frameworks workflow follows a standard pipeline pattern.

Core flow:
```
# css-frameworks primary flow
input = prepare(raw_data)
result = process(input, config={bootstrap, css, framework, frameworks, modules})
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


### Tailwind CSS
```html
<!-- Responsive card -->
<div class="max-w-sm rounded-lg border bg-white p-6 shadow-md dark:bg-gray-800">
  <h2 class="mb-2 text-2xl font-bold text-gray-900 dark:text-white">Title</h2>
  <p class="mb-4 text-gray-700 dark:text-gray-300">Description text</p>
  <button class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 focus:ring-2 focus:ring-blue-400">
    Action
  </button>
</div>
```

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: { primary: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a5f' } },
      fontFamily: { sans: ['Inter', 'sans-serif'] },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
};
```

### Bootstrap 5
```html
<div class="container">
  <div class="row g-4">
    <div class="col-md-6 col-lg-4">
      <div class="card h-100">
        <img src="..." class="card-img-top" alt="...">
        <div class="card-body">
          <h5 class="card-title">Title</h5>
          <p class="card-text">Description</p>
          <a href="#" class="btn btn-primary">Go</a>
        </div>
      </div>
    </div>
  </div>
</div>
```

### PostCSS
```javascript
// postcss.config.js
module.exports = {
  plugins: {
    'postcss-import': {},
    'tailwindcss/nesting': {},
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {}),
  },
};
```

### Sass/SCSS
```scss
// _variables.scss
$primary: #3b82f6;
$breakpoints: (sm: 640px, md: 768px, lg: 1024px, xl: 1280px);

@mixin respond-to($breakpoint) {
  @media (min-width: map-get($breakpoints, $breakpoint)) {
    @content;
  }
}

// components/_card.scss
.card {
  padding: 1rem;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  
  &__title {
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  &__body {
    margin-top: 0.5rem;
  }
  
  @include respond-to(md) {
    padding: 1.5rem;
  }
}
```

### CSS Modules
```typescript
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
}

.primary {
  background: var(--color-primary);
  color: white;
}

.secondary {
  background: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
}

// Button.tsx
import styles from './Button.module.css';

export function Button({ variant = 'primary', children }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

### styled-components (CSS-in-JS)
```typescript
import styled, { css, ThemeProvider } from 'styled-components';

const Button = styled.button<{ $variant?: string }>`
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 600;
  transition: all 0.2s;

  ${(props) =>
    props.$variant === 'primary' &&
    css`
      background: ${props.theme.colors.primary};
      color: white;
      &:hover { background: ${props.theme.colors.primaryDark}; }
    `}

  ${(props) =>
    props.$variant === 'outline' &&
    css`
      background: transparent;
      border: 2px solid ${props.theme.colors.primary};
      color: ${props.theme.colors.primary};
    `}
`;

const theme = {
  colors: { primary: '#3b82f6', primaryDark: '#2563eb', text: '#1f2937' },
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Button $variant="primary">Click Me</Button>
    </ThemeProvider>
  );
}
```

### Emotion (CSS-in-JS)
```typescript
/** @jsxImportSource @emotion/react */
import { css, Global } from '@emotion/react';

const cardStyle = css`
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  background: white;
`;

const titleStyle = (theme) => css`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${theme.colors.text};
`;

function Card({ title, children, theme }) {
  return (
    <div css={cardStyle}>
      <h2 css={titleStyle(theme)}>{title}</h2>
      {children}
    </div>
  );
}
```

### CSS Custom Properties (Theming)
```css
:root {
  --color-primary: #3b82f6;
  --color-surface: #ffffff;
  --color-text: #1f2937;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --radius: 0.5rem;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
  --color-primary: #60a5fa;
  --color-surface: #1f2937;
  --color-text: #f3f4f6;
}

.card {
  background: var(--color-surface);
  color: var(--color-text);
  padding: var(--spacing-md);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
```

### Responsive Patterns
```css
/* Mobile-first */
.container {
  width: 100%;
  padding: 0 1rem;
  margin: 0 auto;
}

@media (min-width: 640px) { .container { max-width: 640px; } }
@media (min-width: 768px) { .container { max-width: 768px; } }
@media (min-width: 1024px) { .container { max-width: 1024px; } }

/* Container queries (modern) */
@container (min-width: 400px) {
  .card { display: flex; gap: 1rem; }
}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Tailwind not working` | Missing content paths | Check `tailwind.config.js` content array |
| `Styles not scoped` | Wrong CSS Modules import | Use `import styles from './file.module.css'` |
| `Sass compilation error` | Syntax or import issue | Check `_partial` naming and `@use` syntax |
| `styled-components SSR flicker` | Missing ServerStyleSheet | Use `ServerStyleSheet` in SSR setup |
| `PostCSS not processing` | Missing plugin or config | Check `postcss.config.js` |

## Common Patterns

Proven patterns for css-frameworks usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Dark Mode Toggle
```javascript
// Toggle dark mode
document.documentElement.classList.toggle('dark');
localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
```

### Responsive Grid (CSS Grid)
```css
.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}
```

### Fluid Typography
```css
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
  line-height: 1.2;
}
```

### Animation Utilities
```css
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
