---
name: responsive-design
description: Mobile-first responsive design — breakpoints, fluid typography, container queries, and touch optimization
domain: content
tags:
- content-creation
- design
- digital-content
- media
- responsive
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
