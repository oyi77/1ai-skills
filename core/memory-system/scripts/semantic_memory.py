"""
semantic_memory.py — SQLite FTS5 knowledge store with embeddings and decay.

Schema:
  memories(id, text, embedding_blob, timestamp, last_accessed, importance, tags, entity_refs, source)
  FTS5 virtual table for BM25 keyword search.

Features:
  • Full-text search via FTS5 + BM25
  • Importance decay (5%/day) + boost on access
  • Auto-archive low-importance old entries
  • Thread-safe
"""

import hashlib
import json
import logging
import sqlite3
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

import numpy as np

from . import config

logger = logging.getLogger(__name__)


def _now() -> float:
    return time.time()


class SemanticMemory:
    def __init__(self, db_path=config.DB_PATH):
        self._db_path = str(db_path)
        self._lock = threading.RLock()
        self._init_schema()

    # ── Schema ──────────────────────────────────────────────────────────────

    def _init_schema(self) -> None:
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    embedding_blob BLOB,
                    timestamp REAL NOT NULL,
                    last_accessed REAL NOT NULL,
                    importance REAL NOT NULL DEFAULT 0.5,
                    tags TEXT NOT NULL DEFAULT '[]',
                    entity_refs TEXT NOT NULL DEFAULT '[]',
                    source TEXT NOT NULL DEFAULT 'semantic',
                    archived INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_ts ON memories(timestamp)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_imp ON memories(importance)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_arch ON memories(archived)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_la ON memories(last_accessed)"
            )
            # FTS5 for keyword search
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    id UNINDEXED,
                    text,
                    tags,
                    content='memories',
                    content_rowid='rowid'
                )
            """)
            # Triggers to keep FTS in sync
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS mem_ai AFTER INSERT ON memories BEGIN
                    INSERT INTO memories_fts(rowid, id, text, tags) VALUES (new.rowid, new.id, new.text, new.tags);
                END
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS mem_ad AFTER DELETE ON memories BEGIN
                    INSERT INTO memories_fts(memories_fts, rowid, id, text, tags) VALUES('delete', old.rowid, old.id, old.text, old.tags);
                END
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS mem_au AFTER UPDATE ON memories BEGIN
                    INSERT INTO memories_fts(memories_fts, rowid, id, text, tags) VALUES('delete', old.rowid, old.id, old.text, old.tags);
                    INSERT INTO memories_fts(rowid, id, text, tags) VALUES (new.rowid, new.id, new.text, new.tags);
                END
            """)

    # ── Write ───────────────────────────────────────────────────────────────

    def add(
        self,
        text: str,
        embedding: Optional[np.ndarray] = None,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        entity_refs: Optional[List[str]] = None,
        source: str = "semantic",
        memory_id: Optional[str] = None,
    ) -> str:
        mid = memory_id or str(uuid.uuid4())
        now = _now()
        emb_blob = (
            embedding.astype(np.float32).tobytes() if embedding is not None else None
        )
        tags_json = json.dumps(tags or [])
        refs_json = json.dumps(entity_refs or [])
        with self._lock:
            with self._conn() as conn:
                conn.execute(
                    """INSERT OR IGNORE INTO memories
                       (id, text, embedding_blob, timestamp, last_accessed, importance, tags, entity_refs, source, archived)
                       VALUES (?,?,?,?,?,?,?,?,?,0)""",
                    (
                        mid,
                        text,
                        emb_blob,
                        now,
                        now,
                        importance,
                        tags_json,
                        refs_json,
                        source,
                    ),
                )
        return mid

    def update_embedding(self, memory_id: str, embedding: np.ndarray) -> None:
        blob = embedding.astype(np.float32).tobytes()
        with self._lock:
            with self._conn() as conn:
                conn.execute(
                    "UPDATE memories SET embedding_blob=? WHERE id=?",
                    (blob, memory_id),
                )

    # ── Read ────────────────────────────────────────────────────────────────

    def get(self, memory_id: str, update_access: bool = True) -> Optional[Dict]:
        with self._lock:
            with self._conn() as conn:
                row = conn.execute(
                    "SELECT id,text,embedding_blob,timestamp,last_accessed,importance,tags,entity_refs,source,archived "
                    "FROM memories WHERE id=?",
                    (memory_id,),
                ).fetchone()
            if not row:
                return None
            result = self._row_to_dict(row)
            if update_access and not result["archived"]:
                self._boost_importance(memory_id, conn if False else None)
            return result

    def fts_search(self, query: str, top_k: int = 20) -> List[Dict]:
        """BM25 full-text search via FTS5."""
        # Sanitize query for FTS5 (escape special chars)
        safe_q = query.replace('"', '""').replace("'", "''")
        with self._lock:
            with self._conn() as conn:
                try:
                    rows = conn.execute(
                        """SELECT m.id, m.text, m.embedding_blob, m.timestamp, m.last_accessed,
                                  m.importance, m.tags, m.entity_refs, m.source, m.archived,
                                  -fts.rank AS bm25_score
                           FROM memories_fts fts
                           JOIN memories m ON m.id = fts.id
                           WHERE memories_fts MATCH ? AND m.archived=0
                           ORDER BY fts.rank
                           LIMIT ?""",
                        (safe_q, top_k),
                    ).fetchall()
                except Exception:
                    # FTS query syntax error → fallback to LIKE
                    rows = conn.execute(
                        """SELECT id,text,embedding_blob,timestamp,last_accessed,
                                  importance,tags,entity_refs,source,archived, 0.5 AS bm25_score
                           FROM memories
                           WHERE text LIKE ? AND archived=0
                           LIMIT ?""",
                        (f"%{query}%", top_k),
                    ).fetchall()
        results = []
        for row in rows:
            d = self._row_to_dict(row[:10])
            d["bm25_score"] = float(row[10]) if row[10] else 0.0
            results.append(d)
        return results

    def get_without_embeddings(self, limit: int = 500) -> List[Dict]:
        """Return memories that need embeddings generated."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id,text,embedding_blob,timestamp,last_accessed,importance,tags,entity_refs,source,archived "
                "FROM memories WHERE embedding_blob IS NULL AND archived=0 LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def get_all_with_embeddings(self) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id,text,embedding_blob,timestamp,last_accessed,importance,tags,entity_refs,source,archived "
                "FROM memories WHERE embedding_blob IS NOT NULL AND archived=0"
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def count(self, archived: bool = False) -> int:
        with self._conn() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM memories WHERE archived=?",
                (1 if archived else 0,),
            ).fetchone()[0]

    # ── Decay & archiving ───────────────────────────────────────────────────

    def apply_decay(self) -> int:
        """Apply daily decay to all non-archived memories. Returns count updated."""
        now = _now()
        updated = 0
        with self._lock:
            with self._conn() as conn:
                rows = conn.execute(
                    "SELECT id, importance, last_accessed FROM memories WHERE archived=0"
                ).fetchall()
                for mid, imp, last_acc in rows:
                    days = (now - last_acc) / 86400.0
                    new_imp = imp * (config.DECAY_RATE**days)
                    conn.execute(
                        "UPDATE memories SET importance=? WHERE id=?",
                        (max(0.0, new_imp), mid),
                    )
                    updated += 1
        return updated

    def archive_low_importance(self) -> int:
        """Archive memories below threshold that are old enough. Returns count archived."""
        cutoff_time = _now() - config.DECAY_ARCHIVE_AFTER_DAYS * 86400
        with self._lock:
            with self._conn() as conn:
                result = conn.execute(
                    """UPDATE memories SET archived=1
                       WHERE importance < ? AND last_accessed < ? AND archived=0""",
                    (config.DECAY_LOW_IMPORTANCE, cutoff_time),
                )
                return result.rowcount

    def _boost_importance(self, memory_id: str, _conn=None) -> None:
        now = _now()
        with self._conn() as conn:
            row = conn.execute(
                "SELECT importance FROM memories WHERE id=?", (memory_id,)
            ).fetchone()
            if row:
                new_imp = min(1.0, row[0] + config.DECAY_ACCESS_BOOST)
                conn.execute(
                    "UPDATE memories SET importance=?, last_accessed=? WHERE id=?",
                    (new_imp, now, memory_id),
                )

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _row_to_dict(self, row) -> Dict:
        id_, text, emb_blob, ts, la, imp, tags_j, refs_j, source, archived = row[:10]
        emb = np.frombuffer(emb_blob, dtype=np.float32).copy() if emb_blob else None
        return {
            "id": id_,
            "text": text,
            "embedding": emb,
            "timestamp": ts,
            "last_accessed": la,
            "importance": imp,
            "tags": json.loads(tags_j) if tags_j else [],
            "entity_refs": json.loads(refs_j) if refs_j else [],
            "source": source,
            "archived": bool(archived),
        }

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn
