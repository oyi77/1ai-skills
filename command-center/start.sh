#!/bin/bash
# OpenClaw Command Center - Start Script
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-3337}"
HOST="${2:-127.0.0.1}"

echo "⚡ Starting OpenClaw Command Center..."
echo "   URL: http://${HOST}:${PORT}"
echo "   Press Ctrl+C to stop"
echo ""

# Kill any existing instance on this port
lsof -ti:${PORT} 2>/dev/null | xargs kill -9 2>/dev/null || true

node "${DIR}/server.js" --port "${PORT}" --host "${HOST}"
