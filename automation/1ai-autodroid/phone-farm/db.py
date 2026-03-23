#!/usr/bin/env python3
"""
Phone Farm — SQLite state store.

Replaces single JSON state file. Thread-safe, WAL mode, survives restarts.
Stores: device state, task results, alerts, config.
"""

import json
import sqlite3
import threading
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent.parent / "logs" / "phone-farm" / "farm.db"
_local = threading.local()


def get_conn() -> sqlite3.Connection:
    """Thread-local SQLite connection (WAL mode)."""
    if not hasattr(_local, "conn") or _local.conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        conn.execute("PRAGMA foreign_keys=ON")
        _local.conn = conn
    return _local.conn


def init_db():
    """Create tables if not exist."""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS devices (
            serial      TEXT PRIMARY KEY,
            name        TEXT NOT NULL DEFAULT '',
            model       TEXT NOT NULL DEFAULT '',
            android_ver TEXT NOT NULL DEFAULT '',
            connection  TEXT NOT NULL DEFAULT 'usb',
            battery     INTEGER DEFAULT -1,
            screen_on   INTEGER DEFAULT 0,
            connected   INTEGER DEFAULT 0,
            current_app TEXT DEFAULT '',
            error_count INTEGER DEFAULT 0,
            last_error  TEXT DEFAULT '',
            last_seen   REAL DEFAULT 0,
            enabled     INTEGER DEFAULT 1,
            config_json TEXT DEFAULT '{}',
            created_at  REAL DEFAULT (unixepoch('now')),
            updated_at  REAL DEFAULT (unixepoch('now'))
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            serial      TEXT NOT NULL,
            device_name TEXT NOT NULL DEFAULT '',
            task_type   TEXT NOT NULL,
            success     INTEGER NOT NULL DEFAULT 0,
            data_json   TEXT DEFAULT '{}',
            error       TEXT DEFAULT '',
            duration_ms INTEGER DEFAULT 0,
            screenshot  TEXT DEFAULT '',
            ts          REAL DEFAULT (unixepoch('now')),
            ts_str      TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            serial      TEXT NOT NULL,
            alert_type  TEXT NOT NULL,
            message     TEXT NOT NULL,
            ts          REAL DEFAULT (unixepoch('now')),
            ts_str      TEXT DEFAULT (datetime('now','localtime')),
            acked       INTEGER DEFAULT 0
        );

        CREATE INDEX IF NOT EXISTS idx_tasks_serial ON tasks(serial);
        CREATE INDEX IF NOT EXISTS idx_tasks_ts ON tasks(ts DESC);
        CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(task_type);
        CREATE INDEX IF NOT EXISTS idx_alerts_serial ON alerts(serial);
        CREATE INDEX IF NOT EXISTS idx_alerts_ts ON alerts(ts DESC);
        CREATE INDEX IF NOT EXISTS idx_devices_connected ON devices(connected);
    """)
    conn.commit()


def upsert_device(serial: str, **kwargs):
    conn = get_conn()
    kwargs["serial"] = serial
    kwargs["updated_at"] = time.time()
    cols = ", ".join(kwargs.keys())
    placeholders = ", ".join(["?" for _ in kwargs])
    updates = ", ".join([f"{k}=excluded.{k}" for k in kwargs if k != "serial"])
    conn.execute(
        f"INSERT INTO devices ({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT(serial) DO UPDATE SET {updates}",
        list(kwargs.values()),
    )
    conn.commit()


def get_device(serial: str) -> Optional[dict]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM devices WHERE serial=?", (serial,)).fetchone()
    return dict(row) if row else None


def get_all_devices(connected_only: bool = False) -> list[dict]:
    conn = get_conn()
    if connected_only:
        rows = conn.execute(
            "SELECT * FROM devices WHERE enabled=1 AND connected=1 ORDER BY name"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM devices WHERE enabled=1 ORDER BY name"
        ).fetchall()
    return [dict(r) for r in rows]


def insert_task(serial: str, device_name: str, task_type: str,
                success: bool, data: dict, error: str = "",
                duration_ms: int = 0, screenshot: str = ""):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (serial, device_name, task_type, success, data_json, error, duration_ms, screenshot) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (serial, device_name, task_type, int(success),
         json.dumps(data), error, duration_ms, screenshot),
    )
    conn.commit()


def get_recent_tasks(serial: str = None, limit: int = 50, task_type: str = None) -> list[dict]:
    conn = get_conn()
    where = []
    params = []
    if serial:
        where.append("serial=?"); params.append(serial)
    if task_type:
        where.append("task_type=?"); params.append(task_type)
    clause = f"WHERE {' AND '.join(where)}" if where else ""
    params.append(limit)
    rows = conn.execute(
        f"SELECT * FROM tasks {clause} ORDER BY ts DESC LIMIT ?", params
    ).fetchall()
    return [dict(r) for r in rows]


def insert_alert(serial: str, alert_type: str, message: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO alerts (serial, alert_type, message) VALUES (?, ?, ?)",
        (serial, alert_type, message),
    )
    conn.commit()


def is_alert_recent(serial: str, alert_type: str, within_sec: int = 1800) -> bool:
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM alerts WHERE serial=? AND alert_type=? AND ts > ? AND acked=0",
        (serial, alert_type, time.time() - within_sec),
    ).fetchone()
    return row is not None


def get_recent_alerts(limit: int = 20, acked: bool = False) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM alerts WHERE acked=? ORDER BY ts DESC LIMIT ?",
        (int(acked), limit),
    ).fetchall()
    return [dict(r) for r in rows]


def get_stats() -> dict:
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM devices WHERE enabled=1").fetchone()[0]
    connected = conn.execute("SELECT COUNT(*) FROM devices WHERE connected=1 AND enabled=1").fetchone()[0]
    tasks_ok = conn.execute("SELECT COUNT(*) FROM tasks WHERE success=1 AND ts > ?",
                            (time.time() - 3600,)).fetchone()[0]
    tasks_fail = conn.execute("SELECT COUNT(*) FROM tasks WHERE success=0 AND ts > ?",
                              (time.time() - 3600,)).fetchone()[0]
    alerts = conn.execute("SELECT COUNT(*) FROM alerts WHERE acked=0").fetchone()[0]
    return {
        "devices_total": total,
        "devices_connected": connected,
        "tasks_1h_ok": tasks_ok,
        "tasks_1h_fail": tasks_fail,
        "unacked_alerts": alerts,
    }


def prune_old_tasks(days: int = 7):
    """Prune task log older than N days."""
    conn = get_conn()
    cutoff = time.time() - days * 86400
    deleted = conn.execute("DELETE FROM tasks WHERE ts < ?", (cutoff,)).rowcount
    conn.execute("DELETE FROM alerts WHERE ts < ? AND acked=1", (cutoff,))
    conn.commit()
    return deleted


if __name__ == "__main__":
    init_db()
    print("DB initialized:", DB_PATH)
    print("Stats:", get_stats())
