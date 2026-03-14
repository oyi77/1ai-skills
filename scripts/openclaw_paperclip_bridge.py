#!/usr/bin/env python3
"""
OpenClaw ↔ Paperclip Bridge
Enables direct collaboration between OpenClaw (Vilona) and Paperclip agents.

Usage:
  python3 scripts/openclaw_paperclip_bridge.py status       # Show all agents + issues
  python3 scripts/openclaw_paperclip_bridge.py create       # Create issue from stdin/args
  python3 scripts/openclaw_paperclip_bridge.py sync         # Sync knowledge between systems
  python3 scripts/openclaw_paperclip_bridge.py analytics    # Share PostBridge analytics with Paperclip
"""

import json
import sys
import os
import requests
from datetime import datetime
from pathlib import Path

# Configuration
PCP_TOKEN = "pcp_0a284b0dd33364992dcbec9f46995cfaffc72fdedcf2621f"
COMPANY_ID = "33e1e20e-d9f2-45f2-b907-0579ab795942"
API_BASE = "http://localhost:3100/api"
PCP_KNOWLEDGE = Path(os.path.expanduser("~/.paperclip/instances/default/workspaces/2796c45e-aed9-48ce-b682-82beadcc9e6c/company-knowledge"))
OC_WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
OC_NOTES = OC_WORKSPACE / "notes"
OC_MEMORY = OC_WORKSPACE / "memory"

HEADERS = {
    "Authorization": f"Bearer {PCP_TOKEN}",
    "Content-Type": "application/json"
}

# PostBridge config
PB_API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
PB_BASE = "https://api.post-bridge.com/v1"
PB_HEADERS = {"Authorization": f"Bearer {PB_API_KEY}"}


def api_get(path):
    """GET from Paperclip API"""
    try:
        r = requests.get(f"{API_BASE}/companies/{COMPANY_ID}/{path}", headers=HEADERS, timeout=10)
        return r.json() if r.ok else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}


def api_post(path, data):
    """POST to Paperclip API"""
    try:
        r = requests.post(f"{API_BASE}/companies/{COMPANY_ID}/{path}", headers=HEADERS, json=data, timeout=10)
        return r.json() if r.ok else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}


def api_patch(path, data):
    """PATCH to Paperclip API"""
    try:
        r = requests.patch(f"{API_BASE}/companies/{COMPANY_ID}/{path}", headers=HEADERS, json=data, timeout=10)
        return r.json() if r.ok else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}


def get_status():
    """Get full status of Paperclip system"""
    print("=" * 60)
    print("🤖 PAPERCLIP STATUS")
    print("=" * 60)

    # Agents
    agents = api_get("agents")
    if isinstance(agents, list):
        print(f"\n📋 Agents ({len(agents)}):")
        for a in agents:
            status_icon = "🟢" if a.get("status") == "running" else "⚪"
            print(f"  {status_icon} {a.get('name', 'Unknown'):20s} | {a.get('role', 'N/A'):10s} | {a.get('status', 'unknown')}")

    # Issues
    issues = api_get("issues?limit=20")
    if isinstance(issues, list):
        active = [i for i in issues if i.get("status") in ("in_progress", "todo", "backlog")]
        done = [i for i in issues if i.get("status") == "done"]
        print(f"\n📌 Active Tasks ({len(active)}):")
        for i in active:
            priority_icon = "🔴" if i.get("priority") == "critical" else "🟡" if i.get("priority") == "high" else "⚪"
            print(f"  {priority_icon} [{i.get('status', '?'):12s}] {i.get('title', 'No title')[:70]}")

        print(f"\n✅ Completed Tasks: {len(done)}")

    print("\n" + "=" * 60)


def create_issue(title, description, priority="critical", assign_to=None):
    """Create a new issue in Paperclip"""
    data = {
        "title": title,
        "description": description,
        "priority": priority,
    }
    if assign_to:
        data["assigneeAgentId"] = assign_to

    result = api_post("issues", data)
    if "error" not in result:
        print(f"✅ Issue created: {result.get('id', 'unknown')[:8]}...")
        print(f"   Title: {title}")
        print(f"   Priority: {priority}")
        return result
    else:
        print(f"❌ Failed: {result.get('error', 'unknown error')}")
        return None


