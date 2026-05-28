"""
Module 4: AnalyticsEngine — PostBridge analytics, reports, recommendations.
Single Responsibility: analytics and reporting only. No posting, no scheduling.

Credentials imported from: autopilot_affiliate_engine/config.py
  → POSTBRIDGE_API_KEY, POSTBRIDGE_BASE_URL (not re-declared here)

PostBridge endpoints:
  GET  /v1/analytics      — views, likes, comments, shares per post
  POST /v1/analytics/sync — trigger platform data refresh
  GET  /v1/posts          — list posts
  GET  /v1/post-results   — per-post success/failure
"""

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

import json
from datetime import datetime, timedelta, timezone

import requests

from autopilot_affiliate_engine.config import POSTBRIDGE_API_KEY, POSTBRIDGE_BASE_URL

try:
    from .base import BaseModule
except ImportError:
    from base import BaseModule  # standalone

WIB = timezone(timedelta(hours=7))


class AnalyticsEngine(BaseModule):
    """Fetch, aggregate, and report on PostBridge post analytics."""

    def __init__(self, config: dict):
        super().__init__(config)
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {POSTBRIDGE_API_KEY}",
            "Content-Type": "application/json",
        })
        self._base = POSTBRIDGE_BASE_URL.rstrip("/")

    # ── Data fetching ─────────────────────────────────────────────────────

    def sync_analytics(self) -> dict:
        """Trigger PostBridge analytics sync. Returns API response."""
        resp = self._session.post(f"{self._base}/analytics/sync", timeout=15)
        resp.raise_for_status()
        return resp.json()

    def get_post_performance(self, days: int = 7) -> list[dict]:
        """
        Posts from last `days` days, enriched with analytics fields.
        Joins /posts with /analytics on post id.
        """
        cutoff = datetime.now(WIB) - timedelta(days=days)
        posts = self._fetch("posts")
        analytics_idx = {
            (a.get("post_id") or a.get("id")): a
            for a in self._fetch("analytics")
            if a.get("post_id") or a.get("id")
        }

        result = []
        for post in posts:
            ts = post.get("scheduled_at") or post.get("created_at", "")
            try:
                if datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(WIB) < cutoff:
                    continue
            except (ValueError, AttributeError):
                pass
            result.append({**post, **analytics_idx.get(post.get("id"), {})})
        return result

    # ── Reports ───────────────────────────────────────────────────────────

    def generate_daily_report(self) -> str:
        """Formatted markdown report for today's posts."""
        posts  = self.get_post_performance(days=1)
        totals = self._agg(posts)
        today  = datetime.now(WIB).strftime("%Y-%m-%d")

        lines = [
            f"# Daily Analytics — {today}",
            f"Posts: **{len(posts)}**",
            "",
            "| Metric   | Total |",
            "|----------|-------|",
            f"| Views    | {totals['views']:,} |",
            f"| Likes    | {totals['likes']:,} |",
            f"| Comments | {totals['comments']:,} |",
            f"| Shares   | {totals['shares']:,} |",
        ]
        if posts:
            top = max(posts, key=lambda p: p.get("views") or p.get("view_count") or 0)
            lines += ["", f"**Top post:** {str(top.get('caption',''))[:80]}…"]
        return "\n".join(lines)

    def generate_weekly_report(self) -> str:
        """Formatted markdown weekly summary with platform breakdown."""
        posts  = self.get_post_performance(days=7)
        totals = self._agg(posts)
        end    = datetime.now(WIB).strftime("%Y-%m-%d")
        start  = (datetime.now(WIB) - timedelta(days=7)).strftime("%Y-%m-%d")

        by_plat: dict[str, dict] = {}
        for p in posts:
            pl = p.get("platform", "unknown")
            d  = by_plat.setdefault(pl, {"posts": 0, "views": 0})
            d["posts"] += 1
            d["views"] += p.get("views") or p.get("view_count") or 0

        lines = [
            f"# Weekly Analytics — {start} → {end}",
            f"Total posts: **{len(posts)}**",
            "",
            "## Totals",
            f"- Views: **{totals['views']:,}**",
            f"- Likes: **{totals['likes']:,}**",
            f"- Comments: **{totals['comments']:,}**",
            f"- Shares: **{totals['shares']:,}**",
            "",
            "## By Platform",
        ] + [
            f"- **{pl}**: {d['posts']} posts · {d['views']:,} views"
            for pl, d in sorted(by_plat.items())
        ] + [""]

        lines += self.recommend_actions()
        return "\n".join(lines)

    # ── Winners / Losers ──────────────────────────────────────────────────

    def identify_winners(self, top_n: int = 5) -> list[dict]:
        """Top N posts by view count."""
        return sorted(
            self.get_post_performance(days=7),
            key=lambda p: p.get("views") or p.get("view_count") or 0,
            reverse=True,
        )[:top_n]

    def identify_losers(self, bottom_n: int = 5) -> list[dict]:
        """Bottom N posts by view count."""
        return sorted(
            self.get_post_performance(days=7),
            key=lambda p: p.get("views") or p.get("view_count") or 0,
        )[:bottom_n]

    # ── Insights ──────────────────────────────────────────────────────────

    def recommend_actions(self) -> list[str]:
        """Data-driven recommendations as a list of strings."""
        posts = self.get_post_performance(days=7)
        if not posts:
            return ["⚠️ No post data — run sync_analytics() first."]

        totals = self._agg(posts)
        recs = ["## Recommendations"]

        eng_rate = (totals["likes"] + totals["comments"] + totals["shares"]) / max(totals["views"], 1) * 100
        if eng_rate < 3:
            recs.append(f"- 🔴 Engagement rate {eng_rate:.1f}% LOW — add stronger CTAs and questions.")
        elif eng_rate > 8:
            recs.append(f"- 🟢 Engagement rate {eng_rate:.1f}% STRONG — double down on this style.")

        by_plat: dict[str, int] = {}
        for p in posts:
            by_plat[p.get("platform", "?")] = by_plat.get(p.get("platform", "?"), 0) + 1
        if by_plat:
            top = max(by_plat, key=by_plat.get)
            recs.append(f"- 📊 Most active: **{top}** ({by_plat[top]} posts).")

        if len(posts) < 7:
            recs.append("- 📉 Less than 1 post/day — increase frequency.")

        return recs

    def get_funnel_metrics(self) -> dict:
        """Views → Clicks → Sales funnel. Clicks from post-results; sales placeholder."""
        posts   = self.get_post_performance(days=7)
        results = self._fetch("post-results")

        views  = sum(p.get("views") or p.get("view_count") or 0 for p in posts)
        clicks = sum(r.get("clicks") or 0 for r in results)
        sales  = 0  # hook up LYNK API separately

        return {
            "views":   views,
            "clicks":  clicks,
            "sales":   sales,
            "ctr_pct": round(clicks / max(views, 1) * 100, 2),
            "cvr_pct": round(sales  / max(clicks, 1) * 100, 2),
        }

    def export_report(self, fmt: str = "markdown") -> str:
        """Export weekly report as markdown or json."""
        if fmt == "json":
            posts = self.get_post_performance(days=7)
            return json.dumps({
                "generated_at": datetime.now(WIB).isoformat(),
                "totals": self._agg(posts),
                "funnel": self.get_funnel_metrics(),
                "posts": posts,
            }, ensure_ascii=False, indent=2)
        return self.generate_weekly_report()

    # ── Private ───────────────────────────────────────────────────────────

    def _fetch(self, endpoint: str) -> list[dict]:
        try:
            resp = self._session.get(f"{self._base}/{endpoint}", timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else data.get("data", [])
        except requests.RequestException as e:
            print(f"[AnalyticsEngine] /{endpoint} failed: {e}")
            return []

    def _agg(self, posts: list[dict]) -> dict:
        return {
            "views":    sum(p.get("views")    or p.get("view_count")    or 0 for p in posts),
            "likes":    sum(p.get("likes")    or p.get("like_count")    or 0 for p in posts),
            "comments": sum(p.get("comments") or p.get("comment_count") or 0 for p in posts),
            "shares":   sum(p.get("shares")   or p.get("share_count")   or 0 for p in posts),
        }


# ── Self-test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from base import load_config  # noqa (standalone)

    cfg = load_config()
    engine = AnalyticsEngine(cfg)

    print("=== Syncing analytics ===")
    try:
        result = engine.sync_analytics()
        print(f"  Response: {str(result)[:120]}")
    except Exception as e:
        print(f"  (sync failed — likely auth/network in dev): {e}")

    print("\n=== Post performance (7 days) ===")
    posts = engine.get_post_performance(days=7)
    print(f"  Posts returned: {len(posts)}")

    print("\n=== Daily Report ===")
    print(engine.generate_daily_report())

    print("\n=== Funnel Metrics ===")
    for k, v in engine.get_funnel_metrics().items():
        print(f"  {k}: {v}")

    print("\n=== Top 3 Winners ===")
    for i, w in enumerate(engine.identify_winners(3), 1):
        views = w.get("views") or w.get("view_count") or 0
        print(f"  {i}. {views:,} views — {str(w.get('caption',''))[:50]}")

    print("\n=== Recommendations ===")
    for rec in engine.recommend_actions():
        print(f"  {rec}")

    print("\n✅ analytics_engine self-test complete")
