"""
config.py — Central configuration for the memory system.
All tuneable constants live here; override via environment variables.
"""

import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(os.getenv("MEMORY_BASE_DIR", Path(__file__).parent / "data"))
DB_PATH = BASE_DIR / "memory.db"
ARCHIVE_DIR = BASE_DIR / "archive"
HNSW_INDEX_PATH = BASE_DIR / "hnsw_index.bin"
HNSW_LABELS_PATH = BASE_DIR / "hnsw_labels.npy"

# ── Embedding ──────────────────────────────────────────────────────────────
EMBED_DIM = int(
    os.getenv("EMBED_DIM", "384")
)  # bge-small = 384, text-embedding-3-small = 1536
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
LOCAL_EMBED_MODEL = os.getenv("LOCAL_EMBED_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "32"))
EMBED_TIMEOUT = float(os.getenv("EMBED_TIMEOUT", "10.0"))  # seconds

# ── Embedding cache ────────────────────────────────────────────────────────
EMBED_CACHE_TTL_DAYS = int(os.getenv("EMBED_CACHE_TTL_DAYS", "30"))

# ── Working memory ─────────────────────────────────────────────────────────
WORKING_MAX_ITEMS = int(os.getenv("WORKING_MAX_ITEMS", "1000"))
WORKING_DEFAULT_TTL = int(os.getenv("WORKING_DEFAULT_TTL", "3600"))  # seconds

# ── Episodic memory ────────────────────────────────────────────────────────
EPISODIC_MAX_ITEMS = int(os.getenv("EPISODIC_MAX_ITEMS", "10000"))
EPISODIC_SUMMARY_EVERY = int(os.getenv("EPISODIC_SUMMARY_EVERY", "15"))  # messages

# ── Semantic memory ────────────────────────────────────────────────────────
SEMANTIC_MAX_ITEMS = int(os.getenv("SEMANTIC_MAX_ITEMS", "50000"))

# ── Decay ──────────────────────────────────────────────────────────────────
DECAY_RATE = float(os.getenv("DECAY_RATE", "0.95"))  # per day
DECAY_ACCESS_BOOST = float(os.getenv("DECAY_ACCESS_BOOST", "0.1"))
DECAY_LOW_IMPORTANCE = float(
    os.getenv("DECAY_LOW_IMPORTANCE", "0.1")
)  # archive threshold
DECAY_ARCHIVE_AFTER_DAYS = int(os.getenv("DECAY_ARCHIVE_AFTER_DAYS", "30"))

# ── Hybrid search weights ──────────────────────────────────────────────────
WEIGHT_SEMANTIC = float(os.getenv("WEIGHT_SEMANTIC", "0.6"))
WEIGHT_RECENCY = float(os.getenv("WEIGHT_RECENCY", "0.2"))
WEIGHT_IMPORTANCE = float(os.getenv("WEIGHT_IMPORTANCE", "0.1"))
WEIGHT_BM25 = float(os.getenv("WEIGHT_BM25", "0.1"))
RECENCY_HALF_LIFE_DAYS = float(os.getenv("RECENCY_HALF_LIFE_DAYS", "30.0"))

# ── Compaction ─────────────────────────────────────────────────────────────
COMPACT_SIMILARITY_THRESHOLD = float(os.getenv("COMPACT_SIMILARITY_THRESHOLD", "0.9"))
COMPACT_MIN_CLUSTER_SIZE = int(os.getenv("COMPACT_MIN_CLUSTER_SIZE", "3"))

# ── HNSW ───────────────────────────────────────────────────────────────────
HNSW_M = int(os.getenv("HNSW_M", "16"))
HNSW_EF_CONSTRUCTION = int(os.getenv("HNSW_EF_CONSTRUCTION", "200"))
HNSW_EF_SEARCH = int(os.getenv("HNSW_EF_SEARCH", "50"))

# ── Worker ─────────────────────────────────────────────────────────────────
WORKER_POLL_INTERVAL = float(os.getenv("WORKER_POLL_INTERVAL", "0.5"))  # seconds
WORKER_RETRY_BASE = float(os.getenv("WORKER_RETRY_BASE", "1.0"))
WORKER_RETRY_MAX = float(os.getenv("WORKER_RETRY_MAX", "8.0"))
WORKER_MAX_RETRIES = int(os.getenv("WORKER_MAX_RETRIES", "4"))

# ── Memory graph ───────────────────────────────────────────────────────────
GRAPH_MAX_HOPS = int(os.getenv("GRAPH_MAX_HOPS", "3"))

# Ensure dirs exist
BASE_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
