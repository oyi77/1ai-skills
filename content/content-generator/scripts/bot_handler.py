"""
BerkahKarya Bot — Main Telegram Handler
Ties together: Wizard → QualityGate → I2V → BGM → Gallery → AutoPost + Batch + Dashboard

Run: python bot_handler.py
Env: TELEGRAM_BOT_TOKEN, NVIDIA_API_KEY, BYTEPLUS_API_KEY, GROQ_API_KEY (optional)
"""

import os, sys, json, time, base64, io, threading, asyncio, subprocess, traceback
import urllib.request, urllib.parse

sys.path.insert(0, os.path.dirname(__file__))

from content_wizard   import (load_state, save_state, clear_state,
                               build_category_message, build_style_message,
                               build_format_message, build_confirm_message)
from prompt_library   import get_prompt, CATEGORIES, STYLES, FORMATS
from quality_gate     import save_gate, get_gate, approve_gate, reject_gate, is_pending, build_preview_message
from gallery          import save_result, get_result, get_results, delete_result, rate_result, mark_posted, build_gallery_message
from cost_dashboard   import log_cost, build_dashboard_message, estimate_generation_cost
from batch_generator  import run_batch, build_batch_options_message, prepare_image_for_i2v
from auto_poster      import generate_caption, queue_post, build_post_options_message, check_credentials
from bgm_manager      import add_bgm_to_video as add_bgm

# ─── CONFIG ──────────────────────────────────────────────────────────
BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
NVIDIA_KEY   = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_KEY = os.environ.get("BYTEPLUS_API_KEY", "")
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
FFMPEG        = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
TG_API        = f"https://api.telegram.org/bot{BOT_TOKEN}"
TG_FILE_API   = f"https://api.telegram.org/file/bot{BOT_TOKEN}"
OUTPUT_DIR    = "/home/openclaw/.openclaw/workspace/output"
IDR_RATE      = 16300


