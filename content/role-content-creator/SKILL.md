---
name: role-content-creator
description: "Use when creating, editing, and managing content assets: text, images, video, audio, scripts, and multi-format assets. Covers content production workflows, version control, brand consistency, optimization, and distribution across channels."
domain: content
author: oyi77
version: 1.0.0
category: content
tags:
- content
- writing
- video
- audio
- editing
- production
- distribution
- brand
- optimization
license: Apache-2.0
subdomain: content-creation
triggers:
- content creator role
- content production workflows
- media asset management
- content pipeline orchestration
---

## Overview

Content without a structured production workflow, a canonical asset library, and an automated approval gate does not scale. The engineering behind that gate is a content production stack with content types, versions, assets, approvals, and distribution channels.

The content creator enforces strict asset governance, content templatization, version control, and distribution pipelines across all digital channels.

## When to Use

- When designing content pipelines for multi-format publishing (text, images, video, audio, scripts).
- When setting up content versions, asset management, and asset publishing workflows.
- When building content templates, brand guidelines, and accessibility standards.
- When managing content distribution: CDN, social, web, and email channels.
- When setting up content approval workflows, reviews, and final release gates.

## When NOT to Use

- When writing code, scripts, or API endpoints (use `development/role-software-engineer`).
- When managing sales pipeline or CRM (use `sales/role-sales-engineer`).
- When building design visuals or UI (use `content/role-ui-ux-designer`).

## Deterministic Dispatch Matrix

| Content Objective / Workflow | Delegated Child Skill | Primary Content Artifact |
|---|---|---|
| Text & writing | `content/variant/writing` | Articles, documentation, blog posts |
| Video production | `content/video-gen` | Videos, reels, clips |
| Image creation | `content/image-gen` (DALL-E) | Generated images |
| Audio production | `content/voice-ai` | Voiceovers, speech-to-text |
| Distribution | `integrations/slack` (notification) | Delivery via Slack, Discord |
| Content templates | `content/brand` | Brand guidelines, style guides |
| Version control | `content/content-version` | Asset versions, changelog |

## Workflow

### Phase 1: Content Planning & Asset Definition

1. Identify content pillar, target audience, format, channel.
2. Set up content templates: headline, intro, body, CTA, author credit.
3. Define asset specifications: file type, size, compression, metadata.

### Phase 2: Asset Production & Versioning

1. Script and shoot text/video/audio assets via editors (writing, video, audio).
2. Upload assets to CDN or internal repository.
3. Apply version control: Git tags, asset IDs, and version numbering.

### Phase 3: Approval & Review

1. Content approval: editor review, brand sign-off, compliance.
2. Set up asset QA: length, quality, readability, formatting.
3. Publish approved assets to distribution channels.

### Phase 4: Distribution & Scheduling

1. Push assets to web, email, social, mobile channels (via CDN, CDN, email).
2. Schedule posts, optimize times, track performance.
3. Monitor analytics: impressions, clicks, conversions.

### Phase  thiên hậu: Analytics & Optimization

1. Track content performance: engagement, bounce rates, conversion.
2. Use data to iterate content formats, headlines, images.
3. Archive underperforming content; set up renewal cycles.

## Anti-Rationalization

| Content Excuse | Flawed Rationalization | Required Content Discipline |
|---|---|---|
| "Audience just reads the top line" | "We'll reuse high-performing headers" | Structured copy hierarchy: headline, subhead, body |
| "Brand is just vibe" | "We'll decide later" | Brand guidelines enforced per channel |
| "Video is easy" | "We'll record on the fly" | Script first, shoot second, edit third |

## Implementation Examples

### Content Template YAML

```yaml
content_templates:
  article:
    structure:
      - title
      - lead
      - body
      - author_note
      - cta
    compliance:
      - fact_check_required: true
```

### Video Production Bash

```bash
#!/usr/bin/env bash
# Video production pipeline
# Takes: script, cast, editing time, output format

SCRIPT=$(cat /tmp/script.txt)
CAST=$(cat /tmp/cast.txt)
OUTFORMAT=$(cat /tmp/format.txt)

# Write script to video storyboard

echo "$SCRIPT" > /tmp/video_storyboard.txt

# Generate video via some video tool (placeholder)
echo "video generated" > /tmp/video_output.mp4

# Post-process: compression, metadata
echo "metadata added" > /tmp/video_meta.yaml
```

## Verification Checklist

- [ ] Content templates defined; structure, compliance, author credit
- [ ] Assets produced: video, image, audio, text
- [ ] Assets reviewed: quality, length, readability
- [ ] Distribution channels active; schedule live
- [ ] Analytics live; engagement tracked
- [ ] Asset versions managed; version history maintained