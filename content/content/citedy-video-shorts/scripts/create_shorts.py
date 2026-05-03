#!/usr/bin/env python3
"""
Citedy Video Shorts — Generate short-form video scripts with visual scene suggestions.

Input: topic + duration → script optimized for short-form, visual scene suggestions,
and PostBridge-ready payload.

Usage:
    python create_shorts.py --topic "5 productivity hacks" --duration 30
    python create_shorts.py --topic "Why Bitcoin matters" --duration 60 --style educational
    python create_shorts.py --topic "..." --output json
"""

import argparse
import json
import math
import os
import subprocess
import sys
from datetime import datetime

DURATION_CONFIGS = {
    15: {"scenes": 3, "words_per_scene": 12, "hook_seconds": 2, "cta_seconds": 3},
    30: {"scenes": 5, "words_per_scene": 20, "hook_seconds": 3, "cta_seconds": 4},
    60: {"scenes": 8, "words_per_scene": 25, "hook_seconds": 3, "cta_seconds": 5},
}

STYLE_PROMPTS = {
    "educational": "Create an informative, clear short video script. Use simple language, "
                   "present one key insight per scene. End with a takeaway.",
    "entertaining": "Create a fun, engaging short video script. Use humor, surprise, "
                    "or storytelling. Hook the viewer in the first 2 seconds.",
    "promotional": "Create a compelling product/brand short video script. Lead with the "
                   "problem, show the solution, end with a clear call-to-action.",
    "storytelling": "Create a narrative-driven short video script. Use tension, "
                    "character, and resolution. Make the viewer feel something.",
}


def call_omniroute(prompt, system_prompt=None):
    """Call OmniRoute for LLM generation."""
    omniroute = os.path.expanduser("~/.openclaw/workspace/scripts/omniroute")
    if not os.path.exists(omniroute):
        omniroute = "omniroute"

    cmd = [omniroute, "--prompt", prompt]
    if system_prompt:
        cmd.extend(["--system", system_prompt])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def generate_script_template(topic, duration, style, use_llm=True):
    """Generate a short-form video script."""
    config = DURATION_CONFIGS.get(duration, DURATION_CONFIGS[30])
    num_scenes = config["scenes"]
    style_prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["educational"])

    # Try LLM generation first
    if use_llm:
        llm_prompt = (
            f"Create a {duration}-second short-form video script about: {topic}\n\n"
            f"Requirements:\n"
            f"- Exactly {num_scenes} scenes\n"
            f"- First scene is a hook ({config['hook_seconds']}s)\n"
            f"- Last scene is CTA ({config['cta_seconds']}s)\n"
            f"- Each scene needs: narration text, visual description, duration\n"
            f"- Keep narration to ~{config['words_per_scene']} words per scene\n"
            f"- Style: {style}\n\n"
            f"Output as JSON with this structure:\n"
            f'{{"title": "...", "scenes": [{{"id": 1, "duration_sec": N, '
            f'"narration": "...", "visual": "...", "text_overlay": "..."}}]}}'
        )

        llm_result = call_omniroute(llm_prompt, style_prompt)
        if llm_result:
            try:
                # Try to extract JSON from response
                start = llm_result.find("{")
                end = llm_result.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(llm_result[start:end])
            except (json.JSONDecodeError, ValueError):
                pass

    # Fallback: generate template structure
    scene_duration = duration / num_scenes
    scenes = []

    for i in range(num_scenes):
        scene = {"id": i + 1, "duration_sec": round(scene_duration)}

        if i == 0:
            scene["duration_sec"] = config["hook_seconds"]
            scene["narration"] = f"[HOOK about {topic} — grab attention immediately]"
            scene["visual"] = "[Bold text overlay or surprising visual]"
            scene["text_overlay"] = f"[Eye-catching title about {topic}]"
        elif i == num_scenes - 1:
            scene["duration_sec"] = config["cta_seconds"]
            scene["narration"] = "[Call to action — follow, like, share, or link]"
            scene["visual"] = "[Logo/branding + CTA text]"
            scene["text_overlay"] = "[Follow for more / Link in bio]"
        else:
            scene["narration"] = f"[Key point {i} about {topic}]"
            scene["visual"] = f"[Visual illustrating point {i}]"
            scene["text_overlay"] = f"[Supporting text for point {i}]"

        scenes.append(scene)

    return {
        "title": f"Short: {topic}",
        "duration_sec": duration,
        "style": style,
        "scenes": scenes,
        "note": "Template generated — fill in bracketed placeholders or re-run with OmniRoute"
    }


def to_postbridge_payload(script_data, topic):
    """Convert script to PostBridge-ready payload."""
    return {
        "type": "video_short",
        "platform": ["tiktok", "instagram_reels", "youtube_shorts"],
        "content": {
            "title": script_data.get("title", topic),
            "description": f"Short-form video about {topic}",
            "duration_sec": script_data.get("duration_sec", 30),
            "scenes": script_data.get("scenes", []),
            "hashtags": [],
            "style": script_data.get("style", "educational")
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "generator": "citedy-video-shorts",
            "status": "draft"
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Generate short-form video scripts")
    parser.add_argument("--topic", required=True, help="Video topic")
    parser.add_argument("--duration", type=int, choices=[15, 30, 60], default=30,
                        help="Duration in seconds (default: 30)")
    parser.add_argument("--style", choices=list(STYLE_PROMPTS.keys()),
                        default="educational", help="Script style")
    parser.add_argument("--output", choices=["json", "markdown", "postbridge"],
                        default="markdown", help="Output format")
    parser.add_argument("--no-llm", action="store_true",
                        help="Skip LLM, output template only")
    args = parser.parse_args()

    script = generate_script_template(args.topic, args.duration, args.style,
                                       use_llm=not args.no_llm)

    if args.output == "json":
        print(json.dumps(script, ensure_ascii=False, indent=2))
    elif args.output == "postbridge":
        payload = to_postbridge_payload(script, args.topic)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        # Markdown output
        print(f"# {script.get('title', args.topic)}\n")
        print(f"**Duration**: {args.duration}s | **Style**: {args.style}\n")

        for scene in script.get("scenes", []):
            print(f"### Scene {scene['id']} ({scene.get('duration_sec', '?')}s)")
            print(f"- **Narration**: {scene.get('narration', 'N/A')}")
            print(f"- **Visual**: {scene.get('visual', 'N/A')}")
            print(f"- **Text Overlay**: {scene.get('text_overlay', 'N/A')}")
            print()

        if script.get("note"):
            print(f"---\n*{script['note']}*")


if __name__ == "__main__":
    main()
