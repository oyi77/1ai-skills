# Memory System — Architecture Reference

## Overview

A production-grade, self-healing hierarchical memory system for autonomous agents. Designed for agents that wake fresh each session but need persistent, searchable knowledge.

---

## 4-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  AGENT                                                  │
│  mm.store() / mm.search() / mm.set_working()            │
└───────────────────┬─────────────────────────────────────┘
                    │  MemoryManager (unified interface)
    ┌───────────────┼───────────────────┐
    │               │                   │
    ▼               ▼                   ▼
┌──────────┐  ┌──────────┐  ┌─────────────────────┐
│ WORKING  │  │ EPISODIC │  │     SEMANTIC         │
│          │  │          │  │                      │
│ dict+LRU │  │ SQLite + │  │ SQLite FTS5 +        │
│ TTL/1000 │  │ HNSW ANN │  │ embedding_blob +     │
│ <1ms     │  │ <10ms    │  │ importance/decay     │
│ No embed │  │ summaries│  │ <50ms                │
└──────────┘  └──────────┘  └─────────────────────┘
                                        │
                              auto-archive when
                              importance < 0.1
                                        │
                                        ▼
                              ┌─────────────────┐
                              │    ARCHIVE       │
                              │ gzipped JSONL   │
                              │ one file/day    │
                              │ cold storage    │
                              └─────────────────┘
```

---

## Async Ingestion Pipeline

```
agent thread                background worker thread
──────────────────          ──────────────────────────
mm.store(text)              poll ingest_queue every 0.5s
    │                           │
    ▼                           ▼
SQLite ingest_queue     batch up to 32 texts
(WAL mode, dedup)           │
    │                       ▼
    │               embed_fn([text1, text2, ...])
    │                       │ (local or API)
    │                       ▼
    │               store embeddings in DB
    │               update HNSW index
    │
returns memory_id   (NEVER blocks)
immediately
```

Key properties:
- SHA256 deduplication: same text never embedded twice
- Exponential backoff: 1s → 2s → 4s → 8s (max 4 retries)
- HTTP 429 → immediate switch to local model
- Worker is a daemon thread (auto-exits with process)

---

## Embedding System

```
embed(text)
    │
    ├─ Check embed_cache (SQLite, 30d TTL)
    │       hit → return cached vector
    │
    └─ Cache miss
            │
            ├─ mode=api_only OR (mode=hybrid AND key present)
            │       → POST /v1/embeddings (OpenAI-compatible)
            │       → 429? → flip to local, set cooldown=60s
            │       → success → return + cache
            │
            └─ mode=local_only OR API failed
                    → SentenceTransformer('BAAI/bge-small-en-v1.5')
                    → ~130MB, 384-dim, ~50ms first, ~2ms cached
                    → failure → None (search degrades to FTS5)
```

---

## Hybrid Search Formula

```
score = 0.6 × semantic_similarity
      + 0.2 × recency_score
      + 0.1 × importance
      + 0.1 × bm25_score

where:
  semantic_similarity = cosine(query_vec, memory_vec)
                        [batch numpy, no loop]
  recency_score       = exp(-age_days / 30)
                        [1.0 at now, ~0.5 at 30 days]
  importance          = stored float, 0–1, decays + boosts
  bm25_score          = BM25Okapi normalised to [0,1]

Degraded mode (no embeddings):
  weight_semantic = 0, weight_bm25 += 0.6
  → pure BM25+recency+importance, still useful
```

---

## Memory Decay System

```python
# On every decay_all() call (recommended: daily)
for each memory:
    days = (now - last_accessed) / 86400
    importance = importance × (0.95 ^ days)   # 5%/day
    # 0.95^10 ≈ 0.60, 0.95^30 ≈ 0.21, 0.95^60 ≈ 0.05

# On every get() or search() hit:
    importance = min(1.0, importance + 0.1)
    last_accessed = now

# Auto-archive condition:
    if importance < 0.1 AND last_accessed < 30 days ago:
        mark archived=1
        write to gzipped JSONL
```

---

## Memory Graph

```
memory_edges table:
  (from_id, to_id, edge_type, weight, created_at)
  PRIMARY KEY: (from_id, to_id, edge_type)

networkx DiGraph: in-memory mirror, rebuilt from DB on init

Edge types:
  refers_to     — A directly references B
  related_topic — thematically connected
  learned_from  — A was derived from B
  contradicts   — A contradicts B

Multi-hop BFS traversal:
  traverse(start, max_hops=3, edge_types=["refers_to"])
  → BFS from start, filters by edge_type
  → returns [{memory_id, hop_distance, path, weight}, ...]
  → enriched with text/importance from DB
