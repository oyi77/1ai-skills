# Remotion Skill — Onboarding Guide
# "I want to make a video. Where do I start?"

This guide walks you through the full journey from zero to rendered video.
No AI tools required. No API keys. Everything runs on your machine.

---

## What Is This Skill?

This skill teaches Claude how to build real `.mp4` videos using **Remotion** —
a framework that lets you write React components that render as video frames.

**What Remotion can do:**
- Narrated explainer videos (TTS narration, captions, chapter cards)
- Product commercials, UGC ads, TikTok/Reels short-form
- Music videos with beat-synced animations
- Movie trailers with Hollywood color grade + film grain
- Anime-style content with speed lines, smear frames, impact flashes
- Data visualizations, infographic stories
- Podcast talking-head videos with lower thirds
- Documentary / mini-doc style
- Countdown event promos, challenge videos, and more

**What it does NOT need:**
- An API key
- An AI image or video generator
- A subscription
- Internet (after initial package downloads)

---

## Prerequisites — Install These Once

### 1. Node.js (required for Remotion)
```bash
# Check if installed:
node --version   # need v18+

# If not installed: https://nodejs.org (download LTS)
```

### 2. Python 3.8+ (required for scripts)
```bash
# Check:
python3 --version

# macOS comes with Python. Windows: https://python.org
```

### 3. ffmpeg (required for audio/video processing)
```bash
# macOS:
brew install ffmpeg

# Ubuntu / Debian:
sudo apt install ffmpeg

# Windows: https://ffmpeg.org/download.html
# (add ffmpeg to PATH after install)

# Verify:
ffmpeg -version
```

### 4. Python packages (free, no API)
```bash
pip install edge-tts           # Text-to-speech (Microsoft, free, no login)
pip install openai-whisper     # Speech-to-text (runs locally, no API)
pip install librosa soundfile  # BPM detection (for music videos)
pip install Pillow             # Image processing
```

**Total install time:** ~5–10 minutes on first run.
**Internet needed after install:** Only for edge-tts (TTS generation).

---

## Path A — "I Want a Narrated Video" (Most Common)

### Step 1: Create a Remotion project

```bash
npx create-video@latest my-video
# Select: blank
cd my-video
npm install
```

### Step 2: Run setup script

```bash
python scripts/setup.py --type narrated
```

This creates:
```
public/
  audio/          ← TTS audio will go here
  images/         ← your product images / thumbnails
  video/          ← source video clips
script.json       ← your video script
README.md
```

### Step 3: Write your script

Open `public/script.json` and edit it:

```json
{
  "title": "My First Video",
  "language": "id",
  "scenes": [
    {
      "id": "intro",
      "title": "Pembukaan",
      "narration": "Halo! Selamat datang di video ini.",
      "background": "gradient-blue"
    },
    {
      "id": "main",
      "title": "Isi Utama",
      "narration": "Hari ini saya akan berbagi tips penting untuk bisnis Anda.",
      "background": "dark"
    },
    {
      "id": "outro",
      "title": "Penutup",
      "narration": "Terima kasih sudah menonton. Jangan lupa subscribe!",
      "background": "gradient-purple"
    }
  ]
}
```

**Background options:** `dark`, `gradient-blue`, `gradient-purple`, `gradient-green`

### Step 4: Generate TTS audio

```bash
# Indonesian voice:
python scripts/pipeline.py --voice id

# English voice:
python scripts/pipeline.py --voice en

# Other voices: id-f (Indonesian female), en-m (English male), zh (Chinese)
```

This generates:
- `public/audio/intro.mp3`, `main.mp3`, `outro.mp3`
- `public/timing.json` (scene durations based on audio length)

### Step 5: Copy a template into your project

```bash
# Copy the narrated starter template
cp path/to/skill/templates/narrated-video-starter.tsx src/Composition.tsx
```

Or ask Claude: *"Give me the narrated video composition for my script.json"*

### Step 6: Preview in Remotion Studio

```bash
npm run dev
# Opens http://localhost:3000
# ← Scrub the timeline, check scenes, adjust timing
```

### Step 7: Render to MP4

```bash
npx remotion render NarratedVideo out/video-raw.mp4
```

