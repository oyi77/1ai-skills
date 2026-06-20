---
name: radix-primitives
description: Radix UI headless primitives — accessible, unstyled React components for dialogs, dropdowns, tooltips
domain: content
tags:
- content-creation
- digital-content
- media
- primitives
- radix
---



## Overview

Radix UI provides unstyled, accessible React primitives (Dialog, Dropdown, Popover, Tooltip, etc.) that handle behavior, keyboard navigation, and ARIA attributes. Style them with Tailwind, CSS, or any CSS-in-JS.

## Capabilities

- Fully accessible out of the box (WAI-ARIA compliant)
- Keyboard navigation and focus management
- Unstyled — bring your own design system
- Controlled and uncontrolled modes
- Composable with Tailwind CSS
- 30+ primitives: Dialog, DropdownMenu, Popover, Select, Tabs, etc.

## When to Use

- Building a custom design system from scratch
- Need accessible components without Material/Chakra styling
- Using shadcn/ui (built on Radix primitives)
- Need fine-grained control over component behavior and appearance

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The radix-primitives workflow follows a standard pipeline pattern.

Core flow:
```
# radix-primitives primary flow
input = prepare(raw_data)
result = process(input, config={accessible, components, dialogs, dropdowns, headless})
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
# radix-primitives primary flow
input = prepare(raw_data)
result = process(input, config={accessible, components, dialogs, dropdowns, headless})
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
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-popover
npm install @radix-ui/react-tooltip @radix-ui/react-tabs @radix-ui/react-accordion
```

### Dialog with Tailwind
```tsx
import * as Dialog from "@radix-ui/react-dialog"

export function Modal({ children, trigger }) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6 w-[90vw] max-w-md">
          {children}
          <Dialog.Close className="absolute top-4 right-4">✕</Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
```

### DropdownMenu
```tsx
import * as DropdownMenu from "@radix-ui/react-dropdown-menu"

export function Menu({ items }) {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger className="px-4 py-2 bg-gray-100 rounded">
        Options
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content className="bg-white rounded-md shadow-lg p-1 min-w-[160px]">
          {items.map((item) => (
            <DropdownMenu.Item key={item.id} className="px-3 py-2 rounded hover:bg-gray-100 cursor-pointer">
              {item.label}
            </DropdownMenu.Item>
          ))}
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  )
}
```

### Tooltip
```tsx
import * as Tooltip from "@radix-ui/react-tooltip"

export function Tip({ children, content }) {
  return (
    <Tooltip.Provider delayDuration={200}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>{children}</Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content className="bg-gray-900 text-white text-sm px-3 py-1.5 rounded" sideOffset={5}>
            {content}
            <Tooltip.Arrow className="fill-gray-900" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  )
}
```

## Common Patterns

- **asChild**: `<Trigger asChild><Button>Open</Button></Trigger>` — composes without extra DOM
- **Portal**: Always wrap Content in Portal for proper z-index layering
- **Animation**: Use `data-[state=open]` and `data-[state=closed]` for CSS transitions
- **Composition**: Combine primitives (Dialog + Form + Select) for complex UIs
- **Focus trap**: Built-in — Dialog automatically traps focus, handles Escape key

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
