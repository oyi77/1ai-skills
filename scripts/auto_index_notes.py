#!/usr/bin/env python3
"""
Index recent notes to vector DB
"""
import sys
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

from pathlib import Path
from tools.vector_db_tools import vector_index, vector_search

notes_dir = Path("notes")
memory_dir = Path("memory")

print("📝 Indexing recent notes to Vector DB...\n")

# Index browser gotchas note
browser_note = notes_dir / "browser-tool-critical-gotchas.md"
if browser_note.exists():
    with open(browser_note) as f:
        content = f.read()
    doc_id = vector_index(
        content,
        title="Browser Tool Critical Gotchas",
        source=str(browser_note)
    print(f"✅ Indexed: {browser_note.name}")
    print(f"   ID: {doc_id}")

# Index INDEX.md for reference
index_file = memory_dir / "INDEX.md"
if index_file.exists():
    with open(index_file) as f:
        content = f.read()
    doc_id = vector_index(
        content,
        title="Memory Index - Quick Reference",
        source=str(index_file)
    print(f"\n✅ Indexed: {index_file.name}")
    print(f"   ID: {doc_id}")

print("\n✅ Indexing complete. Now searching for 'browser tool'...")

results = vector_search("browser tool tab management", top_k=3)

print(f"\n✅ Found {len(results)} results:\n")
for i, r in enumerate(results, 1):
    print(f"{i}. Score: {r['score']:.2f}")
    print(f"   Source: {r['source']}")
    print(f"   {r.title}")
    print(f"   Content: {r['content'][:100]}...")
    print()