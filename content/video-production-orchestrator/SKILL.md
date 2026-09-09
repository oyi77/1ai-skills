---
name: video-production-orchestrator
description: "The single entry point for ALL video generation and editing needs. Analyzes user intent and routes to the right workflow — HyperFrames (product-launch, motion-graphics, faceless-explainer, changelog, captions), Remotion (React), FFmpeg (programmatic), auto-clipper (highlights), content-factory (YouTube), or slides. Use when the user says 'make a video', 'create video', 'edit video', or any video production request; this skill decides WHICH tool fits the ask."
domain: "content-creation"
tags:
  - video
  - orchestrator
  - router
  - hyperframes
  - remotion
  - ffmpeg
  - content-factory
  - auto-clipper
  - slides
  - production
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill orchestrates the video production pipeline across HyperFrames templates, from intake brief to rendered MP4. Use it when multiple video assets must be produced in a batch or on a schedule. It sequences briefing, composition, render, and QA so the line never stalls.


# Video Production Orchestrator

The single entry point for ALL video generation and editing needs. Analyzes intent and routes to the right workflow.

## When to Use

- User says **"make a video"**, **"create video"**, **"generate video"**
- User says **"edit video"**, **"clip video"**, **"trim video"**
- User says **"add captions"**, **"add subtitles"**, **"burn subtitles"**
- User says **"product video"**, **"launch video"**, **"promo video"**
- User says **"explainer"**, **"tutorial"**, **"how-to video"**
- User says **"motion graphics"**, **"kinetic type"**, **"logo sting"**
- User says **"changelog video"**, **"weekly digest video"**
- User says **"presentation"**, **"slides"**, **"deck"**
- User says **"clip highlights"**, **"shorts"**, **"reels"**
- Any video production request where the tool/workflow is unspecified

## When NOT to Use

- User explicitly names a specific skill (e.g., "use hyperframes-product-launch-video")
- User wants image generation (use image-generation skills)
- User wants audio-only (use TTS/music skills)
- User wants to edit an existing video file directly (use ffmpeg or video editing tools)

## Workflow

### 1 · Analyze intent

Parse the user's request for signals:
- Source material (URL, text, existing footage, none)
- Purpose (marketing, education, social, presentation)
- Explicit tool mentions (HyperFrames, Remotion, FFmpeg)

### 2 · Route to workflow

Match signals to the correct skill using the Intent Router table below.

### 3 · Explain the route

Tell the user which workflow was chosen and why (one sentence).

### 4 · Hand off

Read the target skill and follow its workflow.

## Intent Router

### 1. Product / Launch / Promo Video

**Signals:** product URL, "launch", "promo", "marketing", "showcase", "site tour"

**Route to:** `hyperframes-product-launch-video`

**Capabilities:**
- Website capture → animated product video
- Brand-aware design system (frame.md)
- Kinetic captions, BGM, voiceover
- 30-90s sweet spot, up to 3 min

### 2. Motion Graphics / Kinetic Type / Logo Sting

**Signals:** "motion graphics", "kinetic type", "logo sting", "lower-third", "animated headline"

**Route to:** `hyperframes-motion-graphics`

**Capabilities:**
- Short, unnarrated, design-led (~under 10s)
- Kinetic type, stat/chart hits, logo stings
- Transparent overlay output (ProRes 4444)
- 2-3 transition budget rule

### 3. Talking Head / Interview / Podcast + Graphics

**Signals:** "talking head", "interview", "podcast", "add graphics", "lower-thirds", "data callouts"

**Route to:** `hyperframes-talking-head-recut`

**Capabilities:**
- Layer timed graphic cards onto existing footage
- Transcript-synced (local Whisper)
- Footage plays untouched underneath
- Card count formula: `max(5, round(duration / (basePace × densityMultiplier)))`

### 4. Faceless Explainer / Concept / How-To

**Signals:** "explainer", "concept", "how-to", "tutorial", "breakdown", "listicles", "data-viz"

**Route to:** `hyperframes-faceless-explainer`

