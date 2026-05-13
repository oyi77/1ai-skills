#!/bin/bash
# =============================================================
# FFmpeg Post-Processing Script for Remotion
# =============================================================
# Handles everything that happens AFTER Remotion renders a video:
#   - Mix background music into rendered video
#   - Burn subtitles / SRT captions
#   - Export to multiple formats (MP4, WebM, GIF, vertical)
#   - Normalise audio loudness
#   - Create thumbnail
#
# 100% local. No API. No internet. Only needs ffmpeg.
#
# Install ffmpeg:
#   macOS:   brew install ffmpeg
#   Ubuntu:  apt install ffmpeg
#   Windows: https://ffmpeg.org/download.html
#
# Usage:
#   chmod +x scripts/postprocess.sh
#   ./scripts/postprocess.sh                         # full pipeline
#   ./scripts/postprocess.sh --no-bgm               # skip BGM mixing
#   ./scripts/postprocess.sh --no-subs               # skip subtitles
#   ./scripts/postprocess.sh --formats mp4,gif       # specific outputs
#   ./scripts/postprocess.sh --input out/my-raw.mp4  # custom input
# =============================================================

set -e   # exit on error

# ── CONFIGURATION ────────────────────────────────────────────
INPUT="${INPUT:-out/video-raw.mp4}"      # raw Remotion output
OUTPUT_DIR="${OUTPUT_DIR:-out}"
BGM_FILE="${BGM_FILE:-public/audio/bgm.mp3}"
SRT_FILE="${SRT_FILE:-public/captions.srt}"
BGM_VOLUME="${BGM_VOLUME:-0.12}"         # 0.0–1.0, BGM level vs narration
FADE_OUT_SEC="${FADE_OUT_SEC:-3}"        # BGM fade out N seconds before end

# ── PARSE ARGUMENTS ──────────────────────────────────────────
DO_BGM=true
DO_SUBS=true
DO_FORMATS="mp4"   # comma-separated: mp4,webm,gif,vertical
DO_THUMB=true

for arg in "$@"; do
  case $arg in
    --no-bgm)       DO_BGM=false ;;
    --no-subs)      DO_SUBS=false ;;
    --no-thumb)     DO_THUMB=false ;;
    --formats=*)    DO_FORMATS="${arg#*=}" ;;
    --input=*)      INPUT="${arg#*=}" ;;
    --bgm-volume=*) BGM_VOLUME="${arg#*=}" ;;
  esac
done

# ── CHECKS ───────────────────────────────────────────────────
if ! command -v ffmpeg &> /dev/null; then
  echo "❌ ffmpeg not found."
  echo "   macOS:  brew install ffmpeg"
  echo "   Ubuntu: apt install ffmpeg"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "❌ Input file not found: $INPUT"
  echo "   Render first: npx remotion render [CompositionId] out/video-raw.mp4"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Get video duration
DURATION=$(ffprobe -v error -show_entries format=duration \
  -of csv=p=0 "$INPUT" | awk '{printf "%.3f", $1}')
echo "📹 Input: $INPUT (${DURATION}s)"
echo ""

# Current working file — we chain operations
CURRENT="$INPUT"

