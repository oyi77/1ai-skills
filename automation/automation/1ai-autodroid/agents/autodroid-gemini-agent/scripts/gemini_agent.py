#!/usr/bin/env python3
"""
autodroid-gemini-agent v3.0 — Robust Gemini Android automation

State-machine based. Verifies every step. Retries on failure.
No API key needed — controls real app via ADB.

Commands:
  status                              -- check app + device
  chat   --prompt TEXT [--timeout N]  -- send chat, get response
  imagine --prompt TEXT [--out PATH]  -- generate image, save PNG
  screenshot [--out PATH]             -- capture screen
  server [--port N]                   -- start FastAPI server

Tested: Redmi 2409BRN2CY, Android 14, 720x1640, Gemini app ~2026-03
"""

import argparse
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

PACKAGE = "com.google.android.apps.bard"
DOWNLOADS = Path(os.path.expanduser("~/.openclaw/workspace/downloads"))
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

DISMISS_LABELS = {
    "Skip", "Got it", "Not now", "No thanks", "Continue", "Allow",
    "Get started", "Accept", "OK", "Dismiss", "Close", "Agree",
    "Lewati", "Lanjutkan", "Izinkan", "Tidak sekarang", "Oke", "Siap",
    "Lain kali",
}
UI_CHROME = {
    "Buka sidebar", "Chat baru", "Bagikan", "Opsi lainnya",
    "Respons baik", "Respons buruk", "Opsi ulangi", "Tambahkan lampiran",
    "Alat Gambar", "Cepat", "Penalaran", "Pro", "Mikrofon",
    "Open Gemini Live", "Kirim", "Salin", "Simpan", "Download gambar",
    "Kembali", "Scroll ke bawah", "Scroll ke atas",
    "Gemini adalah AI dan dapat melakukan kesalahan.",
    "Sentuh lama gambar untuk menyalin, menyimpan, atau membagikan",
    "Bicara dengan Gemini secara handsfree",
}


# ─── Low-level ADB ──────────────────────────────────────────────────────────

def adb(*args, device=None, binary=False, check=False):
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += list(args)
    if binary:
        r = subprocess.run(cmd, capture_output=True)
        return r.stdout
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"adb {args[0]} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def tap(x, y, device=None):
    adb("shell", "input", "tap", str(x), str(y), device=device)


def swipe(x1, y1, x2, y2, duration=300, device=None):
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration), device=device)


def keyevent(key, device=None):
    adb("shell", "input", "keyevent", str(key), device=device)


def type_word(word, device=None):
    safe = "".join(c for c in word if c.isalnum() or c in "-_@.")
    if safe:
        adb("shell", "input", "text", safe, device=device)


def type_text(text, device=None):
    for i, word in enumerate(text.split()):
        type_word(word, device=device)
        time.sleep(0.08)
        if i < len(text.split()) - 1:
            keyevent("KEYCODE_SPACE", device=device)
            time.sleep(0.05)


def wake(device=None):
    keyevent(224, device=device)
    time.sleep(0.5)
    swipe(360, 1400, 360, 700, duration=200, device=device)
    time.sleep(0.6)


def screencap(path, device=None):
    wake(device=device)
    data = adb("exec-out", "screencap", "-p", device=device, binary=True)
    Path(path).write_bytes(data)
    return str(path)


# ─── UI Parsing ─────────────────────────────────────────────────────────────

def dump_ui(device=None):
    remote = "/sdcard/gai_dump.xml"
    local = "/tmp/gai_dump.xml"
    adb("shell", "uiautomator", "dump", remote, device=device)
    adb("pull", remote, local, device=device)
    try:
        root = ET.parse(local).getroot()
        nodes = []
        for n in root.iter():
            text = (n.get("text") or "").strip()
            desc = (n.get("content-desc") or "").strip()
            cls = n.get("class", "").split(".")[-1]
            bounds = n.get("bounds", "")
            label = text or desc
            if label and bounds:
                nodes.append({
                    "label": label, "text": text, "desc": desc,
                    "class": cls, "bounds": bounds,
                })
        return nodes
    except ET.ParseError:
        return []


def bounds_to_center(b):
    try:
        vals = b.replace("][", ",").replace("[", "").replace("]", "").split(",")
        l, t, r, bo = map(int, vals)
        return (l + r) // 2, (t + bo) // 2
    except Exception:
        return None


