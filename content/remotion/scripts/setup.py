#!/usr/bin/env python3
"""
Remotion Project Setup Script
==============================
Creates the full folder structure and starter files for a Remotion
video project. Run ONCE after `npx create-video@latest`.

Usage:
  python scripts/setup.py
  python scripts/setup.py --type narrated   # narrated video (TTS-driven)
  python scripts/setup.py --type product    # product commercial
  python scripts/setup.py --type shortform  # TikTok/Reels 9:16
  python scripts/setup.py --type music      # music video / lyric

No API key needed. No internet needed. Fully free.

What it creates:
  public/
    audio/          ← TTS output + BGM go here
    images/         ← product images, thumbnails
    video/          ← source footage
    fonts/          ← custom font files
  scripts/          ← this folder
  out/              ← rendered video output
  public/script.json  ← video script template
"""

import os
import json
import sys
import argparse

# ── SCRIPT TEMPLATES ──────────────────────────────────────────

SCRIPT_TEMPLATES = {
    'narrated': {
        "title": "Judul Video Saya",
        "description": "Deskripsi singkat tentang video ini.",
        "language": "id",
        "scenes": [
            {
                "id": "intro",
                "title": "Pembukaan",
                "narration": "Selamat datang! Hari ini kita akan membahas topik yang sangat penting.",
                "background": "gradient-blue",
                "notes": "Antusias, energik"
            },
            {
                "id": "point1",
                "title": "Poin Pertama",
                "narration": "Pertama, kita perlu memahami konsep dasar dari topik ini.",
                "background": "dark",
                "notes": "Jelas dan informatif"
            },
            {
                "id": "point2",
                "title": "Poin Kedua",
                "narration": "Kedua, mari kita lihat bagaimana menerapkannya secara praktis.",
                "background": "dark",
                "notes": ""
            },
            {
                "id": "outro",
                "title": "Penutup",
                "narration": "Itulah yang perlu Anda ketahui. Terima kasih sudah menonton!",
                "background": "gradient-purple",
                "notes": "Hangat, mengundang aksi"
            }
        ]
    },
    'product': {
        "title": "Nama Produk Saya",
        "product_name": "ProMax X1",
        "tagline": "Rethink everything.",
        "price": "299000",
        "currency": "Rp ",
        "cta": "Order Sekarang",
        "scenes": [
            {
                "id": "cold-open",
                "title": "Cold Open",
                "narration": "Apa yang akan kamu lakukan jika ada produk yang bisa mengubah hidupmu?",
                "background": "dark",
                "notes": "Misterius, penasaran"
            },
            {
                "id": "problem",
                "title": "Masalah",
                "narration": "Selama ini kamu mungkin sudah mencoba berbagai solusi. Tapi tidak ada yang benar-benar berhasil.",
                "background": "dark",
                "notes": "Empati"
            },
            {
                "id": "solution",
                "title": "Solusi",
                "narration": "Sekarang ada jawabannya.",
                "background": "brand",
                "notes": "Revelation moment"
            },
            {
                "id": "features",
                "title": "Fitur Unggulan",
                "narration": "Dirancang untuk performa maksimal, dengan kualitas premium yang terjangkau.",
                "background": "dark",
                "notes": ""
            },
            {
                "id": "cta",
                "title": "Call to Action",
                "narration": "Order sekarang dan dapatkan gratis ongkir untuk hari ini saja.",
                "background": "brand",
                "notes": "Urgensi"
            }
        ]
    },
    'shortform': {
        "title": "Short-Form Video",
        "platform": "tiktok",
        "hook": "Kamu PASTI nggak tahu ini...",
        "duration_target": "30s",
        "scenes": [
            {
                "id": "hook",
                "title": "Hook",
                "narration": "Kamu PASTI nggak tahu fakta mengejutkan ini tentang bisnis online.",
                "background": "dark",
                "notes": "HARUS dalam 3 detik pertama"
            },
            {
                "id": "body",
                "title": "Isi",
                "narration": "Kebanyakan orang berpikir mereka butuh modal besar untuk mulai. Padahal tidak.",
                "background": "dark",
                "notes": ""
            },
            {
                "id": "reveal",
                "title": "Reveal",
                "narration": "Yang kamu butuhkan hanya ini: konsistensi 30 hari pertama.",
                "background": "dark",
                "notes": "Punchline"
            },
            {
                "id": "cta",
                "title": "CTA",
                "narration": "Follow untuk tips bisnis setiap hari.",
                "background": "dark",
                "notes": "Soft CTA"
            }
        ]
    },
    'music': {
        "title": "Music Video Project",
        "song_title": "Nama Lagu",
        "artist": "Nama Artis",
        "bpm": 128,
        "key": "A minor",
        "audio_file": "audio/track.mp3",
        "scenes": [
            {
                "id": "intro",
                "title": "Intro",
                "start_beat": 0,
                "end_beat": 8,
                "notes": "Ambient visuals, no lyrics yet"
            },
            {
                "id": "verse1",
                "title": "Verse 1",
                "start_beat": 8,
                "end_beat": 24,
                "notes": "Performance / lyric reveal"
            },
            {
                "id": "chorus",
                "title": "Chorus",
                "start_beat": 24,
                "end_beat": 40,
                "notes": "High energy, beat sync visuals"
            }
        ],
        "lyrics": [
            {"text": "Baris pertama lirik", "beat_start": 8,  "beat_end": 10},
            {"text": "Sambung ke baris dua", "beat_start": 10, "beat_end": 12}
        ]
    }
}

