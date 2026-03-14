# Auto Clipper Indonesia - Tech Stack

## Core Technologies

### Video Processing
- **FFmpeg** - Core video manipulation (clip, reframe, subtitle burn)
- **OpenCV** - Face detection + object tracking untuk reframe
- **MoviePy** - Python wrapper FFmpeg (simpler operations)
- **Whisper AI** - Transcription (for finding golden moments)

### AI & Analysis
- **OpenAI Whisper** - Speech-to-text (local version: faster-whisper)
- **Sentiment Analysis** - Python libraries (textblob, vaderSentiment)
- **Peak Detection Algorithm** - Find most emotional moments

### GUI Framework
- **CustomTkinter** - Modern Python GUI (tkinter based)
- **PyInstaller** - Package to Windows .exe

### Distribution Automation
- **TikTok API** - Upload shorts
- **Instagram API** - Upload Reels (via PostBridge integration)
- **YouTube Data API** - Upload Shorts

### Configuration
- **Python 3.11+**
- **Windows 10/11 64-bit**
- **GPU Optional (CUDA untuk acceleration)**

## Requirements Installation

```bash
pip install moviepy opencv-python faster-whisper
pip install textblob vaderSentiment
pip install customtkinter pyinstaller
pip install requests yt-dlp
```

## System Architecture

```
┌─────────────────────────────────────┐
│         GUI Layer (CustomTkinter)      │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│       Business Logic Layer            │
│  - Clip Manager                      │
│  - AI Analyzer                       │
│  - Render Engine                     │
│  - Upload Manager                    │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│       Core Processing Layer           │
│  - FFmpeg (video manip)              │
│  - OpenCV (face tracking)            │
│  - Whisper (transcription)           │
│  - Platform APIs (TikTok/IG/YT)      │
└─────────────────────────────────────┘
```