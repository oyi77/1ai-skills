#!/usr/bin/env python3
"""
Send Voice Note via TTS (edge-tts).
Usage: python3 send_voice.py @username "teks pesan" [id|en]
"""

import asyncio, edge_tts, os, sys, tempfile
from telethon import TelegramClient

SESSION = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session"
VOICES = {
    "id": "id-ID-ArdiNeural",  # Indonesian male
    "id-f": "id-ID-GadisNeural",  # Indonesian female
    "en": "en-US-GuyNeural",  # English male
}


async def send_voice_note(username: str, text: str, lang: str = "id"):
    client = TelegramClient(SESSION, 23913448, "REDACTED_ROTATED_CREDENTIAL")
    await client.connect()

    voice = VOICES.get(lang, VOICES["id"])
    mp3 = tempfile.mktemp(suffix=".mp3")
    ogg = mp3.replace(".mp3", ".ogg")

    await edge_tts.Communicate(text, voice).save(mp3)
    os.system(f"ffmpeg -i {mp3} -c:a libopus {ogg} -y -loglevel quiet")

    await client.send_file(username, ogg, voice_note=True)
    print(f"🎤 Voice note sent to {username}")

    os.remove(mp3)
    os.remove(ogg)
    await client.disconnect()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 send_voice.py @username 'teks' [id|en]")
        sys.exit(1)
    target = sys.argv[1]
    text = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "id"
    asyncio.run(send_voice_note(target, text, lang))
