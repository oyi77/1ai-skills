---
name: pptx-creator
description: Create and edit PowerPoint presentations programmatically. Generate slide decks with layouts, charts, images, animations, and speaker notes.
domain: content
tags:
- documents
- powerpoint
- pptx
- presentations
- slides
---

# Pptx Creator

## When to Use

- When generating presentations from data or templates
- When creating slide decks for meetings, pitches, or reports
- When batch-generating presentations with variable content
- When converting structured data to visual slides

## When NOT to Use

- For simple text documents (use `docx-creator`)
- For interactive dashboards (use web-based tools)
- For single-image slides (use image generators)

## Overview

Create professional PowerPoint presentations with full layout support. Handles slide masters, charts, tables, images, animations, and speaker notes. Uses python-pptx (Python) or pptxgenjs (Node.js).

## Workflow

1. **Choose template** — Select or create a slide master/layout
2. **Add slides** — Title, content, comparison, chart, image layouts
3. **Populate content** — Text, data tables, charts, images
4. **Apply design** — Colors, fonts, transitions, animations
5. **Add notes** — Speaker notes for each slide
6. **Export** — Save as .pptx or .pdf

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I'll make slides manually" | Programmatic generation is reproducible and handles data updates |
| "Charts in slides are hard" | python-pptx and pptxgenjs support native PowerPoint charts |
| "Nobody reads slides" | Bad slides are ignored; well-designed data slides drive decisions |

## Code Example (Python)

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = 'Q2 Revenue Report'
slide.placeholders[1].text = 'Board Meeting 2026'

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = 'Key Metrics'
body = slide.placeholders[1]
body.text = '• Revenue: $2.4M (+23%)\n• Users: 150K (+45%)\n• NPS: 72 (+8)'

prs.save('presentation.pptx')
```

## Verification

- [ ] Presentation opens without errors
- [ ] All slides render with correct layouts
- [ ] Charts display data correctly
- [ ] Speaker notes are present
- [ ] Animations/transitions work

