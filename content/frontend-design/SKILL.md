---
name: frontend-design
description: Design system patterns — component architecture, Tailwind mastery, visual
  hierarchy, and responsive layouts
domain: content
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

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The frontend-design workflow follows a standard pipeline pattern.

Core flow:
```
# frontend-design primary flow
input = prepare(raw_data)
result = process(input, config={architecture, component, design, frontend, hierarchy})
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
# frontend-design primary flow
input = prepare(raw_data)
result = process(input, config={architecture, component, design, frontend, hierarchy})
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
