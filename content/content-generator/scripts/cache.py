"""SQLite-based cache system for reducing redundant API calls."""

import hashlib
import json
import os
import sqlite3
import time
from typing import Any, Optional


class Cache:
    """SQLite-based cache with TTL and size management."""

    def __init__(
        self,
        db_path: str = ".cache/content_cache.db",
        default_ttl: int = 3600,
        max_size_mb: int = 100,
    ):
        """Initialize the cache.

        Args:
            db_path: Path to SQLite database file.
            default_ttl: Default time-to-live in seconds.
            max_size_mb: Maximum cache size in megabytes.
        """
        self.db_path = db_path
        self.default_ttl = default_ttl
        self.max_size_mb = max_size_mb

        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    hash TEXT NOT NULL,
                    size INTEGER NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at ON cache(expires_at)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_hash ON cache(hash)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at ON cache(created_at)
            """)
            conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _hash_key(self, key: str) -> str:
        """Generate a hash for a key."""
        return hashlib.sha256(key.encode()).hexdigest()[:16]

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from cache.

        Args:
            key: The cache key.

        Returns:
            Cached value if found and not expired, None otherwise.
        """
        hashed_key = self._hash_key(key)
        now = time.time()

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT value, expires_at FROM cache
                WHERE key = ? AND (expires_at > ? OR expires_at = 0)
                """,
                (hashed_key, now),
            )
            row = cursor.fetchone()

            if row:
                try:
                    return json.loads(row["value"])
                except json.JSONDecodeError:
                    return row["value"]

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store a value in cache.

        Args:
            key: The cache key.
            value: The value to cache.
            ttl: Time-to-live in seconds. Uses default if not specified.

        Returns:
            True if successful, False otherwise.
        """
        if ttl is None:
            ttl = self.default_ttl

        hashed_key = self._hash_key(key)
        now = time.time()
        expires_at = now + ttl if ttl > 0 else 0

        # Serialize value
        if isinstance(value, (dict, list)):
            serialized = json.dumps(value)
        else:
            serialized = str(value)

        size = len(serialized.encode())

        # Check size limit before inserting
        self._enforce_size_limit()

        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO cache (key, value, created_at, expires_at, hash, size)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (hashed_key, serialized, now, expires_at, hashed_key, size),
                )
                conn.commit()
            return True
        except sqlite3.Error:
            return False

    def invalidate(self, key: str) -> bool:
        """Remove a specific key from cache.

        Args:
            key: The cache key to invalidate.

        Returns:
            True if key was found and removed, False otherwise.
        """
        hashed_key = self._hash_key(key)

        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM cache WHERE key = ?", (hashed_key,))
            conn.commit()
            return cursor.rowcount > 0

    def invalidate_by_hash(self, prompt_hash: str) -> int:
        """Remove all cache entries matching a prompt hash.

        Args:
            prompt_hash: The prompt hash to invalidate.

        Returns:
            Number of entries removed.
        """
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM cache WHERE hash = ?", (prompt_hash,))
            conn.commit()
            return cursor.rowcount

    def cleanup(self) -> int:
        """Remove all expired entries from cache.

        Returns:
            Number of entries removed.
        """
        now = time.time()

        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM cache WHERE expires_at > 0 AND expires_at < ?",
                (now,),
            )
            conn.commit()
            return cursor.rowcount

    def _enforce_size_limit(self) -> None:
        """Enforce the maximum cache size limit."""
        max_bytes = self.max_size_mb * 1024 * 1024

        with self._get_connection() as conn:
            # Get total cache size
            cursor = conn.execute("SELECT SUM(size) as total FROM cache")
            row = cursor.fetchone()
            total_size = row["total"] if row["total"] else 0

            if total_size > max_bytes:
                # Remove oldest entries until under limit
                cursor = conn.execute(
                    """
                    SELECT key, size FROM cache
                    ORDER BY created_at ASC
                    """
                )

                keys_to_delete = []
                for row in cursor:
                    if total_size <= max_bytes:
                        break
                    keys_to_delete.append((row["key"],))
                    total_size -= row["size"]

                if keys_to_delete:
                    conn.executemany("DELETE FROM cache WHERE key = ?", keys_to_delete)
                    conn.commit()

    def clear(self) -> int:
        """Clear all entries from cache.

        Returns:
            Number of entries removed.
        """
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM cache")
            conn.commit()
            return cursor.rowcount

    def get_stats(self) -> dict:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats.
        """
        with self._get_connection() as conn:
            now = time.time()

            cursor = conn.execute(
                """
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN expires_at > 0 AND expires_at < ? THEN 1 ELSE 0 END) as expired,
                    SUM(size) as total_size
                FROM cache
                """,
                (now,)
            )
            row = cursor.fetchone()

            # Use integer indices for compatibility per project guidelines
            total = row[0] or 0
            expired = row[1] or 0
            total_size = row[2] or 0

            return {
                "total_entries": total,
                "expired_entries": expired,
                "size_bytes": total_size,
                "size_mb": round(total_size / (1024 * 1024), 2),
            }


def hash_prompt(prompt: str) -> str:
    """Generate a hash for a prompt.

    Args:
        prompt: The prompt string to hash.

    Returns:
        A 16-character hash of the prompt.
    """
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]
