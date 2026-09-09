---
name: banner-design
description: Banner design for social media, ads, web, print. 22 art direction styles, exact platform sizes, safe zones, export workflow. Use when creating banners, covers, headers for Facebook, Twitter, LinkedIn, YouTube, Instagram, Google Ads, website hero.
domain: content
author: claudekit
license: MIT
subdomain: banner
tags:
- banner
- design
- social-media
- ads
- cover
- header
- export
- html-css
- screenshot
version: 1.0.0
category: content
---

# Banner Design - Multi-Format Creative Banner System

Design banners across social, ads, web, and print formats. Generates multiple art direction options per request with AI-powered visual elements. This skill handles banner design only. Does NOT handle video editing, full website design, or print production.

## When to Use

- User requests banner, cover, or header design
- Social media cover/header creation
- Ad banner or display ad design
- Website hero section visual design
- Event/print banner design
- Creative asset generation for campaigns

## Prerequisites

**Python:** This skill uses Python scripts. On Windows, use `python` instead of `python3` (e.g., `python scripts/search.py` instead of `python3 scripts/search.py`).

## Workflow

### Step 1: Gather Requirements (AskUserQuestion)

Collect via AskUserQuestion:
1. **Purpose** — social cover, ad banner, website hero, print, or creative asset?
2. **Platform/size** — which platform or custom dimensions?
3. **Content** — headline, subtext, CTA, logo placement?
4. **Brand** — existing brand guidelines? (check `docs/brand-guidelines.md`)
5. **Style preference** — any art direction? (show style options if unsure)
6. **Quantity** — how many options to generate? (default: 3)

### Step 2: Research & Art Direction

1. Activate `ui-ux-pro-max` skill for design intelligence
2. Use Chrome browser to research Pinterest for design references:
   ```
   Navigate to pinterest.com → search "[purpose] banner design [style]"
   Screenshot 3-5 reference pins for art direction inspiration
   ```
3. Select 2-3 complementary art direction styles from references:
   `references/banner-sizes-and-styles.md`

### Step 3: Design & Generate Options

For each art direction option:

1. **Create HTML/CSS banner** using `frontend-design` skill
   - Use exact platform dimensions from size reference
   - Apply safe zone rules (critical content in central 70-80%)
   - Max 2 typefaces, single CTA, 4.5:1 contrast ratio
   - Inject brand context via `inject-brand-context.cjs`

