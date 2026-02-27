#!/bin/bash
# Force reload Vilona persona
# Usage: ./force-vilona.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOUL_FILE="/home/openclaw/.openclaw/workspace/SOUL.md"

echo "🔥 Vilona: Forcing persona reload..."
echo "Reading SOUL.md from: $SOUL_FILE"
cat "$SOUL_FILE"

echo "✅ Done. Persona should now be active."
echo "Note: Send any message to trigger re-evaluation."
