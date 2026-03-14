#!/usr/bin/env python3
import asyncio
import edge_tts
import argparse
import sys
from pathlib import Path

async def generate_tts(text, output_path, voice="id-ID-ArdiNeural"):
    """
    Generate high-quality TTS using edge-tts
    Voices: id-ID-ArdiNeural (Male), id-ID-GadisNeural (Female)
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"✅ TTS Generated: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--voice", default="id-ID-ArdiNeural")
    args = parser.parse_args()

    asyncio.run(generate_tts(args.text, args.output, args.voice))
