---
name: theme-factory
description: Generate and apply professional color themes, typography systems, and design tokens for applications. Create consistent visual identities across platforms.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- design
- themes
- colors
- typography
- design-tokens
- branding
version: 1.0.0
---

# Theme Factory

## When to Use
**Trigger phrases:**
- "theme factory"
- "Generate and apply professional color themes, typography systems, and design tok"


- When creating a new visual theme or color palette
- When defining design tokens for a design system
- When rebranding an application
- When ensuring visual consistency across platforms

## When NOT to Use

- For implementing existing designs (use `frontend-ui-design`)
- For logo design (use image generation skills)
- For content creation (use content skills)

## Overview

Generate professional design systems including color palettes, typography scales, spacing systems, and design tokens. Supports CSS custom properties, Tailwind config, and design token JSON.

## Workflow

1. **Define brand** — Primary color, mood, audience
2. **Generate palette** — Primary, secondary, accent, neutral, semantic colors
3. **Define typography** — Font stack, scale, line heights, weights
4. **Create tokens** — Design token JSON for cross-platform use
5. **Export** — CSS variables, Tailwind config, Figma tokens

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will pick colors by eye" | Systematic color theory ensures accessibility and harmony |
| "One font is enough" | A type scale (headings, body, caption) creates visual hierarchy |
| "Hardcode colors in components" | Design tokens enable theme switching and dark mode |

## Code Example (CSS Custom Properties)

```css
:root {
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-base: 1rem;
  --font-size-2xl: 1.5rem;
  --space-1: 0.25rem;
  --space-4: 1rem;
  --space-8: 2rem;

  [data-theme="dark"] {
    --color-primary-500: #60a5fa;
    --color-bg: #0f172a;
    --color-text: #f8fafc;
  }
}
```

## Code Example (Python) — Color Palette Generation

Generate a full color scale from a single hex primary using HSL interpolation for light→dark variants (simplified HSL demo — for OKLCH-based perceptual uniformity use the `colour` or `culori` libraries listed below):

```python
from typing import Dict, List, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert #RRGGBB to (R, G, B) integer tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB 0-255 to HSL 0-360 / 0-1 / 0-1."""
    r, g, b = r / 255, g / 255, b / 255
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0, 0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60, s, l


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """Convert HSL to #RRGGBB."""
    c = (1 - abs(2 * l - 1)) * s
    hp = h / 60
    x = c * (1 - abs(hp % 2 - 1))
    m = l - c / 2
    if hp < 1:
        r, g, b = c, x, 0
    elif hp < 2:
        r, g, b = x, c, 0
    elif hp < 3:
        r, g, b = 0, c, x
    elif hp < 4:
        r, g, b = 0, x, c
    elif hp < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return "#{:02x}{:02x}{:02x}".format(
        round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)
    )


def generate_scale(primary: str, steps: List[int] = None) -> Dict[str, str]:
    """Generate a 50-900 color scale from one primary hex.

    Light shades (50-400) blend toward white; dark shades (600-900)
    blend toward black; 500 is the reference.
    """
    if steps is None:
        steps = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    h, s, l = rgb_to_hsl(*hex_to_rgb(primary))
    scale = {}
    target_luminances = {
        50: 0.95, 100: 0.85, 200: 0.75, 300: 0.65, 400: 0.55,
        500: l,
        600: 0.35, 700: 0.25, 800: 0.15, 900: 0.08,
    }
    for step in steps:
        t = target_luminances.get(step, l)
        scale[str(step)] = hsl_to_hex(h, max(0, min(1, s)), max(0, min(1, t)))
    return scale


# Example: generate palette from #3b82f6 (Tailwind blue-500)
primary = "#3b82f6"
scale = generate_scale(primary)
for step, color in scale.items():
    print(f"  --color-primary-{step}: {color};")

# Dark-mode invert: shift lightness toward black, reduce saturation
dark_scale = generate_scale("#60a5fa")
dark_scale["50"]  = "#1e3a8a"  # override for deeper dark background
```

**Production-ready palette libraries:**

- [palette] — Extract color palettes from images (k-means clustering)
- [colour] — Advanced color science (perceptual deltas, gamut mapping)
- [wcag-contrast-ratio] — Check accessibility ratios programmatically

## Code Example (JavaScript) — Design Token → CSS Variables

Generate theme CSS and Tailwind config from a design-token JSON object, including dark-mode inversion and TypeScript types:

