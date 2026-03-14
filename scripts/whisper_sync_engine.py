import whisper
import json
import argparse
import sys
import os

def transcribe_to_words(audio_path, output_json):
    """
    Transcribe audio file to word-level timestamps using Whisper (Local AI)
    """
    print(f"🧠 Loading Whisper model...")
    model = whisper.load_model("base") # 'base' is fast and accurate enough
    
    print(f"🎤 Transcribing: {audio_path}")
    # task='transcribe', language='id' for Indonesian
    result = model.transcribe(audio_path, language="id", word_timestamps=True)
    
    word_timestamps = []
    
    # Extract words from segments
    for segment in result.get("segments", []):
        for word_data in segment.get("words", []):
            word_timestamps.append({
                "word": word_data["word"].strip(),
                "start": word_data["start"],
                "end": word_data["end"],
                "duration": word_data["end"] - word_data["start"]
            })
            
    with open(output_json, "w") as f:
        json.dump(word_timestamps, f, indent=2)
        
    print(f"✅ Whisper Sync: {len(word_timestamps)} words found.")
    return word_timestamps

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    
    transcribe_to_words(args.audio, args.json)
