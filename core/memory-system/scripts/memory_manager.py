"""
memory_manager.py — Unified interface to all 4 memory layers.

This is the ONLY file agents need to import.

Usage:
    from skills.memory_system.scripts import MemoryManager

    mm = MemoryManager()
    mm.store("User prefers H1+M5 scalping", importance=0.9, tags=["trading"])
    results = mm.search("trading strategy", top_k=5)
    mm.set_working("current_task", {"type": "analysis", "symbol": "XAUUSD"})
    task = mm.get_working("current_task")
    stats = mm.get_stats()
    report = mm.health_check()
"""
import json
import logging
import threading
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import numpy as np

from . import config
from .working_memory import WorkingMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .archive_memory import ArchiveMemory
from .embedding_engine import EmbeddingEngine
from .ingestion_pipeline import IngestionPipeline
from .hybrid_search import HybridSearch
from .memory_graph import MemoryGraph

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Single entry point for all memory operations.

    Layers:
      1. WorkingMemory  — dict + TTL, <1ms, in-process
      2. EpisodicMemory — HNSW vector index, conversation episodes
      3. SemanticMemory — SQLite FTS5 + embeddings, facts/knowledge
      4. ArchiveMemory  — gzipped JSONL, cold storage

    Async pipeline: embed jobs never block the caller.
    """

    def __init__(self, db_path=None, mode: str = "hybrid"):
        db = db_path or config.DB_PATH
        self._mode = mode
        self._lock = threading.RLock()

        # Layer init
        self._working  = WorkingMemory()
        self._episodic = EpisodicMemory(db_path=db)
        self._semantic = SemanticMemory(db_path=db)
        self._archive  = ArchiveMemory()
        self._graph    = MemoryGraph(db_path=db)

        # Embedding + pipeline
        self._emb = EmbeddingEngine(db_path=db, mode=mode)
        self._pipeline = IngestionPipeline(
            db_path=db,
            embed_fn=self._emb.embed_batch,
            store_fn=self._pipeline_store,
        )

        # Hybrid search
        self._search = HybridSearch(
            semantic_memory=self._semantic,
            episodic_memory=self._episodic,
            embedding_engine=self._emb,
        )

        # Message buffer for auto-summarisation
        self._msg_buffer: List[Dict] = []
        self._msg_buffer_lock = threading.Lock()

        logger.info("MemoryManager: initialised (mode=%s, db=%s)", mode, db)

    # ══════════════════════════════════════════════════════════════════════════
    # 1. STORE
    # ══════════════════════════════════════════════════════════════════════════

    def store(
        self,
        text: str,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        entity_refs: Optional[List[str]] = None,
        source: str = "agent",
        memory_id: Optional[str] = None,
        link_to: Optional[str] = None,
        edge_type: str = "related_topic",
    ) -> str:
        """
        Non-blocking store to semantic memory.
        Embedding is queued asynchronously.
        Returns memory_id.
        """
        mid = self._semantic.add(
            text=text,
            importance=min(1.0, max(0.0, importance)),
            tags=tags or [],
            entity_refs=entity_refs or [],
            source=source,
            memory_id=memory_id,
        )
        # Queue async embedding
        self._pipeline.enqueue_embed(memory_id=mid, text=text, memory_type="semantic")
        # Optionally link in graph
        if link_to:
            try:
                self._graph.add_edge(mid, link_to, edge_type=edge_type)
            except Exception:
                pass
        return mid

    # ══════════════════════════════════════════════════════════════════════════
    # 2. EPISODIC
    # ══════════════════════════════════════════════════════════════════════════

    def add_message(self, role: str, content: str) -> None:
        """Buffer a raw conversation message. Auto-summarises every N messages."""
        with self._msg_buffer_lock:
            self._msg_buffer.append({
                "role": role,
                "content": content,
                "timestamp": time.time(),
            })
            if len(self._msg_buffer) >= config.EPISODIC_SUMMARY_EVERY:
                self._flush_messages()

    def add_episode(self, messages: List[Dict], importance: float = 0.5) -> str:
        """
        Directly add a list of messages as an episode.
        Auto-summarises → async embed.
        """
        summary = self._summarise_messages(messages)
        eid = self._episodic.add_episode(
            summary=summary,
            raw_messages=messages,
            importance=importance,
            message_count=len(messages),
        )
        self._pipeline.enqueue_embed(memory_id=eid, text=summary, memory_type="episodic")
        return eid

    def flush_messages(self) -> Optional[str]:
        """Force flush the message buffer even if under threshold."""
        with self._msg_buffer_lock:
            if self._msg_buffer:
                return self._flush_messages()
        return None

    def _flush_messages(self) -> str:
        """Must be called with _msg_buffer_lock held."""
        messages = list(self._msg_buffer)
        self._msg_buffer.clear()
        return self.add_episode(messages)

    # ══════════════════════════════════════════════════════════════════════════
    # 3. SEARCH
    # ══════════════════════════════════════════════════════════════════════════

    def search(
        self,
        query: str,
        top_k: int = 5,
        sources: Optional[List[str]] = None,
        min_importance: float = 0.0,
    ) -> List[Dict]:
        """
        Hybrid search: semantic + BM25 + recency + importance.
        Always returns results even if embeddings are unavailable.

        Returns list of {text, score, source, timestamp, importance, id, tags}.
        """
        raw = self._search.search(
            query=query,
            top_k=top_k,
            sources=sources,
            min_importance=min_importance,
        )
        return [self._format_result(r) for r in raw]

    def get_memory(self, memory_id: str) -> Optional[Dict]:
        """Fetch a specific memory by id (boosts importance on access)."""
        result = self._semantic.get(memory_id, update_access=True)
        if result:
            return self._format_result(result)
        ep = self._episodic._get_by_id(memory_id)
        if ep:
            return self._format_result(ep)
        return None

    # ══════════════════════════════════════════════════════════════════════════
    # 4. WORKING MEMORY
    # ══════════════════════════════════════════════════════════════════════════

    def set_working(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._working.set(key, value, ttl=ttl)

    def get_working(self, key: str, default: Any = None) -> Any:
        return self._working.get(key, default)

    def delete_working(self, key: str) -> bool:
        return self._working.delete(key)

    # ══════════════════════════════════════════════════════════════════════════
    # 5. GRAPH
    # ══════════════════════════════════════════════════════════════════════════

    def link(
        self,
        from_id: str,
        to_id: str,
        edge_type: str = "related_topic",
        weight: float = 1.0,
    ) -> None:
        self._graph.add_edge(from_id, to_id, edge_type=edge_type, weight=weight)

    def traverse(
        self,
        start_id: str,
        max_hops: int = 3,
        edge_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Multi-hop graph traversal from a memory node."""
        raw = self._graph.traverse(start_id, max_hops=max_hops, edge_types=edge_types)
        enriched = []
        for item in raw:
            mem = self.get_memory(item["memory_id"])
            if mem:
                item.update({"text": mem.get("text", ""), "importance": mem.get("importance", 0.5)})
            enriched.append(item)
        return enriched

    # ══════════════════════════════════════════════════════════════════════════
    # 6. ARCHIVE
    # ══════════════════════════════════════════════════════════════════════════

    def archive_today(self) -> int:
        """Archive all current day's low-importance memories to cold storage."""
        count = self._semantic.archive_low_importance()
        logger.info("MemoryManager.archive_today: archived %d memories", count)
        return count

    def recall_archive(self, date: str) -> List[Dict]:
        """Recall memories from a specific date's archive."""
        return self._archive.recall(date)

    # ══════════════════════════════════════════════════════════════════════════
    # 7. DECAY
    # ══════════════════════════════════════════════════════════════════════════

    def decay_all(self) -> Dict:
        """Apply importance decay to all non-archived memories."""
        sem_count = self._semantic.apply_decay()
        epi_count = self._episodic.apply_decay()
        archived  = self._semantic.archive_low_importance()
        return {
            "semantic_decayed": sem_count,
            "episodic_decayed": epi_count,
            "auto_archived": archived,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # 8. COMPACTION
    # ══════════════════════════════════════════════════════════════════════════

    def compact(self, similarity_threshold: float = None) -> Dict:
        """
        Find clusters of highly-similar memories, summarise each cluster
        into one memory, archive the originals.

        Returns {clusters_found, memories_compacted, new_memories_created}
        """
        threshold = similarity_threshold or config.COMPACT_SIMILARITY_THRESHOLD
        all_mems = self._semantic.get_all_with_embeddings()

        if len(all_mems) < config.COMPACT_MIN_CLUSTER_SIZE:
            return {"clusters_found": 0, "memories_compacted": 0, "new_memories_created": 0}

        # Build embedding matrix
        valid = [m for m in all_mems if m["embedding"] is not None]
        if len(valid) < config.COMPACT_MIN_CLUSTER_SIZE:
            return {"clusters_found": 0, "memories_compacted": 0, "new_memories_created": 0}

        matrix = np.stack([m["embedding"] for m in valid]).astype(np.float32)
        # Normalise
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        matrix = matrix / norms

        # Cosine similarity matrix
        sim_matrix = matrix @ matrix.T

        # Greedy clustering
        used = set()
        clusters = []
        for i in range(len(valid)):
            if i in used:
                continue
            cluster = [i]
            for j in range(i + 1, len(valid)):
                if j not in used and sim_matrix[i, j] >= threshold:
                    cluster.append(j)
                    used.add(j)
            if len(cluster) >= config.COMPACT_MIN_CLUSTER_SIZE:
                clusters.append(cluster)
            used.add(i)

        if not clusters:
            return {"clusters_found": 0, "memories_compacted": 0, "new_memories_created": 0}

        compacted = 0
        created = 0
        for cluster_indices in clusters:
            cluster_mems = [valid[i] for i in cluster_indices]
            # Build merged summary
            texts = [m["text"] for m in cluster_mems]
            avg_importance = float(np.mean([m["importance"] for m in cluster_mems]))
            all_tags = list(set(t for m in cluster_mems for t in m.get("tags", [])))
            summary = self._compact_summarise(texts)

            # Create new compacted memory
            new_id = self.store(
                text=summary,
                importance=min(1.0, avg_importance + 0.1),
                tags=all_tags + ["compacted"],
                source="compaction",
            )
            created += 1

            # Archive originals
            self._archive.archive(cluster_mems)

            # ⚡ Bolt Optimization: Batch database updates using executemany
            # This replaces an individual UPDATE in a loop with a single executemany call,
            # avoiding multiple database connections and reducing round-trips.
            updates = [(m["id"],) for m in cluster_mems]
            if updates:
                with self._semantic._conn() as conn:
                    conn.executemany("UPDATE memories SET archived=1 WHERE id=?", updates)

            # Link originals → compacted
            for m in cluster_mems:
                try:
                    self._graph.add_edge(m["id"], new_id, edge_type="refers_to", weight=0.8)
                except Exception:
                    pass
            compacted += len(cluster_mems)

        logger.info(
            "MemoryManager.compact: found %d clusters, compacted %d → %d new memories",
            len(clusters), compacted, created,
        )
        return {
            "clusters_found": len(clusters),
            "memories_compacted": compacted,
            "new_memories_created": created,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # 9. HEALTH CHECK & SELF-HEALING
    # ══════════════════════════════════════════════════════════════════════════

    def health_check(self) -> Dict:
        """
        Audit memory system integrity and auto-fix issues.

        Checks:
          1. Memories missing embeddings → re-queue
          2. HNSW index consistency → rebuild if needed
          3. Ingest queue stuck jobs → reset
          4. DB schema integrity

        Returns report dict.
        """
        report = {
            "timestamp": time.time(),
            "issues": [],
            "fixes": [],
            "status": "healthy",
        }

        # 1. Memories without embeddings
        missing_sem = self._semantic.get_without_embeddings(limit=500)
        missing_epi = self._episodic.get_without_embeddings()

        if missing_sem:
            report["issues"].append(f"{len(missing_sem)} semantic memories missing embeddings")
            for m in missing_sem:
                self._pipeline.enqueue_embed(m["id"], m["text"], "semantic", priority=1)
            report["fixes"].append(f"Re-queued {len(missing_sem)} semantic embedding jobs")

        if missing_epi:
            report["issues"].append(f"{len(missing_epi)} episodes missing embeddings")
            for ep in missing_epi:
                self._pipeline.enqueue_embed(ep["id"], ep["text"], "episodic", priority=1)
            report["fixes"].append(f"Re-queued {len(missing_epi)} episodic embedding jobs")

        # 2. HNSW index vs DB count
        db_epi_count = self._episodic.count()
        hnsw_count = self._episodic._hnsw.count
        if abs(db_epi_count - hnsw_count) > max(5, db_epi_count * 0.05):
            report["issues"].append(
                f"HNSW index inconsistent: DB={db_epi_count}, index={hnsw_count}"
            )
            self._episodic.rebuild_index()
            report["fixes"].append("Rebuilt HNSW index from DB")

        # 3. Stuck ingest jobs (pending for >10 minutes)
        stuck_cutoff = time.time() - 600
        try:
            with self._pipeline._conn() as conn:
                stuck = conn.execute(
                    "SELECT COUNT(*) FROM ingest_queue WHERE status='pending' AND created_at<?",
                    (stuck_cutoff,),
                ).fetchone()[0]
                if stuck > 0:
                    report["issues"].append(f"{stuck} ingest jobs stuck (>10 min)")
                    conn.execute(
                        "UPDATE ingest_queue SET retries=0, next_try_at=? "
                        "WHERE status='pending' AND created_at<?",
                        (time.time(), stuck_cutoff),
                    )
                    report["fixes"].append(f"Reset {stuck} stuck ingest jobs")
        except Exception as e:
            report["issues"].append(f"Queue check error: {e}")

        # 4. Schema self-healing (re-run inits)
        try:
            self._semantic._init_schema()
            self._episodic._init_schema()
        except Exception as e:
            report["issues"].append(f"Schema check error: {e}")

        if report["issues"]:
            report["status"] = "repaired" if report["fixes"] else "degraded"

        return report

    # ══════════════════════════════════════════════════════════════════════════
    # 10. STATS & MODE
    # ══════════════════════════════════════════════════════════════════════════

    def get_stats(self) -> Dict:
        return {
            "total_memories": (
                self._semantic.count()
                + self._episodic.count()
                + self._working.size()
            ),
            "working": self._working.size(),
            "episodic": self._episodic.count(),
            "semantic": self._semantic.count(),
            "archived": (
                self._semantic.count(archived=True)
                + self._episodic.count(archived=True)
            ),
            "pending_embeddings": self._pipeline.pending_count(),
            "graph_edges": self._graph.edge_count(),
            "graph_nodes": self._graph.node_count(),
            "mode": self._mode,
            "archive": self._archive.stats(),
        }

    def set_mode(self, mode: str) -> None:
        """
        Set operating mode.
        "local_only" — never calls OpenAI API, uses local sentence-transformers
        "hybrid"     — tries API first, falls back to local
        "api_only"   — only OpenAI API (no local fallback)
        """
        self._mode = mode
        self._emb.set_mode(mode)
        logger.info("MemoryManager: mode set to %s", mode)

    # ══════════════════════════════════════════════════════════════════════════
    # INTERNAL HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    def _pipeline_store(self, job_id: str, memory_id: str, memory_type: str, embedding) -> None:
        """Callback from ingestion pipeline to store completed embedding."""
        if memory_type == "semantic":
            self._semantic.update_embedding(memory_id, embedding)
        elif memory_type == "episodic":
            self._episodic.update_embedding(memory_id, embedding)

    def _summarise_messages(self, messages: List[Dict]) -> str:
        """Simple extractive summarisation (no LLM dependency)."""
        if not messages:
            return ""
        parts = []
        for m in messages[-20:]:  # Last 20 for summary
            role = m.get("role", "?")
            content = str(m.get("content", ""))[:300]
            parts.append(f"[{role}] {content}")
        summary = " | ".join(parts)
        return summary[:1000]  # Cap at 1000 chars

    def _compact_summarise(self, texts: List[str]) -> str:
        """Merge multiple similar texts into a summary."""
        if not texts:
            return ""
        # Simple concatenation with dedup
        seen_sentences = set()
        merged = []
        for t in texts:
            for sentence in t.replace(". ", ".\n").split("\n"):
                s = sentence.strip()
                if s and s not in seen_sentences:
                    seen_sentences.add(s)
                    merged.append(s)
        return " ".join(merged)[:1500]

    def _format_result(self, r: Dict) -> Dict:
        """Standardise result format, strip raw embedding blob."""
        return {
            "id": r.get("id", ""),
            "text": r.get("text") or r.get("summary", ""),
            "score": r.get("score", 0.0),
            "source": r.get("source", "unknown"),
            "timestamp": r.get("timestamp", 0.0),
            "importance": r.get("importance", 0.5),
            "tags": r.get("tags", []),
            "entity_refs": r.get("entity_refs", []),
        }

    def shutdown(self) -> None:
        """Graceful shutdown — flush pending jobs."""
        self.flush_messages()
        self._pipeline.shutdown(timeout=10.0)
        logger.info("MemoryManager: shutdown complete")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.shutdown()
