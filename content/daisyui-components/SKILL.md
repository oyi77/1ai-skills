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
