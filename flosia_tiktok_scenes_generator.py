#!/usr/bin/env python3
"""Generate 6 Flosia TikTok scene images using NVIDIA NIM API."""

import asyncio
import base64
import os
import sys
from pathlib import Path

# Add skills path
sys.path.insert(0, str(Path(__file__).parent / "skills" / "content-generator" / "scripts"))

from providers.nvidia import NVIDIAProvider

# Scene prompts for Flosia Deterjen TikTok content
SCENE_PROMPTS = {
    "scene1": """Indonesian woman 25-30 years old, natural beauty, warm brown skin, long wavy black头发, confident smile, wearing casual modern outfit, holding a Flosia Deterjen bottle with brand logo visible, bright natural lighting, modern Indonesian home interior background, clean and welcoming atmosphere, 9:16 vertical professional product photography, realistic skin texture, detailed fabric, soft shadows""",

    "scene2": """Indonesian woman 25-30 years old, same person as before with identical appearance, pouring liquid from Flosia Deterjen bottle into washing machine or bucket, concentration expression, bright laundry room setting, natural daylight, dynamic motion capture, clothes detergent foaming effect, 9:16 vertical shot, realistic detail, professional commercial photography""",

    "scene3": """Indonesian woman 25-30 years old, same person with identical appearance, demonstrating Flosia Deterjen cleaning dirty laundry, showing before-and-after effect, hands immersed in soapy water, satisfaction expression, outdoor laundry area with sunlight, 9:16 vertical professional shot, detailed water and soap effects, clean bright aesthetic""",

    "scene4": """Indonesian woman 25-30 years old, same person with identical appearance, holding up clean bright white laundry with proud satisfied expression, sunshine background, clothes hanging on line, result of using Flosia Deterjen, vibrant colors, happiness, 9:16 vertical lifestyle photography, soft natural lighting, professional quality""",

    "scene5": """Indonesian woman 25-30 years old, same person with identical appearance, close-up shot holding Flosia Deterjen bottle, pointing to product features and label with confident expression, professional product photography, clean minimalist background, 9:16 vertical format, sharp focus on bottle and brand, studio lighting""",

    "scene6": """Indonesian woman 25-30 years old, same person with identical appearance, doing call to action gesture with hands, inviting smile looking directly at camera, warm enthusiastic expression, holding Flosia Deterjen bottle, bright Indonesian home interior, 9:16 vertical commercial shot, engaging personality, professional lighting"""
}

async def generate_scenes():
    """Generate all 6 scene images."""

    # Initialize NVIDIA provider
    provider = NVIDIAProvider()

    # Check availability
    is_available = await provider.is_available()
    if not is_available:
        print("❌ NVIDIA provider not available")
        return False

    print("✅ NVIDIA provider available")
    print(f"📸 Using model: {provider.get_default_model()}")
    print(f"🎯 Generating 6 scenes: 1080x1920 (9:16)\n")

    # Output directory
    output_dir = Path(__file__).parent / "flosia-tiktok-scenes-regenerated"
    output_dir.mkdir(exist_ok=True)

    # Generate each scene
    results = []
    for scene_name, prompt in SCENE_PROMPTS.items():
        print(f"\n🎬 Generating {scene_name}...")

        try:
            # Generate image (minimal payload - just prompt, no width/height)
            result = await provider.generate(
                prompt=prompt,
                model="black-forest-labs/flux.1-dev"
            )

            if result.success and result.data:
                # Save image
                if result.data.get("base64"):
                    image_data = base64.b64decode(result.data["base64"])
                    output_path = output_dir / f"{scene_name}.jpg"
                    with open(output_path, "wb") as f:
                        f.write(image_data)
                    print(f"✅ Saved: {output_path}")
                    results.append(str(output_path))
                else:
                    print(f"❌ No image data returned for {scene_name}")
            else:
                print(f"❌ Failed to generate {scene_name}")
                if result.metadata and "error" in result.metadata:
                    print(f"   Error: {result.metadata['error']}")

        except Exception as e:
            print(f"❌ Exception for {scene_name}: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Generated {len(results)}/6 scenes")
    print(f"📁 Output directory: {output_dir}")
    print(f"{'='*60}\n")

    # List all generated files
    if results:
        print("Generated scenes:")
        for i, path in enumerate(results, 1):
            print(f"  {i}. {path}")
        print()

    return len(results) == 6

if __name__ == "__main__":
    success = asyncio.run(generate_scenes())
    sys.exit(0 if success else 1)