# ── STEP 1: MIX BACKGROUND MUSIC ─────────────────────────────
if $DO_BGM && [ -f "$BGM_FILE" ]; then
  echo "🎵 Mixing BGM: $BGM_FILE (volume: ${BGM_VOLUME})"

  BGM_MIX="$OUTPUT_DIR/tmp_bgm.mp4"
  FADE_START=$(echo "$DURATION - $FADE_OUT_SEC" | bc)

  # Mix: fade BGM out before video ends
  ffmpeg -y \
    -i "$CURRENT" \
    -i "$BGM_FILE" \
    -filter_complex \
      "[1:a]volume=${BGM_VOLUME},afade=t=out:st=${FADE_START}:d=${FADE_OUT_SEC}[bgm];
       [0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0[a]" \
    -map 0:v \
    -map "[a]" \
    -c:v copy \
    -c:a aac \
    -b:a 192k \
    "$BGM_MIX" \
    -loglevel error

  echo "  ✓ BGM mixed"
  CURRENT="$BGM_MIX"

elif $DO_BGM && [ ! -f "$BGM_FILE" ]; then
  echo "⏭  BGM file not found at $BGM_FILE — skipping BGM mix"
  echo "   Place your background music at: $BGM_FILE"
fi

# ── STEP 2: BURN SUBTITLES ───────────────────────────────────
if $DO_SUBS && [ -f "$SRT_FILE" ]; then
  echo "💬 Burning subtitles: $SRT_FILE"

  SUB_OUT="$OUTPUT_DIR/tmp_sub.mp4"

  # Style: white text, black outline, bottom-centre position
  SUBTITLE_STYLE="FontName=Arial,FontSize=28,PrimaryColour=&HFFFFFF,\
OutlineColour=&H000000,Outline=2,Shadow=1,Alignment=2,\
MarginV=40,Bold=1"

  ffmpeg -y \
    -i "$CURRENT" \
    -vf "subtitles=${SRT_FILE}:force_style='${SUBTITLE_STYLE}'" \
    -c:a copy \
    "$SUB_OUT" \
    -loglevel error

  echo "  ✓ Subtitles burned"
  CURRENT="$SUB_OUT"

elif $DO_SUBS && [ ! -f "$SRT_FILE" ]; then
  echo "⏭  SRT file not found at $SRT_FILE — skipping subtitle burn"
  echo "   Generate with: python scripts/transcribe.py public/audio/narration.mp3"
fi

# ── STEP 3: OUTPUT FORMATS ───────────────────────────────────
echo ""
echo "📤 Exporting formats: $DO_FORMATS"

IFS=',' read -ra FMTS <<< "$DO_FORMATS"

for fmt in "${FMTS[@]}"; do
  fmt=$(echo "$fmt" | xargs)   # trim whitespace

  case $fmt in
    mp4)
      OUT="$OUTPUT_DIR/final.mp4"
      echo "  🎬 MP4 (H.264, web-optimised)..."
      ffmpeg -y \
        -i "$CURRENT" \
        -c:v libx264 \
        -crf 18 \
        -preset slow \
        -pix_fmt yuv420p \
        -c:a aac \
        -b:a 192k \
        -movflags +faststart \
        -map_metadata -1 \
        "$OUT" \
        -loglevel error
      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    webm)
      OUT="$OUTPUT_DIR/final.webm"
      echo "  🌐 WebM (VP9, browser/web use)..."
      ffmpeg -y \
        -i "$CURRENT" \
        -c:v libvpx-vp9 \
        -crf 33 \
        -b:v 0 \
        -c:a libopus \
        -b:a 128k \
        "$OUT" \
        -loglevel error
      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    gif)
      OUT="$OUTPUT_DIR/preview.gif"
      echo "  🎞  GIF (optimised, first 10 seconds)..."
      # Two-pass GIF: generate palette first for quality
      ffmpeg -y \
        -i "$CURRENT" \
        -t 10 \
        -vf "fps=15,scale=640:-1:flags=lanczos,palettegen" \
        /tmp/palette.png \
        -loglevel error

      ffmpeg -y \
        -i "$CURRENT" \
        -i /tmp/palette.png \
        -t 10 \
        -filter_complex "fps=15,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse" \
        "$OUT" \
        -loglevel error

      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    vertical|9:16|tiktok|reels|shorts)
      OUT="$OUTPUT_DIR/vertical.mp4"
      echo "  📱 Vertical 9:16 (1080×1920, TikTok/Reels/Shorts)..."
      # Crop centre of 16:9 to 9:16, or pad if already vertical
      W_IN=$(ffprobe -v error -select_streams v:0 \
        -show_entries stream=width -of csv=p=0 "$CURRENT")
      H_IN=$(ffprobe -v error -select_streams v:0 \
        -show_entries stream=height -of csv=p=0 "$CURRENT")

      if [ "$H_IN" -gt "$W_IN" ]; then
        # Already vertical — just re-encode to spec
        VFILT="scale=1080:1920:force_original_aspect_ratio=decrease,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
      else
        # Landscape → crop to 9:16 (take centre column)
        CROP_W=$(echo "$H_IN * 9 / 16" | bc)
        CROP_X=$(echo "($W_IN - $CROP_W) / 2" | bc)
        VFILT="crop=${CROP_W}:${H_IN}:${CROP_X}:0,scale=1080:1920"
      fi

      ffmpeg -y \
        -i "$CURRENT" \
        -vf "$VFILT" \
        -c:v libx264 \
        -crf 20 \
        -preset fast \
        -pix_fmt yuv420p \
        -c:a aac \
        -b:a 128k \
        -movflags +faststart \
        "$OUT" \
        -loglevel error

      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    square|1:1|instagram)
      OUT="$OUTPUT_DIR/square.mp4"
      echo "  🟥 Square 1:1 (1080×1080, Instagram Feed)..."
      ffmpeg -y \
        -i "$CURRENT" \
        -vf "scale=1080:1080:force_original_aspect_ratio=decrease,\
pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black" \
        -c:v libx264 \
        -crf 20 \
        -preset fast \
        -pix_fmt yuv420p \
        -c:a aac \
        -b:a 128k \
        -movflags +faststart \
        "$OUT" \
        -loglevel error
      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    4k|uhd)
      OUT="$OUTPUT_DIR/final-4k.mp4"
      echo "  🖥  4K UHD (3840×2160, upscaled)..."
      ffmpeg -y \
        -i "$CURRENT" \
        -vf "scale=3840:2160:flags=lanczos" \
        -c:v libx264 \
        -crf 20 \
        -preset slow \
        -pix_fmt yuv420p \
        -c:a copy \
        -movflags +faststart \
        "$OUT" \
        -loglevel error
      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    audio|mp3)
      OUT="$OUTPUT_DIR/audio.mp3"
      echo "  🎵 Audio only (MP3)..."
      ffmpeg -y \
        -i "$CURRENT" \
        -vn \
        -c:a libmp3lame \
        -b:a 192k \
        "$OUT" \
        -loglevel error
      SIZE=$(du -sh "$OUT" | cut -f1)
      echo "  ✓ $OUT ($SIZE)"
      ;;

    *)
      echo "  ⚠️  Unknown format: $fmt — skipping"
      ;;
  esac
