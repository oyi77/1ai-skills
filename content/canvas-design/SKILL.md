---
name: canvas-design
description: Design visual art and graphics using HTML5 Canvas, p5.js, or SVG. Create generative art, data visualizations, diagrams, and interactive graphics.
domain: content
tags:
- design
- canvas
- graphics
- visualization
- generative-art
- svg
---

# Canvas Design

## When to Use
**Trigger phrases:**
- "canvas design"
- "Design visual art and graphics using HTML5 Canvas, p5"


- When creating visual diagrams, charts, or infographics
- When generating algorithmic/generative art
- When building interactive data visualizations
- When designing custom graphics for presentations or documents

## When NOT to Use

- For photo editing (use image editors)
- For UI component design (use `frontend-ui-design`)
- For video content (use video generation skills)

## Overview

Create professional visual content using programmatic design tools. Supports HTML5 Canvas, p5.js for generative art, SVG for scalable graphics, and Canvas API for data visualization.

## Workflow

1. **Define visual spec** — Dimensions, style, color palette, content
2. **Choose tool** — p5.js (generative), SVG (scalable), Canvas (pixel)
3. **Create composition** — Layout, shapes, text, images
4. **Apply style** — Colors, gradients, shadows, typography
5. **Export** — PNG, SVG, or interactive HTML

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will use a template" | Programmatic design is reproducible, data-driven, and unique |
| "Design tools are for designers" | Canvas/SVG code is just code — engineers can create visual content |
| "Stock images work" | Custom graphics communicate your specific message better |

## Code Example (p5.js)

```javascript
function setup() {
  createCanvas(800, 600);
  background(20);
  for (let i = 0; i < 200; i++) {
    let x = random(width);
    let y = random(height);
    let size = random(2, 8);
    fill(100, 200, 255, random(50, 200));
    noStroke();
    ellipse(x, y, size);
  }
  fill(255);
  textSize(32);
  textAlign(CENTER);
  text('Data Visualization', width/2, 50);
}
```

## Verification

- [ ] Visual renders at correct dimensions
- [ ] Colors match specified palette
- [ ] Text is legible and properly positioned
- [ ] Export format is correct (PNG/SVG/HTML)

