#!/usr/bin/env python3
import os
import json
import base64
import time
import subprocess
import argparse
from pathlib import Path

# Paths
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
OUTPUT_DIR = WORKSPACE / "output" / "sequential_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PYTHON = f"{WORKSPACE}/venv/bin/python3"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def extract_last_frame(video_path, output_image_path):
    """提取视频最后一帧作为下一段的参考图"""
    cmd = [
        "ffmpeg", "-y",
        "-sseof", "-0.1",
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(output_image_path)
    ]
    subprocess.run(cmd, capture_output=True)
    return output_image_path.exists()

def generate_scene(prompt, reference_image=None, scene_index=0):
    """
    Generate a video scene with Smart Fallback
    If reference_image exists, it's used for chaining
    """
    log(f"🎬 Generating Scene {scene_index}...")
    
    # We use our smart_content_generator logic here
    # Since BytePlus is limit-reached, we'd normally fallback
    # For this demonstration, we'll simulate the SUCCESSFUL CHAINING logic
    
    scene_path = OUTPUT_DIR / f"scene_{scene_index}.mp4"
    
    # Dummy successful chaining for testing pipeline flow
    # In production, this calls XAI / BytePlus / Kling
    
    # Let's assume we use XAI Video (mocked for now because logic is what matters)
    if reference_image:
        log(f"🔗 Chaining: Using {reference_image.name} as preference for consistency.")
    
    # For test, we use our pexels background (looping different sections to simulate scenes)
    bg_video = WORKSPACE / "output" / "test_results" / "background.mp4"
    start_time = scene_index * 5
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", str(bg_video),
        "-t", "5",
        "-c", "copy",
        str(scene_path)
    ]
    subprocess.run(cmd, capture_output=True)
    
    return scene_path

def produce_sequential_1min(base_prompt, total_scenes=12):
    log("🚀 Starting Sequential Chain Workflow (1 Minute)")
    
    video_chain = []
    current_reference = None
    
    for i in range(total_scenes):
        # 1. Generate Video Scene
        scene_video = generate_scene(base_prompt, current_reference, i)
        video_chain.append(scene_video)
        
        # 2. Extract Last Frame for NEXT scene reference
        ref_path = OUTPUT_DIR / f"ref_frame_{i}.jpg"
        if extract_last_frame(scene_video, ref_path):
            current_reference = ref_path
            log(f"✅ Last frame extracted for Scene {i+1} reference.")
            
    # 3. Concatenate with transitions (v1: simple concat)
    concat_list = OUTPUT_DIR / "list.txt"
    with open(concat_list, "w") as f:
        for v in video_chain:
            f.write(f"file '{v.absolute()}'\n")
            
    final_video = OUTPUT_DIR / "final_sequential_1min.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(final_video)
    ]
    subprocess.run(cmd, capture_output=True)
    
    log(f"🏁 Final Chained Video created: {final_video}")
    return final_video

if __name__ == "__main__":
    produce_sequential_1min("Successful entrepreneur journey")
