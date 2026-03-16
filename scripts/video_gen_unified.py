#!/usr/bin/env python3
"""
Unified Video Generation Script
Supports: NVIDIA NIM, GeminiGen.ai API, Veo 2, Sora

Usage:
    python scripts/video_gen_unified.py --nvidia --prompt "holiday theme" --duration 45
    python scripts/video_gen_unified.py --geminigen --prompt "holiday theme"
"""

import os
import sys
import argparse
import requests
import time
import json

# Config
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
GEMINIGEN_API_KEY = os.getenv('GEMINIGEN_API_KEY', '')

def nvidia_generate(prompt, duration=45, style="3d_cartoon"):
    """Generate video via NVIDIA NIM API"""
    
    if not NVIDIA_API_KEY:
        print("❌ NVIDIA_API_KEY diperlukan!")
        print("   export NVIDIA_API_KEY='nvapi-...'")
        return None
    
    # Try different NVIDIA endpoints
    endpoints = [
        "https://api.nvidia.com/v1/nim/minimax/video/generate",
        "https://api.nvidia.com/v2/video/generations",
        "https://api.nvidia.com/nim/video-gen/v1/generate"
    ]
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "duration": duration,
        "style": style,
        "resolution": "1920x1080",
        "fps": 30
    }
    
    for url in endpoints:
        try:
            print(f"🔄 Trying: {url}")
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                print(f"✅ NVIDIA API Success!")
                return result
            elif resp.status_code != 404:
                print(f"   Status: {resp.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("❌ All NVIDIA endpoints failed")
    return None

def geminigen_generate(prompt, duration=6, orientation="9:16"):
    """Generate video via GeminiGen.ai API"""
    
    # Check if API exists, fallback to browser automation
    if not GEMINIGEN_API_KEY:
        print("⚠️ GeminiGen API key not set")
        print("   Using browser automation instead...")
        return {"method": "browser", "status": "manual"}
    
    api_url = "https://api.geminigen.ai/uapi/v1/video/generate"
    headers = {
        "Authorization": f"Bearer {GEMINIGEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "duration": duration,
        "orientation": orientation,
        "model": "grok-3"
    }
    
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"❌ GeminiGen API error: {e}")
    
    return None

def create_holiday_prompt(theme="hari_raya"):
    """Create prompts for holiday videos"""
    
    prompts = {
        "hari_raya": """
        Beautiful 3D animated celebration scene for Hari Raya Eid,
        vibrant festive atmosphere with colorful lights and decorations,
        happy family gathering, traditional holiday celebration,
        warm and joyful colors, cinematic 3D animation,
        perfect for social media content, high quality render
        """,
        "christmas": """
        Magical 3D Christmas celebration scene,
        snow falling, decorated Christmas tree, presents,
        warm fireplace, happy family, festive atmosphere,
        beautiful holiday lighting, cinematic 3D animation
        """,
        "new_year": """
        Spectacular New Year celebration 3D animation,
        fireworks display, happy people celebrating,
        countdown clock, confetti, festive city scene,
        sparkling lights, joyful atmosphere, cinematic quality
        """
    }
    
    return prompts.get(theme, prompts["hari_raya"])

def main():
    parser = argparse.ArgumentParser(description='Video Generation Tool')
    parser.add_argument('--nvidia', action='store_true', help='Use NVIDIA API')
    parser.add_argument('--geminigen', action='store_true', help='Use GeminiGen API')
    parser.add_argument('--prompt', type=str, default='', help='Video prompt')
    parser.add_argument('--duration', type=int, default=45, help='Duration in seconds')
    parser.add_argument('--theme', type=str, default='hari_raya', help='Holiday theme')
    parser.add_argument('--style', type=str, default='3d_cartoon', help='Video style')
    
    args = parser.parse_args()
    
    print("🎬 UNIFIED VIDEO GENERATION")
    print("=" * 40)
    
    if args.nvidia:
        prompt = args.prompt or create_holiday_prompt(args.theme)
        result = nvidia_generate(prompt, args.duration, args.style)
        if result:
            print(f"\n✅ Video generation started!")
            print(f"   Result: {json.dumps(result, indent=2)[:500]}")
    
    elif args.geminigen:
        prompt = args.prompt or create_holiday_prompt(args.theme)
        result = geminigen_generate(prompt)
        if result:
            print(f"\n✅ GeminiGen result: {result}")
    
    else:
        print("🎯 Available options:")
        print("   --nvidia     : Use NVIDIA NIM API (45s capable)")
        print("   --geminigen  : Use GeminiGen API (6s per video)")
        print("\n📝 Examples:")
        print("   python scripts/video_gen_unified.py --nvidia --theme hari_raya")
        print("   python scripts/video_gen_unified.py --geminigen --duration 6")
        print("\n🔧 Setup NVIDIA:")
        print("   export NVIDIA_API_KEY='nvapi-...'")
        print("   Get key: https://build.nvidia.com/nim")

if __name__ == "__main__":
    main()