```

---

## Self-Healing

`health_check()` performs these repairs automatically:

1. **Missing embeddings** → scan for `embedding_blob IS NULL` → re-queue to ingest pipeline
2. **HNSW vs DB count drift** → if |hnsw_count - db_count| > 5% → rebuild index from DB
3. **Stuck ingest jobs** → `pending` AND `created_at < 10 minutes ago` → reset retry timer
4. **Schema corruption** → re-run `_init_schema()` which uses `CREATE TABLE IF NOT EXISTS`

Returns: `{status, issues: [...], fixes: [...]}` for observability.

---

## Compaction Algorithm

```
1. Load all semantic memories with embeddings
2. Build embedding matrix (N × dim)
3. Normalise rows → unit vectors
4. Compute cosine similarity matrix: M @ M.T
5. Greedy clustering:
   - For each unvisited memory i:
     - Find all j where sim[i,j] >= threshold (default: 0.9)
     - If cluster size >= 3: record cluster
6. For each cluster:
   - Extract unique sentences from all texts
   - Join → merged summary (cap 1500 chars)
   - Store as new memory (avg importance + 0.1)
   - Archive originals (mark archived=1 + write JSONL)
   - Link originals → new via refers_to edge
```

---

## Thread Safety

- `WorkingMemory`: `threading.RLock` on all mutations
- `SemanticMemory`: `threading.RLock` for writes, SQLite WAL for reads
- `EpisodicMemory`: `threading.RLock` for HNSW writes
- `EmbeddingEngine`: `threading.Lock` for local model lazy load
- `IngestionPipeline`: dedicated daemon thread, SQLite WAL queue
- `MemoryGraph`: `threading.RLock` for networkx mutations

Multiple agents can call `mm.store()` / `mm.search()` concurrently safely.

---

## SQLite Schema Summary

```sql
-- Semantic memories
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    text TEXT,
    embedding_blob BLOB,      -- float32 bytes
    timestamp REAL,
    last_accessed REAL,
    importance REAL,
    tags TEXT,                -- JSON array
    entity_refs TEXT,         -- JSON array
    source TEXT,
    archived INTEGER
);
CREATE VIRTUAL TABLE memories_fts USING fts5(...);  -- BM25

-- Episodic memories
CREATE TABLE episodes (
    id TEXT PRIMARY KEY,
    summary TEXT,
    raw_messages TEXT,        -- JSON
    embedding_blob BLOB,
    timestamp REAL,
    last_accessed REAL,
    importance REAL,
    message_count INTEGER,
    archived INTEGER
);

-- Embedding cache
CREATE TABLE embed_cache (
    hash TEXT PRIMARY KEY,    -- SHA256 of text
    embedding_bytes BLOB,
    created_at REAL
);

-- Async ingest queue (SQLite WAL as queue)
CREATE TABLE ingest_queue (
    id TEXT PRIMARY KEY,
    memory_id TEXT,
    text TEXT,
    text_hash TEXT,           -- SHA256 dedup
    memory_type TEXT,         -- semantic | episodic
    status TEXT,              -- pending | done | failed
    retries INTEGER,
    priority INTEGER,
    created_at REAL,
    next_try_at REAL,
    error TEXT
);

-- Memory graph
CREATE TABLE memory_edges (
    from_id TEXT,
    to_id TEXT,
    edge_type TEXT,
    weight REAL,
    created_at REAL,
    PRIMARY KEY (from_id, to_id, edge_type)
);
```

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Working memory op | ~1µs | In-process dict |
| Semantic FTS search | ~2ms | SQLite FTS5 BM25 |
| Hybrid search (100 mems) | ~45ms | numpy batch cosine |
| Store (non-blocking) | ~2.5ms | SQLite insert + queue |
| Local embed (batch 32) | ~600ms | bge-small, first batch |
| Local embed (cached) | ~0.1ms | SQLite cache hit |
| HNSW ANN search (10k) | ~2ms | hnswlib |
| health_check | ~50ms | full audit |

---

## Dependency Matrix

| Package | Required | Purpose |
|---------|----------|---------|
| numpy | ✅ | Embedding math |
| sentence-transformers | ✅ | Local embeddings |
| hnswlib | ✅ | ANN vector search |
| rank-bm25 | ✅ | BM25 keyword scoring |
| networkx | ✅ | In-memory graph |
| sqlite3 | ✅ | Built-in Python |
| faiss-cpu | ❌ optional | Alternative ANN (not used) |
| redis | ❌ optional | Distributed working memory |
