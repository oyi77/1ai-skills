#!/usr/bin/env python3
"""
Character Consistency System

Maintains consistent characters/avatars across all content:
- Base character images
- Style parameters for regeneration
- Scene variations with same character
- Background consistency
"""

import json
import os
import requests
from pathlib import Path
from datetime import datetime

CHARACTERS_DIR = Path(__file__).parent.parent / "characters"
CHARACTERS_DIR.mkdir(exist_ok=True)

GEMINIGEN_API_KEY = os.environ.get("GEMINIGEN_API_KEY", "geminiai-89bb141f0c3a1075bff6fbdcd31ca701")
GEMINIGEN_BASE = "https://api.geminigen.ai/uapi/v1"

# Default character styles
DEFAULT_CHARACTERS = {
    "avatar_motivator": {
        "name": "Motivator Avatar",
        "style": "anime style, Indonesian male, confident smile, casual outfit, warm lighting",
        "negative": "realistic, photo, western features",
        "base_prompt": "Portrait of {style}, facing camera, upper body, clean background"
    },
    "avatar_beauty": {
        "name": "Beauty Avatar", 
        "style": "anime style, Indonesian female, gentle smile, hijab, soft makeup",
        "negative": "realistic, photo, revealing clothes",
        "base_prompt": "Portrait of {style}, soft lighting, beauty influencer pose"
    },
    "avatar_tech": {
        "name": "Tech Bro Avatar",
        "style": "anime style, young Asian male, glasses, hoodie, confident look",
        "negative": "realistic, photo, formal suit",
        "base_prompt": "Portrait of {style}, tech startup vibe, laptop in background"
    }
}

# Scene templates
SCENE_TEMPLATES = {
    "kitchen": "in a modern kitchen, cooking, warm lighting",
    "office": "in a home office, working on laptop, professional setting",
    "outdoor": "outdoor setting, natural lighting, greenery background",
    "bedroom": "in a cozy bedroom, relaxed atmosphere",
    "gym": "at the gym, fitness setting, energetic vibe",
    "cafe": "at a trendy cafe, coffee shop atmosphere",
}


def get_character(character_id: str) -> dict:
    """Get character configuration."""
    char_dir = CHARACTERS_DIR / character_id
    config_path = char_dir / "config.json"
    
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    
    # Check defaults
    if character_id in DEFAULT_CHARACTERS:
        return DEFAULT_CHARACTERS[character_id]
    
    return None


def create_character(character_id: str, config: dict):
    """Create a new character."""
    char_dir = CHARACTERS_DIR / character_id
    char_dir.mkdir(exist_ok=True)
    (char_dir / "variations").mkdir(exist_ok=True)
    
    config["id"] = character_id
    config["created_at"] = datetime.now().isoformat()
    
    with open(char_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    return char_dir


def generate_character_image(character_id: str, scene: str = None, output_path: Path = None) -> Path:
    """Generate image for character, optionally in a scene."""
    char = get_character(character_id)
    if not char:
        raise ValueError(f"Character '{character_id}' not found")
    
    # Build prompt
    style = char.get("style", "")
    base_prompt = char.get("base_prompt", "Portrait of {style}")
    prompt = base_prompt.format(style=style)
    
    # Add scene if specified
    if scene:
        scene_desc = SCENE_TEMPLATES.get(scene, scene)
        prompt = f"{prompt}, {scene_desc}"
    
    # Generate with GeminiGen
    headers = {"x-api-key": GEMINIGEN_API_KEY}
    resp = requests.post(
        f"{GEMINIGEN_BASE}/generate_image",
        headers=headers,
        data={
            "prompt": prompt,
            "model": "nano-banana-pro",
            "aspect_ratio": "9:16",
            "style": "Anime General",
            "resolution": "1K"
        }
    )
    result = resp.json()
    
    if "uuid" not in result:
        raise Exception(f"Generation failed: {result}")
    
    uuid = result["uuid"]
    print(f"  Generating... UUID: {uuid}")
    
    # Poll for result
    import time
    for _ in range(60):
        time.sleep(3)
        status = requests.get(f"{GEMINIGEN_BASE}/history/{uuid}", headers=headers).json()
        if status.get("status") == 2:
            img_url = status["generated_image"][0]["image_url"]
            img_data = requests.get(img_url).content
            
            # Determine output path
            if not output_path:
                char_dir = CHARACTERS_DIR / character_id
                char_dir.mkdir(exist_ok=True)
                if scene:
                    output_path = char_dir / "variations" / f"{scene}.png"
                else:
                    output_path = char_dir / "base.png"
            
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_bytes(img_data)
            print(f"  ✅ Saved: {output_path}")
            return output_path
        elif status.get("status") == 3:
            raise Exception(f"Generation failed: {status.get('error_message')}")
    
    raise Exception("Generation timeout")


def list_characters() -> list:
    """List all available characters."""
    characters = []
    
    # From directories
    for d in CHARACTERS_DIR.iterdir():
        if d.is_dir():
            config_path = d / "config.json"
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                    characters.append({
                        "id": d.name,
                        "name": config.get("name", d.name),
                        "has_base": (d / "base.png").exists(),
                        "variations": len(list((d / "variations").glob("*.png"))) if (d / "variations").exists() else 0
                    })
    
    # Add defaults not yet created
    for char_id in DEFAULT_CHARACTERS:
        if not any(c["id"] == char_id for c in characters):
            characters.append({
                "id": char_id,
                "name": DEFAULT_CHARACTERS[char_id]["name"],
                "has_base": False,
                "variations": 0,
                "is_default": True
            })
    
    return characters


def init_characters():
    """Initialize default characters with base images."""
    print("🎨 Initializing default characters...")
    
    for char_id, config in DEFAULT_CHARACTERS.items():
        print(f"\n📦 Creating {char_id}...")
        create_character(char_id, config)
        
        try:
            generate_character_image(char_id)
        except Exception as e:
            print(f"  ⚠️ Could not generate base image: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Character Consistency System")
    parser.add_argument("--list", action="store_true", help="List all characters")
    parser.add_argument("--create", type=str, help="Create character with ID")
    parser.add_argument("--style", type=str, help="Style description for new character")
    parser.add_argument("--generate", type=str, help="Generate image for character ID")
    parser.add_argument("--scene", type=str, help="Scene for generation")
    parser.add_argument("--init", action="store_true", help="Initialize default characters")
    parser.add_argument("--scenes", action="store_true", help="List available scenes")
    
    args = parser.parse_args()
    
    if args.init:
        init_characters()
    elif args.list:
        characters = list_characters()
        print("🎭 Characters:")
        for c in characters:
            status = "✅" if c.get("has_base") else "⏳"
            default = " (default)" if c.get("is_default") else ""
            print(f"  {status} {c['id']}: {c['name']}{default} ({c['variations']} variations)")
    elif args.scenes:
        print("🎬 Available Scenes:")
        for scene, desc in SCENE_TEMPLATES.items():
            print(f"  {scene}: {desc}")
    elif args.create:
        config = {
            "name": args.create,
            "style": args.style or "anime style character",
            "base_prompt": "Portrait of {style}, facing camera"
        }
        path = create_character(args.create, config)
        print(f"✅ Created character: {path}")
        
        if args.style:
            print("🎨 Generating base image...")
            generate_character_image(args.create)
    elif args.generate:
        print(f"🎨 Generating image for {args.generate}...")
        path = generate_character_image(args.generate, scene=args.scene)
        print(f"✅ Generated: {path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
