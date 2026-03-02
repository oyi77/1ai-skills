# 🚀 QUICKSTART - Vector DB Plugin

## Install & Run in 3 Steps

### Step 1: Install Dependencies
```bash
pip install chromadb sentence-transformers numpy tiktoken PyPDF2
```

### Step 2: Run Test
```bash
cd ~/.openclaw/workspace/plugins/vector-db
python3 WORKING_TEST.py
```

### Step 3: Deploy
```bash
bash DEPLOY.sh
```

---

## Files for Different Needs

| File | Use Case |
|------|----------|
| `WORKING_TEST.py` | Full test with model download |
| `minimal_test.py` | Fast check tanpa download |
| `DEPLOY.sh` | One-click deploy |
| `run_all_tests.py` | Comprehensive test suite |
| `FIX_COMPLETE.md` | Detail semua fix |

---

## Perintah Super Cepat (Copy-Paste)

```bash
# Install + Test + Deploy sekaligus
pip install chromadb sentence-transformers numpy tiktoken PyPDF2 && cd ~/.openclaw/workspace/plugins/vector-db && python3 WORKING_TEST.py && bash DEPLOY.sh
```

---

## Gunakan di OpenClaw

```python
from plugins.vector_db import VectorEngine

engine = VectorEngine()
results = engine.search("cari info", top_k=5)
```

---

Done! 🎉