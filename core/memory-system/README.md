# memory-system

> Resilient 4-layer hierarchical memory for autonomous agents. Production-ready. Works offline.

[![Tests](https://img.shields.io/badge/tests-57%2F57-brightgreen)]() [![Python](https://img.shields.io/badge/python-3.9%2B-blue)]() [![License](https://img.shields.io/badge/license-MIT-green)]()

## The Problem

Autonomous agents lose all context between sessions. They re-learn the same facts, forget user preferences, can't connect related knowledge. Every restart is amnesia.

## The Solution

A 4-layer memory system that persists across sessions, decays stale knowledge, boosts accessed memories, and searches with semantic + keyword + recency scoring — all without blocking the agent.

```python
from memory_system.scripts import MemoryManager

mm = MemoryManager()
mm.store("User prefers XAUUSD scalping H1+M5", importance=0.9, tags=["trading"])
mm.store("Risk limit 2% per trade", importance=0.85, tags=["trading", "risk"])
mm.set_working("active_symbol", "XAUUSD")

results = mm.search("trading risk management", top_k=5)
# → [{"text": "Risk limit 2% per trade", "score": 0.89, ...}, ...]

stats = mm.health_check()
# → {"status": "healthy", "issues": [], "fixes": []}
```

## Layers

| Layer | Storage | Latency | Use |
|-------|---------|---------|-----|
| Working | in-process dict | <1ms | Active state, session context |
| Episodic | SQLite + HNSW | <10ms | Conversation history |
| Semantic | SQLite FTS5 | <50ms | Facts, preferences, knowledge |
| Archive | gzipped JSONL | cold | Historical, expired memories |

## Features

- **Non-blocking**: all embedding is async background, store returns in ~2ms
- **Hybrid search**: 60% semantic + 20% recency + 10% importance + 10% BM25
- **Memory graph**: multi-hop traversal (A→B→C chains)
- **Decay + boost**: importance decays 5%/day, accessing memory boosts it
- **Self-healing**: `health_check()` audits and auto-repairs broken state
- **Compaction**: clusters similar memories (cosine > 0.9) into summaries
- **Local-only mode**: 100% offline with `BAAI/bge-small-en-v1.5`
- **Graceful degradation**: embeddings fail → FTS5 keyword search

## Installation

```bash
pip install hnswlib rank-bm25 networkx numpy sentence-transformers

# Optional: set OpenAI key for API embeddings
export OPENAI_API_KEY=sk-...
```

## Quick Start

```python
import sys
sys.path.insert(0, "/path/to/skills/1ai-skills/core")

from memory_system.scripts import MemoryManager

mm = MemoryManager()

# Store knowledge (non-blocking)
mm.store("Gold price correlates inversely with USD strength",
         importance=0.8, tags=["trading", "macro"])

# Working memory (in-process, TTL)
mm.set_working("current_analysis", {"symbol": "XAUUSD", "bias": "bullish"}, ttl=3600)

# Conversation episodes (auto-summarized)
mm.add_message("user", "What's the XAUUSD setup today?")
mm.add_message("assistant", "Bullish breakout above 2950, targeting 2975")

# Search (always returns results, even offline)
results = mm.search("gold trading strategy", top_k=5)

# Link related memories (graph)
mm.link(id_a, id_b, edge_type="related_topic")
neighbors = mm.traverse(id_a, max_hops=2)

# Maintenance (run daily)
mm.decay_all()
report = mm.health_check()
stats = mm.get_stats()
```

## API Reference

See [SKILL.md](SKILL.md) for complete API docs.

## Architecture

See [references/architecture.md](references/architecture.md) for full design documentation.

## Test Results

```
RESULTS: 57/57 passed | 0 failed | 18.7s

✅ Working memory set/get, TTL, LRU eviction
✅ Semantic FTS5 search
✅ Episodic episodes + keyword search
✅ Archive gzipped JSONL
✅ Async pipeline (20 stores in 0.05s)
✅ Hybrid search ranked results
✅ Embedding fallback (local_only mode)
✅ Memory graph multi-hop traversal
✅ Decay (0.479 actual vs 0.479 expected)
✅ Health check & self-healing
✅ Stats API
✅ Compaction (4 clusters → 4 new memories)
```

## Structure

```
memory-system/
├── SKILL.md               # OpenClaw agent skill docs
├── README.md              # This file
├── scripts/
│   ├── __init__.py        # exports MemoryManager
│   ├── config.py          # all tuneable constants
│   ├── memory_manager.py  # unified API (start here)
│   ├── working_memory.py
│   ├── episodic_memory.py
│   ├── semantic_memory.py
│   ├── archive_memory.py
│   ├── embedding_engine.py
│   ├── ingestion_pipeline.py
│   ├── hybrid_search.py
│   ├── memory_graph.py
│   └── test_memory.py
└── references/
    └── architecture.md    # full design doc
```

## License

MIT
