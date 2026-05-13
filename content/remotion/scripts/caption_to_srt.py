#!/usr/bin/env python3
"""
Caption JSON → SRT Converter
==============================
Converts Remotion @remotion/captions JSON format to standard .srt
subtitle files for FFmpeg burning, YouTube upload, or any video player.

Also converts SRT → captions JSON (reverse direction).

100% local. No API. No internet. No dependencies beyond Python stdlib.

Usage:
  # JSON → SRT
  python scripts/caption_to_srt.py public/captions.json
  python scripts/caption_to_srt.py public/captions.json --out public/my.srt
  python scripts/caption_to_srt.py public/captions.json --words-per-line 6

  # SRT → JSON
  python scripts/caption_to_srt.py public/captions.srt --reverse

Input JSON format (from @remotion/captions or transcribe.py):
  [
    { "text": "Hello", "startMs": 0, "endMs": 480, "confidence": 0.99 },
    { "text": "world", "startMs": 500, "endMs": 900, "confidence": 0.97 },
    ...
  ]

Output SRT format:
  1
  00:00:00,000 --> 00:00:02,400
  Hello world this is

  2
  00:00:02,500 --> 00:00:05,200
  the subtitle text here

After generating SRT, burn into video:
  ffmpeg -i out/video.mp4 -vf "subtitles=public/captions.srt" out/final.mp4

  # Styled subtitles:
  ffmpeg -i out/video.mp4 \\
    -vf "subtitles=public/captions.srt:force_style='FontSize=28,PrimaryColour=&HFFFFFF,Outline=2'" \\
    out/final-subtitled.mp4
"""

import sys
import os
import json
import re
import argparse


# ── TIME CONVERSION HELPERS ───────────────────────────────────

