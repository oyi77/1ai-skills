# 🚀 Vector DB Plugin - Deployment Guide

## ✅ Status: Ready for Deployment

All fixes applied and tested. Plugin is ready to use.

---

## 📦 What's Included

### Engines (3)
- **ZVec** (Alibaba-style): ChromaDB + BGE-M3
- **PageIndex** (VectifyAI-style): Hierarchical chunking + page tracking
- **Ruvector** (Multilingual): Indonesian + English support

### Tools (9+)
- `memory_search` - Semantic search across all engines
- `index_document` - Index content
- `semantic_similarity` - Compare texts
- `smart_chunk` - Intelligent text chunking
- `zvec_search`, `pageindex_search`, `ruvector_search` - Engine-specific
- `pageindex_index_pdf` - PDF indexing
- `ruvector_search_indonesian` - Indonesian content search

---

## 🛠️ Installation

### Step 1: Install Dependencies
```bash
pip install chromadb sentence-transformers numpy tiktoken PyPDF2
```

### Step 2: Verify Installation
```bash
cd ~/.openclaw/workspace/plugins/vector-db
python3 run_all_tests.py
```

### Step 3: Deploy to OpenClaw
```bash
# Copy plugin to OpenClaw plugins directory
mkdir -p ~/.openclaw/plugins
cp -r ~/.openclaw/workspace/plugins/vector-db ~/.openclaw/plugins/

# Restart OpenClaw
openclaw restart
```

---

## 🧪 Testing

### Quick Test
```bash
python3 test.py
```

### Comprehensive Test
```bash
python3 run_all_tests.py
```

### Manual Engine Tests
```bash
python3 zvec/engine.py
python3 pageindex/engine.py
python3 ruvector/engine.py
python3 shared/engine.py
```

---

## 📖 Usage Examples

### Example 1: Search Memory
```python
from plugins.vector_db.shared.engine import memory_search

results = memory_search(
    query="strategi trading Asia",
    max_results=5,
    min_score=0.7
)

for item in results:
    print(f"{item['score']:.3f}: {item['content'][:100]}")
```

### Example 2: Index Document
```python
from plugins.vector_db.shared.engine import index_document

doc_id = index_document(
    content="Your long document here...",
    title="Dokumen Strategi",
    source="internal"
)
print(f"Indexed: {doc_id}")
```

### Example 3: Smart Chunking
```python
from plugins.vector_db.shared.engine import smart_chunk

text = "# Section 1\n\nContent...\n\n# Section 2\n\nMore content..."
chunks = smart_chunk(text, max_tokens=500)
print(f"Created {len(chunks)} chunks")
```

### Example 4: Search Indonesian Content
```python
from plugins.vector_db.ruvector.handler import handler

results = handler({
    'action': 'search_indonesian',
    'query': 'cara optimasi iklan',
    'top_k': 3
})

for item in results['results']:
    print(f"[{item['language']}] {item['content'][:80]}...")
```

---

## 🔧 Troubleshooting

### Problem: ChromaDB Error
```
ValueError: You are using a deprecated configuration of Chroma.
```
**Solution:** Plugin code already updated. Just upgrade ChromaDB:
```bash
pip install 'chromadb>=0.4.0' --upgrade
```

### Problem: Module Not Found
```
No module named 'zvec'
```
**Solution:** Run from plugin directory or use full imports with `plugins.vector_db` prefix.

### Problem: Model Download
```
OSError: Model not found
```
**Solution:** First run will download models (~100-400MB). Ensure internet connection.

---

## 📊 Performance

| Engine | Speed | Memory | Best For |
|--------|-------|--------|----------|
| ZVec | ⚡ Fast | 💾 Low | Similarity search |
| PageIndex | 🚀 Medium | 💾 Medium | Long documents |
| Ruvector | 🌍 Multi | 💾 Medium | Multilingual |

---

## 🎯 Integration

Plugin automatically integrates with:
- ✅ OpenClaw tool calling
- ✅ Memory search hooks
- ✅ Cross-provider fallbacks
- ✅ Elevated execution mode

---

## 📁 File Structure

```
plugins/vector-db/
├── manifest.json              ✅ Plugin config
├── __init__.py               ✅ Initialization
├── README.md                 ✅ Documentation
├── FIXES_APPLIED.md        ✅ Change log
├── DEPLOY.md               ✅ This file
├── install.sh              ✅ Install script
├── test.py                 ✅ Quick test
├── run_all_tests.py        ✅ Full test suite
├── validate.py             ✅ Validator
├── examples_id.py          ✅ Indonesian examples
│
├── shared/
│   └── engine.py            ✅ Unified engine
│
├── zvec/
│   ├── engine.py            ✅ ZVec implementation (fixed)
│   └── handler.py           ✅ OpenClaw handler
│
├── pageindex/
│   ├── engine.py            ✅ PageIndex (fixed)
│   └── handler.py           ✅ OpenClaw handler
│
└── ruvector/
    ├── engine.py            ✅ Ruvector (fixed)
    └── handler.py           ✅ OpenClaw handler
```

---

## ✅ Verification Checklist

- [ ] Dependencies installed
- [ ] `run_all_tests.py` passes
- [ ] Plugin copied to `~/.openclaw/plugins/`
- [ ] OpenClaw restarted
- [ ] Test via OpenClaw commands works

---

## 🎉 Ready to Use!

Plugin is fully functional and ready for production use.

**Questions?** Check `README.md` or `FIXES_APPLIED.md` for details.

---

**Last Updated:** 2026-03-02
**Version:** 1.0.0
**Status:** ✅ Production Ready