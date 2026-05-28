"""
hybrid_search.py — Combined semantic + BM25 + recency + importance scoring.

Formula:
  score = 0.6 * semantic_similarity
        + 0.2 * recency_score          (exp decay, half-life 30 days)
        + 0.1 * importance             (stored 0-1)
        + 0.1 * bm25_score             (normalised)

Graceful degradation:
  • If embeddings unavailable → weight_semantic=0, redistribute to BM25
  • If FTS fails → LIKE fallback
  • Always returns results (may be less accurate)
"""
import logging
import math
import time
from typing import Dict, List, Optional

import numpy as np

from . import config

logger = logging.getLogger(__name__)

try:
    from rank_bm25 import BM25Okapi
    _HAS_BM25 = True
except ImportError:
    _HAS_BM25 = False
    logger.warning("hybrid_search: rank_bm25 not available — BM25 scoring disabled")


def _recency_score(timestamp: float, now: float = None) -> float:
    """Exponential decay: score=1.0 at now, ~0.5 at 30 days."""
    if now is None:
        now = time.time()
    age_days = (now - timestamp) / 86400.0
    return math.exp(-age_days / config.RECENCY_HALF_LIFE_DAYS)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Safe cosine similarity."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def _normalize_bm25(scores: List[float]) -> List[float]:
    """Min-max normalise BM25 scores to [0,1]."""
    if not scores:
        return scores
    min_s = min(scores)
    max_s = max(scores)
    if max_s == min_s:
        return [0.5] * len(scores)
    return [(s - min_s) / (max_s - min_s) for s in scores]


class HybridSearch:
    def __init__(
        self,
        semantic_memory=None,
        episodic_memory=None,
        embedding_engine=None,
    ):
        self._sem = semantic_memory
        self._epi = episodic_memory
        self._emb = embedding_engine

    def search(
        self,
        query: str,
        top_k: int = 10,
        sources: Optional[List[str]] = None,
        min_importance: float = 0.0,
    ) -> List[Dict]:
        """
        Unified search across semantic + episodic memories.

        sources: None = all, or subset of ["semantic", "episodic"]
        Returns list of result dicts sorted by hybrid score (desc).
        """
        sources = sources or ["semantic", "episodic"]
        now = time.time()
        candidates: List[Dict] = []

        # 1. Get query embedding (may be None → degraded mode)
        query_vec = None
        if self._emb:
            try:
                query_vec = self._emb.embed(query)
            except Exception as e:
                logger.warning("hybrid_search: embedding failed (%s) — using keyword only", e)

        # 2. Gather candidates from each source
        if "semantic" in sources and self._sem:
            candidates.extend(self._fetch_semantic(query, query_vec, top_k * 3))

        if "episodic" in sources and self._epi:
            candidates.extend(self._fetch_episodic(query, query_vec, top_k * 3))

        if not candidates:
            return []

        # 3. Deduplicate by id
        seen = {}
        for c in candidates:
            cid = c.get("id", "")
            if cid not in seen:
                seen[cid] = c

        candidates = list(seen.values())

        # Filter by min_importance
        if min_importance > 0:
            candidates = [c for c in candidates if c.get("importance", 0) >= min_importance]

        # 4. BM25 scoring over candidate texts
        bm25_scores = self._bm25_score(query, candidates)

        # 5. Compute hybrid score for each candidate
        w_sem   = config.WEIGHT_SEMANTIC   if query_vec is not None else 0.0
        w_rec   = config.WEIGHT_RECENCY
        w_imp   = config.WEIGHT_IMPORTANCE
        w_bm25  = config.WEIGHT_BM25 + (config.WEIGHT_SEMANTIC if query_vec is None else 0.0)

        for i, c in enumerate(candidates):
            sem_sim  = c.pop("semantic_similarity", 0.0)
            rec      = _recency_score(c.get("timestamp", now), now)
            imp      = float(c.get("importance", 0.5))
            bm25     = bm25_scores[i]
            score    = w_sem * sem_sim + w_rec * rec + w_imp * imp + w_bm25 * bm25
            c["score"]             = round(score, 4)
            c["_debug_semantic"]   = round(sem_sim, 4)
            c["_debug_recency"]    = round(rec, 4)
            c["_debug_bm25"]       = round(bm25, 4)

        # 6. Sort descending and return top_k
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

    # ── Internal fetchers ────────────────────────────────────────────────────

    def _fetch_semantic(self, query: str, query_vec, top_k: int) -> List[Dict]:
        results = []
        # Vector search — batch cosine via numpy for speed
        if query_vec is not None:
            all_mems = self._sem.get_all_with_embeddings()
            valid = [m for m in all_mems if m.get("embedding") is not None]
            if valid:
                matrix = np.stack([m["embedding"] for m in valid]).astype(np.float32)
                q = query_vec.astype(np.float32)
                # Batch cosine: (M @ q) / (||M|| * ||q||)
                q_norm = np.linalg.norm(q)
                row_norms = np.linalg.norm(matrix, axis=1)
                row_norms = np.where(row_norms == 0, 1e-9, row_norms)
                sims = (matrix @ q) / (row_norms * (q_norm if q_norm > 0 else 1e-9))
                top_indices = np.argsort(sims)[::-1][:top_k]
                for i in top_indices:
                    valid[i]["semantic_similarity"] = float(sims[i])
                    results.append(valid[i])

        # Always add FTS results
        try:
            fts_results = self._sem.fts_search(query, top_k=top_k)
            for r in fts_results:
                r.setdefault("semantic_similarity", 0.0)
            results.extend(fts_results)
        except Exception as e:
            logger.debug("hybrid_search: FTS error: %s", e)

        return results

    def _fetch_episodic(self, query: str, query_vec, top_k: int) -> List[Dict]:
        results = []
        if query_vec is not None:
            try:
                vec_results = self._epi.vector_search(query_vec, top_k=top_k)
                results.extend(vec_results)
            except Exception as e:
                logger.debug("hybrid_search: episodic vector search error: %s", e)

        # Keyword fallback
        kw_results = self._epi.keyword_search(query, top_k=top_k)
        for r in kw_results:
            r.setdefault("semantic_similarity", 0.0)
        results.extend(kw_results)
        return results

    # ── BM25 ─────────────────────────────────────────────────────────────────

    def _bm25_score(self, query: str, candidates: List[Dict]) -> List[float]:
        if not _HAS_BM25 or not candidates:
            return [0.5] * len(candidates)
        try:
            corpus = [
                (c.get("text") or c.get("summary", "")).lower().split()
                for c in candidates
            ]
            bm25 = BM25Okapi(corpus)
            raw_scores = bm25.get_scores(query.lower().split())
            return _normalize_bm25(raw_scores.tolist())
        except Exception as e:
            logger.debug("hybrid_search: BM25 error: %s", e)
            return [0.5] * len(candidates)
