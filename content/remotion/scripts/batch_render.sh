#!/bin/bash
# =============================================================
# Batch Render Script for Remotion
# =============================================================
# Renders multiple Remotion compositions in one command.
# No API. No internet. Just npx remotion render + ffmpeg.
#
# Usage:
#   chmod +x scripts/batch_render.sh
#   ./scripts/batch_render.sh                      # render all compositions
#   ./scripts/batch_render.sh NarratedVideo        # render one by name
#   ./scripts/batch_render.sh --codec gif          # render all as GIF
#   ./scripts/batch_render.sh --scale 0.5          # half size (for testing)
#   ./scripts/batch_render.sh --list               # list all compositions
#   ./scripts/batch_render.sh --props '{"lang":"id"}' # pass props
#
# Environment variables:
#   CODEC=h264         output codec (h264, h265, vp8, vp9, gif, prores)
#   CRF=18             quality (lower = better, default 18)
#   SCALE=1            output scale (0.5 = half size for testing)
#   CONCURRENCY=1      parallel render processes (CPU-heavy, use 1)
#   PROPS='{}'         JSON props to pass to all compositions
# =============================================================

set -e

# ── CONFIG ───────────────────────────────────────────────────
CODEC="${CODEC:-h264}"
CRF="${CRF:-18}"
SCALE="${SCALE:-1}"
CONCURRENCY="${CONCURRENCY:-1}"
PROPS="${PROPS:-}"
OUT_DIR="${OUT_DIR:-out}"

# ── PARSE ARGS ────────────────────────────────────────────────
SPECIFIC_COMP=""
JUST_LIST=false
EXTRA_FLAGS=""

for arg in "$@"; do
  case $arg in
    --list)           JUST_LIST=true ;;
    --codec=*)        CODEC="${arg#*=}" ;;
    --scale=*)        SCALE="${arg#*=}" ;;
    --crf=*)          CRF="${arg#*=}" ;;
    --props=*)        PROPS="${arg#*=}" ;;
    --out-dir=*)      OUT_DIR="${arg#*=}" ;;
    --*)              EXTRA_FLAGS="$EXTRA_FLAGS $arg" ;;
    *)                SPECIFIC_COMP="$arg" ;;
  esac
done

# ── CHECKS ────────────────────────────────────────────────────
if ! command -v npx &> /dev/null; then
  echo "❌ npx not found. Install Node.js: https://nodejs.org"
  exit 1
fi

if [ ! -f "package.json" ]; then
  echo "❌ No package.json found. Run from your Remotion project root."
  exit 1
fi

mkdir -p "$OUT_DIR"

# ── LIST COMPOSITIONS ─────────────────────────────────────────
if $JUST_LIST; then
  echo "📋 Available compositions:"
  npx remotion compositions 2>/dev/null || \
    echo "  (run 'npm run dev' to see compositions in Studio)"
  exit 0
fi

# ── BUILD RENDER FLAGS ────────────────────────────────────────
RENDER_FLAGS="--codec $CODEC --scale $SCALE"

if [ "$CODEC" = "h264" ] || [ "$CODEC" = "h265" ]; then
  RENDER_FLAGS="$RENDER_FLAGS --crf $RENDER_FLAGS"
fi

if [ -n "$PROPS" ]; then
  RENDER_FLAGS="$RENDER_FLAGS --props='$PROPS'"
fi

RENDER_FLAGS="$RENDER_FLAGS $EXTRA_FLAGS"

# ── FILE EXTENSION ────────────────────────────────────────────
case $CODEC in
  gif)    EXT="gif" ;;
  vp8)    EXT="webm" ;;
  vp9)    EXT="webm" ;;
  prores) EXT="mov" ;;
  *)      EXT="mp4" ;;
esac

# ── RENDER ────────────────────────────────────────────────────
echo ""
echo "🎬 Remotion Batch Render"
echo "   Codec:  $CODEC"
echo "   Scale:  ${SCALE}x"
echo "   Output: $OUT_DIR/"
echo ""

START_TIME=$SECONDS

if [ -n "$SPECIFIC_COMP" ]; then
  # Render single named composition
  OUT_FILE="$OUT_DIR/${SPECIFIC_COMP}.${EXT}"
  echo "▶ Rendering: $SPECIFIC_COMP → $OUT_FILE"

  CMD="npx remotion render $SPECIFIC_COMP $OUT_FILE $RENDER_FLAGS"
  echo "  CMD: $CMD"
  eval "$CMD"

  if [ -f "$OUT_FILE" ]; then
    SIZE=$(du -sh "$OUT_FILE" | cut -f1)
    echo "  ✅ Done: $OUT_FILE ($SIZE)"
  fi

else
  # Render all compositions
  echo "🔍 Discovering compositions..."

  # Get list of composition IDs from Remotion
  COMPOSITIONS=$(npx remotion compositions --quiet 2>/dev/null | \
    grep -E '^[A-Za-z]' | awk '{print $1}' || true)

  if [ -z "$COMPOSITIONS" ]; then
    echo "  ⚠️  Could not auto-discover compositions."
    echo "  Manually specify: ./scripts/batch_render.sh CompositionId"
    echo "  Or list them: ./scripts/batch_render.sh --list"
    exit 1
  fi

  TOTAL=$(echo "$COMPOSITIONS" | wc -l | xargs)
  echo "   Found $TOTAL composition(s)"
  echo ""

  SUCCESS=0
  FAIL=0

  while IFS= read -r COMP; do
    [ -z "$COMP" ] && continue
    OUT_FILE="$OUT_DIR/${COMP}.${EXT}"
    echo "▶ [$((SUCCESS + FAIL + 1))/$TOTAL] $COMP"

    CMD="npx remotion render $COMP $OUT_FILE $RENDER_FLAGS"

    if eval "$CMD" 2>&1 | tail -5; then
      SIZE=$(du -sh "$OUT_FILE" 2>/dev/null | cut -f1 || echo "?")
      echo "  ✅ $OUT_FILE ($SIZE)"
      SUCCESS=$((SUCCESS + 1))
    else
      echo "  ❌ Failed: $COMP"
      FAIL=$((FAIL + 1))
    fi
    echo ""

  done <<< "$COMPOSITIONS"

  ELAPSED=$((SECONDS - START_TIME))
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ Batch complete in ${ELAPSED}s"
  echo "   Success: $SUCCESS / $((SUCCESS + FAIL))"
  if [ $FAIL -gt 0 ]; then
    echo "   Failed:  $FAIL"
  fi
fi

echo ""
echo "Output files:"
ls -lh "$OUT_DIR"/*.mp4 "$OUT_DIR"/*.webm "$OUT_DIR"/*.gif 2>/dev/null | \
  awk '{print "  "$5, $9}' || echo "  (no files found)"

echo ""
echo "Next: run post-processing?"
echo "  ./scripts/postprocess.sh --formats mp4,vertical,gif"
