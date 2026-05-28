"""
memory_graph.py — Memory relationship graph with multi-hop traversal.

Storage:
  • SQLite table: memory_edges (persistent)
  • networkx DiGraph (in-memory, rebuilt from DB on init)

Edge types:
  refers_to, related_topic, learned_from, contradicts

Features:
  • Multi-hop traversal: traverse(start_id, max_hops=3, edge_types=[...])
  • Weighted edges (0.0–1.0)
  • Thread-safe
"""
import logging
import sqlite3
import threading
import time
from typing import Dict, List, Optional, Set, Tuple

from . import config

logger = logging.getLogger(__name__)

VALID_EDGE_TYPES = {"refers_to", "related_topic", "learned_from", "contradicts"}

try:
    import networkx as nx
    _HAS_NX = True
except ImportError:
    _HAS_NX = False
    logger.warning("memory_graph: networkx not available — in-memory graph disabled, using SQL only")


class MemoryGraph:
    def __init__(self, db_path=config.DB_PATH):
        self._db_path = str(db_path)
        self._lock = threading.RLock()
        self._graph = nx.DiGraph() if _HAS_NX else None
        self._init_schema()
        self._load_from_db()

    # ── Schema ───────────────────────────────────────────────────────────────

    def _init_schema(self) -> None:
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_edges (
                    from_id TEXT NOT NULL,
                    to_id TEXT NOT NULL,
                    edge_type TEXT NOT NULL,
                    weight REAL NOT NULL DEFAULT 1.0,
                    created_at REAL NOT NULL,
                    PRIMARY KEY (from_id, to_id, edge_type)
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_me_from ON memory_edges(from_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_me_to ON memory_edges(to_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_me_type ON memory_edges(edge_type)")

    def _load_from_db(self) -> None:
        """Populate networkx graph from DB on startup."""
        if self._graph is None:
            return
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT from_id, to_id, edge_type, weight FROM memory_edges"
            ).fetchall()
        with self._lock:
            for from_id, to_id, etype, weight in rows:
                self._graph.add_edge(from_id, to_id, edge_type=etype, weight=weight)
        logger.info("MemoryGraph: loaded %d edges from DB", len(rows))

    # ── Write ────────────────────────────────────────────────────────────────

    def add_edge(
        self,
        from_id: str,
        to_id: str,
        edge_type: str = "related_topic",
        weight: float = 1.0,
    ) -> None:
        if edge_type not in VALID_EDGE_TYPES:
            raise ValueError(f"Invalid edge_type '{edge_type}'. Valid: {VALID_EDGE_TYPES}")
        now = time.time()
        with self._lock:
            with self._conn() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO memory_edges
                       (from_id, to_id, edge_type, weight, created_at)
                       VALUES (?,?,?,?,?)""",
                    (from_id, to_id, edge_type, weight, now),
                )
            if self._graph is not None:
                self._graph.add_edge(from_id, to_id, edge_type=edge_type, weight=weight)

    def remove_edge(self, from_id: str, to_id: str, edge_type: Optional[str] = None) -> None:
        with self._lock:
            with self._conn() as conn:
                if edge_type:
                    conn.execute(
                        "DELETE FROM memory_edges WHERE from_id=? AND to_id=? AND edge_type=?",
                        (from_id, to_id, edge_type),
                    )
                else:
                    conn.execute(
                        "DELETE FROM memory_edges WHERE from_id=? AND to_id=?",
                        (from_id, to_id),
                    )
            if self._graph is not None and self._graph.has_edge(from_id, to_id):
                self._graph.remove_edge(from_id, to_id)

    def remove_node(self, memory_id: str) -> None:
        """Remove all edges for a memory."""
        with self._lock:
            with self._conn() as conn:
                conn.execute(
                    "DELETE FROM memory_edges WHERE from_id=? OR to_id=?",
                    (memory_id, memory_id),
                )
            if self._graph is not None and self._graph.has_node(memory_id):
                self._graph.remove_node(memory_id)

    # ── Traversal ────────────────────────────────────────────────────────────

    def traverse(
        self,
        start_id: str,
        max_hops: int = 3,
        edge_types: Optional[List[str]] = None,
        direction: str = "forward",  # "forward" | "backward" | "both"
    ) -> List[Dict]:
        """
        Multi-hop BFS traversal from start_id.

        Returns list of {
            memory_id, hop_distance, path, edge_type, weight
        } sorted by hop_distance asc.
        """
        edge_types_set = set(edge_types) if edge_types else VALID_EDGE_TYPES

        if self._graph is not None:
            return self._traverse_nx(start_id, max_hops, edge_types_set, direction)
        else:
            return self._traverse_sql(start_id, max_hops, edge_types_set, direction)

    def _traverse_nx(
        self, start_id: str, max_hops: int, edge_types: Set[str], direction: str
    ) -> List[Dict]:
        with self._lock:
            if not self._graph.has_node(start_id):
                return []

            visited: Dict[str, Dict] = {}
            queue: List[Tuple] = [(start_id, 0, [start_id])]

            while queue:
                node, hop, path = queue.pop(0)
                if hop >= max_hops:
                    continue

                # Determine neighbours
                if direction in ("forward", "both"):
                    for nbr, edge_data in self._graph[node].items() if node in self._graph else []:
                        etype = edge_data.get("edge_type", "related_topic")
                        weight = edge_data.get("weight", 1.0)
                        if etype in edge_types and nbr not in visited and nbr != start_id:
                            visited[nbr] = {
                                "memory_id": nbr,
                                "hop_distance": hop + 1,
                                "path": path + [nbr],
                                "edge_type": etype,
                                "weight": weight,
                            }
                            queue.append((nbr, hop + 1, path + [nbr]))

                if direction in ("backward", "both"):
                    for pred in self._graph.predecessors(node):
                        edge_data = self._graph[pred][node]
                        etype = edge_data.get("edge_type", "related_topic")
                        weight = edge_data.get("weight", 1.0)
                        if etype in edge_types and pred not in visited and pred != start_id:
                            visited[pred] = {
                                "memory_id": pred,
                                "hop_distance": hop + 1,
                                "path": [pred] + path,
                                "edge_type": etype,
                                "weight": weight,
                            }
                            queue.append((pred, hop + 1, [pred] + path))

        results = list(visited.values())
        results.sort(key=lambda x: (x["hop_distance"], -x["weight"]))
        return results

    def _traverse_sql(
        self, start_id: str, max_hops: int, edge_types: Set[str], direction: str
    ) -> List[Dict]:
        """Pure SQL BFS fallback (no networkx)."""
        edge_type_placeholders = ",".join("?" * len(edge_types))
        visited: Dict[str, Dict] = {}
        frontier = [start_id]

        for hop in range(1, max_hops + 1):
            if not frontier:
                break
            placeholders = ",".join("?" * len(frontier))
            with self._conn() as conn:
                if direction in ("forward", "both"):
                    rows = conn.execute(
                        f"""SELECT from_id, to_id, edge_type, weight
                            FROM memory_edges
                            WHERE from_id IN ({placeholders})
                            AND edge_type IN ({edge_type_placeholders})""",
                        frontier + list(edge_types),
                    ).fetchall()
                    for fr, to, etype, w in rows:
                        if to not in visited and to != start_id:
                            visited[to] = {"memory_id": to, "hop_distance": hop, "path": [], "edge_type": etype, "weight": w}

                if direction in ("backward", "both"):
                    rows = conn.execute(
                        f"""SELECT from_id, to_id, edge_type, weight
                            FROM memory_edges
                            WHERE to_id IN ({placeholders})
                            AND edge_type IN ({edge_type_placeholders})""",
                        frontier + list(edge_types),
                    ).fetchall()
                    for fr, to, etype, w in rows:
                        if fr not in visited and fr != start_id:
                            visited[fr] = {"memory_id": fr, "hop_distance": hop, "path": [], "edge_type": etype, "weight": w}

            frontier = [v["memory_id"] for v in visited.values() if v["hop_distance"] == hop]

        results = list(visited.values())
        results.sort(key=lambda x: (x["hop_distance"], -x["weight"]))
        return results

    # ── Query ────────────────────────────────────────────────────────────────

    def neighbors(self, memory_id: str, edge_types: Optional[List[str]] = None) -> List[Dict]:
        """Direct 1-hop neighbors."""
        return self.traverse(memory_id, max_hops=1, edge_types=edge_types)

    def find_path(self, start_id: str, end_id: str, max_hops: int = 4) -> Optional[List[str]]:
        """Find shortest path between two memories (networkx only)."""
        if self._graph is None:
            return None
        try:
            with self._lock:
                path = nx.shortest_path(self._graph, start_id, end_id)
                if len(path) - 1 <= max_hops:
                    return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            pass
        return None

    def edge_count(self) -> int:
        with self._conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM memory_edges").fetchone()[0]

    def node_count(self) -> int:
        with self._conn() as conn:
            return conn.execute(
                "SELECT COUNT(DISTINCT from_id) FROM memory_edges"
            ).fetchone()[0]

    # ── Internal ─────────────────────────────────────────────────────────────

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
