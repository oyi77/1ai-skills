#!/usr/bin/env python3
import os
import json
import base64
import argparse
import requests
from pathlib import Path

def generate_nvidia(prompt, output_path):
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key: return False, "No key"
    
    url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    payload = {"prompt": prompt}
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}: {resp.text[:100]}"
            
        data = resp.json()
        artifacts = data.get("artifacts", [])
        if not artifacts or artifacts[0].get("finishReason") != "SUCCESS":
            return False, f"Failed: {artifacts[0].get('finishReason') if artifacts else 'No artifacts'}"
            
        b64 = artifacts[0].get("base64")
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(b64))
        return True, "Success"
    except Exception as e:
        return False, str(e)

def generate_xai(prompt, output_path):
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key: return False, "No key"
    
    url = "https://api.x.ai/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "prompt": prompt,
        "model": "grok-2-vision-1212", # or Grok-3 if available
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}: {resp.text[:100]}"
            
        data = resp.json()
        # XAI usually returns URLs
        img_url = data.get("data", [{}])[0].get("url")
        if img_url:
            img_resp = requests.get(img_url)
            with open(output_path, "wb") as f:
                f.write(img_resp.content)
            return True, "Success"
        return False, "No URL in response"
    except Exception as e:
        return False, str(e)

def generate_openai(prompt, output_path):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key: return False, "No key"
    
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1792", # vertical 9:16
        "quality": "standard"
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}: {resp.text[:100]}"
            
        data = resp.json()
        img_url = data.get("data", [{}])[0].get("url")
        if img_url:
            img_resp = requests.get(img_url)
            with open(output_path, "wb") as f:
                f.write(img_resp.content)
            return True, "Success"
        return False, "No URL in response"
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--provider", default="nvidia")
    args = parser.parse_args()
    
    if args.provider == "nvidia":
        success, msg = generate_nvidia(args.prompt, args.output)
    elif args.provider == "xai":
        success, msg = generate_xai(args.prompt, args.output)
    elif args.provider == "openai":
        success, msg = generate_openai(args.prompt, args.output)
    else:
        success, msg = False, "Unknown provider"
        
    if success:
        print(f"✅ SUCCESS: {args.output}")
        exit(0)
    else:
        print(f"❌ FAILED: {msg}")
        exit(1)

if __name__ == "__main__":
    main()
