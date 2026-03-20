"""
Content Kingdom Self-Improve Engine
Runs after every successful pipeline. Analyzes results, updates strategy.

Self-improve loop:
1. Read engagement data from last 7 days
2. Identify what's working (high CTR, shares, saves)
3. Update config.json: boost winning products/hooks/times
4. Prune losing patterns
5. Log decisions with reasoning
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
STATE_FILE = SKILL_DIR / "state.json"
OUTPUT_DIR = SKILL_DIR / "output"
LOG_FILE = SKILL_DIR / "logs" / "self_improve.log"
LEARNINGS_DIR = SKILL_DIR / "learnings"

LEARNINGS_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_config():
    try:
        return json.loads(CONFIG_FILE.read_text())
    except Exception as e:
        log(f"Config load failed: {e}")
        return {}


def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
    log("✅ Config updated")


def load_recent_analytics():
    """Load PostBridge analytics from output files."""
    analytics = []
    for f in sorted(OUTPUT_DIR.glob("analytics_*.json"), reverse=True)[:7]:
        try:
            data = json.loads(f.read_text())
            analytics.extend(data if isinstance(data, list) else [data])
        except Exception:
            pass
    return analytics


def load_phase_outputs():
    """Load recent pipeline outputs for self-analysis."""
    outputs = {}
    for key in ["schedule", "post", "analyze", "optimize"]:
        for f in sorted(OUTPUT_DIR.glob(f"{key}_*.json"), reverse=True)[:3]:
            try:
                outputs[key] = json.loads(f.read_text())
                break
            except Exception:
                pass
    return outputs


def analyze_winning_patterns(analytics, outputs):
    """
    Identify what's working. Returns dict of insights.
    Patterns we look for:
    - Best posting times (by engagement rate)
    - Best products (by CTR / conversions)
    - Best hook patterns (by shares/saves)
    - Best platforms (by reach)
    """
    insights = {
        "winning_products": [],
        "losing_products": [],
        "best_times": {},
        "best_platforms": [],
        "hook_patterns": [],
        "recommendations": [],
    }

    if not analytics:
        log("No analytics data — using state.json winners")
        # Fallback: read from state.json winners
        try:
            state = json.loads(STATE_FILE.read_text())
            phases = state.get("phases", {})
            scale = phases.get("scale", {}).get("data", {})
            winners = scale.get("winners", [])
            if winners:
                insights["winning_products"] = [w.get("product", "") for w in winners[:3]]
                insights["recommendations"].append(f"Boost winners: {insights['winning_products']}")
        except Exception:
            pass
        return insights

    # Aggregate by product
    product_stats = {}
    for post in analytics:
        product = post.get("product", post.get("caption_theme", "unknown"))
        platform = post.get("platform", "unknown")
        views = post.get("views", 0) or 0
        likes = post.get("likes", 0) or 0
        shares = post.get("shares", 0) or 0
        clicks = post.get("clicks", 0) or 0

        if product not in product_stats:
            product_stats[product] = {"views": 0, "likes": 0, "shares": 0, "clicks": 0, "posts": 0}
        product_stats[product]["views"] += views
        product_stats[product]["likes"] += likes
        product_stats[product]["shares"] += shares
        product_stats[product]["clicks"] += clicks
        product_stats[product]["posts"] += 1

    # Score each product: engagement rate = (likes+shares*3+clicks*5) / max(views,1)
    scored = []
    for product, stats in product_stats.items():
        score = (stats["likes"] + stats["shares"] * 3 + stats["clicks"] * 5) / max(stats["views"], 1)
        scored.append((product, score, stats))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Top 3 = winners, bottom 2 = losers
    if scored:
        insights["winning_products"] = [p for p, s, _ in scored[:3]]
        insights["losing_products"] = [p for p, s, _ in scored[-2:] if s < 0.01]

    if insights["winning_products"]:
        insights["recommendations"].append(f"✅ Boost budget for: {', '.join(insights['winning_products'][:2])}")
    if insights["losing_products"]:
        insights["recommendations"].append(f"⚠️ Reduce posts for: {', '.join(insights['losing_products'])}")

    return insights


def update_config_with_insights(cfg, insights):
    """Apply insights to config. Only improve, never break."""
    changes = []

    # 1. Boost winning products (move to top of priority list)
    products = cfg.get("products", [])
    if insights["winning_products"] and products:
        # Create priority map
        priority = {p: i for i, p in enumerate(insights["winning_products"])}
        products_sorted = sorted(
            products,
            key=lambda p: priority.get(p.get("name", ""), 999)
        )
        if products_sorted != products:
            cfg["products"] = products_sorted
            changes.append(f"Reordered products: winners first — {insights['winning_products'][:2]}")

    # 2. Update self_improve metadata
    cfg["_self_improve"] = {
        "last_run": datetime.now().isoformat(),
        "last_insights": insights,
        "total_runs": cfg.get("_self_improve", {}).get("total_runs", 0) + 1,
    }

    return cfg, changes


def save_learning(insights, changes):
    """Write learning to learnings/ for future reference."""
    today = datetime.now().strftime("%Y-%m-%d")
    learning_file = LEARNINGS_DIR / f"learning_{today}.json"
    learning = {
        "date": today,
        "insights": insights,
        "changes_applied": changes,
        "ts": datetime.now().isoformat(),
    }
    learning_file.write_text(json.dumps(learning, indent=2, ensure_ascii=False))
    log(f"Learning saved: {learning_file}")


def run():
    log("=" * 60)
    log("Self-Improve Engine starting...")

    cfg = load_config()
    if not cfg:
        log("No config — skipping")
        return

    analytics = load_recent_analytics()
    outputs = load_phase_outputs()
    log(f"Loaded {len(analytics)} analytics records, {len(outputs)} phase outputs")

    insights = analyze_winning_patterns(analytics, outputs)
    log(f"Insights: winners={insights['winning_products']}, losers={insights['losing_products']}")
    for rec in insights["recommendations"]:
        log(f"  → {rec}")

    cfg, changes = update_config_with_insights(cfg, insights)

    if changes:
        save_config(cfg)
        for c in changes:
            log(f"Applied: {c}")
    else:
        log("No config changes needed — pipeline performing optimally")
        # Still save metadata
        cfg["_self_improve"] = {
            "last_run": datetime.now().isoformat(),
            "last_insights": insights,
            "total_runs": cfg.get("_self_improve", {}).get("total_runs", 0) + 1,
        }
        save_config(cfg)

    save_learning(insights, changes)
    log("✅ Self-improve complete")


if __name__ == "__main__":
    run()
