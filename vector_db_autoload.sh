#!/bin/bash
# Vector DB Auto-Loader
# Add this to ~/.bashrc or ~/.zshrc or openclaw startup

echo "🔄 Loading Vector DB Tools..."

# Add to PYTHONPATH
export PYTHONPATH="/home/openclaw/.openclaw/plugins:/home/openclaw/.openclaw/workspace/tools:$PYTHONPATH"

# Create python startup file
cat > /tmp/vector_db_startup.py << 'EOF'
import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools')

# Import tools
try:
    from vector_db_tools import vector_search, vector_index, vector_chunk, vector_status
    print("✅ Vector DB tools loaded: vector_search, vector_index, vector_chunk, vector_status")
except Exception as e:
    print(f"⚠️  Could not load Vector DB tools: {e}")
EOF

# Run python with startup
alias python3='python3 -i /tmp/vector_db_startup.py'

echo "✅ Vector DB Auto-Loader configured"
echo "Tools available:"
echo "  - vector_search(query, top_k=5)"
echo "  - vector_index(content, title, source)"
echo "  - vector_chunk(text, max_tokens=500)"
echo "  - vector_status()"

# Optional: Add to python startup for all sessions
if [ -f ~/.pythonrc ]; then
    echo "import sys; sys.path.insert(0, '/home/openclaw/.openclaw/plugins'); sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools'); from vector_db_tools import vector_search, vector_index, vector_chunk, vector_status" >> ~/.pythonrc
    export PYTHONSTARTUP=~/.pythonrc
fi
