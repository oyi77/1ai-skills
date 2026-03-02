#!/usr/bin/env python3
"""
Vector DB - Index All Documents in Workspace
Indexes: MEMORY.md, SOUL.md, USER.md, and all memory/*.md files
"""

import sys
import os

sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

print("=" * 70)
print("🚀 VECTOR DB - INDEXING ALL DOCUMENTS")
print("=" * 70)
print()

from vector_db import VectorEngine

engine = VectorEngine()
available = list(engine.engines.keys())
print(f"✅ Engines available: {available}")
print()

doc_count = 0
errors = []

# Function to index a file
def index_file(filepath, title, source):
    global doc_count
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 100:  # Only index if has meaningful content
                doc_id = engine.index_document(
                    content,
                    {'title': title, 'source': source}
                )
                doc_count += 1
                print(f"   ✅ {source} ({len(content):,} chars) → {doc_id[:16]}...")
                return True
    except Exception as e:
        errors.append(f"{source}: {e}")
        print(f"   ❌ {source}: {e}")
    return False

# 1. Index MEMORY.md
print("📄 Indexing MEMORY.md...")
index_file(
    '/home/openclaw/.openclaw/workspace/MEMORY.md',
    'BerkahKarya Strategic Intelligence',
    'MEMORY.md'
)

# 2. Index SOUL.md
print("📄 Indexing SOUL.md...")
index_file(
    '/home/openclaw/.openclaw/workspace/SOUL.md',
    'Vilona Soul Configuration',
    'SOUL.md'
)

# 3. Index USER.md
print("📄 Indexing USER.md...")
index_file(
    '/home/openclaw/.openclaw/workspace/USER.md',
    'User Profile - BerkahKarya',
    'USER.md'
)

# 4. Index all memory/*.md files
print("\n📄 Indexing memory files...")
memory_dir = '/home/openclaw/.openclaw/workspace/memory'
if os.path.exists(memory_dir):
    files = sorted([f for f in os.listdir(memory_dir) if f.endswith('.md')])
    print(f"   Found {len(files)} files")
    
    for filename in files:
        filepath = os.path.join(memory_dir, filename)
        index_file(
            filepath,
            f'Memory: {filename}',
            f'memory/{filename}'
        )

# 5. Index AGENTS.md
print("\n📄 Indexing AGENTS.md...")
index_file(
    '/home/openclaw/.openclaw/workspace/AGENTS.md',
    'Agent Configuration Guide',
    'AGENTS.md'
)

# 6. Index HEARTBEAT.md if exists
if os.path.exists('/home/openclaw/.openclaw/workspace/HEARTBEAT.md'):
    print("📄 Indexing HEARTBEAT.md...")
    index_file(
        '/home/openclaw/.openclaw/workspace/HEARTBEAT.md',
        'Heartbeat Configuration',
        'HEARTBEAT.md'
    )

print()
print("=" * 70)
print("📊 INDEXING COMPLETE")
print("=" * 70)
print(f"✅ Total documents indexed: {doc_count}")

if errors:
    print(f"⚠️  Errors: {len(errors)}")
    for e in errors[:5]:
        print(f"   - {e}")

print()
print("💾 Vector DB Location:")
for engine_name in available:
    cache_dir = f'/home/openclaw/.openclaw/vector-cache/{engine_name}'
    if os.path.exists(cache_dir):
        size = os.popen(f'du -sh {cache_dir} 2>/dev/null').read().strip()
        print(f"   {engine_name}: {size}")

print()
print("🔍 Ready to search! Try:")
print("   cd ~/.openclaw/workspace && python3 QUERY_VECTOR.py 'strategi trading'")
print("=" * 70)