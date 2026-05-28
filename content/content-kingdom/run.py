#!/usr/bin/env python3
"""
Content Kingdom — CLI Runner
=============================
Single entry point for ALL content operations.
Every cron job, every script, every pipeline should go through here.

Usage:
    python3 run.py                    # Run full daily pipeline
    python3 run.py --phase post       # Run specific phase
    python3 run.py --phase learn      # Process pending learnings
    python3 run.py --stats            # Show learning stats
    python3 run.py --bootstrap        # Bootstrap training data
    python3 run.py --rules            # Show active rules
    python3 run.py --feedback "text"  # Manually add feedback
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure modules are importable
sys.path.insert(0, str(Path(__file__).parent))

from modules.learning_engine import (
    get_learning_stats, get_active_rules, get_design_guidelines,
    get_copy_guidelines, bootstrap_veris, capture_feedback,
    get_top_performing_patterns,
)
from modules.chat_learning_hook import process_user_feedback


def cmd_stats():
    """Show learning system stats."""
    stats = get_learning_stats()
    print(f"\n📊 Content Kingdom — Learning Stats")
    print(f"{'='*40}")
    print(f"  Total learnings: {stats['total_learnings']}")
    print(f"  Active rules:    {stats['active_rules']}")
    print(f"  Total rules:     {stats['total_rules']}")
    print(f"  Training sessions: {stats['training_sessions']}")
    
    if stats['by_type']:
        print(f"\n  By type:")
        for t, c in stats['by_type'].items():
            print(f"    {t}: {c}")
    
    if stats['by_source']:
        print(f"\n  By source:")
        for s, c in stats['by_source'].items():
            print(f"    {s}: {c}")
    
    patterns = get_top_performing_patterns()
    if patterns and "message" not in patterns:
        print(f"\n  Top performing patterns:")
        for platform, data in patterns.items():
            print(f"    {platform}: {data['total_posts']} posts, avg engagement {data['avg_engagement']}")


def cmd_rules(category=None):
    """Show active rules."""
    rules = get_active_rules(category)
    cat_label = f" ({category})" if category else ""
    print(f"\n📋 Active Rules{cat_label}: {len(rules)}")
    print(f"{'='*50}")
    for r in rules:
        print(f"  [{r['category']:10}] p{r['priority']}: {r['rule'][:70]}")
        if r.get('description'):
            print(f"             {r['description'][:70]}")


def cmd_guidelines():
    """Show consolidated guidelines."""
    design = get_design_guidelines()
    copy = get_copy_guidelines()
    
    print(f"\n🎨 Design Guidelines")
    print(f"{'='*40}")
    for k, v in design.items():
        if k != "rules":
            print(f"  {k}: {v}")
    
    print(f"\n📝 Copy Guidelines")
    print(f"{'='*40}")
    for k, v in copy.items():
        if k != "rules":
            print(f"  {k}: {v}")


def cmd_bootstrap():
    """Bootstrap training data."""
    result = bootstrap_veris()
    print(f"✅ {result}")
    cmd_stats()


def cmd_feedback(text, source="user"):
    """Manually add feedback."""
    result = process_user_feedback(text, user_name=source)
    if result:
        print(f"✅ Captured: [{result['type']}] from {result['source']}")
        print(f"   Content: {result['content'][:80]}")
    else:
        print("ℹ️ No content-related feedback detected in message.")


def cmd_pipeline():
    """Run full daily pipeline through Content Kingdom."""
    print("🚀 Content Kingdom — Daily Pipeline")
    print(f"{'='*40}")
    
    # Import orchestrator
    try:
        from orchestrator import run_daily_pipeline
        result = run_daily_pipeline()
        print(f"✅ Pipeline complete: {result}")
    except ImportError:
        # Fallback: call daily_content_poster.py
        import subprocess
        poster = Path(__file__).parent.parent.parent.parent / "scripts/daily_content_poster.py"
        if poster.exists():
            print(f"  Falling back to {poster}")
            subprocess.run([sys.executable, str(poster)], check=True)
        else:
            print("❌ No pipeline available")


def main():
    parser = argparse.ArgumentParser(description="Content Kingdom CLI")
    parser.add_argument("--phase", help="Run specific phase")
    parser.add_argument("--stats", action="store_true", help="Show learning stats")
    parser.add_argument("--rules", action="store_true", help="Show active rules")
    parser.add_argument("--rules-category", help="Filter rules by category")
    parser.add_argument("--guidelines", action="store_true", help="Show design/copy guidelines")
    parser.add_argument("--bootstrap", action="store_true", help="Bootstrap training data")
    parser.add_argument("--feedback", help="Add manual feedback")
    parser.add_argument("--feedback-source", default="user", help="Feedback source")
    
    args = parser.parse_args()
    
    if args.stats:
        cmd_stats()
    elif args.rules or args.rules_category:
        cmd_rules(args.rules_category)
    elif args.guidelines:
        cmd_guidelines()
    elif args.bootstrap:
        cmd_bootstrap()
    elif args.feedback:
        cmd_feedback(args.feedback, args.feedback_source)
    elif args.phase:
        print(f"Running phase: {args.phase}")
        if args.phase == "post":
            cmd_pipeline()
        elif args.phase == "learn":
            cmd_stats()
        else:
            try:
                from orchestrator import run_phase
                run_phase(args.phase)
            except ImportError:
                print(f"❌ Phase '{args.phase}' not available in standalone mode")
    else:
        cmd_pipeline()


if __name__ == "__main__":
    main()
