#!/usr/bin/env python3
"""
YouTube Shorts Pipeline for Viral Content Creator

Generates viral short-form video scripts with hooks, captions, hashtags,
and B-roll suggestions. PostBridge-ready output.

Usage:
    python youtube_shorts_pipeline.py --topic "cara dapat uang dari TikTok"
    python youtube_shorts_pipeline.py --topic "tips trading emas" --hook "Stop! Jangan trading sebelum tau ini"
    python youtube_shorts_pipeline.py --topic "skincare routine" --style ugc --lang id
"""

import argparse
import json
import os
import sys
from datetime import datetime

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"
POSTBRIDGE_API_KEY = os.environ.get("POSTBRIDGE_API_KEY", "REDACTED_POSTBRIDGE_KEY")


def get_llm_client():
    """Get OpenAI-compatible client via OmniRoute."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai not installed. Run: pip install openai")
        sys.exit(1)
    return OpenAI(base_url=OMNIROUTE_BASE, api_key=OMNIROUTE_KEY)


def llm_chat(client, system_prompt, user_prompt, temperature=0.7):
    """Send chat completion via OmniRoute."""
    try:
        resp = client.chat.completions.create(
            model=OMNIROUTE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[LLM Error: {e}]"


def generate_script(client, topic, hook=None, style="professional", lang="id"):
    """Generate viral YouTube Shorts script."""
    lang_context = "Indonesian (Bahasa Indonesia, casual Jakarta style)" if lang == "id" else "English"

    system = f"""You are a viral YouTube Shorts scriptwriter. Write in {lang_context}.
Output ONLY valid JSON with these fields:
- hook: string (attention-grabbing first line, max 10 words)
- body: string (main content, 3-5 punchy sentences, max 45 seconds when read aloud)
- cta: string (call to action, 1 sentence)
- duration_estimate: string (estimated duration like "30-45s")

Style: {style} (ugc = casual/authentic, professional = polished/authoritative)
The hook MUST stop the scroll. Use curiosity gaps, shocking stats, or direct challenges."""

    user_hook = f'\nUse this hook as starting point: "{hook}"' if hook else ""
    prompt = f"Create a viral YouTube Shorts script about: {topic}{user_hook}"

    raw = llm_chat(client, system, prompt)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return {"hook": hook or topic, "body": raw, "cta": "Follow untuk tips lainnya!", "duration_estimate": "30-45s"}


def generate_caption(client, topic, script, lang="id"):
    """Generate optimized caption with hashtags (Indonesia TikTok style)."""
    lang_context = "Indonesian TikTok/YouTube Shorts style" if lang == "id" else "English social media style"

    system = f"""You are a social media caption specialist for {lang_context}.
Output ONLY valid JSON with:
- caption: string (engaging caption, 2-3 lines max, with emojis)
- hashtags: array of strings (10-15 relevant hashtags, mix trending + niche)
- first_comment: string (engagement-boosting first comment to post)

Hashtag strategy: 5 broad/trending + 5 niche/specific + 3-5 long-tail.
Caption must create curiosity to watch the full video."""

    prompt = f"""Topic: {topic}
Script hook: {script.get('hook', '')}
Script body: {script.get('body', '')}

Generate caption and hashtags."""

    raw = llm_chat(client, system, prompt)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return {"caption": topic, "hashtags": [f"#{topic.replace(' ', '')}"], "first_comment": ""}


def generate_broll_keywords(client, topic, script):
    """Generate B-roll keyword suggestions for stock footage / AI generation."""
    system = """You are a video editor. Suggest B-roll visuals for a YouTube Shorts video.
Output ONLY a JSON array of objects with:
- keyword: string (search term for stock footage)
- timing: string (when in the video, e.g. "0:00-0:05")
- description: string (brief description of the visual)

Suggest 4-6 B-roll segments that match the script flow."""

    prompt = f"Topic: {topic}\nScript: {json.dumps(script)}"
    raw = llm_chat(client, system, prompt, temperature=0.5)
    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return [{"keyword": topic, "timing": "0:00-0:30", "description": "General footage"}]


def build_postbridge_payload(script, caption_data, topic):
    """Build PostBridge-ready payload for scheduling."""
    return {
        "platform": "youtube_shorts",
        "content": {
            "title": script.get("hook", topic)[:100],
            "description": caption_data.get("caption", ""),
            "hashtags": caption_data.get("hashtags", []),
            "script": script,
        },
        "scheduling": {
            "optimal_times": ["07:30", "12:00", "18:00", "20:30"],
            "timezone": "Asia/Jakarta",
        },
        "metadata": {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "api_key_ref": "POSTBRIDGE_API_KEY",
        },
    }


def run_pipeline(topic, hook=None, style="professional", lang="id"):
    """Run the full YouTube Shorts pipeline."""
    print(f"[YouTube Shorts Pipeline] Starting...")
    print(f"  Topic: {topic}")
    if hook:
        print(f"  Hook: {hook}")
    print()

    client = get_llm_client()

    # Step 1: Generate script
    print("[1/3] Generating viral script...")
    script = generate_script(client, topic, hook, style, lang)
    print(f"  Hook: {script.get('hook', 'N/A')}")
    print(f"  Duration: {script.get('duration_estimate', 'N/A')}")

    # Step 2: Generate caption + hashtags
    print("[2/3] Generating caption & hashtags...")
    caption_data = generate_caption(client, topic, script, lang)
    print(f"  Hashtags: {len(caption_data.get('hashtags', []))}")

    # Step 3: Generate B-roll keywords
    print("[3/3] Generating B-roll suggestions...")
    broll = generate_broll_keywords(client, topic, script)
    print(f"  B-roll segments: {len(broll)}")

    # Build PostBridge payload
    postbridge_payload = build_postbridge_payload(script, caption_data, topic)

    result = {
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "script": script,
        "caption": caption_data.get("caption", ""),
        "hashtags": caption_data.get("hashtags", []),
        "first_comment": caption_data.get("first_comment", ""),
        "b_roll_keywords": broll,
        "postbridge_ready": postbridge_payload,
    }

    print()
    print("=" * 60)
    print(f"HOOK: {script.get('hook', '')}")
    print(f"BODY: {script.get('body', '')}")
    print(f"CTA: {script.get('cta', '')}")
    print(f"CAPTION: {caption_data.get('caption', '')}")
    print(f"HASHTAGS: {' '.join(caption_data.get('hashtags', []))}")
    print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts Pipeline")
    parser.add_argument("--topic", "-t", required=True, help="Video topic")
    parser.add_argument("--hook", help="Optional custom hook line")
    parser.add_argument("--style", choices=["ugc", "professional"], default="professional")
    parser.add_argument("--lang", choices=["id", "en"], default="id")
    parser.add_argument("--output", "-o", help="Output JSON file path")

    args = parser.parse_args()
    result = run_pipeline(args.topic, args.hook, args.style, args.lang)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nSaved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
