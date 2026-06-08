"""
ingestion_pipeline.py — Async queue + background worker for embedding ingestion.

Architecture:
  agent_response
    → raw_memory_store (non-blocking enqueue)
    → SQLite WAL queue
    → background_worker thread
    → vector_db_update

Features:
  • NEVER blocks the main agent thread
  • SHA256 job deduplication
  • Exponential backoff retry (1s → 2s → 4s → 8s)
  • Batch embedding (up to EMBED_BATCH_SIZE texts per call)
  • Rate-limit guard: HTTP 429 → immediate local fallback
  • Graceful shutdown
"""

import hashlib
import json
import logging
import sqlite3
import threading
import time
import uuid
from typing import Any, Callable, Dict, List, Optional

from . import config

logger = logging.getLogger(__name__)

_JOB_STATUS_PENDING = "pending"
_JOB_STATUS_DONE = "done"
_JOB_STATUS_FAILED = "failed"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class IngestionPipeline:
    """
    Background ingestion worker.
    Call enqueue_embed() from any thread — returns immediately.
    Worker thread picks up jobs, batches them, calls embed_fn, then
    calls store_fn to persist the embedding.
    """

    def __init__(
        self,
        db_path=config.DB_PATH,
        embed_fn: Optional[Callable[[List[str]], List[Any]]] = None,
        store_fn: Optional[Callable[[str, str, Any], None]] = None,
    ):
        """
        embed_fn(texts) → list of np.ndarray (or None per item)
        store_fn(job_id, memory_id, embedding) → None
        """
        self._db_path = str(db_path)
        self._embed_fn = embed_fn
        self._store_fn = store_fn
        self._shutdown = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._init_queue_table()
        self._start_worker()

    # ── Public API ───────────────────────────────────────────────────────────

    def enqueue_embed(
        self,
        memory_id: str,
        text: str,
        memory_type: str = "semantic",
        priority: int = 0,
    ) -> str:
        """
        Non-blocking: enqueue an embedding job.
        Deduplicates by (memory_id, text_hash).
        Returns job_id.
        """
        text_hash = _sha256(text)
        job_id = str(uuid.uuid4())
        now = time.time()
        with self._conn() as conn:
            # Deduplicate: skip if already pending/done for this memory+text
            existing = conn.execute(
                """SELECT id FROM ingest_queue
                   WHERE memory_id=? AND text_hash=? AND status IN ('pending','done')
                   LIMIT 1""",
                (memory_id, text_hash),
            ).fetchone()
            if existing:
                return existing[0]
            conn.execute(
                """INSERT INTO ingest_queue
                   (id, memory_id, text, text_hash, memory_type, status, retries, priority, created_at, next_try_at)
                   VALUES (?,?,?,?,?,?,0,?,?,?)""",
                (
                    job_id,
                    memory_id,
                    text,
                    text_hash,
                    memory_type,
                    _JOB_STATUS_PENDING,
                    priority,
                    now,
                    now,
                ),
            )
        return job_id

    def enqueue_batch(self, items: List[Dict]) -> List[str]:
        """
        Enqueue multiple items at once.
        Each item: {memory_id, text, memory_type?, priority?}
        """
        return [
            self.enqueue_embed(
                memory_id=item["memory_id"],
                text=item["text"],
                memory_type=item.get("memory_type", "semantic"),
                priority=item.get("priority", 0),
            )
            for item in items
        ]

    def pending_count(self) -> int:
        with self._conn() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM ingest_queue WHERE status=?",
                (_JOB_STATUS_PENDING,),
            ).fetchone()[0]

    def shutdown(self, timeout: float = 5.0) -> None:
        self._shutdown.set()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=timeout)

    def set_embed_fn(self, fn: Callable) -> None:
        self._embed_fn = fn

    def set_store_fn(self, fn: Callable) -> None:
        self._store_fn = fn

    # ── Schema ───────────────────────────────────────────────────────────────

    def _init_queue_table(self) -> None:
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ingest_queue (
                    id TEXT PRIMARY KEY,
                    memory_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    text_hash TEXT NOT NULL,
                    memory_type TEXT NOT NULL DEFAULT 'semantic',
                    status TEXT NOT NULL DEFAULT 'pending',
                    retries INTEGER NOT NULL DEFAULT 0,
                    priority INTEGER NOT NULL DEFAULT 0,
                    created_at REAL NOT NULL,
                    next_try_at REAL NOT NULL,
                    error TEXT
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_iq_status ON ingest_queue(status, next_try_at)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_iq_mem ON ingest_queue(memory_id)"
            )

    # ── Worker ───────────────────────────────────────────────────────────────

    def _start_worker(self) -> None:
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name="memory-ingestion-worker",
            daemon=True,
        )
        self._worker_thread.start()
        logger.info("IngestionPipeline: worker thread started")

    def _worker_loop(self) -> None:
        while not self._shutdown.is_set():
            try:
                processed = self._process_batch()
                if processed == 0:
                    # Nothing to do — sleep briefly
                    self._shutdown.wait(config.WORKER_POLL_INTERVAL)
            except Exception as e:
                logger.error("IngestionPipeline: worker error: %s", e, exc_info=True)
                self._shutdown.wait(2.0)

    def _process_batch(self) -> int:
        """Pick up to EMBED_BATCH_SIZE pending jobs, embed, store. Returns count processed."""
        now = time.time()
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT id, memory_id, text, memory_type, retries
                   FROM ingest_queue
                   WHERE status=? AND next_try_at<=?
                   ORDER BY priority DESC, created_at ASC
                   LIMIT ?""",
                (_JOB_STATUS_PENDING, now, config.EMBED_BATCH_SIZE),
            ).fetchall()

        if not rows:
            return 0

        job_ids = [r[0] for r in rows]
        memory_ids = [r[1] for r in rows]
        texts = [r[2] for r in rows]
        mem_types = [r[3] for r in rows]
        retries_list = [r[4] for r in rows]

        # Generate embeddings
        if self._embed_fn is None:
            logger.warning("IngestionPipeline: no embed_fn set, skipping batch")
            return 0

        try:
            embeddings = self._embed_fn(texts)
        except Exception as e:
            logger.error("IngestionPipeline: embed_fn error: %s", e)
            embeddings = [None] * len(texts)

        # Store results
        for job_id, mem_id, text, mem_type, retries, emb in zip(
            job_ids, memory_ids, texts, mem_types, retries_list, embeddings
        ):
            if emb is not None:
                try:
                    if self._store_fn:
                        self._store_fn(job_id, mem_id, mem_type, emb)
                    self._mark_done(job_id)
                except Exception as e:
                    self._mark_retry(job_id, retries, str(e))
            else:
                self._mark_retry(job_id, retries, "embedding returned None")

        return len(rows)

    def _mark_done(self, job_id: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "UPDATE ingest_queue SET status=? WHERE id=?",
                (_JOB_STATUS_DONE, job_id),
            )

    def _mark_retry(self, job_id: str, retries: int, error: str) -> None:
        new_retries = retries + 1
        if new_retries > config.WORKER_MAX_RETRIES:
            with self._conn() as conn:
                conn.execute(
                    "UPDATE ingest_queue SET status=?, error=? WHERE id=?",
                    (_JOB_STATUS_FAILED, error[:500], job_id),
                )
            logger.warning(
                "IngestionPipeline: job %s permanently failed: %s", job_id, error
            )
            return
        # Exponential backoff
        delay = min(config.WORKER_RETRY_BASE * (2**retries), config.WORKER_RETRY_MAX)
        next_try = time.time() + delay
        with self._conn() as conn:
            conn.execute(
                "UPDATE ingest_queue SET retries=?, next_try_at=?, error=? WHERE id=?",
                (new_retries, next_try, error[:500], job_id),
            )
        logger.debug(
            "IngestionPipeline: job %s retry %d in %.1fs", job_id, new_retries, delay
        )

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn
