---
name: youtube-factory
description: Generate complete YouTube videos from a single prompt - script, voiceover, stock footage, captions, thumbnail.
  Self-contained, no external modules. 100% free tools.
domain: content
tags: video, youtube, content-creation, tts, automation, faceless
version: 1.3.0
author: Mayank8290
homepage: https://github.com/Mayank8290/openclaw-video-skills
metadata:
  openclaw:
    requires:
      bins:
      - ffmpeg
      - edge-tts
      env:
      - PEXELS_API_KEY
    primaryEnv: PEXELS_API_KEY
---
# Youtube Factory

## When to Use

**Trigger phrases:**
- "youtube factory"
- "Help me with youtube factory"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Generate complete YouTube videos from a single prompt. Script, voiceover, stock footage, captions, thumbnail - all automated.

**100% FREE tools** - No expensive APIs required.

> **Love this skill?** Support the creator and help keep it free: **[Buy Me a Coffee](https://buymeacoffee.com/mayank8290)**


## When NOT to Use

- When the content requires deep domain expertise you do not have
- For legal, medical, or financial advice content
- When real-time data is required (use live data feeds)


## Overview

Youtube Factory enables content production with professional quality and consistency.

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