def sync_knowledge():
    """Sync critical knowledge between OpenClaw and Paperclip"""
    print("🔄 Syncing knowledge between OpenClaw ↔ Paperclip...")

    # 1. Write PostBridge API reference to Paperclip knowledge
    postbridge_ref = OC_NOTES / "postbridge-api-reference.md"
    if postbridge_ref.exists():
        dest = PCP_KNOWLEDGE / "resources" / "tool-guides" / "postbridge-api-reference.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(postbridge_ref.read_text())
        print(f"  ✅ PostBridge API reference → Paperclip knowledge")

    # 2. Write crisis status to Paperclip
    crisis_file = OC_NOTES / "crisis-status-2026-03-12.md"
    if crisis_file.exists():
        dest = PCP_KNOWLEDGE / "areas" / "finance" / "crisis-status-latest.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(crisis_file.read_text())
        print(f"  ✅ Crisis status → Paperclip finance area")

    # 3. Write financial status JSON
    fin_file = OC_MEMORY / "2026-03-12-financial-status.json"
    if fin_file.exists():
        dest = PCP_KNOWLEDGE / "areas" / "finance" / "financial-status-latest.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(fin_file.read_text())
        print(f"  ✅ Financial status JSON → Paperclip finance area")

    # 4. Read Paperclip's content strategy back to OpenClaw
    pcp_strategy = PCP_KNOWLEDGE.parent / "CONTENT_STRATEGY.md"
    if pcp_strategy.exists():
        dest = OC_NOTES / "paperclip-content-strategy.md"
        dest.write_text(pcp_strategy.read_text())
        print(f"  ✅ Paperclip content strategy → OpenClaw notes")

    # 5. Read Paperclip's marketing knowledge
    pcp_marketing = PCP_KNOWLEDGE / "areas" / "marketing"
    if pcp_marketing.exists():
        for f in pcp_marketing.glob("*.md"):
            dest = OC_NOTES / f"paperclip-{f.name}"
            dest.write_text(f.read_text())
            print(f"  ✅ Paperclip {f.name} → OpenClaw notes")

    print("✅ Knowledge sync complete")


def share_postbridge_analytics():
    """Fetch PostBridge analytics and share with Paperclip"""
    print("📊 Fetching PostBridge analytics...")

    # Trigger sync
    try:
        r = requests.post(f"{PB_BASE}/analytics/sync", headers=PB_HEADERS, timeout=15)
        sync_result = r.json()
        print(f"  Sync triggered: {len(sync_result.get('triggered', []))} platforms")
    except Exception as e:
        print(f"  ⚠️ Sync failed: {e}")

    # Get analytics
    try:
        r = requests.get(f"{PB_BASE}/analytics?limit=50", headers=PB_HEADERS, timeout=15)
        analytics = r.json()

        total_views = sum(a.get("view_count", 0) for a in analytics.get("data", []))
        total_likes = sum(a.get("like_count", 0) for a in analytics.get("data", []))
        total_comments = sum(a.get("comment_count", 0) for a in analytics.get("data", []))
        total_shares = sum(a.get("share_count", 0) for a in analytics.get("data", []))

        report = f"""# PostBridge Analytics Report
Generated: {datetime.now().isoformat()}

## Summary
- Total Views: {total_views}
- Total Likes: {total_likes}
- Total Comments: {total_comments}
- Total Shares: {total_shares}
- Analytics Records: {analytics.get('meta', {}).get('total', 0)}

## Per-Post Breakdown
"""
        for a in analytics.get("data", []):
            report += f"\n### {a.get('platform', 'unknown')} - {a.get('platform_post_id', 'N/A')}\n"
            report += f"- Views: {a.get('view_count', 0)}\n"
            report += f"- Likes: {a.get('like_count', 0)}\n"
            report += f"- URL: {a.get('share_url', 'N/A')}\n"

        # Write to both systems
        dest_pcp = PCP_KNOWLEDGE / "areas" / "marketing" / "postbridge-analytics-latest.md"
        dest_pcp.parent.mkdir(parents=True, exist_ok=True)
        dest_pcp.write_text(report)

        dest_oc = OC_NOTES / "postbridge-analytics-latest.md"
        dest_oc.write_text(report)

        print(f"  ✅ Analytics report written to both systems")
        print(f"  📊 Views: {total_views} | Likes: {total_likes} | Comments: {total_comments}")

    except Exception as e:
        print(f"  ❌ Analytics fetch failed: {e}")

    # Get post results
    try:
        r = requests.get(f"{PB_BASE}/post-results?limit=50", headers=PB_HEADERS, timeout=15)
        results = r.json()
        errors = [p for p in results.get("data", []) if p.get("error")]

        if errors:
            error_report = f"""# PostBridge Post Errors
Generated: {datetime.now().isoformat()}
Total errors: {len(errors)}

## Errors
"""
            for e in errors[:20]:
                error_report += f"- Post {e.get('post_id', 'N/A')[:8]}: {e.get('error', 'unknown')}\n"

            dest = PCP_KNOWLEDGE / "areas" / "marketing" / "postbridge-errors-latest.md"
            dest.write_text(error_report)
            print(f"  ⚠️ {len(errors)} post errors documented")

    except Exception as e:
        print(f"  ❌ Post results fetch failed: {e}")


