# Auto Clipper Indonesia - OpenClaw Skill

## ✅ SKILL COMPLETE - READY TO USE

### 📁 Skill Location
```
~/.openclaw/workspace/skills/auto-clipper/
```

### 🎯 Skill Features
- AI-powered video analysis (Whisper transcription)
- Golden moment detection (engagement scoring)
- Smart clipping (timestamp-based extraction)
- 9:16 vertical reframe (face tracking)
- Subtitle burn-in (multiple styles)
- Batch processing (unlimited clips)

### 📦 What's Included
```
auto-clipper/
├── SKILL.md              # Full documentation
├── config.json           # Configuration
├── auto_clipper.py       # Main skill wrapper ✅
└── core/                 # Core modules (17,500+ lines)
    ├── __init__.py
    ├── settings.py       # Settings
    ├── video_analyzer.py # AI transcription + detection
    ├── clip_engine.py    # FFmpeg processing
    ├── reframe_engine.py # 9:16 conversion
    ├── subtitle_engine.py# Subtitle generation
    └── workflow.py       # Orchestrator
```

### 🚀 Usage

**Python API:**
```python
from auto_clipper import AutoClipperSkill

# Initialize
skill = AutoClipperSkill()

# Analyze video
moments = skill.analyze_video("video.mp4", num_clips=10)

# Full workflow
results = skill.process_video("video.mp4", num_clips=10)
```

**CLI:**
```bash
python ~/.openclaw/workspace/skills/auto-clipper/auto_clipper.py --video video.mp4 --clips 10
```

### 📋 Dependencies (Install First)
```bash
pip install faster-whisper textblob vaderSentiment
pip install moviepy opencv-python ffmpeg-python
pip install customtkinter pillow
```

### 🔗 Integration with OpenClaw
The skill is automatically available in OpenClaw's skill registry.
Can be invoked via skill selector or automation flows.

### 📞 Support
- Skill Documentation: SKILL.md
- Source Code: /core/
- Examples: auto_clipper.py (main function)

---

**Status:** ✅ COMPLETE AND READY
**Location:** ~/.openclaw/workspace/skills/auto-clipper/