#!/usr/bin/env python3
"""
Fix PostBridge: delete 323 posts on old accounts, reschedule to ALL 59 accounts with media.
Handles pagination properly. Uploads hook images for posts without media.
"""
import requests, json, sys, time, os, random
from datetime import datetime, timedelta

API = "https://api.post-bridge.com/v1"
KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
HDR = {"Authorization": f"Bearer {KEY}"}
HOOK_DIR = os.path.expanduser("~/.openclaw/workspace/autopilot_affiliate_engine/jendralbot_assets/hook_frames_canva/hook_frames_canva_output")

DRY = "--live" not in sys.argv

def get(ep, **kw):
    r = requests.get(f"{API}{ep}", headers=HDR, params=kw); r.raise_for_status(); return r.json()

def post(ep, data):
    r = requests.post(f"{API}{ep}", headers={**HDR, "Content-Type": "application/json"}, json=data)
    return r.status_code, r.json()

def put(url, data, ct):
    return requests.put(url, data=data, headers={"Content-Type": ct}).status_code

def delete(ep):
    return requests.delete(f"{API}{ep}", headers=HDR).status_code

def get_all(ep, **params):
    """Paginate through all results."""
    all_items, offset = [], 0
    while True:
        d = get(ep, limit=100, offset=offset, **params)
        items = d.get("data", [])
        all_items.extend(items)
        total = d.get("meta", {}).get("total", len(items))
        offset += 100
        if offset >= total or not items: break
        time.sleep(0.15)
    return all_items

def upload_image(path):
    """Upload image to PostBridge, return media_id."""
    name = os.path.basename(path)
    size = os.path.getsize(path)
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    
    code, resp = post("/media/create-upload-url", {
        "name": name, "size_bytes": size, "mime_type": mime
    })
    if code not in (200, 201):
        print(f"    Upload URL failed: {resp}")
        return None
    
    media_id = resp.get("data", {}).get("media_id") or resp.get("media_id")
    upload_url = resp.get("data", {}).get("upload_url") or resp.get("upload_url")
    
    if not media_id or not upload_url:
        print(f"    Missing media_id/upload_url: {resp}")
        return None
    
    with open(path, "rb") as f:
        status = put(upload_url, f.read(), mime)
    
    if status != 200:
        print(f"    Upload failed: HTTP {status}")
        return None
    
    return media_id

# === MAIN ===
print("=" * 60)
print("PostBridge Scheduled Posts Fix")
print("=" * 60)

# 1. Accounts
accounts = get_all("/social-accounts")
print(f"\n📱 Accounts: {len(accounts)}")
by_plat = {}
for a in accounts:
    by_plat.setdefault(a["platform"], []).append(a["id"])
for p in sorted(by_plat):
    print(f"  {p}: {by_plat[p]}")

all_ids = [a["id"] for a in accounts]

# 2. Scheduled posts
scheduled = get_all("/posts", status="scheduled")
print(f"\n📋 Scheduled posts: {len(scheduled)}")

# Dedup content
seen = {}
for p in scheduled:
    cap = p.get("caption", "")
    key = cap[:120]
    if key not in seen:
        seen[key] = {
            "caption": cap,
            "media_ids": p.get("media") or [],  # list of media_id strings or null
        }

print(f"   Unique captions: {len(seen)}")
has_media = sum(1 for v in seen.values() if v["media_ids"])
no_media = len(seen) - has_media
print(f"   With media: {has_media} | Without media: {no_media}")

# 3. Prepare hook images for posts without media
hook_images = sorted([os.path.join(HOOK_DIR, f) for f in os.listdir(HOOK_DIR) if f.endswith('.png')]) if os.path.isdir(HOOK_DIR) else []
print(f"\n🖼️  Hook images available: {len(hook_images)}")

if DRY:
    print(f"\n🔍 DRY RUN")
    print(f"   Would delete: {len(scheduled)} posts")
    print(f"   Would create: {len(seen)} posts → {len(all_ids)} accounts each")
    print(f"   Would upload: {no_media} images (for posts without media)")
    print(f"\n   Run with --live to execute")
    sys.exit(0)

# 4. Upload images for posts without media
uploaded_media = []
if no_media > 0 and hook_images:
    print(f"\n📤 Uploading {min(no_media, len(hook_images))} hook images...")
    for i, img_path in enumerate(hook_images[:no_media]):
        mid = upload_image(img_path)
        if mid:
            uploaded_media.append(mid)
            print(f"  ✅ [{i+1}] {os.path.basename(img_path)} → {mid[:12]}...")
        time.sleep(0.3)
    print(f"Uploaded: {len(uploaded_media)}/{no_media}")

# 5. Delete ALL old scheduled posts
print(f"\n🗑️  Deleting {len(scheduled)} old posts...")
deleted = 0
for i, p in enumerate(scheduled):
    code = delete(f"/posts/{p['id']}")
    if code in (200, 204): deleted += 1
    time.sleep(0.1)
    if (i+1) % 100 == 0: print(f"  ... {i+1}/{len(scheduled)}")
print(f"Deleted: {deleted}/{len(scheduled)}")

# 6. Reschedule ALL content to ALL accounts
print(f"\n📅 Creating {len(seen)} posts for {len(all_ids)} accounts...")
base = datetime.now() + timedelta(hours=2)
created = 0
errors = 0
img_idx = 0

for i, (key, content) in enumerate(seen.items()):
    sched_at = base + timedelta(minutes=i * 20)  # every 20 min
    
    payload = {
        "caption": content["caption"],
        "scheduled_at": sched_at.strftime("%Y-%m-%dT%H:%M:%S") + "+07:00",
        "social_accounts": all_ids,
    }
    
    # Attach media
    if content["media_ids"]:
        payload["media"] = content["media_ids"]
    elif uploaded_media:
        payload["media"] = [uploaded_media[img_idx % len(uploaded_media)]]
        img_idx += 1
    
    code, resp = post("/posts", payload)
    if code in (200, 201):
        created += 1
    else:
        errors += 1
        if errors <= 5: print(f"  ❌ {resp.get('message', resp)}")
    
    time.sleep(0.15)
    if (i+1) % 50 == 0: print(f"  ... {i+1}/{len(seen)} created")

hours_span = len(seen) * 20 / 60
print(f"\n{'='*60}")
print(f"✅ DONE")
print(f"   Deleted:  {deleted} old posts")
print(f"   Created:  {created} new posts")
print(f"   Errors:   {errors}")
print(f"   Accounts: {len(all_ids)} (all platforms)")
print(f"   Schedule: every 20min over {hours_span:.0f}h")
print(f"   Media:    {has_media} existing + {len(uploaded_media)} uploaded")
print(f"{'='*60}")
