#!/usr/bin/env python3
"""Viral Research + Content Pipeline"""

import argparse
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

OUTPUT_DIR = Path("output/viral_research")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load keys from env
BYTEPLUS_API_KEY = os.environ.get(
    "BYTEPLUS_API_KEY", "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea"
)
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")

CATEGORIES = [
    {"id": "601152", "name": "Fashion"},
    {"id": "600322", "name": "Beauty"},
    {"id": "600650", "name": "Home"},
]

CONTENT_TEMPLATES = {
    "motivation": {
        "headline": "Stop waiting for perfect moment\nThe time is NOW",
        "prompt": "Cinematic shot of person stepping into light, empowering, 4k",
        "caption": "The perfect moment doesn't exist. Stop waiting. Start NOW. 💪 #motivation #mindset #success",
    },
    "money": {
        "headline": "Money follows action\nNot wishes",
        "prompt": "Business person walking confidently in city, successful, golden hour, 4k",
        "caption": "Stop wishing for money. Start DOING. 💰 #money #wealth #entrepreneur",
    },
    "beauty": {
        "headline": "This transformation\nChanged everything",
        "prompt": "Beautiful face, soft lighting, makeup transformation, 4k",
        "caption": "POV: When you find the holy grail 💄✨ #beauty #makeup #transformation",
    },
}


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def generate_content(niche):
    t = CONTENT_TEMPLATES.get(niche, CONTENT_TEMPLATES["motivation"])
    return {"niche": niche, **t}


def run_pipeline(cookies=None):
    now = datetime.now()
    print("=" * 50)
    print("🚀 VIRAL PIPELINE")
    print(f"   Time: {now.strftime('%Y-%m-%d %H:%M')} WIB")
    print(f"   BytePlus: {'✅' if BYTEPLUS_API_KEY else '❌'}")
    print("=" * 50)

    if not cookies:
        print("\n⚠️ Using patterns (no cookies)")

    # Generate 3 content pieces
    for niche in ["motivation", "money", "beauty"]:
        content = generate_content(niche)
        print(f"\n--- {niche.upper()} ---")
        print(f"📣 {content['headline']}")
        print(f"📝 {content['caption'][:50]}...")
        print(f"🎬 {content['prompt'][:40]}...")

        if BYTEPLUS_API_KEY:
            print(f"   ✅ Ready for BytePlus video")

    # Save
    path = OUTPUT_DIR / f"content_{now.strftime('%Y%m%d_%H%M%S')}.json"
    save_json(
        {
            "timestamp": now.isoformat(),
            "content": [generate_content(n) for n in ["motivation", "money", "beauty"]],
        },
        path,
    )
    print(f"\n✅ Saved: {path}")


if __name__ == "__main__":
    run_pipeline()
