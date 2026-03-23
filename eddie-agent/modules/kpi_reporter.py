"""
KPI Reporter
Pulls analytics from PostBridge, generates markdown KPI reports.
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, List, Any

logger = logging.getLogger("eddie.kpi")


class KPIReporter:
    """Fetch analytics and generate formatted KPI markdown reports."""

    def __init__(self, config: dict, postbridge_client):
        self.config = config
        self.pb = postbridge_client
        self.accounts = config.get("accounts", {})
        report_dir = config.get("kpi", {}).get(
            "report_output_dir",
            str(Path(__file__).parent.parent / "reports")
        )
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def _get_all_account_ids(self) -> List[str]:
        ids = []
        for platform_accounts in self.accounts.values():
            for acc in platform_accounts:
                ids.append(str(acc["id"]))
        return ids

    def _get_accounts_by_platform(self) -> Dict[str, List[dict]]:
        return self.accounts

    def pull_analytics(self, days_back: int = 7) -> Dict[str, Any]:
        """
        Pull analytics for all accounts for the last N days.
        Returns structured analytics data.
        """
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=days_back)
        start_date = start.strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")

        logger.info(f"Pulling analytics {start_date} → {end_date}")

        # Trigger sync first
        try:
            self.pb.sync_analytics()
            logger.info("Analytics sync triggered")
        except Exception as e:
            logger.warning(f"Analytics sync failed (non-critical): {e}")

        # Pull overall analytics
        try:
            raw = self.pb.get_analytics(start_date=start_date, end_date=end_date)
        except Exception as e:
            logger.error(f"Failed to pull analytics: {e}")
            return {"error": str(e), "period": f"{start_date} to {end_date}"}

        return {
            "period": {"start": start_date, "end": end_date, "days": days_back},
            "raw": raw,
            "pulled_at": now.isoformat()
        }

    def pull_post_results(self) -> Dict[str, Any]:
        """Pull recent post success/failure data."""
        logger.info("Pulling post results...")
        try:
            results = self.pb.get_post_results(limit=100)
            failed = [r for r in results if r.get("status") == "failed"]
            success = [r for r in results if r.get("status") in ("published", "success", "sent")]
            pending = [r for r in results if r.get("status") in ("pending", "scheduled")]

            return {
                "total": len(results),
                "success": len(success),
                "failed": len(failed),
                "pending": len(pending),
                "success_rate": round(len(success) / len(results) * 100, 1) if results else 0,
                "failed_posts": failed[:10],  # Cap to avoid giant reports
                "raw": results
            }
        except Exception as e:
            logger.error(f"Failed to pull post results: {e}")
            return {"error": str(e)}

    def _extract_summary_metrics(self, analytics: dict) -> dict:
        """Extract key metrics from raw analytics response."""
        raw = analytics.get("raw", {})
        if not raw or "error" in analytics:
            return {"error": analytics.get("error", "No data")}

        # Handle both list and dict response shapes
        if isinstance(raw, list):
            total_views = sum(item.get("views", 0) for item in raw)
            total_likes = sum(item.get("likes", 0) for item in raw)
            total_comments = sum(item.get("comments", 0) for item in raw)
            total_shares = sum(item.get("shares", 0) for item in raw)
            total_reach = sum(item.get("reach", 0) for item in raw)
        elif isinstance(raw, dict):
            data = raw.get("data", raw)
            if isinstance(data, list):
                total_views = sum(item.get("views", 0) for item in data)
                total_likes = sum(item.get("likes", 0) for item in data)
                total_comments = sum(item.get("comments", 0) for item in data)
                total_shares = sum(item.get("shares", 0) for item in data)
                total_reach = sum(item.get("reach", 0) for item in data)
            else:
                total_views = data.get("total_views", 0)
                total_likes = data.get("total_likes", 0)
                total_comments = data.get("total_comments", 0)
                total_shares = data.get("total_shares", 0)
                total_reach = data.get("total_reach", 0)
        else:
            return {"error": "Unexpected analytics format"}

        total_engagement = total_likes + total_comments + total_shares
        engagement_rate = round(total_engagement / total_views * 100, 2) if total_views > 0 else 0

        return {
            "views": total_views,
            "likes": total_likes,
            "comments": total_comments,
            "shares": total_shares,
            "reach": total_reach,
            "total_engagement": total_engagement,
            "engagement_rate_pct": engagement_rate
        }

    def generate_report(self, days_back: int = 7, save: bool = True) -> str:
        """
        Generate a full markdown KPI report.
        Returns the markdown string and optionally saves to file.
        """
        logger.info(f"Generating KPI report (last {days_back} days)")
        analytics = self.pull_analytics(days_back=days_back)
        post_results = self.pull_post_results()
        metrics = self._extract_summary_metrics(analytics)

        now_wib = datetime.now()
        report_date = now_wib.strftime("%Y-%m-%d %H:%M")

        # Build account table
        account_rows = []
        for platform, accounts in self._get_accounts_by_platform().items():
            for acc in accounts:
                account_rows.append(
                    f"| {platform.capitalize()} | {acc['label']} | {acc['id']} | "
                    f"{'✅' if acc.get('active') else '❌'} |"
                )
        account_table = "\n".join(account_rows)

        # Metrics section
        if "error" in metrics:
            metrics_section = f"> ⚠️ Analytics unavailable: {metrics['error']}"
        else:
            thresholds = self.config.get("kpi", {}).get("alert_thresholds", {})
            min_engagement = thresholds.get("min_engagement_rate", 0.02) * 100
            er_status = "✅" if metrics["engagement_rate_pct"] >= min_engagement else "⚠️"

            metrics_section = f"""| Metric | Value |
