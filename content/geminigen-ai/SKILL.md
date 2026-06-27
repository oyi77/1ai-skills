---
name: geminigen-ai
description: Unified multimedia API for image generation (nano-banana-pro, imagen-4), video generation (Grok, Veo, Sora),
  and text-to-speech. Replaces grok-video-generation, seedance, and gemini-image-generator.
domain: content
tags:
- api
- content-creation
- digital-content
- geminigen
- media
- video
---
# Geminigen Ai

## When to Use

**Trigger phrases:**
- "geminigen ai"
- "Help me with geminigen ai"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


> ✅ **CANONICAL PROVIDER** — This is the single source of truth for all media generation in the 1ai-skills stack.
> Image (nano-banana-pro) · Video (grok-3 / veo / sora) · TTS — all unified under this API.
> Replaces: `grok-video-generation`, `seedance`, `gemini-image-generator`, `content-generator` (media providers).


## When NOT to Use

- When the content requires deep domain expertise you do not have
- For legal, medical, or financial advice content
- When real-time data is required (use live data feeds)


## Overview

Geminigen Ai enables content production with professional quality and consistency.

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