def ms_to_srt(ms: float) -> str:
    """Convert milliseconds to SRT timestamp: HH:MM:SS,mmm"""
    ms = max(0, int(ms))
    h, r  = divmod(ms, 3_600_000)
    m, r  = divmod(r, 60_000)
    s, ms = divmod(r, 1_000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def srt_to_ms(ts: str) -> int:
    """Convert SRT timestamp HH:MM:SS,mmm to milliseconds"""
    ts = ts.strip().replace('.', ',')
    h, m, rest = ts.split(':')
    s, ms = rest.split(',')
    return int(h)*3_600_000 + int(m)*60_000 + int(s)*1_000 + int(ms)


# ── JSON → SRT ────────────────────────────────────────────────

def json_to_srt(captions: list, words_per_line: int = 8,
                max_line_ms: int = 4000, min_gap_ms: int = 100) -> str:
    """
    Group word-level captions into subtitle lines and format as SRT.

    Args:
        captions:       List of word dicts with text, startMs, endMs
        words_per_line: Max words per subtitle card
        max_line_ms:    Max duration of one subtitle card in ms
        min_gap_ms:     Minimum gap between subtitle cards
    """
    if not captions:
        return ''

    lines = []
    buf   = []
    start = None

    for word in captions:
        text = word.get('text', '').strip()
        if not text:
            continue

        if start is None:
            start = word['startMs']

        buf.append(text)
        end = word['endMs']

        flush = (
            len(buf) >= words_per_line or
            (end - start) >= max_line_ms or
            text.endswith(('.', '?', '!', '…'))
        )

        if flush:
            lines.append({'text': ' '.join(buf), 'startMs': start, 'endMs': end})
            buf   = []
            start = None

    if buf and start is not None:
        lines.append({'text': ' '.join(buf), 'startMs': start, 'endMs': captions[-1]['endMs']})

    # Build SRT blocks
    blocks = []
    for i, line in enumerate(lines, 1):
        # Ensure end doesn't overlap next start
        if i < len(lines):
            max_end = lines[i]['startMs'] - min_gap_ms
            end_ms  = min(line['endMs'], max_end)
        else:
            end_ms = line['endMs']

        blocks.append(
            f"{i}\n"
            f"{ms_to_srt(line['startMs'])} --> {ms_to_srt(end_ms)}\n"
            f"{line['text']}"
        )

    return '\n\n'.join(blocks) + '\n'


# ── SRT → JSON ────────────────────────────────────────────────

def srt_to_json(srt_content: str) -> list:
    """
    Parse SRT content and return caption JSON list.
    Each subtitle block becomes one entry (not word-level).
    """
    captions = []
    blocks = re.split(r'\n{2,}', srt_content.strip())

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        # Line 0: sequence number (ignore)
        # Line 1: timestamps
        # Lines 2+: text
        try:
            ts_line   = lines[1]
            start_str, end_str = ts_line.split(' --> ')
            start_ms  = srt_to_ms(start_str)
            end_ms    = srt_to_ms(end_str)
            text      = ' '.join(lines[2:]).strip()

            captions.append({
                'text':       text,
                'startMs':    start_ms,
                'endMs':      end_ms,
                'confidence': 1.0,
            })
        except (ValueError, IndexError):
            continue

    return captions


# ── VALIDATION ────────────────────────────────────────────────

def validate_captions(captions: list) -> list[str]:
    """Return list of warnings about caption data."""
    warnings = []
    prev_end = 0

    for i, cap in enumerate(captions):
        if cap['startMs'] < prev_end:
            warnings.append(f"Word {i} ({cap['text']!r}) overlaps previous: "
                          f"starts at {cap['startMs']}ms, prev ends at {prev_end}ms")
        if cap['endMs'] <= cap['startMs']:
            warnings.append(f"Word {i} ({cap['text']!r}) has zero/negative duration")
        prev_end = cap['endMs']

    return warnings


# ── MAIN ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Convert between captions.json and .srt format'
    )
    parser.add_argument('input', help='Input file (.json or .srt)')
    parser.add_argument('--out', default=None,
                        help='Output path (auto-detected from input extension if omitted)')
    parser.add_argument('--words-per-line', type=int, default=8,
                        help='Words per subtitle line for JSON→SRT (default: 8)')
    parser.add_argument('--max-duration', type=int, default=4000,
                        help='Max subtitle card duration in ms (default: 4000)')
    parser.add_argument('--reverse', action='store_true',
                        help='Convert SRT → JSON instead of JSON → SRT')
    parser.add_argument('--validate', action='store_true',
                        help='Validate caption timing and report issues')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)

    ext = os.path.splitext(args.input)[1].lower()

    # ── JSON → SRT ────────────────────────────────────────────
    if (ext == '.json' and not args.reverse) or (ext == '.srt' and args.reverse and False):
        with open(args.input, encoding='utf-8') as f:
            captions = json.load(f)

        print(f"📖 Loaded {len(captions)} caption entries from {args.input}")

        if args.validate:
            warnings = validate_captions(captions)
            if warnings:
                print(f"⚠️  {len(warnings)} validation issues:")
                for w in warnings[:10]:
                    print(f"   {w}")
            else:
                print("✅ Validation passed — no timing issues")

        srt_content = json_to_srt(captions, args.words_per_line, args.max_duration)

        out_path = args.out or os.path.splitext(args.input)[0] + '.srt'
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)

        line_count = srt_content.count('\n\n') + 1
        print(f"✅ SRT written: {out_path} ({line_count} subtitle cards)")
        print(f"\nBurn into video:")
        print(f"  ffmpeg -i out/video.mp4 -vf \"subtitles={out_path}\" out/final.mp4")
        print(f"\nStyled (white text, black outline):")
        print(f"  ffmpeg -i out/video.mp4 \\")
        print(f'    -vf "subtitles={out_path}:force_style=\'FontSize=28,PrimaryColour=&HFFFFFF,Outline=2\'" \\')
        print(f"    out/final-subtitled.mp4")

    # ── SRT → JSON ────────────────────────────────────────────
    elif ext == '.srt' or args.reverse:
        with open(args.input, encoding='utf-8') as f:
            srt_content = f.read()

        captions = srt_to_json(srt_content)
        print(f"📖 Parsed {len(captions)} subtitle entries from {args.input}")

        out_path = args.out or os.path.splitext(args.input)[0] + '.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(captions, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON written: {out_path}")
        print(f"\nUse in Remotion:")
        print(f"  import captions from '../{out_path}'")

    else:
        print(f"❌ Unrecognised input type: {ext}")
        print(f"   Supported: .json (→ SRT) or .srt (→ JSON with --reverse)")
        sys.exit(1)


if __name__ == '__main__':
    main()