# ─── TELEGRAM API WRAPPERS ───────────────────────────────────────────
def tg(method: str, data: dict = None, files: dict = None) -> dict:
    url = f"{TG_API}/{method}"
    try:
        if files:
            # multipart form upload
            boundary = "----TGBoundary"
            body_parts = []
            if data:
                for k, v in data.items():
                    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
            for fname, (filename, fbytes, ctype) in files.items():
                body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{fname}\"; filename=\"{filename}\"\r\nContent-Type: {ctype}\r\n\r\n".encode())
                body_parts.append(fbytes)
                body_parts.append(b"\r\n")
            body_parts.append(f"--{boundary}--\r\n".encode())
            body = b"".join(body_parts)
            req = urllib.request.Request(url, data=body,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
        elif data:
            req = urllib.request.Request(url, data=json.dumps(data).encode(),
                headers={"Content-Type": "application/json"}, method="POST")
        else:
            req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  TG error [{method}]: {e}")
        return {}


def send_text(chat_id, text: str, buttons: list = None, reply_to: int = None) -> dict:
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_to:
        data["reply_to_message_id"] = reply_to
    if buttons:
        data["reply_markup"] = json.dumps({
            "inline_keyboard": [[
                {"text": b["text"], "callback_data": b["callback_data"]}
                for b in row
            ] for row in buttons]
        })
    return tg("sendMessage", data)


def send_photo(chat_id, image_path: str, caption: str = "", buttons: list = None) -> dict:
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    ext = os.path.splitext(image_path)[1].lower() or ".jpg"
    ctype = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    data = {"chat_id": str(chat_id), "caption": caption, "parse_mode": "Markdown"}
    if buttons:
        data["reply_markup"] = json.dumps({
            "inline_keyboard": [[
                {"text": b["text"], "callback_data": b["callback_data"]}
                for b in row
            ] for row in buttons]
        })
    files = {"photo": (os.path.basename(image_path), img_bytes, ctype)}
    return tg("sendPhoto", data, files)


def send_video(chat_id, video_path: str, caption: str = "", buttons: list = None) -> dict:
    with open(video_path, "rb") as f:
        vid_bytes = f.read()
    data = {"chat_id": str(chat_id), "caption": caption, "parse_mode": "Markdown"}
    if buttons:
        data["reply_markup"] = json.dumps({
            "inline_keyboard": [[
                {"text": b["text"], "callback_data": b["callback_data"]}
                for b in row
            ] for row in buttons]
        })
    files = {"video": (os.path.basename(video_path), vid_bytes, "video/mp4")}
    return tg("sendVideo", data, files)


def answer_callback(callback_id: str, text: str = ""):
    tg("answerCallbackQuery", {"callback_query_id": callback_id, "text": text})


def edit_message(chat_id, message_id: int, text: str, buttons: list = None):
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if buttons:
        data["reply_markup"] = json.dumps({
            "inline_keyboard": [[
                {"text": b["text"], "callback_data": b["callback_data"]}
                for b in row
            ] for row in buttons]
        })
    tg("editMessageText", data)


def download_file(file_id: str, dest_path: str) -> str:
    """Download Telegram file by file_id. Returns local path."""
    resp = tg("getFile", {"file_id": file_id})
    file_path = resp.get("result", {}).get("file_path")
    if not file_path:
        return ""
    url = f"{TG_FILE_API}/{file_path}"
    urllib.request.urlretrieve(url, dest_path)
    return dest_path


# ─── IMAGE GENERATION ────────────────────────────────────────────────
def generate_image(prompt: str, model: str, out_path: str) -> str:
    """Generate image via NVIDIA (Flux or SD3). Returns path or ''."""
    if "sd3" in model or "stable-diffusion-3" in model:
        url, key = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium", "image"
    else:
        url, key = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev", None

    headers = {"Authorization": f"Bearer {NVIDIA_KEY}", "Content-Type": "application/json", "Accept": "application/json"}
    payload = json.dumps({"prompt": prompt}).encode()

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
        b64 = data.get("image") if key else data.get("artifacts", [{}])[0].get("base64", "")

        if not b64:
            # Flux filtered → fallback to SD3
            req2 = urllib.request.Request(
                "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium",
                data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req2, timeout=90) as resp2:
                data2 = json.loads(resp2.read())
            b64 = data2.get("image", "")

        if not b64:
            return ""
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        return out_path
    except Exception as e:
        print(f"  Image gen error: {e}")
        return ""


def submit_i2v(image_path: str, anim_prompt: str, duration: int = 5) -> str:
    """Submit I2V task. Returns task_id."""
    img_bytes = prepare_image_for_i2v(image_path)
    img_b64   = base64.b64encode(img_bytes).decode()

    payload = json.dumps({
        "model": "seedance-1-0-lite-i2v-250428",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}, "role": "first_frame"},
            {"type": "text", "text": anim_prompt}
        ],
        "duration": min(duration, 10),
        "seed": -1
    }).encode()

    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}", "Content-Type": "application/json"}
    try:
        req = urllib.request.Request(f"{BYTEPLUS_BASE}/contents/generations/tasks",
                                     data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read()).get("id", "")
    except Exception as e:
        print(f"  I2V submit error: {e}")
        return ""


def poll_i2v(task_id: str, out_path: str, timeout: int = 300) -> str:
    """Poll I2V task until done. Returns video path or ''."""
    headers = {"Authorization": f"Bearer {BYTEPLUS_KEY}"}
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(6)
        try:
            req = urllib.request.Request(
                f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}", headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            status = data.get("status")
            if status == "succeeded":
                vid_url = data["content"]["video_url"]
                urllib.request.urlretrieve(vid_url, out_path)
                return out_path
            elif status in ("failed", "cancelled"):
                return ""
        except Exception as e:
            print(f"  Poll error: {e}")
    return ""