### Step 8: Post-process (add BGM, export formats)

```bash
# Put your background music at public/audio/bgm.mp3 first
./scripts/postprocess.sh --formats mp4,vertical,gif
```

Output files:
- `out/final.mp4` — standard 16:9
- `out/vertical.mp4` — 9:16 for TikTok/Reels
- `out/preview.gif` — animated preview

---

## Path B — "I Want a TikTok/Short-Form Video"

### Step 1: Create project + use the TikTok template

```bash
npx create-video@latest my-tiktok
cd my-tiktok && npm install

# Copy template
cp skill/templates/tiktok-viral-short.tsx src/Composition.tsx
```

### Step 2: Edit the CONFIG block at the top

Open `src/Composition.tsx` and find the `── CONFIG ──` section:

```tsx
const HOOK_TEXT = 'You\'ve been doing this WRONG 😱';
const BODY_LINES = [
  'Most people think they need hours...',
  'But here\'s the 3-step shortcut.',
  // ... add your lines
];
const CTA_TEXT = 'Follow for more tips 👆';
const ACCENT    = '#FFE500';   // your brand colour
```

### Step 3: Preview + render

```bash
npm run dev                                          # preview at localhost:3000
npx remotion render TikTokViral out/tiktok-raw.mp4  # render
./scripts/postprocess.sh --no-bgm --formats vertical # export 9:16
```

**Result:** `out/vertical.mp4` — ready to upload to TikTok/Reels/Shorts.

---

## Path C — "I Want a Music Video"

### Step 1: Detect BPM of your track

```bash
python scripts/bpm_detect.py public/audio/track.mp3 --save
```

Output: `public/bpm.json`
```json
{
  "bpm": 128.0,
  "framesPerBeat": 14,
  "framesPerBar": 56,
  "beatFrames": [0, 14, 28, ...]
}
```

### Step 2: Copy the music video template

```bash
cp skill/templates/music-video-lyric.tsx src/Composition.tsx
```

### Step 3: Edit CONFIG — set BPM and lyrics

```tsx
const BPM        = 128;       // ← from bpm.json
const AUDIO_FILE = 'audio/track.mp3';

const LYRICS = [
  { text: 'Your first lyric line', beatStart: 0  },
  { text: 'Second line here',      beatStart: 4  },
  { text: 'CHORUS GOES HERE',      beatStart: 16 },
];
```

### Step 4: Render

```bash
npm run dev
npx remotion render MusicVideo out/mv-raw.mp4
./scripts/postprocess.sh --no-bgm --formats mp4,vertical
```

---

## Path D — "I Want a Video With Automatic Captions"

### Step 1: Generate captions from your audio (no API, local only)

```bash
python scripts/transcribe.py public/audio/narration.mp3 --lang id
```

This uses **OpenAI Whisper running on your machine**. No internet needed after model download.

Output:
- `public/captions.json` — word-level timing for Remotion
- `public/captions.srt` — standard subtitle file

### Step 2: Import captions in your composition

```tsx
import captionsData from '../public/captions.json';

// Use with @remotion/captions:
import { createTikTokStyleCaptions } from '@remotion/captions';
const { pages } = createTikTokStyleCaptions({ captions: captionsData });
```

### Step 3: Burn captions into final video (alternative to in-video captions)

```bash
# After rendering:
./scripts/postprocess.sh --formats mp4   # auto-detects public/captions.srt
```

---

## Path E — "I Just Want to Use a Template"

If you're not sure what you need, pick from the template table:

| I want to make... | Use this template | Format |
|---|---|---|
| A narrated explainer | `narrated-video-starter.tsx` | 16:9 |
| A TikTok/Reels video | `tiktok-viral-short.tsx` | 9:16 |
| A product commercial | `product-launch-commercial.tsx` | 16:9 |
| A YouTube tutorial | `youtube-tutorial.tsx` | 16:9 |
| A music video | `music-video-lyric.tsx` | 16:9 |
| A data story/infographic | `data-story-infographic.tsx` | 16:9 |
| A movie trailer | `movie-trailer-cinematic.tsx` | 16:9 |
| A UGC / testimonial ad | `ugc-testimonial-ad.tsx` | 9:16 |
| A podcast video | `podcast-talking-head.tsx` | 16:9 |
| A brand logo intro | `brand-logo-intro.tsx` | 16:9 |
| A challenge video | `viral-challenge-gameshow.tsx` | 16:9 |
| An ASMR product reveal | `asmr-product-reveal.tsx` | 9:16 |
| An event countdown | `countdown-event-promo.tsx` | 16:9 |

