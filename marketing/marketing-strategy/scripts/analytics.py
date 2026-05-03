#!/usr/bin/env python3
"""
analytics.py — Social media performance analytics tracker.

Features:
  - Track post performance over time (engagement, reach, saves, shares)
  - Identify top content patterns (format, length, topic, posting time)
  - Weekly performance report generator
  - Optimal posting time detection per platform
  - Content scoring and pattern recognition

Usage:
    python3 analytics.py record --post-id abc123 --platform instagram --likes 450 --comments 32
    python3 analytics.py report --week          # This week's report
    python3 analytics.py report --compare       # This week vs last
    python3 analytics.py best-times --platform twitter
    python3 analytics.py patterns               # Top content patterns
    python3 analytics.py dashboard              # Full dashboard
"""

import json
import os
import sys
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Optional
from statistics import mean, stdev

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_DIR       = Path(__file__).parent.parent / "data"
ANALYTICS_FILE = DATA_DIR / "analytics.json"
LOG_FILE       = DATA_DIR / "analytics.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("analytics")


# ─── Data Model ───────────────────────────────────────────────────────────────

def empty_store() -> dict:
    return {
        "posts": {},          # post_id -> PostRecord
        "weekly_snapshots": {},  # "YYYY-WNN" -> WeeklySnapshot
        "settings": {
            "platforms": ["twitter", "instagram", "tiktok", "linkedin"],
            "target_engagement_rate": 0.05,
        },
    }


def post_record(
    post_id: str,
    platform: str,
    content: str = "",
    content_type: str = "image",  # image, video, text, reel, story, thread
    topic: str = "",
    hashtags: list = None,
    posted_at: str = None,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    saves: int = 0,
    views: int = 0,
    reach: int = 0,
    follower_count: int = 0,
    link_clicks: int = 0,
) -> dict:
    return {
        "post_id":       post_id,
        "platform":      platform,
        "content":       content,
        "content_type":  content_type,
        "topic":         topic,
        "hashtags":      hashtags or [],
        "posted_at":     posted_at or datetime.now().isoformat(),
        "metrics": {
            "likes":         likes,
            "comments":      comments,
            "shares":        shares,
            "saves":         saves,
            "views":         views,
            "reach":         reach,
            "follower_count": follower_count,
            "link_clicks":   link_clicks,
        },
        "computed": {},  # filled in on read
        "recorded_at": datetime.now().isoformat(),
    }


# ─── Analytics Store ──────────────────────────────────────────────────────────

class AnalyticsStore:
    def __init__(self, path: Path = ANALYTICS_FILE):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return empty_store()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def record_post(self, record: dict) -> dict:
        """Store a post record, computing derived metrics."""
        record["computed"] = self._compute_metrics(record)
        self.data["posts"][record["post_id"]] = record
        self._save()
        log.info(f"📊 Recorded {record['platform']} post {record['post_id']}")
        return record

    def _compute_metrics(self, record: dict) -> dict:
        m    = record["metrics"]
        fc   = m.get("follower_count", 0)
        reach = m.get("reach", 0) or fc

        total_engagement = (
            m["likes"] + m["comments"] * 2 + m["shares"] * 3 + m["saves"] * 2
        )
        engagement_rate = round(total_engagement / reach, 4) if reach > 0 else 0

        # Content length score
        content = record.get("content", "")
        content_len = len(content.split())
        if content_len < 10:
            length_bucket = "micro"
        elif content_len < 50:
            length_bucket = "short"
        elif content_len < 150:
            length_bucket = "medium"
        else:
            length_bucket = "long"

        # Hour of day posted
        try:
            dt   = datetime.fromisoformat(record["posted_at"])
            hour = dt.hour
            dow  = dt.strftime("%A")  # Monday, Tuesday, ...
        except Exception:
            hour = 12
            dow  = "Unknown"

        # Overall content score (0-100)
        content_score = min(100, int(engagement_rate * 1000))

        return {
            "total_engagement":  total_engagement,
            "engagement_rate":   engagement_rate,
            "content_score":     content_score,
            "length_bucket":     length_bucket,
            "posted_hour":       hour,
            "posted_dow":        dow,
            "hashtag_count":     len(record.get("hashtags", [])),
        }

    def get_posts(
        self,
        platform: str = None,
        since: datetime = None,
        until: datetime = None,
    ) -> list[dict]:
        posts = list(self.data["posts"].values())
        if platform:
            posts = [p for p in posts if p["platform"] == platform]
        if since:
            posts = [p for p in posts if datetime.fromisoformat(p["posted_at"]) >= since]
        if until:
            posts = [p for p in posts if datetime.fromisoformat(p["posted_at"]) <= until]
        return posts

    def update_metrics(self, post_id: str, **metrics):
        """Update metrics for an existing post (e.g., refresh after 24h)."""
        if post_id not in self.data["posts"]:
            log.error(f"Post {post_id} not found")
            return
        for k, v in metrics.items():
            if k in self.data["posts"][post_id]["metrics"]:
                self.data["posts"][post_id]["metrics"][k] = v
        self.data["posts"][post_id]["computed"] = self._compute_metrics(
            self.data["posts"][post_id]
        )
        self._save()


