#!/usr/bin/env python3
"""
GeminiGen AI - Multimedia AI Platform Integration
Supports: Image, Video (Veo/Sora/Grok), TTS
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

API_KEY = os.getenv("GEMINIGEN_API_KEY", "geminiai-89bb141f0c3a1075bff6fbdcd31ca701")
BASE_URL = "https://api.geminigen.ai/uapi/v1"
HEADERS = {"x-api-key": API_KEY}


def generate_image(prompt, model="nano-banana-pro", aspect="9:16", style="Photorealistic", resolution="1K"):
    """Generate an image from text prompt."""
    resp = requests.post(
        f"{BASE_URL}/generate_image",
        headers=HEADERS,
        data={
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect,
            "style": style,
            "resolution": resolution,
            "output_format": "png"
        }
    )
    return resp.json()


def generate_video_veo(prompt, model="veo-2", aspect="9:16", resolution="720p"):
    """Generate video using Google Veo model."""
    resp = requests.post(
        f"{BASE_URL}/video-gen/veo",
        headers=HEADERS,
        data={
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect,
            "resolution": resolution
        }
    )
    return resp.json()


def generate_video_sora(prompt, model="sora-2", duration=10, aspect="portrait", resolution="small"):
    """Generate video using OpenAI Sora model."""
    resp = requests.post(
        f"{BASE_URL}/video-gen/sora",
        headers=HEADERS,
        data={
            "prompt": prompt,
            "model": model,
            "duration": duration,
            "aspect_ratio": aspect,
            "resolution": resolution
        }
    )
    return resp.json()


def text_to_speech(text, model="tts-flash", voice_id="GM013", voice_name="Gacrux", speed=1):
    """Convert text to speech."""
    resp = requests.post(
        f"{BASE_URL}/text-to-speech",
        headers=HEADERS,
        json={
            "model": model,
            "voices": [{"name": voice_name, "voice": {"id": voice_id, "name": voice_name}}],
            "speed": speed,
            "input": text,
            "output_format": "mp3"
        }
    )
    return resp.json()


def get_history(uuid):
    """Get generation history/status by UUID."""
    resp = requests.get(f"{BASE_URL}/history/{uuid}", headers=HEADERS)
    return resp.json()


def wait_for_result(uuid, max_wait=600, poll_interval=5):
    """Wait for generation to complete and return result URL."""
    start = time.time()
    while time.time() - start < max_wait:
        data = get_history(uuid)
        status = data.get("status")
        
        if status == 2:  # Completed
            # Return appropriate media URL
            if data.get("generated_image"):
                return data["generated_image"][0].get("image_url")
            elif data.get("generated_video"):
                return data["generated_video"][0].get("video_url")
            elif data.get("generated_audio"):
                return data["generated_audio"][0].get("audio_url")
            return data.get("generate_result")
        
        if status == 3:  # Failed
            raise Exception(f"Generation failed: {data.get('error_message')}")
        
        print(f"Status: {status}, Progress: {data.get('status_percentage', 0)}%", file=sys.stderr)
        time.sleep(poll_interval)
    
    raise Exception(f"Timeout waiting for result after {max_wait}s")


def download_file(url, output_path):
    """Download file from URL to local path."""
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="GeminiGen AI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Image generation
    img_parser = subparsers.add_parser("image", help="Generate image")
    img_parser.add_argument("prompt", help="Image prompt")
    img_parser.add_argument("--model", default="nano-banana-pro", choices=["nano-banana-pro", "nano-banana-2", "imagen-4"])
    img_parser.add_argument("--aspect", default="9:16", choices=["1:1", "16:9", "9:16", "4:3", "3:4"])
    img_parser.add_argument("--style", default="Photorealistic")
    img_parser.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"])
    img_parser.add_argument("--output", "-o", help="Output file path")
    img_parser.add_argument("--wait", action="store_true", help="Wait for completion and download")
    
    # Video Veo
    veo_parser = subparsers.add_parser("veo", help="Generate video with Veo")
    veo_parser.add_argument("prompt", help="Video prompt")
    veo_parser.add_argument("--model", default="veo-2", choices=["veo-3.1", "veo-3.1-fast", "veo-2"])
    veo_parser.add_argument("--aspect", default="9:16", choices=["16:9", "9:16"])
    veo_parser.add_argument("--resolution", default="720p", choices=["720p", "1080p"])
    veo_parser.add_argument("--output", "-o", help="Output file path")
    veo_parser.add_argument("--wait", action="store_true", help="Wait for completion and download")
    
    # Video Sora
    sora_parser = subparsers.add_parser("sora", help="Generate video with Sora")
    sora_parser.add_argument("prompt", help="Video prompt")
    sora_parser.add_argument("--model", default="sora-2", choices=["sora-2", "sora-2-pro", "sora-2-pro-hd"])
    sora_parser.add_argument("--duration", type=int, default=10, choices=[10, 15, 25])
    sora_parser.add_argument("--aspect", default="portrait", choices=["landscape", "portrait"])
    sora_parser.add_argument("--resolution", default="small", choices=["small", "large"])
    sora_parser.add_argument("--output", "-o", help="Output file path")
    sora_parser.add_argument("--wait", action="store_true", help="Wait for completion and download")
    
    # TTS
    tts_parser = subparsers.add_parser("tts", help="Text to speech")
    tts_parser.add_argument("text", help="Text to convert")
    tts_parser.add_argument("--model", default="tts-flash", choices=["tts-flash", "tts-pro"])
    tts_parser.add_argument("--voice-id", default="GM013")
    tts_parser.add_argument("--voice-name", default="Gacrux")
    tts_parser.add_argument("--speed", type=float, default=1.0)
    tts_parser.add_argument("--output", "-o", help="Output file path")
    tts_parser.add_argument("--wait", action="store_true", help="Wait for completion and download")
    
    # Status check
    status_parser = subparsers.add_parser("status", help="Check generation status")
    status_parser.add_argument("uuid", help="Generation UUID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "image":
        result = generate_image(args.prompt, args.model, args.aspect, args.style, args.resolution)
        print(json.dumps(result, indent=2))
        if args.wait and result.get("uuid"):
            url = wait_for_result(result["uuid"])
            if args.output and url:
                download_file(url, args.output)
                print(f"Downloaded to: {args.output}")
    
    elif args.command == "veo":
        result = generate_video_veo(args.prompt, args.model, args.aspect, args.resolution)
        print(json.dumps(result, indent=2))
        if args.wait and result.get("uuid"):
            url = wait_for_result(result["uuid"])
            if args.output and url:
                download_file(url, args.output)
                print(f"Downloaded to: {args.output}")
    
    elif args.command == "sora":
        result = generate_video_sora(args.prompt, args.model, args.duration, args.aspect, args.resolution)
        print(json.dumps(result, indent=2))
        if args.wait and result.get("uuid"):
            url = wait_for_result(result["uuid"])
            if args.output and url:
                download_file(url, args.output)
                print(f"Downloaded to: {args.output}")
    
    elif args.command == "tts":
        result = text_to_speech(args.text, args.model, args.voice_id, args.voice_name, args.speed)
        print(json.dumps(result, indent=2))
        if args.wait and result.get("result", {}).get("uuid"):
            uuid = result["result"]["uuid"]
            url = wait_for_result(uuid)
            if args.output and url:
                download_file(url, args.output)
                print(f"Downloaded to: {args.output}")
    
    elif args.command == "status":
        result = get_history(args.uuid)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
