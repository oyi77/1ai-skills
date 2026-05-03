#!/usr/bin/env python3
"""
Persona Manager - Multi-Account Persona System

Manages different personas for each social media account to ensure:
- No duplicate content across accounts
- Unique voice/style per account
- Consistent character representation
"""

import json
import os
from pathlib import Path
from datetime import datetime

PERSONAS_DIR = Path(__file__).parent.parent / "personas"
PERSONAS_DIR.mkdir(exist_ok=True)

DEFAULT_PERSONAS = {
    "motivator_id": {
        "name": "Motivator Indonesia",
        "language": "id",
        "niche": "motivation",
        "style": {
            "tone": "inspiring, warm, relatable",
            "emoji_usage": "moderate",
            "slang_level": "casual Indonesian",
            "signature": "💪🔥"
        },
        "character": "avatar_motivator",
        "posting_times": ["07:00", "12:00", "19:00"],
        "hashtags": ["#motivasi", "#sukses", "#semangat", "#inspirasi"],
        "accounts": {
            "tiktok": "@motivator_id",
            "instagram": "@motivator_id",
        }
    },
    "tech_bro_en": {
        "name": "Tech Bro",
        "language": "en",
        "niche": "tech",
        "style": {
            "tone": "confident, direct, educational",
            "emoji_usage": "minimal",
            "slang_level": "tech jargon",
            "signature": "🚀"
        },
        "character": "avatar_tech",
        "posting_times": ["09:00", "15:00", "21:00"],
        "hashtags": ["#tech", "#ai", "#coding", "#startup"],
        "accounts": {
            "tiktok": "@techbro_ai",
            "twitter": "@techbro_ai",
        }
    },
    "beauty_id": {
        "name": "Beauty Queen ID",
        "language": "id",
        "niche": "beauty",
        "style": {
            "tone": "friendly, girly, enthusiastic",
            "emoji_usage": "heavy",
            "slang_level": "Gen-Z Indonesian",
            "signature": "✨💖"
        },
        "character": "avatar_beauty",
        "posting_times": ["10:00", "14:00", "20:00"],
        "hashtags": ["#skincare", "#makeup", "#cantik", "#glowup"],
        "accounts": {
            "tiktok": "@beautyqueen_id",
            "instagram": "@beautyqueen_id",
        }
    }
}


def list_personas():
    """List all available personas."""
    personas = []
    for f in PERSONAS_DIR.glob("*.json"):
        with open(f) as file:
            data = json.load(file)
            personas.append({
                "id": f.stem,
                "name": data.get("name"),
                "niche": data.get("niche"),
                "language": data.get("language")
            })
    return personas


def get_persona(persona_id: str) -> dict:
    """Get persona by ID."""
    path = PERSONAS_DIR / f"{persona_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def create_persona(persona_id: str, config: dict):
    """Create or update a persona."""
    config["id"] = persona_id
    config["created_at"] = datetime.now().isoformat()
    
    path = PERSONAS_DIR / f"{persona_id}.json"
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    return path


def generate_content_variant(content: str, persona_id: str) -> str:
    """Transform content to match persona's voice."""
    persona = get_persona(persona_id)
    if not persona:
        return content
    
    style = persona.get("style", {})
    
    # Add signature
    signature = style.get("signature", "")
    if signature:
        content = f"{content} {signature}"
    
    # Add hashtags
    hashtags = persona.get("hashtags", [])
    if hashtags:
        content = f"{content}\n\n{' '.join(hashtags[:5])}"
    
    return content


def init_default_personas():
    """Initialize default personas."""
    for pid, config in DEFAULT_PERSONAS.items():
        create_persona(pid, config)
    print(f"✅ Initialized {len(DEFAULT_PERSONAS)} default personas")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Persona Manager")
    parser.add_argument("--list", action="store_true", help="List all personas")
    parser.add_argument("--get", type=str, help="Get persona by ID")
    parser.add_argument("--create", type=str, help="Create persona with ID")
    parser.add_argument("--niche", type=str, help="Niche for new persona")
    parser.add_argument("--language", type=str, default="id", help="Language")
    parser.add_argument("--init", action="store_true", help="Initialize defaults")
    
    args = parser.parse_args()
    
    if args.init:
        init_default_personas()
    elif args.list:
        personas = list_personas()
        if not personas:
            print("No personas found. Run --init to create defaults.")
        for p in personas:
            print(f"  {p['id']}: {p['name']} ({p['niche']}, {p['language']})")
    elif args.get:
        persona = get_persona(args.get)
        if persona:
            print(json.dumps(persona, indent=2))
        else:
            print(f"Persona '{args.get}' not found")
    elif args.create:
        config = {
            "name": args.create,
            "niche": args.niche or "general",
            "language": args.language,
            "style": {
                "tone": "neutral",
                "emoji_usage": "moderate",
                "slang_level": "standard"
            }
        }
        path = create_persona(args.create, config)
        print(f"✅ Created persona: {path}")


if __name__ == "__main__":
    main()
