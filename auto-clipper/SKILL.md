---
name: auto-clipper
description: AI-powered video clipper - Convert long videos into viral Shorts/TikToks/Reels automatically
dependencies:
  - faster-whisper
  - textblob
  - vadersentiment
  - moviepy
  - opencv-python
  - ffmpeg-python
  - customtkinter
---

# Auto Clipper Indonesia 🎬

**Production-ready** AI-powered video clipper untuk content creator Indonesia.

## 🎯 Features

- **AI Transcription** - local Whisper model (Indonesian + English)
- **Golden Moment Detection** - automaticamente detect best clips
- **Smart Reframe** - 9:16 vertical conversion dengan face tracking
- **Subtitle Burn** - Auto-generate dan burn subtitles
- **Batch Processing** - Process unlimited clips
- **Progress Tracking** - Real-time status updates

## 📦 Files

```
auto-clipper/
├── SKILL.md              # This file
├── config.json           # Configuration
├── auto_clipper.py       # Main skill wrapper
└── core/                 # Core modules (from project)
    ├── __init__.py
    ├── video_analyzer.py
    ├── clip_engine.py
    ├── reframe_engine.py
    ├── subtitle_engine.py
    └── workflow.py
```

## 🔧 Installation

### Install Dependencies
```bash
pip install faster-whisper textblob vaderSentiment
pip install moviepy opencv-python ffmpeg-python
pip install customtkinter pillow requests
```

### Install FFmpeg (Required)
```bash
# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

## 📖 Usage

### Basic Usage
```python
from auto_clipper import AutoClipperSkill

# Initialize
skill = AutoClipperSkill()

# Full workflow (analyze + process + export)
results = skill.process_video(
    video_path="path/to/video.mp4",
    num_clips=10,
    clip_duration=30
)
print(f"Created {len(results)} clips")
```

### Advanced Usage
```python
# With custom configuration
skill = AutoClipperSkill(config={
    "clip_duration": 45,
    "output_resolution": "1080p",
    "num_clips": 15,
    "add_subtitles": True
})

# Analyze only - get golden moments
moments = skill.analyze_video("video.mp4")
print(f"Found {len(moments)} golden moments")

# Process specific clips
results = skill.process_clips(
    video_path="video.mp4",
    clip_indices=[0, 2, 5],  # Process specific moments
    add_subtitles=True
)

# Export with subtitle style
results = skill.export(
    video_path="video.mp4",
    clips=selected_moments,
    subtitle_style="social",
    output_resolution="1080p"
)
```

### CLI Usage
```bash
# Process video
python auto_clipper.py --video video.mp4 --clips 10 --duration 30

# Analyze video only
python auto_clipper.py --video video.mp4 --analyze

# With subtitles
python auto_clipper.py --video video.mp4 --subtitles --style social
```

## ⚙️ Configuration

Edit `config.json`:
```json
{
  "clip_duration": 30,
  "output_resolution": "720p",
  "whisper_model": "base",
  "num_clips": 10,
  "add_subtitles": true,
  "output_format": "mp4",
  "output_directory": "./output"
}
```

## 🎨 Subtitle Styles

```python
# Clean - Minimal subtitles
style = "clean"

# Bold - High attention
style = "bold"

# Social - Large, for mobile
style = "social"

# TikTok - Top position
style = "tiktok"
```

## 📊 Output

Results dalam format:
```python
{
    "clip_id": "clip_001",
    "status": "success",
    "output_path": "./output/clip_001.mp4",
    "start_time": 30.5,
    "end_time": 60.2,
    "duration": 29.7,
    "size_mb": 12.5,
    "original_text": "Hook: This blew my mind..."
}
```

## 🛠️ Troubleshooting

### Whisper Installation Failed?

```bash
# Windows
pip install faster-whisper --no-build-isolation

# Linux/macOS
sudo apt install libasound2-dev  # For audio support
pip install faster-whisper
```

### FFmpeg Not Found?

```bash
# Verify installation
ffmpeg -version

# Add to PATH (Windows)
setx PATH "%PATH%;C:\ffmpeg\bin"

# macOS
echo 'export PATH="/usr/local/opt/ffmpeg/bin:$PATH"' >> ~/.zshrc
```

### Memory Issues?

Use smaller Whisper model:
```python
skill = AutoClipperSkill(config={"whisper_model": "tiny"})
```

### Processing Slow?

Optimize settings:
```json
{
  "output_resolution": "720p",
  "whisper_model": "tiny",
  "clip_duration": 30
}
```

## 📈 Performance

| Setting | Speed | Quality |
|---------|-------|---------|
| Whisper tiny + 720p | ⚡ Fast | Good |
| Whisper base + 720p | 🚀 Normal | Better |
| Whisper small + 1080p | 🚶 Slow | Best |

## ⚠️ Requirements

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.11+
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB for dependencies
- **FFmpeg**: Required for video processing

## 🚀 Next Updates

Planned improvements:
- [ ] Distribution automation (TikTok/IG/YT)
- [ ] Face beautification filter
- [ ] Background music addition
- [ ] Template library
- [ ] Cloud rendering option

## 📝 License

Proprietary - BerkahKarya

## 💰 Support

Join our community:
- Telegram: @berkahkarya
- Website: berkahkarya.id

---

**BerkahKarya** ⚡ | Auto Clipper Indonesia