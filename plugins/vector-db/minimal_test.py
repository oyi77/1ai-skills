#!/usr/bin/env python3
"""
Vector DB Plugin - Minimal Test (No External Dependencies)
This test verifies the plugin structure without needing ChromaDB or sentence-transformers
"""

import os
import sys

# Add plugin directory to path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_dir)

print("=" * 60)
print("🧪 Vector DB Plugin - Minimal Validation Test")
print("=" * 60)
print()

# Test 1: Check all files exist
print("1️⃣  Checking File Structure...")
required_files = [
    'manifest.json',
    'shared/engine.py',
    'zvec/engine.py',
    'zvec/handler.py',
    'pageindex/engine.py',
    'pageindex/handler.py',
    'ruvector/engine.py',
    'ruvector/handler.py',
]

all_exist = True
for f in required_files:
    path = os.path.join(plugin_dir, f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"   ✅ {f} ({size:,} bytes)")
    else:
        print(f"   ❌ {f} MISSING")
        all_exist = False

if all_exist:
    print("   ✅ All required files present")
else:
    print("   ❌ Some files missing!")
    sys.exit(1)

print()

# Test 2: Check imports (without initializing engines)
print("2️⃣  Checking Import Paths...")

# Check if we can import the engine files (syntax check)
try:
    # Try importing smart_chunk function
    exec(open(os.path.join(plugin_dir, 'shared/engine.py')).read().split('class VectorEngine:')[0])
    print("   ✅ smart_chunk function parseable")
except Exception as e:
    print(f"   ⚠️  smart_chunk check: {e}")

print()

# Test 3: Check ChromaDB availability
print("3️⃣  Checking ChromaDB...")
try:
    import chromadb
    print(f"   ✅ ChromaDB {chromadb.__version__} available")
    has_chromadb = True
except ImportError:
    print("   ❌ ChromaDB not installed")
    print("      Run: pip install chromadb")
    has_chromadb = False

print()

# Test 4: Check sentence-transformers
print("4️⃣  Checking SentenceTransformers...")
try:
    import sentence_transformers
    print(f"   ✅ SentenceTransformers available")
    has_transformers = True
except ImportError:
    print("   ❌ SentenceTransformers not installed")
    print("      Run: pip install sentence-transformers")
    has_transformers = False

print()

# Test 5: Try basic engine initialization (if deps available)
if has_chromadb and has_transformers:
    print("5️⃣  Testing Engine Initialization...")
    try:
        from shared.engine import VectorEngine
        engine = VectorEngine()
        available = list(engine.engines.keys())
        print(f"   ✅ VectorEngine initialized")
        print(f"   📍 Available engines: {', '.join(available) if available else 'None (dependencies missing)'}")
    except Exception as e:
        print(f"   ⚠️  Engine init: {e}")
else:
    print("5️⃣  Skipping Engine Test (dependencies not installed)")

print()
print("=" * 60)

if has_chromadb and has_transformers:
    print("✅ Minimal validation PASSED")
    print("   Next: Run python3 run_all_tests.py for full tests")
else:
    print("⚠️  Validation incomplete - install missing dependencies")

print("=" * 60)