|--------|-------|
| 👁️ Total Views | {metrics['views']:,} |
| ❤️ Total Likes | {metrics['likes']:,} |
| 💬 Total Comments | {metrics['comments']:,} |
| 🔁 Total Shares | {metrics['shares']:,} |
| 📡 Total Reach | {metrics['reach']:,} |
| ⚡ Total Engagement | {metrics['total_engagement']:,} |
| 📊 Engagement Rate | {metrics['engagement_rate_pct']}% {er_status} |"""

        # Post results section
        if "error" in post_results:
            posts_section = f"> ⚠️ Post results unavailable: {post_results['error']}"
        else:
            sr_status = "✅" if post_results.get("success_rate", 0) >= 80 else "⚠️"
            posts_section = f"""| Status | Count |
|--------|-------|
| ✅ Published | {post_results.get('success', 0)} |
| ❌ Failed | {post_results.get('failed', 0)} |
| ⏳ Pending | {post_results.get('pending', 0)} |
| 📝 Total | {post_results.get('total', 0)} |
| 🎯 Success Rate | {post_results.get('success_rate', 0)}% {sr_status} |"""

        # Failed posts detail
        failed_detail = ""
        if post_results.get("failed_posts"):
            failed_rows = []
            for fp in post_results["failed_posts"][:5]:
                failed_rows.append(
                    f"| {fp.get('id', '-')} | {fp.get('platform', '-')} | "
                    f"{fp.get('error_message', fp.get('error', 'Unknown'))[:60]} |"
                )
            if failed_rows:
                failed_detail = f"""
### ❌ Failed Posts (Top 5)

| Post ID | Platform | Error |
|---------|----------|-------|
{chr(10).join(failed_rows)}
"""

        period = analytics.get("period", {})
        period_str = f"{period.get('start', 'N/A')} → {period.get('end', 'N/A')} ({period.get('days', days_back)} days)"

        md = f"""# 📊 Eddie KPI Report
**Generated:** {report_date} WIB
**Period:** {period_str}

---

## 🔗 Connected Accounts

| Platform | Label | ID | Active |
|----------|-------|----|--------|
{account_table}

**Total Accounts:** {sum(len(v) for v in self._get_accounts_by_platform().values())}

---

## 📈 Performance Metrics

{metrics_section}

---

## 📬 Post Publishing Results

{posts_section}
{failed_detail}

---

## 🎯 KPI Health Check

| Check | Status | Note |
|-------|--------|------|
| Analytics Data | {'✅ OK' if 'error' not in metrics else '❌ Failed'} | Period: {period_str} |
| Publishing Success | {'✅ OK' if post_results.get('success_rate', 0) >= 80 else '⚠️ Below 80%'} | Rate: {post_results.get('success_rate', 'N/A')}% |
| Engagement Rate | {'✅ OK' if "error" not in metrics and metrics.get("engagement_rate_pct", 0) >= 2.0 else '⚠️ Below 2%'} | Rate: {metrics.get('engagement_rate_pct', 'N/A')}% |

---
*Report by Eddie Agent v1.0 | BerkahKarya*
"""

        if save:
            filename = f"kpi_report_{now_wib.strftime('%Y-%m-%d_%H%M')}.md"
            report_path = self.report_dir / filename
            report_path.write_text(md, encoding="utf-8")
            logger.info(f"Report saved: {report_path}")

        return md