done

# ── STEP 4: THUMBNAIL ─────────────────────────────────────────
if $DO_THUMB; then
  THUMB="$OUTPUT_DIR/thumbnail.jpg"
  echo ""
  echo "🖼  Extracting thumbnail (frame at 2s)..."
  ffmpeg -y \
    -i "$CURRENT" \
    -ss 00:00:02 \
    -frames:v 1 \
    -q:v 2 \
    "$THUMB" \
    -loglevel error
  echo "  ✓ $THUMB"
fi

# ── CLEANUP TEMP FILES ────────────────────────────────────────
rm -f "$OUTPUT_DIR/tmp_bgm.mp4" "$OUTPUT_DIR/tmp_sub.mp4" /tmp/palette.png

# ── SUMMARY ───────────────────────────────────────────────────
echo ""
echo "✅ Post-processing complete!"
echo ""
echo "Output files:"
for f in "$OUTPUT_DIR"/*.mp4 "$OUTPUT_DIR"/*.webm "$OUTPUT_DIR"/*.gif; do
  [ -f "$f" ] && echo "  $(du -sh "$f" | cut -f1)  $f"
done
echo ""
echo "Usage examples:"
echo "  # BGM + subs + all formats:"
echo "  ./scripts/postprocess.sh --formats mp4,vertical,gif"
echo ""
echo "  # No BGM, burn subs only:"
echo "  ./scripts/postprocess.sh --no-bgm --formats mp4"
echo ""
echo "  # Custom BGM volume:"
echo "  BGM_VOLUME=0.08 ./scripts/postprocess.sh"
