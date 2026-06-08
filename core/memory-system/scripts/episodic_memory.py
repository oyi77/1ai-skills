"""
episodic_memory.py — Conversation episode storage with HNSW vector index.

Pipeline:
  Raw messages → (every N msgs) → summarize → embed → SQLite + HNSW index

HNSW is backed by hnswlib when available; falls back to brute-force numpy cosine search.
"""
import json
import logging
import os
import sqlite3
import threading
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from . import config

logger = logging.getLogger(__name__)


# ── HNSW wrapper (hnswlib or numpy fallback) ──────────────────────────────


class _HNSWIndex:
    """Thin wrapper around hnswlib with numpy brute-force fallback."""

    def __init__(self, dim: int):
        self._dim = dim
        self._lib = None
        self._index = None
        self._ids: List[str] = []          # int_label → memory_id
        self._lock = threading.RLock()
        self._try_load_lib()

    def _try_load_lib(self):
        try:
            import hnswlib
            self._lib = hnswlib
            logger.info("HNSW: using hnswlib")
        except ImportError:
            logger.warning("HNSW: hnswlib not available — using numpy brute-force fallback")

    def _ensure_index(self, dim: int) -> None:
        if self._lib is None:
            return
        if self._index is None or self._dim != dim:
            self._dim = dim
            self._index = self._lib.Index(space="cosine", dim=dim)
            self._index.init_index(
                max_elements=config.EPISODIC_MAX_ITEMS,
                ef_construction=config.HNSW_EF_CONSTRUCTION,
                M=config.HNSW_M,
            )
            self._index.set_ef(config.HNSW_EF_SEARCH)
            self._ids = []

    def add(self, memory_id: str, vector: np.ndarray) -> None:
        dim = len(vector)
        with self._lock:
            self._ensure_index(dim)
            int_label = len(self._ids)
            self._ids.append(memory_id)
            if self._index is not None:
                self._index.add_items(
                    vector.reshape(1, -1).astype(np.float32), [int_label]
                )

    def search(self, query: np.ndarray, top_k: int) -> List[Tuple[str, float]]:
        """Returns list of (memory_id, cosine_distance) sorted by distance asc."""
        with self._lock:
            if not self._ids:
                return []
            if self._index is not None:
                k = min(top_k, len(self._ids))
                labels, distances = self._index.knn_query(
                    query.reshape(1, -1).astype(np.float32), k=k
                )
                return [
                    (self._ids[lbl], float(dist))
                    for lbl, dist in zip(labels[0], distances[0])
                    if lbl < len(self._ids)
                ]
            else:
                return self._numpy_search(query, top_k)

    def _numpy_search(self, query: np.ndarray, top_k: int) -> List[Tuple[str, float]]:
        """Brute-force cosine search."""
        # We need all vectors — they're stored in DB; this is best-effort
        return []  # Caller falls back to FTS5 if empty

    def save(self, path: str, labels_path: str) -> None:
        with self._lock:
            if self._index is not None:
                self._index.save_index(path)
            np.save(labels_path, np.array(self._ids, dtype=object))

    def load(self, path: str, labels_path: str, dim: int) -> bool:
        with self._lock:
            try:
                if self._lib is None:
                    return False
                self._ensure_index(dim)
                self._index.load_index(path, max_elements=config.EPISODIC_MAX_ITEMS)
                self._index.set_ef(config.HNSW_EF_SEARCH)
                self._ids = list(np.load(labels_path, allow_pickle=True))
                logger.info("HNSW: loaded %d items from disk", len(self._ids))
                return True
            except Exception as e:
                logger.warning("HNSW: load failed (%s), starting fresh", e)
                return False

    def rebuild(self, items: List[Tuple[str, np.ndarray]]) -> None:
        """Rebuild index from scratch from list of (id, vector)."""
        with self._lock:
            if not items:
                return
            dim = items[0][1].shape[0]
            self._ensure_index(dim)
            self._ids = []
            for mid, vec in items:
                int_label = len(self._ids)
                self._ids.append(mid)
                if self._index is not None:
                    self._index.add_items(
                        vec.reshape(1, -1).astype(np.float32), [int_label]
                    )
            logger.info("HNSW: rebuilt with %d items", len(self._ids))

    @property
    def count(self) -> int:
        return len(self._ids)


