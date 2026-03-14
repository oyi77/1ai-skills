import asyncio
import edge_tts
import json
import argparse
import os

async def generate_with_metadata_v3(text, voice, output_audio, output_json):
    communicate = edge_tts.Communicate(text, voice)
    words = []
    audio_data = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            words.append({
                "word": chunk["text"],
                "start": chunk["start"] / 10000000,
                "end": (chunk["start"] + chunk["duration"]) / 10000000,
                "duration": chunk["duration"] / 10000000
            })
    
    # Save collected audio
    with open(output_audio, "wb") as f:
        f.write(audio_data)
    
    # Save the JSON metadata
    with open(output_json, "w") as f:
        json.dump(words, f, indent=2)
    
    print(f"✅ Audio: {output_audio} ({len(audio_data)} bytes)")
    print(f"✅ Metadata: {len(words)} words captured in {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice", default="id-ID-GadisNeural")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    asyncio.run(generate_with_metadata_v3(args.text, args.voice, args.audio, args.json))
