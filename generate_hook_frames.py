#!/usr/bin/env python3
"""
Generate Hook Frames for JENDRALBOT Products
Using AI image generation (Gemini or external API)
"""

import json
from pathlib import Path

PRODUCTS_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_products.json"
OUTPUT_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_products():
    with open(PRODUCTS_FILE) as f:
        data = json.load(f)
        return data['products']

def generate_image_prompts(products):
    """Generate image prompts for each product"""
    prompts = {}

    for product in products:
        name = product['name']
        price = product.get('price', 0) if product.get('is_paid') else "GRATIS"

        # Create curiosity hook
        prompts[f"{name}_curiosity"] = f"""
Vertical 9:16 image for TikTok/Instagram Reel.
Product: {name}
Price: IDR {price}
Style: Bold, high contrast, viral TikTok aesthetic.
Text: "{name}" in large bold red/yellow text.
Hook: "GILA!" or "PARAH!" or "KAGET?" in attention-grabbing font.
Background: Dark gradient (black to dark blue).
Additional text: Price tag "{price}" in contrasting color.
Make it scroll-stopping, 3-second attention grabber.
"""

        # Create problem-solution hook
        prompts[f"{name}_solution"] = f"""
Vertical 9:16 image for social media.
Product: {name}
Price: IDR {price}
Style: Problem-solution split design.
Left side: "Masalah?" or "Susah?" in red.
Right side: "Solusi!" with product name in green.
Background: Split - dark red (left) to dark green (right).
Price: "{price}" clearly visible.
Professional yet attention-grabbing.
"""

        # Create benefit-focused hook
        prompts[f"{name}_benefit"] = f"""
Vertical 9:16 promotional image.
Product: {name}
Price: IDR {price}
Style: Benefit-focused visual.
Main text: "Auto Profit!" or "Langsung Cuan!"
Subtitle: Product name in white bold.
Call-to-action: "Link in bio" arrow pointing down.
Background: Gradient gold to dark blue.
Price tag: Large "{price}" in gold.
Premium but accessible feel.
"""

    return prompts

def save_prompts_to_file(prompts):
    """Save prompts for AI image generation"""
    prompts_file = OUTPUT_DIR / "image_prompts.json"

    with open(prompts_file, 'w') as f:
        json.dump(prompts, f, indent=2)

    print(f"✅ Generated {len(prompts)} image prompts")
    print(f"📁 Saved to: {prompts_file}")
    print()

    return prompts_file

def main():
    print("="*60)
    print("🎨 GENERATING HOOK FRAME PROMPTS")
    print("="*60)
    print()

    products = load_products()
    print(f"📦 Found {len(products)} products")
    print()

    prompts = generate_image_prompts(products)
    print(f"🎯 Created {len(prompts)} image prompts")
    print()

    prompts_file = save_prompts_to_file(prompts)

    print("="*60)
    print("📋 NEXT: Use these prompts with AI image generator")
    print("="*60)
    print()
    print("Options:")
    print("1. Gemini AI Image Generator (built-in)")
    print("2. DALL-E via API")
    print("3. Midjourney")
    print("4. Stable Diffusion (local)")
    print("5. Canva AI Image")
    print()
    print("Recommended: Use gemini-image-generator skill")
    print("Command:")
    print(f"  python -c \"from skills.gemini_image_generator import generate; generate_from_file('{prompts_file}')\"")

if __name__ == "__main__":
    main()