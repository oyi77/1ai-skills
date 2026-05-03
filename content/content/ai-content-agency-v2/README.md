# AI Content Agency v2 - Usage Guide

## Overview

**Ultimate AI Content Agency** - 9 specialized workflows in 1 skill:
1. **etika-makan** - Creative Director Ideation (3 angles)
2. **makan-steak** - Detailing & POV Shots production
3.kan-mie** - Stitching Production (multi-provider + auto-stitching)
4. **makan-rawat** - POV Narrative Generation (Native POV shots format)
5. **makan-host** - FOMO Stack 4-Layer + Troll Logic
- **makan-latar** - Storyboarding 3-Second Rule
- **makan-visuals** - Image Prompts for AI image generation
- **makan-layar** - Lighting Specs & Mood Setup
- **makan-musik** - Audio & Voiceover Management (ElevenLabs voice + SSML)
- **makan-animasi** - Animation & Video Generation (Kling + BytePlus Seedance)
- **makan-fx** - FFmpeg & Video Effects

## Skill Structure

```
ai-content-agency-v2/
├── README.md           ← Usage guide (ini)
├── SKILL.md            ← Core concept
├── workflows/           ← 9 workflow definitions
├── sub-skills/          ← Sub-skills per workflow
└── scripts/             ← Implementation scripts
```

## Usage Pattern

### Step 1: Generate Concepts (etika-makan)
```
/api/webhook/ideation → creative_director_ideation
```

### Step 2: Production Workflow
```
/api/webhook/wf-[1-9]/ → specific workflow
```

### Step 3: Render & Stitch (kan-mie)
```
/api/webhook/wf-creatomate-stitch
```

## Quick Start

### Basic Usage (User-facing):
```
User: "Bikin video 9:16 untuk madu hutan Kalimantan"
→ skill aktif: "content-generator" → generate_tiktok_viral.py
→ output: video final (TikTok 9:16, 60s, viral)
```

### Advanced Usage (Agency Mode):
```
User: "Campaign untuk madu hutan"
→ skill aktif: "ai-content-agency-v2"
→ router: workflow_router → "wf-" + best_workflow_id
→ full pipeline: ideation → research → production → final video
```

## Workflows Overview

| Workflow ID | Name Focus | Provider(s) | Output |
|------------|-----------|----------|--------|
| 1 | wf-detailing | Detailing | NIM, BytePlus, Kling | Sensory/texture descriptions |
| 2 | wf-pov      | POV Shots | Groq/NVIDIA (LLM + Image) | POV scripts, 1-3s retention |
| 3 | wf-storyboard | Storyboard | LLM | 3-sec retention, text overlay info |
| 4 | wf-latehost  |  |  | |
| 5 | wf-imageprompt |  Image Gen | NIM | Camera specs, lighting |
|  | |  | |
|  |  |  |  |
|  |  |  | |
- |  |  |  | |
-  |  |  |  |
-  |  |  |  |
|  |  |  |  |
|  |  |  │  |  |
|  |  │  │  |  |
|  |  │  │  │
|  |  │  │  │
|  |  │  │  │
|  |  │  │  │
|  |  │  │  │
|  |  │  │  │
|  |  │  │  │
|  |  │  │  │
|  |  |  │  │
|  |  │  │  │
|  │  │  │  │  │  │
|  │  │  │  │  │
|  │  │  │  │  │
|  |  │  │  │  │  │  │
|  │  │  │  │  │ │  │ │
|  │  │  │  │  │  │ │ │  │  │
|  │  │  │  │  │ │ │  │ │  │
|  |  │  │  │  │ │ │ │ │  │  │  │  │ │ │  │ │ │ │ │  │ │  │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ ───> 10 lines from end of file
```

## Technical Details

### Providers & APIs (All Verified 2026-02-27)

| Provider | Type | Purpose | Status | Endpoint |
|----------|------|--------|--------|
| **NVIDIA NIM** | Image | ✅ WORKING | `ai.api.nvidia.com/v1/genai/` |
| **BytePlus Seedance** | Video | ✅ WORKING | `ark.ap-southeast.bytepluses.com/api/v3` |
| **Kling** | Video | ✅ WORKING | `klingai.com` |
| **ElevenLabs** | Voice | ✅ WORKING | `try.elevenlabs.com` |

### FFmpeg Filters

| Filter | Use Cases | Syntax |
|--------|------------|--------|
| scale, fps | Resize, frame rate | `scale=1080:1920,fps=30` |
| overlay | Text, graphics, logos | `drawtext:text=Text:...` |
| fade, xfade | Transitions | `fade=t=in:st=X:d=5:alpha=1` |
| zoom, pan, rotate | Camera movement | `zoom=pan=1:z=1` |
| trim, select | Clip segments | `start=X:duration=Y` |

### SSML Format (WF6 Only)

```ssml
Narasi: "Ada hal-hal yang nggak bisa dibeli.<break time='1.2s'/>Tapi bisa dijaga.<break time='0.8'/>Kayak warisan.<break time='0.5'/>Kayak tradisi.<break time='1.5'/>Dan ini, adalah cara gue menjaganya."

SSML Required:
- <break time="0.8s" />     → 0.8s pause
- <break time="1.2s" />    → 1.2s pause (emotional)
- <break time="1.5s" />    → 1.5s pause (reveal produk)
- <break time="0.5s" />     → 0.5s pause (antara frasa)
```

### Voice Formats

| Provider | Model | Style | Language Support |
|----------|-------|-------|----------------|
| ElevenLabs | 11 different | 45+ languages | ✅ Indonesian (id-ID, ms-ID) |

### Video Formats

| Format | Platform | Ratio | Use When |
|--------|---------|------|-----------|
| TikTok | 9:16 vertical | 1:00 min | TikTok viral |
| YouTube | 16:9 horizontal | 10-20 min (normal) |
| Instagram | 4:5 / 1:1 | Carousel, Reels | 15.0 min | Instagram, Reels | 15.0 min |
| YouTube Shorts | 9:16 | 30s-60s | Shorts | 30-60s |
| Stories | 9:16 | 15 sec | Stories | 15 sec |

### Quality Gates

1. **Vision QC** (WF 4) - GPT-4o Vision API
2. **HitL Gate** (WF 4.2) - Telegram approval before rendering
3. **Creatomate** (WF 5) - Auto-stitching final video

## File Structure

```
skills/1ai-skills/ai-content-agency-v2/
├── README.md
├── SKILL.md (ini file)
├── workflows/
│   │   ├── wf-detailing/
│   │   ├── wf-pov/
│   │   ├── wf-storyboard/
│   ├── sub-skills/
│   │   ├── etika-makan/
│   ├── makan-steak/
│   ├── makan-mie/
│   └── scripts/
```

---

**Skill Location:** `/home/openclaw/.openclaw/workspace/skills/ai-content-agency-v2/`

**Installed:** ✅ March 11, 20:29 UTC+7

**Ready to Use:** YES - 9 workflows active, 4 sub-skills integrated, providers verified