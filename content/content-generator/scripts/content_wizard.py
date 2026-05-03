"""
Content Wizard — State Manager
Handles step-by-step guided flow for Telegram users.
State persisted in wizard_state.json between messages.

Flow:
  1. User kirim foto produk
  2. Bot auto-detect → tampil pilihan kategori (confirm/ganti)
  3. User pilih style
  4. User pilih format output
  5. Generate!
"""

import json, os, time
from prompt_library import CATEGORIES, STYLES, FORMATS, get_prompt

STATE_FILE = "/home/openclaw/.openclaw/workspace/output/wizard_state.json"
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)


# ─── STATE MANAGER ────────────────────────────────────────────────────
def load_state(chat_id: str) -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            all_states = json.load(f)
        return all_states.get(str(chat_id), {})
    return {}

def save_state(chat_id: str, state: dict):
    all_states = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            all_states = json.load(f)
    all_states[str(chat_id)] = {**state, "updated_at": time.time()}
    with open(STATE_FILE, "w") as f:
        json.dump(all_states, f, indent=2)

def clear_state(chat_id: str):
    all_states = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            all_states = json.load(f)
    all_states.pop(str(chat_id), None)
    with open(STATE_FILE, "w") as f:
        json.dump(all_states, f, indent=2)


# ─── MESSAGE BUILDERS ─────────────────────────────────────────────────
def build_category_message(detected: dict = None) -> tuple[str, list]:
    """Step 1: Pilih kategori produk"""

    if detected and detected.get("confidence") in ("high", "medium") and detected.get("category"):
        cat = detected["category"]
        cat_label = CATEGORIES.get(cat, {}).get("label", cat)
        text = (
            f"Hei! Foto produknya udah aku terima nih 🎉\n\n"
            f"Kayaknya ini produk **{cat_label}** ya — *{detected.get('product_desc', '')}*?\n\n"
            f"Kalau bener, langsung lanjut! Kalau salah, pilih kategori yang tepat di bawah 👇"
        )
        buttons = []
        # First row: confirm detected
        buttons.append([{"text": f"✅ Bener, {cat_label}!", "callback_data": f"wiz:cat:{cat}"}])
        # Other categories
        row = []
        for k, v in CATEGORIES.items():
            if k != cat:
                row.append({"text": v["label"], "callback_data": f"wiz:cat:{k}"})
                if len(row) == 2:
                    buttons.append(row)
                    row = []
        if row:
            buttons.append(row)
    else:
        text = (
            "Hei! Foto produknya udah aku terima nih 🎉\n\n"
            "Yuk mulai! Ini produk kamu masuk kategori apa? 👇"
        )
        buttons = []
        row = []
        for k, v in CATEGORIES.items():
            row.append({"text": v["label"], "callback_data": f"wiz:cat:{k}"})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

    return text, buttons


def build_style_message(category: str) -> tuple[str, list]:
    """Step 2: Pilih visual style"""
    cat_label = CATEGORIES.get(category, {}).get("label", category)
    text = (
        f"Oke, kategori **{cat_label}** ✅\n\n"
        f"Sekarang, pilih vibe visual yang paling cocok buat produk kamu 🎨"
    )
    buttons = []
    row = []
    for k, v in STYLES.items():
        row.append({"text": v["label"], "callback_data": f"wiz:style:{k}"})
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return text, buttons


def build_format_message(style: str) -> tuple[str, list]:
    """Step 3: Pilih format output"""
    style_label = STYLES.get(style, {}).get("label", style)
    text = (
        f"Style **{style_label}** — pilihan yang mantap! 🔥\n\n"
        f"Terakhir, mau output dalam format apa?"
    )
    buttons = []
    row = []
    for k, v in FORMATS.items():
        row.append({"text": v["label"], "callback_data": f"wiz:fmt:{k}"})
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return text, buttons


