#!/usr/bin/env python3
"""PostBridge auto-retry failed posts + bulk CSV scheduling."""

import csv
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone

API_KEY = "REDACTED_POSTBRIDGE_KEY"
API_BASE = "https://api.post-bridge.com/v1"


def _api(method, path, data=None):
    """Make API call to PostBridge."""
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"[API ERROR] {e.code} {url}: {err_body}")
        return None
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return None


def auto_retry_failed():
    """Fetch failed posts and retry them."""
    print("[*] Fetching post results (limit=100)...")
    result = _api("GET", "/post-results?limit=100")
    if not result:
        print("[!] Could not fetch post results.")
        return

    posts = result if isinstance(result, list) else result.get("data", result.get("results", []))
    retried = 0
    skipped = 0

    for post in posts:
        status = post.get("status", "").upper()
        error = (post.get("error") or post.get("error_code") or "").upper()

        if status not in ("FAILED", "ERROR"):
            continue

        caption = post.get("caption", post.get("text", ""))
        account_ids = post.get("account_ids", post.get("accounts", []))
        media_id = post.get("media_id")

        # FILE_ACCESS errors need manual re-upload
        if "FILE_ACCESS" in error or "FILE" in error:
            print(f"  [SKIP] Post {post.get('id', '?')}: FILE_ACCESS — needs re-upload of original media")
            skipped += 1
            continue

        # THREADS_FAIL / RATE_LIMIT — reschedule +2h from now
        if any(k in error for k in ("THREADS", "RATE_LIMIT", "RATE", "LIMIT", "TIMEOUT")):
            scheduled = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
            payload = {
                "caption": caption,
                "account_ids": account_ids,
                "scheduled_at": scheduled,
            }
            if media_id:
                payload["media_id"] = media_id

            print(f"  [RETRY] Post {post.get('id', '?')}: {error} → rescheduled to {scheduled}")
            resp = _api("POST", "/posts", payload)
            if resp:
                retried += 1
            continue

        # Unknown failure — attempt retry anyway
        scheduled = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = {
            "caption": caption,
            "account_ids": account_ids,
            "scheduled_at": scheduled,
        }
        if media_id:
            payload["media_id"] = media_id

        print(f"  [RETRY] Post {post.get('id', '?')}: {error or 'UNKNOWN'} → rescheduled to {scheduled}")
        resp = _api("POST", "/posts", payload)
        if resp:
            retried += 1

    print(f"\n[DONE] Retried: {retried}, Skipped (needs re-upload): {skipped}")


def bulk_schedule_from_csv(csv_path):
    """Schedule posts from CSV file.

    CSV columns: caption,media_id,scheduled_at,account_ids
    account_ids should be semicolon-separated if multiple.
    """
    print(f"[*] Reading CSV: {csv_path}")
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"[!] File not found: {csv_path}")
        return
    except Exception as e:
        print(f"[!] Error reading CSV: {e}")
        return

    if not rows:
        print("[!] CSV is empty.")
        return

    print(f"[*] Scheduling {len(rows)} posts...")
    success = 0

    for i, row in enumerate(rows, 1):
        caption = row.get("caption", "").strip()
        media_id = row.get("media_id", "").strip()
        scheduled_at = row.get("scheduled_at", "").strip()
        raw_accounts = row.get("account_ids", "").strip()

        if not caption:
            print(f"  [{i}] SKIP — no caption")
            continue

        # Parse account_ids (semicolon or comma separated)
        account_ids = [a.strip() for a in raw_accounts.replace(";", ",").split(",") if a.strip()]

        payload = {
            "caption": caption,
            "account_ids": account_ids,
        }
        if media_id:
            payload["media_id"] = media_id
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        resp = _api("POST", "/posts", payload)
        if resp:
            post_id = resp.get("id", resp.get("post_id", "?"))
            print(f"  [{i}] OK — post {post_id} scheduled at {scheduled_at or 'now'}")
            success += 1
        else:
            print(f"  [{i}] FAILED — could not schedule")

    print(f"\n[DONE] Scheduled: {success}/{len(rows)}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 postbridge_auto.py retry              — auto-retry failed posts")
        print("  python3 postbridge_auto.py bulk-csv posts.csv  — bulk schedule from CSV")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "retry":
        auto_retry_failed()
    elif cmd == "bulk-csv":
        if len(sys.argv) < 3:
            print("[!] Missing CSV path. Usage: python3 postbridge_auto.py bulk-csv posts.csv")
            sys.exit(1)
        bulk_schedule_from_csv(sys.argv[2])
    else:
        print(f"[!] Unknown command: {cmd}")
        print("Valid commands: retry, bulk-csv")
        sys.exit(1)


if __name__ == "__main__":
    main()
