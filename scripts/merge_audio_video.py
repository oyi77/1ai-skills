#!/usr/bin/env python3
import subprocess
import argparse
import os
from pathlib import Path

def merge_audio_video(video_path, tts_path, bgm_path, output_path, bgm_volume=0.15):
    """
    Merge Video + TTS Voiceover + Background Music using FFmpeg
    """
    # Build complex filter for audio mixing
    # [1:a] is TTS, [2:a] is BGM
    # we lower BGM volume and mix them
    filter_complex = f"[2:a]volume={bgm_volume}[bgm];[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(tts_path),
        "-i", str(bgm_path),
        "-filter_complex", filter_complex,
        "-map", "0:v",        # Map video from source 0
        "-map", "[a]",        # Map mixed audio
        "-c:v", "copy",       # Copy video codec (fast)
        "-c:a", "aac",        # Encode audio to AAC
        "-shortest",          # Match duration to shortest stream (usually video or TTS)
        str(output_path)
    ]
    
    print(f"🚀 Running FFmpeg Merger...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Video merged successfully: {output_path}")
        return True
    else:
        print(f"❌ FFmpeg Error: {result.stderr}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--tts", required=True)
    parser.add_argument("--bgm", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--volume", type=float, default=0.15)
    args = parser.parse_args()

    merge_audio_video(args.video, args.tts, args.bgm, args.output, args.volume)
