#!/bin/bash
# Vector DB Plugin - Deployment Script
# Run this in terminal to deploy the plugin

echo "═══════════════════════════════════════════════════════════"
echo "🚀 Vector DB Plugin Deployment"
echo "═══════════════════════════════════════════════════════════"
echo ""

PLUGIN_SOURCE="/home/openclaw/.openclaw/workspace/plugins/vector-db"
PLUGIN_TARGET="$HOME/.openclaw/plugins/vector-db"

echo "📍 Source: $PLUGIN_SOURCE"
echo "📍 Target: $PLUGIN_TARGET"
echo ""

# Check source exists
if [ ! -d "$PLUGIN_SOURCE" ]; then
    echo "❌ Plugin source not found!"
    exit 1
fi

# Create target directory
echo "📁 Creating plugin directory..."
mkdir -p "$PLUGIN_TARGET"

# Copy files
echo "📂 Copying plugin files..."
cp -r "$PLUGIN_SOURCE"/* "$PLUGIN_TARGET/"

# Verify
echo ""
echo "✅ Plugin deployed!"
echo ""
echo "📂 Files copied:"
ls -la "$PLUGIN_TARGET/" | head -20

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "   1. Install dependencies: pip install chromadb sentence-transformers"
echo "   2. Restart OpenClaw if needed"
echo "   3. Test: python3 -c 'from plugins.vector_db import VectorEngine; print(\"OK\")'"
echo ""
echo "Plugin ready to use! 🎉"