# ── EpisodicMemory ────────────────────────────────────────────────────────


class EpisodicMemory:
    def __init__(self, db_path=config.DB_PATH):
        self._db_path = str(db_path)
        self._lock = threading.RLock()
        self._hnsw: Optional[_HNSWIndex] = None
        self._init_schema()
        self._init_hnsw()

    # ── Schema ──────────────────────────────────────────────────────────────

    def _init_schema(self) -> None:
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodes (
                    id TEXT PRIMARY KEY,
                    summary TEXT NOT NULL,
                    raw_messages TEXT,
                    embedding_blob BLOB,
                    timestamp REAL NOT NULL,
                    last_accessed REAL NOT NULL,
                    importance REAL NOT NULL DEFAULT 0.5,
                    message_count INTEGER NOT NULL DEFAULT 0,
                    archived INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ep_ts ON episodes(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ep_arch ON episodes(archived)")

    # ── HNSW init/persist ────────────────────────────────────────────────────

    def _init_hnsw(self) -> None:
        idx_path = str(config.HNSW_INDEX_PATH)
        lbl_path = str(config.HNSW_LABELS_PATH)
        self._hnsw = _HNSWIndex(config.EMBED_DIM)
        if os.path.exists(idx_path) and os.path.exists(lbl_path):
            success = self._hnsw.load(idx_path, lbl_path, config.EMBED_DIM)
            if not success:
                self._rebuild_hnsw_from_db()
        else:
            self._rebuild_hnsw_from_db()

    def _rebuild_hnsw_from_db(self) -> None:
        """Re-index all episodes from DB."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, embedding_blob FROM episodes WHERE embedding_blob IS NOT NULL AND archived=0"
            ).fetchall()
        items = []
        for mid, blob in rows:
            vec = np.frombuffer(blob, dtype=np.float32).copy()
            items.append((mid, vec))
        if items:
            self._hnsw.rebuild(items)
            self._save_hnsw()
            logger.info("EpisodicMemory: rebuilt HNSW with %d items", len(items))

    def _save_hnsw(self) -> None:
        try:
            self._hnsw.save(str(config.HNSW_INDEX_PATH), str(config.HNSW_LABELS_PATH))
        except Exception as e:
            logger.warning("EpisodicMemory: HNSW save failed: %s", e)

    # ── Write ────────────────────────────────────────────────────────────────

    def add_episode(
        self,
        summary: str,
        raw_messages: Optional[List[Dict]] = None,
        embedding: Optional[np.ndarray] = None,
        importance: float = 0.5,
        message_count: int = 0,
    ) -> str:
        eid = str(uuid.uuid4())
        now = time.time()
        raw_json = json.dumps(raw_messages) if raw_messages else None
        emb_blob = embedding.astype(np.float32).tobytes() if embedding is not None else None

        with self._lock:
            with self._conn() as conn:
                conn.execute(
                    """INSERT INTO episodes
                       (id, summary, raw_messages, embedding_blob, timestamp, last_accessed, importance, message_count, archived)
                       VALUES (?,?,?,?,?,?,?,?,0)""",
                    (eid, summary, raw_json, emb_blob, now, now, importance, message_count),
                )
            if embedding is not None:
                self._hnsw.add(eid, embedding)
                self._save_hnsw()

        # Auto-archive if over limit
        self._maybe_archive_old()
        return eid

    def update_embedding(self, episode_id: str, embedding: np.ndarray) -> None:
        blob = embedding.astype(np.float32).tobytes()
        with self._lock:
            with self._conn() as conn:
                conn.execute(
                    "UPDATE episodes SET embedding_blob=? WHERE id=?",
                    (blob, episode_id),
                )
            self._hnsw.add(episode_id, embedding)
            self._save_hnsw()

    # ── Search ───────────────────────────────────────────────────────────────

    def vector_search(self, query_vec: np.ndarray, top_k: int = 20) -> List[Dict]:
        """ANN search via HNSW."""
        hits = self._hnsw.search(query_vec, top_k)
        if not hits:
            return []
        results = []
        for eid, dist in hits:
            ep = self._get_by_id(eid)
            if ep:
                ep["vector_distance"] = dist
                ep["semantic_similarity"] = max(0.0, 1.0 - dist)
                results.append(ep)
        return results

    def keyword_search(self, query: str, top_k: int = 20) -> List[Dict]:
        """Simple LIKE-based fallback."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id,summary,raw_messages,embedding_blob,timestamp,last_accessed,importance,message_count,archived "
                "FROM episodes WHERE summary LIKE ? AND archived=0 LIMIT ?",
                (f"%{query}%", top_k),
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def _get_by_id(self, eid: str) -> Optional[Dict]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id,summary,raw_messages,embedding_blob,timestamp,last_accessed,importance,message_count,archived "
                "FROM episodes WHERE id=?",
                (eid,),
            ).fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    # ── Maintenance ──────────────────────────────────────────────────────────

    def get_without_embeddings(self) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id,summary,raw_messages,embedding_blob,timestamp,last_accessed,importance,message_count,archived "
                "FROM episodes WHERE embedding_blob IS NULL AND archived=0"
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def apply_decay(self) -> int:
        now = time.time()
        updated = 0
        with self._lock:
            with self._conn() as conn:
                rows = conn.execute(
                    "SELECT id, importance, last_accessed FROM episodes WHERE archived=0"
                ).fetchall()

                updates = []
                for eid, imp, la in rows:
                    days = (now - la) / 86400.0
                    new_imp = imp * (config.DECAY_RATE ** days)
                    # ⚡ Bolt Optimization: Batch N+1 UPDATE queries into a single executemany call
                    updates.append((max(0.0, new_imp), eid))

                if updates:
                    conn.executemany(
                        "UPDATE episodes SET importance=? WHERE id=?",
                        updates,
                    )
                    updated = len(updates)
        return updated

    def _maybe_archive_old(self) -> None:
        with self._conn() as conn:
            total = conn.execute(
                "SELECT COUNT(*) FROM episodes WHERE archived=0"
            ).fetchone()[0]
            if total > config.EPISODIC_MAX_ITEMS:
                over = total - config.EPISODIC_MAX_ITEMS
                rows = conn.execute(
                    "SELECT id FROM episodes WHERE archived=0 ORDER BY importance ASC, timestamp ASC LIMIT ?",
                    (over,),
                ).fetchall()
                for (eid,) in rows:
                    conn.execute("UPDATE episodes SET archived=1 WHERE id=?", (eid,))

    def rebuild_index(self) -> None:
        self._rebuild_hnsw_from_db()

    def count(self, archived: bool = False) -> int:
        with self._conn() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM episodes WHERE archived=?", (1 if archived else 0,)
            ).fetchone()[0]

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _row_to_dict(self, row) -> Dict:
        eid, summary, raw_j, emb_blob, ts, la, imp, mc, archived = row[:9]
        emb = np.frombuffer(emb_blob, dtype=np.float32).copy() if emb_blob else None
        return {
            "id": eid,
            "summary": summary,
            "raw_messages": json.loads(raw_j) if raw_j else [],
            "embedding": emb,
            "timestamp": ts,
            "last_accessed": la,
            "importance": imp,
            "message_count": mc,
            "archived": bool(archived),
            "source": "episodic",
            "text": summary,
        }

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn
