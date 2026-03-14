#!/usr/bin/env python3
"""
Add voiceover to trading education videos using OpenClaw TTS
Then re-upload to PostBridge with crossposting
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

# Accounts for crosspost
ALGO_TEXT = [49814, 49811]       # Twitter, Threads  
ALGO_MEDIA = [49810, 49663, 49661]  # IG, TikTok, IG

VOICEOVER_SCRIPTS = {
    "risk_mgmt": {
        "narration": "Ninety percent of traders fail. And it's NOT because of bad strategy. It's because they ignore risk management. Here's the number one rule: Never risk more than one percent of your account on a single trade. That means on a ten thousand dollar account, your maximum risk per trade is just one hundred dollars. Always use a stop loss. No exceptions. The traders who survive are the ones who protect their capital first. Remember: survive first, profits come to those who last. Master risk management, and you're already ahead of ninety percent of traders.",
        "caption": "🔴 90% of traders FAIL because of ONE thing...\n\nIt's NOT strategy. It's RISK MANAGEMENT.\n\n💡 The 1% Rule can save your account.\n\nFull voice narration included! 🔊\n\n#trading #riskmanagement #forex #xauusd #education #tradingtips #fyp"
    },
    "candles": {
        "narration": "Want to read the market like a pro? Start with candlestick patterns. Number one: the Engulfing Pattern. When a big green candle completely swallows the previous red candle, that's a strong reversal signal. Number two: the Pin Bar, also called a Hammer. This shows price rejection and a potential reversal. Number three: the Doji. This tiny candle means the market is undecided. Watch for what comes next. These three patterns alone can make you a better trader. Master candlesticks BEFORE any indicator. Price action doesn't lie.",
        "caption": "🕯️ 5 Candlestick Patterns that ACTUALLY work!\n\nLearn to read price action like a PRO.\n\n🔊 Full narration included\n\n#candlestick #priceaction #trading #forex #technicalanalysis #xauusd #fyp"
    },
    "psychology": {
        "narration": "Your worst enemy in trading isn't the market. It's your own brain. Trap number one: FOMO. Chasing trades you missed always leads to bad entries. Trap number two: Revenge trading. After a loss, you want to make it back immediately. This is how accounts blow up. The solution? Discipline over emotion. Every single time. Start journaling every trade. Write down your entry reason, your emotions, and the result. After fifty trades, you'll see patterns you never noticed. Data beats feelings. Always. Master your psychology, and the profits will follow.",
        "caption": "🧠 Your BRAIN is your biggest enemy in trading.\n\n5 emotional traps that KILL your account.\n\n🔊 Full narration included\n\n#tradingpsychology #forex #mindset #discipline #trading #xauusd #fyp"
    }
}


def generate_tts(text, output_path):
    """Generate TTS using edge-tts (free, high quality)"""
    print(f"  🎙️ Generating voiceover ({len(text)} chars)...")
    
    # Use edge-tts (Microsoft Edge TTS - free, good quality)
    cmd = [
        "edge-tts",
        "--voice", "en-US-GuyNeural",  # Professional male voice
        "--rate", "+5%",  # Slightly faster for engagement
        "--text", text,
        "--write-media", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0 and os.path.exists(output_path):
        size = os.path.getsize(output_path) / 1024
        print(f"  ✅ TTS saved: {output_path} ({size:.0f}KB)")
        return True
    else:
        print(f"  ❌ edge-tts failed: {result.stderr[:200]}")
        # Fallback: try gtts
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            if os.path.exists(output_path):
                print(f"  ✅ gTTS fallback saved: {output_path}")
                return True
        except Exception as e:
            print(f"  ❌ gTTS fallback also failed: {e}")
        
        # Fallback 2: pico2wave
        try:
            cmd2 = ["pico2wave", "-w", output_path, "-l", "en-US", text[:500]]
            result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=30)
            if result2.returncode == 0 and os.path.exists(output_path):
                print(f"  ✅ pico2wave fallback saved: {output_path}")
                return True
        except:
            pass
            
        return False


def merge_audio_video(video_path, audio_path, output_path):
    """Merge voiceover audio with video using FFmpeg"""
    print(f"  🎬 Merging audio + video...")
    
    # Get video duration
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True, timeout=30
    )
    video_dur = float(probe.stdout.strip()) if probe.stdout.strip() else 60
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(video_dur),
        "-shortest",
        "-map", "0:v:0", "-map", "1:a:0",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0 and os.path.exists(output_path):
        size = os.path.getsize(output_path) / 1024 / 1024
        print(f"  ✅ Merged: {output_path} ({size:.1f}MB)")
        return True
    else:
        print(f"  ❌ Merge failed: {result.stderr[-200:]}")
        return False


def upload_and_crosspost(video_path, caption):
    """Upload to PostBridge and crosspost"""
    fname = os.path.basename(video_path)
    fsize = os.path.getsize(video_path)
    
    print(f"  📤 Uploading {fname} ({fsize/1024/1024:.1f}MB)...")
    
    resp = requests.post(f"{PB_BASE}/media/create-upload-url", headers=PB_H,
        json={"name": fname, "mime_type": "video/mp4", "size_bytes": fsize})
    
    if resp.status_code not in [200, 201]:
        print(f"  ❌ Upload URL failed: {resp.status_code} {resp.text[:200]}")
        # Text-only fallback
        resp2 = requests.post(f"{PB_BASE}/posts", headers=PB_H,
            json={"caption": caption, "social_accounts": ALGO_TEXT})
        if resp2.status_code in [200, 201]:
            print(f"  📝 Text-only crosspost: {resp2.json().get('id','?')[:8]}")
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
                print(f"  ✅ Crosspost to {len(all_accounts)} accounts: {resp3.json().get('id','?')[:8]}")
                return True
            else:
                print(f"  ❌ Crosspost failed: {resp3.status_code} {resp3.text[:200]}")
    
    return False


def main():
    print("=" * 60)
    print("🎙️ VOICEOVER TRADING VIDEO PIPELINE")
    print("=" * 60)
    
    for lesson_id, data in VOICEOVER_SCRIPTS.items():
        lesson_dir = os.path.join(BASE_DIR, lesson_id)
        video_path = os.path.join(lesson_dir, f"{lesson_id}_trading_edu.mp4")
        audio_path = os.path.join(lesson_dir, f"{lesson_id}_voiceover.mp3")
        final_path = os.path.join(lesson_dir, f"{lesson_id}_trading_edu_vo.mp4")
        
        if not os.path.exists(video_path):
            print(f"\n⚠️ Video not found: {video_path}, skipping")
            continue
        
        print(f"\n{'='*40}")
        print(f"📚 {lesson_id}")
        print(f"{'='*40}")
        
        # Step 1: Generate TTS
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
            if not generate_tts(data["narration"], audio_path):
                print(f"  ⚠️ TTS failed, skipping voiceover for {lesson_id}")
                continue
        else:
            print(f"  ℹ️ TTS already exists: {audio_path}")
        
        # Step 2: Merge audio + video
        if not os.path.exists(final_path) or os.path.getsize(final_path) < 10000:
            if not merge_audio_video(video_path, audio_path, final_path):
                print(f"  ⚠️ Merge failed for {lesson_id}")
                continue
        else:
            print(f"  ℹ️ Final video already exists: {final_path}")
        
        # Step 3: Upload and crosspost
        upload_and_crosspost(final_path, data["caption"])
        
        print(f"✅ {lesson_id} COMPLETE\n")
    
    print("\n" + "=" * 60)
    print("🏁 ALL VOICEOVER VIDEOS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
