#!/usr/bin/env python3
"""
Jendralbot Content Variator
Generate MANY variations of images & videos
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from itertools import product

# ── Configuration ──────────────────────────────────────────────────────────────────
PRODUCTS = {
    "starter_ai_content": {
        "name": "Starter AI Content",
        "price": "Rp 49.000",
        "link": "https://lynk.id/jendralbot/xlymwzj2jylv",
        "niche": "beginners",
        "hashtags": "#AIcontent #contentcreation #starter #AIindonesia #belajarAI"
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "niche": "ecommerce",
        "hashtags": "#ecommerce #onlinestore #productphoto #marketplace #AIbusiness"
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": "Rp 75.000",
        "link": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "niche": "culinary",
        "hashtags": "#kuliner #foodphotography #GoFood #GrabFood #restaurant"
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "niche": "professional",
        "hashtags": "#AIcontent #professional #business #AIautomation #efficiency"
    }
}

# ── Variation Options ─────────────────────────────────────────────────────────────

# Image Generation Prompts (Gemini 3 Pro Image)
IMAGE_VARIATIONS = {
    "styles": [
        "professional minimalist studio shot",
        "modern tech startup aesthetic",
        "creative colorful vibrant",
        "elegant premium luxury style",
        "playful friendly casual",
        "clean white background",
        "gradient background with tech feel",
        "dark mode aesthetic"
    ],
    "subjects": [
        "product package mockup",
        "app interface showcase",
        "user using mobile app",
        "dashboard screenshot",
        "benefit visualization",
        "before vs after comparison",
        "workflow diagram",
        "success story illustration"
    ],
    "elements": [
        "with AI robot assistant",
        "with smartphone showing app",
        "with data visualization charts",
        "with happy user testimonial",
        "with productivity tools",
        "with modern office setup",
        "with cloud and sync icons",
        "with automation symbols"
    ],
    "colors": [
        "blue and white color scheme",
        "purple and gradient",
        "green and eco-friendly",
        "orange and energy",
        "black and premium",
        "multi-color rainbow",
        "brand specific colors"
    ]
}

# TikTok Video Concepts
VIDEO_CONCEPTS = {
    "hooks": [
        "Problem-Solution",
        "Before-After",
        "How-To Tutorial",
        "Testimonial Story",
        "Benefit Highlight",
        "Value Proposition",
        "Feature Showcase",
        "Comparison"
    ],
    "tones": [
        "Professional & Business",
        "Casual & Friendly",
        "Urgent & Exciting",
        "Educational & Step-by-step",
        "Emotional & Story-driven",
        "Direct & Sales-focused",
        "Humorous & Light",
        "Inspiring & Motivational"
    ],
    "durations": [15, 30, 45, 60],  # seconds
    "styles": [
        "fast-paced montage",
        "slow cinematic",
        "screen recording style",
        "animation motion graphics",
        "user-generated content style",
        " testimonial interview",
        "product demonstration",
        "benefit visualizer"
    ]
}

# Caption Variations
CAPTION_VARIATIONS = {
    "hooks": [
        "🔥 STOP - Problem statement",
        "😱 Shocking truth reveal",
        "💡 Smart discovery revealed",
        "🚀 Secret weapon discovered",
        "🎯 Pain point identified",
        "✨ Transformation story",
        "⚠️ Reality check",
        "💎 Premium insight shared"
    ],
    "structures": [
        "Problem → Agitation → Solution",
        "Before → Bridge → After",
        "Hook → Story → Value → CTA",
        "Question → Answer → Action",
        "Myth → Fact → Proof",
        "Struggle → Breakthrough → Result"
    ],
    "cta_types": [
        "DM me 'INFO' for details",
        "Tap link in bio",
        "Comment 'MAU' for access",
        "Save this for later",
        "Share with someone who needs",
        "Follow for daily tips"
    ],
    "hashtag_mixes": [
        "Trending (10) + Niche (5) + Brand (3)",
        "Niche (15) + Trending (3)",
        "Broad (8) + Specific (10)",
        "High-volume (18)",
        "Niche-precise (10)"
    ]
}

# ── Generation Logic ─────────────────────────────────────────────────────────────

def generate_image_prompt(product_key, variation_idx):
    """Generate unique image prompt for each variation"""
    product = PRODUCTS[product_key]

    # Select variations based on index
    style = IMAGE_VARIATIONS["styles"][variation_idx % len(IMAGE_VARIATIONS["styles"])]
    subject = IMAGE_VARIATIONS["subjects"][(variation_idx // len(IMAGE_VARIATIONS["styles"])) % len(IMAGE_VARIATIONS["subjects"])]
    element = IMAGE_VARIATIONS["elements"][(variation_idx // (len(IMAGE_VARIATIONS["styles"]) * len(IMAGE_VARIATIONS["subjects"]))) % len(IMAGE_VARIATIONS["elements"])]
    color = IMAGE_VARIATIONS["colors"][variation_idx % len(IMAGE_VARIATIONS["colors"])]

    # Build prompt
    prompt = f"""
    Professional product photography for {product['name']} ({product['price']}).

    Style: {style}
    Subject: {subject}
    Element: {element}
    Color scheme: {color}
    Target audience: {product['niche']}

    Make it visually stunning, high quality, suitable for Instagram/TikTok marketing.
    Include price tag: {product['price']}
    Add subtle branding touches.
    """

    return prompt.strip()

def generate_video_concept(product_key, variation_idx):
    """Generate unique video concept for each variation"""
    product = PRODUCTS[product_key]

    hook = VIDEO_CONCEPTS["hooks"][variation_idx % len(VIDEO_CONCEPTS["hooks"])]
    tone = VIDEO_CONCEPTS["tones"][(variation_idx // len(VIDEO_CONCEPTS["hooks"])) % len(VIDEO_CONCEPTS["tones"])]
    duration = VIDEO_CONCEPTS["durations"][variation_idx % len(VIDEO_CONCEPTS["durations"])]
    style = VIDEO_CONCEPTS["styles"][(variation_idx // len(VIDEO_CONCEPTS["tones"])) % len(VIDEO_CONCEPTS["styles"])]

    concept = {
        "product": product_key,
        "hook": hook,
        "tone": tone,
        "duration": duration,
        "style": style,
        "prompt": f"""
        {product['name']} - {product['price']}

        Hook: {hook}
        Tone: {tone}
        Style: {style}
        Duration: {duration} seconds

        Key message:
        - Value proposition for {product['niche']}
        - How {product['name']} solves problems
        - Benefits and features
        - Call to action: {product['link']}

        Make it viral-worthy with strong engagement hooks.
        """
    }

    return concept

def generate_caption(product_key, variation_idx):
    """Generate unique caption for each variation"""
    product = PRODUCTS[product_key]

    hook = CAPTION_VARIATIONS["hooks"][variation_idx % len(CAPTION_VARIATIONS["hooks"])]
    structure = CAPTION_VARIATIONS["structures"][variation_idx % len(CAPTION_VARIATIONS["structures"])]
    cta = CAPTION_VARIATIONS["cta_types"][variation_idx % len(CAPTION_VARIATIONS["cta_types"])]
    hashtags = CAPTION_VARIATIONS["hashtag_mixes"][variation_idx % len(CAPTION_VARIATIONS["hashtag_mixes"])]

    # Generate caption based on structure
    if structure == "Problem → Agitation → Solution":
        caption = f"""
{hook}

