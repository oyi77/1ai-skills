# Auto Clipper Indonesia - Changelog

## [2.0.0] - 2026-03-12

### 🎉 Major Upgrade: ViMax-Inspired Features

Based on study of HKUDS/ViMax (https://github.com/HKUDS/ViMax)

#### New Features

##### 1. Consistency Engine (`core/consistency_engine.py`)
- Track character appearance across multiple clips
- Scene context preservation (location, time, style)
- Smart reference selection for visual consistency
- Color and brightness grading corrections
- Import/export consistency context

**Usage:**
```python
from core import ConsistencyEngine

engine = ConsistencyEngine()
engine.set_reference("reference.mp4", characters=["Speaker"])
report = engine.check_consistency("new_clip.mp4")
engine.apply_consistency_corrections("input.mp4", "output.mp4")
```

##### 2. Storyboard Generator (`core/storyboard_generator.py`)
- Auto-generate shot lists from content type
- Professional cinematography planning
- 5 pre-built templates:
  - `hook_open` - 15-30s attention grabber
  - `insight_explanation` - 30s educational
  - `emotional_peak` - 20s storytelling
  - `product_showcase` - 30s product demo
  - `before_after` - 25s transformation
- 10 shot types: Wide, Medium, Close-Up, POV, etc.
- Camera movement planning (Pan, Zoom, Dolly, Track)
- JSON export for editing software integration

**Usage:**
```python
from core import generate_quick_storyboard, StoryboardGenerator

# Quick generation
sb = generate_quick_storyboard("hook_open", 30)

# Full control
gen = StoryboardGenerator()
sb = gen.generate_short_form("product_showcase", 30)
gen.print_storyboard(sb)
gen.export_storyboard(sb, "storyboard.json")
```

##### 3. New Enums
- `ShotType` - WIDE, MEDIUM, CLOSE_UP, EXTREME_CLOSE_UP, POV, etc.
- `CameraMovement` - STATIC, PAN, ZOOM, DOLLY, TRACK, etc.

#### Improvements

- Enhanced workflow orchestration with consistency checks
- Better storyboard-to-processing integration
- Production-ready shot planning
- Professional cinematographic output

#### Documentation

- `VIMAX_UPGRADE.md` - Full upgrade notes
- `auto_clipper_demo.py` - Complete demo script
- Updated `SKILL.md` - All v2.0 features documented

#### Breaking Changes

None - fully backward compatible with v1.0

#### Files Changed

```
+ core/consistency_engine.py      (NEW - 16KB)
+ core/storyboard_generator.py    (NEW - 19KB)
+ VIMAX_UPGRADE.md                (NEW - 8KB)
+ auto_clipper_demo.py            (NEW - 8KB)
* core/__init__.py                (Updated imports)
* SKILL.md                        (Updated documentation)
```

---

## [1.0.0] - 2026-03-12

Initial release

- Core video processing (FFmpeg/MoviePy)
- AI transcription (faster-whisper)
- Golden moment detection
- 9:16 vertical reframe
- Subtitle burn-in
- Batch processing
- Progress tracking

---

## Upgrade Path

**From v1.0 to v2.0:**
```bash
cd ~/.openclaw/workspace/skills/auto-clipper
git pull  # Or copy new files
pip install opencv-python  # Optional, for face detection
python3 auto_clipper_demo.py  # Verify installation
```

**Quick Test:**
```python
from core import generate_quick_storyboard, ConsistencyEngine

# Test storyboard
sb = generate_quick_storyboard("hook_open", 15)
print(f"Generated {len(sb.clips)} shots")

# Test consistency (no video needed)
print("ConsistencyEngine ready for use")
```

---

*Generated: March 12, 2026*
*Based on: HKUDS/ViMax Research*