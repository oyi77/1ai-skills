#!/usr/bin/env python3
"""
Generate scene images for Maya betrayal story using NVIDIA Flux API
"""

import requests
import base64
import json
import os
from pathlib import Path

# NVIDIA Flux API key
NVIDIA_API_KEY = "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"

def generate_flux_image(prompt, output_path):
    """Generate image using NVIDIA Flux API"""

    url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()

        result = response.json()

        # Extract and decode base64 image
        image_data = base64.b64decode(result['artifacts'][0]['base64'])

        # Save image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(image_data)

        print(f"✓ Generated: {output_path}")
        return output_path

    except Exception as e:
        print(f"✗ Error generating image: {e}")
        return None

# Maya character prompt (for consistency)
maya_prompt = "Maya, friendly female narrator, 2D minimalist cartoon style, pastel color palette (soft blue, green, cream), clean smooth lines, consistent character design"

# First, generate the missing Maya expression (wise)
print("\n[EXTRA] Generating missing Maya wise expression...")
wise_prompt = f"{maya_prompt}, wise knowing expression, calm and confident, lessons learned, warm cream background, authoritative yet friendly, 9:16 vertical aspect ratio"
wise_output = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories/character_reference/maya_wise.png"
wise_result = generate_flux_image(wise_prompt, wise_output)
if wise_result:
    print(f"✓ Generated missing wise expression")

# Scene descriptions based on story script
scenes = [
    {
        "name": "01_hook_intro",
        "prompt": f"{maya_prompt}, Maya speaking directly to viewer with serious expression, pointing finger forward, text overlay 'If you loan money to a friend', dramatic lighting, 9:16 vertical aspect ratio",
        "timing": "0-3s"
    },
    {
        "name": "02_partnership",
        "prompt": "2D minimalist cartoon scene, two male business partners John and Mike in modern office, shaking hands, looking excited, pastel professional colors, building startup from scratch, clean simple design, 9:16 vertical aspect ratio",
        "timing": "3-20s"
    },
    {
        "name": "03_success",
        "prompt": "2D minimalist cartoon, startup success scene, growing upward graphs, money symbols, celebration, pastel green and blue colors, business growth visualization, clean design, 9:16 vertical aspect ratio",
        "timing": "20-25s"
    },
    {
        "name": "04_betrayal",
        "prompt": f"{maya_prompt}, Maya with dramatic shocked expression, dark background with red undertones, conveying betrayal and shock, intense atmosphere, 9:16 vertical aspect ratio",
        "timing": "25-35s"
    },
    {
        "name": "05_transfer",
        "prompt": "2D minimalist cartoon, money being transferred from company account to personal account, visual of betrayal, dark dramatic colors, money bags flying away, 9:16 vertical aspect ratio",
        "timing": "35-40s"
    },
    {
        "name": "06_lawsuit",
        "prompt": "2D minimalist cartoon, document pile representing lawsuits, papers everywhere, overwhelming paperwork, frustrated person, somber atmosphere, 9:16 vertical aspect ratio",
        "timing": "40-45s"
    },
    {
        "name": "07_lesson",
        "prompt": f"{maya_prompt}, Maya with wise calm expression, warm friendly tone, teaching lesson, cream background with peace symbols, trustworthy and knowledgeable, 9:16 vertical aspect ratio",
        "timing": "45-55s"
    },
    {
        "name": "08_cta",
        "prompt": f"{maya_prompt}, Maya inviting gesture, friendly smile, looking at camera encouraging follow, bright positive energy, soft blue background, 9:16 vertical aspect ratio",
        "timing": "55-60s"
    },
]

output_dir = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories/scenes"
generated_images = []

print("=" * 60)
print("Generating Maya Betrayal Story Scenes")
print("=" * 60)

for i, scene in enumerate(scenes, 1):
    print(f"\n[{i}/{len(scenes)}] Scene: {scene['name']} ({scene['timing']})")

    filename = f"scene_{scene['name']}.png"
    output_path = os.path.join(output_dir, filename)

    prompt = scene['prompt']

    result = generate_flux_image(prompt, output_path)
    if result:
        generated_images.append({
            "name": scene['name'],
            "path": result,
            "timing": scene['timing']
        })

# Save scenes metadata
scenes_data = {
    "total_scenes": len(generated_images),
    "story": "The $50,000 Business Betrayal",
    "duration": "60 seconds",
    "aspect_ratio": "9:16",
    "style": "2D minimalist cartoon with pastel palette",
    "generated_at": "2026-03-10",
    "scenes": generated_images
}

scenes_file = os.path.join(output_dir, "scenes_metadata.json")
with open(scenes_file, 'w') as f:
    json.dump(scenes_data, f, indent=2)

print(f"\n✓ Scenes metadata saved: {scenes_file}")
print(f"\nTotal scenes generated: {len(generated_images)}")
print("=" * 60)