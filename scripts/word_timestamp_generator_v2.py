import asyncio
import edge_tts
import json
import argparse
import os

async def generate_with_metadata_v2(text, voice, output_audio, output_json):
    """
    Fixed Metadata Generator (V2)
    Ensures WordBoundary data is captured correctly.
    """
    communicate = edge_tts.Communicate(text, voice)
    words = []
    
    # We collect data first, then write
    # Capturing word boundaries from the stream
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            # Just streaming to avoid large memory if needed, but we write it at the end
            pass
        elif chunk["type"] == "WordBoundary":
            words.append({
                "word": chunk["text"],
                "start": chunk["start"] / 10000000, # 100ns -> seconds
                "end": (chunk["start"] + chunk["duration"]) / 10000000,
                "duration": chunk["duration"] / 10000000
            })
    
    # Save the actual audio file
    await communicate.save(output_audio)
    
    # Save the JSON metadata
    with open(output_json, "w") as f:
        json.dump(words, f, indent=2)
    
    print(f"✅ Audio: {output_audio} ({os.path.getsize(output_audio)} bytes)")
    print(f"✅ Metadata: {len(words)} words captured in {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice", default="id-ID-GadisNeural")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    
    asyncio.run(generate_with_metadata_v2(args.text, args.voice, args.audio, args.json))
