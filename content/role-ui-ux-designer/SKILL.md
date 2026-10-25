---
name: role-ui-ux-designer
description: Use when orchestrating UI/UX design systems, anti-AI-slop frontend styling,
  tactile micro-interactions, responsive design tokens, accessibility standards, and
  high-fidelity interface engineering.
domain: content
author: oyi77
version: 1.0.0
category: content
tags:
- ui
- ux
- design-systems
- anti-slop
- frontend
- accessibility
- typography
- design-tokens
- micro-interactions
license: MIT
subdomain: ui-ux-design
---

## Overview

The `role-ui-ux-designer` skill directs visual hierarchy, responsive layout engineering, accessible interaction patterns (WCAG 2.1 AA/AAA), tactile micro-motion, and disciplined design token architectures. This role enforces a strict defense against generic AI-generated templates (purple-cyan gradients, unearned glassmorphism orbs, cookie-cutter centered 3-card heroes, floating emoji headers, and sluggish unoptimized animations).

```
[Phase 1: Archetype & Token System] ──► [Phase 2: Anti-Slop Layout Composition]
                                                               │
[Phase 5: Responsive & A11y Verification] ◄── [Phase 4: Micro-Interactions] ◄─┘
```

The UI/UX designer operates through purposeful typography scales, cohesive color palettes, strict button ergonomics (zero dead clicks), semantic vector iconography, and spring-physics micro-interactions running smoothly at 60 FPS.

## When to Use

- When architecting end-to-end design systems, component libraries, or CSS token architectures (`:root` variables).
- When styling web applications, dashboards, consoles, SaaS landing pages, or mobile-first interfaces.
- When eliminating AI slop, unearned gradients, and centered generic cards in existing frontends.
- When crafting fluid micro-interactions, layout transitions, and tactile hover/press states.
- When enforcing WCAG accessibility compliance (text contrast >= 4.5:1, visible focus rings, ARIA landmarks).
- When designing responsive layouts across breakpoints (375px mobile to 1440px desktop) with zero horizontal overflow.

## When NOT to Use

- When writing backend server endpoints or database migrations (use `development/role-software-engineer`).
- When setting up CI/CD pipelines, container orchestration, or cloud hosting (use `devops/role-devops-sre-engineer`).
- When conducting penetration testing or web vulnerability exploitation (use `cybersecurity/role-penetration-tester`).
- When orchestrating product roadmaps, user stories, or PRDs (use `operations/role-product-manager`).

## Deterministic Dispatch Matrix

| UI/UX Objective / Design Challenge | Delegated Child Skill | Primary Design Artifact |
|---|---|---|
| Full-lifecycle design OS, 24 commands (craft, critique, audit, polish, shape), 4 surface modes | `content/impeccable` | Production interface with PRODUCT.md & DESIGN.md artifacts |
| Anti-AI-slop design floor, dealt visual direction, distinctive styling | `content/hallmark` | Production stylesheet adhering to the strict anti-slop floor |
| Comprehensive UI/UX design standards, 50+ styles, 192 product palettes | `content/ui-ux-pro-max` | High-fidelity interface design tokens and component specs |
| Distinctive layout composition, image-to-code pipelines, typography | `content/anti-slop-frontend` | Styled component templates countering generic AI boilerplate |
| Tailwind mastery, layout grids, spacing rules, and surface archetypes | `content/frontend-design` | Clean, responsive Tailwind CSS layouts with zero dead clicks |
| Tactile micro-interactions, layout motion, spring physics, and polish | `content/emil-design-skills` | High-precision motion tokens with cubic-bezier easing curves |
| Semantic CSS custom properties, color systems, and token definitions | `content/design-tokens` | Complete design token dictionary (`tokens.css` or theme schema) |
| Fluid viewport layouts, container queries, mobile touch target sizes | `content/responsive-design` | Responsive media query systems without horizontal overflow |

## Workflow

### Phase 1: Surface Archetype & Design Token Setup

1. Commit explicitly to the interface archetype:
   - **MONITOR**: High density, status indicators, monospace telemetry data, tabular alignment (dashboards).
   - **OPERATE**: Action affordances, clear selection state, clean data tables (admin consoles, queues).
   - **COMPARE**: Aligned columns, parity of structure, one highlighted tier (pricing tables).
   - **DECIDE / LEARN**: Hero allowed, single primary proposition, linear narrative (landing pages, documentation).
2. Dispatch to `content/design-tokens` and `content/ui-ux-pro-max` to define semantic color tokens, font families, and radius scales at `:root`.
3. Never use raw hex values or arbitrary utility colors past the token definitions.

### Phase 2: Anti-Slop Composition & Typography Discipline

1. Apply `content/hallmark` and `content/anti-slop-frontend` invariants:
   - Ban purple-to-cyan or violet-to-blue linear gradients on buttons, text, and card borders.
   - Ban centered 3-card hero stacks; left-align copy and hierarchy naturally.
   - Ban emojis in UI copy, buttons, badges, and headers; use crisp SVG vector icons exclusively.
2. Establish a clear typographical hierarchy: primary display font paired with high-legibility UI sans, and monospace for numerical/telemetry data.

### Phase 3: Layout Construction & Component Ergonomics

1. Scaffold layouts using `content/frontend-design` with disciplined flexbox and CSS grid structures.
2. Build interactive components with complete state coverage: default, hover glow (<= 14px), active press (`scale(0.98)`), focus-visible ring, disabled (opacity 0.5), and loading state.
3. Ensure all interactive targets meet minimum size constraints (desktop >= 36px height, mobile touch targets >= 44x44px with >= 8px physical separation).

