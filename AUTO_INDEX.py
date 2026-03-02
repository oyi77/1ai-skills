#!/usr/bin/env python3
"""
Vector DB Auto-Indexer + Setup
Indexes existing documents from workspace
"""

import sys
import os

# Setup paths
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

print("=" * 60)
print("🔧 Vector DB Auto-Indexer")
print("=" * 60)
print()

# Import plugin
from vector_db import VectorEngine, smart_chunk

engine = VectorEngine()
print(f"✅ Engine initialized: {list(engine.engines.keys())}")
print()

# Index 1: MEMORY.md
print("📄 Indexing MEMORY.md...")
try:
    with open('/home/openclaw/.openclaw/workspace/MEMORY.md', 'r') as f:
        memory_content = f.read()
    
    doc_id = engine.index_document(
        memory_content,
        title="BerkahKarya Strategic Intelligence",
        source="MEMORY.md"
    )
    print(f"   ✅ Indexed: {doc_id[:20]}...")
except Exception as e:
    print(f"   ⚠️  Error: {e}")

print()

# Index 2: Daily memory files
print("📄 Indexing daily memory files...")
memory_dir = '/home/openclaw/.openclaw/workspace/memory'
if os.path.exists(memory_dir):
    files = [f for f in os.listdir(memory_dir) if f.endswith('.md')]
    print(f"   Found {len(files)} files")
    
    for i, filename in enumerate(files[:5]):  # Index first 5
        try:
            with open(os.path.join(memory_dir, filename), 'r') as f:
                content = f.read()
            
            doc_id = engine.index_document(
                content,
                title=f"Memory: {filename}",
                source=f"memory/{filename}"
            )
            print(f"   ✅ {filename}")
        except Exception as e:
            print(f"   ⚠️  {filename}: {e}")

print()

# Index 3: SOUL.md
print("📄 Indexing SOUL.md...")
try:
    with open('/home/openclaw/.openclaw/workspace/SOUL.md', 'r') as f:
        soul_content = f.read()
    
    doc_id = engine.index_document(
        soul_content,
        title="Vilona Soul Configuration",
        source="SOUL.md"
    )
    print(f"   ✅ Indexed: {doc_id[:20]}...")
except Exception as e:
    print(f"   ⚠️  Error: {e}")

print()

# Index 4: USER.md  
print("📄 Indexing USER.md...")
try:
    with open('/home/openclaw/.openclaw/workspace/USER.md', 'r') as f:
        user_content = f.read()
    
    doc_id = engine.index_document(
        user_content,
        title="User Profile - BerkahKarya",
        source="USER.md"
    )
    print(f"   ✅ Indexed: {doc_id[:20]}...")
except Exception as e:
    print(f"   ⚠️  Error: {e}")

print()
print("=" * 60)
print("✅ Indexing Complete!")
print("=" * 60)
print()
print("Total documents indexed in Vector DB")
print("Ready for semantic search queries.")