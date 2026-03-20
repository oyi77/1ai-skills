#!/usr/bin/env python3
"""
Phone-Based Personal Assistant via Telegram Voice Messages
Transcribes voice → sends to OmniRoute → returns text response
"""
import sys, os, json, subprocess, tempfile
from pathlib import Path

def transcribe_audio(audio_file):
    """Transcribe audio using faster-whisper, openai-whisper, or OmniRoute fallback"""
    audio_path = str(audio_file)
    
    # Try faster-whisper first (fastest)
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segs, _ = model.transcribe(audio_path, language="id")
        return " ".join(s.text for s in segs).strip()
    except ImportError:
        pass
    
    # Try openai-whisper
    try:
        import whisper
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path, language="id")
        return result["text"].strip()
    except ImportError:
        pass
    
    # Fallback: OmniRoute Whisper API
    try:
        from openai import OpenAI
        client = OpenAI(base_url="http://localhost:20128/v1", api_key="omniroute")
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(model="whisper-1", file=f, language="id")
        return result.text
    except Exception as e:
        return f"Transcription failed: {e}"

def ask_agent(text):
    """Send text to OmniRoute and get response"""
    try:
        from openai import OpenAI
        client = OpenAI(base_url="http://localhost:20128/v1", api_key="omniroute")
        r = client.chat.completions.create(
            model="auto/pro-chat",
            messages=[
                {"role": "system", "content": "Kamu adalah Vilona, asisten AI BerkahKarya. Jawab singkat dan helpful dalam bahasa Indonesia."},
                {"role": "user", "content": text}
            ],
            max_tokens=300
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Agent error: {e}"

def process_voice_message(audio_file):
    """Full pipeline: audio → text → agent → response"""
    transcript = transcribe_audio(audio_file)
    if transcript.startswith("Transcription failed"):
        return {"error": transcript}
    
    response = ask_agent(transcript)
    return {
        "transcript": transcript,
        "response": response
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python voice_handler.py <audio_file>")
        sys.exit(1)
    
    result = process_voice_message(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result.get("error"):
        print(f"\n🎤 You said: {result['transcript']}")
        print(f"🤖 Vilona: {result['response']}")
