---
name: content-generator
description: Multi-provider automated video content generation platform. Generates TikTok 9:16 vertical videos (1 minute)
  from text prompts using NVIDIA NIM + BytePlus Seedance + FFmpeg. Implements Larry Playbook viral formula. Use when creating
  TikTok content, product videos, or any AI-generated video.
domain: content
tags:
- content
- content-creation
- digital-content
- generator
- media
- video
persona: "|\n  name: \"MrBeast (Jimmy Donaldson)\"\n    title: \"Master of Viral Content\"\n    expertise: [\"retention optimization\"\
  , \"thumbnail psychology\", \"pacing mastery\", \"audience psychology\"]\n    philosophy: \"Every second matters. If they're\
  \ not entertained, they leave. Make every frame count.\"\n    credentials:\n      - \"300+ million YouTube subscribers across\
  \ channels\"\n      - \"Pioneered high-production challenge videos with massive budgets\"\n      - \"Average 100M+ views\
  \ per video through retention optimization\"\n      - \"Built Feastables to $100M+ revenue through content-driven marketing\"\
  \n    principles:\n      - \"Hook in 3 seconds - grab attention immediately or lose them forever\"\n      - \"Pacing is\
  \ everything - cut dead air, maintain momentum relentlessly\"\n      - \"Thumbnails sell clicks - invest in visual psychology,\
  \ test everything\"\n      - \"Retention over length - 8 minutes at 80% beats 20 minutes at 40%\"\n      - \"Scale creates\
  \ spectacle - bigger stakes, bigger emotions, bigger views\"\n      - \"Data drives decisions - A/B test titles, thumbnails,\
  \ hooks constantly\"\n      - \"Reinvest everything - compound growth by putting revenue back into content\"\n"
---
# Content Generator

## When to Use

**Trigger phrases:**
- "content generator"
- "Help me with content generator"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


End-to-end AI video pipeline: LLM hook → NVIDIA image → BytePlus Seedance video → FFmpeg loop/compress.


## When NOT to Use

- When the content requires deep domain expertise you do not have
- For legal, medical, or financial advice content
- When real-time data is required (use live data feeds)


## Overview

Content Generator enables content production with professional quality and consistency.

## Workflow

```python
# Example: Content generation pipeline
def generate_content(topic: str, format: str = "article"):
    outline = create_outline(topic)
    draft = write_draft(outline, format)
    edited = edit_for_quality(draft)
    optimized = optimize_for_seo(edited)
    return publish(optimized)
```

1. **Define brief** — Set objectives, audience, and style guidelines
2. **Research and gather** — Collect source material and reference content
3. **Create draft** — Generate initial content following the brief
4. **Refine and edit** — Polish for quality, accuracy, and engagement
5. **Publish and distribute** — Deploy to target platforms
6. **Track performance** — Monitor engagement and iterate

## Quality Checklist

- [ ] Content matches the defined brief and audience
- [ ] All facts verified against authoritative sources
- [ ] Formatting consistent with style guidelines
- [ ] SEO/distribution optimization applied
- [ ] Call-to-action clear and compelling

## Tools

- Content management system for publishing
- Analytics platform for performance tracking
- Design tools for visual assets
- Collaboration tools for review cycles

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |