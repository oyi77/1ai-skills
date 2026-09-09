---
name: design-system
description: Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variables, spacing/typography scales, component specs, strategic slide creation. Use for design tokens, systematic design, brand-compliant presentations.
domain: content
author: claudekit
license: MIT
subdomain: design-system
tags:
- design-system
- tokens
- css-variables
- component-specs
- slides
- presentations
- chartjs
- tailwind
version: 1.0.0
category: content
---


# Design System

Token architecture, component specifications, systematic design, slide generation.
## When to Use

- Design token creation
- Component state definitions
- CSS variable systems
- Spacing/typography scales
- Design-to-code handoff
- Tailwind theme configuration
- **Slide/presentation generation**

## Workflow

1. **Define** — Establish primitive tokens (colors, spacing, typography)
2. **Map** — Create semantic aliases for primitives
3. **Apply** — Build component-specific tokens
4. **Generate** — Output CSS variables and Tailwind config
5. **Validate** — Check for hardcoded values in codebase

## Token Architecture

Load: `references/token-architecture.md`

### Three-Layer Structure

```
Primitive (raw values)
       ↓
Semantic (purpose aliases)
       ↓
Component (component-specific)
```

**Example:**
```css
/* Primitive */
--color-blue-600: #2563EB;

/* Semantic */
--color-primary: var(--color-blue-600);

/* Component */
--button-bg: var(--color-primary);
```

## Quick Start

**Generate tokens:**
```bash
node scripts/generate-tokens.cjs --config tokens.json -o tokens.css
```

**Validate usage:**
```bash
node scripts/validate-tokens.cjs --dir src/
```

Requirements: Node 18+ for the `.cjs` token scripts (`apt install nodejs`), Python 3 for the slide search/validator scripts (`apt install python3`).

## References

| Topic | File |
|-------|------|
| Token Architecture | `references/token-architecture.md` |
| Primitive Tokens | `references/primitive-tokens.md` |
| Semantic Tokens | `references/semantic-tokens.md` |
| Component Tokens | `references/component-tokens.md` |
| Component Specs | `references/component-specs.md` |
| States & Variants | `references/states-and-variants.md` |
| Tailwind Integration | `references/tailwind-integration.md` |

## Component Spec Pattern

| Property | Default | Hover | Active | Disabled |
|----------|---------|-------|--------|----------|
| Background | primary | primary-dark | primary-darker | muted |
| Text | white | white | white | muted-fg |
| Border | none | none | none | muted-border |
| Shadow | sm | md | none | none |

## Scripts

| Script | Purpose |
|--------|---------|
| `generate-tokens.cjs` | Generate CSS from JSON token config |
| `validate-tokens.cjs` | Check for hardcoded values in code |
| `search-slides.py` | BM25 search + contextual recommendations |
| `slide-token-validator.py` | Validate slide HTML for token compliance |
| `fetch-background.py` | Fetch images from Pexels/Unsplash |

## Templates

| Template | Purpose |
|----------|---------|
| `design-tokens-starter.json` | Starter JSON with three-layer structure |

## Integration

**With brand:** Extract primitives from brand colors/typography
**With ui-styling:** Component tokens → Tailwind config

**Skill Dependencies:** brand, ui-styling
**Primary Agents:** ui-ux-designer, frontend-developer

## Slide System

Brand-compliant presentations using design tokens + Chart.js + contextual decision system.

### Source of Truth

| File | Purpose |
|------|---------|
| `docs/brand-guidelines.md` | Brand identity, voice, colors |
| `assets/design-tokens.json` | Token definitions (primitive→semantic→component) |
| `assets/design-tokens.css` | CSS variables (import in slides) |
| `assets/css/slide-animations.css` | CSS animation library |

### Slide Search (BM25)

```bash
# Basic search (auto-detect domain)
python scripts/search-slides.py "investor pitch"

# Domain-specific search
python scripts/search-slides.py "problem agitation" -d copy
python scripts/search-slides.py "revenue growth" -d chart

# Contextual search (Premium System)
python scripts/search-slides.py "problem slide" --context --position 2 --total 9
python scripts/search-slides.py "cta" --context --position 9 --prev-emotion frustration
```

### Decision System CSVs

| File | Purpose |
|------|---------|
| `data/slide-strategies.csv` | 15 deck structures + emotion arcs + sparkline beats |
| `data/slide-layouts.csv` | 25 layouts + component variants + animations |
| `data/slide-layout-logic.csv` | Goal → Layout + break_pattern flag |
| `data/slide-typography.csv` | Content type → Typography scale |
| `data/slide-color-logic.csv` | Emotion → Color treatment |
| `data/slide-backgrounds.csv` | Slide type → Image category (Pexels/Unsplash) |
| `data/slide-copy.csv` | 25 copywriting formulas (PAS, AIDA, FAB) |
| `data/slide-charts.csv` | 25 chart types with Chart.js config |