2. **Generate visual elements** with AI image generation
   - Use `ai-multimodal` or `geminigen-ai` skills for visuals
   - Generate backgrounds, patterns, illustrations, product shots
   - Aspect ratios: `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `2:3`, `3:2`
   - Match to platform - e.g., Twitter header = `3:1` (use `3:2` closest), Instagram story = `9:16`

3. **Compose final banner** — overlay text, CTA, logo on generated visual in HTML/CSS

### Step 4: Export Banners to Images

After designing HTML banners, export each to PNG using Chrome DevTools:

1. **Serve HTML files** via local server (python http.server or similar)
2. **Screenshot each banner** at exact platform dimensions:
   ```bash
   # Export banner to PNG at exact dimensions
   # Use Playwright/Puppeteer or Chrome DevTools screenshot
   ```
3. **Auto-compress** if >5MB (Sharp compression built-in)

**Output path convention**:
```
assets/banners/{campaign}/
├── minimalist-1500x500.png
├── gradient-1500x500.png
├── bold-type-1500x500.png
├── minimalist-1080x1080.png    # if multi-size requested
└── ...
```

- Use kebab-case for filenames: `{style}-{width}x{height}.{ext}`
- Date prefix for time-sensitive campaigns: `{YYMMDD}-{style}-{size}.png`
- Campaign folder groups all variants together

### Step 5: Present Options & Iterate

Present all exported images side-by-side. For each option show:
- Art direction style name
- Exported PNG preview
- Key design rationale
- File path & dimensions

Iterate based on user feedback until approved.

## Banner Size Quick Reference

| Platform | Type | Size (px) | Aspect Ratio |
|----------|------|-----------|--------------|
| Facebook | Cover | 820 × 312 | ~2.6:1 |
| Twitter/X | Header | 1500 × 500 | 3:1 |
| LinkedIn | Personal | 1584 × 396 | 4:1 |
| YouTube | Channel art | 2560 × 1440 | 16:9 |
| Instagram | Story | 1080 × 1920 | 9:16 |
| Instagram | Post | 1080 × 1080 | 1:1 |
| Google Ads | Med Rectangle | 300 × 250 | 6:5 |
| Google Ads | Leaderboard | 728 × 90 | 8:1 |
| Website | Hero | 1920 × 600-1080 | ~3:1 |

Full reference: `references/banner-sizes-and-styles.md`

## Art Direction Styles (Top 10)

| Style | Best For | Key Elements |
|-------|----------|--------------|
| Minimalist | SaaS, tech | White space, 1-2 colors, clean type |
| Bold Typography | Announcements | Oversized type as hero element |
| Gradient | Modern brands | Mesh gradients, chromatic blends |
| Photo-Based | Lifestyle, e-com | Full-bleed photo + text overlay |
| Geometric | Tech, fintech | Shapes, grids, abstract patterns |
| Retro/Vintage | F&B, craft | Distressed textures, muted colors |
| Glassmorphism | SaaS, apps | Frosted glass, blur, glow borders |
| Neon/Cyberpunk | Gaming, events | Dark bg, glowing neon accents |
| Editorial | Media, luxury | Grid layouts, pull quotes |
| 3D/Sculptural | Product, tech | Rendered objects, depth, shadows |

Full 22 styles: `references/banner-sizes-and-styles.md`

## Design Rules

- **Safe zones**: critical content in central 70-80% of canvas
- **CTA**: one per banner, bottom-right, min 44px height, action verb
- **Typography**: max 2 fonts, min 16px body, ≥32px headline
- **Text ratio**: under 20% for ads (Meta penalizes heavy text)
- **Print**: 300 DPI, CMYK, 3-5mm bleed
- **Brand**: always inject via `inject-brand-context.cjs`

## Integration

- **ui-ux-pro-max** — Use for design intelligence and style selection
- **brand** — Inject brand context and validate assets
- **geminigen-ai** — Generate AI visuals for banners
- **frontend-design** — Build HTML/CSS banner layouts
## Overview

Banner-design produces platform-ready creative across social, ads, web, and print from a single HTML/CSS source: 22 art direction styles, exact per-platform pixel sizes with safe zones (full matrix in `references/banner-sizes-and-styles.md`), and an export pipeline that screenshots HTML to PNG at the target dimensions. It pairs with ui-ux-pro-max for style intelligence, brand for identity injection/validation, and geminigen-ai for AI visuals. Serve an HTML banner locally with `npx http-server .` (or `python3 -m http.server`), then screenshot the target viewport to PNG at exact size.

## When NOT to Use

- Full-page website design — route to design/ui-styling instead of squeezing a page into a banner canvas
- Video or animated ad formats — route to HyperFrames/Remotion; this skill outputs static images
- Print production (brochures, multi-page) — a banner is single-surface; route multi-page print to design/document-creator
- Logo or icon creation — use design/logo or icon workflows
- When the user just needs a quick crop/resize of an existing asset — use an image tool, not a redesign

## Verification

1. Canvas dimensions match the target platform exactly (reference matrix, e.g. 1080×1080 Instagram post, 300×250 medium rectangle)
2. Critical content sits inside the safe zone (central 70–80%); nothing vital within 10% of any edge
3. One CTA per banner, bottom-right, ≥44px hit area, action verb
4. Text ratio under 20% for paid social (Meta ad-policy check)
5. Export at the exact pixel size; no letterboxing or upscaling artifacts
6. Brand pass: colors and type come from the injected brand context; `validate-asset.cjs` returns PASS

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "One design will work across platforms" | Ratios differ wildly (3:1 header vs 9:16 story); cropping one master breaks composition per surface |
| "I'll fill the whole canvas, more is better" | Dense banners fail at small ad sizes; safe zones and negative space carry the CTA |
| "Text-heavy is fine, it explains more" | Paid platforms penalize >20% text ratio with lower delivery and cost per result |
| "Screenshot at any size, it will scale" | Pixel-perfect export requires rendering at the exact target dimensions, not scaling |
| "Print and web colors are the same" | Web is RGB, print is CMYK at 300 DPI with bleed — export differs per medium |

