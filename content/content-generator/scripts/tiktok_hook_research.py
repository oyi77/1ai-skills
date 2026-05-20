#!/usr/bin/env python3
"""
TikTok Viral Hook Research System

Extract viral hooks from trending TikTok content.

Features:
1. Trending Search — Search TikTok for viral videos
2. Hook Extraction — Parse captions to find viral hooks
3. Pattern Analysis — Identify what makes hooks viral
4. Template Generation — Convert patterns into reusable templates

Usage:
    python3 tiktok_hook_research.py --mode search|extract|analyze --query "interior design"
"""

import argparse
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# ── CONFIG ────────────────────────────────────────────────────────────
OUTPUT_DIR = Path("/tmp/tiktok_hook_research")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HOOK_PATTERNS = {
    "landlord_rejection": {
        "regex": r"(landlord|owner|manager|rental).*(won't|said no|refused|denied)",
        "template": "My [relationship] said [constraint], so I [showed/proved] [result]",
        "confidence": 0.9,
    },
    "third_party_problem": {
        "regex": r"(friend|flatmate|partner|mum|dad|roommate).*(disagreed|doubted|skeptical|didn't believe)",
        "template": "My [relationship] was [reaction] about [AI result], so I [showed/proved] [proof]",
        "confidence": 0.85,
    },
    "impossible_challenge": {
        "regex": r"(thinks|believes|said).*(impossible|can't|won't work|no way)",
        "template": "My [relationship] thinks [X] is impossible, so I proved them wrong with [AI result]",
        "confidence": 0.8,
    },
    "transformation_reveal": {
        "regex": r"(before.*after|reveal|transformation|showed|showcased)",
        "template": "Watch this [X] transform from [style A] to [style B]",
        "confidence": 0.75,
    },
}


# ── HTTP HELPERS ─────────────────────────────────────────────────────
def post_json(url, payload, headers):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ssl_ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=clip_ctx, timeout=60) as r:
        return json.loads(r.read())


# ── MODULE 1: TRENDING SEARCH ───────────────────────────────────
def search_trending_videos(query: str, count: int = 20) -> List[Dict]:
    """
    Search TikTok for trending videos.
    FOR NOW: Simulated based on known viral patterns.
    TODO: Integrate with TikTok Search API (requires approval).
    """
    print(f"\n🔍 Searching TikTok trending: {query} (top {count})...")

    # Simulated results based on viral patterns
    # In production, replace with actual TikTok API call
    simulated_results = []

    viral_videos = [
        {
            "video_id": f"vt_{i:06d}",
            "caption": "My landlord said I can't change anything, so I showed her what AI thinks our kitchen could look like",
            "views": 234000,
            "likes": 15000,
            "comments": 234,
            "shares": 4500,
            "hashtags": "#interiordesign #rental #AI #transformation",
            "trending_score": 0.95,
        },
        {
            "video_id": f"vt_{i+1:06d}",
            "caption": "My mum was skeptical about AI interior design until I showed her this bedroom transformation",
            "views": 80000,
            "likes": 5200,
            "comments": 89,
            "shares": 1200,
            "hashtags": "#bedroom #interiordesign #AI #homedesign",
            "trending_score": 0.85,
        },
        {
            "video_id": f"vt_{i+2:06d}",
            "caption": "My flatmate thinks this style is impossible, so I proved them wrong with this AI living room design",
            "views": 60000,
            "likes": 3800,
            "comments": 67,
            "shares": 900,
            "hashtags": "#livingroom #interiordesign #AI #transformation",
            "trending_score": 0.80,
        },
        {
            "video_id": f"vt_{i+3:06d}",
            "caption": "Showed them AI room design and they changed their mind instantly",
            "views": 150000,
            "likes": 9500,
            "comments": 156,
            "shares": 3100,
            "hashtags": "#AI #interiordesign #transformation #viral",
            "trending_score": 0.88,
        },
        {
            "video_id": f"vt_{i+4:06d}",
            "caption": "Before/After reveal of rental apartment that went viral",
            "views": 120000,
            "likes": 7800,
            "comments": 134,
            "shares": 2700,
            "hashtags": "#apartment #rental #transformation #beforeafter",
            "trending_score": 0.82,
        },
        {
            "video_id": f"vt_{i+5:06d}",
            "caption": "Proved them wrong with AI interior design and they apologized",
            "views": 95000,
            "likes": 5900,
            "comments": 102,
            "shares": 1900,
            "hashtags": "#AI #interiordesign #proof #viral",
            "trending_score": 0.75,
        },
    ]

    # Filter by query if provided
    if query:
        query_lower = query.lower()
        for video in viral_videos:
            if (
                query_lower in video["caption"].lower()
                or query_lower in video["hashtags"].lower()
            ):
                simulated_results.append(video)
    else:
        simulated_results = viral_videos[:count]

    print(f"  ✅ Found {len(simulated_results)} viral videos")
    return simulated_results


