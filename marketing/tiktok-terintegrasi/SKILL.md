---
name: tiktok-terintegrasi
description: Integrated TikTok content suite with 9 specialized workflows — generates 9:16 videos and images using NVIDIA
  NIM, BytePlus Seedance, Kling AI, and ElevenLabs TTS.
domain: marketing
tags:
- growth
- marketing
- seo
- terintegrasi
- text-to-speech
- tiktok
- video
- workflow
---
# Tiktok Terintegrasi

## When to Use

**Trigger phrases:**
- "tiktok terintegrasi"
- "Help me with tiktok terintegrasi"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

r = requests.post(f"{BASE_URL}/media/create-upload-url", headers=HEADERS,
    json={"name": "video.mp4", "mime_type": "video/mp4", "size_bytes": size})
media_id, upload_url = r.json()["media_id"], r.json()["upload_url"]
requests.put(upload_url, data=open(path,"rb"), headers={"Content-Type": "video/mp4"})

# 2. Create post (media REQUIRED for Instagram)
requests.post(f"{BASE_URL}/posts", headers=HEADERS, json={
    "caption": caption, "scheduled_at": scheduled_at,
    "social_accounts": account_ids, "media": [media_id]
})

# 3. Verify (always!)
results = requests.get(f"{BASE_URL}/post-results", headers=HEADERS).json()
```

**Full reference:** `~/.openclaw/workspace/skills/postbridge-social-manager/SKILL.md`

## Overview

Tiktok Terintegrasi drives growth marketing with data-driven strategies.

## Workflow

1. **Research** — Analyze market, competitors, and audience
2. **Strategy** — Define goals, channels, and messaging
3. **Create** — Develop content and creative assets
4. **Launch** — Deploy campaigns across channels
5. **Optimize** — A/B test and iterate based on data
6. **Report** — Track KPIs and ROI

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel

