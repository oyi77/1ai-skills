---
name: design-tokens
description: Design token systems — color, typography, spacing, and theme architecture for consistent design. Use when designing token systems — color, typography, spacing, and theme architecture.
domain: content
tags:
- content-creation
- design
- digital-content
- media
- tokens
---



## Overview

Design tokens are the single source of truth for design decisions. This skill covers token taxonomy, color scales, typography, spacing systems, dark mode, and implementation via CSS custom properties and Tailwind.

## Capabilities

- Define color scales with semantic naming (primary, success, error)
- Build typography scales with consistent line heights and weights
- Create spacing systems based on a base unit (4px or 8px)
- Implement dark mode via token swapping
- Export tokens to CSS custom properties, Tailwind, and Figma

## When to Use
**Trigger phrases:**
- "design tokens"
- "designing tokens"
- "Design token systems — color, typography, spacing, and theme architecture for co"


- Starting a new design system from scratch
- Inconsistencies in colors, fonts, or spacing across the app
- Need to support dark mode or multiple themes
- Syncing design decisions between Figma and code

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The design-tokens workflow follows a standard pipeline pattern.

Core flow:
```
# design-tokens primary flow
input = prepare(raw_data)
result = process(input, config={architecture, color, consistent, design, spacing})
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
# design-tokens primary flow
input = prepare(raw_data)
result = process(input, config={architecture, color, consistent, design, spacing})
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


### Token Definition
```json
{
  "color": {
    "primary": { "50": "#eff6ff", "500": "#3b82f6", "900": "#1e3a8a" },
    "success": { "500": "#22c55e" },
    "error": { "500": "#ef4444" }
  },
  "spacing": { "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px" },
  "fontSize": { "xs": "12px", "sm": "14px", "base": "16px", "lg": "18px", "xl": "24px" }
}
```

### CSS Custom Properties
```css
:root {
  --color-primary: var(--color-primary-500);
  --color-bg: #ffffff;
  --color-text: #171717;
}
[data-theme="dark"] {
  --color-bg: #0a0a0a;
  --color-text: #fafafa;
}
```

## Common Patterns

- **Semantic naming**: Use `primary`, `success`, `error` — not `blue-500`, `green-500`
- **Scale by 100s**: Color shades: 50, 100, 200, ..., 900
- **4px base unit**: All spacing multiples of 4px for rhythm
- **Dark mode swap**: Swap 50↔900, 100↔800, etc.

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |

## Video / Motion Graphics

Design tokens ensure brand consistency across [Remotion](../video/remotion/SKILL.md) video compositions. Define brand colors, spacing, and typography tokens once, use across all video scenes. Tokens map directly to CSS custom properties in Remotion components.