Problem: [Pain point for {product['niche']}]

Agitation:
This keeps you stuck. Frustrating, isn't it?

Solution: {product['name']}
{product['price']}

[Key benefits to be filled]

{cta}

{product['link']}

{product['hashtags']}
        """.strip()

    elif structure == "Before → Bridge → After":
        caption = f"""
{hook}

BEFORE:
[Struggling with {product['niche']} challenges]

BRIDGE:
Then I discovered {product['name']}

AFTER:
[Success results with specific metrics]

{cta}

{product['link']}

{product['hashtags']}
        """.strip()

    elif structure == "Hook → Story → Value → CTA":
        caption = f"""
{hook}

[Relatable story about someone in {product['niche']}]

They tried {product['name']} and everything changed.

✅ [Benefit 1]
✅ [Benefit 2]
✅ [Benefit 3]

{cta}

{product['link']}

{product['hashtags']}
        """.strip()

    else:
        caption = f"""
{hook}

{product['name']} - {product['price']}

Perfect for {product['niche']}

[Value proposition]

{cta}

{product['link']}

{product['hashtags']}
        """.strip()

    return caption

def create_variation_plan(per_product=10):
    """Create comprehensive variation plan for all products"""

    plan = {
        "generated_at": datetime.now().isoformat(),
        "products": {}
    }

    for product_key in PRODUCTS:
        variations = []

        for idx in range(per_product):
            image_prompt = generate_image_prompt(product_key, idx)
            video_concept = generate_video_concept(product_key, idx)
            caption_text = generate_caption(product_key, idx)

            variation = {
                "variation_id": f"{product_key}_var_{idx + 1}",
                "image_prompt": image_prompt,
                "video_concept": video_concept,
                "caption": caption_text,
                "tags": {
                    "style_idx": idx % len(IMAGE_VARIATIONS["styles"]),
                    "hook_idx": idx % len(CAPTION_VARIATIONS["hooks"]),
                    "tone_idx": idx % len(VIDEO_CONCEPTS["tones"]),
                    "structure_idx": idx % len(CAPTION_VARIATIONS["structures"])
                }
            }

            variations.append(variation)

        plan["products"][product_key] = {
            "product_info": PRODUCTS[product_key],
            "total_variations": per_product,
            "variations": variations
        }

    return plan

def main():
    print("=" * 80)
    print("🎨 JENDRALBOT CONTENT VARIATOR")
    print("=" * 80)
    print()
    print("Generating VARIATIONS for images, videos, and captions...")
    print()

    per_product = 10  # Number of variations per product
    plan = create_variation_plan(per_product)

    # Save plan
    output_file = Path.home() / ".openclaw" / "workspace" / "jendralbot_variations.json"
    with open(output_file, "w") as f:
        json.dump(plan, f, indent=2)

    # Summary
    total_variations = len(PRODUCTS) * per_product

    print("=" * 80)
    print("📊 VARIATION PLAN SUMMARY")
    print("=" * 80)
    print()

    for product_key, data in plan["products"].items():
        print(f"📦 {data['product_info']['name']} ({data['product_info']['price']})")
        print(f"   Variations: {data['total_variations']}")
        print(f"   Images: {data['total_variations']} unique prompts")
        print(f"   Videos: {data['total_variations']} unique concepts")
        print(f"   Captions: {data['total_variations']} unique texts")
        print()

    print("=" * 80)
    print(f"✅ TOTAL:")
    print(f"   Products: {len(PRODUCTS)}")
    print(f"   Variations per product: {per_product}")
    print(f"   TOTAL VARIATIONS: {total_variations}")
    print()
    print(f"   That means:")
    print(f"   • {total_variations} UNIQUE images")
    print(f"   • {total_variations} UNIQUE videos")
    print(f"   • {total_variations} UNIQUE captions")
    print(f"   • ∞ INFINITE possible combinations!")
    print()
    print("=" * 80)
    print(f"✅ Plan saved to: {output_file}")
    print()
    print("📋 NEXT STEPS:")
    print("1. Review jendralbot_variations.json")
    print("2. Select variations you want to generate")
    print("3. Run generation scripts for images/videos")
    print("4. Post to social media with variety!")
    print("=" * 80)

if __name__ == "__main__":
    main()