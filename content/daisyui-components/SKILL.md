---
name: daisyui-components
description: daisyUI component library for Tailwind — themed components, colors, responsive, dark mode
---



## Overview

daisyUI adds component classes to Tailwind CSS — buttons, cards, modals, dropdowns, etc. — without JavaScript. Uses Tailwind's plugin system with theme customization via CSS variables.

## Capabilities

- 50+ component classes (btn, card, modal, dropdown, etc.)
- Built-in themes (light, dark, cupcake, corporate, etc.)
- Responsive components with Tailwind breakpoints
- No JavaScript required — pure CSS components
- Theme customization via CSS variables
- Color utilities (primary, secondary, accent, etc.)

## When to Use

- Want pre-built UI components with Tailwind workflow
- Need themed components without writing custom CSS
- Building prototypes or MVPs quickly
- Want consistent design without a full design system

## Pseudo Code

The daisyui-components workflow follows a standard pipeline pattern.

Core flow:
```
# daisyui-components primary flow
input = prepare(raw_data)
result = process(input, config={colors, component, components, daisyui, dark})
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
# daisyui-components primary flow
input = prepare(raw_data)
result = process(input, config={colors, component, components, daisyui, dark})
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
npm install daisyui
```

```js
// tailwind.config.js
module.exports = {
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "corporate"],
    darkTheme: "dark",
  },
}
```

### Component Usage
```html
<!-- Button -->
<button class="btn btn-primary">Click Me</button>
<button class="btn btn-outline btn-secondary">Outline</button>

<!-- Card -->
<div class="card bg-base-100 shadow-xl">
  <figure><img src="/photo.jpg" alt="Photo" /></figure>
  <div class="card-body">
    <h2 class="card-title">Title</h2>
    <p>Content</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>

<!-- Modal -->
<dialog id="my_modal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Hello!</h3>
    <p class="py-4">Modal content</p>
    <div class="modal-action">
      <form method="dialog"><button class="btn">Close</button></form>
    </div>
  </div>
</dialog>
```

### Dark Mode Toggle
```html
<label class="swap swap-rotate">
  <input type="checkbox" data-toggle-theme="dark,light" />
  <div class="swap-on">🌙</div>
  <div class="swap-off">☀️</div>
</label>
```

## Common Patterns

- **Color modifiers**: `btn-primary`, `btn-secondary`, `btn-accent`, `btn-ghost`, `btn-link`
- **Size modifiers**: `btn-xs`, `btn-sm`, `btn-md`, `btn-lg`
- **State modifiers**: `btn-active`, `btn-disabled`, `loading`
- **Responsive**: `btn md:btn-lg` — larger on medium screens
- **Themes**: Apply per-section with `data-theme="dark"` attribute

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
