#!/usr/bin/env python3
"""
Generate Maya character reference images using NVIDIA Flux API
"""

import requests
import base64
import json
import os
from pathlib import Path

# NVIDIA Flux API key
NVIDIA_API_KEY = "REDACTED_NVIDIA_API_KEY"

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
        response = requests.post(url, headers=headers, json=payload, timeout=60)
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

# Maya character description
maya_base_prompt = "Maya, friendly female narrator, 2D minimalist cartoon style, pastel color palette (soft blue, green, cream tones), clean smooth lines, professional animation quality, simple but detailed enough to be recognizable, consistent character design"

# Generate Maya with different expressions
expressions = [
    ("neutral", "neutral calm expression, slight gentle smile, approachable and trustworthy, engaging the viewer, solid pastel blue background"),
    ("concerned", "slightly concerned expression, furrowed brows, worried look, empathetic, soft green background"),
    ("dramatic", "dramatic shocked expression, wide eyes, serious and intense, darker tones, conveying gravity of betrayal"),
    ("wise", "wise knowing expression, calm and confident, lessons learned, warm cream background, authoritative yet friendly"),
]

output_dir = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories/character_reference"
generated_images = []

print("=" * 60)
print("Generating Maya Character Reference Images")
print("=" * 60)

for expr_name, expr_desc in expressions:
    filename = f"maya_{expr_name}.png"
    output_path = os.path.join(output_dir, filename)

    prompt = f"{maya_base_prompt}, {expr_desc}, 9:16 vertical aspect ratio"

    result = generate_flux_image(prompt, output_path)
    if result:
        generated_images.append(result)

# Save character reference metadata
reference_data = {
    "character_name": "Maya",
    "description": "Friendly female narrator for betrayal stories",
    "visual_style": "2D minimalist cartoon with pastel palette",
    "palette": ["soft blue", "green", "cream"],
    "expressions": [os.path.basename(img) for img in generated_images],
    "generation_date": "2026-03-10",
    "generated_images": generated_images
}

reference_file = os.path.join(output_dir, "maya_character_reference.json")
with open(reference_file, 'w') as f:
    json.dump(reference_data, f, indent=2)

print(f"\n✓ Character reference saved: {reference_file}")
print(f"\nTotal images generated: {len(generated_images)}")
print("=" * 60)