### Phase 4: Motion Craft & Micro-Interactions

1. Dispatch to `content/emil-design-skills` to configure tactile interaction motion.
2. Enforce motion rules:
   - Never use `transition: all`.
   - Never animate layout properties (`width`, `height`, `top`, `left`); animate `transform` and `opacity` only.
   - Use high-precision easing curves: `cubic-bezier(0.16, 1, 0.3, 1)` or spring dynamics (150-300ms duration).
3. Respect accessibility settings via `@media (prefers-reduced-motion: reduce)`.

### Phase 5: Responsive Auditing & Accessibility Verification

1. Test viewports across 375px (mobile), 768px (tablet), 1024px (laptop), and 1440px (desktop) via `content/responsive-design`.
2. Verify zero horizontal overflow on small viewports (`overflow-x: hidden` is not a substitute for proper flex wrapping).
3. Measure WCAG 2.1 AA contrast ratios (>= 4.5:1 for normal text, >= 3:1 for large text and interactive boundaries).
4. Verify visible 2-3px focus rings on all keyboard interactive elements.

## Anti-Rationalization

| Design Excuse | Flawed Rationalization | Required UI/UX Design Discipline |
|---|---|---|
| "Adding a colorful gradient makes the app look modern" | "Users love vibrant purple-cyan glow effects." | Gradients without functional hierarchy scream low-effort AI slop. Ground designs in disciplined, high-contrast monochrome or calibrated palettes. |
| "Emojis make buttons friendly and approachable" | "A rocket emoji (🚀) increases click-through rates." | Emojis degrade enterprise brand integrity and render inconsistently across operating systems. Use crisp, monochrome SVG icons. |
| "Centered layout looks balanced on all screen sizes" | "Center-aligning everything makes mobile responsive trivial." | Center-stacked dashboards make data unreadable. Left-align content naturally with tabular alignment for data. |
| "A 100px floating blur orb creates glassmorphism depth" | "Apple uses blurred glass effects everywhere." | Heavy backdrop blurs degrade frame rates on mobile GPUs and obscure content legibility. Use 1px crisp borders with subtle surface tints. |
| "transition: all is convenient and animates everything" | "It ensures any property change animates smoothly." | `transition: all` triggers expensive layout reflows and accidental property jumps. Explicitly declare `transition: transform 180ms ease, opacity 180ms ease`. |

## Implementation Examples

### Anti-Slop Design Token & Button System (CSS)

```css
:root {
  /* Surface Archetype: Linear Dark */
  --bg-canvas: #090a0f;
  --bg-surface: #11131a;
  --bg-surface-raised: #181b24;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);
  
  /* Text & Accent Tokens */
  --text-primary: #f0f2f5;
  --text-muted: #8b92a5;
  --accent-brand: #3b82f6;
  --accent-brand-hover: #2563eb;
  
  /* Motion Tokens */
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 150ms;
}

/* Ergonomic, Accessible Button */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 2.25rem; /* 36px */
  padding: 0 1rem;
  border-radius: 6px;
  background-color: var(--accent-brand);
  color: #ffffff;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--duration-fast) var(--ease-spring),
              background-color var(--duration-fast) ease,
              box-shadow var(--duration-fast) ease;
}

.btn-primary:hover {
  background-color: var(--accent-brand-hover);
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.35);
}

.btn-primary:active {
  transform: scale(0.98);
}

.btn-primary:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 2px;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

### Contrast & Token Verification Runner (Python)

```python
import re

def verify_stylesheet_tokens(css_content: str):
    """Verifies that stylesheet adheres to anti-slop token rules and bans transition: all."""
    # Check for transition: all
    if "transition: all" in css_content or "transition:all" in css_content:
        raise ValueError("SLOP DETECTED: 'transition: all' is strictly banned.")
    
    # Check for banned AI gradient slop
    banned_gradient_patterns = [
        r"from-purple-\d+.*to-cyan-\d+",
        r"from-violet-\d+.*to-blue-\d+",
        r"linear-gradient\(.*#8b5cf6.*#06b6d4.*\)"
    ]
    for pattern in banned_gradient_patterns:
        if re.search(pattern, css_content, re.IGNORECASE):
            raise ValueError(f"SLOP DETECTED: Banned AI gradient detected ({pattern}).")
            
    print("SUCCESS: Stylesheet passed all Anti-Slop token and motion checks.")

if __name__ == "__main__":
    sample_css = """
    :root { --accent: #3b82f6; }
    .card { transition: transform 150ms cubic-bezier(0.16, 1, 0.3, 1), opacity 150ms ease; }
    """
    verify_stylesheet_tokens(sample_css)
```

## Verification Checklist

- [ ] All colors and font declarations reference `:root` tokens or theme variables.
- [ ] No `transition: all` used anywhere; layout dimensions (`width`, `height`) are not animated.
- [ ] Banned AI-slop gradients (purple-cyan, violet-blue linear meshes) completely eliminated.
- [ ] Interactive buttons meet minimum touch target standards (36px desktop, 44px mobile).
- [ ] Text contrast meets or exceeds WCAG 2.1 AA (>= 4.5:1 text, >= 3:1 boundaries).
- [ ] Visible focus rings present on all interactive elements during keyboard navigation.
- [ ] Zero emoji in UI copy, badges, or buttons; crisp SVG icons used exclusively.
- [ ] Mobile responsive layout displays cleanly across 375px-1440px with zero horizontal scroll.
