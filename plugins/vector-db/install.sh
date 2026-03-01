#!/bin/bash
# Vector DB Plugin Installation Script

echo "🔌 Installing Vector DB Plugin for OpenClaw..."
echo ""

# Check Python
echo "📦 Checking Python dependencies..."

pip install --quiet chromadb sentence-transformers numpy tiktoken 2>/dev/null || pip3 install --quiet chromadb sentence-transformers numpy tiktoken

if [ $? -eq 0 ]; then
    echo "✅ Core dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Optional PDF support
echo "📄 Installing optional PDF support..."
pip install --quiet PyPDF2 2>/dev/null || pip3 install --quiet PyPDF2

if [ $? -eq 0 ]; then
    echo "✅ PDF support installed"
fi

# Create cache directories
echo "📁 Setting up cache directories..."
mkdir -p ~/.openclaw/vector-cache/{zvec,pageindex,ruvector}

# Verify plugin structure
echo "🔍 Verifying plugin structure..."

PLUGIN_DIR="${1:-.}/plugins/vector-db"

if [ -d "$PLUGIN_DIR" ]; then
    echo "✅ Plugin directory found: $PLUGIN_DIR"
    
    # Check required files
    REQUIRED=(
        "manifest.json"
        "__init__.py"
        "shared/engine.py"
        "zvec/engine.py"
        "pageindex/engine.py"
        "ruvector/engine.py"
    )
    
    MISSING=0
    for file in "${REQUIRED[@]}"; do
        if [ -f "$PLUGIN_DIR/$file" ]; then
            echo "  ✅ $file"
        else
            echo "  ❌ Missing: $file"
            MISSING=$((MISSING + 1))
        fi
    done
    
    if [ $MISSING -eq 0 ]; then
        echo ""
        echo "🎉 Vector DB Plugin ready!"
        echo ""
        echo "Quick test:"
        echo "  cd $PLUGIN_DIR && python3 shared/engine.py"
    else
        echo ""
        echo "⚠️  $MISSING file(s) missing. Plugin may not work correctly."
    fi
else
    echo "❌ Plugin directory not found: $PLUGIN_DIR"
    exit 1
fi

echo ""
echo "To integrate with OpenClaw:"
echo "  1. Copy plugin to ~/.openclaw/plugins/vector-db/"
echo "  2. Restart OpenClaw"
echo "  3. Plugin will auto-load via manifest.json"