# Hybrid Memory Integration
## Vector DB + qmd Collaboration

### 🎯 Tujuan
**Kolaborasi** antara:
- **Vector DB**: Semantic understanding (makna, konteks)
- **qmd**: Keyword matching (exact match, recall)
- **Hybrid**: Terbaik dari kedua dunia

### 🤝 Cara Kerja Kolaborasi

```
User Query
    ↓
HybridMemoryProvider.search()
    ↓
├── Vector DB (Semantic)
│   ├── Detect language (ID/EN)
│   ├── Choose engine (Ruvector/ZVec)
│   └── Semantic similarity search
│       └── Results with scores 0.4-0.8
│
├── qmd (Keyword - Optional)
│   └── Exact keyword matching
│       └── Results with score 0.5
│
└── Merge & Deduplicate
    ├── Boost score if found in both
    ├── Sort by relevance
    └── Return top results
```

### 📊 Perbandingan

| Aspek | Vector DB | qmd | Hybrid |
|-------|-----------|-----|--------|
| **Pencarian** | Semantic | Keyword | Both |
| **Bahasa** | Multi-language aware | Single | Auto-detect |
| **Relevansi** | Context-aware | Exact match | Combined |
| **Recall** | High | Very High | Very High |
| **Precision** | High | Medium | Very High |

### 💡 Contoh

**Query**: "cara optimasi iklan"

**Vector DB** | **qmd** | **Hybrid**
---|---|---
Hasil konten mirip makna | Hasil exact keyword | **Keduanya** + duplikat removed
Score: 0.78 | Score: 0.50 | **Score boosted**: 0.85

### 🔄 Alur Data

1. **Heartbeat** sync memory files → Vector DB
2. **qmd** tetap scan file system (bawaan OpenClaw)
3. **User query** → Hybrid search
4. **Hasil** → Merge → Return

### 🎉 Keuntungan

- ✅ **Semantic**: Mengerti makna, bukan cuma keyword
- ✅ **Exact**: Tetap bisa exact match
- ✅ **Language**: Auto-detect ID/EN
- ✅ **Fallback**: qmd sebagai backup
- ✅ **Boost**: Score lebih tinggi kalau found di both

### 🚀 Usage

```python
# Automatic hybrid search
results = memory_search("cara optimasi iklan")

# Results from both Vector DB + qmd
for r in results:
    print(f"{r['score']:.3f}: {r['content']}")
    print(f"Engine: {r['engine']}")
```

### ✅ Status: FULLY INTEGRATED

| Komponen | Status |
|----------|--------|
| Vector DB | ✅ Active |
| qmd | ✅ Fallback |
| Hybrid Merge | ✅ Working |
| Auto Language | ✅ Working |
| Heartbeat Sync | ✅ Configured |

**Integration: COMPLETE** 🎉