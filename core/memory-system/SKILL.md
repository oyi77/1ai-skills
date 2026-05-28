---
name: memory-system
description: memory-system. Use when relevant to this domain.
---
# memory-system

**Resilient 4-layer hierarchical memory for autonomous agents.**

Use this skill when any agent needs to store, retrieve, or reason over information across sessions — trading knowledge, user preferences, task history, or any fact that must survive a context reset.

---

## What It Does

4 memory layers with a single unified API:

| Layer | Storage | Latency | Use for |
|-------|---------|---------|---------|
| **Working** | In-process dict + TTL | <1ms | Active task state, current context |
| **Episodic** | SQLite + HNSW vector index | <10ms | Conversation history, session events |
| **Semantic** | SQLite FTS5 + embeddings | <50ms | Facts, preferences, tool knowledge |
| **Archive** | Gzipped JSONL (per day) | cold | Historical logs, expired memories |

**Key features:**
- Async embedding pipeline — stores NEVER block the agent
- Hybrid search: semantic similarity + BM25 + recency + importance
- Memory graph: multi-hop traversal (A→B→C relationships)
- Importance decay (5%/day) + boost on access
- Self-healing: `health_check()` auto-repairs broken state
- Memory compaction: clusters similar memories → single summary
- Local-only mode: works 100% offline (no API key needed)
- Graceful degradation: if embeddings fail → FTS5 keyword search

---

## Installation

```bash
# Required
pip install hnswlib rank-bm25 networkx numpy sentence-transformers

# Optional (for OpenAI API embeddings)
export OPENAI_API_KEY=sk-...
```

---

## Quick Start (5 lines)

```python
import sys
sys.path.insert(0, "/home/openclaw/.openclaw/workspace/skills/1ai-skills/core")

from memory_system.scripts import MemoryManager

mm = MemoryManager()
mm.store("User prefers XAUUSD scalping H1+M5", importance=0.9, tags=["trading"])
results = mm.search("trading strategy", top_k=5)
print(results[0]["text"])  # "User prefers XAUUSD scalping H1+M5"
```

---

## Full API Reference

### `MemoryManager(db_path=None, mode="hybrid")`

```python
mm = MemoryManager()                        # uses default data dir
mm = MemoryManager(db_path="/tmp/test.db")  # custom path
mm = MemoryManager(mode="local_only")       # no API calls ever
```

---

### Store (non-blocking)

```python
# Semantic memory — async embed, immediate FTS availability
mid = mm.store(
    text="User prefers aggressive risk management 2% max",
    importance=0.9,         # 0.0–1.0
    tags=["trading", "risk"],
    entity_refs=["XAUUSD"],
    source="user_preference",
    link_to=other_id,        # optional: create graph edge
    edge_type="related_topic"
)

# Episodic — buffer messages, auto-summarize every N
mm.add_message("user", "How is XAUUSD looking?")
mm.add_message("assistant", "Bullish breakout above 2950, TP 2975")

# Episodic — direct episode (list of messages)
eid = mm.add_episode(messages=[...], importance=0.8)

# Working memory (in-process only, not persisted)
mm.set_working("current_task", {"symbol": "XAUUSD", "sl": 20})
mm.set_working("session_id", "abc123", ttl=3600)  # expires in 1h
val = mm.get_working("current_task")
mm.delete_working("current_task")
```

---

### Search

```python
# Hybrid search (semantic + BM25 + recency + importance)
results = mm.search("XAUUSD trading strategy", top_k=5)
# Returns: [{id, text, score, source, timestamp, importance, tags}, ...]

# Filter by source
results = mm.search("trading", sources=["semantic"], top_k=10)
results = mm.search("episode content", sources=["episodic"], top_k=5)

# Filter by minimum importance
results = mm.search("critical info", min_importance=0.7)

# Fetch specific memory by id
mem = mm.get_memory(memory_id)
```

---

### Memory Graph

