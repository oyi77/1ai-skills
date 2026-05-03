#!/usr/bin/env python3
"""
Continuous Viral TikTok Research System

Features:
1. Hourly research — Scan trending TikTok hooks, viral topics
2. Performance tracking — Log views, engagement per hook type
3. Confidence system — Update scores based on performance
4. Auto-generation — Generate content using top-performing hooks

Usage:
    python3 viral_research_system.py --mode research|generate|analyze
"""

import argparse
import json
import os
import random
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

# ── CONFIG ────────────────────────────────────────────────────
POST_BRIDGE_KEY = os.environ.get("POST_BRIDGE_API_KEY", "")
POST_BRIDGE_URL = "https://api.post-bridge.com/v1"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

OUTPUT_DIR = Path("/tmp/viral_research")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESEARCH_DIR = OUTPUT_DIR / "research"
CONTENT_DIR = OUTPUT_DIR / "content"
MEMORY_DIR = OUTPUT_DIR / "memory"

for d in [RESEARCH_DIR, CONTENT_DIR, MEMORY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# ── LARRY PLAYBOOK HOOKS (with confidence) ──────────────────
HOOK_TEMPLATES = {
    "landlord_kitchen": {
        "template": "My landlord said I can't change anything, so I showed her what AI thinks our {room} could look like",
        "hashtags": "#interiordesign #rental #AI #transformation",
        "base_confidence": 0.9,
        "avg_views": 234000,
        "total_posts": 0,
        "avg_views_per_post": 0,
        "top_views": 0,
        "bottom_views": float('inf'),
    },
    "parent_bedroom": {
        "template": "My {parent} was skeptical about AI until I showed them this {style} for our {room}",
        "hashtags": "#bedroom #interiordesign #AI #homedesign",
        "base_confidence": 0.75,
        "avg_views": 80000,
        "total_posts": 0,
        "avg_views_per_post": 0,
        "top_views": 0,
        "bottom_views": float('inf'),
    },
    "roommate_living": {
        "template": "My flatmate thinks {style} is impossible, so I proved them wrong with this AI {result} for our {room}",
        "hashtags": "#livingroom #interiordesign #AI #transformation",
        "base_confidence": 0.65,
        "avg_views": 60000,
        "total_posts": 0,
        "avg_views_per_post": 0,
        "top_views": 0,
        "bottom_views": float('inf'),
    },
}

# ── MEMORY STRUCTURE ───────────────────────────────────────────────
MEMORY_FILE = MEMORY_DIR / "performance_memory.json"

def load_memory() -> Dict:
    """Load performance memory from disk."""
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {k: v for k, v in HOOK_TEMPLATES.items()}

def save_memory(memory: Dict):
    """Save performance memory to disk."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print(f"💾 Memory saved: {MEMORY_FILE}")

def update_confidence(memory: Dict, hook_type: str, views: int):
    """
    Update confidence score based on performance.
    - Success (> target) → confidence UP
    - Failure (< target) → confidence DOWN
    """
    target_views = memory[hook_type]["avg_views"]
    current_conf = memory[hook_type].get("confidence", memory[hook_type]["base_confidence"])

    if views >= target_views:
        # Success — increase confidence
        new_conf = min(current_conf + 0.1, 1.0)
        change = "📈 UP"
    elif views < target_views * 0.5:
        # Failure — decrease confidence
        new_conf = max(current_conf - 0.15, 0.2)
        change = "📉 DOWN"
    else:
        # Neutral — keep confidence
        new_conf = current_conf
        change = "➡️ STABLE"

    memory[hook_type]["confidence"] = round(new_conf, 2)

    # Update stats
    total_posts = memory[hook_type]["total_posts"] + 1
    avg_views = (memory[hook_type]["avg_views_per_post"] * memory[hook_type]["total_posts"] + views) / total_posts
    memory[hook_type]["total_posts"] = total_posts
    memory[hook_type]["avg_views_per_post"] = avg_views
    memory[hook_type]["top_views"] = max(memory[hook_type]["top_views"], views)
    memory[hook_type]["bottom_views"] = min(memory[hook_type]["bottom_views"], views)

    return change, new_conf

# ── RESEARCH MODULE ───────────────────────────────────────────────
def research_trending_topics() -> List[str]:
    """
    Research trending TikTok topics.
    For now, returns simulated results based on known viral themes.
    TODO: Integrate with actual TikTok API or scraping.
    """
    print(f"\n🔍 Researching trending TikTok topics...")

    # Simulated viral topics (TODO: real API integration)
    topics = [
        "AI interior design transformation",
        "Rental apartment hacks",
        "Small space optimization",
        "Budget-friendly renovations",
        "Before/after reveals",
        "Landlord negotiation wins",
        "Flatmate DIY challenges",
        "Minimalist lifestyle",
        "Scandinavian design trends",
        "Cozy apartment aesthetics",
        "Smart home automation on budget",
        "IKEA hack videos",
        "Storage solutions for small spaces",
        "Natural lighting optimization",
        "Plant-based room decor",
        "Warm color psychology",
    ]

    # TODO: Replace with real TikTok API call
    # For now, random selection
    selected = random.sample(topics, min(5, len(topics)))

    research_file = RESEARCH_DIR / f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(research_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "topics": selected,
            "source": "simulated",  # TODO: "tiktok_api"
            "total_topics": len(topics),
        }, f, indent=2)

    print(f"  ✅ Found {len(selected)} trending topics")
    print(f"  💾 Saved: {research_file.name}")

    return selected

def analyze_hook_performance() -> Dict:
    """Analyze hook performance from memory."""
    print(f"\n📊 Analyzing hook performance...")

    memory = load_memory()

    analysis = {}
    for hook_type, data in memory.items():
        if data["total_posts"] == 0:
            continue

        # Calculate metrics
        avg_views = data["avg_views_per_post"]
        confidence = data.get("confidence", data["base_confidence"])
        total = data["total_posts"]

        # Performance rating
        if avg_views >= data["avg_views"]:
            rating = "🔥 VIRAL"
            score = 5
        elif avg_views >= data["avg_views"] * 0.7:
            rating = "⭐ STRONG"
            score = 4
        elif avg_views >= data["avg_views"] * 0.4:
            rating = "✅ GOOD"
            score = 3
        elif avg_views >= data["avg_views"] * 0.2:
            rating = "⚠️ WEAK"
            score = 2
        else:
            rating = "❌ FAILING"
            score = 1

        analysis[hook_type] = {
            "avg_views": avg_views,
            "total_posts": total,
            "confidence": confidence,
            "rating": rating,
            "score": score,
        }

    # Sort by score
    ranked = sorted(analysis.items(), key=lambda x: x[1]["score"], reverse=True)

    print(f"  Top hook: {ranked[0][0]} ({ranked[0][1]['rating']})")
    print(f"  Bottom hook: {ranked[-1][0]} ({ranked[-1][1]['rating']})")

    return analysis

def generate_content_recommendations(analysis: Dict) -> List[Dict]:
    """
    Generate content recommendations based on top performers.
    """
    print(f"\n💡 Generating content recommendations...")

    # Get top 2 performing hooks
    ranked = sorted(analysis.items(), key=lambda x: x[1]["score"], reverse=True)
    top_hooks = ranked[:2]

    recommendations = []
    for hook_type, perf in top_hooks:
        hook = HOOK_TEMPLATES[hook_type]

        # Generate variations
        variations = [
            f"Original: {hook['template'][:60]}...",
            f"Alt 1: {hook['template'][:30]}... see result",
            f"Alt 2: Before/after version of {hook['template'][:30]}...",
        ]

        rec = {
            "hook_type": hook_type,
            "confidence": perf["confidence"],
            "avg_views": perf["avg_views"],
            "rating": perf["rating"],
            "template": hook["template"],
            "hashtags": hook["hashtags"],
            "variations": variations,
        }
        recommendations.append(rec)

        print(f"  ✅ {hook_type}: {perf['rating']} (conf: {perf['confidence']:.2f})")

    return recommendations

# ── GENERATION MODULE ───────────────────────────────────────────────
def log_post_performance(hook_type: str, views: int):
    """Log post performance to memory."""
    print(f"\n📝 Logging post performance: {hook_type} = {views:,} views")

    memory = load_memory()
    change, new_conf = update_confidence(memory, hook_type, views)

    print(f"  {change} confidence: {new_conf:.2f}")
    save_memory(memory)

    # Log to history
    history_file = MEMORY_DIR / f"history_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(history_file, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "hook_type": hook_type,
            "views": views,
            "confidence": new_conf,
        }) + "\n")

    print(f"  💾 Logged to: {history_file.name}")

    return memory[hook_type]

# ── LLM CONTENT GENERATOR ──────────────────────────────────────────
def generate_viral_content(hook_type: str, topic: str) -> Dict:
    """Generate viral hook + caption using LLM."""
    print(f"\n🤖 Generating viral content: {hook_type} + {topic}")

    if not GROQ_API_KEY:
        # Fallback to template
        hook = HOOK_TEMPLATES[hook_type]
        return {
            "hook": hook["template"][:80],
            "caption": f"Check this out! {hook['hashtags']}",
            "hashtags": hook["hashtags"],
        }

    hook = HOOK_TEMPLATES[hook_type]

    user_prompt = f"""You are a viral TikTok content expert using Larry's proven formula.

HOOK TEMPLATE: "{hook['template']}"
CURRENT TOPIC: {topic}
HASHTAGS: {hook['hashtags']}

Generate JSON with:
- "hook": Punchy headline (max 80 chars), based on template + topic
- "caption": Story-style caption (150-200 chars), natural tone
- "hashtags": 5 relevant hashtags as string
- "room": Choose from: kitchen_small, living_room_cozy, bedroom_minimal

Return ONLY valid JSON, no extra text."""

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a viral TikTok content expert. Always respond with valid JSON only."},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.85,
            "max_tokens": 400,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(GROQ_URL, data=data, headers=headers, method="POST")
        ssl_ctx = ssl.create_default_context()

        with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as r:
            resp = json.loads(r.read())

        text = resp["choices"][0]["message"]["content"]
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            content = json.loads(text[start:end])
            content.setdefault("hashtags", hook["hashtags"])
            content.setdefault("hook_type", hook_type)
            return content

    except Exception as e:
        print(f"  ⚠️  LLM error: {e} — using template")

    return {
        "hook": hook["template"][:80],
        "caption": f"Check this out! {hook['hashtags']}",
        "hashtags": hook["hashtags"],
        "hook_type": hook_type,
        "room": "kitchen_small",
    }

# ── MAIN ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Continuous Viral TikTok Research System")
    parser.add_argument("--mode", required=True,
                        choices=["research", "analyze", "generate", "log"],
                        help="Operation mode")
    parser.add_argument("--hook-type", help="Hook type (for log mode)")
    parser.add_argument("--views", type=int, help="Views (for log mode)")
    parser.add_argument("--topic", default="AI interior design transformation",
                        help="Topic (for generate mode)")
    args = parser.parse_args()

    print("=" * 70)
    print("🚀 CONTINUOUS VIRAL TIKTOK RESEARCH SYSTEM")
    print("=" * 70)
    print()

    if args.mode == "research":
        # Research trending topics
        topics = research_trending_topics()

        print(f"\n✅ Research complete")
        print(f"   Topics: {', '.join(topics)}")

    elif args.mode == "analyze":
        # Analyze hook performance
        analysis = analyze_hook_performance()

        print(f"\n✅ Analysis complete")
        print(f"   Total hook types analyzed: {len(analysis)}")

        # Save analysis report
        report_file = OUTPUT_DIR / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w") as f:
            json.dump(analysis, f, indent=2)
        print(f"   Report: {report_file.name}")

    elif args.mode == "generate":
        # Generate content recommendations
        memory = load_memory()
        analysis = {k: {
            "confidence": v.get("confidence", v["base_confidence"]),
            "avg_views": v.get("avg_views_per_post", v["avg_views"]),
        } for k, v in memory.items()}

        recommendations = generate_content_recommendations(analysis)

        print(f"\n✅ Generated {len(recommendations)} recommendations")

        # Save recommendations
        rec_file = CONTENT_DIR / f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rec_file, "w") as f:
            json.dump(recommendations, f, indent=2)
        print(f"   Saved: {rec_file.name}")

    elif args.mode == "log":
        # Log post performance
        if not args.hook_type or args.views is None:
            print("❌ --hook-type and --views required for log mode")
            return

        hook_data = log_post_performance(args.hook_type, args.views)

        print(f"\n✅ Logged performance")
        print(f"   New confidence: {hook_data['confidence']:.2f}")
        print(f"   Total posts: {hook_data['total_posts']}")

    print()
    print("=" * 70)

    # System summary
    memory = load_memory()
    print("\n📊 SYSTEM SUMMARY")
    print(f"   Total hook types tracked: {len(memory)}")
    print(f"   Total posts logged: {sum(v['total_posts'] for v in memory.values())}")
    print(f"   Top performer: {max(memory.items(), key=lambda x: x[1]['avg_views_per_post'])[0][0]}")
    print("=" * 70)

if __name__ == "__main__":
    main()