# ── MODULE 2: HOOK EXTRACTION ───────────────────────────────
def extract_hook_from_caption(caption: str) -> Dict:
    """
    Extract hook components from a caption.
    Returns: hook_type, hook_template, key_elements, trending_score.
    """
    caption_clean = re.sub(r"#\w+", "", caption).strip()

    # Try to match against patterns
    matches = []
    for pattern_name, pattern_data in HOOK_PATTERNS.items():
        if re.search(pattern_data["regex"], caption_clean, re.IGNORECASE):
            matches.append(
                {
                    "pattern_name": pattern_name,
                    "confidence": pattern_data["confidence"],
                    "template": pattern_data["template"],
                }
            )

    if not matches:
        # Unknown pattern
        return {
            "hook_type": "unknown",
            "hook_template": caption[:80],
            "confidence": 0.5,
            "trending_score": 0.5,
            "key_elements": extract_key_elements(caption),
        }

    # Return highest confidence match
    best_match = max(matches, key=lambda x: x["confidence"])

    return {
        "hook_type": best_match["pattern_name"],
        "hook_template": best_match["template"],
        "confidence": best_match["confidence"],
        "trending_score": best_match["confidence"] * 0.8,  # Approximate
        "key_elements": extract_key_elements(caption_clean),
    }


def extract_key_elements(text: str) -> Dict:
    """Extract key elements from text: relationship, constraint, action, result."""
    relationships = [
        "landlord",
        "owner",
        "mum",
        "dad",
        "friend",
        "flatmate",
        "partner",
        "manager",
    ]
    constraints = ["can't", "won't", "no", "refused", "denied", "rejected"]
    actions = ["showed", "proved", "demonstrated", "revealed", "displayed", "presented"]
    results = ["result", "outcome", "proof", "demonstration"]

    found = {
        "relationships": [r for r in relationships if r.lower() in text.lower()],
        "constraints": [c for c in constraints if c.lower() in text.lower()],
        "actions": [a for a in actions if a.lower() in text.lower()],
        "results": [r for r in results if r.lower() in text.lower()],
        "hashtags": re.findall(r"#\w+", text),
    }

    return found


# ── MODULE 3: PATTERN ANALYSIS ─────────────────────────────
def analyze_hook_patterns(videos: List[Dict]) -> Dict:
    """
    Analyze patterns across multiple viral videos.
    Returns: top_patterns, avg_metrics, insights.
    """
    print(f"\n📊 Analyzing {len(videos)} viral videos...")

    # Extract hooks from all videos
    hooks = [extract_hook_from_caption(v["caption"]) for v in videos]

    # Group by hook type
    by_type = {}
    for i, hook_data in enumerate(hooks):
        htype = hook_data["hook_type"]
        if htype not in by_type:
            by_type[htype] = []
        by_type[htype].append(
            {
                "video_id": videos[i]["video_id"],
                "views": videos[i]["views"],
                "likes": videos[i]["likes"],
                "comments": videos[i]["comments"],
                "shares": videos[i]["shares"],
                "confidence": hook_data["confidence"],
                "trending_score": hook_data["trending_score"],
            }
        )

    # Calculate averages per type
    type_stats = {}
    for htype, items in by_type.items():
        if not items:
            continue

        total_views = sum(v["views"] for v in items)
        avg_views = total_views / len(items)
        avg_likes = sum(v["likes"] for v in items) / len(items)
        avg_comments = sum(v["comments"] for v in items) / len(items)
        avg_shares = sum(v["shares"] for v in items) / len(items)
        avg_score = sum(v["trending_score"] for v in items) / len(items)

        type_stats[htype] = {
            "count": len(items),
            "avg_views": round(avg_views, 0),
            "avg_likes": round(avg_likes, 0),
            "avg_comments": round(avg_comments, 0),
            "avg_shares": round(avg_shares, 0),
            "avg_trending_score": round(avg_score, 2),
            "top_video": max(items, key=lambda x: x["views"]),
            "bottom_video": min(items, key=lambda x: x["views"]),
        }

    # Sort types by avg views
    top_types = sorted(
        type_stats.items(),
        key=lambda x: x[1]["avg_views"],
        reverse=True,
    )

    # Generate insights
    insights = []
    if top_types:
        top = top_types[0]
        insights.append(
            f"Top performing hook: {top[0]} (avg {top[1]['avg_views']:,} views)"
        )

        # Analyze top's characteristics
        if top[1]["count"] >= 3:
            insights.append(
                f"High confidence - pattern proven across {top[1]['count']} videos"
            )

        bottom = top_types[-1]
        if bottom[1]["count"] >= 3:
            insights.append(
                f"Low performing hook: {bottom[0]} (avg {bottom[1]['avg_views']:,} views)"
            )

    # Cross-reference with original patterns
    print(f"  ✅ Identified {len(type_stats)} hook types")
    print(f"  ✅ Generated {len(insights)} insights")

    return {
        "by_type": type_stats,
        "top_types": top_types,
        "insights": insights,
        "total_videos_analyzed": len(videos),
    }


