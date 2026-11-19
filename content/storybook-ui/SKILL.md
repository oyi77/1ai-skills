---
name: storybook-ui
description: Use when storybook for UI component development — stories, addons, controls,
  a11y testing, visual regression.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- digital-content
- media
- storybook
- testing
version: 1.0.0
category: content
---




## Overview

Storybook is a workshop for developing, testing, and documenting UI components in isolation. This skill focuses on React with CSF3, interaction tests, accessibility checks, visual regression, and component-level performance guardrails. It also notes where framework-specific checks differ; verify current Storybook APIs against the installed version.

## Capabilities

- Component development in isolation with hot reload
- Interactive controls for props (args, argTypes)
- Accessibility testing with a11y addon
- Visual regression testing with Chromatic
- Interaction testing with play functions
- Documentation with autodocs and MDX

## When to Use
**Trigger phrases:**
- "storybook ui"
- "Storybook for UI component development — stories, addons, controls, a11y testing"


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

## React Performance Guardrails

Apply these when stories or components expose production behavior:

- **No waterfalls:** do not fetch unrelated data serially in a story or component; parallelize independent requests and show loading/error states.
- **Bundle discipline:** import individual icons/components; avoid importing an entire library for one symbol. Keep browser-only code out of server-rendered modules.
- **Server/client boundary:** keep static content and data work server-side where the framework supports it; mark client components only when they need state, effects, or browser APIs.
- **Rerender control:** keep stable object/function references where it matters, use stable list keys, and measure before adding memoization.
- **Long lists:** virtualize lists with hundreds of rows; test keyboard navigation and screen-reader semantics after virtualization.
- **Hydration:** stories must render the same initial markup on server and client; isolate time, random IDs, browser APIs, and layout reads behind client-safe boundaries.
- **Loading/error/empty states:** every async story includes all states, not only the successful screenshot.

## Verification

- [ ] CSF3 stories render with controls and autodocs
- [ ] Interaction stories exercise keyboard and pointer paths
- [ ] Accessibility addon reports no blocking violations
- [ ] Loading, empty, error, disabled, and success states are represented
- [ ] No hydration mismatch or browser-only code runs during server render
- [ ] Long lists are virtualized or an explicit reason is recorded
- [ ] Bundle imports are scoped; no unnecessary full-library import
- [ ] Visual regression runs at representative viewport/theme combinations
- [ ] Component performance measured before memoization or complexity is added

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