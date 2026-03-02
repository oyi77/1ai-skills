# Vector DB Plugin - Quick Reference

## 🚀 Start Here

```python
# 1. Load tools (auto via SOUL.md or manual)
exec(open('/home/openclaw/.openclaw/workspace/vector_db_startup.py').read())

# 2. Search
results = vector_search("cara optimasi", top_k=3)

# 3. Use results
for r in results:
    print(f"{r['score']:.3f}: {r['content'][:100]}")
```

## 📚 Full Documentation

- [PROJECT_INDEX.md](PROJECT_INDEX.md) - Navigation hub
- [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) - Complete docs
- [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt) - One-page summary
- [VIDEO_TUTORIAL.md](VIDEO_TUTORIAL.md) - Video guide

## 🔧 API Reference

| Function | Parameters | Returns |
|----------|-----------|---------|
| `vector_search` | query, top_k=5 | List[dict] |
| `vector_index` | content, title, source | str (doc_id) |
| `vector_chunk` | text, max_tokens=500 | List[str] |
| `vector_detect_language` | text | 'id'/'en'/'mixed' |
| `vector_status` | - | dict |

## 🌐 Web Dashboard

Open in browser:
```
file:///home/openclaw/.openclaw/workspace/dashboard/index.html
```

Or serve via API:
```bash
python3 scripts/vector_db_api.py
# Then visit http://localhost:8765
```

## 📊 Stats

- **Documents**: 116 indexed
- **Engines**: 3 active
- **Storage**: ~16MB
- **Avg Search**: 0.3s

## 🔗 Links

- Project: https://github.com/oyi77/1ai-skills
- Status: PRODUCTION READY ✅
- Version: 1.0.0