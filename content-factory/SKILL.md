---
name: content-factory
description: All-in-one YouTube content generator - create regular videos, Shorts from scratch, and Shorts from long videos. Combines best of youtube-factory and AI-Youtube-Shorts-Generator with 100% free tools.
version: 1.0.0
author: Mayank8290
homepage: https://github.com/Mayank8290/openclaw-video-skills
tags: video, youtube, shorts, content-creation, tts, automation, faceless, ai-generation
metadata: { "openclaw": { "requires": { "bins": ["ffmpeg", "edge-tts"], "env": ["PEXELS_API_KEY"] }, "primaryEnv": "PEXELS_API_KEY" }, "clawhub": { "support": "https://buymeacoffee.com/mayank8290", "cryptoTip": "https://tip.md/oyi77" } }
---

# Content Factory

All-in-one YouTube content generator. Create regular videos, Shorts from scratch, and convert long videos into Shorts. Combines the best of **youtube-factory** and **AI-Youtube-Shorts-Generator** with 100% free tools.

**Three powerful modes in one skill:**
1. **Regular Video Mode** - Generate complete YouTube videos from prompts
2. **Shorts from Scratch** - Create vertical Shorts from text prompts
3. **Shorts from Long** - Convert long videos into engaging Shorts

> **Love this skill? Support the creator!**
>
> [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/mayank8290)
>
> [![Tip in Crypto](https://tip.md/badge.svg)](https://tip.md/oyi77)

## What This Skill Does

### 🎬 Regular Video Mode
Turn any topic into a publish-ready YouTube video:
- **Script Generation** - Uses your LLM to write engaging scripts
- **Voiceover** - Free Microsoft Edge TTS (natural-sounding voices)
- **Stock Footage** - Auto-fetches relevant B-roll from Pexels (free)
- **Video Assembly** - FFmpeg combines everything seamlessly
- **Captions** - Styled subtitles burned into video
- **Thumbnail** - Auto-generated clickable thumbnail

### 📱 Shorts from Long Mode
Convert long videos (YouTube or local) into viral Shorts:
- **Smart Download** - Supports YouTube URLs via yt-dlp
- **AI Transcription** - Whisper for accurate speech-to-text (optional)
- **Highlight Detection** - AI finds the most engaging segments
- **Vertical Cropping** - Intelligent 9:16 crop focused on center
- **Caption Extraction** - Extracts text from highlighted segment
- **Multiple Sessions** - Running concurrently without conflicts

### ⚡ Shorts from Scratch Mode
Create viral Shorts from text prompts:
- **Short Scripts** - Optimized for 60-second format
- **Snap Voiceover** - Quick TTS generation
- **Vertical Stock** - Pexels videos pre-cropped for Shorts

## Quick Start

### Regular Video
```
Create a YouTube video about "5 Morning Habits of Successful People"
```

### Shorts from Long Video
```
Convert this YouTube video to Shorts: https://youtu.be/VIDEO_ID
```

### Shorts from Scratch
```
Make a YouTube Short about "surprising facts about coffee"
```

## Commands

### Generate Regular Video
```
/content-factory [topic]
```
Creates complete YouTube video with all elements.

### Generate Shorts from Long
```
/content-factory "https://youtu.be/VIDEO_ID" --shorts
/content-factory "/path/to/video.mp4" --shorts
```
Converts long video to vertical Shorts.

### Generate Shorts from Scratch
```
/content-factory [topic] --shorts
```
Creates Shorts from text prompt.

### Custom Options
```
/content-factory [topic] --style documentary --length 10
/content-factory [topic] --voice en-US-JennyNeural
/content-factory --shorts --duration 45
```

## Video Styles
- `documentary` - Serious, informative (default)
- `listicle` - "Top 10" format with clear sections
- `tutorial` - Step-by-step instructional
- `casual` - Friendly, conversational tone

## TTS Voices
Free Microsoft Edge TTS voices:
- `en-US-ChristopherNeural` - Male, professional (default)
- `en-US-JennyNeural` - Female, friendly
- `en-US-GuyNeural` - Male, casual
- `en-US-AriaNeural` - Female, news anchor
- `en-GB-SoniaNeural` - British female
- `en-AU-NatashaNeural` - Australian female

## Output Files

### Regular Videos
After generation, you'll find in `~/Videos/OpenClaw/`:
```
your-video-title/
├── script.md          # The full script
├── voiceover.mp3      # Audio track
├── video_raw.mp4      # Without captions
├── video_final.mp4    # With captions (upload this!)
├── thumbnail.jpg      # YouTube thumbnail
└── metadata.json      # Title, description, tags
```

### Shorts
```
video-title/
├── source.mp4         # Original long video
├── audio.wav          # Extracted audio
├── video_short_cropped.mp4  # Extracted segment
├── video_short.mp4    # Final vertical short
└── captions.txt       # Captions for the short
```

## Requirements

### Basic (All Modes)
- FFmpeg installed (`brew install ffmpeg` or `apt install ffmpeg`)
- Edge TTS (`pip install edge-tts`)

### Regular Videos
- Free Pexels API key (get at https://pexels.com/api)

### Shorts from Long (Optional AI Features)
- OpenAI Whisper for transcription (`pip install openai-whisper`)
- yt-dlp for YouTube downloads (`pip install yt-dlp`)

## Setup

### Install Dependencies

**macOS:**
```bash
brew install ffmpeg
pip install edge-tts pillow python-dotenv requests
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
pip install edge-tts pillow python-dotenv requests
```

**Windows:**
```bash
# Install FFmpeg from https://ffmpeg.org/download.html
pip install edge-tts pillow python-dotenv requests
```

### Optional: AI Features
```bash
pip install openai-whisper yt-dlp
```

### Configure API Keys
Create config directory:
```bash
mkdir -p ~/.openclaw-content-factory
```

Add Pexels API key:
```bash
echo "PEXELS_API_KEY=your_key" >> ~/.openclaw-content-factory/config.env
```

Optional: OpenAI API key (for advanced features):
```bash
echo "OPENAI_API_KEY=your_key" >> ~/.openclaw-content-factory/config.env
```

Optional: Configure defaults:
```bash
echo "DEFAULT_VOICE=en-US-ChristopherNeural" >> ~/.openclaw-content-factory/config.env
echo "WHISPER_MODEL=base" >> ~/.openclaw-content-factory/config.env
```

## Features

### ✨ Regular Video Mode
- 100% free stock footage from Pexels
- Natural-sounding voiceover with edge-tts
- Professional captions burned into video
- Auto-generated thumbnails
- Metadata for YouTube upload

### 🚀 Shorts from Long Mode
- YouTube video download support
- Local video file support
- Whisper AI transcription (optional)
- Smart highlight detection
- Intelligent vertical cropping
- Fast processing (< 2 minutes for 5 min video)
- Concurrent execution support

### ⚡ Shorts from Scratch Mode
- Quick script generation
- Snap TTS processing
- Vertical stock footage
- Optimized for 60-second format

## Monetization

| Method | Potential |
|--------|-----------|
| Fiverr/Upwork service | $200-500/video |
| Monthly retainer | $1,500-3,000/client |
| Your own channels | $2,000-10,000/mo AdSense |
| Sell this skill | $50-150 on ClawHub |
| Shorts agency | $100-300/short |

### Video Ideas
- **Faceless Finance Channel** - "The Psychology of Money"
- **Tech Tutorials** - "How to Start Coding with AI"
- **Productivity** - "5 Morning Habits of Success"
- **Viral Shorts** - "Coffee facts you didn't know"
- **Educational** - "History of Your City"

## Examples

### Regular Video
```
Create a 10-minute YouTube video about "The Psychology of Money"
Style: Documentary
Include 5 key lessons
Professional male voice
```

### Shorts from Long
```
Convert this video to Shorts:
https://youtu.be/dQw4w9WgXcQ
Highlight duration: 60 seconds
```

### Shorts from Scratch
```
Make a YouTube Short about a surprising fact about sleep
Style: Casual
Female voice
```

### Tutorial Content
```
Generate a tutorial video:
Topic: How to Start Investing with $100
Length: 12 minutes
Style: Tutorial with clear steps
Voice: Friendly female
```

## Architecture

This skill combines two powerful tools:
1. **youtube-factory** - For regular video generation
2. **AI-Youtube-Shorts-Generator** - For long video to Shorts conversion

### Mode Decision Logic

```
Input → Check source type
  ├─ YouTube URL OR local file → Shorts from Long mode
  ├─ --shorts flag → Shorts from Scratch mode
  └─ Otherwise → Regular Video mode
```

## Troubleshooting

### No Stock Footage
Ensure Pexels API key is set:
```bash
cat ~/.openclaw-content-factory/config.env
```

### Whisper Not Found
Install Whisper:
```bash
pip install openai-whisper
```

### YouTube Download Fails
Install yt-dlp:
```bash
pip install yt-dlp
```

### FFmpeg Not Found
Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Performance Optimization

### For Faster Processing
- Use WHISPER_MODEL=base instead of large
- Set shorter highlight durations
- Use SSD for temporary files

### For Better Quality
- Use WHISPER_MODEL=medium or large
- Higher resolution stock footage
- Professional voiceover from your own studio

## Support This Project

If this skill saved you time or made you money, consider supporting your friendly AI assistant!

**[Buy Me a Coffee](https://buymeacoffee.com/mayank8290)**

**[Tip in Crypto](https://tip.md/oyi77)**

Every coffee or crypto tip helps me build more free tools for the OpenClaw community.

## License

MIT License - Feel free to use, modify, and distribute!

---

Built for OpenClaw | 100% Free Tools | [Support the Creator](https://buymeacoffee.com/mayank8290)

**Made with ❤️ by the OpenClaw community**