```javascript
/**
 * Generate CSS custom properties string from a token tree.
 * Flattens nested keys into `--category-key-subkey` variable names.
 */
function tokensToCSS(tokens, { prefix = "", theme = "light" } = {}) {
  const lines = [];
  for (const [key, value] of Object.entries(tokens)) {
    const varName = prefix ? `${prefix}-${key}` : key;
    if (typeof value === "object" && value !== null && !Array.isArray(value)) {
      lines.push(tokensToCSS(value, { prefix: varName, theme }));
    } else {
      lines.push(`  --${varName}: ${value};`);
    }
  }
  return lines.join("\n");
}

/**
 * Invert a light palette for dark mode by swapping light/dark steps.
 *   dark[50] -> light[900], dark[100] -> light[800], etc.
 */
function invertPalette(tokens) {
  const inverted = JSON.parse(JSON.stringify(tokens));
  for (const [cat, scale] of Object.entries(tokens)) {
    if (typeof scale !== "object") continue;
    inverted[cat] = {};
    for (const [step, color] of Object.entries(scale)) {
      const num = parseInt(step, 10);
      const invertedStep = isNaN(num) ? step : String(1000 - num);
      inverted[cat][invertedStep] = color;
    }
  }
  return inverted;
}

// ---- Example ----
const tokens = {
  color: {
    primary: { 50: "#eff6ff", 500: "#3b82f6", 900: "#1e3a8a" },
    neutral: { 50: "#fafafa", 500: "#737373", 900: "#171717" },
  },
  font: {
    family: { sans: "'Inter', system-ui, sans-serif" },
    size:    { xs: "0.75rem", base: "1rem", xl: "1.5rem" },
  },
  space: { 1: "0.25rem", 4: "1rem", 8: "2rem" },
};

const lightCSS = `:root {\n${tokensToCSS(tokens)}\n}`;
console.log(lightCSS);

const darkTokens = invertPalette(tokens);
const darkCSS = `[data-theme="dark"] {\n${tokensToCSS(darkTokens)}\n}`;
console.log(darkCSS);

// ---- Tailwind v3/v4 config export ----
function tokensToTailwind(tokens) {
  const tw = { theme: { extend: {} } };
  for (const [cat, values] of Object.entries(tokens)) {
    if (cat === "font" && values.family) {
      tw.theme.extend.fontFamily = { sans: values.family.sans.split(",").map(s => s.trim()) };
    }
    if (cat === "space") {
      tw.theme.extend.spacing = Object.fromEntries(
        Object.entries(values).map(([k, v]) => [k, v])
      );
    }
  }
  return tw;
}
// Usage: write tailwind.config.js with module.exports = tokensToTailwind(tokens)
```

## Setup & Configuration

**Python environment:**
```bash
pip install colour-science           # advanced color science
pip install palettable               # predefined color palettes
pip install wcag-contrast-ratio      # accessibility ratio checks
pip install Pillow                   # image-based palette extraction
```

**Node.js environment:**
```bash
npm install chroma-js           # color manipulation (OKLCH, HSL, contrast)
npm install color               # CSS color string parsing
npm install culori              # color conversion + interpolation
npm install @radix-ui/colors   # radix color scales reference
```

**Figma token sync (optional):**
```bash
npm install style-dictionary        # Amazon Style Dictionary — compile design tokens
npx token-transformer                # convert Figma Tokens to Style-Dictionary format
```

