# Auto Clipper Indonesia 🇮🇩

AI-powered video clipper software - Convert long-form videos into multiple viral Shorts/TikToks/Reels automatically.

## 🎯 Project Overview

**Product:** Windows Desktop Application
**Price:** Rp 298.000 (lifetime)
**Target:** Indonesian content creators
**Status:** Phase 1: MVP Development (Day 1 - Started)

---

## ✨ Key Features

### MVP (Week 1)
- ✅ Video upload interface
- ✅ AI transcription (Whisper)
- ✅ Golden moment detection
- ✅ Manual clip selection
- ✅ Basic clipping & export
- ✅ 9:16 center crop

### Full Product (Week 4)
- 🎯 Face tracking & auto-reframe
- 📝 Subtitle hardcode (Indonesian/English)
- 🚀 Bulk processing (unlimited)
- 📲 Auto-distribution (TikTok/IG/YT)
- 🎨 Multiple subtitle styles
- 💾 Professional GUI

---

## 📁 Project Structure

```
auto-clipper-indonesia/
├── src/
│   ├── main.py                    # Entry point
│   ├── gui/                       # GUI components
│   │   ├── main_window.py        # Main window ✅
│   │   ├── upload_panel.py       # Video upload ✅
│   │   ├── analyze_panel.py      # Analysis UI ✅
│   │   ├── clip_panel.py         # Clip selection ✅
│   │   └── export_panel.py       # Export management ✅
│   ├── core/                      # Business logic
│   │   ├── video_analyzer.py     # AI analysis (TODO)
│   │   ├── clip_engine.py        # Video clipping (TODO)
│   │   ├── reframe_engine.py     # 9:16 reframe (TODO)
│   │   └── subtitle_engine.py    # Subtitles (TODO)
│   ├── distribution/              # Platform upload (TODO)
│   │   ├── tiktok_uploader.py
│   │   ├── instagram_uploader.py
│   │   └── youtube_uploader.py
│   └── utils/                     # Utilities ✅
│       ├── config.py             # App settings ✅
│       └── logger.py             # Logging ✅
├── assets/                        # Media files
├── logs/                          # System logs
├── output/                        # Exported videos
├── temp/                          # Temporary files
├── tests/                         # Test suite
├── docs/                          # Documentation
├── requirements.txt               # Dependencies ✅
├── setup.py                       # Build script ✅
└── README.md                      # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Windows 10/11 64-bit
- GPU optional (for acceleration)

### Installation

```bash
# Clone/download project
cd auto-clipper-indonesia

# Install dependencies
pip install -r requirements.txt

# Run application
cd src
python main.py
```

### Build Executable

```bash
# Build Windows .exe using PyInstaller
python setup.py build

# Output: build/auto_clipper.exe
```

---

## 📅 Development Timeline

### Week 1: MVP Core (Days 1-5)
- ✅ Day 1: Project structure + GUI foundation
- ⏳ Day 2 (TOMORROW): AI analysis engine (Whisper + sentiment)
- ⏳ Day 3: Clip engine (FFmpeg integration)
- ⏳ Day 4: Integration & workflow
- ⏳ Day 5: Testing & refinement

**Deliverable:** Working prototype that can upload, analyze, and export clips

### Week 2: Advanced Features
- Face tracking reframe
- Subtitle generation & hardcode
- Style templates

### Week 3: Distribution Automation
- TikTok/IG/YT upload APIs
- Bulk processing
- Scheduling

### Week 4: Productization
- Error handling & optimization
- User testing
- Packaging (.exe installer)
- Documentation

---

## 🛠️ Tech Stack

**Video Processing**
- FFmpeg, MoviePy, OpenCV

**AI & Analysis**
- Faster-Whisper (transcription)
- TextBlob, VADER (sentiment)

**GUI**
- CustomTkinter (modern Python GUI)

**Distribution**
- TikTok API
- Instagram (PostBridge)
- YouTube Data API

---

## 💼 Business Model

**Product:** Lifetime software license
**Price:** Rp 298.000 - Rp 498.500
**Marketplaces:** Shopee, Tokopedia, Direct website

**Revenue Projections:**
- 10 sales = Rp 3-5 million
- 50 sales = Rp 15-25 million
- 100 sales = Rp 30-50 million

---

## 📊 Current Status (Day 1)

### Completed ✅
- [x] Project structure created
- [x] Tech stack defined
- [x] Requirements file
- [x] Config & utility modules
- [x] GUI foundation (main window + 4 panels)
- [x] Upload panel (file browser)
- [x] Analysis panel (progress UI)
- [x] Clip panel (selection + settings)
- [x] Export panel (list + folder)

### Next Steps (Day 2 - TOMORROW)
- [ ] Install faster-whisper
- [ ] Create video analyzer module
- [ ] Implement transcription pipeline
- [ ] Build golden moment detection
- [ ] Connect analyzer to GUI

---

## 🎯 Success Criteria

**MVP Success (Day 5)**
- ✅ Video loads successfully
- ⏳ Transcription works (95% accuracy)
- ⏳ Detects top 10 moments correctly
- ⏳ Clips export properly
- ⏳ No crashes on test videos

**Product Success (Day 28)**
- 🎯 All features implemented
- 🎯 <2 minutes per clip
- 🎯 Stable on Windows
- 🎯 5 beta testers approve

---

## 🆘 Troubleshooting

### Common Issues

**Import Error: customtkinter not found**
```bash
pip install customtkinter
```

**FFmpeg not found**
- Windows: Install from https://ffmpeg.org/download.html
- Add to PATH: `C:\ffmpeg\bin`

**Whisper transcription slow**
- Use faster-whisper instead of standard Whisper
- Check GPU support (CUDA if available)

---

## 📞 Support

- **Documentation:** Check `/docs` folder
- **Issues:** Submit to project tracker
- **Contact:** contact@berkahkarya.id

---

## 📝 License

Proprietary - BerkahKarya

---

**Updated:** March 12, 2026 (Day 1 - Phase 1)
**Next Update:** Day 2 - AI Analysis Engine 🔥