**Steps for any template:**
1. `npx create-video@latest my-project` → select `blank`
2. `cd my-project && npm install`
3. Copy template file to `src/Composition.tsx`
4. Edit the `── CONFIG ──` block at the top of the file
5. `npm run dev` → preview
6. `npx remotion render [CompositionId] out/video.mp4` → render

---

## Troubleshooting

### "command not found: npx"
Install Node.js from https://nodejs.org (LTS version)

### "command not found: ffmpeg"
```bash
brew install ffmpeg      # macOS
apt install ffmpeg       # Ubuntu
```

### "ModuleNotFoundError: No module named 'edge_tts'"
```bash
pip install edge-tts
```

### "ModuleNotFoundError: No module named 'whisper'"
```bash
pip install openai-whisper
```

### Remotion Studio shows blank white screen
- Check `src/Root.tsx` — does it export `RemotionRoot`?
- Check the entry point is registered: `remotion.config.ts` or `package.json`

### Audio not syncing with video
- Always use `startFrom={paddingFrames}` on `<Audio>` in sequences
- Check `public/timing.json` was generated after audio files

### Video renders too slowly
```bash
# Use half-size for preview renders:
npx remotion render MyComp out/preview.mp4 --scale 0.5

# Full quality for final:
npx remotion render MyComp out/final.mp4 --crf 18
```

### "Cannot find module '../public/timing.json'"
Run the pipeline first:
```bash
python scripts/pipeline.py --voice id
```

---

## Quick Reference — All Scripts

```bash
# Setup
python scripts/setup.py --type narrated

# TTS + timing
python scripts/pipeline.py --voice id

# Transcribe audio → captions (local, no API)
python scripts/transcribe.py public/audio/narration.mp3 --lang id

# Detect BPM for music videos
python scripts/bpm_detect.py public/audio/track.mp3 --save

# Convert captions.json ↔ .srt
python scripts/caption_to_srt.py public/captions.json

# Prepare images + video assets
python scripts/prepare_assets.py --format 9:16

# Render all compositions
./scripts/batch_render.sh

# Post-process: BGM + subtitles + multi-format export
./scripts/postprocess.sh --formats mp4,vertical,gif
```

## Quick Reference — Remotion Commands

```bash
npm run dev                                        # Studio preview
npx remotion render MyComp out/video.mp4           # Render MP4
npx remotion render MyComp out/video.gif --codec gif  # Render GIF
npx remotion render --scale 0.5                    # Half-size (fast preview)
npx remotion still MyComp out/thumb.jpg --frame 30 # Single frame thumbnail
npx remotion compositions                          # List all compositions
```

---

## Voice Codes for TTS (edge-tts, all free)

| Code | Language | Gender | Voice |
|------|----------|--------|-------|
| `id` | Indonesian | Male | ArdiNeural |
| `id-f` | Indonesian | Female | GadisNeural |
| `en` | English | Female | JennyNeural |
| `en-m` | English | Male | GuyNeural |
| `zh` | Chinese | Female | XiaoxiaoNeural |
| `zh-m` | Chinese | Male | YunxiNeural |

Usage: `python scripts/pipeline.py --voice id`

---

## What To Ask Claude

Once you have a project set up, you can ask Claude things like:

- *"Create a 3-scene narrated video about [topic] in Indonesian"*
- *"Build me a TikTok hook for a product called [name]"*
- *"Add a karaoke lyric reveal component with fill animation"*
- *"Make a product reveal scene with slow spotlight animation"*
- *"Generate a timing.json for these 4 scenes: [list scenes]"*
- *"Write a script.json for a tutorial video about [topic] with 5 steps"*
- *"Add Hollywood color grade and film grain to my composition"*
- *"Create a before/after split reveal for my before.mp4 and after.mp4"*

Claude will use this skill to write working Remotion code directly.
