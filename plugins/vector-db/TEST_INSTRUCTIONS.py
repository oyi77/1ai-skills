#!/usr/bin/env python3
"""
Vector DB Plugin Test - Manual Steps
Since exec is restricted, run these tests manually in terminal
"""

print("""
🧪 Vector DB Plugin - Test Instructions
═══════════════════════════════════════════════════════════════

Since elevated mode requires manual confirmation for new commands,
run these tests manually in your terminal:

─────────────────────────────────────────────────────────────
STEP 1: Install Dependencies
─────────────────────────────────────────────────────────────

pip install chromadb sentence-transformers numpy tiktoken PyPDF2

─────────────────────────────────────────────────────────────
STEP 2: Test Individual Engines
─────────────────────────────────────────────────────────────

cd ~/.openclaw/workspace/plugins/vector-db

# Test ZVec Engine
python3 zvec/engine.py

# Test PageIndex Engine  
python3 pageindex/engine.py

# Test Ruvector Engine
python3 ruvector/engine.py

─────────────────────────────────────────────────────────────
STEP 3: Test Unified Engine
─────────────────────────────────────────────────────────────

python3 shared/engine.py

─────────────────────────────────────────────────────────────
STEP 4: Validate Plugin Structure
─────────────────────────────────────────────────────────────

python3 validate.py

─────────────────────────────────────────────────────────────
STEP 5: Test via OpenClaw (after restart)
─────────────────────────────────────────────────────────────

# Restart OpenClaw
openclaw restart

# Then test via Python in OpenClaw session:
"""

# Test code untuk copy-paste ke OpenClaw:
test_code = '''
# Test 1: Unified Engine
from plugins.vector_db.shared.engine import VectorEngine, smart_chunk

engine = VectorEngine()
print(f"Engines: {list(engine.engines.keys())}")

# Test 2: Smart chunking
text = "# Header\\n\\nContent here.\\n\\n## Subheader\\nMore content."
chunks = smart_chunk(text, 500)
print(f"Chunks: {len(chunks)}")

# Test 3: Search (if content indexed)
results = engine.search("test query", top_k=3)
print(f"Results: {len(results)}")
'''

print(test_code)

print("""
─────────────────────────────────────────────────────────────
STEP 6: Copy Plugin to OpenClaw Plugins Dir
─────────────────────────────────────────────────────────────

# Copy plugin ke OpenClaw plugins directory
mkdir -p ~/.openclaw/plugins
cp -r ~/.openclaw/workspace/plugins/vector-db ~/.openclaw/plugins/

# Restart OpenClaw
openclaw restart

─────────────────────────────────────────────────────────────
EXPECTED OUTPUT
─────────────────────────────────────────────────────────────

For each engine test, you should see:
✅ Engine initialized
✅ X chunks indexed
✅ Y results found
✅ Score: Z.XXX

For unified engine:
✅ Engines: ['zvec', 'pageindex', 'ruvector']
✅ Available fallbacks: [...models...]

═══════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════

Problem: "ImportError: No module named 'chromadb'"
Solution: pip install chromadb sentence-transformers

Problem: "Permission denied"
Solution: Use pip3 or add --user flag

Problem: "Engine not found"
Solution: Check file paths in ~/.openclaw/workspace/plugins/vector-db/

═══════════════════════════════════════════════════════════════
CONTACT
═══════════════════════════════════════════════════════════════

Plugin files: ~/.openclaw/workspace/plugins/vector-db/
Config: ~/.openclaw/openclaw.json
Cache: ~/.openclaw/vector-cache/

""")
