#!/usr/bin/env python3
"""
Custom Morning Brief

Daily briefing agent that aggregates news, tasks, open loops,
and content drafts. Delivers via Telegram.

Usage:
    python morning_brief.py
    python morning_brief.py --dry-run
    python morning_brief.py --topics "AI,trading,crypto"
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
NOTES_DIR = WORKSPACE / "notes"

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"

DEFAULT_TOPICS = ["AI", "trading", "crypto", "open source", "SEO"]


def get_llm_client():
    """Get OpenAI-compatible client via OmniRoute."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai not installed. Run: pip install openai")
        sys.exit(1)
    return OpenAI(base_url=OMNIROUTE_BASE, api_key=OMNIROUTE_KEY)


def llm_chat(client, system_prompt, user_prompt):
    """Send chat completion via OmniRoute."""
    try:
        resp = client.chat.completions.create(
            model=OMNIROUTE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[LLM Error: {e}]"


def read_file_safe(path):
    """Read file if it exists, return empty string otherwise."""
    try:
        return Path(path).read_text()
    except (FileNotFoundError, PermissionError):
        return ""


def gather_memory(date_str=None):
    """Read yesterday's memory notes."""
    if not date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime("%Y-%m-%d")

    memory_file = MEMORY_DIR / f"{date_str}.md"
    content = read_file_safe(memory_file)
    if content:
        print(f"  Found memory: {memory_file.name} ({len(content)} chars)")
    else:
        print(f"  No memory file for {date_str}")
    return content


def gather_open_loops():
    """Read open loops / pending tasks."""
    content = read_file_safe(NOTES_DIR / "open-loops.md")
    if content:
        print(f"  Found open-loops.md ({len(content)} chars)")
    else:
        print("  No open-loops.md found")
    return content


def gather_news(topics):
    """Search for news on configured topics."""
    results = {}
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            for topic in topics[:5]:
                hits = list(ddgs.news(topic, max_results=3))
                results[topic] = [
                    {"title": h.get("title", ""), "body": h.get("body", "")[:150]}
                    for h in hits
                ]
                print(f"  News [{topic}]: {len(hits)} results")
    except ImportError:
        print("  WARNING: duckduckgo-search not installed")
    except Exception as e:
        print(f"  WARNING: News search failed: {e}")
    return results


def gather_twitter_trends(topics):
    """Search Twitter for trending topics."""
    results = {}
    try:
        for topic in topics[:3]:
            cmd = ["twitter-cli", "search", topic, "--limit", "3"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if proc.returncode == 0 and proc.stdout.strip():
                results[topic] = proc.stdout.strip()[:500]
                print(f"  Twitter [{topic}]: found results")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  WARNING: twitter-cli not available or timed out")
    except Exception as e:
        print(f"  WARNING: Twitter search failed: {e}")
    return results


def synthesize_brief(memory, open_loops, news, twitter, topics):
    """Use LLM to synthesize all sources into a morning brief."""
    client = get_llm_client()

    today = datetime.now().strftime("%Y-%m-%d")
    news_text = json.dumps(news, ensure_ascii=False, indent=1) if news else "No news gathered."
    twitter_text = json.dumps(twitter, ensure_ascii=False, indent=1) if twitter else "No Twitter data."

    system = """You are a personal briefing assistant. Create a concise morning brief.
Use this exact format (plain text, no markdown code blocks):

☀️ Morning Brief — {date}

📋 OPEN TASKS
- List pending tasks from open loops (bullet points)

📰 NEWS & TRENDS
- Summarize top news per topic (1 line each)

💡 INSIGHTS & OPPORTUNITIES
- Note any actionable opportunities spotted

🔁 YESTERDAY RECAP
- Key points from yesterday's notes

Keep it concise — max 30 lines total. Prioritize actionable items."""

    prompt = f"""Date: {today}
Topics of interest: {', '.join(topics)}

Yesterday's notes:
{memory[:1500] if memory else 'No notes from yesterday.'}

Open loops:
{open_loops[:1000] if open_loops else 'No open loops found.'}

News:
{news_text[:2000]}

Twitter trends:
{twitter_text[:1000]}

Generate the morning brief."""

    return llm_chat(client, system, prompt)


def send_telegram(message, dry_run=False):
    """Send brief via openclaw system event."""
    if dry_run:
        print("\n[DRY RUN] Would send to Telegram:")
        print(message)
        return True

    try:
        cmd = [
            "openclaw", "system", "event",
            "--text", message,
            "--mode", "now",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode == 0:
            print("  Sent to Telegram via openclaw system event")
            return True
        else:
            print(f"  WARNING: openclaw command failed: {proc.stderr}")
            return False
    except FileNotFoundError:
        print("  WARNING: openclaw command not found, printing to stdout")
        print(message)
        return False
    except Exception as e:
        print(f"  WARNING: Send failed: {e}")
        print(message)
        return False


def run_brief(topics=None, date_str=None, dry_run=False):
    """Run the full morning brief pipeline."""
    topics = topics or DEFAULT_TOPICS

    print("=" * 60)
    print(f"MORNING BRIEF — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Gather
    print("\n[1/3] Gathering sources...")
    memory = gather_memory(date_str)
    open_loops = gather_open_loops()
    news = gather_news(topics)
    twitter = gather_twitter_trends(topics)

    # Synthesize
    print("\n[2/3] Synthesizing brief...")
    brief = synthesize_brief(memory, open_loops, news, twitter, topics)

    # Deliver
    print("\n[3/3] Delivering...")
    send_telegram(brief, dry_run)

    print("\n" + "=" * 60)
    print("Morning brief complete.")
    print("=" * 60)

    return brief


def main():
    parser = argparse.ArgumentParser(description="Custom Morning Brief")
    parser.add_argument("--topics", help="Comma-separated topics (default: AI,trading,crypto,open source,SEO)")
    parser.add_argument("--date", help="Date for memory lookup (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Print brief without sending to Telegram")

    args = parser.parse_args()

    topics = args.topics.split(",") if args.topics else DEFAULT_TOPICS
    run_brief(topics=topics, date_str=args.date, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
