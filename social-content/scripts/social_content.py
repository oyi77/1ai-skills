#!/usr/bin/env python3
"""Social content generator — produces platform-optimized posts via OmniRoute LLM."""

import argparse
import json
import sys

from openai import OpenAI

PLATFORM_CONSTRAINTS = {
    "twitter": (
        "Twitter/X post. MUST be 280 characters or fewer. "
        "Be punchy, use line breaks for emphasis, end with a strong CTA."
    ),
    "tiktok": (
        "TikTok caption. Lead with a scroll-stopping hook in the first line. "
        "Use casual, energetic language. Add relevant emoji sparingly. Keep it under 150 words."
    ),
    "instagram": (
        "Instagram caption. Open with a compelling first line (visible before 'more'). "
        "Write in short paragraphs. Emphasize visual storytelling cues. Keep it under 2200 characters."
    ),
    "linkedin": (
        "LinkedIn post. Professional yet personable tone. "
        "Use data points or insights to add authority. Structure with line breaks for readability. "
        "Keep it under 3000 characters."
    ),
}

TONE_INSTRUCTIONS = {
    "casual": "Write in a relaxed, conversational style as if talking to a friend.",
    "professional": "Write in a polished, authoritative style suitable for industry professionals.",
    "viral": "Write to maximize shares and engagement — use curiosity gaps, bold claims, and emotional hooks.",
}

BEST_TIMES = {
    "twitter": "12-1 PM or 5-6 PM",
    "tiktok": "6-9 PM",
    "instagram": "11 AM-1 PM or 7-9 PM",
    "linkedin": "7-8 AM or 5-6 PM",
}


def generate_content(topic: str, platform: str, tone: str) -> dict:
    """Call OmniRoute LLM and return structured social content."""
    client = OpenAI(base_url="http://localhost:20128/v1", api_key="omniroute")

    system_prompt = (
        "You are an expert social-media content strategist.\n"
        f"Platform: {PLATFORM_CONSTRAINTS[platform]}\n"
        f"Tone: {TONE_INSTRUCTIONS[tone]}\n\n"
        "Return ONLY valid JSON with these keys:\n"
        '  "caption": the post text,\n'
        '  "hashtags": list of 3-7 relevant hashtags (each prefixed with #),\n'
        '  "cta": a short call-to-action phrase.\n'
        "Do NOT wrap the JSON in markdown code fences."
    )

    user_prompt = f"Create a {platform} post about: {topic}"

    response = client.chat.completions.create(
        model="auto",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if the model added them anyway
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0].strip()

    llm_data = json.loads(raw)

    return {
        "caption": llm_data.get("caption", ""),
        "hashtags": llm_data.get("hashtags", []),
        "cta": llm_data.get("cta", "Link in bio!"),
        "best_time_to_post": BEST_TIMES[platform],
        "postbridge_payload": {
            "content": llm_data.get("caption", ""),
            "platform": platform,
            "scheduled": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Generate platform-optimized social content.")
    parser.add_argument("--topic", required=True, help="Content topic or idea")
    parser.add_argument(
        "--platform",
        required=True,
        choices=["tiktok", "instagram", "twitter", "linkedin"],
        help="Target social platform",
    )
    parser.add_argument(
        "--tone",
        required=True,
        choices=["casual", "professional", "viral"],
        help="Content tone",
    )
    args = parser.parse_args()

    try:
        result = generate_content(args.topic, args.platform, args.tone)
    except json.JSONDecodeError as exc:
        print(f"Error: LLM returned invalid JSON — {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
