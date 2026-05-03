#!/usr/bin/env python3
"""
Content Suite - Master Pipeline

Complete workflow from research to engagement:
1. Research viral content
2. Plan content calendar
3. Generate scripts
4. Create storyboard
5. Generate consistent characters
6. Produce video (GeminiGen + Remotion)
7. Publish to platforms
8. Activate buzzer engagement
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_manager import get_persona, list_personas, generate_content_variant
from buzzer import create_buzz_plan, execute_buzz, log_buzz_activity
from character import get_character, generate_character_image, list_characters

SUITE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = SUITE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def step_research(niche: str, platform: str = "tiktok") -> dict:
    """Step 1: Research viral content in niche."""
    print("\n📊 STEP 1: VIRAL RESEARCH")
    print(f"  Niche: {niche}")
    print(f"  Platform: {platform}")
    
    # TODO: Integrate with kalodata
    # For now, return sample trends
    trends = {
        "niche": niche,
        "platform": platform,
        "trending_topics": [
            "morning routine for success",
            "mindset shift that changed my life",
            "secret habits of winners"
        ],
        "top_hooks": [
            "No one tells you this about...",
            "I was broke until I learned...",
            "Stop doing X, start doing Y"
        ],
        "optimal_times": ["07:00", "12:00", "19:00"],
        "hashtags": ["#motivation", "#sukses", "#mindset"]
    }
    
    print(f"  ✅ Found {len(trends['trending_topics'])} trending topics")
    return trends


def step_plan(research: dict, days: int = 7, posts_per_day: int = 3) -> list:
    """Step 2: Create content calendar."""
    print("\n📅 STEP 2: CONTENT PLANNING")
    print(f"  Days: {days}")
    print(f"  Posts/day: {posts_per_day}")
    
    calendar = []
    start_date = datetime.now()
    
    for day in range(days):
        date = start_date + timedelta(days=day)
        for i, time in enumerate(research["optimal_times"][:posts_per_day]):
            topic = research["trending_topics"][i % len(research["trending_topics"])]
            hook = research["top_hooks"][i % len(research["top_hooks"])]
            
            calendar.append({
                "date": date.strftime("%Y-%m-%d"),
                "time": time,
                "topic": topic,
                "hook_template": hook,
                "status": "planned"
            })
    
    print(f"  ✅ Planned {len(calendar)} posts")
    return calendar


def step_script(calendar_entry: dict, persona_id: str) -> dict:
    """Step 3: Generate script for a calendar entry."""
    print("\n📝 STEP 3: SCRIPT WRITING")
    
    persona = get_persona(persona_id)
    topic = calendar_entry["topic"]
    hook = calendar_entry["hook_template"]
    
    # Generate script (simplified - would use LLM in production)
    script = {
        "hook": f"{hook} {topic}",
        "body": f"Here's what I learned about {topic}...",
        "cta": "Follow for more!",
        "full_text": f"{hook} {topic}\n\nHere's what I learned...\n\nFollow for more!"
    }
    
    # Apply persona voice
    if persona:
        script["full_text"] = generate_content_variant(script["full_text"], persona_id)
        script["hashtags"] = persona.get("hashtags", [])
    
    print(f"  Hook: {script['hook'][:50]}...")
    print(f"  ✅ Script generated")
    return script


def step_storyboard(script: dict, scenes: int = 3) -> list:
    """Step 4: Create storyboard from script."""
    print("\n🎬 STEP 4: STORYBOARD")
    
    # Split script into scenes
    storyboard = []
    duration_per_scene = 60 // scenes  # For 60s video
    
    parts = [script["hook"], script["body"], script["cta"]]
    for i, part in enumerate(parts[:scenes]):
        storyboard.append({
            "scene": i + 1,
            "duration": duration_per_scene,
            "text": part,
            "visual": f"Scene {i+1} visual",
            "transition": "crossfade" if i > 0 else "none"
        })
    
    print(f"  ✅ Created {len(storyboard)} scenes")
    return storyboard


def step_character(character_id: str, scenes: list = None) -> dict:
    """Step 5: Ensure character consistency."""
    print("\n🎭 STEP 5: CHARACTER CONSISTENCY")
    
    char = get_character(character_id)
    if not char:
        print(f"  ⚠️ Character {character_id} not found, using default")
        character_id = "avatar_motivator"
        char = get_character(character_id)
    
    char_dir = SUITE_DIR / "characters" / character_id
    base_img = char_dir / "base.png"
    
    # Generate base if not exists
    if not base_img.exists():
        print(f"  Generating base image...")
        try:
            generate_character_image(character_id)
        except Exception as e:
            print(f"  ⚠️ Could not generate: {e}")
    
    print(f"  ✅ Character: {char.get('name', character_id)}")
    return {
        "character_id": character_id,
        "base_image": str(base_img) if base_img.exists() else None,
        "style": char.get("style", "")
    }


def step_produce(storyboard: list, character: dict, output_name: str) -> Path:
    """Step 6: Produce video with Remotion."""
    print("\n🎥 STEP 6: VIDEO PRODUCTION")
    
    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    
    # This would integrate with the full video pipeline
    # For now, show what would happen
    print(f"  Storyboard: {len(storyboard)} scenes")
    print(f"  Character: {character['character_id']}")
    print(f"  Output: {output_path}")
    
    # TODO: Call multi_stage_i2v.py or remotion render
    print(f"  ⚠️ Video production requires full pipeline integration")
    
    return output_path


def step_publish(video_path: Path, persona_id: str, platforms: list = None) -> dict:
    """Step 7: Publish to platforms via PostBridge."""
    print("\n📤 STEP 7: PUBLISHING")
    
    persona = get_persona(persona_id)
    platforms = platforms or ["tiktok"]
    
    # Get persona accounts
    accounts = persona.get("accounts", {}) if persona else {}
    
    results = {}
    for platform in platforms:
        account = accounts.get(platform, "default")
        print(f"  {platform}: {account}")
        # TODO: Integrate with PostBridge
        results[platform] = {"status": "pending", "account": account}
    
    print(f"  ✅ Scheduled for {len(platforms)} platforms")
    return results


def step_engage(post_urls: list, accounts: int = 3) -> dict:
    """Step 8: Activate buzzer engagement."""
    print("\n💬 STEP 8: BUZZER ENGAGEMENT")
    
    all_plans = []
    for url in post_urls:
        plan = create_buzz_plan(url, accounts)
        all_plans.extend(plan)
    
    print(f"  Created {len(all_plans)} engagement actions")
    print(f"  ⚠️ Dry run - use --execute to activate")
    
    return {"plans": all_plans, "status": "pending"}


def run_full_pipeline(niche: str, persona_id: str, character_id: str, days: int = 1):
    """Run the complete pipeline."""
    print("=" * 60)
    print("🚀 CONTENT SUITE - FULL PIPELINE")
    print("=" * 60)
    print(f"Niche: {niche}")
    print(f"Persona: {persona_id}")
    print(f"Character: {character_id}")
    print(f"Days: {days}")
    
    # Step 1: Research
    research = step_research(niche)
    
    # Step 2: Plan
    calendar = step_plan(research, days=days, posts_per_day=1)
    
    # Process first entry as demo
    entry = calendar[0]
    
    # Step 3: Script
    script = step_script(entry, persona_id)
    
    # Step 4: Storyboard
    storyboard = step_storyboard(script)
    
    # Step 5: Character
    character = step_character(character_id)
    
    # Step 6: Produce
    output_name = f"{niche}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    video_path = step_produce(storyboard, character, output_name)
    
    # Step 7: Publish (demo)
    publish_result = step_publish(video_path, persona_id)
    
    # Step 8: Engage (demo)
    engage_result = step_engage(["https://example.com/post1"])
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)
    
    # Summary
    summary = {
        "niche": niche,
        "persona": persona_id,
        "character": character_id,
        "calendar_entries": len(calendar),
        "script": script,
        "storyboard_scenes": len(storyboard),
        "video_path": str(video_path),
        "publish_status": publish_result,
        "engagement_status": engage_result
    }
    
    # Save summary
    summary_path = OUTPUT_DIR / f"{output_name}_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n📋 Summary saved: {summary_path}")
    
    return summary


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Content Suite Pipeline")
    parser.add_argument("--niche", type=str, default="motivation", help="Content niche")
    parser.add_argument("--persona", type=str, default="motivator_id", help="Persona ID")
    parser.add_argument("--character", type=str, default="avatar_motivator", help="Character ID")
    parser.add_argument("--days", type=int, default=1, help="Days to plan")
    parser.add_argument("--step", type=str, help="Run specific step only")
    
    args = parser.parse_args()
    
    if args.step:
        # Run specific step
        if args.step == "research":
            step_research(args.niche)
        elif args.step == "characters":
            print("🎭 Initializing characters...")
            from character import init_characters
            init_characters()
        else:
            print(f"Unknown step: {args.step}")
    else:
        # Run full pipeline
        run_full_pipeline(
            niche=args.niche,
            persona_id=args.persona,
            character_id=args.character,
            days=args.days
        )


if __name__ == "__main__":
    main()
