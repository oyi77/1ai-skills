#!/usr/bin/env python3
import os
import json
import requests
import time
import argparse
from pathlib import Path

# Paths
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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") # Using the key from logs if available or env
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def expand_script(short_caption):
    """
    Expand a short caption into a 50-60 second narrative script using Groq.
    """
    prompt = f"""
    You are a viral TikTok scriptwriter. Expand this short caption into a 50-60 second narrative script in INDONESIAN.
    The tone should be persuasive, motivational, and natural (human-like).
    
    ORIGINAL CAPTION: {short_caption}
    
    REQUIREMENTS:
    1. Use simple, direct Indonesian language.
    2. Add a strong hook at the beginning.
    3. Include a middle section that explains the "Pain Points" and "Solution".
    4. End with a clear but natural Call to Action.
    5. Duration must be around 140-160 words (to hit ~60 seconds).
    
    Return ONLY the script text, no introductions.
    """
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"⚠️ Groq Error: {resp.status_code}")
            return short_caption * 3 # Simple fallback
    except Exception as e:
        print(f"⚠️ Script expansion failed: {e}")
        return short_caption

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    print(expand_script(args.text))
