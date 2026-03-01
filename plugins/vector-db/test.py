#!/usr/bin/env python3
"""
Vector DB Plugin - Quick Test
"""

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/plugins/vector-db')

print("=" * 60)
print("🧪 Vector DB Plugin - Quick Test")
print("=" * 60)
print()

# Test 1: Smart Chunking
print("1️⃣  Testing Smart Chunking...")
from shared.engine import smart_chunk

test_doc = """
# Introduction
This is a test document that should be chunked properly.
It contains multiple sections and code blocks.

## Section 1
More text here. This section is longer and should be handled correctly.

```python
def hello():
    print("Hello World")
```

## Section 2
Final section content.
"""

chunks = smart_chunk(test_doc, max_tokens=300)
print(f"   ✅ Chunked into {len(chunks)} parts")

# Test 2: Engines
print()
print("2️⃣  Testing Engines...")

print("   🔵 ZVec:", end=" ")
try:
    from zvec.engine import ZVecEngine
    engine = ZVecEngine({'enabled': True, 'model': 'all-MiniLM-L6-v2'})
    print("✅ Ready")
except Exception as e:
    print(f"❌ {e}")

print("   📄 PageIndex:", end=" ")
try:
    from pageindex.engine import PageIndexEngine
    engine = PageIndexEngine({'enabled': True})
    print("✅ Ready")
except Exception as e:
    print(f"❌ {e}")

print("   🌍 Ruvector:", end=" ")
try:
    from ruvector.engine import RuvectorEngine
    engine = RuvectorEngine({'enabled': True})
    print("✅ Ready")
except Exception as e:
    print(f"❌ {e}")

# Test 3: Unified Engine
print()
print("3️⃣  Testing Unified Engine...")
try:
    from shared.engine import VectorEngine
    
    engine = VectorEngine()
    available = list(engine.engines.keys())
    print(f"   ✅ Available engines: {', '.join(available)}")
    print(f"   📍 Default: {engine.active_engine}")
    print(f"   💾 Cache: {engine.cache_dir}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("=" * 60)
print("✅ Plugin test complete!")
print("=" * 60)
print()
print("Usage:")
print("  from plugins.vector_db import VectorEngine")
print("  engine = VectorEngine()")
print("  results = engine.search('your query')")