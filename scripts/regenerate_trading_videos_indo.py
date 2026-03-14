#!/usr/bin/env python3
"""
Regenerate trading education videos with Indonesian voiceover
Natural Indonesian speech style - like a real person talking
"""
import subprocess
import os
import json
import requests
from datetime import datetime, timezone

BASE_DIR = "/home/openclaw/.openclaw/workspace/remix_factory/trading_edu"
PB_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
PB_BASE = "https://api.post-bridge.com/v1"
PB_H = {"Authorization": f"Bearer {PB_KEY}", "Content-Type": "application/json"}

ALGO_TEXT = [49814, 49811]
ALGO_MEDIA = [49810, 49663, 49661]

# Indonesian voiceover scripts - natural, conversational, like a real human
LESSONS = {
    "risk_mgmt": {
        "narration": (
            "Hei, tau gak sih? Sembilan puluh persen trader itu gagal. "
            "Bukan karena strategi mereka jelek ya... Tapi karena, mereka gak pake risk management! "
            "Nah sekarang gue kasih tau satu aturan simpel. Namanya The One Percent Rule. "
            "Jadi gini, lo gak boleh risiko lebih dari satu persen modal di satu trade. "
            "Misalnya akun lo sepuluh juta, berarti risiko maksimal lo cuma seratus ribu per trade. "
            "Kedengeran dikit ya? Tapi justru itu yang bikin lo bisa survive! "
            "Dan satu lagi yang penting banget, selalu... selalu pake stop loss. "
            "Gak ada alasan buat trading tanpa stop loss. Titik. "
            "Inget ya, trader yang sukses itu bukan yang paling banyak untungnya. "
            "Tapi yang paling lama bertahannya. Survive dulu, cuan belakangan."
        ),
        "caption": (
            "🔴 90% trader GAGAL karena SATU hal ini...\n\n"
            "Bukan strategi. Bukan timing.\n"
            "Tapi RISK MANAGEMENT!\n\n"
            "💡 The 1% Rule bisa selamatin akun trading kamu.\n\n"
            "🔊 Full narasi Bahasa Indonesia\n\n"
            "#trading #riskmanagement #forex #xauusd #edukasi #tradingpemula #fyp"
        )
    },
    "candles": {
        "narration": (
            "Oke guys, kalo lo mau baca market kayak pro, lo harus paham candlestick pattern. "
            "Gak perlu hafal semua ya, cukup tiga ini dulu. "
            "Pertama, Engulfing Pattern. Ini tuh kayak candle gede nelen candle kecil sebelumnya. "
            "Kalo ada bullish engulfing, biasanya harga mau naik. Sinyalnya kuat banget. "
            "Kedua, Pin Bar atau yang sering disebut Hammer. "
            "Ini kelihatan kayak palu gitu ya, ekornya panjang. "
            "Artinya harga udah coba turun tapi ditolak balik. Potensi reversal! "
            "Ketiga, si Doji. Candle kecil mungil, artinya market lagi bingung. "
            "Buyer sama seller lagi tarik-tarikan. Nah, perhatiin candle setelahnya, "
            "itu yang nentuin arah selanjutnya. "
            "Tiga pattern ini aja dulu, kuasain sebelum lo pake indikator apapun. "
            "Karena price action itu gak pernah bohong!"
        ),
        "caption": (
            "🕯️ 3 Candlestick Pattern yang WAJIB kamu tau!\n\n"
            "Belajar baca market kayak PRO.\n"
            "Engulfing, Pin Bar, Doji — cukup 3 ini dulu!\n\n"
            "🔊 Full narasi Bahasa Indonesia\n\n"
            "#candlestick #priceaction #trading #forex #technicalanalysis #xauusd #fyp"
        )
    },
    "psychology": {
        "narration": (
            "Bro, musuh terbesar lo di trading itu bukan market loh. Tapi otak lo sendiri! "
            "Serius, gue kasih tau jebakan-jebakan yang sering banget kejadian. "
            "Pertama, FOMO. Lo liat harga udah terbang, terus lo ngejar masuk. "
            "Hasilnya? Entry di puncak, terus turun. Nyesek kan? "
            "Kedua, revenge trading. Habis loss, lo langsung buka posisi lagi dengan lot gede. "
            "Mau balas dendam katanya. Eh malah makin rugi. Ini yang bikin akun jebol! "
            "Nah terus solusinya gimana? Disiplin. Titik. "
            "Lo harus bisa bedain antara emosi sama analisis. "
            "Dan cara paling gampang? Journaling. Catat semua trade lo. "
            "Kenapa entry, kenapa exit, emosi lo waktu itu gimana. "
            "Setelah lima puluh trade, lo bakal liat pola yang selama ini gak lo sadari. "
            "Inget, data ngalahin perasaan. Selalu!"
        ),
        "caption": (
            "🧠 Musuh TERBESAR di trading? OTAK KAMU SENDIRI!\n\n"
            "FOMO, revenge trading, overconfidence...\n"
            "Jebakan emosi yang bikin akun JEBOL 💥\n\n"
            "🔊 Full narasi Bahasa Indonesia\n\n"
            "#tradingpsychology #forex #mindset #disiplin #trading #xauusd #fyp"
        )
    }
}