# ─── Reporting Engine ─────────────────────────────────────────────────────────

class ReportGenerator:
    def __init__(self, store: AnalyticsStore):
        self.store = store

    # ── Helper: week boundaries ─────────────────────────────────────────────

    @staticmethod
    def _week_range(offset: int = 0) -> tuple[datetime, datetime]:
        """Return (start, end) for the week at `offset` weeks from now (0 = current)."""
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday()) - timedelta(weeks=offset)
        end   = start + timedelta(days=6)
        return (
            datetime.combine(start, datetime.min.time()),
            datetime.combine(end,   datetime.max.time()),
        )

    # ── Top Posts ────────────────────────────────────────────────────────────

    def top_posts(self, posts: list[dict], n: int = 5, by: str = "engagement_rate") -> list[dict]:
        """Return top N posts sorted by metric."""
        return sorted(
            posts,
            key=lambda p: p.get("computed", {}).get(by, 0),
            reverse=True,
        )[:n]

    # ── Optimal Posting Times ────────────────────────────────────────────────

    def optimal_posting_times(self, platform: str = None) -> dict:
        """Identify best hours/days to post based on historical data."""
        posts = self.store.get_posts(platform=platform)
        if len(posts) < 5:
            return {"error": "Not enough data (need 5+ posts). Keep recording!"}

        # Group by hour and day
        hour_scores  = defaultdict(list)
        dow_scores   = defaultdict(list)

        for p in posts:
            comp = p.get("computed", {})
            er   = comp.get("engagement_rate", 0)
            hour_scores[comp.get("posted_hour", 12)].append(er)
            dow_scores[comp.get("posted_dow", "Unknown")].append(er)

        best_hours = sorted(
            [(h, round(mean(scores), 4)) for h, scores in hour_scores.items()],
            key=lambda x: x[1], reverse=True,
        )
        best_days = sorted(
            [(d, round(mean(scores), 4)) for d, scores in dow_scores.items()],
            key=lambda x: x[1], reverse=True,
        )

        return {
            "platform": platform or "all",
            "best_hours": [{"hour": f"{h:02d}:00", "avg_er": er} for h, er in best_hours[:3]],
            "best_days":  [{"day": d, "avg_er": er} for d, er in best_days[:3]],
            "worst_hours":[{"hour": f"{h:02d}:00", "avg_er": er} for h, er in best_hours[-2:]],
            "data_points": len(posts),
        }

    # ── Content Patterns ─────────────────────────────────────────────────────

    def content_patterns(self, platform: str = None) -> dict:
        """Identify which content types, topics, lengths perform best."""
        posts = self.store.get_posts(platform=platform)
        if len(posts) < 3:
            return {"error": "Need 3+ posts for pattern analysis"}

        def group_avg(posts: list[dict], key: str) -> list[dict]:
            groups = defaultdict(list)
            for p in posts:
                val = p.get("computed", {}).get(key) or p.get(key, "unknown")
                groups[val].append(p.get("computed", {}).get("engagement_rate", 0))
            return sorted(
                [{"value": v, "avg_er": round(mean(scores), 4), "count": len(scores)}
                 for v, scores in groups.items()],
                key=lambda x: x["avg_er"], reverse=True,
            )

        type_perf    = group_avg(posts, "content_type")
        length_perf  = group_avg(posts, "length_bucket")

        # Topic performance (based on topic field)
        topic_groups = defaultdict(list)
        for p in posts:
            topic = p.get("topic", "untagged")
            topic_groups[topic].append(p.get("computed", {}).get("engagement_rate", 0))
        topic_perf = sorted(
            [{"topic": t, "avg_er": round(mean(s), 4), "count": len(s)}
             for t, s in topic_groups.items()],
            key=lambda x: x["avg_er"], reverse=True,
        )

        # Hashtag count analysis
        hashtag_groups = defaultdict(list)
        for p in posts:
            hc = p.get("computed", {}).get("hashtag_count", 0)
            bucket = f"{(hc // 5) * 5}-{(hc // 5) * 5 + 4}"
            hashtag_groups[bucket].append(p.get("computed", {}).get("engagement_rate", 0))
        hashtag_perf = sorted(
            [{"hashtag_range": b, "avg_er": round(mean(s), 4), "count": len(s)}
             for b, s in hashtag_groups.items()],
            key=lambda x: x["avg_er"], reverse=True,
        )

        return {
            "platform":     platform or "all",
            "by_type":      type_perf,
            "by_length":    length_perf,
            "by_topic":     topic_perf,
            "by_hashtags":  hashtag_perf,
            "total_posts":  len(posts),
        }

    # ── Weekly Report ────────────────────────────────────────────────────────

    def weekly_report(self, offset: int = 0, platform: str = None) -> dict:
        """Generate weekly performance report."""
        start, end = self._week_range(offset)
        week_label = start.strftime("Week of %b %d, %Y")

        posts = self.store.get_posts(platform=platform, since=start, until=end)

        if not posts:
            return {
                "week": week_label,
                "error": "No posts recorded for this week",
                "tip": "Start recording posts with: analytics.py record ...",
            }

        # Aggregate metrics
        total_likes    = sum(p["metrics"]["likes"]    for p in posts)
        total_comments = sum(p["metrics"]["comments"] for p in posts)
        total_shares   = sum(p["metrics"]["shares"]   for p in posts)
        total_saves    = sum(p["metrics"]["saves"]    for p in posts)
        total_reach    = sum(p["metrics"]["reach"]    for p in posts)
        total_clicks   = sum(p["metrics"]["link_clicks"] for p in posts)

        avg_er         = round(mean(p["computed"].get("engagement_rate", 0) for p in posts), 4)
        best_posts     = self.top_posts(posts, n=3)

        # Platform breakdown
        platform_breakdown = defaultdict(lambda: {"posts": 0, "total_engagement": 0, "avg_er": []})
        for p in posts:
            pl = p["platform"]
            platform_breakdown[pl]["posts"] += 1
            platform_breakdown[pl]["total_engagement"] += p["computed"].get("total_engagement", 0)
            platform_breakdown[pl]["avg_er"].append(p["computed"].get("engagement_rate", 0))

        for pl in platform_breakdown:
            ers = platform_breakdown[pl]["avg_er"]
            platform_breakdown[pl]["avg_er"] = round(mean(ers), 4) if ers else 0

        # Content type breakdown
        type_breakdown = defaultdict(int)
        for p in posts:
            type_breakdown[p.get("content_type", "unknown")] += 1

        report = {
            "week":         week_label,
            "period":       {"from": start.strftime("%Y-%m-%d"), "to": end.strftime("%Y-%m-%d")},
            "summary": {
                "total_posts":    len(posts),
                "total_likes":    total_likes,
                "total_comments": total_comments,
                "total_shares":   total_shares,
                "total_saves":    total_saves,
                "total_reach":    total_reach,
                "total_clicks":   total_clicks,
                "avg_engagement_rate": f"{avg_er:.1%}",
            },
            "top_posts": [
                {
                    "post_id":        p["post_id"],
                    "platform":       p["platform"],
                    "content_type":   p["content_type"],
                    "topic":          p.get("topic", ""),
                    "likes":          p["metrics"]["likes"],
                    "comments":       p["metrics"]["comments"],
                    "engagement_rate": f"{p['computed'].get('engagement_rate', 0):.1%}",
                    "content_score":  p["computed"].get("content_score", 0),
                }
                for p in best_posts
            ],
            "platform_breakdown": dict(platform_breakdown),
            "content_type_breakdown": dict(type_breakdown),
            "optimal_times":    self.optimal_posting_times(platform=platform),
        }

        # Comparison to previous week
        prev_start, prev_end = self._week_range(offset + 1)
        prev_posts = self.store.get_posts(platform=platform, since=prev_start, until=prev_end)
        if prev_posts:
            prev_er = mean(p["computed"].get("engagement_rate", 0) for p in prev_posts)
            er_delta = avg_er - prev_er
            report["week_over_week"] = {
                "prev_posts":    len(prev_posts),
                "prev_avg_er":   f"{prev_er:.1%}",
                "er_change":     f"{'+' if er_delta >= 0 else ''}{er_delta:.1%}",
                "posts_change":  len(posts) - len(prev_posts),
            }

        return report

    # ── Dashboard ────────────────────────────────────────────────────────────

    def dashboard(self, platform: str = None) -> str:
        """Generate a full text dashboard."""
        report   = self.weekly_report(0, platform=platform)
        patterns = self.content_patterns(platform=platform)
        times    = self.optimal_posting_times(platform=platform)

        lines = [
            "=" * 60,
            f"📊 ANALYTICS DASHBOARD — {report.get('week', 'This Week')}",
            "=" * 60,
        ]

        # Summary
        s = report.get("summary", {})
        lines += [
            "\n📈 WEEKLY SUMMARY",
            f"  Posts:          {s.get('total_posts', 0)}",
            f"  Total Likes:    {s.get('total_likes', 0):,}",
            f"  Total Comments: {s.get('total_comments', 0):,}",
            f"  Total Shares:   {s.get('total_shares', 0):,}",
            f"  Total Saves:    {s.get('total_saves', 0):,}",
            f"  Total Reach:    {s.get('total_reach', 0):,}",
            f"  Avg Eng. Rate:  {s.get('avg_engagement_rate', 'N/A')}",
        ]

        # WoW
        wow = report.get("week_over_week")
        if wow:
            lines += [
                "\n📅 WEEK-OVER-WEEK",
                f"  Engagement Rate: {wow.get('er_change', 'N/A')}",
                f"  Posts: {'+' if wow['posts_change'] >= 0 else ''}{wow['posts_change']}",
            ]

        # Top posts
        top = report.get("top_posts", [])
        if top:
            lines.append("\n🏆 TOP POSTS THIS WEEK")
            for i, p in enumerate(top, 1):
                lines.append(f"  {i}. [{p['platform']}] {p.get('topic', p['post_id'])} — {p['engagement_rate']} ER")

        # Best times
        if "best_hours" in times:
            lines.append("\n⏰ BEST POSTING TIMES")
            for t in times.get("best_hours", []):
                lines.append(f"  {t['hour']} → avg ER {t['avg_er']:.1%}")
            for d in times.get("best_days", []):
                lines.append(f"  {d['day']} → avg ER {d['avg_er']:.1%}")

        # Content patterns
        if "by_type" in patterns:
            lines.append("\n🎯 CONTENT PATTERNS")
            lines.append("  By Type:")
            for t in patterns.get("by_type", [])[:3]:
                lines.append(f"    {t['value']}: {t['avg_er']:.1%} avg ER ({t['count']} posts)")
            lines.append("  By Length:")
            for t in patterns.get("by_length", [])[:3]:
                lines.append(f"    {t['value']}: {t['avg_er']:.1%} avg ER")
            lines.append("  By Topic:")
            for t in patterns.get("by_topic", [])[:3]:
                lines.append(f"    {t['topic']}: {t['avg_er']:.1%} avg ER")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


