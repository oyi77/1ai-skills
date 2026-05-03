#!/usr/bin/env python3
"""
YouTube Content Pipeline for Viral Content Creator

Full YouTube content pipeline: idea scouting, topic research,
script generation, and performance tracking.

Usage:
    python youtube_pipeline.py --niche "trading tips"
    python youtube_pipeline.py --idea "cara profit trading emas" --generate-script
    python youtube_pipeline.py --track --video-id "abc123"
"""

import argparse
import json
import os
import sys
from datetime import datetime

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"


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


def parse_json_response(raw, container="{"):
    """Extract JSON from LLM response."""
    try:
        if container == "{":
            start, end = raw.find("{"), raw.rfind("}") + 1
        else:
            start, end = raw.find("["), raw.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def web_search(query, max_results=10):
    """Search web via duckduckgo-search."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except ImportError:
        print("WARNING: duckduckgo-search not installed. Run: pip install duckduckgo-search")
        return []
    except Exception as e:
        print(f"WARNING: Search failed: {e}")
        return []


def idea_scout(niche, count=10):
    """Scout trending video ideas for a niche.

    Searches trending topics on DuckDuckGo, then uses LLM to
    generate YouTube video ideas based on what's trending.
    """
    print(f"[Idea Scout] Scouting ideas for niche: {niche}")

    # Search for trending topics
    search_results = web_search(f"{niche} trending 2026 YouTube video ideas", max_results=15)

    trending_context = "\n".join(
        f"- {r.get('title', '')}: {r.get('body', '')[:100]}"
        for r in search_results[:10]
    ) if search_results else "No search results available."

    client = get_llm_client()
    system = """You are a YouTube content strategist. Generate video ideas based on trending topics.
Output ONLY valid JSON array of objects with:
- title: string (compelling video title)
- hook: string (first 5 seconds hook)
- why_trending: string (why this topic is hot now)
- difficulty: string (easy/medium/hard)
- estimated_views: string (view potential estimate)
- keywords: array of strings (5-8 SEO keywords)"""

    prompt = f"""Niche: {niche}
Trending context:
{trending_context}

Generate {count} YouTube video ideas that would perform well right now."""

    raw = llm_chat(client, system, prompt)
    ideas = parse_json_response(raw, "[")
    if not ideas:
        ideas = [{"title": f"{niche} video idea", "hook": "Check this out", "why_trending": "trending topic", "difficulty": "medium", "estimated_views": "10K+", "keywords": [niche]}]

    print(f"  Found {len(ideas)} ideas")
    return ideas


def research_topic(idea):
    """Deep-research a specific video idea.

    Gathers supporting data, stats, competitor analysis, and
    talking points for the video topic.
    """
    topic = idea if isinstance(idea, str) else idea.get("title", str(idea))
    print(f"[Research] Researching: {topic}")

    # Search for supporting content
    search_results = web_search(f"{topic} guide tutorial tips", max_results=10)
    competitor_results = web_search(f"{topic} YouTube", max_results=5)

    sources = "\n".join(
        f"- {r.get('title', '')}: {r.get('body', '')[:150]}"
        for r in search_results[:8]
    ) if search_results else "No sources found."

    competitors = "\n".join(
        f"- {r.get('title', '')}: {r.get('href', '')}"
        for r in competitor_results[:5]
    ) if competitor_results else "No competitor videos found."

    client = get_llm_client()
    system = """You are a YouTube content researcher. Analyze a topic and provide comprehensive research.
Output ONLY valid JSON with:
- summary: string (topic overview, 2-3 sentences)
- key_points: array of strings (5-7 main talking points)
- stats: array of strings (3-5 relevant statistics or data points)
- competitor_gaps: array of strings (what existing videos miss)
- unique_angle: string (suggested unique perspective)
- target_audience: string (who this video is for)
- content_length: string (recommended video length)"""

    prompt = f"""Topic: {topic}

Source material:
{sources}

Competitor videos:
{competitors}

Provide deep research for creating a YouTube video on this topic."""

    raw = llm_chat(client, system, prompt)
    research = parse_json_response(raw)
    if not research:
        research = {"summary": topic, "key_points": [], "stats": [], "competitor_gaps": [], "unique_angle": "", "target_audience": "general", "content_length": "8-12 minutes"}

    print(f"  Key points: {len(research.get('key_points', []))}")
    return research


def generate_script(topic, research=None, lang="id"):
    """Generate a full YouTube video script.

    Creates intro, body sections, and outro with hooks,
    transitions, and calls to action.
    """
    topic_str = topic if isinstance(topic, str) else topic.get("title", str(topic))
    print(f"[Script] Generating script for: {topic_str}")

    lang_context = "Indonesian (Bahasa Indonesia, casual YouTube style)" if lang == "id" else "English"
    research_context = json.dumps(research, ensure_ascii=False) if research else "No research provided."

    client = get_llm_client()
    system = f"""You are a professional YouTube scriptwriter. Write in {lang_context}.
