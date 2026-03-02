# Vector DB Plugin - Video Tutorial Script

## 🎬 Tutorial Video Outline

### Episode 1: Introduction (2 min)
- What is Vector DB?
- Why semantic search vs keyword search?
- Overview of 3 engines (ZVec, PageIndex, Ruvector)

### Episode 2: Installation (3 min)
```bash
# 1. Install dependencies
pip install chromadb sentence-transformers

# 2. Verify installation
cd ~/.openclaw/workspace
python3 check_status.py

# 3. Auto-load
exec(open('vector_db_startup.py').read())
```

### Episode 3: Basic Search (5 min)
```python
# Simple search
results = vector_search("cara optimasi iklan", top_k=3)

for r in results:
    print(f"{r['score']:.3f}: {r['content']}")
```

### Episode 4: Advanced Features (5 min)
- Language detection
- Smart chunking
- Multi-engine routing
- Hybrid search with qmd

### Episode 5: Integration Examples (5 min)
- Content generator integration
- Market research integration
- Trading analysis integration

## 📹 Recording Notes

**Screen Recording Tools:**
- OBS Studio (free)
- SimpleScreenRecorder (Linux)

**Demo Commands:**
```python
# Show database status
vector_status()

# Show search results
vector_search("trading", top_k=3)

# Show chunking
vector_chunk("long text...", max_tokens=100)
```

## 🎯 Key Learning Points

1. **Semantic > Keyword**: Understanding meaning, not just matching words
2. **Auto-language**: ID → Ruvector, EN → ZVec
3. **Heartbeat sync**: Auto-index every 30 min
4. **Global tool**: Available in all sessions

## 📎 Resources

- GitHub: https://github.com/oyi77/1ai-skills
- Docs: PROJECT_DOCUMENTATION.md
- API: scripts/vector_db_api.py