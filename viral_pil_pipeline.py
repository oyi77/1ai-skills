#!/usr/bin/env python3
"""
Viral Content Pipeline — Create images with PIL + Post to all accounts
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────────────────────────
IMGBB_API_KEY    = os.environ.get("IMGBB_API_KEY", "")
POST_BRIDGE_KEY  = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_Kyc2gafDF7Qc8c2ALELtEC")
POST_BRIDGE_URL  = "https://api.post-bridge.com/v1"

OUTPUT_DIR = Path("output/viral_pil")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# ── Viral Concepts ───────────────────────────────────────────────────────────────
CONCEPTS = [
    {
        "id": 1,
        "niche": "Motivational",
        "headline": "YOUR ONLY COMPETITION\nIS YESTERDAY'S YOU",
        "bg_color": (26, 26, 46),
        "text_color": (255, 255, 255),
        "caption": "Every single day is a fresh start. Stop comparing yourself to others. The only race that matters is the one you run against your past self. Drop a 💪 if you needed to hear this today! #motivation #mindset #success #growth #viral",
    },
    {
        "id": 2,
        "niche": "Money Mindset",
        "headline": "MONEY FOLLOWS\nACTION, NOT WISHES",
        "bg_color": (255, 215, 0),
        "text_color": (0, 0, 0),
        "caption": "Stop waiting for the 'perfect moment'. The people winning financially are NOT the smartest. They're the ones who STARTED. What's ONE thing you can do TODAY? Comment below 👇 #money #wealth #entrepreneur #success #mindset",
    },
    {
        "id": 3,
        "niche": "Success Mindset",
        "headline": "IN 1 YEAR\nYOUR LIFE CAN\nCOMPLETELY CHANGE",
        "bg_color": (45, 27, 105),
        "text_color": (255, 255, 255),
        "caption": "365 days. That's all it takes. I stopped talking and started DOING. Like this if you're working on your glow-up right now 👇 #transformation #success #glowup #motivation #viral",
    },
    {
        "id": 4,
        "niche": "Growth Mindset",
        "headline": "DISCOMFORT\nIS THE PRICE\nOF GROWTH",
        "bg_color": (231, 76, 60),
        "text_color": (255, 255, 255),
        "caption": "Nothing grows in the comfort zone. Every breakthrough starts with being uncomfortable. Embrace the struggle. Growth is waiting on the other side. 💪 #growth #mindset #motivation #success #viral",
    },
    {
        "id": 5,
        "niche": "Productivity",
        "headline": "5AM HABIT THAT\nCHANGED MY LIFE",
        "bg_color": (39, 174, 96),
        "text_color": (255, 255, 255),
        "caption": "Started waking up at 5AM: more productive, clearer mind, less anxiety. First 3 days are hard. After that, you'll never go back. Save this if you want to try it! 🔖 #5am #productivity #habits #success",
    },
]


# ── Create Image with PIL ───────────────────────────────────────────────────────
def create_image_pil(concept: dict, output_path: Path) -> bool:
    """Create image with PIL."""
    print(f"  🎨 Creating image with PIL...")
    
    try:
        # Create canvas (9:16 aspect ratio, 1080x1920)
        W, H = 1080, 1920
        img = Image.new("RGB", (W, H), concept["bg_color"])
        draw = ImageDraw.Draw(img)
        
        # Try to find a font
        font_size = 72
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text and calculate positioning
        lines = concept["headline"].split('\n')
        total_height = len(lines) * (font_size + 20)
        start_y = (H - total_height) // 2
        
        # Draw each line
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            x = (W - text_w) // 2
            y = start_y + i * (font_size + 20)
            draw.text((x, y), line, fill=concept["text_color"], font=font)
        
        # Save
        img.save(output_path, "JPEG", quality=90)
        size_kb = output_path.stat().st_size / 1024
        print(f"  ✅ Image created: {output_path} ({size_kb:.0f}KB)")
        return True
        
    except Exception as e:
        print(f"  ❌ PIL error: {e}")
        return False


# ── Upload to ImgBB ────────────────────────────────────────────────────────────
def upload_imgbb(img_path: Path) -> str:
    """Upload image to ImgBB."""
    print(f"  📤 Uploading to ImgBB...")
    
    import base64
    img_b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    
    data = urllib.parse.urlencode({
        "key": IMGBB_API_KEY,
        "image": img_b64,
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request("https://api.imgbb.com/1/upload", data=data)
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        if result.get("success"):
            url = result["data"]["url"]
            print(f"  ✅ Uploaded")
            return url
        else:
            print(f"  ❌ Upload failed")
            return ""
    except Exception as e:
        print(f"  ❌ Upload error: {e}")
        return ""


# ── Get All Accounts ────────────────────────────────────────────────────────────
def get_accounts() -> dict:
    """Fetch all connected accounts."""
    accounts = []
    offset = 0
    
    while True:
        url = f"{POST_BRIDGE_URL}/social-accounts?limit=50&offset={offset}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            batch = data.get("data", [])
            accounts.extend(batch)
            
            meta = data.get("meta", {})
            if offset + 50 >= meta.get("total", 0):
                break
            offset += 50
        except:
            break
    
    fb_ids = [a["id"] for a in accounts if a["platform"] == "facebook"]
    tik_ids = [a["id"] for a in accounts if a["platform"] == "tiktok"]
    
    return {"facebook": fb_ids, "tiktok": tik_ids}


# ── Schedule Post ─────────────────────────────────────────────────────────────
def schedule_post(account_ids: list, caption: str, media_url: str, sched_time: str) -> dict:
    """Schedule a post using correct Post-Bridge API format."""
    # Post-Bridge expects: caption, social_accounts (not account_ids), media (array of {url})
    payload = {
        "caption": caption,
        "social_accounts": account_ids,
        "media": [{"url": media_url}],
        "scheduled_at": sched_time,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{POST_BRIDGE_URL}/posts", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": str(e), "status_code": e.code, "body": body[:500]}
    except Exception as e:
        return {"error": str(e)}


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("🚀 VIRAL CONTENT PIPELINE — PIL + POST-BRIDGE")
    print("=" * 60)
    print()
    
    # Get accounts
    print("📱 Fetching accounts...")
    accs = get_accounts()
    fb_ids = accs["facebook"]
    tik_ids = accs["tiktok"]
    print(f"  Facebook: {len(fb_ids)} accounts")
    print(f"  TikTok: {len(tik_ids)} accounts")
    print()
    
    # Schedule times: 30min from now, +4h each
    now_utc = datetime.now(timezone.utc)
    results = []
    
    for i, concept in enumerate(CONCEPTS):
        img_path = OUTPUT_DIR / f"viral{concept['id']}.jpg"
        sched_time = now_utc + timedelta(minutes=30, hours=i*4)
        sched_utc = sched_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        sched_wib = (sched_time + JAKARTA_OFFSET).strftime("%Y-%m-%d %H:%M WIB")
        
        print(f"─" * 60)
        print(f"🎯 Post {i+1}/5 — {concept['niche']}")
        print(f"⏰ Scheduled: {sched_wib}")
        print()
        
        # Create image
        if not img_path.exists():
            ok = create_image_pil(concept, img_path)
            if not ok:
                print(f"  ⚠️ Skipping (image failed)")
                continue
        else:
            print(f"  ✅ Image exists: {img_path}")
        
        # Upload
        img_url = upload_imgbb(img_path)
        if not img_url:
            print(f"  ⚠️ Skipping (upload failed)")
            continue
        
        # Schedule
        print(f"  📤 Scheduling to {len(fb_ids)} FB + {len(tik_ids)} TikTok...")
        
        post_fb = schedule_post(fb_ids, concept["caption"], img_url, sched_utc)
        post_tik = schedule_post(tik_ids, concept["caption"], img_url, sched_utc)
        
        fb_ok = "error" not in post_fb
        tik_ok = "error" not in post_tik
        
        # Log errors for debugging
        if not fb_ok:
            print(f"  FB Error: {post_fb.get('body', post_fb.get('error', '?'))[:200]}")
        if not tik_ok:
            print(f"  TikTok Error: {post_tik.get('body', post_tik.get('error', '?'))[:200]}")
        
        results.append({
            "id": concept["id"],
            "niche": concept["niche"],
            "scheduled": sched_wib,
            "image": str(img_path),
            "url": img_url,
            "facebook": fb_ok,
            "tiktok": tik_ok,
            "fb_response": post_fb,
            "tik_response": post_tik,
        })
        
        print(f"  Facebook: {'✅' if fb_ok else '❌'}")
        print(f"  TikTok: {'✅' if tik_ok else '❌'}")
        print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    for r in results:
        fb = "✅" if r.get("facebook") else "❌"
        tik = "✅" if r.get("tiktok") else "❌"
        print(f"{fb}{tik} Post {r['id']} [{r['niche']}] → {r['scheduled']}")
    
    summary_path = OUTPUT_DIR / "summary.json"
    summary_path.write_text(json.dumps(results, indent=2))
    print(f"\n💾 Saved: {summary_path}")


if __name__ == "__main__":
    main()
