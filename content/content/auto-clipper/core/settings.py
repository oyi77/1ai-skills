"""
Auto Clipper Indonesia - Settings
Default configuration for standalone skill
"""

import logging
from pathlib import Path

# Create directories
OUTPUT_DIR = Path(__file__).parent.parent / "output"
TEMP_DIR = Path(__file__).parent.parent / "temp"
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
DEFAULT_CLIP_DURATION = 30
MIN_CLIP_DURATION = 10
MAX_CLIP_DURATION = 60
DEFAULT_OUTPUT_FORMAT = 'mp4'
DEFAULT_OUTPUT_RESOLUTION = '720p'
DEFAULT_BITRATE = '2000k'

# 9:16 Settings
ASPECT_RATIO_WIDTH = 1080
ASPECT_RATIO_HEIGHT = 1920

# AI Settings
TRANSCRIPTION_MODEL = "base"
WHISPER_LANGUAGE = "id"
GOLDEN_MOMENT_COUNT = 10

# Subtitle Settings
SUBTITLE_FONT_FAMILY = "Arial"
SUBTITLE_FONT_SIZE = 28
SUBTITLE_FONT_COLOR = "white"
SUBTITLE_STROKE_COLOR = "black"
SUBTITLE_STROKE_WIDTH = 3
SUBTITLE_POSITION = "bottom"

# Logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)