#!/usr/bin/env python3
"""
Load Google Maps API Key from OpenClaw Config
"""

import json
import os
from pathlib import Path

# Try multiple locations to find the API key
possible_locations = [
    Path.home() / ".credentials" / "google_places.txt",
    Path.home() / ".credentials" / "google_maps.txt",
    Path.home() / ".openclaw" / "config.json",
    Path.home() / ".openclaw.json",
    Path.home() / ".google_places_api_key.txt",
]

api_key = None

for location in possible_locations:
    if location.exists():
        try:
            if "config.json" in location.name or location.name == ".openclaw.json":
                with open(location) as f:
                    config = json.load(f)
                    # Try multiple paths in config
                    api_key = config.get("google_places_api_key") or \
                             config.get("google_maps_api_key") or \
                             config.get("credentials", {}).get("google_places") or \
                             config.get("credentials", {}).get("google_maps")

                    if api_key:
                        print(f"[INFO] Found API key in {location.name}")
                        break
            else:
                with open(location) as f:
                    content = f.read().strip()
                    if content and len(content) > 10:
                        api_key = content
                        print(f"[INFO] Found API key in {location.name}")
                        break
        except Exception as e:
            continue

if api_key:
    print(f"[SUCCESS] Google Maps API Key: {api_key[:20]}...{api_key[-4:]}")
else:
    print("[ERROR] API Key not found in standard locations")
    print(f"Checked: {', '.join([str(l) for l in possible_locations])}")

print()
print(f"API KEY: {api_key}")