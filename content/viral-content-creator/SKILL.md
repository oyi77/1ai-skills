---
name: viral-content-creator
description: Use when generating 50+ video variations from one product image with hook-based A/B testing, viral score prediction, autopilot scheduling.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content
- media
- testing
- video
- viral
version: 1.0.0
category: content
---

# Viral Content Creator

## When to Use

**Trigger phrases:**
- "hook-based A/B testing"
- "viral score prediction"
- "autopilot scheduling"
- "generate 50+ variations"

**Use cases:**
- Dub product video into 5 languages using `voice-ai` + `voice-chatterbox-tts`, then clip top-performing hooks via `auto-clipper`.
- Generate 100+ variant ads from one image using `remotion` compositions, iterating hooks based on `kalodata-product-research` trends.
- Create a high-velocity "viral loop" campaign: auto-generate clips -> test hooks -> scale winners -> distribute via `multi-platform-distribution`.

## When NOT to Use

- For deep voice synthesis without hooks (use `voice-ai`).
- For high-fidelity bespoke animation (use `remotion`).
- For simple clip extraction without AI-score prediction (use `auto-clipper`).

## Overview

Viral Content Creator is a high-velocity engine for maximizing content "hit rate" via programmatic variation. Virality is defined not by raw views, but by **share velocity** (shares/view ratio), **comment-to-view ratio**, and **watch-through rate**. It leverages a "Generate -> Test -> Scale" loop to find the winning combination of hook, audio, and visual timing for specific platform thresholds (e.g., TikTok's 2-second drop-off cliff).

## Process

1. **Hook Mining** — Use `kalodata-product-research` to extract top 1% winning hooks for the product niche (`kalodata-product-research 1%`).
2. **Score Prediction** — Filter hooks through a virality model to predict "Share Probability" and "Retention Score".
3. **Programmatic Generation** — Generate variations using `remotion` and `voice-ai` (`kalodata-product-research 1%`).
```bash
npx remotion render src/index.tsx out.mp4 --props='{"hook": "Winner_1", "audio": "Voice_A"}'
```
4. **A/B Testing** — Distribute small batches via `multi-platform-distribution` to measure real-time retention.
5. **Scale & Distribute** — Amplify the top 3 variations across all accounts.

## Quality Checklist

- [ ] Hook score >= 70% on at least 3 target clips.
- [ ] Share rate > 12% in a statistically significant test group.
- [ ] Comment-to-view ratio >= 2% for high-intent hooks.
- [ ] All audio synchronized with visual cuts within +- 2 frames.

## Tools

- `voice-ai` (Narrations & Voiceovers)
- `voice-chatterbox-tts` (Local high-fidelity cloning)
- `remotion` (Programmatic video rendering)
- `auto-clipper` (Smart highlight extraction)
- `kalodata-product-research` (Trend & Hook mining)
- `multi-platform-distribution` (Automated publishing)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "One great video is enough" | Algorithm variance means a single hit is luck; 50 variations make a hit inevitable. |
| "Manual editing is higher quality" | Human editors cannot A/B test 100 hooks in 24 hours. Programmatic scale wins. |
| "Views = Virality" | Views are a vanity metric. Only share velocity and retention prove a viral hook. |

## Verification

- [ ] Output MP4s verified for target platform aspect ratios (9:16).
- [ ] Audio-visual sync verified via `remotion` frame-check.
- [ ] Hook variations verified to be distinct in sentiment and pacing.
- [ ] Distribution logs confirm 100% delivery to target platform API.