# ─── GENERATION PIPELINE ─────────────────────────────────────────────
def run_generation_pipeline(chat_id: str, state: dict):
    """
    Full pipeline: Image → QualityGate → (approve) I2V → BGM → Gallery → offer AutoPost
    Runs in a background thread.
    """
    category    = state.get("category", "minuman")
    style       = state.get("style", "dark_moody")
    fmt         = state.get("format", "foto")
    product_img = state.get("product_image")
    product_desc = state.get("product_desc", category)

    project     = f"{category}_{style}_{int(time.time())}"
    out_dir     = os.path.join(OUTPUT_DIR, "wizard_output", project)
    os.makedirs(out_dir, exist_ok=True)

    send_text(chat_id, "⚙️ Generating image dulu... (15-20 detik)")

    config    = get_prompt(category, style, fmt, product_desc)
    img_path  = os.path.join(out_dir, "generated.jpg")
    img_result = generate_image(config["image_prompt"], config["image_model"], img_path)

    if not img_result:
        send_text(chat_id, "❌ Gagal generate image. Coba lagi ya!")
        clear_state(chat_id)
        return

    log_cost("nvidia_flux", "wizard_image", chat_id, project=project)

    # Quality Gate — show image first
    gate_ctx = {"category": category, "style": style, "format": fmt,
                "config": config, "out_dir": out_dir, "project": project,
                "product_desc": product_desc}
    save_gate(chat_id, img_result, gate_ctx)

    preview_text, preview_btns = build_preview_message(img_result)
    send_photo(chat_id, img_result, f"🖼️ *Preview — {style.replace('_',' ').title()}*\n\n{preview_text}", preview_btns)

    # Save image to gallery
    save_result(chat_id, img_result, {
        "type": "image", "category": category, "style": style,
        "format": fmt, "prompt": config["image_prompt"],
        "cost_usd": 0.004, "project": project
    })

    # If format is foto only — done here
    if fmt == "foto":
        reject_gate(chat_id)   # clear gate since no I2V needed
        send_text(chat_id, "✅ *Foto selesai!* Mau diposting ke mana?",
                  _post_buttons_for_file(img_result))
        save_state(chat_id, {**state, "last_output": img_result, "last_type": "image"})
    # If video format — gate will trigger I2V in handle_gate_approve


def run_i2v_pipeline(chat_id: str, gate: dict):
    """Called after quality gate approved. Runs I2V → BGM → gallery → offer post."""
    ctx      = gate["context"]
    config   = ctx["config"]
    out_dir  = ctx["out_dir"]
    project  = ctx["project"]
    category = ctx["category"]
    style    = ctx["style"]
    product_desc = ctx.get("product_desc", category)

    send_text(chat_id, "🎬 Generating video... (30-60 detik) ⏳")

    img_path = gate["image_path"]
    vid_raw  = os.path.join(out_dir, "i2v_raw.mp4")

    task_id = submit_i2v(img_path, config.get("i2v_prompt", f"Animate this {category} product smoothly"))
    if not task_id:
        send_text(chat_id, "❌ Gagal submit I2V task. Coba lagi?",
                  [[{"text": "🔄 Coba Lagi", "callback_data": "gate:retry"},
                    {"text": "❌ Batal", "callback_data": "gate:cancel"}]])
        return

    log_cost("byteplus_lite", "wizard_i2v", chat_id, project=project)
    vid_result = poll_i2v(task_id, vid_raw)

    if not vid_result:
        send_text(chat_id, "❌ Video generation timeout. Coba lagi?",
                  [[{"text": "🔄 Coba Lagi", "callback_data": "gate:retry"},
                    {"text": "❌ Batal", "callback_data": "gate:cancel"}]])
        return

    # Add BGM
    send_text(chat_id, "🎵 Adding BGM...")
    vid_bgm = os.path.join(out_dir, "final_bgm.mp4")
    try:
        bgm_result = add_bgm(vid_raw, category, style)
        final_vid  = bgm_result if bgm_result and os.path.exists(bgm_result) else vid_raw
    except Exception:
        final_vid = vid_raw

    # Save to gallery
    vid_id = save_result(chat_id, final_vid, {
        "type": "video", "category": category, "style": style,
        "format": ctx.get("format", "video_15s"),
        "prompt": config.get("i2v_prompt", ""),
        "cost_usd": 0.054, "project": project
    })

    # Send video to user
    send_video(chat_id, final_vid,
               f"🎬 *{style.replace('_',' ').title()}* — Video siap!\n"
               f"🗂️ Tersimpan di galeri (ID: {vid_id})")

    # Offer auto-post
    caption_data = generate_caption(category, style, ctx.get("product_desc", category))
    post_text, post_btns = build_post_options_message(final_vid, caption_data)

    # Store pending post context
    state = load_state(chat_id)
    save_state(chat_id, {**state,
                         "last_output": final_vid,
                         "last_gallery_id": vid_id,
                         "last_type": "video",
                         "pending_caption": caption_data})

    send_text(chat_id, post_text, post_btns)
    clear_state(chat_id)


