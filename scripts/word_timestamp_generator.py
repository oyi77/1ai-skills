import asyncio
import edge_tts
import json
import argparse
import sys

async def generate_with_metadata(text, voice, output_audio, output_json):
    """
    Generate audio and capture word-level timestamps
    """
    communicate = edge_tts.Communicate(text, voice)
    submaker = edge_tts.SubMaker()
    
    # Save audio and collect metadata
    with open(output_audio, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # WordBoundary metadata: {'start': 0, 'end': 2000000, 'text': 'Hello'}
                # start/end are in 100ns units
                submaker.create_sub(chunk["start"], chunk["end"], chunk["text"])

    # Convert metadata to JSON
    # metadata is list of formatted strings, we need to parse them
    word_data = []
    # submaker.subs is list of SRT segment like strings, let's use a better way
    # actually edge-tts WordBoundary gives exact timings.
    
    # Re-running stream just to get exact data for JSON
    # (Simplified for this script)
    
    # Let's write the JSON manually from what we get in the loop above
    # Start again to be precise
    words = []
    comm = edge_tts.Communicate(text, voice)
    with open(output_audio, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            if chunk["type"] == "WordBoundary":
                words.append({
                    "word": chunk["text"],
                    "start": chunk["start"] / 10000000, # Convert to seconds
                    "end": chunk["end"] / 10000000,
                    "duration": (chunk["end"] - chunk["start"]) / 10000000
                })
    
    with open(output_json, "w") as f:
        json.dump(words, f, indent=2)
    
    print(f"✅ Audio: {output_audio}")
    print(f"✅ Timestamps: {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice", default="id-ID-GadisNeural")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    
    asyncio.run(generate_with_metadata(args.text, args.voice, args.audio, args.json))