def create_revenue_tasks():
    """Create revenue-critical tasks in Paperclip based on our findings"""

    # Task 1: Update PostBridge knowledge
    create_issue(
        title="[OpenClaw→Paperclip] CRITICAL: Instagram Posts Need Media — 26 Posts Rejected",
        description="""## Discovery by OpenClaw (Vilona)

PostBridge API investigation revealed:
- **26 Instagram posts were REJECTED** because they were text-only
- Instagram REQUIRES images/videos attached to posts
- Error: "No supported media files found. Instagram only supports images and videos."
- PostBridge returns HTTP 201 (not 200) for media uploads — old scripts treated 201 as failure

## Fix Applied
- Campaign rebuilt with proper images: 27/27 posts with media
- Scheduled: March 13-19, 3/day across Instagram/TikTok/Facebook
- PostBridge API docs updated in company-knowledge

## Action for Paperclip Agents
1. Update all content generation scripts to ALWAYS include media
2. Verify media upload flow: POST /media/create-upload-url → PUT file → use media_id
3. Check /v1/post-results after every post for success/failure verification

## PostBridge API Reference
See: company-knowledge/resources/tool-guides/postbridge-api-reference.md""",
        priority="critical"
    )

    # Task 2: Coordinate campaign monitoring
    create_issue(
        title="[OpenClaw→Paperclip] Monitor New Campaign (March 13-19) — 27 Posts With Media",
        description="""## Campaign Details
- 27 posts scheduled across Instagram, TikTok, Facebook
- All posts have proper product images attached (FIXED)
- Schedule: March 13-19, 3/day at 06:00/12:00/18:00 WIB
- Products: All 9 LYNK products

## Monitoring Tasks
1. Check PostBridge post-results daily for success/failure
2. Sync analytics every 6 hours: POST /v1/analytics/sync
3. Report metrics to Telegram
4. If conversions still zero after 48h → escalate product page issues

## Analytics Commands
```bash
# Sync
curl -X POST "https://api.post-bridge.com/v1/analytics/sync" -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi"

# Get data
curl "https://api.post-bridge.com/v1/analytics?limit=50" -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi"
```""",
        priority="high"
    )


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        get_status()
    elif cmd == "sync":
        sync_knowledge()
    elif cmd == "analytics":
        share_postbridge_analytics()
    elif cmd == "create-revenue-tasks":
        create_revenue_tasks()
    elif cmd == "full-bridge":
        # Run everything
        get_status()
        print()
        sync_knowledge()
        print()
        share_postbridge_analytics()
        print()
        create_revenue_tasks()
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: status | sync | analytics | create-revenue-tasks | full-bridge")
