#!/usr/bin/env python3
"""
Local Speech-to-Text Transcription Script
==========================================
Transcribes audio files to captions JSON + SRT using OpenAI Whisper
running 100% LOCALLY. No API key. No internet after model download.

First run downloads the model (~150MB for 'base'). Subsequent runs are
fully offline.

Usage:
  python scripts/transcribe.py public/audio/narration.mp3
  python scripts/transcribe.py public/audio/narration.mp3 --model small
  python scripts/transcribe.py public/audio/narration.mp3 --lang id
  python scripts/transcribe.py public/audio/narration.mp3 --model medium --lang id

Install (one-time, free):
  pip install openai-whisper
  # Also requires ffmpeg: brew install ffmpeg OR apt install ffmpeg

Model sizes (all FREE, local):
  tiny    — fastest, least accurate (~75MB)
  base    — good balance (~150MB) ← RECOMMENDED
  small   — better accuracy (~500MB)
  medium  — high accuracy (~1.5GB)
  large   — best accuracy (~3GB), slow on CPU

Output files:
  public/captions.json   ← word-level timing for Remotion @remotion/captions
  public/captions.srt    ← standard subtitle file for FFmpeg burning

Output format (captions.json):
  [
    { "text": "Hello", "startMs": 0, "endMs": 480, "confidence": 0.99 },
    ...
  ]
"""

import sys
import os
import json
import argparse

# ── CONFIG ────────────────────────────────────────────────────
DEFAULT_MODEL    = 'base'     # tiny | base | small | medium | large
DEFAULT_LANG     = None       # None = auto-detect, 'id' = Indonesian, 'en' = English
OUTPUT_DIR       = 'public'
CAPTIONS_FILE    = os.path.join(OUTPUT_DIR, 'captions.json')
SRT_FILE         = os.path.join(OUTPUT_DIR, 'captions.srt')


def ms_to_srt_time(ms: float) -> str:
    """Convert milliseconds to SRT timestamp format: HH:MM:SS,mmm"""
    ms = int(ms)
    h, remainder = divmod(ms, 3_600_000)
    m, remainder = divmod(remainder, 60_000)
    s, ms_part   = divmod(remainder, 1_000)
    return f"{h:02}:{m:02}:{s:02},{ms_part:03}"


def captions_to_srt(captions: list, words_per_line: int = 8) -> str:
    """
    Group word-level captions into subtitle lines and format as SRT.
    """
    if not captions:
        return ''

    lines = []
    buffer = []
    buffer_start_ms = None

    for word in captions:
        if buffer_start_ms is None:
            buffer_start_ms = word['startMs']

        buffer.append(word['text'].strip())

        # New line when we hit word limit OR 3 seconds of content
        if (len(buffer) >= words_per_line or
                word['endMs'] - buffer_start_ms > 3000):
            lines.append({
                'text': ' '.join(buffer),
                'startMs': buffer_start_ms,
                'endMs': word['endMs'],
            })
            buffer = []
            buffer_start_ms = None

    # Flush remaining
    if buffer and buffer_start_ms is not None:
        lines.append({
            'text': ' '.join(buffer),
            'startMs': buffer_start_ms,
            'endMs': captions[-1]['endMs'],
        })

    # Format as SRT
    srt_blocks = []
    for i, line in enumerate(lines, 1):
        srt_blocks.append(
            f"{i}\n"
            f"{ms_to_srt_time(line['startMs'])} --> {ms_to_srt_time(line['endMs'])}\n"
            f"{line['text']}"
        )

    return '\n\n'.join(srt_blocks) + '\n'


def transcribe(audio_path: str, model_name: str, language: str | None) -> list:
    """
    Run Whisper locally and return word-level caption list.
    """
    try:
        import whisper
    except ImportError:
        print("❌ openai-whisper not installed.")
        print("   Install with: pip install openai-whisper")
        print("   Also needs ffmpeg: brew install ffmpeg OR apt install ffmpeg")
        sys.exit(1)

    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        sys.exit(1)

    print(f"📥 Loading Whisper model: {model_name}")
    print(f"   (First run downloads ~{{'tiny':75,'base':150,'small':500,'medium':1500,'large':3000}.get(model_name, '?')}MB — free, one-time)")
    model = whisper.load_model(model_name)

    print(f"🎙  Transcribing: {audio_path}")
    if language:
        print(f"   Language hint: {language}")

    options = {
        'word_timestamps': True,
        'verbose': False,
    }
    if language:
        options['language'] = language

    result = model.transcribe(audio_path, **options)

    # Extract word-level timestamps
    captions = []
    for segment in result.get('segments', []):
        words = segment.get('words', [])
        if not words:
            # Segment has no word timestamps — fall back to segment-level
            captions.append({
                'text': segment['text'].strip(),
                'startMs': round(segment['start'] * 1000),
                'endMs':   round(segment['end']   * 1000),
                'confidence': round(segment.get('avg_logprob', 0) + 1, 3),
            })
        else:
            for word in words:
                text = word.get('word', '').strip()
                if not text:
                    continue
                captions.append({
                    'text': text,
                    'startMs': round(word['start'] * 1000),
                    'endMs':   round(word['end']   * 1000),
                    'confidence': round(word.get('probability', 1.0), 3),
                })

    print(f"   ✓ {len(captions)} words transcribed")
    return captions


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio to captions.json + captions.srt (no API, local Whisper)'
    )
    parser.add_argument('audio', help='Path to audio file (mp3, wav, m4a, etc.)')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help=f'Whisper model size (default: {DEFAULT_MODEL})')
    parser.add_argument('--lang', default=DEFAULT_LANG,
                        help='Language code: id=Indonesian, en=English, zh=Chinese (auto if omitted)')
    parser.add_argument('--words-per-line', type=int, default=8,
                        help='Words per subtitle line (default: 8)')
    parser.add_argument('--srt-only', action='store_true',
                        help='Only output SRT, skip captions.json')
    parser.add_argument('--out-dir', default=OUTPUT_DIR,
                        help=f'Output directory (default: {OUTPUT_DIR})')
    args = parser.parse_args()

    captions_path = os.path.join(args.out_dir, 'captions.json')
    srt_path      = os.path.join(args.out_dir, 'captions.srt')

    os.makedirs(args.out_dir, exist_ok=True)

    # Run transcription
    captions = transcribe(args.audio, args.model, args.lang)

    if not captions:
        print("⚠️  No captions generated — check audio file.")
        sys.exit(1)

    # Write captions.json
    if not args.srt_only:
        with open(captions_path, 'w', encoding='utf-8') as f:
            json.dump(captions, f, indent=2, ensure_ascii=False)
        print(f"✅ Captions JSON: {captions_path}")
        print(f"   Import in Remotion: import captions from '../public/captions.json'")

    # Write captions.srt
    srt_content = captions_to_srt(captions, args.words_per_line)
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    print(f"✅ SRT file: {srt_path}")
    print(f"   Burn with ffmpeg: ffmpeg -i out/video.mp4 -vf subtitles={srt_path} out/final.mp4")

    # Preview first 5 lines
    print(f"\nFirst 5 words:")
    for cap in captions[:5]:
        t = cap['startMs'] / 1000
        print(f"  {t:.2f}s  {cap['text']!r}")


if __name__ == '__main__':
    main()
