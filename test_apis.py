#!/usr/bin/env python3
"""Test API Keys"""

import json
import urllib.request
import os

# ── Test Cerebras ─────────────────────────────────────────────────────────────
print("=" * 60)
print("Testing Cerebras AI")
print("=" * 60)

key = "csk-wt858dxn9v8f52wdc44h96mpdde238rccj29cfte4kyrdpme"

# Try different endpoint/model formats
configs = [
    {
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "model": "llama3.1-70b",
        "name": "llama3.1-70b"
    },
    {
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "model": "llama-3.3-70b",
        "name": "llama-3.3-70b"
    },
    {
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "model": "llama-3.1-70b",
        "name": "llama-3.1-70b"
    },
]

for cfg in configs:
    print(f"\nTrying: {cfg['name']}")
    payload = {
        "model": cfg["model"],
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 50,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(cfg["url"], data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        print(f"  ✅ Success! Response: {result.get('choices', [{}])[0].get('message', {}).get('content', '?')[:50]}")
        break
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP {e.code}: {e.read().decode()[:200]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

# ── Test BytePlus (AIML API) ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Testing BytePlus Seedance (via AIML API)")
print("=" * 60)

key = "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea"

configs = [
    {
        "name": "bytedance/seedance-1-0-lite-t2v",
        "model": "bytedance/seedance-1-0-lite-t2v"
    },
    {
        "name": "bytedance/seedance-1.0-lite-t2v",
        "model": "bytedance/seedance-1.0-lite-t2v"
    },
]

for cfg in configs:
    print(f"\nTrying: {cfg['name']}")
    payload = {
        "model": cfg["model"],
        "prompt": "A sunset over mountains, cinematic, 9:16",
        "resolution": "480p",  # smallest for test
        "duration": 5,
        "aspect_ratio": "9:16",
        "watermark": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request("https://api.aimlapi.com/v2/video/generations", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        print(f"  ✅ Success! Task ID: {result.get('id')}, Status: {result.get('status')}")
        break
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP {e.code}: {e.read().decode()[:300]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 60)
