

---

## 🔄 Session Startup (Auto-Load)

**Run at the start of every session:**

```python
# Auto-load Vector DB Tools
exec(open('/home/openclaw/.openclaw/workspace/vector_db_startup.py').read())
```

**This loads:**
- `vector_search(query, top_k=5)` - Semantic document search
- `vector_index(content, title, source)` - Index new documents
- `vector_chunk(text, max_tokens=500)` - Smart text chunking
- `vector_detect_language(text)` - Auto ID/EN detection
- `vector_status()` - Check Vector DB status

**Usage:**
```python
results = vector_search("cara optimasi iklan", top_k=3)
for r in results:
    print(f"{r['score']:.3f}: {r['content'][:100]}")
```

---
