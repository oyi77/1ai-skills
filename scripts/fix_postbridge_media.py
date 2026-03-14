#!/usr/bin/env python3
"""
Fix PostBridge: 72 scheduled posts have no media.
1. Upload v4 images → get media IDs
2. Remove YouTube account from image-only posts (YT needs video)
3. Patch all posts with rotating images
"""
import os, sys, json, time, requests
from pathlib import Path
from itertools import cycle

API_KEY  = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"
HEADERS  = {"Authorization": f"Bearer {API_KEY}"}

# Accounts by platform
YOUTUBE_IDS   = {49678}
INSTAGRAM_IDS = {49682, 49676}
THREADS_IDS   = {49683, 49680, 49677}
FACEBOOK_IDS  = {49675, 49674, 49673, 49672}
# YouTube only works with video — remove from image posts
NEEDS_MEDIA   = INSTAGRAM_IDS  # Threads & Facebook can be text-only but images help

IMG_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames_v4")


def upload_image(img_path):
    """Upload image to PostBridge, return media_id."""
    # Step 1: get upload URL
    size_bytes = img_path.stat().st_size
    r = requests.post(
        f"{BASE_URL}/media/create-upload-url",
        headers=HEADERS,
        json={"name": img_path.name, "mime_type": "image/png", "size_bytes": size_bytes},
        timeout=20,
    )
    if r.status_code not in (200, 201):
        print(f"  ❌ get-upload-url failed: {r.status_code} {r.text[:100]}")
        return None
    data = r.json()
    upload_url = data.get("upload_url")
    media_id   = data.get("media_id")
    if not upload_url:
        print(f"  ❌ no upload_url in response: {data}")
        return None

    # Step 2: PUT file to S3/CDN
    with open(img_path, "rb") as f:
        r2 = requests.put(upload_url, data=f,
                          headers={"Content-Type": "image/png"}, timeout=30)
    if r2.status_code not in (200, 204):
        print(f"  ❌ upload PUT failed: {r2.status_code}")
        return None

    print(f"  ✅ Uploaded {img_path.name} → id={media_id}")
    return media_id


def get_all_scheduled():
    """Get all 72 scheduled posts."""
    posts, offset = [], 0
    while True:
        r = requests.get(
            f"{BASE_URL}/posts",
            headers=HEADERS,
            params={"status": "scheduled", "limit": 50, "offset": offset},
            timeout=20,
        )
        data = r.json().get("data", [])
        if not data:
            break
        posts.extend(data)
        offset += len(data)
        if len(data) < 50:
            break
    return posts


def patch_post(post_id, social_accounts, media_ids):
    """Patch post: update accounts + add media."""
    payload = {
        "social_accounts": social_accounts,
    }
    if media_ids:
        payload["media"] = [{"id": mid} for mid in media_ids]

    r = requests.patch(
        f"{BASE_URL}/posts/{post_id}",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=20,
    )
    return r.status_code, r.text[:150]


def main():
    print("=== PostBridge Media Fix ===\n")

    # 1. Upload 4 v4 images (dark + white, 2 products — enough to rotate)
    images = sorted(IMG_DIR.glob("*_v4_dark.png"))[:4]
    if not images:
        print("❌ No v4 images found in", IMG_DIR)
        sys.exit(1)

    print(f"Uploading {len(images)} images...")
    media_ids = []
    for img in images:
        mid = upload_image(img)
        if mid:
            media_ids.append(mid)
        time.sleep(0.5)

    if not media_ids:
        print("❌ No images uploaded successfully")
        sys.exit(1)
    print(f"\n✅ {len(media_ids)} images uploaded: {media_ids}\n")

    # 2. Get all scheduled posts
    print("Fetching scheduled posts...")
    posts = get_all_scheduled()
    print(f"Found {len(posts)} posts\n")

    img_cycle = cycle(media_ids)
    ok, skipped, failed = 0, 0, 0

    for post in posts:
        pid = post["id"]
        raw_accounts = post.get("social_accounts", [])
        # PostBridge returns account IDs as integers
        acct_ids = set(raw_accounts) if isinstance(raw_accounts[0], int) else \
                   {a["id"] for a in raw_accounts}

        has_media = bool(post.get("media"))
        has_youtube = bool(acct_ids & YOUTUBE_IDS)
        has_instagram = bool(acct_ids & INSTAGRAM_IDS)

        if has_media:
            # Already has media — only fix YouTube if needed
            if has_youtube and not has_instagram:
                # YouTube-only post, no video → remove YouTube account
                new_accounts = list(acct_ids - YOUTUBE_IDS)
                if not new_accounts:
                    print(f"  ⏭  {pid[:8]}… skipped (YouTube only, no video, no other accounts)")
                    skipped += 1
                    continue
                status, txt = patch_post(pid, new_accounts, None)
                print(f"  🔧 {pid[:8]}… removed YouTube → {status}")
            else:
                skipped += 1
            continue

        # No media — fix it
        # Remove YouTube (can't post images to YouTube)
        new_accounts = list(acct_ids - YOUTUBE_IDS)
        if not new_accounts:
            print(f"  ⏭  {pid[:8]}… skip (YouTube-only post, would need video)")
            skipped += 1
            continue

        # Add rotating image
        mid = next(img_cycle)
        status, txt = patch_post(pid, new_accounts, [mid])
        if status in (200, 201):
            print(f"  ✅ {pid[:8]}… accounts={new_accounts} media={mid} → {status}")
            ok += 1
        else:
            print(f"  ❌ {pid[:8]}… FAILED {status}: {txt}")
            failed += 1

        time.sleep(0.3)  # rate limit

    print(f"\n=== DONE ===")
    print(f"Fixed:   {ok}")
    print(f"Skipped: {skipped}")
    print(f"Failed:  {failed}")


if __name__ == "__main__":
    main()
