---
name: responsive-design
description: Use when mobile-first responsive design — breakpoints, fluid typography,
  container queries, and touch optimization.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- design
- digital-content
- media
- responsive
version: 1.0.0
triggers:
- "responsive-design"
- "mobile-first"
- "breakpoints"
- "responsive layout"
- "mobile layout"
- "fluid typography"
category: content
---
## Overview

Responsive design that works across all devices. Covers mobile-first approach, breakpoint strategy, fluid typography, container queries, touch targets, and performance optimization.

## Capabilities

- Design mobile-first layouts that scale to desktop
- Implement fluid typography with clamp()
- Use container queries for component-level responsiveness
- Optimize touch targets for mobile (44px minimum)
- Handle responsive images and lazy loading

## When to Use
**Trigger phrases:**
- "responsive design"
- "Mobile-first responsive design — breakpoints, fluid typography, container querie"


- Building a new responsive layout
- Existing layout breaks on certain screen sizes
- Mobile traffic is >50% but mobile experience is poor
- Need component-level responsive behavior

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The responsive-design workflow follows a standard pipeline pattern.

Core flow:
```
# responsive-design primary flow
input = prepare(raw_data)
result = process(input, config={breakpoints, container, design, first, fluid})
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
# responsive-design primary flow
input = prepare(raw_data)
result = process(input, config={breakpoints, container, design, first, fluid})
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


## Modern CSS Platform Rules

Prefer native CSS primitives before JavaScript observers or viewport glue:

- **Container queries** for component behavior (`@container`), not viewport breakpoints for every component.
- **Subgrid** when nested content must align to a parent grid; do not duplicate column math.
- **Anchor positioning** (`anchor-name`, `position-anchor`, `position-area`) for tooltips/popovers tied to an element; use JS only for behavior CSS cannot express.
- **`field-sizing: content`** for auto-growing textareas/inputs when supported; keep a sensible max size and fallback.
- **`:user-invalid` / `:user-valid`** for post-interaction form feedback; avoid showing errors before the user submits/touches a field.
- Test support and provide a readable fallback; native APIs are progressive enhancement, not permission to break older browsers.

```css
/* Component adapts to its container, not the viewport */
.card-grid { container-type: inline-size; }
@container (min-width: 42rem) { .card-grid { grid-template-columns: repeat(3, 1fr); } }

/* Native validation after user interaction */
input:user-invalid { border-color: var(--color-danger); }
```

## Responsive Verification

- [ ] Component behavior uses container queries where parent width—not viewport—drives layout
- [ ] Tooltip/popover positioning has a CSS anchor or a tested collision fallback
- [ ] Forms use native validation states and preserve labels/error text for assistive tech
- [ ] Auto-growing fields have a max size and keyboard-safe fallback
- [ ] Tested at 320px, 768px, 1024px, 1440px and with long/translated content

### Mobile-First CSS
```css
/* Mobile first (default) */
.grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }

/* Tablet */
@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); gap: 2rem; }
}
```

### Fluid Typography
```css
h1 { font-size: clamp(1.75rem, 4vw, 3rem); }
body { font-size: clamp(1rem, 2vw, 1.125rem); }
```

### Container Queries
```css
.card-container { container-type: inline-size; }
@container (min-width: 400px) {
  .card { display: flex; gap: 1rem; }
}
```

## Common Patterns

- **Mobile first**: Write mobile styles by default, add `min-width` media queries
- **3 breakpoints**: Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)
- **44px touch targets**: All interactive elements minimum 44x44px on mobile
- **Fluid everything**: Use `clamp()` for font-size, spacing, and widths

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

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |