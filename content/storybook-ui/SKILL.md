---
name: storybook-ui
description: Storybook for UI component development — stories, addons, controls, a11y testing, visual regression
domain: content
tags:
- content-creation
- digital-content
- media
- storybook
- testing
---



## Overview

Storybook is a frontend workshop for building, testing, and documenting UI components in isolation. Supports React, Vue, Svelte, Angular, and more. Essential for component-driven development.

## Capabilities

- Component development in isolation with hot reload
- Interactive controls for props (args, argTypes)
- Accessibility testing with a11y addon
- Visual regression testing with Chromatic
- Interaction testing with play functions
- Documentation with autodocs and MDX

## When to Use

- Building a component library or design system
- Need to develop UI components in isolation
- Want visual regression testing in CI
- Documenting components for team consumption
- Testing accessibility of UI components

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The storybook-ui workflow follows a standard pipeline pattern.

Core flow:
```
# storybook-ui primary flow
input = prepare(raw_data)
result = process(input, config={addons, component, controls, development, regression})
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
# storybook-ui primary flow
input = prepare(raw_data)
result = process(input, config={addons, component, controls, development, regression})
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


### Installation
```bash
npx storybook@latest init
# React example
npm install -D @storybook/react @storybook/react-vite
```

### CSF3 Story Format
```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react"
import { Button } from "./Button"

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary", "outline"] },
    size: { control: "select", options: ["sm", "md", "lg"] },
  },
}
export default meta
type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: { variant: "primary", children: "Click me" },
}

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: "flex", gap: 8 }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
}
```

### Interaction Testing
```tsx
import { expect, userEvent, within } from "@storybook/test"

export const WithInteraction: Story = {
  args: { label: "Counter" },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await userEvent.click(canvas.getByRole("button"))
    await expect(canvas.getByText("Count: 1")).toBeInTheDocument()
  },
}
```

### Storybook Config
```js
// .storybook/main.ts
export default {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-essentials", "@storybook/addon-a11y"],
  framework: "@storybook/react-vite",
}
```

## Common Patterns

- **Autodocs**: `tags: ["autodocs"]` auto-generates documentation page
- **Decorators**: Wrap stories with ThemeProvider, Router, etc.
- **Play functions**: Test interactions that run in the browser
- **MDX docs**: Combine Markdown and JSX for rich documentation
- **Chromatic**: `npx chromatic` for visual regression in CI

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