def _post_buttons_for_file(file_path: str) -> list:
    creds  = check_credentials()
    ttok   = "✅" if creds["tiktok"] else "🔐"
    igok   = "✅" if creds["instagram"] else "🔐"
    return [
        [{"text": f"{ttok} TikTok", "callback_data": "post:tiktok"},
         {"text": f"{igok} Instagram", "callback_data": "post:instagram"}],
        [{"text": "🗂️ Galeri", "callback_data": "gallery:browse"},
         {"text": "✖️ Skip", "callback_data": "post:skip"}],
    ]


# ─── CALLBACK ROUTING ────────────────────────────────────────────────
def handle_callback(cb: dict):
    callback_id = cb["id"]
    chat_id     = str(cb["message"]["chat"]["id"])
    msg_id      = cb["message"]["message_id"]
    data        = cb.get("data", "")
    state       = load_state(chat_id)

    answer_callback(callback_id)

    # ── WIZARD callbacks ─────────────────────────────────────────────
    if data.startswith("wiz:cat:"):
        cat = data.split(":", 2)[2]
        save_state(chat_id, {**state, "category": cat})
        text, btns = build_style_message(cat)
        edit_message(chat_id, msg_id, text, btns)

    elif data.startswith("wiz:style:"):
        style = data.split(":", 2)[2]
        new_state = {**state, "style": style}
        save_state(chat_id, new_state)
        text, btns = build_format_message(style)
        edit_message(chat_id, msg_id, text, btns)

    elif data.startswith("wiz:fmt:"):
        fmt = data.split(":", 2)[2]
        new_state = {**state, "format": fmt}
        save_state(chat_id, new_state)
        text, btns = build_confirm_message(new_state)
        edit_message(chat_id, msg_id, text, btns)

    elif data == "wiz:generate":
        edit_message(chat_id, msg_id, "✅ Oke! Mulai generate...", [])
        threading.Thread(target=run_generation_pipeline, args=(chat_id, state), daemon=True).start()

    elif data in ("wiz:restart", "wiz:reset"):
        clear_state(chat_id)
        text, btns = build_category_message()
        edit_message(chat_id, msg_id, text, btns)

    # ── QUALITY GATE callbacks ────────────────────────────────────────
    elif data == "gate:approve":
        gate = get_gate(chat_id)
        if not gate or gate.get("status") != "pending":
            send_text(chat_id, "⚠️ Tidak ada quality gate aktif.")
            return
        approve_gate(chat_id)
        edit_message(chat_id, msg_id, "✅ Approved! Starting video generation...")
        threading.Thread(target=run_i2v_pipeline, args=(chat_id, gate), daemon=True).start()

    elif data == "gate:retry":
        gate = get_gate(chat_id)
        reject_gate(chat_id)
        edit_message(chat_id, msg_id, "🔄 OK, regenerate image dulu...")
        if gate:
            ctx = gate.get("context", {})
            # Rebuild state and retry image gen
            retry_state = {
                "category": ctx.get("category", state.get("category")),
                "style":    ctx.get("style", state.get("style")),
                "format":   ctx.get("format", state.get("format")),
                "product_desc": ctx.get("product_desc", state.get("product_desc")),
            }
            threading.Thread(target=run_generation_pipeline, args=(chat_id, retry_state), daemon=True).start()

    elif data == "gate:cancel":
        reject_gate(chat_id)
        clear_state(chat_id)
        edit_message(chat_id, msg_id, "❌ Dibatalkan. Kirim foto produk baru untuk mulai lagi.")

    # ── GALLERY callbacks ─────────────────────────────────────────────
    elif data == "gallery:browse" or data == "gallery:list:0":
        text, btns = build_gallery_message(chat_id)
        send_text(chat_id, text, btns)

    elif data.startswith("gallery:list:"):
        offset = int(data.split(":")[-1])
        results = get_results(chat_id, limit=5, offset=offset)
        if not results:
            send_text(chat_id, "📭 Galeri kosong.")
            return
        lines = [f"🗂️ *Galeri (offset {offset}):*\n"]
        for r in results:
            emoji = "🖼️" if r["type"] == "image" else "🎬"
            lines.append(f"{emoji} ID {r['id']} — {r['category']} × {r['style']}")
        btns = [[{"text": f"{'🖼️' if r['type']=='image' else '🎬'} ID {r['id']}", "callback_data": f"gallery:view:{r['id']}"}
                 for r in results[:3]]]
        if offset >= 5:
            btns.append([{"text": "◀ Prev", "callback_data": f"gallery:list:{offset-5}"},
                          {"text": "Next ▶", "callback_data": f"gallery:list:{offset+5}"}])
        else:
            btns.append([{"text": "Next ▶", "callback_data": f"gallery:list:{offset+5}"}])
        btns.append([{"text": "✖️ Tutup", "callback_data": "gallery:close"}])
        send_text(chat_id, "\n".join(lines), btns)

    elif data.startswith("gallery:view:"):
        rid = int(data.split(":")[-1])
        r   = get_result(rid)
        if not r:
            send_text(chat_id, "❌ Konten tidak ditemukan.")
            return
        emoji = "🖼️" if r["type"] == "image" else "🎬"
        text  = (f"{emoji} *Konten ID {rid}*\n"
                 f"Kategori: {r['category']} × {r['style']}\n"
                 f"Format: {r['format']}\n"
                 f"Cost: ${r['cost_usd']:.4f}\n"
                 f"Posted ke: {r['posted_to']}")
        btns  = [
            [{"text": "📤 Post TikTok", "callback_data": f"gallery:post:{rid}:tiktok"},
             {"text": "📤 Post IG",    "callback_data": f"gallery:post:{rid}:instagram"}],
            [{"text": "⭐⭐⭐ Rate",   "callback_data": f"gallery:rate:{rid}:3"},
             {"text": "🗑️ Hapus",     "callback_data": f"gallery:delete:{rid}"}],
            [{"text": "◀ Back",       "callback_data": "gallery:browse"}],
        ]
        if r["type"] == "image" and os.path.exists(r.get("file_path", "")):
            send_photo(chat_id, r["file_path"], text, btns)
        elif r["type"] == "video" and os.path.exists(r.get("file_path", "")):
            send_video(chat_id, r["file_path"], text, btns)
        else:
            send_text(chat_id, text + "\n\n⚠️ File tidak ditemukan.", btns)

    elif data.startswith("gallery:delete:"):
        rid = int(data.split(":")[-1])
        delete_result(rid)
        edit_message(chat_id, msg_id, f"🗑️ Konten ID {rid} dihapus.",
                     [[{"text": "◀ Kembali ke Galeri", "callback_data": "gallery:browse"}]])

    elif data.startswith("gallery:rate:"):
        parts = data.split(":")
        rid, stars = int(parts[2]), int(parts[3])
        rate_result(rid, stars)
        answer_callback(callback_id, f"{'⭐'*stars} Rating tersimpan!")

    elif data.startswith("gallery:post:"):
        parts    = data.split(":")
        rid      = int(parts[2])
        platform = parts[3]
        r        = get_result(rid)
        if not r or not os.path.exists(r.get("file_path", "")):
            send_text(chat_id, "❌ File tidak ditemukan.")
            return
        caption_data = generate_caption(r["category"], r["style"], r["category"])
        qid = queue_post(r["file_path"], platform, caption_data, chat_id)
        mark_posted(rid, platform)
        send_text(chat_id, f"✅ Ditambahkan ke queue posting ({platform})\nQueue ID: `{qid}`")

    elif data == "gallery:costs":
        text = build_dashboard_message(chat_id)
        send_text(chat_id, text, [[{"text": "✖️ Tutup", "callback_data": "gallery:close"}]])

    elif data == "gallery:close":
        edit_message(chat_id, msg_id, "✖️ Galeri ditutup.")

    # ── BATCH callbacks ───────────────────────────────────────────────
    elif data.startswith("batch:style:"):
        cat = data.split(":")[-1]
        save_state(chat_id, {**state, "batch_mode": "style_sweep", "batch_category": cat})
        est = estimate_generation_cost("foto")
        total_est = est["total_usd"] * 5
        send_text(chat_id, (
            f"🎨 *Style Sweep — {cat}*\n\n"
            f"Generate 5 style berbeda:\n"
            f"Dark & Moody, Clean Studio, Luxury Gold, Dramatic Detail, Lifestyle\n\n"
            f"💰 Estimasi: ~${total_est:.2f} (~Rp {int(total_est*IDR_RATE):,})\n\n"
            f"Lanjut?"
        ), [[{"text": "🚀 Mulai Batch!", "callback_data": f"batch:run:style:{cat}"},
              {"text": "❌ Batal", "callback_data": "batch:cancel"}]])

    elif data.startswith("batch:run:style:"):
        cat = data.split(":")[-1]
        prod_desc = state.get("product_desc", cat)
        out_dir   = os.path.join(OUTPUT_DIR, f"batch_{cat}_{int(time.time())}")
        edit_message(chat_id, msg_id, f"🚀 Batch style sweep dimulai...\n5 variasi {cat} sedang di-generate!\n⏳ Estimasi: 3-5 menit")
        threading.Thread(
            target=_run_batch_bg,
            args=(chat_id, state.get("product_image", ""), cat, prod_desc, out_dir, "style_sweep"),
            daemon=True
        ).start()

    elif data.startswith("batch:format:"):
        cat = data.split(":")[-1]
        send_text(chat_id, "Format sweep (Foto, 15s, 30s) — Coming soon! Pakai style sweep dulu ya.",
                  [[{"text": "🎨 Style Sweep", "callback_data": f"batch:style:{cat}"}]])

    elif data == "batch:cancel":
        edit_message(chat_id, msg_id, "❌ Batch dibatalkan.")

    # ── AUTO POST callbacks ───────────────────────────────────────────
    elif data == "post:tiktok" or data == "post:instagram":
        platform     = data.split(":")[1]
        last_output  = state.get("last_output")
        caption_data = state.get("pending_caption", {})
        if not last_output or not os.path.exists(last_output):
            send_text(chat_id, "❌ Tidak ada file untuk diposting.")
            return
        creds = check_credentials()
        if not creds.get(platform):
            send_text(chat_id, f"⚠️ Token untuk {platform} belum dikonfigurasi.\n"
                               f"Set env: TIKTOK_ACCESS_TOKEN / INSTAGRAM_ACCESS_TOKEN")
            return
        qid = queue_post(last_output, platform, caption_data, chat_id)
        if state.get("last_gallery_id"):
            mark_posted(state["last_gallery_id"], platform)
        edit_message(chat_id, msg_id,
                     f"✅ *Ditambahkan ke posting queue!*\n"
                     f"Platform: {platform}\nQueue ID: `{qid}`\n\n"
                     f"Jalankan `process_queue()` untuk kirim.")

    elif data == "post:skip":
        edit_message(chat_id, msg_id, "✅ Selesai! Konten tersimpan di galeri kamu. /gallery")

    elif data == "post:edit":
        send_text(chat_id, "✏️ Kirim caption baru (text saja):")
        save_state(chat_id, {**state, "awaiting": "edit_caption"})

    # ── DASHBOARD callbacks ───────────────────────────────────────────
    elif data == "dash:refresh":
        text = build_dashboard_message(chat_id)
        edit_message(chat_id, msg_id, text,
                     [[{"text": "🔄 Refresh", "callback_data": "dash:refresh"},
                       {"text": "✖️ Tutup", "callback_data": "dash:close"}]])

    elif data == "dash:close":
        edit_message(chat_id, msg_id, "📊 Dashboard ditutup.")

    else:
        print(f"  Unknown callback: {data}")


