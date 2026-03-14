#!/usr/bin/env python3
import subprocess
import argparse
import os
from pathlib import Path

def produce_1min_video(video_path, tts_path, bgm_path, output_path, bgm_volume=0.10):
    """
    Produce a 1-minute synced video:
    1. Loop input video to 60s
    2. Mix TTS and BGM
    3. Apply 60s limit and sync
    """
    
    # Filter complex: 
    # [2:a] is BGM -> lower volume -> add fade out at end
    # amix combines TTS [1:a] and BGM
    filter_complex = (
        f"[2:a]volume={bgm_volume},afade=t=out:st=58:d=2[bgm];"
        f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",   # Loop video infinitely
        "-i", str(video_path),
        "-i", str(tts_path),
        "-i", str(bgm_path),
        "-filter_complex", filter_complex,
        "-map", "0:v",          # Take video from looped source
        "-map", "[a]",          # Take mixed audio
        "-c:v", "libx264",      # Re-encode for sync
        "-preset", "ultrafast",
        "-crf", "28",
        "-c:a", "aac",
        "-t", "60",             # Cut exactly at 60 seconds
        "-shortest",
        str(output_path)
    ]
    
    print(f"🚀 Running 1-Minute Production Engine...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 1-Minute Video synced and ready: {output_path}")
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
    parser.add_argument("--volume", type=float, default=0.10)
    args = parser.parse_args()

    produce_1min_video(args.video, args.tts, args.bgm, args.output, args.volume)
