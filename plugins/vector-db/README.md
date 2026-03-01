# Vector DB Plugin

## Overview

Plugin OpenClaw untuk integrasi vector database (ZVec, PageIndex, Ruvector) dengan unified interface.

## Engines

### 🔵 ZVec (Alibaba-style)
- **Backend**: ChromaDB + BGE-M3 embeddings
- **Strength**: Efisien untuk similarity search
- **Best for**: General semantic search, English content

### 📄 PageIndex (VectifyAI-style)
- **Backend**: ChromaDB + Hierarchical chunking
- **Strength**: Dokumen panjang dengan page/section tracking
- **Best for**: PDFs, articles, structured documents

### 🌍 Ruvector (Multilingual)
- **Backend**: ChromaDB + SentenceTransformers
- **Strength**: Multilingual embeddings (Indonesian, English, dll)
- **Best for**: Mixed-language content, Indonesian text

## Installation

```bash
# Install dependencies
pip install chromadb sentence-transformers numpy tiktoken

# Optional for PDF support
pip install PyPDF2
```

## Configuration

File: `~/.openclaw/plugins/vector-db/manifest.json`

```json
{
  "config": {
    "defaultEngine": "zvec",
    "chunkSize": 500,
    "maxTokens": 8192,
    "cacheEnabled": true
  }
}
```

## Usage

### Via OpenClaw Commands

```
/memory_search query="cari tentang OpenClaw" max_results=5
/index_document content="..." title="My Doc"
/semantic_similarity text1="..." text2="..."
```

### Via Python

```python
from plugins.vector_db import VectorEngine, smart_chunk

# Initialize
engine = VectorEngine()

# Search
results = engine.search("query", top_k=5)

# Index
doc_id = engine.index_document("content", metadata={"title": "My Doc"})

# Smart chunking
chunks = smart_chunk(long_text, max_tokens=500)
```

## Tools

| Tool | Description |
|------|-------------|
| `memory_search` | Enhanced semantic search across all engines |
| `index_document` | Index content for future search |
| `semantic_similarity` | Compare similarity between texts |
| `smart_chunk` | Intelligent text chunking |
| `zvec_search` | Search ZVec specifically |
| `pageindex_search` | Search with page/section tracking |
| `pageindex_index_pdf` | Index PDF file |
| `ruvector_search` | Multilingual search |
| `ruvector_search_indonesian` | Search Indonesian content |

## Storage

- **Cache**: `~/.openclaw/vector-cache/`
- **ZVec**: `~/.openclaw/vector-cache/zvec/`
- **PageIndex**: `~/.openclaw/vector-cache/pageindex/`
- **Ruvector**: `~/.openclaw/vector-cache/ruvector/`

## Testing

```bash
# Test individual engines
cd ~/.openclaw/plugins/vector-db
python3 zvec/engine.py
python3 pageindex/engine.py
python3 ruvector/engine.py

# Test unified engine
python3 shared/engine.py
```

## Integration dengan OpenClaw

Plugin otomatis terintegrasi dengan:
- `memory_search` hook (enhancement)
- Tool calling interface
- Cross-provider fallbacks

## Troubleshooting

**ChromaDB not installed**
```bash
pip install chromadb
```

**SentenceTransformers error**
```bash
pip install sentence-transformers
```

**Out of disk space**
```bash
# Clean caches
rm -rf ~/.openclaw/vector-cache/*
```

## License
MIT