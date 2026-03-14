"""
Auto Clipper Indonesia - Configuration
Store app settings and constants
"""

import os
from pathlib import Path

# App Info
APP_NAME = "Auto Clipper Indonesia"
VERSION = "1.0.0-MVP"
COMPANY = "BerkahKarya"

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
for dir_path in [ASSETS_DIR, OUTPUT_DIR, TEMP_DIR]:
    dir_path.mkdir(exist_ok=True)

# Video Processing Settings
# Supported formats
VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
AUDIO_FORMATS = ['.mp3', '.wav', '.aac']
IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

# Clip Settings
DEFAULT_CLIP_DURATION = 30  # seconds
MIN_CLIP_DURATION = 10     # seconds
MAX_CLIP_DURATION = 60     # seconds

# Output Settings
DEFAULT_OUTPUT_FORMAT = 'mp4'
DEFAULT_OUTPUT_RESOLUTION = '720p'  # 720p, 1080p
DEFAULT_BITRATE = '2000k'

# 9:16 Settings
ASPECT_RATIO_WIDTH = 1080
ASPECT_RATIO_HEIGHT = 1920

# AI Analysis Settings
TRANSCRIPTION_MODEL = "base"  # tiny, base, small, medium, large (faster-whisper)
WHISPER_LANGUAGE = "id"       # indonesian
SILICON_THRESHOLD = 0.5       # seconds (minimum silence to detect segment)
GOLDEN_MOMENT_COUNT = 10      # number of moments to detect

# Subtitle Settings
SUBTITLE_FONT_FAMILY = "Arial"
SUBTITLE_FONT_SIZE = 28
SUBTITLE_FONT_COLOR = "white"
SUBTITLE_STROKE_COLOR = "black"
SUBTITLE_STROKE_WIDTH = 3
SUBTITLE_POSITION = "bottom_center"

# API Keys (loaded from environment if needed)
WHISPER_DEVICE = "cpu"  # cpu or cuda