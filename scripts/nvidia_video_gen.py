#!/usr/bin/env python3
"""
NVIDIA NIM Video Generation for 3D Cartoon Holiday Video
"""

import os
import requests
import json
import time

# NVIDIA API Configuration
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')

if not NVIDIA_API_KEY:
    print("❌ NVIDIA_API_KEY tidak ditemukan!")
    print("Setup: export NVIDIA_API_KEY='nvapi-...'")
    exit(1)

# NVIDIA NIM Video Gen API
API_URL = "https://api.nvidia.com/v1/nim/minimax/video/generate"

def generate_holiday_video(duration=45, style="3d_cartoon"):
    """Generate 45-second 3D cartoon holiday video"""
    
    prompt = """
    Beautiful 3D animated video celebrating Hari Raya (celebration), 
    vibrant festive atmosphere, colorful lanterns and decorations, 
    happy family gathering, traditional holiday elements, festive lighting,
    joyful atmosphere, cinematic 3D animation style, high quality,
    celebration scene with warm colors, perfect for social media,
    45 second duration, smooth animation
    """
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "duration": duration,  # 45 seconds
        "style": style,
        "resolution": "1920x1080",
        "fps": 30,
        "guidance_scale": 7.5,
        "negative_prompt": "low quality, blurry, distorted, ugly",
        "output_format": "mp4"
    }
    
    print(f"🎬 Generating 45s 3D cartoon holiday video...")
    print(f"   Prompt: {prompt[:100]}...")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get('video_url') or result.get('url')
            print(f"✅ Video generation started!")
            print(f"   Job ID: {result.get('job_id')}")
            print(f"   Status: {result.get('status', 'processing')}")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def check_status(job_id):
    """Check video generation status"""
    status_url = f"https://api.nvidia.com/v1/nim/minimax/video/status/{job_id}"
    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}"}
    
    response = requests.get(status_url, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Generate 45 second holiday video
    result = generate_holiday_video(duration=45, style="3d_cartoon")
    
    if result:
        job_id = result.get('job_id')
        print(f"\n📊 To check status:")
        print(f"   python scripts/nvidia_video_gen.py --status {job_id}")