def generate_tts_indo(text, output_path):
    """Generate natural Indonesian TTS"""
    print(f"  🎙️ Generating Indonesian voiceover ({len(text)} chars)...")
    
    cmd = [
        "edge-tts",
        "--voice", "id-ID-ArdiNeural",
        "--rate=-3%",       # Slightly slower for natural feel
        "--pitch=+1Hz",     # Slightly higher for energy
        "--text", text,
        "--write-media", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0 and os.path.exists(output_path):
        size = os.path.getsize(output_path) / 1024
        print(f"  ✅ TTS saved: {output_path} ({size:.0f}KB)")
        return True
    else:
        print(f"  ❌ TTS failed: {result.stderr[:200]}")
        return False


def merge_audio_video(video_path, audio_path, output_path):
    """Merge voiceover with video, pad video if audio is longer"""
    
    # Get durations
    def get_duration(path):
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=30
        )
        return float(r.stdout.strip()) if r.stdout.strip() else 0
    
    vid_dur = get_duration(video_path)
    aud_dur = get_duration(audio_path)
    
    print(f"  📐 Video: {vid_dur:.1f}s, Audio: {aud_dur:.1f}s")
    
    # If audio longer than video, extend video with last frame
    target_dur = max(vid_dur, aud_dur)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(target_dur),
        "-map", "0:v:0", "-map", "1:a:0",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    # If audio is longer, loop last frame
    if aud_dur > vid_dur + 2:
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", video_path,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-t", str(aud_dur),
            "-map", "0:v:0", "-map", "1:a:0",
            "-pix_fmt", "yuv420p",
            "-shortest",
            output_path
        ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0 and os.path.exists(output_path):
        size = os.path.getsize(output_path) / 1024 / 1024
        final_dur = get_duration(output_path)
        print(f"  ✅ Merged: {output_path} ({size:.1f}MB, {final_dur:.0f}s)")
        return True
    else:
        print(f"  ❌ Merge failed: {result.stderr[-300:]}")
        return False


def upload_and_crosspost(video_path, caption):
    """Upload to PostBridge and crosspost to all algo accounts"""
    fname = os.path.basename(video_path)
    fsize = os.path.getsize(video_path)
    
    print(f"  📤 Uploading {fname} ({fsize/1024/1024:.1f}MB)...")
    
    resp = requests.post(f"{PB_BASE}/media/create-upload-url", headers=PB_H,
        json={"name": fname, "mime_type": "video/mp4", "size_bytes": fsize})
    
    if resp.status_code not in [200, 201]:
        print(f"  ❌ Upload URL failed: {resp.status_code} {resp.text[:200]}")
        resp2 = requests.post(f"{PB_BASE}/posts", headers=PB_H,
            json={"caption": caption, "social_accounts": ALGO_TEXT})
        if resp2.status_code in [200, 201]:
            print(f"  📝 Text-only fallback: {resp2.json().get('id','?')[:8]}")
        return False
    
    data = resp.json()
    upload_url = data.get("upload_url") or data.get("url")
    media_id = data.get("media_id") or data.get("id")
    
    if upload_url:
        with open(video_path, "rb") as f:
            up = requests.put(upload_url, data=f, headers={"Content-Type": "video/mp4"})
        
        if up.status_code in [200, 201, 204]:
            print(f"  ✅ Uploaded! media_id={media_id}")
            all_accounts = ALGO_TEXT + ALGO_MEDIA
            resp3 = requests.post(f"{PB_BASE}/posts", headers=PB_H,
                json={"caption": caption, "social_accounts": all_accounts, "media": [media_id]})
            if resp3.status_code in [200, 201]:
                print(f"  ✅ Crosspost to {len(all_accounts)} accounts!")
                return True
            else:
                print(f"  ❌ Crosspost failed: {resp3.status_code}")
    return False


def main():
    print("=" * 60)
    print("🇮🇩 TRADING EDUCATION — INDONESIAN VOICEOVER V3")
    print("=" * 60)
    
    for lid, data in LESSONS.items():
        lesson_dir = os.path.join(BASE_DIR, lid)
        video_src = os.path.join(lesson_dir, f"{lid}_trading_edu.mp4")  # Original video (no audio)
        audio_path = os.path.join(lesson_dir, f"{lid}_voiceover_indo.mp3")
        final_path = os.path.join(lesson_dir, f"{lid}_trading_edu_indo.mp4")
        
        if not os.path.exists(video_src):
            print(f"\n⚠️ Source video not found: {video_src}")
            continue
        
        print(f"\n{'='*40}")
        print(f"🎬 {lid}")
        print(f"{'='*40}")
        
        # Step 1: Generate Indonesian TTS
        if not generate_tts_indo(data["narration"], audio_path):
            continue
        
        # Step 2: Merge audio + video
        if not merge_audio_video(video_src, audio_path, final_path):
            continue
        
        # Step 3: Upload and crosspost
        upload_and_crosspost(final_path, data["caption"])
        
        # Step 4: Copy to workspace for Telegram send
        workspace_copy = f"/home/openclaw/.openclaw/workspace/{lid}_indo.mp4"
        subprocess.run(["cp", final_path, workspace_copy])
        print(f"  📋 Copied to: {workspace_copy}")
        
        print(f"✅ {lid} COMPLETE\n")
    
    print("\n" + "=" * 60)
    print("🏁 ALL INDONESIAN VOICEOVER VIDEOS DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
