"""
embedding_engine.py — Dual-provider embedding with cache, fallback, and rate-limit guard.

Priority:
  1. OpenAI-compatible API (if key present and not in local_only mode)
  2. Local sentence-transformers (fallback)
  3. Zero-vector (last resort — search degrades to FTS5 only)

Features:
  • SHA256 embedding cache (SQLite)
  • Batch requests (up to EMBED_BATCH_SIZE texts)
  • HTTP 429 → immediate switch to local
  • Thread-safe; can be called from multiple agents concurrently
"""

import hashlib
import json
import logging
import sqlite3
import threading
import time
from typing import List, Optional

import numpy as np

from . import config

logger = logging.getLogger(__name__)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class EmbeddingEngine:
    def __init__(self, db_path=config.DB_PATH, mode: str = "hybrid"):
        self._db_path = str(db_path)
        self._lock = threading.Lock()
        self._mode = mode  # "hybrid" | "local_only" | "api_only"
        self._local_model = None
        self._local_model_lock = threading.Lock()
        self._use_api = True  # flipped to False on 429 until reset
        self._api_cooldown_until = 0.0
        self._init_cache_table()

    # ── Public ──────────────────────────────────────────────────────────────

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        if mode == "local_only":
            self._use_api = False
            logger.info("EmbeddingEngine: forced local_only mode")

    def embed(self, text: str) -> Optional[np.ndarray]:
        """Embed single text. Returns ndarray or None on total failure."""
        results = self.embed_batch([text])
        return results[0] if results else None

    def embed_batch(self, texts: List[str]) -> List[Optional[np.ndarray]]:
        """
        Embed a list of texts. Returns list of ndarray (or None for failures).
        Uses cache; only calls provider for cache misses.
        """
        if not texts:
            return []

        results: List[Optional[np.ndarray]] = [None] * len(texts)
        cache_misses: List[int] = []
        miss_texts: List[str] = []

        # 1. Check cache
        for i, text in enumerate(texts):
            cached = self._cache_get(text)
            if cached is not None:
                results[i] = cached
            else:
                cache_misses.append(i)
                miss_texts.append(text)

        if not miss_texts:
            return results

        # 2. Generate embeddings for misses
        embeddings = self._generate(miss_texts)

        # 3. Store in cache + fill results
        for idx, (original_idx, text, emb) in enumerate(
            zip(cache_misses, miss_texts, embeddings)
        ):
            if emb is not None:
                self._cache_put(text, emb)
            results[original_idx] = emb

        return results

    def dim(self) -> int:
        return config.EMBED_DIM

    # ── Provider dispatch ───────────────────────────────────────────────────

    def _generate(self, texts: List[str]) -> List[Optional[np.ndarray]]:
        """Route to API or local depending on mode and availability."""
        # Process in batches
        all_results: List[Optional[np.ndarray]] = []
        for i in range(0, len(texts), config.EMBED_BATCH_SIZE):
            batch = texts[i : i + config.EMBED_BATCH_SIZE]
            batch_results = self._generate_batch(batch)
            all_results.extend(batch_results)
        return all_results

    def _generate_batch(self, texts: List[str]) -> List[Optional[np.ndarray]]:
        if self._mode == "local_only":
            return self._local_embed(texts)

        # Check if API cooldown active
        if self._use_api and time.time() < self._api_cooldown_until:
            logger.debug("EmbeddingEngine: API in cooldown, using local")
            self._use_api = False

        if self._use_api and config.OPENAI_API_KEY:
            result = self._api_embed(texts)
            if result is not None:
                return result
            # API failed → fallback

        return self._local_embed(texts)

    def _api_embed(self, texts: List[str]) -> Optional[List[Optional[np.ndarray]]]:
        """Call OpenAI-compatible API. Returns None on any failure."""
        import urllib.request
        import urllib.error

        url = f"{config.OPENAI_API_BASE}/embeddings"
        payload = json.dumps(
            {
                "model": config.OPENAI_EMBED_MODEL,
                "input": texts,
            }
        ).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=config.EMBED_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                embeddings = [
                    np.array(item["embedding"], dtype=np.float32)
                    for item in sorted(data["data"], key=lambda x: x["index"])
                ]
                return embeddings
        except urllib.error.HTTPError as e:
            if e.code == 429:
                logger.warning(
                    "EmbeddingEngine: API rate-limited (429), switching to local"
                )
                self._use_api = False
                self._api_cooldown_until = time.time() + 60.0  # 1 minute cooldown
            else:
                logger.warning("EmbeddingEngine: API HTTP error %s", e.code)
            return None
        except Exception as e:
            logger.warning("EmbeddingEngine: API error %s", e)
            return None

    def _local_embed(self, texts: List[str]) -> List[Optional[np.ndarray]]:
        """Use sentence-transformers. Lazy-loads model on first call."""
        model = self._get_local_model()
        if model is None:
            logger.warning(
                "EmbeddingEngine: local model unavailable, returning zero-vectors"
            )
            return [None] * len(texts)
        try:
            embeddings = model.encode(
                texts, normalize_embeddings=True, show_progress_bar=False
            )
            # Update dim based on actual output
            actual_dim = embeddings.shape[1]
            if actual_dim != config.EMBED_DIM:
                # patch module-level dim used everywhere
                config.EMBED_DIM = actual_dim
            return [embeddings[i].astype(np.float32) for i in range(len(texts))]
        except Exception as e:
            logger.error("EmbeddingEngine: local embed error: %s", e)
            return [None] * len(texts)

    def _get_local_model(self):
        if self._local_model is not None:
            return self._local_model
        with self._local_model_lock:
            if self._local_model is not None:
                return self._local_model
            try:
                from sentence_transformers import SentenceTransformer

                logger.info(
                    "EmbeddingEngine: loading local model %s", config.LOCAL_EMBED_MODEL
                )
                self._local_model = SentenceTransformer(config.LOCAL_EMBED_MODEL)
                logger.info("EmbeddingEngine: local model loaded")
                return self._local_model
            except Exception as e:
                logger.error("EmbeddingEngine: cannot load local model: %s", e)
                return None

    # ── Cache ───────────────────────────────────────────────────────────────

    def _init_cache_table(self) -> None:
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS embed_cache (
                    hash TEXT PRIMARY KEY,
                    embedding_bytes BLOB NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_embed_cache_ts ON embed_cache(created_at)"
            )

    def _cache_get(self, text: str) -> Optional[np.ndarray]:
        h = _sha256(text)
        cutoff = time.time() - config.EMBED_CACHE_TTL_DAYS * 86400
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT embedding_bytes FROM embed_cache WHERE hash=? AND created_at>?",
                (h, cutoff),
            ).fetchone()
        if row:
            return np.frombuffer(row[0], dtype=np.float32).copy()
        return None

    def _cache_put(self, text: str, emb: np.ndarray) -> None:
        h = _sha256(text)
        blob = emb.astype(np.float32).tobytes()
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO embed_cache(hash, embedding_bytes, created_at) VALUES (?,?,?)",
                (h, blob, time.time()),
            )

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
