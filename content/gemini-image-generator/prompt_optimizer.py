#!/usr/bin/env python3
"""
Gemini Prompt Optimizer
Generate optimal REFINER PRODUKSI instructions for product image generation.
"""

import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional

# Load configuration
CONFIG_PATH = Path(__file__).parent / "config.yaml"
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Default templates (embedded fallback)
TEMPLATES = {
    "fashion": {
        "environments": [
            "clean white studio background, professional e-commerce style",
            "minimal gray backdrop, contemporary aesthetic",
            "premium lifestyle setting, urban environment"
        ],
        "lighting": ["soft diffused studio lighting", "natural daylight", "dramatic side lighting"],
        "styles": ["minimal", "premium", "casual", "luxury"]
    },
    "electronics": {
        "environments": [
            "modern tech backdrop, sleek gradient",
            "futuristic environment, holographic elements",
            "clean workspace, professional setup"
        ],
        "lighting": ["cool tech lighting", "neon accents", "clean white light"],
        "styles": ["modern", "tech", "minimal", "futuristic"]
    },
    "food": {
        "environments": [
            "clean marble surface, culinary styling",
            "warm rustic table, cozy atmosphere",
            "premium restaurant backdrop, elegant presentation"
        ],
        "lighting": ["warm natural light", "dramatic food photography lighting", "soft diffused"],
        "styles": ["appetizing", "fresh", "premium", "rustic"]
    },
    "beauty": {
        "environments": [
            "soft gradient background, feminine aesthetic",
            "clean white spa setting, minimal decor",
            "luxury vanity setup, premium feel"
        ],
        "lighting": ["soft diffused beauty lighting", "ring light effect", "gentle side lighting"],
        "styles": ["elegant", "fresh", "luxury", "natural"]
    },
    "home": {
        "environments": [
            "cozy living room, warm natural setting",
            "modern minimal interior, contemporary design",
            "luxury home environment, premium lifestyle"
        ],
        "lighting": ["warm ambient lighting", "natural daylight", "soft evening light"],
        "styles": ["cozy", "modern", "premium", "minimal"]
    }
}


def load_config() -> Dict:
    """Load configuration from YAML file"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def load_template(category: str) -> Dict:
    """Load template for category"""
    # Try file first
    template_file = TEMPLATES_DIR / f"{category}.txt"
    if template_file.exists():
        return {"base": template_file.read_text(encoding='utf-8')}
    
    # Fallback to embedded
    return TEMPLATES.get(category, TEMPLATES["fashion"])


def generate_instruction(
    category: str = "fashion",
    product_name: str = "product",
    style: Optional[str] = None,
    lighting: Optional[str] = None,
    custom_details: str = ""
) -> str:
    """
    Generate REFINER PRODUKSI instruction for Gemini.
    
    Args:
        category: Product category (fashion, electronics, food, beauty, home)
        product_name: Name of product
        style: Visual style (optional, auto-selected if not provided)
        lighting: Lighting setup (optional, auto-selected if not provided)
        custom_details: Additional instructions
    
    Returns:
        Complete instruction string for Gemini
    """
    template = load_template(category)
    
    # Select environment
    environments = template.get("environments", ["clean studio background"])
    environment = environments[0] if not style else next(
        (e for e in environments if style.lower() in e.lower()), environments[0]
    )
    
    # Select lighting
    lighting_options = template.get("lighting", ["soft diffused"])
    lighting_setup = lighting if lighting else lighting_options[0]
    
    # Get style
    styles = template.get("styles", ["premium"])
    selected_style = style if style else styles[0]
    
    # Build instruction
    instruction = f"""REFINER PRODUKSI: {environment}
Rasio: 9:16
Lighting: {lighting_setup}
Intruksi tambahan: Generate {selected_style} posed product photography featuring {product_name}. Professional e-commerce quality, TikTok optimized vertical format (9:16). Integrate model pose naturally with product. Clean composition, high-end aesthetic. {custom_details}"""
    
    return instruction.strip()


def generate_short_instruction(
    category: str,
    product_name: str
) -> str:
    """
    Generate concise instruction for quick use.
    
    Args:
        category: Product category
        product_name: Product name
    
    Returns:
        Short instruction string
    """
    templates = {
        "fashion": f"Fashion product: {product_name}. Clean studio background, soft lighting, 9:16 ratio. Professional e-commerce style, model posing naturally with product.",
        "electronics": f"Tech product: {product_name}. Modern gradient backdrop, cool lighting, 9:16 ratio. Sleek presentation, minimalist aesthetic.",
        "food": f"Food product: {product_name}. Marble surface, warm natural lighting, 9:16 ratio. Appetizing presentation, culinary styling.",
        "beauty": f"Beauty product: {product_name}. Soft gradient background, ring light effect, 9:16 ratio. Elegant feminine aesthetic.",
        "home": f"Home product: {product_name}. Cozy interior setting, warm ambient lighting, 9:16 ratio. Lifestyle presentation."
    }
    
    return templates.get(category, templates["fashion"])


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate optimal prompts for Gemini Product Image Generation"
    )
    
    parser.add_argument(
        "--category", "-c",
        choices=["fashion", "electronics", "food", "beauty", "home"],
        default="fashion",
        help="Product category"
    )
    
    parser.add_argument(
        "--product", "-p",
        required=True,
        help="Product name/description"
    )
    
    parser.add_argument(
        "--style", "-s",
        help="Visual style (optional)"
    )
    
    parser.add_argument(
        "--lighting", "-l",
        help="Lighting setup (optional)"
    )
    
    parser.add_argument(
        "--details", "-d",
        default="",
        help="Additional details/instructions"
    )
    
    parser.add_argument(
        "--short",
        action="store_true",
        help="Generate concise instruction"
    )
    
    args = parser.parse_args()
    
    if args.short:
        instruction = generate_short_instruction(
            category=args.category,
            product_name=args.product
        )
    else:
        instruction = generate_instruction(
            category=args.category,
            product_name=args.product,
            style=args.style,
            lighting=args.lighting,
            custom_details=args.details
        )
    
    print("="*70)
    print("GEMINI IMAGE GENERATION INSTRUCTION")
    print("="*70)
    print()
    print(instruction)
    print()
    print("="*70)
    print("Steps:")
    print("1. Open: https://gemini.google.com/share/c7150b8213a4")
    print("2. Upload pose model image")
    print("3. Upload product image") 
    print("4. Paste instruction above")
    print("5. Generate images")
    print("="*70)


if __name__ == "__main__":
    main()
