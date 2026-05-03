#!/usr/bin/env python3
"""Tech News Digest - Aggregate and summarize tech news from multiple sources."""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import openai
from duckduckgo_search import DDGS


TWITTER_CLI = "/home/openclaw/.local/bin/twitter"
NOTES_DIR = Path("/home/openclaw/.openclaw/workspace/notes")
LLM_BASE_URL = "http://localhost:20128/v1"
LLM_API_KEY = "omniroute"
SIMILARITY_THRESHOLD = 0.7


def search_duckduckgo(topics: list[str], count: int) -> list[dict]:
    """Search DuckDuckGo for tech news on given topics."""
    results = []
    per_topic = max(1, count // len(topics)) if topics else count
    with DDGS() as ddgs:
        for topic in topics:
            query = f"{topic} news today"
            try:
                hits = list(ddgs.news(query, max_results=per_topic))
                for h in hits:
                    results.append({
                        "title": h.get("title", ""),
                        "url": h.get("url", ""),
                        "body": h.get("body", ""),
                        "source": f"duckduckgo/{topic}",
                        "date": h.get("date", ""),
                    })
            except Exception as e:
                print(f"[warn] DuckDuckGo search failed for '{topic}': {e}", file=sys.stderr)
    return results


def search_twitter(topics: list[str], count: int) -> list[dict]:
    """Search Twitter via CLI for hashtag-based tech news."""
    results = []
    hashtags = " ".join(f"#{t}" for t in topics)
    try:
        proc = subprocess.run(
            [TWITTER_CLI, "search", hashtags, "--count", str(count), "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            tweets = json.loads(proc.stdout)
            if isinstance(tweets, list):
                for tw in tweets:
                    results.append({
                        "title": tw.get("text", "")[:120],
                        "url": tw.get("url", ""),
                        "body": tw.get("text", ""),
                        "source": "twitter",
                        "date": tw.get("created_at", ""),
                    })
        else:
            print(f"[warn] Twitter CLI returned code {proc.returncode}", file=sys.stderr)
            if proc.stderr.strip():
                print(f"[warn] {proc.stderr.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print(f"[warn] Twitter CLI not found at {TWITTER_CLI}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("[warn] Twitter CLI timed out", file=sys.stderr)
    except Exception as e:
        print(f"[warn] Twitter search failed: {e}", file=sys.stderr)
    return results


def deduplicate(items: list[dict]) -> list[dict]:
    """Remove near-duplicate items based on title similarity."""
    unique = []
    for item in items:
        title = item["title"].strip()
        if not title:
            continue
        is_dup = False
        for kept in unique:
            ratio = SequenceMatcher(None, title.lower(), kept["title"].lower()).ratio()
            if ratio >= SIMILARITY_THRESHOLD:
                is_dup = True
                break
        if not is_dup:
            unique.append(item)
    return unique


def summarize_with_llm(items: list[dict]) -> str:
    """Send top items to OmniRoute LLM for summarization into a digest."""
    client = openai.OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

    bullet_list = ""
    for i, item in enumerate(items, 1):
        bullet_list += f"{i}. **{item['title']}**\n"
        if item.get("body"):
            bullet_list += f"   {item['body'][:300]}\n"
        if item.get("url"):
            bullet_list += f"   Source: {item['url']}\n"
        bullet_list += "\n"

    prompt = (
        "You are a tech news editor. Summarize the following news items into a concise, "
        "well-structured daily digest in markdown format. Group related stories together. "
        "For each item, write a 1-2 sentence summary and include the source URL. "
        "Add a brief editorial intro at the top.\n\n"
        f"News items:\n{bullet_list}"
    )

    try:
        response = client.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[warn] LLM summarization failed: {e}", file=sys.stderr)
        # Fallback: return raw bullet list
        return f"## Raw News Items\n\n{bullet_list}"


def build_digest(topics: list[str], count: int) -> str:
    """Main pipeline: search, deduplicate, summarize."""
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"[info] Searching DuckDuckGo for: {', '.join(topics)}", file=sys.stderr)
    ddg_results = search_duckduckgo(topics, count * 2)
    print(f"[info] Got {len(ddg_results)} results from DuckDuckGo", file=sys.stderr)

    print(f"[info] Searching Twitter for: {', '.join(topics)}", file=sys.stderr)
    tw_results = search_twitter(topics, count)
    print(f"[info] Got {len(tw_results)} results from Twitter", file=sys.stderr)

    all_results = ddg_results + tw_results
    print(f"[info] Total raw results: {len(all_results)}", file=sys.stderr)

    deduped = deduplicate(all_results)
    print(f"[info] After deduplication: {len(deduped)}", file=sys.stderr)

    top_items = deduped[:count]
    print(f"[info] Sending top {len(top_items)} items to LLM for summarization", file=sys.stderr)

    summary = summarize_with_llm(top_items)

    digest = f"# Tech News Digest - {today}\n\n{summary}\n\n---\n*Generated by tech-news-digest skill on {today}*\n"
    return digest


def main():
    parser = argparse.ArgumentParser(description="Generate a tech news digest")
    parser.add_argument(
        "--topics",
        type=str,
        default="AI,crypto,trading",
        help="Comma-separated list of topics to search (default: AI,crypto,trading)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of top items to include in digest (default: 10)",
    )
    args = parser.parse_args()

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    digest = build_digest(topics, args.count)

    # Save to file
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = NOTES_DIR / f"tech-digest-{today}.md"
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(digest, encoding="utf-8")
    print(f"[info] Digest saved to {output_path}", file=sys.stderr)

    # Print to stdout
    print(digest)


if __name__ == "__main__":
    main()
