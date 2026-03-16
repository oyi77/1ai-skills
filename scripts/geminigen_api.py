#!/usr/bin/env python3
"""
GeminiGen.ai API Integration for Video Generation
"""

import os
import requests
import json
import time

GEMINIGEN_API_KEY = os.getenv('GEMINIGEN_API_KEY', '')
API_BASE = "https://api.geminigen.ai/uapi/v1"

def generate_video(prompt, duration=6, orientation="portrait"):
    """Generate video via GeminiGen API"""
    if not GEMINIGEN_API_KEY:
        print("export GEMINIGEN_API_KEY='key-anda'")
        return None
    
    endpoint = f"{API_BASE}/video/generate"
    headers = {"Authorization": f"Bearer {GEMINIGEN_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "duration": duration, "orientation": orientation, "model": "grok-3"}
    
    print(f"Generating: {prompt[:60]}...")
    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            print("SUCCESS!")
            return resp.json()
        print(f"Error {resp.status_code}")
    except Exception as e:
        print(f"Exception: {e}")
    return None

def check_status(video_id):
    headers = {"Authorization": f"Bearer {GEMINIGEN_API_KEY}"}
    try:
        return requests.get(f"{API_BASE}/video/status/{video_id}", headers=headers).json()
    except: return {"error": "failed"}

def main():
    import sys
    args = sys.argv[1:]
    
    if "--help" in args:
        print("Usage: python scripts/geminigen_api.py [--prompt '...'] [--duration 6] [--check ID]")
        return
    
    prompt = "Beautiful 3D cartoon celebration Hari Raya, festive holiday scene, happy family, colorful, cinematic 3D animation"
    
    if "--prompt" in args:
        i = args.index("--prompt") + 1
        prompt = args[i]
    if "--duration" in args:
        i = args.index("--duration") + 1
        duration = int(args[i])
    if "--check" in args:
        i = args.index("--check") + 1
        print(json.dumps(check_status(args[i]), indent=2))
        return
    
    result = generate_video(prompt)
    if result:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