def build_confirm_message(state: dict) -> tuple[str, list]:
    """Step 4: Konfirmasi sebelum generate"""
    cat  = state.get("category")
    sty  = state.get("style")
    fmt  = state.get("format")
    desc = state.get("product_desc", "produk kamu")

    cat_label = CATEGORIES.get(cat, {}).get("label", cat)
    sty_label = STYLES.get(sty, {}).get("label", sty)
    fmt_label = FORMATS.get(fmt, {}).get("label", fmt)

    text = (
        f"Sip! Ini summary pilihan kamu:\n\n"
        f"📦 Produk: {cat_label}\n"
        f"🎨 Style: {sty_label}\n"
        f"📤 Format: {fmt_label}\n\n"
        f"Langsung gaskeun? 🚀"
    )
    buttons = [
        [
            {"text": "🚀 Gas Generate!", "callback_data": "wiz:generate"},
            {"text": "🔄 Ulang dari awal", "callback_data": "wiz:reset"},
        ]
    ]
    return text, buttons


def build_generating_message(state: dict) -> str:
    """Message saat proses generate"""
    sty_label = STYLES.get(state.get("style"), {}).get("label", "")
    return (
        f"Oke, lagi dimasak nih... 🔥\n\n"
        f"Hasilnya bakal keluar dalam 30-60 detik.\n"
        f"Sambil nunggu, minum kopi dulu ☕"
    )


# ─── WIZARD ROUTER ────────────────────────────────────────────────────
def handle_callback(callback_data: str, chat_id: str) -> dict:
    """
    Process a button callback and return next action.
    Returns dict with: message, buttons, action
    """
    state = load_state(chat_id)
    parts = callback_data.split(":")

    if len(parts) < 2 or parts[0] != "wiz":
        return {"action": "ignore"}

    step = parts[1]

    if step == "reset":
        clear_state(chat_id)
        return {
            "action": "message",
            "text": "Oke, mulai dari awal ya! Kirim foto produk kamu 📸",
            "buttons": None
        }

    elif step == "cat":
        category = parts[2]
        state["category"] = category
        state["step"] = "style"
        save_state(chat_id, state)
        text, buttons = build_style_message(category)
        return {"action": "message", "text": text, "buttons": buttons}

    elif step == "style":
        style = parts[2]
        state["style"] = style
        state["step"] = "format"
        save_state(chat_id, state)
        text, buttons = build_format_message(style)
        return {"action": "message", "text": text, "buttons": buttons}

    elif step == "fmt":
        fmt = parts[2]
        state["format"] = fmt
        state["step"] = "confirm"
        save_state(chat_id, state)
        text, buttons = build_confirm_message(state)
        return {"action": "message", "text": text, "buttons": buttons}

    elif step == "generate":
        state["step"] = "generating"
        save_state(chat_id, state)
        return {
            "action": "generate",
            "state": state,
            "text": build_generating_message(state)
        }

    return {"action": "ignore"}


def handle_image(image_path: str, chat_id: str, detected: dict = None) -> dict:
    """Called when user sends a product image"""
    state = {
        "step": "category",
        "image_path": image_path,
        "category": None,
        "style": None,
        "format": None,
        "product_desc": detected.get("product_desc", "produk") if detected else "produk",
        "detected": detected or {},
    }
    save_state(chat_id, state)
    text, buttons = build_category_message(detected)
    return {"action": "message", "text": text, "buttons": buttons}


def get_final_prompt(chat_id: str) -> dict:
    """Get the final prompt config ready for generation"""
    state = load_state(chat_id)
    category = state.get("category")
    style = state.get("style")
    fmt = state.get("format")
    product_desc = state.get("product_desc", "the product")
    image_path = state.get("image_path")

    prompt_config = get_prompt(category, style, fmt, product_desc)
    prompt_config["image_path"] = image_path
    prompt_config["format"] = fmt
    return prompt_config


if __name__ == "__main__":
    # Quick test
    print("Testing wizard flow...")
    test_detected = {
        "category": "minuman",
        "style_recommendation": "dark_moody",
        "product_desc": "botol jus mangga premium",
        "confidence": "high",
    }
    result = handle_image("/tmp/test.jpg", "test_chat", test_detected)
    print("Step 1 message:", result["text"][:100])
    print("Buttons:", [[b["text"] for b in row] for row in result["buttons"]])