# ─── Seed Demo Data ───────────────────────────────────────────────────────────

def seed_demo_data(store: AnalyticsStore):
    """Populate store with demo data for testing."""
    import random

    platforms     = ["instagram", "twitter", "tiktok"]
    content_types = ["image", "video", "reel", "text", "story"]
    topics        = ["productivity", "mindset", "finance", "tools", "story"]
    hours         = [7, 8, 9, 12, 17, 18, 19, 20, 21]

    log.info("🌱 Seeding demo data (30 posts)...")
    for i in range(30):
        platform     = random.choice(platforms)
        content_type = random.choice(content_types)
        topic        = random.choice(topics)
        hour         = random.choice(hours)
        fc           = random.randint(1000, 50000)
        likes        = random.randint(10, int(fc * 0.1))
        comments     = random.randint(2, int(likes * 0.15))
        shares       = random.randint(0, int(likes * 0.05))
        saves        = random.randint(0, int(likes * 0.08))
        views        = random.randint(likes * 3, likes * 20)
        reach        = random.randint(fc // 2, fc * 2)
        days_ago     = random.randint(0, 28)
        posted_at    = (datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))).replace(hour=hour).isoformat()

        record = post_record(
            post_id      = f"demo_{platform}_{i:03d}",
            platform     = platform,
            content_type = content_type,
            topic        = topic,
            content      = f"Sample {topic} post #{i} — {'short' if i % 2 == 0 else 'This is a longer post with more content to fill the medium bucket for analysis purposes'}",
            hashtags     = [f"#{topic}", "#growth"] if random.random() > 0.3 else [],
            posted_at    = posted_at,
            likes        = likes,
            comments     = comments,
            shares       = shares,
            saves        = saves,
            views        = views,
            reach        = reach,
            follower_count = fc,
            link_clicks  = random.randint(0, int(likes * 0.02)),
        )
        store.record_post(record)
    log.info("✅ Demo data seeded")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analytics — Track and report social media performance")
    sub    = parser.add_subparsers(dest="cmd")

    # record
    p_rec = sub.add_parser("record", help="Record a post's metrics")
    p_rec.add_argument("--post-id",      required=True)
    p_rec.add_argument("--platform",     required=True)
    p_rec.add_argument("--content",      default="")
    p_rec.add_argument("--content-type", default="image",
                       choices=["image", "video", "reel", "text", "story", "thread", "carousel"])
    p_rec.add_argument("--topic",        default="")
    p_rec.add_argument("--hashtags",     default="", help="Comma-separated hashtags")
    p_rec.add_argument("--likes",        type=int, default=0)
    p_rec.add_argument("--comments",     type=int, default=0)
    p_rec.add_argument("--shares",       type=int, default=0)
    p_rec.add_argument("--saves",        type=int, default=0)
    p_rec.add_argument("--views",        type=int, default=0)
    p_rec.add_argument("--reach",        type=int, default=0)
    p_rec.add_argument("--followers",    type=int, default=0)
    p_rec.add_argument("--clicks",       type=int, default=0)
    p_rec.add_argument("--posted-at",    default=None, help="ISO datetime of post (default: now)")

    # update
    p_upd = sub.add_parser("update", help="Update metrics for existing post")
    p_upd.add_argument("--post-id", required=True)
    p_upd.add_argument("--likes",   type=int)
    p_upd.add_argument("--comments",type=int)
    p_upd.add_argument("--shares",  type=int)
    p_upd.add_argument("--saves",   type=int)
    p_upd.add_argument("--views",   type=int)
    p_upd.add_argument("--reach",   type=int)

    # report
    p_rep = sub.add_parser("report", help="Generate weekly report")
    p_rep.add_argument("--week",    action="store_true", help="This week (default)")
    p_rep.add_argument("--last",    action="store_true", help="Last week")
    p_rep.add_argument("--compare", action="store_true", help="Compare this week vs last")
    p_rep.add_argument("--platform", default=None)

    # best-times
    p_bt = sub.add_parser("best-times", help="Optimal posting time analysis")
    p_bt.add_argument("--platform", default=None)

    # patterns
    p_pat = sub.add_parser("patterns", help="Content pattern analysis")
    p_pat.add_argument("--platform", default=None)

    # dashboard
    p_dash = sub.add_parser("dashboard", help="Full analytics dashboard")
    p_dash.add_argument("--platform", default=None)

    # demo
    sub.add_parser("demo", help="Seed demo data for testing")

    args = parser.parse_args()
    store = AnalyticsStore()
    gen   = ReportGenerator(store)

    if args.cmd == "record":
        record = post_record(
            post_id       = args.post_id,
            platform      = args.platform,
            content       = args.content,
            content_type  = args.content_type,
            topic         = args.topic,
            hashtags      = [h.strip() for h in args.hashtags.split(",") if h.strip()],
            posted_at     = args.posted_at,
            likes         = args.likes,
            comments      = args.comments,
            shares        = args.shares,
            saves         = args.saves,
            views         = args.views,
            reach         = args.reach,
            follower_count= args.followers,
            link_clicks   = args.clicks,
        )
        result = store.record_post(record)
        computed = result["computed"]
        print(f"✅ Recorded post {args.post_id}")
        print(f"   Engagement Rate: {computed['engagement_rate']:.1%}")
        print(f"   Content Score:   {computed['content_score']}/100")
        print(f"   Posted:          {computed['posted_dow']} at {computed['posted_hour']:02d}:00")

    elif args.cmd == "update":
        updates = {k: v for k, v in {
            "likes":    args.likes,
            "comments": args.comments,
            "shares":   args.shares,
            "saves":    args.saves,
            "views":    args.views,
            "reach":    args.reach,
        }.items() if v is not None}
        store.update_metrics(args.post_id, **updates)
        print(f"✅ Updated {args.post_id}")

    elif args.cmd == "report":
        if args.compare:
            r0 = gen.weekly_report(0, platform=args.platform)
            r1 = gen.weekly_report(1, platform=args.platform)
            print(json.dumps({"this_week": r0, "last_week": r1}, indent=2))
        elif args.last:
            print(json.dumps(gen.weekly_report(1, platform=args.platform), indent=2))
        else:
            print(json.dumps(gen.weekly_report(0, platform=args.platform), indent=2))

    elif args.cmd == "best-times":
        result = gen.optimal_posting_times(platform=args.platform)
        print(json.dumps(result, indent=2))

    elif args.cmd == "patterns":
        result = gen.content_patterns(platform=args.platform)
        print(json.dumps(result, indent=2))

    elif args.cmd == "dashboard":
        print(gen.dashboard(platform=args.platform))

    elif args.cmd == "demo":
        seed_demo_data(store)
        print(gen.dashboard())

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