### Contextual Decision Flow

```
1. Parse goal/context
        ↓
2. Search slide-strategies.csv → Get strategy + emotion beats
        ↓
3. For each slide:
   a. Query slide-layout-logic.csv → layout + break_pattern
   b. Query slide-typography.csv → type scale
   c. Query slide-color-logic.csv → color treatment
   d. Query slide-backgrounds.csv → image if needed
   e. Apply animation class from slide-animations.css
        ↓
4. Generate HTML with design tokens
        ↓
5. Validate with slide-token-validator.py
```

### Pattern Breaking (Duarte Sparkline)

Premium decks alternate between emotions for engagement:
```
"What Is" (frustration) ↔ "What Could Be" (hope)
```

System calculates pattern breaks at 1/3 and 2/3 positions.

### Slide Requirements

**ALL slides MUST:**
1. Import `assets/design-tokens.css` - single source of truth
2. Use CSS variables: `var(--color-primary)`, `var(--slide-bg)`, etc.
3. Use Chart.js for charts (NOT CSS-only bars)
4. Include navigation (keyboard arrows, click, progress bar)
5. Center align content
6. Focus on persuasion/conversion

### Chart.js Integration

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<canvas id="revenueChart"></canvas>
<script>
new Chart(document.getElementById('revenueChart'), {
    type: 'line',
    data: {
        labels: ['Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            data: [5, 12, 28, 45],
            borderColor: '#FF6B6B',  // Use brand coral
            backgroundColor: 'rgba(255, 107, 107, 0.1)',
            fill: true,
            tension: 0.4
        }]
    }
});
</script>
```

### Token Compliance

```css
/* CORRECT - uses token */
background: var(--slide-bg);
color: var(--color-primary);
font-family: var(--typography-font-heading);

/* WRONG - hardcoded */
background: #0D0D0D;
color: #FF6B6B;
font-family: 'Space Grotesk';
```

### Reference Implementation

Working example with all features:
```
assets/designs/slides/claudekit-pitch-251223.html
```

### Command

```bash
/slides:create "10-slide investor pitch for ClaudeKit Marketing"
```

## Best Practices

1. Never use raw hex in components - always reference tokens
2. Semantic layer enables theme switching (light/dark)
3. Component tokens enable per-component customization
4. Use HSL format for opacity control
5. Document every token's purpose
6. **Slides must import design-tokens.css and use var() exclusively**
## Overview

design-system turns brand primitives into a three-layer token architecture — primitive → semantic → component — exposed as CSS variables and consumed by components and slides. It ships real tooling: `scripts/generate-tokens.cjs` (primitive→semantic→component generation), `scripts/embed-tokens.cjs` (token→CSS embedding), `scripts/validate-tokens.cjs` / `scripts/html-token-validator.py` (compliance checks), and `scripts/search-slides.py` + `scripts/generate-slide.py` (BM25 slide search and deck generation with Chart.js). The slide system enforces one source of truth: every deck imports `assets/design-tokens.css` and uses `var()` exclusively — no raw hex.

## When NOT to Use

- A single throwaway component — inline tokens beat a full system until reuse appears
- UI implementation without a design-language decision — route to ui-styling/ui-ux-pro-max first
- Brand definition itself (colors, voice) — that is brand; this skill consumes its output
- A deck that will be delivered as native PowerPoint/PDF — slides here are HTML-screen-first
- When the team already has an authoritative token platform (Tokens Studio, Style Dictionary) — keep one source of truth and export to it

## Verification

1. Every color/space/type used in components and slides resolves through `var(--...)` — run `scripts/html-token-validator.py` on generated HTML, zero raw-hex violations
2. The three layers stay clean: primitives hold raw values, semantics name intent, components bind to semantics (no component→primitive direct links)
3. `scripts/validate-tokens.cjs` passes — tokens parse, required namespaces exist, no orphaned/duplicate tokens
4. Slides import `assets/design-tokens.css` and the BM25 search returns the expected strategy/layout reference for the request
5. A deck renders with the Chart.js chart displaying real data and pattern-breaking at the 1/3 and 2/3 positions

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "I'll hardcode the color here, it's just one place" | One raw hex becomes ten; the validator exists because drift is the default |
| "Two layers are enough" | Without the semantic layer, product decisions rewrite primitives and ripple everywhere |
| "Tokens are a documentation task" | Tokens are executable: generation, embedding, and validation scripts enforce compliance mechanically |
| "The slide search is extra work" | BM25 over the strategy/layout/decision CSVs is how a deck gets contextual structure instead of a generic template |
| "Validation slows iteration" | Validation is a 2-second gate that catches off-system values before a human review round |

