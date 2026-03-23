#!/usr/bin/env python3
"""Content Factory - multi-agent content pipeline: Research → Write → Thumbnail."""
import json, sys, os
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import quote_plus

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"
POSTBRIDGE_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"

CONTENT_TYPES = {
    "tiktok_caption": "TikTok caption (max 300 chars, hook + value + CTA, include hashtags)",
    "instagram_caption": "Instagram caption (engaging, with line breaks, 5-10 hashtags)",
    "twitter_thread": "Twitter thread (5-7 tweets, numbered, each under 280 chars)",
    "article": "Blog article (800-1200 words, SEO-friendly, with subheadings)",
    "script": "Video script (60-90 seconds, hook/body/CTA structure)",
}


def _llm_call(system_prompt, user_prompt):
    """Call OmniRoute LLM."""
    payload = json.dumps({
        "model": OMNIROUTE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.8,
        "max_tokens": 1500,
    }).encode()

    req = Request(
        f"{OMNIROUTE_BASE}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OMNIROUTE_KEY}",
            "Content-Type": "application/json",
        },
    )
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]


def research_agent(niche):
    """Research trending topics in a niche using DuckDuckGo."""
    try:
        query = quote_plus(f"{niche} trending 2026")
        url = f"https://html.duckduckgo.com/html/?q={query}"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        # Extract result titles
        import re
        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html)
        titles = [re.sub(r"<[^>]+>", "", t).strip() for t in titles[:10]]
        return titles if titles else [f"Trending in {niche}"]
    except Exception as e:
        return [f"Research fallback: trending topics in {niche} (error: {e})"]


def writing_agent(topic, content_type="tiktok_caption"):
    """Generate content using OmniRoute LLM."""
    type_desc = CONTENT_TYPES.get(content_type, CONTENT_TYPES["tiktok_caption"])
    system = f"You are a viral content creator. Create a {type_desc}. Write in the same language as the topic. Be engaging, authentic, and value-driven."
    return _llm_call(system, f"Create content about: {topic}")


def thumbnail_agent(content):
    """Generate an image prompt for thumbnail/cover art."""
    system = "You are a visual designer. Generate a detailed AI image prompt for a social media thumbnail or cover image. The prompt should be specific, vivid, and optimized for Midjourney/DALL-E. Output ONLY the prompt, nothing else."
    return _llm_call(system, f"Create a thumbnail prompt for this content:\n{content[:500]}")


def build_postbridge_payload(topic, content, content_type):
    """Build a PostBridge-compatible payload."""
    return {
        "title": topic,
        "body": content,
        "content_type": content_type,
        "created_at": datetime.now().isoformat(),
        "source": "content-factory",
    }


def orchestrate(niche, content_type="tiktok_caption"):
    """Full pipeline: research → write → thumbnail."""
    print(f"[Research] Searching trends in '{niche}'...")
    topics = research_agent(niche)
    topic = topics[0] if topics else niche
    print(f"[Research] Top topic: {topic}")

    print(f"[Writing] Generating {content_type}...")
    content = writing_agent(topic, content_type)
    print(f"[Writing] Done ({len(content)} chars)")

    print(f"[Thumbnail] Generating image prompt...")
    thumb_prompt = thumbnail_agent(content)
    print(f"[Thumbnail] Done")

    # Extract hashtags from content
    import re
    hashtags = re.findall(r"#\w+", content)

    result = {
        "topic": topic,
        "content": content,
        "thumbnail_prompt": thumb_prompt,
        "hashtags": hashtags,
        "content_type": content_type,
        "research_topics": topics[:5],
        "postbridge_payload": build_postbridge_payload(topic, content, content_type),
        "generated_at": datetime.now().isoformat(),
    }

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Content Factory Pipeline")
    parser.add_argument("--niche", required=True, help="Content niche (e.g., 'trading emas')")
    parser.add_argument(
        "--type",
        default="tiktok_caption",
        choices=list(CONTENT_TYPES.keys()),
        help="Content type to generate",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    result = orchestrate(args.niche, args.type)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"Topic: {result['topic']}")
        print(f"Type: {result['content_type']}")
        print(f"{'='*60}")
        print(f"\n📝 Content:\n{result['content']}")
        print(f"\n🎨 Thumbnail Prompt:\n{result['thumbnail_prompt']}")
        print(f"\n# Hashtags: {' '.join(result['hashtags'])}")
        print(f"\n📊 Research topics: {', '.join(result['research_topics'])}")