For production theme pipelines, use [Style Dictionary](https://amzn.github.io/style-dictionary/) to compile tokens into platform-specific outputs (CSS, iOS, Android, React Native) from a single JSON source.

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Color scale looks muddy / low saturation | Reduce the saturation multiplier for mid-range steps (200-400). Perceptual spacing via OKLCH color space produces cleaner ramps. Try `culori` with `lch()` interpolation |
| WCAG AA contrast fails on primary-500 buttons | Shift the button color toward the darker end of the scale (use primary-600 or primary-700 for text on white backgrounds). Check ratio with `wcag-contrast-ratio` library |
| Dark-mode tokens produce washed-out colors | Dark mode needs lower saturation, not just inverted lightness. Reduce saturation by 15-30% for mid-tones and boost the lighter end (50-200) to ensure contrast on dark backgrounds |
| Typography scale looks uneven | Minor second (1.067) for dense UIs, major third (1.25) for editorial. Scale base size from 16px and verify each step: `h1 = base * ratio^3`, `h2 = base * ratio^2`, `h3 = base * ratio` |
| Generated palette has too many/too few shades | Target 10-step (50-900) for brands, 6-step (100-700) for neutral grays. Merge extremes (50+100, 800+900) when the palette feels redundant |
| Spacing tokens feel arbitrary | Use a modular scale: `space(n) = base * n` where `base = 4px` (tight) or `8px` (generous). Every distance should be a multiple of the base unit |
| Figma tokens won't import | Convert to W3C Design Tokens format using `style-dictionary` or `token-transformer`. Some tools expect `$value` / `$type` keys instead of plain values |

## Monetization

### Theme Marketplace
Create and sell premium themes as digital products:

- **Tailwind UI kits** — Full application themes with color palettes, typography, components ($49-149/sale). List on Tailwind UI, ThemeForest, or Gumroad
- **Figma Design System** — Complete token-based design systems with light/dark mode, component library, and documentation ($79-199/sale)
- **Brand-in-a-box** — Generate brand identity packages (logo + palette + typography + tokens) and sell on a micro-site. Target startups that need instant branding ($199-499/package)
- **Subscription palette feed** — Weekly or monthly curated color palettes with code exports (CSS/JSON/Tailwind) on a membership platform ($9-29/month)

### Design System Service
Offer custom design system consulting as a service:

- **Design system audit** — Review existing UI for inconsistencies, document token gaps, produce a migration plan ($500-2,000/engagement)
- **Custom theme generation** — Build a complete production theme from brand guidelines: colors, typography, spacing, components, dark mode ($1,000-5,000)
- **Token integration** — Wire the theme into their codebase (CSS custom properties, Tailwind, styled-components) with CI/CD token publishing ($2,000-8,000)
- **Multi-brand white-label** — Architecture for SaaS platforms needing per-tenant themes (brand colors, logo, fonts) with runtime token switching ($5,000-15,000)

### Automated Add-ons
- **WCAG accessibility scanner for themes** — SaaS that crawls any CSS file and reports contrast failures ($49/month)
- **Theme snapshot service** — Generate before/after screenshots of an app with different themes for client pitches (per-project)
- **Token diff pipeline** — CI plugin that fails builds when design tokens change unexpectedly, with approval workflow (open-source with paid enterprise tier)

## Process

1. **Define primitives** — Lock in the brand primary hex. Choose neutral undertone (warm/cool/true gray). Pick font superfamily (e.g. Inter for UI + Merriweather for headings). Set the base space unit (4px or 8px).
2. **Map semantic roles** — Assign token names to functional roles: `--color-bg`, `--color-text`, `--color-border`, `--color-accent`. Decide which roles are theme-aware (swap in dark mode) and which are invariant.
3. **Generate palette scale** — Run the Python or JS palette generator from the primary, producing 10-step (50-900) scales for each role color. Verify each step with `wcag-contrast-ratio` against expected backgrounds.
4. **Create variant recipes** — Define interaction states: `hover` → adjust lightness by ±8%, `active` → ±12%, `disabled` → opacity 0.38 + desaturate. Store as functions in design tokens, not hardcoded values.
5. **Export targets** — Compile tokens to CSS custom properties for web, JSON for style-dictionary, Tailwind config for utility-first, and Figma tokens for designers. Dark mode is a separate export pass with inverted values.
6. **Version & publish** — Token breaking changes must be communicated via semver. Publish to npm as `@company/design-tokens` or to a design token CDN endpoint for runtime fetching.

## Verification

- [ ] Every semantic role has a token assignment (bg, text, border, accent, success, error, warning, info)
- [ ] WCAG AA contrast ratio ≥4.5:1 for body text, ≥3:1 for large text (18px+ bold or 24px+ regular) on all role-appropriate backgrounds
- [ ] Dark-mode tokens verified: minimum contrast ratio maintained, not just inverted (saturation may need adjustment)
- [ ] Typography scale covers at least: display, h1, h2, h3, body, caption, overline, code
- [ ] Spacing scale is a strict multiple of the base unit — no orphan distances
- [ ] Token export produces files for every target (CSS, JSON, Tailwind, Figma) that parse without errors
- [ ] Dark mode toggles cleanly (swap `data-theme` attribute) with no un-themed flash
- [ ] Token changes are versioned: bump MAJOR on breaking role renames, MINOR on new roles, PATCH on color value tweaks
