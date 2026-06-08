"""
working_memory.py — Ultra-fast in-process memory with TTL + LRU eviction.

Design:
  • Pure Python dict, no DB, no embeddings
  • Thread-safe via threading.Lock
  • LRU via collections.OrderedDict
  • TTL: each item carries an expiry timestamp
  • <1 ms per operation
"""

import time
import threading
import json
import logging
from collections import OrderedDict
from typing import Any, Optional

from . import config

logger = logging.getLogger(__name__)


class WorkingMemory:
    """
    In-process key-value store with TTL and LRU eviction.
    Falls back gracefully; never raises on get/set.
    """

    def __init__(
        self,
        max_items: int = config.WORKING_MAX_ITEMS,
        default_ttl: int = config.WORKING_DEFAULT_TTL,
    ):
        self._max = max_items
        self._default_ttl = default_ttl
        self._store: OrderedDict[str, dict] = OrderedDict()  # key → {value, expiry}
        self._lock = threading.RLock()

    # ── Public API ──────────────────────────────────────────────────────────

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store key → value.  ttl=None uses default; ttl=0 means no expiry."""
        if ttl is None:
            ttl = self._default_ttl
        expiry = time.time() + ttl if ttl > 0 else float("inf")
        with self._lock:
            if key in self._store:
                del self._store[key]  # remove so we re-insert at end (LRU)
            self._store[key] = {"value": value, "expiry": expiry}
            if len(self._store) > self._max:
                self._evict()

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve value or default.  Refreshes LRU position on hit."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            if time.time() > entry["expiry"]:
                del self._store[key]
                return default
            # Move to end (most-recently-used)
            self._store.move_to_end(key)
            return entry["value"]

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def keys(self) -> list:
        now = time.time()
        with self._lock:
            return [k for k, v in self._store.items() if v["expiry"] > now]

    def size(self) -> int:
        return len(self.keys())

    def purge_expired(self) -> int:
        """Remove expired items. Returns count removed."""
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._store.items() if v["expiry"] <= now]
            for k in expired:
                del self._store[k]
        return len(expired)

    def to_dict(self) -> dict:
        """Snapshot of all non-expired values."""
        now = time.time()
        with self._lock:
            return {k: v["value"] for k, v in self._store.items() if v["expiry"] > now}

    def stats(self) -> dict:
        now = time.time()
        with self._lock:
            total = len(self._store)
            expired = sum(1 for v in self._store.values() if v["expiry"] <= now)
        return {
            "total": total,
            "active": total - expired,
            "expired": expired,
            "max": self._max,
        }

    # ── Internals ───────────────────────────────────────────────────────────

    def _evict(self) -> None:
        """Evict LRU item (first item in OrderedDict)."""
        if self._store:
            evicted_key = next(iter(self._store))
            del self._store[evicted_key]
            logger.debug("WorkingMemory: evicted LRU key=%s", evicted_key)
