#!/usr/bin/env python3
"""
Generate Sample Voice Over & Video Template
For: Guru Pintar AI faceless video (15 detik)
"""

from pathlib import Path
import subprocess

workspace = Path.home() / ".openclaw" / "workspace"

print("=" * 80)
print("🎵 VOICE OVER GENERATION")
print("=" * 80)
print()

# Voice over script
voice_script = {
    "hook": {
        "text": "STOP! Konten manual makan waktu 4 jam per post!",
        "duration": "3s",
        "tone": "Energetic, attention-grabbing, urgent but friendly"
    },
    "body": {
        "text": "Dulu, ide konten kosong nungguin 2 jam. Writing caption 1 jam, edit gambar 45 menit, posting 15 menit. Total: 4 jam per post! Masalah? Hanya 2-3 konten per minggu. GAK SCALE!",
        "duration": "9s",
        "tone": "Empathetic then energized"
    },
    "solution": {
        "text": "Dengan Guru Pintar AI, ide 5 menit, caption 1 menit, edit 1 menit. Total: 8 menit per post! ROI: 90 jam/hari dihemat = 360 konten per bulan!",
        "duration": "8s",
        "tone": "Excited, inspiring"
    },
    "cta": {
        "text": "Mulai dari belajar GRATIS di Guru Pintar AI. Level-up ke AI Content Pro saat sudah terbukti works! Kunjungi: l-i-n-k-dot-i-n-slash-ai-content-pro",
        "duration": "5s",
        "tone": "Hopeful, inviting, natural"
    }
}

print("✅ VOICE OVER SCRIPT:")
print("-" * 80)
for section, details in voice_script.items():
    print(f"\n{section.upper()} ({details['duration']})")
    print(f"Tone: {details['tone']}")
    print(f"\nText:")
    print(f'  "{details["text"]}"')

print()
print("=" * 80)
print("🎙️ AUDIO GENERATION - METHOD 1: Google TTS (FREE)")
print("=" * 80)
print()

# Create voice over with Google TTS
tts_script = workspace / "scripts" / "generate_voiceover.sh"
with open(tts_script, "w") as f:
    f.write("""#!/bin/bash
# Generate Voice Over using Google Cloud Text-to-Speech
# Setup: pip install google-cloud-texttospeech
# API Key: Need GCP service account

OUTPUT_FILE="hook_audio.mp3"

# This example shows API usage pattern
# For actual usage, need GCP credentials
echo "To generate voice over with Google TTS:"
echo "1. Install: pip install google-cloud-text-to-speech"
echo "2. Set GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json"
echo "3. Run: python google_tts.py --output OUTPUT_FILE"
""")

print(f"Created TTS script: {tts_script}")
print()

print("⚠️  NOTE: For Google TTS, need GCP account & credentials")
print("   Alternative: Use online TTS tools (ElevenLabs FREE, Google TTS web)")
print()

print("=" * 80)
print("🎯 VIDEO TEMPLATE FOR MANUAL PRODUCTION")
print("=" * 80)
print()

video_template = {
    "duration": "15s",
    "aspect_ratio": "9:16 (1080x1920)",
    "platform": "TikTok / Instagram Reels / YouTube Shorts",
    "sections": [
        {
            "time": "0-3s",
            "visual": "Hook Image (hook_image.png) - full screen",
            "text_overlay": "🔥 STOP! (bold orange-red, centered)",
            "audio": "Voice over: 'STOP! Konten manual makan waktu 4 jam per post!'"
        },
        {
            "time": "3-12s",
            "visual": "B-roll screen recording (product interface or frustrated person working)",
            "text_overlays": [
                "⏱️ 4 jam/post (timestamp)",
                "💸 Manual, lambat, frustrating",
                "❌ GAK SCALE!"
            ],
            "audio": "Voice over explaining problem + emotional pain"
        },
        {
            "time": "12-15s",
            "visual": "Before/After split screen OR product centered",
            "text_overlay": "✅ Start GRATIS: https://lnkd.in/ai-content-pro",
            "audio": "Voice over CTA with hopeful tone"
        }
    ]
}

