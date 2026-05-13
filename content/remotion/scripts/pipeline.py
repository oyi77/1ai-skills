#!/usr/bin/env python3
"""
Remotion TTS + Timing Pipeline Script
Usage: python scripts/pipeline.py [--voice id|en|zh]

Prerequisites:
  pip install edge-tts
  brew install ffmpeg  # or: apt install ffmpeg

Expects: public/script.json
Outputs: public/audio/*.mp3, public/timing.json
"""

import asyncio
import json
import os
import subprocess
import sys
import argparse
import edge_tts

# ============================================================
# CONFIGURATION
# ============================================================
FPS = 30
PADDING_BEFORE_SEC = 0.5   # silence before narration starts
PADDING_AFTER_SEC = 0.3    # silence after narration ends

VOICES = {
    'id': 'id-ID-ArdiNeural',        # Indonesian male
    'id-f': 'id-ID-GadisNeural',     # Indonesian female
    'en': 'en-US-JennyNeural',       # English female (default)
    'en-m': 'en-US-GuyNeural',       # English male
    'zh': 'zh-CN-XiaoxiaoNeural',    # Chinese female
    'zh-m': 'zh-CN-YunxiNeural',     # Chinese male
}
# ============================================================


def get_audio_duration(filepath: str) -> float:
    """Get audio duration in seconds using ffprobe."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'json', filepath],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {filepath}: {result.stderr}")
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


async def generate_tts(text: str, output_path: str, voice: str) -> None:
    """Generate TTS audio using Edge TTS (free)."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


async def run_pipeline(script_path: str, voice_key: str):
    voice = VOICES.get(voice_key, VOICES['en'])
    print(f"🎙️  Using voice: {voice}")

    # Load script
    with open(script_path, encoding='utf-8') as f:
        script = json.load(f)

    scenes = script.get('scenes', [])
    if not scenes:
        print("❌ No scenes found in script.json")
        sys.exit(1)

    os.makedirs('public/audio', exist_ok=True)

    # Step 1: Generate TTS for each scene
    print(f"\n📢 Generating TTS for {len(scenes)} scenes...")
    for scene in scenes:
        sid = scene['id']
        text = scene.get('narration', '').strip()
        out_path = f"public/audio/{sid}.mp3"

        if not text:
            print(f"  ⚠️  Skipping {sid} — no narration text")
            continue

        if os.path.exists(out_path):
            print(f"  ✓ {sid}.mp3 (exists, skipping)")
        else:
            print(f"  → Generating {sid}.mp3 ...")
            await generate_tts(text, out_path, voice)
            print(f"  ✓ {sid}.mp3 done")

    # Step 2: Measure durations + build timing.json
    print(f"\n⏱️  Computing timing...")
    timing = {'fps': FPS, 'scenes': [], 'totalFrames': 0, 'totalSeconds': 0}
    cumulative_frame = 0

    for scene in scenes:
        sid = scene['id']
        audio_path = f"public/audio/{sid}.mp3"

        if os.path.exists(audio_path) and scene.get('narration', '').strip():
            narration_sec = get_audio_duration(audio_path)
        else:
            narration_sec = 3.0  # fallback duration
            print(f"  ⚠️  {sid}: using fallback 3s duration")

        total_sec = PADDING_BEFORE_SEC + narration_sec + PADDING_AFTER_SEC
        duration_frames = round(total_sec * FPS)

        timing['scenes'].append({
            'id': sid,
            'title': scene.get('title', sid),
            'audioFile': f"{sid}.mp3",
            'narrationSeconds': round(narration_sec, 3),
            'totalSeconds': round(total_sec, 3),
            'durationFrames': duration_frames,
            'startFrame': cumulative_frame,
            'endFrame': cumulative_frame + duration_frames,
            'paddingBeforeFrames': round(PADDING_BEFORE_SEC * FPS),
            'background': scene.get('background', 'dark'),
        })

        print(f"  {sid}: {narration_sec:.1f}s narration → {duration_frames} frames")
        cumulative_frame += duration_frames

    timing['totalFrames'] = cumulative_frame
    timing['totalSeconds'] = round(cumulative_frame / FPS, 2)

    with open('public/timing.json', 'w', encoding='utf-8') as f:
        json.dump(timing, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Pipeline complete!")
    print(f"   Total: {cumulative_frame} frames = {timing['totalSeconds']}s")
    print(f"   Timing saved: public/timing.json")
    print(f"\n🎬 Next steps:")
    print(f"   1. Update src/Root.tsx to use timing.json")
    print(f"   2. npm run dev  (preview in Remotion Studio)")
    print(f"   3. npx remotion render NarratedVideo out/video.mp4")


def main():
    parser = argparse.ArgumentParser(description='Remotion TTS + Timing Pipeline')
    parser.add_argument('--script', default='public/script.json', help='Path to script JSON')
    parser.add_argument('--voice', default='en', choices=list(VOICES.keys()),
                        help=f'Voice to use. Options: {list(VOICES.keys())}')
    args = parser.parse_args()

    if not os.path.exists(args.script):
        print(f"❌ Script not found: {args.script}")
        print(f"   Create public/script.json with scenes array")
        sys.exit(1)

    asyncio.run(run_pipeline(args.script, args.voice))


if __name__ == '__main__':
    main()