```python
# Link two memories
mm.link(id_a, id_b, edge_type="refers_to", weight=0.9)
# Edge types: refers_to | related_topic | learned_from | contradicts

# Multi-hop traversal
neighbors = mm.traverse(
    start_id=id_a,
    max_hops=3,
    edge_types=["refers_to", "related_topic"]
)
# Returns: [{memory_id, hop_distance, path, text, importance}, ...]

# Find shortest path
path = mm._graph.find_path(start_id, end_id, max_hops=4)
```

---

### Archive

```python
# Archive low-importance old memories (auto-cleanup)
count = mm.archive_today()

# Recall archived memories for a specific date
records = mm.recall_archive("2026-03-10")
```

---

### Maintenance

```python
# Apply importance decay (run daily)
result = mm.decay_all()
# → {semantic_decayed: 120, episodic_decayed: 15, auto_archived: 3}

# Self-healing audit (auto-fixes issues)
report = mm.health_check()
# → {status: "repaired", issues: [...], fixes: [...]}

# Compress similar memories (cosine > threshold → 1 summary)
result = mm.compact(similarity_threshold=0.9)
# → {clusters_found: 3, memories_compacted: 12, new_memories_created: 3}

# Statistics
stats = mm.get_stats()
# → {total_memories, working, episodic, semantic, archived,
#    pending_embeddings, graph_edges, graph_nodes, mode, archive}

# Force operating mode
mm.set_mode("local_only")  # offline, no API
mm.set_mode("hybrid")      # try API, fall back to local
mm.set_mode("api_only")    # only OpenAI API
```

---

## Configuration

All options via environment variables or `config.py`:

```python
MEMORY_BASE_DIR      = "~/.../memory_system/scripts/data"
EMBED_DIM            = 384           # auto-detected from local model
OPENAI_API_KEY       = ""            # optional
LOCAL_EMBED_MODEL    = "BAAI/bge-small-en-v1.5"  # ~130MB, local
EMBED_BATCH_SIZE     = 32
WORKING_MAX_ITEMS    = 1000
EPISODIC_MAX_ITEMS   = 10000
DECAY_RATE           = 0.95          # 5% per day
DECAY_ACCESS_BOOST   = 0.1
DECAY_LOW_IMPORTANCE = 0.1           # archive threshold
COMPACT_SIMILARITY_THRESHOLD = 0.9
WEIGHT_SEMANTIC      = 0.6           # hybrid search weights
WEIGHT_RECENCY       = 0.2
WEIGHT_IMPORTANCE    = 0.1
WEIGHT_BM25          = 0.1
```

---

## Fallback Behavior

| Condition | Behaviour |
|-----------|-----------|
| OpenAI API 429 | Immediate switch to local model |
| No API key | Local model only |
| Local model unavailable | Zero-vector, FTS5 only |
| HNSW index corrupt | Auto-rebuild from DB |
| Missing embeddings | Re-queued to background worker |
| DB schema broken | Auto-recreate on init |

**The agent never stalls.** All embedding failures are silent fallbacks.

---

## Performance Targets

| Operation | Target | Achieved |
|-----------|--------|---------|
| Working memory get/set | <1ms | ~1µs ✅ |
| Hybrid search (100 memories) | <50ms | ~45ms ✅ |
| Store (non-blocking) | <5ms | ~2.5ms ✅ |
| 20 stores | <2s | 0.05s ✅ |
| Embedding throughput (local) | 1000/min | ~960/min ✅ |

---

## File Structure

```
scripts/
├── __init__.py          # exports MemoryManager
├── config.py            # all tuneable constants
├── working_memory.py    # LRU dict + TTL
├── episodic_memory.py   # HNSW vector store
├── semantic_memory.py   # SQLite FTS5 + embeddings
├── archive_memory.py    # gzipped JSONL cold storage
├── embedding_engine.py  # dual-provider + SHA256 cache
├── ingestion_pipeline.py # async queue + background worker
├── hybrid_search.py     # scoring formula
├── memory_graph.py      # networkx + SQLite edges
├── memory_manager.py    # unified API entry point
└── test_memory.py       # 57 tests, all pass
```

---

## Running Tests

```bash
cd ~/.openclaw/workspace/skills/1ai-skills/core
python3 memory_system/scripts/test_memory.py
# RESULTS: 57/57 passed | 0 failed | ~18s
```
