"""
postbridge_with_interceptor.py — Integration Example: PostBridge + AI Interceptor
==================================================================================
Shows how to wrap PostBridge API calls with the AI Content Interceptor
for automatic caption enhancement, platform compliance, and retry.

Usage:
    python3 postbridge_with_interceptor.py --caption "Produk terbaik kami" --accounts 49675 49674
    python3 postbridge_with_interceptor.py --caption "Check this out!" --accounts 49682 --media photo.jpg
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Setup path
# ---------------------------------------------------------------------------
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from ai_interceptor import AIInterceptor, InterceptResult
from content_interceptor import create_content_interceptor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("postbridge_example")


# ---------------------------------------------------------------------------
# Mock PostBridge API (replace with actual API calls)
# ---------------------------------------------------------------------------
POSTBRIDGE_API_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_API_KEY = os.environ.get("POSTBRIDGE_API_KEY", "pb_live_AT9Xm4PKaYBzAvFZYGgexi")


def _mock_postbridge_create_post(
    caption: str,
    social_accounts: List[int],
    scheduled_at: Optional[str] = None,
    media_ids: Optional[List[str]] = None,
    media: Optional[List[str]] = None,
    **kwargs,
) -> dict:
    """
    Mock PostBridge post creation. Replace with actual API call:

        import requests
        response = requests.post(
            f"{POSTBRIDGE_API_BASE}/posts",
            headers={"Authorization": f"Bearer {POSTBRIDGE_API_KEY}"},
            json={
                "caption": caption,
                "social_accounts": social_accounts,
                "scheduled_at": scheduled_at,
                "media": media_ids or [],
            }
        )
        return response.json()
    """
    logger.info("📤 PostBridge: Creating post for %d accounts", len(social_accounts))
    logger.info("   Caption: %s...", caption[:80])
    logger.info("   Accounts: %s", social_accounts)
    logger.info("   Media: %s", media or media_ids or [])

    # Simulate validation
    if not social_accounts:
        raise ValueError("No valid accounts remaining after platform compliance check")

    # Simulate missing media error for Instagram
    instagram_accounts = {49682, 49676}
    has_instagram = any(a in instagram_accounts for a in social_accounts)
    has_media = bool(media or media_ids)

    if has_instagram and not has_media:
        raise ValueError("No supported media files found for Instagram account")

    time.sleep(0.05)  # Simulate API latency

    return {
        "id": f"post_{int(time.time())}",
        "status": "scheduled",
        "caption": caption,
        "social_accounts": social_accounts,
        "media_count": len(media or media_ids or []),
        "scheduled_at": scheduled_at,
        "created_at": time.time(),
    }


# ---------------------------------------------------------------------------
# Demo 1: Basic post with caption enhancement
# ---------------------------------------------------------------------------
def demo_basic_post(caption: str, account_ids: List[int], media: Optional[List[str]] = None):
    """Simple post with auto caption enhancement."""
    print("\n" + "="*60)
    print("Demo 1: Basic Post with Caption Enhancement")
    print("="*60)

    interceptor = create_content_interceptor()

    result: InterceptResult = interceptor.run(
        func=_mock_postbridge_create_post,
        skill_type="postbridge_post",
        kwargs={
            "caption": caption,
            "social_accounts": account_ids,
            "media": media or [],
            "scheduled_at": "2026-03-22T10:00:00+07:00",
        },
    )

    print(f"\n📊 Intercept Summary:")
    print(f"  Success:       {result.success}")
    print(f"  Quality Score: {result.quality_score:.1f}/10")
    print(f"  Retries:       {result.retries}")
    print(f"  Pre-Enhanced:  {result.pre_enhanced}")

    if result.output:
        print(f"\n✅ Post Created:")
        print(json.dumps(result.output, indent=2, default=str))
    else:
        print(f"\n❌ Post Failed: {result.error_message}")

    return result


# ---------------------------------------------------------------------------
# Demo 2: Instagram post (requires media — will auto-filter without)
# ---------------------------------------------------------------------------
def demo_instagram_compliance(caption: str, media_path: Optional[str] = None):
    """Demonstrate platform compliance: Instagram requires media."""
    print("\n" + "="*60)
    print("Demo 2: Instagram Platform Compliance")
    print("="*60)

    interceptor = create_content_interceptor()

    # Try to post to Instagram + Facebook
    # Instagram requires media — compliance hook will filter it if missing
    account_ids = [49682, 49675]  # Instagram + Facebook
    print(f"Attempting post to: Instagram (49682) + Facebook (49675)")
    print(f"Media: {media_path or 'None (Instagram will be filtered out)'}")

    result: InterceptResult = interceptor.run(
        func=_mock_postbridge_create_post,
        skill_type="postbridge_post",
        kwargs={
            "caption": caption,
            "social_accounts": account_ids,
            "media": [media_path] if media_path else [],
            "scheduled_at": "2026-03-22T10:00:00+07:00",
        },
    )

    print(f"\n✅ Result: success={result.success}")
    print(f"  Accounts in output: {result.output.get('social_accounts', []) if result.output else 'N/A'}")

    # Check audit trail for compliance actions
    compliance_events = [e for e in result.audit_trail if "compliance" in str(e.get("event", ""))]
    if compliance_events:
        print(f"\n⚠️  Compliance actions taken:")
        for event in compliance_events:
            print(f"  - {event['event']}: {event.get('data', {})}")

    return result


# ---------------------------------------------------------------------------
# Demo 3: Batch posting with interceptor
# ---------------------------------------------------------------------------
def demo_batch_posts(captions: List[str], account_ids: List[int]):
    """Post multiple captions to multiple accounts with interception."""
    print("\n" + "="*60)
    print("Demo 3: Batch Posting")
    print("="*60)

    interceptor = create_content_interceptor()
    results = []

    for i, caption in enumerate(captions, 1):
        print(f"\nPost {i}/{len(captions)}: {caption[:50]}...")

        result = interceptor.run(
            func=_mock_postbridge_create_post,
            skill_type="postbridge_post",
            kwargs={
                "caption": caption,
                "social_accounts": account_ids,
                "media": [],
                "scheduled_at": f"2026-03-22T{10+i:02d}:00:00+07:00",
            },
        )

        results.append(result)
        status = "✅" if result.success else "❌"
        print(f"  {status} Quality={result.quality_score:.1f} Retries={result.retries}")

        # Rate limiting
        time.sleep(0.1)

    print(f"\n📊 Batch Summary:")
    print(f"  Total:   {len(results)}")
    print(f"  Success: {sum(1 for r in results if r.success)}")
    print(f"  Failed:  {sum(1 for r in results if not r.success)}")
    avg_quality = sum(r.quality_score for r in results) / len(results)
    print(f"  Avg Quality: {avg_quality:.1f}/10")

    return results


# ---------------------------------------------------------------------------
# Demo 4: Error recovery (missing media)
# ---------------------------------------------------------------------------
def demo_error_recovery(caption: str):
    """Demonstrate automatic error recovery for missing media."""
    print("\n" + "="*60)
    print("Demo 4: Error Recovery (Missing Media)")
    print("="*60)

    interceptor = create_content_interceptor()

    # Post to Instagram WITHOUT media — should trigger recovery hook
    print("Posting to Instagram WITHOUT media (will trigger error recovery)...")
    print("Expected: MissingMediaErrorHook will filter Instagram account out")

    result = interceptor.run(
        func=_mock_postbridge_create_post,
        skill_type="postbridge_post",
        kwargs={
            "caption": caption,
            "social_accounts": [49682, 49675],  # Instagram + Facebook
            "media": [],  # No media!
        },
    )

    error_events = [e for e in result.audit_trail if "error" in str(e.get("event", "")).lower() or "recover" in str(e.get("event", "")).lower()]
    if error_events:
        print(f"\n🔧 Recovery actions:")
        for event in error_events:
            print(f"  - {event['event']}")

    print(f"\nFinal result: success={result.success}")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PostBridge with AI Interceptor Demo")
    parser.add_argument("--caption", default="Produk digital terbaik dari BerkahKarya! Dapatkan sekarang 🔥", help="Post caption")
    parser.add_argument("--accounts", nargs="+", type=int, default=[49675, 49674], help="Account IDs")
    parser.add_argument("--media", default=None, help="Media file path")
    parser.add_argument("--demo", choices=["1", "2", "3", "4", "all"], default="all", help="Demo to run")
    args = parser.parse_args()

    print("📱 PostBridge with AI Content Interceptor")
    print(f"Caption: {args.caption[:60]}...")
    print(f"Accounts: {args.accounts}")
    print(f"Media: {args.media}")

    if args.demo in ("1", "all"):
        demo_basic_post(args.caption, args.accounts, [args.media] if args.media else None)

    if args.demo in ("2", "all"):
        demo_instagram_compliance(args.caption, args.media)

    if args.demo in ("3", "all"):
        sample_captions = [
            "Tips sukses jualan digital #1 💰",
            "Cara dapat passive income dari rumah 🏠",
            "Produk digital terlaris bulan ini 🔥",
        ]
        demo_batch_posts(sample_captions, args.accounts)

    if args.demo in ("4", "all"):
        demo_error_recovery(args.caption)

    print("\n✅ Demo complete! Check /tmp/ai_interceptor.log for full audit trail.")


if __name__ == "__main__":
    main()