def find_node(nodes, label=None, cls=None, partial=False):
    for n in nodes:
        if label:
            match = (n["label"] == label) if not partial else (label in n["label"])
            if not match:
                continue
        if cls and cls not in n["class"]:
            continue
        return n
    return None


def tap_node(nodes, label=None, cls=None, partial=False, device=None):
    n = find_node(nodes, label=label, cls=cls, partial=partial)
    if n:
        c = bounds_to_center(n["bounds"])
        if c:
            tap(*c, device=device)
            return True
    return False


# ─── Screen State Detection ──────────────────────────────────────────────────

def detect_screen(nodes):
    labels = {n["label"] for n in nodes}
    classes = {n["class"] for n in nodes}

    has_input = any("EditText" in n["class"] for n in nodes)
    has_chat_input = any(n["label"] in ("Minta Gemini", "Ask Gemini", "Message Gemini") for n in nodes)
    has_img_input = any("Deskripsikan" in n["label"] for n in nodes)
    has_response = any(
        len(n["text"]) > 30
        and n["text"] not in UI_CHROME
        and n["class"] in ("TextView",)
        for n in nodes
    )
    has_generated_img = any("Gambar yang dibuat" in n["label"] for n in nodes)
    has_viewer = any("Gambar yang dihasilkan" in n["label"] for n in nodes)
    has_download = any("Download gambar" in n["label"] or n.get("desc") == "Download gambar" for n in nodes)
    is_lockscreen = any("systemui" in n.get("desc", "").lower() or "keyguard" in n.get("label", "").lower() for n in nodes)

    if has_viewer or has_download:
        return "VIEWER"
    if has_generated_img:
        return "CHAT_WITH_IMAGE"
    if has_img_input:
        return "IMAGE_GEN"
    if has_chat_input:
        return "HOME"
    if has_response:
        return "CHAT"
    if is_lockscreen or not nodes:
        return "LOCK"
    return "UNKNOWN"


# ─── High-level Actions ──────────────────────────────────────────────────────

def launch_gemini(device=None):
    wake(device=device)
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(0.5)
    adb("shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1",
        device=device)
    time.sleep(3.5)
    wake(device=device)


def dismiss_all_popups(nodes, device=None):
    dismissed = 0
    for n in nodes:
        if n["label"] in DISMISS_LABELS:
            c = bounds_to_center(n["bounds"])
            if c:
                tap(*c, device=device)
                time.sleep(0.4)
                dismissed += 1
    return dismissed


def ensure_home_screen(device=None, max_attempts=3):
    for attempt in range(max_attempts):
        nodes = dump_ui(device=device)
        state = detect_screen(nodes)
        if state == "HOME":
            return True
        if state == "LOCK":
            wake(device=device)
            time.sleep(1)
            continue
        if state in ("CHAT", "CHAT_WITH_IMAGE", "IMAGE_GEN", "VIEWER"):
            launch_gemini(device=device)
            nodes = dump_ui(device=device)
            dismiss_all_popups(nodes, device=device)
            time.sleep(0.5)
            continue
        if state == "UNKNOWN":
            wake(device=device)
            time.sleep(1)
    return False


def open_image_gen(device=None, max_attempts=4):
    for attempt in range(max_attempts):
        nodes = dump_ui(device=device)
        state = detect_screen(nodes)
        print(f"[open_image_gen] state={state} attempt={attempt+1}", file=sys.stderr)

        if state == "IMAGE_GEN":
            return True

        dismiss_all_popups(nodes, device=device)
        time.sleep(0.3)
        nodes = dump_ui(device=device)

        if find_node(nodes, label="🖼️ Buat Gambar"):
            tap_node(nodes, label="🖼️ Buat Gambar", device=device)
            time.sleep(1.5)
            continue

        if find_node(nodes, label="Chat baru"):
            tap_node(nodes, label="Chat baru", device=device)
            time.sleep(2)
            nodes = dump_ui(device=device)
            if find_node(nodes, label="🖼️ Buat Gambar"):
                tap_node(nodes, label="🖼️ Buat Gambar", device=device)
                time.sleep(1.5)
                continue

        if state == "LOCK":
            wake(device=device)
            time.sleep(1)
            continue

        launch_gemini(device=device)
    return False