def _run_batch_bg(chat_id: str, image_path: str, category: str,
                   product_desc: str, out_dir: str, mode: str):
    """Run batch in background thread, send results to chat."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_batch(
            image_path=image_path, category=category, product_desc=product_desc,
            output_dir=out_dir, mode=mode, chat_id=chat_id
        ))
        loop.close()

        success = result.get("success", 0)
        total   = result.get("total", 0)
        est     = result.get("estimate", {})
        send_text(chat_id,
                  f"🎉 *Batch selesai!* {success}/{total} berhasil\n"
                  f"💰 Cost: ~${est.get('total_usd', 0):.3f} "
                  f"(~Rp {est.get('total_idr', 0):,})")

        for r in result.get("results", []):
            if r.get("video") and os.path.exists(r["video"]):
                style_label = r["style"].replace("_", " ").title()
                vid_id = save_result(chat_id, r["video"], {
                    "type": "video", "category": category,
                    "style": r["style"], "format": r.get("format", "foto"),
                    "cost_usd": 0.054, "project": os.path.basename(out_dir)
                })
                send_video(chat_id, r["video"],
                           f"{r['status']} *{r['idx']}/5 — {style_label}*\n"
                           f"Professional minimal showcase\nGaleri ID: {vid_id}")
                time.sleep(1)  # Rate limit
    except Exception as e:
        traceback.print_exc()
        send_text(chat_id, f"❌ Batch error: {e}")


# ─── MESSAGE ROUTING ─────────────────────────────────────────────────
def handle_message(msg: dict):
    chat_id = str(msg["chat"]["id"])
    text    = msg.get("text", "")
    state   = load_state(chat_id)

    # PHOTO → start wizard
    if "photo" in msg:
        photos   = msg["photo"]
        file_id  = photos[-1]["file_id"]   # largest size
        dest     = os.path.join(OUTPUT_DIR, f"product_{chat_id}_{int(time.time())}.jpg")
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        send_text(chat_id, "Hei! Foto produknya udah aku terima nih 🎉\nLagi analisis dulu ya...")
        download_file(file_id, dest)

        # Try vision detection (import dynamically to avoid crash if missing)
        detected = {}
        try:
            sys.path.insert(0, os.path.dirname(__file__))
            from vision_detector import detect_product
            detected = detect_product(dest)
        except Exception:
            pass

        save_state(chat_id, {
            "product_image": dest,
            "product_desc": detected.get("product_name", "produk"),
            "detected_category": detected.get("category")
        })

        text_msg, btns = build_category_message(detected if detected else None)
        send_text(chat_id, text_msg, btns)
        return

    # COMMANDS
    if text.startswith("/start"):
        send_text(chat_id,
                  "👋 Halo! Aku *BerkahKarya Bot* 🔥\n\n"
                  "Kirim foto produkmu untuk mulai generate konten marketing!\n\n"
                  "Perintah lainnya:\n"
                  "📊 /dashboard — Cost tracker\n"
                  "🗂️ /gallery — Galeri konten\n"
                  "🚀 /batch — Batch generate\n"
                  "❓ /help — Bantuan")
        return

    if text.startswith("/dashboard"):
        txt = build_dashboard_message(chat_id)
        send_text(chat_id, txt,
                  [[{"text": "🔄 Refresh", "callback_data": "dash:refresh"},
                    {"text": "✖️ Tutup",   "callback_data": "dash:close"}]])
        return

    if text.startswith("/gallery"):
        txt, btns = build_gallery_message(chat_id)
        send_text(chat_id, txt, btns)
        return

    if text.startswith("/batch"):
        if state.get("category"):
            txt, btns = build_batch_options_message(state["category"])
        else:
            txt   = "🚀 *Batch Generation*\n\nKirim foto produk dulu, atau pilih kategori:"
            btns  = [[{"text": v["label"], "callback_data": f"batch:style:{k}"}]
                     for k, v in list(CATEGORIES.items())[:4]]
        send_text(chat_id, txt, btns)
        return

    if text.startswith("/help"):
        send_text(chat_id,
                  "❓ *BerkahKarya Bot Help*\n\n"
                  "1️⃣ Kirim foto produk → Bot detect otomatis\n"
                  "2️⃣ Pilih kategori, style, format\n"
                  "3️⃣ Approve preview image → Generate video\n"
                  "4️⃣ BGM ditambah otomatis\n"
                  "5️⃣ Post ke TikTok / Instagram\n\n"
                  "*Format output:*\n"
                  "• Foto — Image saja\n"
                  "• Video 15s — I2V pendek\n"
                  "• Video 30s — I2V lebih panjang\n\n"
                  "*Perintah:*\n"
                  "/gallery /dashboard /batch")
        return

    # STATE: awaiting caption edit
    if state.get("awaiting") == "edit_caption" and text:
        save_state(chat_id, {**state, "pending_caption": {"caption": text, "hashtags": []}, "awaiting": None})
        send_text(chat_id, "✅ Caption diupdate!",
                  [[{"text": "📤 Post TikTok", "callback_data": "post:tiktok"},
                    {"text": "📤 Post IG",     "callback_data": "post:instagram"}],
                   [{"text": "✖️ Skip",         "callback_data": "post:skip"}]])
        return

    # Fallback
    if text and not text.startswith("/"):
        send_text(chat_id,
                  "📸 Kirim foto produkmu untuk mulai, atau ketik /help",
                  [[{"text": "🗂️ Galeri", "callback_data": "gallery:browse"},
                    {"text": "💰 Dashboard", "callback_data": "dash:refresh"}]])


# ─── MAIN POLLING LOOP ───────────────────────────────────────────────
def main():
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        return

    print("🤖 BerkahKarya Bot starting...")
    print(f"   NVIDIA key: {'✅' if NVIDIA_KEY else '❌'}")
    print(f"   BytePlus key: {'✅' if BYTEPLUS_KEY else '❌'}")

    offset = 0
    print("✅ Polling for updates...")

    while True:
        try:
            resp = tg("getUpdates", {"offset": offset, "timeout": 30, "limit": 10})
            updates = resp.get("result", [])

            for upd in updates:
                offset = upd["update_id"] + 1
                try:
                    if "callback_query" in upd:
                        handle_callback(upd["callback_query"])
                    elif "message" in upd:
                        handle_message(upd["message"])
                except Exception as e:
                    traceback.print_exc()
                    print(f"  Error handling update: {e}")

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped.")
            break
        except Exception as e:
            print(f"  Polling error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