# ── MODULE 4: TEMPLATE GENERATION ───────────────────────────
def generate_hook_templates(analysis: Dict) -> Dict:
    """
    Generate reusable hook templates from analysis.
    Returns: optimized_templates, confidence_scores.
    """
    print(f"\n💡 Generating hook templates...")

    templates = {}
    confidence_scores = {}

    for hook_type, stats in analysis["by_type"].items():
        if stats["count"] == 0:
            continue

        avg_views = stats["avg_views"]
        confidence = stats["avg_trending_score"]

        # Generate template based on top video
        top_video = stats["top_video"]

        # Extract hook structure
        hook = extract_hook_from_caption(top_video["caption"])

        # Optimize template
        template = hook["hook_template"]
        if avg_views >= 100000:
            template += " (PROVEN 100K+ avg views)"
        elif avg_views >= 50000:
            template += " (STRONG 50K+ avg views)"
        elif avg_views >= 20000:
            template += " (GOOD 20K+ avg views)"
        else:
            template += " (TEST <20K avg views)"

        templates[hook_type] = {
            "template": template,
            "confidence": round(confidence, 2),
            "avg_views": avg_views,
            "count": stats["count"],
            "example_caption": top_video["caption"],
            "example_views": top_video["views"],
            "hashtags": top_video["hashtags"],
        }

        confidence_scores[hook_type] = round(confidence, 2)

    print(f"  ✅ Generated {len(templates)} hook templates")

    return {
        "templates": templates,
        "confidence_scores": confidence_scores,
    }


# ── MAIN ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="TikTok Viral Hook Research System")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["search", "extract", "analyze", "generate"],
        help="Operation mode",
    )
    parser.add_argument(
        "--query",
        default="interior design transformation",
        help="Search query (for search mode)",
    )
    parser.add_argument(
        "--count", type=int, default=20, help="Number of videos to search (default: 20)"
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON file with video data (for extract/analyze modes)",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("🔍 TIKTOK VIRAL HOOK RESEARCH SYSTEM")
    print("=" * 70)

    if args.mode == "search":
        videos = search_trending_videos(args.query, args.count)

        # Save search results
        output_file = (
            OUTPUT_DIR / f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "query": args.query,
                    "count": args.count,
                    "videos": videos,
                },
                f,
                indent=2,
            )

        print(f"\n💾 Saved: {output_file}")

    elif args.mode == "extract":
        if not args.input:
            print("❌ --input required for extract mode")
            return

        with open(args.input, "r") as f:
            data = json.load(f)

        videos = data.get("videos", [])
        hooks = [extract_hook_from_caption(v["caption"]) for v in videos]

        # Save extracted hooks
        output_file = (
            OUTPUT_DIR / f"hooks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "source_file": args.input,
                    "hooks": hooks,
                },
                f,
                indent=2,
            )

        print(f"\n💾 Saved: {output_file}")

    elif args.mode == "analyze":
        if not args.input:
            print("❌ --input required for analyze mode")
            return

        with open(args.input, "r") as f:
            data = json.load(f)

        videos = data.get("videos", [])
        analysis = analyze_hook_patterns(videos)

        # Save analysis
        output_file = (
            OUTPUT_DIR / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "source_file": args.input,
                    "analysis": analysis,
                },
                f,
                indent=2,
            )

        print(f"\n💾 Saved: {output_file}")

    elif args.mode == "generate":
        if not args.input:
            print("❌ --input required for generate mode")
            return

        with open(args.input, "r") as f:
            data = json.load(f)

        # Load analysis if available, otherwise extract first
        if "analysis" in data:
            analysis = data["analysis"]
        else:
            videos = data.get("videos", [])
            analysis = analyze_hook_patterns(videos)

        templates = generate_hook_templates(analysis)

        # Save templates
        output_file = (
            OUTPUT_DIR / f"templates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "source_file": args.input,
                    "templates": templates,
                },
                f,
                indent=2,
            )

        print(f"\n💾 Saved: {output_file}")
        print("\n📋 TEMPLATES READY FOR CONTENT GENERATION:")
        for htype, tmpl in templates["templates"].items():
            print(f"  {htype}: {tmpl['template'][:60]}...")
        print()

    print("=" * 70)


if __name__ == "__main__":
    main()
