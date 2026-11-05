---
name: role-content-creator
description: "Use when creating and managing multi-format content assets. Covers production workflows, brand consistency, and distribution across digital channels."
domain: content
author: oyi77
version: 1.0.0
category: content
tags:
- content
- writing
- production
- brand
- distribution
license: Apache-2.0
subdomain: content-creation
triggers:
- content creator role
- content production workflows
- media asset management
- content pipeline orchestration
---

# Role Content Creator

## Overview

Content without structured production workflow, canonical asset library, and automated approval gate does not scale. The content creator enforces strict asset governance, content templatization, version control, and distribution pipelines across all digital channels.

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
| Text & writing | `content/writing` | Articles, documentation, blog posts |
| Video production | `content/video/gen` | Videos, reels, clips |
| Image creation | `content/image-gen` (DALL-E) | Generated images |
| Audio production | `content/voice-ai` | Voiceovers, speech-to-text |
| Distribution | `integrations/slack` (notification) | Delivery via Slack, Discord |
| Content templates | `content/brand` | Brand guidelines, style guides |

## Workflow

### Phase 1: Content Planning & Asset Definition

1. **Identify** content pillar, target audience, format, channel.
2. **Set up** content templates: headline, intro, body, CTA, author credit.
3. **Define** asset specifications: file type, size, compression, metadata.

### Phase 2: Asset Production & Versioning

1. **Script** and shoot text/video/audio assets via editors (writing, video, audio).
2. **Upload** assets to CDN or internal repository.
3. **Apply** version control: Git tags, asset IDs, and version numbering.

### Phase 3: Approval & Review

1. **Approve** content: editor review, brand sign-off, compliance.
2. **QA** assets: length, quality, readability, formatting.
3. **Publish** approved assets to distribution channels.

### Phase 4: Distribution & Scheduling

1. **Push** assets to web, email, social, mobile channels (via CDN, social, and email).
2. **Schedule** posts, optimize times, track performance.
3. **Monitor** analytics: impressions, clicks, conversions.

### Phase 5: Analytics & Optimization

1. **Track** content performance: engagement, bounce rates, conversion.
2. **Iterate** content formats, headlines, images using data.
3. **Archive** underperforming content; set up renewal cycles.

## Anti-Rationalization

| Content Excuse | Flawed Rationalization | Required Content Discipline |
|---|---|---|
| "Audience just reads top line" | "We'll reuse high-performing headers" | Structured copy hierarchy: headline, subhead, body |
| "Brand is just vibe" | "We'll decide later" | Brand guidelines enforced per channel |
| "Video is easy" | "We'll record on fly" | Script first, shoot second, edit third |

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

### Content Template Validator (bash)

```bash
#!/usr/bin/env bash
# Content template validator
# Validates a content YAML file for required fields

TEMPLATE_FILE=${1:-/tmp/content_template.yaml}
if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Error: Template file $TEMPLATE_FILE not found"
  exit 1
fi

REQUIRED_FIELDS="title body cta"
MISSING=0

for field in $REQUIRED_FIELDS; do
  if ! grep -qE "^[[:space:]]+- $field$" "$TEMPLATE_FILE"; then
    echo "FAIL: Missing required field '$field'"
    MISSING=$((MISSING + 1))
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "SUCCESS: Template is compliant"
  exit 0
else
  echo "FAIL: Template missing $MISSING required field(s)"
  exit 1
fi
```

## Verification Checklist

- [ ] Content templates defined; structure, compliance, author credit
- [ ] Assets produced: video, image, audio, text
- [ ] Assets reviewed: quality, length, readability
- [ ] Distribution channels active; schedule live
- [ ] Analytics live; engagement tracked