GITIGNORE_CONTENT = """# Remotion
out/
.remotion/

# Audio (generated)
public/audio/*.mp3
public/audio/*.wav

# Timing (generated)
public/timing.json

# Python
__pycache__/
*.pyc
.env

# Node
node_modules/
.next/
dist/
"""

README_CONTENT = """# Remotion Video Project

## Quick Start

```bash
# 1. Install dependencies
npm install
pip install edge-tts  # for TTS narration

# 2. Generate TTS audio + timing (for narrated videos)
python scripts/pipeline.py --voice id

# 3. Preview in Remotion Studio
npm run dev

# 4. Render to file
npx remotion render [CompositionId] out/video.mp4
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/pipeline.py` | Generate TTS audio + timing.json |
| `scripts/transcribe.py` | Speech-to-text → captions (no API, uses local Whisper) |
| `scripts/bpm_detect.py` | Detect BPM of audio file (for music videos) |
| `scripts/postprocess.sh` | FFmpeg: mix BGM, burn subtitles, export formats |
| `scripts/batch_render.sh` | Render all compositions in one command |
| `scripts/prepare_assets.py` | Resize/convert images + videos for Remotion |
| `scripts/caption_to_srt.py` | Convert captions JSON to .srt file |
| `scripts/setup.py` | This setup script |

## Folder Structure

```
public/
  audio/      ← TTS files + BGM
  images/     ← product images, backgrounds
  video/      ← source clips
  fonts/      ← custom fonts
src/
  Root.tsx    ← register compositions
  Composition.tsx ← main video
  scenes/     ← scene components
scripts/      ← all Python + shell helpers
out/          ← rendered output
```

## Free Tools Used (No API Key Required)

- **edge-tts** — Microsoft TTS, no login needed: `pip install edge-tts`
- **openai-whisper** — Local speech recognition: `pip install openai-whisper`
- **librosa** — BPM detection: `pip install librosa`
- **ffmpeg** — Video processing: `brew install ffmpeg` or `apt install ffmpeg`
"""


def create_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)
    print(f"  📁 {path}/")


def write_file(path: str, content: str, skip_if_exists: bool = True) -> None:
    if skip_if_exists and os.path.exists(path):
        print(f"  ⏭  {path} (exists, skipped)")
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  📄 {path}")


def main():
    parser = argparse.ArgumentParser(
        description='Set up a Remotion video project structure.'
    )
    parser.add_argument(
        '--type',
        choices=['narrated', 'product', 'shortform', 'music'],
        default='narrated',
        help='Type of video project to scaffold'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing files'
    )
    args = parser.parse_args()

    skip_existing = not args.force

    print(f"\n🎬 Setting up Remotion project (type: {args.type})\n")

    # ── Create directories ────────────────────────────────────
    print("Creating folder structure...")
    for d in [
        'public/audio',
        'public/images',
        'public/video',
        'public/fonts',
        'scripts',
        'out',
        'src/scenes',
    ]:
        create_dir(d)

    # ── Create placeholder files ──────────────────────────────
    print("\nCreating starter files...")

    # .gitkeep files so empty dirs are tracked
    for d in ['public/audio', 'public/images', 'public/video', 'public/fonts', 'out']:
        gitkeep = os.path.join(d, '.gitkeep')
        if not os.path.exists(gitkeep):
            open(gitkeep, 'w').close()

    # script.json
    script_data = SCRIPT_TEMPLATES.get(args.type, SCRIPT_TEMPLATES['narrated'])
    write_file('public/script.json', json.dumps(script_data, indent=2, ensure_ascii=False), skip_existing)

    # .gitignore
    write_file('.gitignore', GITIGNORE_CONTENT, skip_existing)

    # README
    write_file('README.md', README_CONTENT, skip_existing)

    # ── Print next steps ──────────────────────────────────────
    print(f"""
✅ Project structure created!

Next steps:
  1. Install Python deps:
       pip install edge-tts ffmpeg-python

  2. Edit your script:
       public/script.json

  3. Generate TTS + timing:
       python scripts/pipeline.py --voice id

  4. Start Remotion Studio:
       npm run dev

  5. Render when ready:
       npx remotion render NarratedVideo out/video.mp4

Free tools needed (no API key):
  pip install edge-tts openai-whisper librosa Pillow
  brew install ffmpeg   # macOS
  apt install ffmpeg    # Ubuntu/Debian
""")


if __name__ == '__main__':
    main()
