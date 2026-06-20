---
name: tailwind-advanced
description: Advanced Tailwind CSS — custom plugins, JIT, container queries, animations, dark mode, design systems
domain: content
tags:
- advanced
- content-creation
- digital-content
- media
- tailwind
---



## Overview

Advanced Tailwind CSS patterns for production applications — custom plugins, container queries, complex animations, design system integration, and performance optimization beyond basic utility classes.

## Capabilities

- Custom Tailwind plugins for project-specific utilities
- Container queries for component-level responsive design
- Complex animations with keyframes and transitions
- Dark mode with class strategy and system preference
- Design system tokens via CSS custom properties
- JIT compiler optimization and purge strategies

## When to Use

- Building a design system on top of Tailwind
- Need component-scoped responsive design (container queries)
- Complex animations beyond basic Tailwind utilities
- Custom utilities that repeat across the project

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The tailwind-advanced workflow follows a standard pipeline pattern.

Core flow:
```
# tailwind-advanced primary flow
input = prepare(raw_data)
result = process(input, config={advanced, animations, container, custom, dark})
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
# tailwind-advanced primary flow
input = prepare(raw_data)
result = process(input, config={advanced, animations, container, custom, dark})
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


### Custom Plugin
```js
// tailwind.config.js
const plugin = require("tailwindcss/plugin")

module.exports = {
  plugins: [
    plugin(function ({ addUtilities, addComponents, theme }) {
      addUtilities({
        ".text-gradient": {
          "background-clip": "text",
          "-webkit-text-fill-color": "transparent",
          "background-image": `linear-gradient(to right, ${theme("colors.blue.500")}, ${theme("colors.purple.500")})`,
        },
      })
      addComponents({
        ".card-elevated": {
          padding: theme("spacing.6"),
          "border-radius": theme("borderRadius.lg"),
          "box-shadow": theme("boxShadow.xl"),
          "background-color": theme("colors.white"),
        },
      })
    }),
  ],
}
```

### Container Queries
```html
<div class="@container">
  <div class="@lg:grid @lg:grid-cols-3 @sm:block">
    <!-- Responsive to container, not viewport -->
  </div>
</div>
```

### Custom Animations
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        "fade-in-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "fade-in-up": "fade-in-up 0.5s ease-out",
        shimmer: "shimmer 2s infinite linear",
      },
    },
  },
}
```

### Dark Mode with CSS Variables
```css
@layer base {
  :root {
    --bg-primary: 255 255 255;
    --text-primary: 15 23 42;
  }
  .dark {
    --bg-primary: 15 23 42;
    --text-primary: 248 250 252;
  }
}
```
```html
<div class="bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))]">
```

## Common Patterns

- **Arbitrary values**: `w-[342px]`, `bg-[#1da1f2]`, `grid-cols-[200px_1fr]`
- **Group/peer**: `group-hover:opacity-100`, `peer-checked:bg-blue-500`
- **Variant stacking**: `dark:md:hover:bg-gray-800`
- **@apply sparingly**: Only for repeated patterns in component CSS
- **Content config**: `content: ["./src/**/*.{ts,tsx}"]` for proper purging

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
