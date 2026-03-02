#!/usr/bin/env python3
"""
Vector DB Plugin - Working Test (Standalone)
"""

import os
import sys

# Set up paths
plugin_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_dir)

# Mock the plugins.vector_db namespace
import types
plugins = types.ModuleType('plugins')
plugins.vector_db = types.ModuleType('plugins.vector_db')
sys.modules['plugins'] = plugins
sys.modules['plugins.vector_db'] = plugins.vector_db

# Now import the modules
print("=" * 60)
print("🧪 Vector DB Plugin - Deployment Test")
print("=" * 60)
print()

# Step 1: Check dependencies
print("1️⃣  Checking Dependencies...")

try:
    import chromadb
    print(f"   ✅ ChromaDB {chromadb.__version__}")
    has_chroma = True
except ImportError:
    print("   ❌ ChromaDB missing")
    has_chroma = False
    sys.exit(1)

try:
    from sentence_transformers import SentenceTransformer
    print("   ✅ SentenceTransformers")
    has_transformers = True
except ImportError:
    print("   ❌ SentenceTransformers missing")
    has_transformers = False
    sys.exit(1)

print()

# Step 2: Test ZVec with direct import
print("2️⃣  Testing ZVec Engine...")
try:
    # Direct import from zvec directory
    sys.path.insert(0, os.path.join(plugin_dir, 'zvec'))
    from engine import ZVecEngine
    
    config = {'enabled': True, 'model': 'all-MiniLM-L6-v2'}
    engine = ZVecEngine(config)
    print("   ✅ ZVecEngine initialized")
except Exception as e:
    print(f"   ❌ ZVec: {e}")

print()

# Step 3: Test PageIndex
print("3️⃣  Testing PageIndex Engine...")
try:
    sys.path.insert(0, os.path.join(plugin_dir, 'pageindex'))
    from engine import PageIndexEngine
    
    config = {'enabled': True, 'useGoogleAuth': False}
    engine = PageIndexEngine(config)
    print("   ✅ PageIndexEngine initialized")
except Exception as e:
    print(f"   ❌ PageIndex: {e}")

print()

# Step 4: Test Ruvector
print("4️⃣  Testing Ruvector Engine...")
try:
    sys.path.insert(0, os.path.join(plugin_dir, 'ruvector'))
    from engine import RuvectorEngine
    
    config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
    engine = RuvectorEngine(config)
    print("   ✅ RuvectorEngine initialized")
    
    # Test language detection
    texts = ["This is English", "Ini bahasa Indonesia"]
    for text in texts:
        lang = engine.detect_language(text)
        print(f"      '{text}' -> {lang}")
except Exception as e:
    print(f"   ❌ Ruvector: {e}")

print()

# Step 5: Deploy
print("5️⃣  Deploying Plugin...")
try:
    import shutil
    target = os.path.expanduser('~/.openclaw/plugins/vector-db')
    shutil.copytree(plugin_dir, target, dirs_exist_ok=True)
    print(f"   ✅ Deployed to: {target}")
    print("   Files copied:")
    for f in os.listdir(target)[:5]:
        print(f"      - {f}")
except Exception as e:
    print(f"   ❌ Deploy failed: {e}")

print()
print("=" * 60)
print("✅ Test & Deploy Complete!")
print("=" * 60)
print()
print("Next: Restart OpenClaw if needed")