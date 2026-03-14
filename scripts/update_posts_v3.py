#!/usr/bin/env python3
"""
Upload v3 images to PostBridge and update all 60 scheduled posts.
Each post gets a matching product image (dark or white alternating).
"""
import requests
import json
import os
import re
from pathlib import Path
import time

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
V3_DIR = Path("/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames_v3")

# Product keyword → image filename mapping
PRODUCT_IMAGE_MAP = {
    "jobmagnet": ["jobmagnet_ai_dark.png", "jobmagnet_ai_white.png"],
    "job": ["jobmagnet_ai_dark.png", "jobmagnet_ai_white.png"],
    "cv": ["jobmagnet_ai_white.png", "jobmagnet_ai_dark.png"],
    "karir": ["jobmagnet_ai_dark.png"],
    "ad engine": ["ai_ad_engine_dark.png", "ai_ad_engine_white.png"],
    "iklan": ["ai_ad_engine_dark.png", "ai_ad_engine_white.png"],
    "ads": ["ai_ad_engine_white.png"],
    "food menu": ["food_menu_ai_dark.png", "food_menu_ai_white.png"],
    "kuliner": ["mesin_cetak_dark.png", "mesin_cetak_white.png"],
    "mesin cetak": ["mesin_cetak_dark.png", "mesin_cetak_white.png"],
    "sellpix": ["sellpix_ai_dark.png", "sellpix_ai_white.png"],
    "foto produk": ["sellpix_ai_white.png", "sellpix_ai_dark.png"],
    "marketplace": ["sellpix_ai_dark.png"],
    "guru pintar": ["guru_pintar_ai_dark.png", "guru_pintar_ai_white.png"],
    "edukasi": ["guru_pintar_ai_white.png"],
    "kelas affiliate": ["kelas_affiliate_dark.png", "kelas_affiliate_white.png"],
    "tiktok": ["kelas_affiliate_dark.png", "ai_content_premium_dark.png"],
    "affiliate": ["kelas_affiliate_white.png", "ai_content_premium_white.png"],
    "konten": ["ai_content_premium_dark.png", "ai_content_premium_white.png"],
    "content": ["ai_content_premium_white.png"],
    "ai creative": ["ai_ad_engine_dark.png"],
    "creative": ["ai_ad_engine_white.png"],
    "viral": ["ai_content_premium_dark.png"],
}

DEFAULT_IMAGES = ["ai_content_premium_dark.png", "ai_ad_engine_white.png", "guru_pintar_ai_dark.png", "sellpix_ai_white.png"]


def pick_image_for_caption(caption: str, post_index: int) -> str:
    """Pick best matching v3 image for a caption."""
    cap_lower = caption.lower()
    for keyword, images in PRODUCT_IMAGE_MAP.items():
        if keyword in cap_lower:
            return images[post_index % len(images)]
    return DEFAULT_IMAGES[post_index % len(DEFAULT_IMAGES)]


def upload_image(filepath: Path) -> str | None:
    """Upload image to PostBridge, return media_id."""
    stat = filepath.stat()

    # Step 1: Get upload URL
    r = requests.post(
        f"{BASE_URL}/media/create-upload-url",
        headers=HEADERS,
        json={"name": filepath.name, "size_bytes": stat.st_size, "mime_type": "image/png"}
    )
    if r.status_code not in (200, 201):
        print(f"    ❌ create-upload-url failed: {r.status_code} {r.text[:200]}")
        return None

    data = r.json()
    upload_url = data.get("upload_url") or data.get("data", {}).get("upload_url")
    media_id = data.get("media_id") or data.get("id") or data.get("data", {}).get("media_id") or data.get("data", {}).get("id")

    if not upload_url or not media_id:
        print(f"    ❌ No upload_url/id in response: {json.dumps(data)[:300]}")
        return None

    # Step 2: Upload file
    with open(filepath, "rb") as f:
        put_r = requests.put(upload_url, data=f, headers={"Content-Type": "image/png"})
    if put_r.status_code not in (200, 204):
        print(f"    ❌ PUT upload failed: {put_r.status_code}")
        return None

    return media_id


def update_post_media(post_id: str, media_id: str) -> bool:
    """Patch post with new media."""
    r = requests.patch(
        f"{BASE_URL}/posts/{post_id}",
        headers=HEADERS,
        json={"media": [{"id": media_id}]}
    )
    return r.status_code in (200, 204)


def main():
    print("🚀 Fetching scheduled posts...")
    r = requests.get(f"{BASE_URL}/posts?limit=100&status=scheduled", headers=HEADERS)
    if r.status_code != 200:
        print(f"❌ Failed to fetch posts: {r.status_code}")
        return

    posts = r.json().get("data", [])
    print(f"Found {len(posts)} scheduled posts\n")

    if not posts:
        print("No scheduled posts found.")
        return

    # Cache uploaded images to avoid re-uploading same file
    uploaded_cache: dict[str, str] = {}  # filename → media_id

    updated = 0
    failed = 0

    for idx, post in enumerate(posts):
        post_id = post.get("id")
        caption = post.get("caption", "")
        scheduled_at = (post.get("scheduled_at") or "")[:16]

        img_name = pick_image_for_caption(caption, idx)
        img_path = V3_DIR / img_name

        if not img_path.exists():
            img_path = V3_DIR / DEFAULT_IMAGES[idx % len(DEFAULT_IMAGES)]

        print(f"[{idx+1:02d}/{len(posts)}] {scheduled_at} → {img_name}")

        # Upload if not cached
        if img_name not in uploaded_cache:
            media_id = upload_image(img_path)
            if not media_id:
                print(f"    ⚠️  Upload failed, skipping")
                failed += 1
                continue
            uploaded_cache[img_name] = media_id
            print(f"    ✅ Uploaded → {media_id[:16]}...")
        else:
            media_id = uploaded_cache[img_name]

        # Update post
        if update_post_media(post_id, media_id):
            updated += 1
        else:
            failed += 1
            print(f"    ❌ Patch failed")

        # Rate limit: 10 req/s
        time.sleep(0.12)

    print(f"\n✅ Done: {updated} updated, {failed} failed")
    print(f"📦 Uploaded {len(uploaded_cache)} unique images")


if __name__ == "__main__":
    main()
