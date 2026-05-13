#!/usr/bin/env python3
"""
BPM Detection Script for Music Videos
=======================================
Detects the BPM (beats per minute) of an audio file and outputs
a timing config for Remotion music video compositions.

100% local. No API. No internet after package install.

Usage:
  python scripts/bpm_detect.py public/audio/track.mp3
  python scripts/bpm_detect.py public/audio/track.mp3 --fps 60
  python scripts/bpm_detect.py public/audio/track.mp3 --save

Install (one-time, free):
  pip install librosa soundfile numpy

Output (printed + optionally saved to public/bpm.json):
  {
    "bpm": 128.0,
    "fps": 30,
    "framesPerBeat": 14,
    "framesPerBar": 56,
    "framesPerHalfBar": 28,
    "beatTimes": [0.0, 0.469, 0.938, ...],
    "beatFrames": [0, 14, 28, ...],
    "totalBeats": 256
  }

Use in Remotion:
  import bpmData from '../public/bpm.json';
  const beat = bpmData.framesPerBeat;
  const isOnBeat = frame % beat < 3;
"""

import sys
import os
import json
import argparse

# ── CONFIG ────────────────────────────────────────────────────
DEFAULT_FPS   = 30
OUTPUT_FILE   = 'public/bpm.json'


def detect_bpm(audio_path: str, fps: int) -> dict:
    """
    Detect BPM using librosa's beat tracking algorithm.
    Returns full timing config for Remotion.
    """
    try:
        import librosa
        import numpy as np
    except ImportError:
        print("❌ librosa not installed.")
        print("   Install with: pip install librosa soundfile numpy")
        sys.exit(1)

    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        sys.exit(1)

    print(f"🎵 Loading audio: {audio_path}")
    # Load audio (librosa handles mp3, wav, m4a, flac, ogg)
    y, sr = librosa.load(audio_path, mono=True)

    duration_sec = len(y) / sr
    print(f"   Duration: {duration_sec:.1f}s")

    print("🥁 Detecting BPM and beat positions...")

    # Detect tempo and beat frames
    tempo, beat_frames_samples = librosa.beat.beat_track(y=y, sr=sr)

    # librosa may return an array — take first value
    bpm = float(tempo[0] if hasattr(tempo, '__len__') else tempo)

    # Convert beat sample positions to seconds
    beat_times_sec = librosa.frames_to_time(beat_frames_samples, sr=sr)

    # Convert to Remotion frame numbers
    beat_frames_remotion = [round(t * fps) for t in beat_times_sec]

    # Calculate derived values
    frames_per_beat     = round((60 / bpm) * fps)
    frames_per_bar      = frames_per_beat * 4
    frames_per_half_bar = frames_per_beat * 2
    frames_per_8_bars   = frames_per_beat * 32

    total_frames = round(duration_sec * fps)
    total_beats  = len(beat_times_sec)

    result = {
        "bpm":               round(bpm, 2),
        "fps":               fps,
        "framesPerBeat":     frames_per_beat,
        "framesPerBar":      frames_per_bar,
        "framesPerHalfBar":  frames_per_half_bar,
        "framesPerPhrase":   frames_per_8_bars,   # 8 bars = typical verse/chorus
        "beatTimes":         [round(t, 3) for t in beat_times_sec.tolist()],
        "beatFrames":        beat_frames_remotion,
        "totalBeats":        total_beats,
        "totalFrames":       total_frames,
        "durationSeconds":   round(duration_sec, 2),
    }

    return result


def print_usage_examples(data: dict) -> None:
    bpm = data['bpm']
    fpb = data['framesPerBeat']
    fps = data['fps']

    print(f"""
╔══════════════════════════════════════════════╗
║           BPM Detection Results              ║
╠══════════════════════════════════════════════╣
  BPM:              {bpm}
  Frames/beat:      {fpb}  (at {fps}fps)
  Frames/bar (4/4): {data['framesPerBar']}
  Frames/half-bar:  {data['framesPerHalfBar']}
  Frames/phrase:    {data['framesPerPhrase']} (8 bars)
  Total beats:      {data['totalBeats']}
  Duration:         {data['durationSeconds']}s
╚══════════════════════════════════════════════╝

Use in Remotion (TypeScript):
─────────────────────────────
import bpmData from '../public/bpm.json';

const {{ framesPerBeat: beat, framesPerBar: bar }} = bpmData;

// Flash on every beat
const isOnBeat = frame % beat < 3;

// Flash on downbeat (every bar)
const isDownbeat = frame % bar < 3;

// Pulse scale with beat
const beatPhase = frame % beat;
const beatPulse = interpolate(beatPhase, [0, 3, beat], [1.05, 1, 1], {{
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp'
}});

// Snap to nearest beat (for positioning)
const currentBeat = Math.floor(frame / beat);

// Check if frame is within N frames of any detected beat
const nearBeat = bpmData.beatFrames.some(bf => Math.abs(frame - bf) < 3);
""")


def main():
    parser = argparse.ArgumentParser(
        description='Detect BPM of audio file for Remotion music video projects'
    )
    parser.add_argument('audio', help='Path to audio file (mp3, wav, m4a, flac, ogg)')
    parser.add_argument('--fps', type=int, default=DEFAULT_FPS,
                        help=f'Remotion FPS (default: {DEFAULT_FPS})')
    parser.add_argument('--save', action='store_true',
                        help=f'Save results to {OUTPUT_FILE}')
    parser.add_argument('--out', default=OUTPUT_FILE,
                        help=f'Output JSON path (default: {OUTPUT_FILE})')
    args = parser.parse_args()

    data = detect_bpm(args.audio, args.fps)

    print_usage_examples(data)

    if args.save:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved to: {args.out}")
        print(f"   Import: import bpmData from '../public/bpm.json'")
    else:
        print(f"ℹ  Add --save to write to {args.out}")


if __name__ == '__main__':
    main()
