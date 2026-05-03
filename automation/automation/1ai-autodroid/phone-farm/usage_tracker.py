#!/usr/bin/env python3
"""
Phone Farm — Usage Tracker

Tracks API calls and task executions per tenant.
In-memory counters with periodic SQLite flush.
"""

import threading
import time
import db

_counts: dict[str, dict[str, int]] = {}
_lock = threading.Lock()
_last_flush = time.time()
_flush_interval = 60


def track(tenant_id: str, endpoint: str, method: str = "GET"):
    with _lock:
        if tenant_id not in _counts:
            _counts[tenant_id] = {}
        key = f"{method}:{endpoint}"
        _counts[tenant_id][key] = _counts[tenant_id].get(key, 0) + 1
    _maybe_flush()


def get_usage(
    tenant_id: str, period_start: float = None, period_end: float = None
) -> dict:
    with _lock:
        tenant_counts = dict(_counts.get(tenant_id, {}))
    if period_start:
        return {k: v for k, v in tenant_counts.items()}
    return tenant_counts


def get_total(tenant_id: str) -> int:
    with _lock:
        return sum(_counts.get(tenant_id, {}).values())


def get_all_usage() -> dict:
    with _lock:
        return {tid: dict(counts) for tid, counts in _counts.items()}


def _maybe_flush():
    global _last_flush
    now = time.monotonic()
    if now - _last_flush >= _flush_interval:
        _last_flush = now
        _flush_to_db()


def _flush_to_db():
    with _lock:
        snapshot = {tid: dict(counts) for tid, counts in _counts.items()}
    if not snapshot:
        return
    conn = db.get_conn()
    now = time.time()
    period_start = now - _flush_interval
    try:
        for tenant_id, counts in snapshot.items():
            for key, count in counts.items():
                parts = key.split(":", 1)
                method = parts[0] if len(parts) > 1 else "GET"
                endpoint = parts[1] if len(parts) > 1 else key
                conn.execute(
                    "INSERT OR REPLACE INTO usage (tenant_id, endpoint, method, count, period_start, period_end) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (tenant_id, endpoint, method, count, period_start, now),
                )
        conn.commit()
    except Exception:
        pass
    # Reset in-memory counters after flush
    with _lock:
        for tid in snapshot:
            if tid in _counts:
                for key in snapshot[tid]:
                    _counts[tid][key] = max(
                        0, _counts[tid].get(key, 0) - snapshot[tid][key]
                    )
                if not any(v > 0 for v in _counts[tid].values()):
                    del _counts[tid]


def force_flush():
    _flush_to_db()


def reset():
    global _last_flush
    with _lock:
        _counts.clear()
    _last_flush = time.monotonic()


if __name__ == "__main__":
    db.init_db()
    track("default", "/devices", "GET")
    track("default", "/devices", "GET")
    track("default", "/tasks", "GET")
    print("Usage:", get_usage("default"))
    print("Total:", get_total("default"))