Output ONLY valid JSON with:
- title: string (SEO-optimized video title)
- hook: string (first 5-10 seconds, must stop the scroll)
- intro: string (30-60 second intro after hook)
- sections: array of objects with "heading" and "content" (3-5 main sections)
- outro: string (call to action + closing)
- thumbnail_text: string (2-4 words for thumbnail)
- description: string (YouTube description with keywords)
- tags: array of strings (15-20 YouTube tags)
- estimated_duration: string (video duration estimate)"""

    prompt = f"""Topic: {topic_str}

Research:
{research_context}

Write a complete YouTube video script that maximizes watch time and engagement."""

    raw = llm_chat(client, system, prompt, temperature=0.8)
    script = parse_json_response(raw)
    if not script:
        script = {"title": topic_str, "hook": "", "intro": "", "sections": [], "outro": "", "thumbnail_text": "", "description": "", "tags": [], "estimated_duration": "8-12 min"}

    print(f"  Title: {script.get('title', 'N/A')}")
    print(f"  Sections: {len(script.get('sections', []))}")
    return script


def track_performance(video_id=None):
    """Track video performance metrics.

    Placeholder for YouTube Analytics API integration.
    Returns mock structure for now — connect to YouTube Data API
    when API key is available.
    """
    print(f"[Track] Performance tracking for: {video_id or 'all videos'}")
    print("  NOTE: Connect YouTube Data API for live metrics.")
    return {
        "video_id": video_id,
        "status": "tracking_not_configured",
        "message": "Set YOUTUBE_API_KEY env var to enable live tracking. "
                   "Use YouTube Studio manually until API is connected.",
        "metrics_template": {
            "views": 0,
            "watch_time_hours": 0,
            "avg_view_duration": "0:00",
            "likes": 0,
            "comments": 0,
            "ctr": "0%",
            "impressions": 0,
        },
    }


def build_postbridge_payload(script, topic):
    """Build PostBridge-ready payload for scheduling."""
    return {
        "platform": "youtube",
        "content": {
            "title": script.get("title", topic),
            "description": script.get("description", ""),
            "tags": script.get("tags", []),
            "script": script,
        },
        "scheduling": {
            "optimal_times": ["07:00", "12:00", "17:00", "20:00"],
            "timezone": "Asia/Jakarta",
        },
        "metadata": {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "pipeline": "youtube_pipeline",
        },
    }


def run_full_pipeline(niche, idea=None, lang="id"):
    """Run the full YouTube content pipeline: scout → research → script."""
    print("=" * 60)
    print("YOUTUBE CONTENT PIPELINE")
    print("=" * 60)

    # Step 1: Idea scouting (skip if idea provided)
    if idea:
        ideas = [{"title": idea}]
        print(f"\n[1/3] Using provided idea: {idea}")
    else:
        print(f"\n[1/3] Scouting ideas for: {niche}")
        ideas = idea_scout(niche, count=5)

    top_idea = ideas[0]
    topic = top_idea.get("title", niche)

    # Step 2: Research
    print(f"\n[2/3] Researching top idea...")
    research = research_topic(top_idea)

    # Step 3: Script generation
    print(f"\n[3/3] Generating script...")
    script = generate_script(top_idea, research, lang)

    # Build output
    postbridge = build_postbridge_payload(script, topic)

    result = {
        "niche": niche,
        "timestamp": datetime.now().isoformat(),
        "idea": top_idea,
        "research": research,
        "script": script,
        "all_ideas": ideas,
        "postbridge_ready": postbridge,
    }

    print("\n" + "=" * 60)
    print(f"TITLE: {script.get('title', 'N/A')}")
    print(f"HOOK: {script.get('hook', 'N/A')}")
    print(f"SECTIONS: {len(script.get('sections', []))}")
    print(f"TAGS: {', '.join(script.get('tags', [])[:5])}...")
    print(f"IDEAS GENERATED: {len(ideas)}")
    print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="YouTube Content Pipeline")
    parser.add_argument("--niche", "-n", help="Content niche for idea scouting")
    parser.add_argument("--idea", "-i", help="Specific idea to research and script")
    parser.add_argument("--generate-script", action="store_true", help="Generate script for the idea")
    parser.add_argument("--track", action="store_true", help="Track video performance")
    parser.add_argument("--video-id", help="YouTube video ID for tracking")
    parser.add_argument("--lang", choices=["id", "en"], default="id", help="Script language")
    parser.add_argument("--output", "-o", help="Output JSON file path")

    args = parser.parse_args()

    if args.track:
        result = track_performance(args.video_id)
    elif args.idea and args.generate_script:
        client = get_llm_client()
        research = research_topic(args.idea)
        script = generate_script(args.idea, research, args.lang)
        result = {"idea": args.idea, "research": research, "script": script}
    elif args.niche or args.idea:
        result = run_full_pipeline(args.niche or "general", args.idea, args.lang)
    else:
        parser.print_help()
        return

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nSaved to: {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