print("📹 VIDEO SECTIONS:")
print("-" * 80)
for i, section in enumerate(video_template["sections"], 1):
    print(f"\n{i}. TIME: {section['time']}")
    print(f"   Visual: {section['visual']}")
    if "text_overlay" in section:
        print(f"   Text: {section['text_overlay']}")
    if "text_overlays" in section:
        print(f"   Text Overlays:")
        for text in section["text_overlays"]:
            print(f"      • {text}")
    print(f"   Audio: {section['audio']}")

print()
print("=" * 80)
print("🎨 ADDITIONAL VISUAL ELEMENTS")
print("=" * 80)
print()

visual_elements = {
    "text_overlays": {
        "font": "Arial Bold / Helvetica Bold",
        "color": "White (for dark backgrounds), Orange-red (#FF4500) for emphasis",
        "size": "Large (400-500px width) for hook, Medium (300-400px) for body",
        "shadow": "Yes, black text-shadow for readability",
        "position": "Center or bottom-center for CTA"
    },
    "b_roll_footage": {
        "source_1": "Screen recording of content creation software",
        "source_2": "Stock footage: Person frustrated at computer",
        "source_3": "Stock footage: Clock showing 4:00 passing",
        "source_4": "Animation: Counter counting 1→4 hours rapidly",
        "style": "Montage style, quick cuts between shots"
    },
    "background_music": {
        "source": "Spotify Free Tier - Upbeat instrumental playlists",
        "volume": "30-40% of voice max",
        "mood": "Energetic, hopeful, professional",
        "fade": "Fade in at 0s, fade out at 15s"
    },
    "effects": {
        "transitions": "Quick cuts, no slow fades (keep energy)",
        "zoom": "Slight zoom on important text (CTA)",
        "highlight": "Brief flash on key numbers (4 jam, 8 menit)"
    }
}

print("📝 TEXT OVERLAYS:")
for key, value in visual_elements["text_overlays"].items():
    print(f"   {key}: {value}")

print()
print("🎞️ B-ROLL FOOTAGE:")
for key, value in visual_elements["b_roll_footage"].items():
    print(f"   {key}: {value}")

print()
print("🎵 BACKGROUND MUSIC:")
for key, value in visual_elements["background_music"].items():
    print(f"   {key}: {value}")

print()
print("✨ EFFECTS:")
for key, value in visual_elements["effects"].items():
    print(f"   {key}: {value}")

print()
print("=" * 80)
print("📋 PRODUCTION CHECKLIST")
print("=" * 80)
print()

checklist = [
    "☐ Download hook_image.png",
    "☐ Record/find B-roll footage (screen recording or stock)",
    "☐ Generate voice over (Google TTS or ElevenLabs)",
    "☐ Select background music (Spotify FREE)",
    "☐ Assemble video in CapCut / Adobe Premier / FFmpeg",
    "☐ Add text overlays (use template above)",
    "☐ Sync audio with visuals",
    "☐ Export: 1080x1920, H.264, MP4, <10MB",
    "☐ Review final video for quality",
    "☐ Share for review to human"
]

for item in checklist:
    print(item)

print()
print("=" * 80)
print("🚀 QUICK START: AUTO-FULL PRODUCTION (Optional)")
print("=" * 80)
print()

print("For FULL automation, can use:")
print()
print("1. content-generator skill → Auto-generate AI videos")
print('   python3 scripts/content_generator.py --product guru_pintar_ai --type faceless --qty 50')
print()
print("2. FFmpeg command line → Combine elements programmatically")
print('   ffmpeg -i hook_image.png -i audio.mp3 -i b-roll.mp4 output_9x16.mp4')
print()
print("3. CapCut Template → Load all assets, auto-assemble")
print()

print("=" * 80)
print("✅ COMPLETE!")
print("=" * 80)
print()
print("Generated:")
print("  ✅ Hook image: content/samples/hook_image.png")
print("  ✅ Voice over script: (see above)")
print("  ✅ Video template: (see above sections)")
print()
print("Next steps:")
print("  1. Review image & script")
print("  2. Approve for production")
print("  3. Assemble video (manual or automated)")
print("  4. Share final sample for human review")
print("=" * 80)