"""
Auto Poster — Post generated content to TikTok & Instagram
Handles: caption generation, hashtags, scheduling queue
"""
import os, json, time, subprocess
import urllib.request, urllib.parse

GROQ_KEY    = os.environ.get("GROQ_API_KEY")
TIKTOK_KEY  = os.environ.get("TIKTOK_ACCESS_TOKEN", "")
IG_TOKEN    = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
IG_USER_ID  = os.environ.get("INSTAGRAM_USER_ID", "")

QUEUE_FILE  = "/home/openclaw/.openclaw/workspace/output/post_queue.json"
os.makedirs(os.path.dirname(QUEUE_FILE), exist_ok=True)


# ─── CAPTION GENERATOR ───────────────────────────────────────────────
def generate_caption(category: str, style: str, product_desc: str,
                      platform: str = "tiktok") -> dict:
    """Generate platform-optimized caption + hashtags via Groq"""
    platform_tips = {
        "tiktok":    "TikTok — max 2200 chars, 3-5 hashtags, hook di baris pertama, casual & relatable",
        "instagram": "Instagram — max 2200 chars, 5-10 hashtags, storytelling, emojis natural",
        "facebook":  "Facebook — conversational, longer form ok, 1-2 hashtags only",
    }

    prompt = f"""Kamu copywriter viral Indonesia untuk konten produk.

Buat caption untuk platform {platform}:
- Produk: {product_desc}
- Kategori: {category}
- Visual style: {style}
- Tips platform: {platform_tips.get(platform, '')}

Respond ONLY JSON:
{{
  "caption": "caption text disini (Bahasa Indonesia, natural, engaging)",
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "hook": "kalimat pembuka yang menarik perhatian dalam 3 detik",
  "cta": "call-to-action yang subtle, tidak jualan banget"
}}"""

    NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY")
    if GROQ_KEY:
        llm_url, llm_model, llm_auth = "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile", f"Bearer {GROQ_KEY}"
    else:
        llm_url, llm_model, llm_auth = "https://integrate.api.nvidia.com/v1/chat/completions", "meta/llama-3.3-70b-instruct", f"Bearer {NVIDIA_KEY}"

    payload = json.dumps({
        "model": llm_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500, "temperature": 0.8
    }).encode()

    try:
        req = urllib.request.Request(
            llm_url, data=payload,
            headers={"Authorization": llm_auth, "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"].strip()
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
    except Exception as e:
        return {
            "caption": f"Produk {product_desc} yang kamu cari! 🔥",
            "hashtags": [f"#{category}", "#produk", "#viral"],
            "hook": f"Cobain {product_desc} ini!",
            "cta": "Cek bio untuk info lebih lanjut"
        }


# ─── QUEUE MANAGER ───────────────────────────────────────────────────
def queue_post(file_path: str, platform: str, caption_data: dict,
               chat_id: str, schedule_ts: int = None) -> str:
    """Add to post queue. Returns queue_id."""
    queue = _load_queue()
    queue_id = f"post_{int(time.time())}_{len(queue)}"
    queue[queue_id] = {
        "file_path":   file_path,
        "platform":    platform,
        "caption":     caption_data.get("caption", ""),
        "hashtags":    caption_data.get("hashtags", []),
        "hook":        caption_data.get("hook", ""),
        "chat_id":     chat_id,
        "status":      "pending",
        "schedule_ts": schedule_ts or int(time.time()),
        "created_at":  int(time.time()),
        "error":       None,
    }
    _save_queue(queue)
    return queue_id


def process_queue(platform: str = None) -> list:
    """Process all pending posts. Returns list of results."""
    queue   = _load_queue()
    results = []
    now     = int(time.time())

    for qid, item in list(queue.items()):
        if item["status"] != "pending":
            continue
        if item.get("schedule_ts", 0) > now:
            continue
        if platform and item["platform"] != platform:
            continue

        print(f"  📤 Posting {qid} to {item['platform']}...")
        result = _post_item(item)
        queue[qid]["status"] = "posted" if result["ok"] else "failed"
        queue[qid]["error"]  = result.get("error")
        queue[qid]["posted_at"] = int(time.time())
        results.append({"id": qid, **result})

    _save_queue(queue)
    return results


def _post_item(item: dict) -> dict:
    """Post a single item to its platform"""
    platform  = item["platform"]
    file_path = item["file_path"]
    caption   = item["caption"]
    hashtags  = " ".join(item.get("hashtags", []))
    full_text = f"{caption}\n\n{hashtags}"

    if not os.path.exists(file_path):
        return {"ok": False, "error": "File not found"}

    if platform == "tiktok":
        return _post_tiktok(file_path, full_text)
    elif platform == "instagram":
        return _post_instagram(file_path, full_text)
    else:
        return {"ok": False, "error": f"Unknown platform: {platform}"}


def _post_tiktok(file_path: str, caption: str) -> dict:
    """Post to TikTok via API"""
    if not TIKTOK_KEY:
        return {"ok": False, "error": "TIKTOK_ACCESS_TOKEN not configured"}

    try:
        # TikTok Content Posting API v2
        url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {TIKTOK_KEY}",
            "Content-Type": "application/json"
        }
        file_size = os.path.getsize(file_path)
        payload = json.dumps({
            "post_info": {
                "title": caption[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_comment": False,
                "disable_duet": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }).encode()

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            init_data = json.loads(resp.read())

        upload_url  = init_data["data"]["upload_url"]
        publish_id  = init_data["data"]["publish_id"]

        # Upload video
        with open(file_path, "rb") as f:
            video_data = f.read()
        upload_req = urllib.request.Request(
            upload_url, data=video_data,
            headers={"Content-Type": "video/mp4", "Content-Range": f"bytes 0-{file_size-1}/{file_size}"},
            method="PUT"
        )
        urllib.request.urlopen(upload_req, timeout=60)

        return {"ok": True, "platform": "tiktok", "publish_id": publish_id}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _post_instagram(file_path: str, caption: str) -> dict:
    """Post to Instagram via Graph API"""
    if not IG_TOKEN or not IG_USER_ID:
        return {"ok": False, "error": "INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_USER_ID not configured"}

    try:
        is_video = file_path.endswith(".mp4")

        if is_video:
            # Step 1: Create media container
            url = f"https://graph.instagram.com/v18.0/{IG_USER_ID}/media"
            payload = urllib.parse.urlencode({
                "media_type": "REELS",
                "video_url": file_path,  # must be publicly accessible URL
                "caption": caption,
                "access_token": IG_TOKEN
            }).encode()
        else:
            url = f"https://graph.instagram.com/v18.0/{IG_USER_ID}/media"
            payload = urllib.parse.urlencode({
                "image_url": file_path,
                "caption": caption,
                "access_token": IG_TOKEN
            }).encode()

        req = urllib.request.Request(url, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            container = json.loads(resp.read())

        creation_id = container.get("id")
        if not creation_id:
            return {"ok": False, "error": f"No creation_id: {container}"}

        # Step 2: Publish
        pub_url = f"https://graph.instagram.com/v18.0/{IG_USER_ID}/media_publish"
        pub_payload = urllib.parse.urlencode({
            "creation_id": creation_id,
            "access_token": IG_TOKEN
        }).encode()
        pub_req = urllib.request.Request(pub_url, data=pub_payload, method="POST")
        with urllib.request.urlopen(pub_req, timeout=30) as resp:
            pub_data = json.loads(resp.read())

        return {"ok": True, "platform": "instagram", "media_id": pub_data.get("id")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─── BUILD MESSAGES ───────────────────────────────────────────────────
def build_post_options_message(file_path: str, caption_data: dict) -> tuple[str, list]:
    """Show caption preview + platform options"""
    caption   = caption_data.get("caption", "")[:100]
    hashtags  = " ".join(caption_data.get("hashtags", []))
    hook      = caption_data.get("hook", "")

    text = (
        f"✍️ *Caption siap!*\n\n"
        f"🪝 Hook: _{hook}_\n\n"
        f"📝 Preview:\n{caption}...\n\n"
        f"🏷️ Hashtags: {hashtags}\n\n"
        f"Mau dipost ke mana?"
    )

    tiktok_ok = "✅" if TIKTOK_KEY else "🔐"
    ig_ok     = "✅" if IG_TOKEN else "🔐"

    buttons = [
        [
            {"text": f"{tiktok_ok} TikTok",    "callback_data": "post:tiktok"},
            {"text": f"{ig_ok} Instagram",     "callback_data": "post:instagram"},
        ],
        [
            {"text": "📋 Edit Caption",         "callback_data": "post:edit"},
            {"text": "⏰ Schedule",              "callback_data": "post:schedule"},
        ],
        [{"text": "❌ Skip posting",            "callback_data": "post:skip"}],
    ]
    return text, buttons


def check_credentials() -> dict:
    """Check which platforms are configured"""
    return {
        "tiktok":    bool(TIKTOK_KEY),
        "instagram": bool(IG_TOKEN and IG_USER_ID),
    }


# ─── QUEUE HELPERS ────────────────────────────────────────────────────
def _load_queue() -> dict:
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return {}

def _save_queue(data: dict):
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_queue_status() -> dict:
    queue   = _load_queue()
    pending = sum(1 for i in queue.values() if i["status"] == "pending")
    posted  = sum(1 for i in queue.values() if i["status"] == "posted")
    failed  = sum(1 for i in queue.values() if i["status"] == "failed")
    return {"total": len(queue), "pending": pending, "posted": posted, "failed": failed}


if __name__ == "__main__":
    creds = check_credentials()
    print("Platform credentials:", creds)
    test_caption = generate_caption("minuman", "dark_moody", "jus mangga premium", "tiktok")
    print("\nTest caption:", json.dumps(test_caption, indent=2, ensure_ascii=False))
