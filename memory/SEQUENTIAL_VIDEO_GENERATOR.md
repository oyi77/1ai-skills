# Sequential Video Generator - Implementation Notes

**Date:** 2026-02-27
**Status:** Partially implemented (Scene 1 working, need debug for Scene 2+)

## Method (Paijo's Requirement)

Metode yang benar untuk bikin konten nyambung:

1. **Generate base image** → sebagai anchor untuk consistency
2. **Generate storyboard** → alur cerita yang logical
3. **Chain generate videos:**
   - Scene 1: Base image → generate video → extract last frame
   - Scene 2: Last frame dari scene 1 → generate next → extract last frame
   - Scene 3: Last frame dari scene 2 → generate next → extract last frame
   - dst.
4. **Concatenate** → gabung semua video dengan smooth transitions

## Implementation Status

### ✅ Working
- Base image generation (NVIDIA Flux)
- Storyboard generation (5 scenes per concept)
- Scene 1 T2V generation (5.4MB video)
- Last frame extraction (FFmpeg)
- Basic concatenation (without crossfade)

### ⏳ In Progress
- Scene 2+ sequential chaining
- I2V chaining with image conditioning
- Crossfade transitions (xfade filter)

### ❌ Known Issues
- BytePlus API latency (30-120s per scene)
- NVIDIA API 500 errors (intermittent)
- Code bugs (API response format, variable naming)

## Files

**Main Script:**
- `/home/openclaw/.openclaw/workspace/skills/content-generator/scripts/sequential_video_generator.py`

**Dependencies:**
- NVIDIA Flux (base image generation)
- BytePlus Seedance (video generation T2V/I2V)
- FFmpeg (frame extraction, concatenation, transitions)

## API Response Formats

### BytePlus API (Video Generation)

**Request:**
```json
{
  "model": "seedance-1-0-pro-250528",
  "content": [
    {"type": "text", "text": "Beautiful kitchen, modern design"},
  ],
  "parameters": {
    "aspect_ratio": "9:16"
  }
}
```

**Response (Submit):**
```json
{
  "id": "cgt-20260227221715-7slwc"
}
```

**Response (Status Check):**
```json
{
  "id": "cgt-20260227221715-7slwc",
  "status": "running",  // "queued", "running", "succeeded", "failed"
  "created_at": 1772201835,
  "updated_at": 1772201835
}
```

**Response (Success):**
```json
{
  "id": "cgt-20260227221715-7slwc",
  "status": "succeeded",
  "content": {
    "video_url": "https://..."
  }
}
```

**Key Points:**
- Task ID in `id` field, NOT `task_id`
- Video URL in `content.video_url`, NOT `result.video.url`

## Next Steps

1. **Debug Scene 2+ chaining**
   - Fix variable naming issues
   - Ensure scene_index iteration is correct

2. **Implement I2V chaining**
   - Use last frame as base64 input for next scene
   - Test consistency across scenes

3. **Add crossfade transitions**
   - Use FFmpeg xfade filter
   - Set transition duration (0.5s default)

4. **Optimize for speed**
   - Parallel generation (all scenes simultaneously)
   - Use faster models (lite version)

## Alternative Approach

For now, **independent generation + crossfade transitions** is sufficient for portfolio and client samples.

The sequential chaining approach is better for:
- Long-form content (60s+)
- Storytelling videos
- Consistent characters/objects

For 15s TikTok clips, independent generation is acceptable.

*Last Updated: 2026-02-27*