**Capabilities:**
- No product/website to capture — visuals invented per scene
- Frame preset design system
- Narrative-driven storyboard
- Sub-agent frame dispatch

### 5. Changelog / Digest Video

**Signals:** "changelog", "weekly digest", "release notes", "what's new"

**Route to:** `hyperframes-changelog-video`

**Capabilities:**
- Markdown → branded video pipeline
- Mock-UI visualizations (not bullet points)
- Annie VO (HeyGen) + word timestamps
- Square 1080, ~45-60s

### 6. Embedded Captions / Subtitles

**Signals:** "add captions", "subtitles", "burn subtitles", "caption rail"

**Route to:** `hyperframes-embedded-captions`

**Capabilities:**
- Drop/rail/embed caption model
- Overlay law (captions are NOT a reserved band)
- Matte occlusion for embedded climaxes
- Word-timestamp alignment from TTS

### 7. Presentation / Slides / Deck

**Signals:** "presentation", "slides", "deck", "pitch deck", "PowerPoint"

**Route to:** `content/slides` skill

**Capabilities:**
- Discrete slides, fragment reveals
- Branching, hotspot navigation
- Presenter mode
- Output is navigable deck (not rendered video)

### 8. Programmatic Video (FFmpeg)

**Signals:** "convert video", "compress", "resize", "extract audio", "merge videos", "add watermark"

**Route to:** Direct FFmpeg commands or `content/auto-clipper` for highlights

**Capabilities:**
- Format conversion, compression, resizing
- Audio extraction, merging
- Watermarking, subtitle burn-in
- Batch processing

### 9. YouTube / Faceless Channel Content

**Signals:** "YouTube video", "faceless channel", "content factory", "generate video from prompt"

**Route to:** `content/content-factory` skill

**Capabilities:**
- Full video from prompts
- Script → scenes → audio → video pipeline
- Vertical Shorts from text
- Long-form video assembly

### 10. Video Highlights / Clips / Shorts

**Signals:** "clip highlights", "shorts", "reels", "tiktok clips", "best moments"

**Route to:** `content/auto-clipper` skill

**Capabilities:**
- FFmpeg + AI scene detection
- Long video → short engaging highlights
- TikTok/Reels/YouTube Shorts optimized

## Decision Tree

```
Is the request explicitly about video?
├── No → Not this orchestrator
└── Yes → What type?
    ├── Product/Launch/Promo → hyperframes-product-launch-video
    ├── Motion Graphics/Logo → hyperframes-motion-graphics
    ├── Talking Head + Graphics → hyperframes-talking-head-recut
    ├── Faceless Explainer → hyperframes-faceless-explainer
    ├── Changelog/Digest → hyperframes-changelog-video
    ├── Captions/Subtitles → hyperframes-embedded-captions
    ├── Presentation/Slides → content/slides
    ├── Programmatic/Convert → FFmpeg / auto-clipper
    ├── YouTube/Channel → content/content-factory
    └── Unclear → Ask 1-2 clarifying questions
```

## Clarification Questions (when intent is unclear)

Ask at most 2 questions:

1. **Source:** "What's the source material? (product URL, article/text, existing video, or from scratch)"
2. **Purpose:** "What's the purpose? (marketing/promo, education/explainer, social media, presentation)"

Then route based on the answers.

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll just use FFmpeg for everything" | FFmpeg is for programmatic edits, not creative production |
| "I'll use HyperFrames for everything" | HyperFrames is for HTML-based video; existing footage needs talking-head-recut |
| "I'll ask the user to pick the skill" | The orchestrator decides — don't push routing to the user |
| "I'll skip the orchestrator and guess" | Wrong tool = wasted effort. Route deliberately. |
| "I'll use Remotion for everything" | Remotion is React-based; HTML is simpler for agents. Use HyperFrames unless React is specifically needed. |

## Verification

- [ ] Intent matched to correct workflow
- [ ] User didn't have to pick the tool (orchestrator decided)
- [ ] Route explanation provided to user
- [ ] Next steps clear (which skill to read next)