def type_in_field(text, field_label, fallback_xy, device=None):
    nodes = dump_ui(device=device)
    field = find_node(nodes, label=field_label) or find_node(nodes, label=field_label, partial=True)
    if field:
        c = bounds_to_center(field["bounds"])
        if c:
            tap(*c, device=device)
    else:
        tap(*fallback_xy, device=device)
    time.sleep(0.8)
    clear_field(device=device)
    type_text(text, device=device)
    time.sleep(0.4)


def clear_field(device=None):
    keyevent("KEYCODE_CTRL_A", device=device)
    time.sleep(0.1)
    keyevent("KEYCODE_DEL", device=device)
    time.sleep(0.1)


def send(device=None):
    nodes = dump_ui(device=device)
    send_node = (find_node(nodes, label="Kirim") or
                 find_node(nodes, desc="Kirim") or
                 find_node(nodes, label="Send"))
    if send_node:
        c = bounds_to_center(send_node["bounds"])
        if c:
            tap(*c, device=device)
            return True
    tap(648, 963, device=device)
    return False


RESPONSE_SKIP = {
    "Gemini adalah AI dan dapat melakukan kesalahan.",
    "Sentuh lama gambar untuk menyalin, menyimpan, atau membagikan",
    "Bicara dengan Gemini secara handsfree",
}

def wait_for_response(timeout=60, device=None):
    deadline = time.time() + timeout
    seen = set()
    while time.time() < deadline:
        time.sleep(2.5)
        nodes = dump_ui(device=device)
        candidates = []
        for n in nodes:
            t = n["text"]
            if not t or len(t) < 30:
                continue
            if n["class"] not in ("TextView",):
                continue
            if t in UI_CHROME or t in DISMISS_LABELS or t in RESPONSE_SKIP:
                continue
            if any(t.startswith(e) for e in ("🖼", "🎸", "✨", "📄", "📚")):
                continue
            candidates.append(t)
        if candidates:
            best = max(candidates, key=len)
            if best not in seen:
                seen.add(best)
                return best
    return None


def save_generated_image(ts_before, device=None):
    nodes = dump_ui(device=device)
    state = detect_screen(nodes)

    if state == "VIEWER":
        return _download_from_viewer(ts_before, device=device)

    if state == "CHAT_WITH_IMAGE":
        img_node = find_node(nodes, label="Gambar yang dibuat 1") or \
                   find_node(nodes, partial=True, label="Gambar yang dibuat")
        if img_node:
            c = bounds_to_center(img_node["bounds"])
            if c:
                tap(*c, device=device)
                time.sleep(1.5)
                nodes2 = dump_ui(device=device)
                state2 = detect_screen(nodes2)
                if state2 == "VIEWER":
                    return _download_from_viewer(ts_before, device=device)
    return None


def _download_from_viewer(ts_before, device=None):
    nodes = dump_ui(device=device)
    dl_node = (find_node(nodes, label="Download gambar") or
               find_node(nodes, desc="Download gambar") or
               find_node(nodes, label="Simpan"))
    if dl_node:
        c = bounds_to_center(dl_node["bounds"])
        if c:
            tap(*c, device=device)
            time.sleep(3)
            return _get_latest_mediastore_image(ts_before, device=device)
    return None


def _get_latest_mediastore_image(ts_before, device=None):
    out = adb("shell", "content", "query",
              "--uri", "content://media/external/images/media",
              "--projection", "_id:_display_name:_data:date_added",
              device=device)
    best_path, best_ts = None, ts_before
    for line in out.splitlines():
        try:
            if "date_added=" not in line or "_data=" not in line:
                continue
            ts = int(line.split("date_added=")[1].split(",")[0].strip())
            path = line.split("_data=")[1].split(",")[0].strip()
            if ts > best_ts:
                best_ts, best_path = ts, path
        except Exception:
            continue
    return best_path


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_status(device=None):
    installed = PACKAGE in adb("shell", "pm", "list", "packages", PACKAGE, device=device)
    model = adb("shell", "getprop", "ro.product.model", device=device)
    android = adb("shell", "getprop", "ro.build.version.release", device=device)
    devices = [l.split()[0] for l in adb("devices").splitlines()[1:] if "\tdevice" in l]
    result = {
        "gemini_installed": installed,
        "package": PACKAGE,
        "device": device or (devices[0] if devices else "none"),
        "model": model,
        "android_version": android,
        "connected_devices": devices,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_chat(prompt, device=None, timeout=60, max_retries=3):
    for attempt in range(1, max_retries + 1):
        print(f"[chat] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            print("[chat] Launching Gemini...", file=sys.stderr)
            launch_gemini(device=device)

            nodes = dump_ui(device=device)
            dismiss_all_popups(nodes, device=device)
            time.sleep(0.5)

            nodes = dump_ui(device=device)
            state = detect_screen(nodes)
            print(f"[chat] Screen state: {state}", file=sys.stderr)

            if state == "LOCK":
                wake(device=device)
                time.sleep(1)
                continue

            dismiss_all_popups(nodes, device=device)
            nodes = dump_ui(device=device)

            if not tap_node(nodes, label="Chat baru", device=device):
                tap(472, 124, device=device)
            time.sleep(1.5)

            print("[chat] Typing prompt...", file=sys.stderr)
            type_in_field(prompt, "Minta Gemini", (316, 1370), device=device)

            print("[chat] Sending...", file=sys.stderr)
            send(device=device)

            print(f"[chat] Waiting for response (up to {timeout}s)...", file=sys.stderr)
            response = wait_for_response(timeout=timeout, device=device)

            ss_path = str(DOWNLOADS / "gemini_chat.png")
            screencap(ss_path, device=device)

            if response:
                result = {
                    "ok": True,
                    "response": response,
                    "device": device or "default",
                    "screenshot_path": ss_path,
                    "attempt": attempt,
                }
                print(json.dumps(result, indent=2))
                return result
            else:
                print(f"[chat] No response detected (attempt {attempt})", file=sys.stderr)

        except Exception as e:
            print(f"[chat] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "response": None,
        "error": "No response after all retries",
        "device": device or "default",
        "screenshot_path": None,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_imagine(prompt, out=None, device=None, max_retries=3):
    ts_before = int(time.time())

    for attempt in range(1, max_retries + 1):
        print(f"[imagine] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            print("[imagine] Launching Gemini...", file=sys.stderr)
            launch_gemini(device=device)

            nodes = dump_ui(device=device)
            dismiss_all_popups(nodes, device=device)

            if not open_image_gen(device=device):
                print("[imagine] Failed to open image gen screen", file=sys.stderr)
                continue

            nodes = dump_ui(device=device)
            state = detect_screen(nodes)
            print(f"[imagine] Screen state: {state}", file=sys.stderr)

            if state != "IMAGE_GEN":
                continue

            print("[imagine] Typing prompt...", file=sys.stderr)
            type_in_field(prompt, "Deskripsikan", (316, 860), device=device)

            print("[imagine] Sending...", file=sys.stderr)
            send(device=device)

            print("[imagine] Waiting for generation (~30s)...", file=sys.stderr)
            deadline = time.time() + 45
            image_ready = False
            while time.time() < deadline:
                time.sleep(3)
                wake(device=device)
                nodes = dump_ui(device=device)
                state = detect_screen(nodes)
                if state in ("CHAT_WITH_IMAGE", "VIEWER"):
                    image_ready = True
                    print(f"[imagine] Image ready! State: {state}", file=sys.stderr)
                    break

            if not image_ready:
                print("[imagine] Timeout waiting for image", file=sys.stderr)
                ss_path = str(DOWNLOADS / "gemini_imagine_timeout.png")
                screencap(ss_path, device=device)
                continue

            time.sleep(1)
            remote_path = save_generated_image(ts_before, device=device)

            ss_path = str(DOWNLOADS / "gemini_imagine_screen.png")
            screencap(ss_path, device=device)

            if remote_path:
                local_path = out or str(DOWNLOADS / "gemini_imagine.png")
                adb("pull", remote_path, local_path, device=device)
                if Path(local_path).exists() and Path(local_path).stat().st_size > 1000:
                    result = {
                        "ok": True,
                        "image_path": local_path,
                        "screenshot_path": ss_path,
                        "device": device or "default",
                        "prompt": prompt,
                        "attempt": attempt,
                    }
                    print(json.dumps(result, indent=2))
                    return result
                else:
                    print("[imagine] File pull failed or empty", file=sys.stderr)
            else:
                print("[imagine] Could not locate saved image in MediaStore", file=sys.stderr)

        except Exception as e:
            print(f"[imagine] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "image_path": None,
        "error": "Image generation failed after all retries",
        "device": device or "default",
        "screenshot_path": str(DOWNLOADS / "gemini_imagine_screen.png"),
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(device=None, out=None):
    out_path = out or str(DOWNLOADS / "gemini_screenshot.png")
    screencap(out_path, device=device)
    result = {
        "ok": True,
        "screenshot_path": out_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── API Server ──────────────────────────────────────────────────────────────

def run_server(port=8765):
    try:
        import fastapi, uvicorn
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "-q"], check=True)
        import fastapi, uvicorn

    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(title="Gemini Android Agent", version="3.0.0", description="""
Reliable API to control Gemini Android app via ADB.
All endpoints return JSON with `ok: true/false` and full details.
""")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    class ChatRequest(BaseModel):
        prompt: str
        device: Optional[str] = None
        timeout: int = 60
        max_retries: int = 3

    class ImagineRequest(BaseModel):
        prompt: str
        device: Optional[str] = None
        out: Optional[str] = None
        max_retries: int = 3

    @app.get("/")
    def root():
        return {"service": "autodroid-gemini-agent", "version": "3.0.0",
                "endpoints": ["/status", "/chat", "/imagine", "/screenshot"]}

    @app.get("/status")
    def api_status(device: Optional[str] = None):
        return cmd_status(device=device)

    @app.post("/chat")
    def api_chat(req: ChatRequest):
        result = cmd_chat(req.prompt, device=req.device, timeout=req.timeout, max_retries=req.max_retries)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Chat failed"))
        return result

    @app.post("/imagine")
    def api_imagine(req: ImagineRequest):
        result = cmd_imagine(req.prompt, out=req.out, device=req.device, max_retries=req.max_retries)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Image generation failed"))
        return result

    @app.get("/screenshot")
    def api_screenshot(device: Optional[str] = None, out: Optional[str] = None):
        return cmd_screenshot(device=device, out=out)

    @app.get("/health")
    def health():
        devices = [l.split()[0] for l in adb("devices").splitlines()[1:] if "\tdevice" in l]
        return {"status": "ok", "connected_devices": devices, "count": len(devices)}

    print(f"[server] autodroid-gemini-agent v3.0 on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[server] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="autodroid-gemini-agent v3.0 — Robust Gemini Android API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s chat --prompt "Halo Gemini siapa kamu"
  %(prog)s imagine --prompt "sunset over mountains in Indonesia"
  %(prog)s screenshot --out /tmp/screen.png
  %(prog)s server --port 8765

API (after starting server):
  curl -X POST http://localhost:8765/chat -H "Content-Type: application/json" \\
       -d '{"prompt": "hello gemini"}'
  curl -X POST http://localhost:8765/imagine \\
       -d '{"prompt": "kota Jakarta neon futuristik"}'
"""
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status")
    s.add_argument("--device", "-d")

    s = sub.add_parser("chat")
    s.add_argument("--prompt", "-p", required=True)
    s.add_argument("--device", "-d")
    s.add_argument("--timeout", "-t", type=int, default=60)
    s.add_argument("--retries", type=int, default=3)

    s = sub.add_parser("imagine")
    s.add_argument("--prompt", "-p", required=True)
    s.add_argument("--out", "-o")
    s.add_argument("--device", "-d")
    s.add_argument("--retries", type=int, default=3)

    s = sub.add_parser("screenshot")
    s.add_argument("--device", "-d")
    s.add_argument("--out", "-o")

    s = sub.add_parser("server")
    s.add_argument("--port", type=int, default=8765)

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status(device=args.device)
    elif args.cmd == "chat":
        cmd_chat(args.prompt, device=args.device, timeout=args.timeout, max_retries=args.retries)
    elif args.cmd == "imagine":
        cmd_imagine(args.prompt, out=args.out, device=args.device, max_retries=args.retries)
    elif args.cmd == "screenshot":
        cmd_screenshot(device=args.device, out=args.out)
    elif args.cmd == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
