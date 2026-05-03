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


@dataclass
class QueryParams:
    """Pagination, filtering, sorting, and field selection for list endpoints."""

    search: str = ""
    sort: str = ""
    order: str = "asc"
    offset: int = 0
    limit: int = 50
    fields: list = field(default_factory=list)
    MAX_LIMIT = 200

    def __post_init__(self):
        self.offset = max(0, self.offset)
        self.limit = min(max(1, self.limit), self.MAX_LIMIT)

    def validate_sort(self, allowed_columns: list[str]) -> str:
        if not self.sort:
            return ""
        cols = [c.strip().lstrip("-") for c in self.sort.split(",")]
        valid = [c for c in cols if c in allowed_columns]
        if not valid:
            return ""
        sort_expr = ", ".join(valid)
        if self.sort.strip().startswith("-") and self.order != "desc":
            sort_expr = (
                valid[0]
                + " DESC"
                + (", " + ", ".join(valid[1:]) if len(valid) > 1 else "")
            )
        elif self.order == "desc":
            sort_expr = sort_expr.replace(valid[0], valid[0] + " DESC", 1)
        return sort_expr

    def build_where(
        self,
        search_columns: list[str] = None,
        extra_wheres: list[str] = None,
        params: list = None,
    ) -> tuple[str, list]:
        wheres = []
        p = params or []
        if extra_wheres:
            wheres.extend(extra_wheres)
        if self.search and search_columns:
            conditions = []
            for col in search_columns:
                conditions.append(f"LOWER({col}) LIKE ?")
                p.append(f"%{self.search.lower()}%")
            if conditions:
                wheres.append(f"({' OR '.join(conditions)})")
        clause = (" WHERE " + " AND ".join(wheres)) if wheres else ""
        return clause, p


def paginated_query(
    table: str,
    where_clause: str,
    params: list,
    sort_expr: str,
    qp: QueryParams,
) -> dict:
    """Run a paginated SELECT with COUNT, ORDER BY, LIMIT/OFFSET, and optional field selection."""
    conn = get_conn()
    count_row = conn.execute(
        f"SELECT COUNT(*) FROM {table}{where_clause}", params
    ).fetchone()
    total = count_row[0] if count_row else 0
    order_clause = f" ORDER BY {sort_expr}" if sort_expr else ""
    rows = conn.execute(
        f"SELECT * FROM {table}{where_clause}{order_clause} LIMIT ? OFFSET ?",
        (*params, qp.limit, qp.offset),
    ).fetchall()
    items = [dict(r) for r in rows]
    if qp.fields:
        select_fields = [f.strip() for f in qp.fields]
        items = [
            {k: v for k, v in item.items() if k in select_fields} for item in items
        ]
    return {
        "items": items,
        "total": total,
        "offset": qp.offset,
        "limit": qp.limit,
        "has_more": (qp.offset + qp.limit) < total,
    }


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
        CREATE TABLE IF NOT EXISTS tenants (
            id               TEXT PRIMARY KEY,
            name             TEXT NOT NULL DEFAULT '',
            email            TEXT DEFAULT '',
            stripe_customer_id TEXT DEFAULT '',
            api_key_hash     TEXT DEFAULT '',
            plan             TEXT DEFAULT 'free',
            rate_limit       REAL DEFAULT 100.0,
            created_at       REAL DEFAULT (unixepoch('now')),
            updated_at       REAL DEFAULT (unixepoch('now'))
        );

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
            tenant_id   TEXT DEFAULT 'default' REFERENCES tenants(id),
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
            ts_str      TEXT DEFAULT (datetime('now','localtime')),
            tenant_id   TEXT DEFAULT 'default' REFERENCES tenants(id)
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            serial      TEXT NOT NULL,
            alert_type  TEXT NOT NULL,
            message     TEXT NOT NULL,
            ts          REAL DEFAULT (unixepoch('now')),
            ts_str      TEXT DEFAULT (datetime('now','localtime')),
            acked       INTEGER DEFAULT 0,
            tenant_id   TEXT DEFAULT 'default' REFERENCES tenants(id)
        );

        CREATE INDEX IF NOT EXISTS idx_tasks_serial ON tasks(serial);
        CREATE INDEX IF NOT EXISTS idx_tasks_ts ON tasks(ts DESC);
        CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(task_type);
        CREATE INDEX IF NOT EXISTS idx_alerts_serial ON alerts(serial);
        CREATE INDEX IF NOT EXISTS idx_alerts_ts ON alerts(ts DESC);
        CREATE INDEX IF NOT EXISTS idx_devices_connected ON devices(connected);

        -- Device groups
        CREATE TABLE IF NOT EXISTS groups (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT UNIQUE NOT NULL,
            description TEXT DEFAULT '',
            tenant_id   TEXT DEFAULT 'default' REFERENCES tenants(id),
            created_at  REAL DEFAULT (unixepoch('now'))
        );

        CREATE TABLE IF NOT EXISTS device_groups (
            device_serial TEXT NOT NULL REFERENCES devices(serial) ON DELETE CASCADE,
            group_id      INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
            PRIMARY KEY (device_serial, group_id)
        );

        -- Device tags
        CREATE TABLE IF NOT EXISTS tags (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#888888'
        );

        CREATE TABLE IF NOT EXISTS device_tags (
            device_serial TEXT NOT NULL REFERENCES devices(serial) ON DELETE CASCADE,
            tag_id        INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (device_serial, tag_id)
        );

        -- Usage tracking (aggregated per period)
        CREATE TABLE IF NOT EXISTS usage (
            tenant_id    TEXT NOT NULL DEFAULT 'default' REFERENCES tenants(id),
            endpoint     TEXT NOT NULL DEFAULT '',
            method       TEXT NOT NULL DEFAULT 'GET',
            count        INTEGER NOT NULL DEFAULT 0,
            period_start REAL NOT NULL,
            period_end   REAL NOT NULL,
            PRIMARY KEY (tenant_id, endpoint, method, period_start)
        );

        CREATE INDEX IF NOT EXISTS idx_usage_tenant ON usage(tenant_id);
        CREATE INDEX IF NOT EXISTS idx_usage_period ON usage(period_start, period_end);

        -- Screenshot history
        CREATE TABLE IF NOT EXISTS screenshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            serial      TEXT NOT NULL,
            path        TEXT NOT NULL DEFAULT '',
            thumbnail   TEXT NOT NULL DEFAULT '',
            ts          REAL DEFAULT (unixepoch('now')),
            ts_str      TEXT DEFAULT (datetime('now','localtime')),
            tenant_id   TEXT DEFAULT 'default'
        );

        CREATE INDEX IF NOT EXISTS idx_screenshots_serial ON screenshots(serial);
        CREATE INDEX IF NOT EXISTS idx_screenshots_ts ON screenshots(ts DESC);

        -- Audit log
        CREATE TABLE IF NOT EXISTS audit_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id   TEXT DEFAULT 'default',
            user_id     TEXT DEFAULT '',
            method      TEXT NOT NULL DEFAULT '',
            path        TEXT NOT NULL DEFAULT '',
            status_code INTEGER DEFAULT 0,
            ip          TEXT DEFAULT '',
            user_agent   TEXT DEFAULT '',
            duration_ms  INTEGER DEFAULT 0,
            ts          REAL DEFAULT (unixepoch('now')),
            ts_str      TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_log(ts DESC);
        CREATE INDEX IF NOT EXISTS idx_audit_tenant ON audit_log(tenant_id);

        -- Users for email/password authentication
        CREATE TABLE IF NOT EXISTS users (
            id          TEXT PRIMARY KEY,
            email       TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name        TEXT NOT NULL DEFAULT '',
            role        TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user', 'admin', 'consumer')),
            tenant_id   TEXT DEFAULT 'default' REFERENCES tenants(id),
            credits     REAL DEFAULT 0,
            created_at  REAL DEFAULT (unixepoch('now')),
            updated_at  REAL DEFAULT (unixepoch('now')),
            last_login  REAL DEFAULT 0,
            banned      INTEGER DEFAULT 0
        );

        -- User sessions for email/password login
        CREATE TABLE IF NOT EXISTS sessions (
            id          TEXT PRIMARY KEY,
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token_hash  TEXT NOT NULL,
            expires_at  REAL NOT NULL,
            created_at  REAL DEFAULT (unixepoch('now'))
        );

        -- Password reset tokens
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            token_hash  TEXT PRIMARY KEY,
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            expires_at  REAL NOT NULL
        );

        -- Earnings from device rental tasks
        CREATE TABLE IF NOT EXISTS earnings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            device_serial TEXT NOT NULL,
            amount      REAL NOT NULL,
            task_type   TEXT NOT NULL,
            ts          REAL DEFAULT (unixepoch('now')),
            ts_str      TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);
        CREATE INDEX IF NOT EXISTS idx_earnings_user ON earnings(user_id);
        CREATE INDEX IF NOT EXISTS idx_earnings_ts ON earnings(ts DESC);

        -- Default tenant
        INSERT OR IGNORE INTO tenants (id, name, plan) VALUES ('default', 'Default', 'free');
    """)
    conn.commit()
    _migrate_tenant_ids()


def _migrate_tenant_ids():
    conn = get_conn()
    cols = {r[1] for r in conn.execute("PRAGMA table_info(devices)").fetchall()}
    if "tenant_id" not in cols:
        conn.execute("ALTER TABLE devices ADD COLUMN tenant_id TEXT DEFAULT 'default'")
    cols = {r[1] for r in conn.execute("PRAGMA table_info(tasks)").fetchall()}
    if "tenant_id" not in cols:
        conn.execute("ALTER TABLE tasks ADD COLUMN tenant_id TEXT DEFAULT 'default'")
    cols = {r[1] for r in conn.execute("PRAGMA table_info(alerts)").fetchall()}
    if "tenant_id" not in cols:
        conn.execute("ALTER TABLE alerts ADD COLUMN tenant_id TEXT DEFAULT 'default'")
    cols = {r[1] for r in conn.execute("PRAGMA table_info(groups)").fetchall()}
    if "tenant_id" not in cols:
        conn.execute("ALTER TABLE groups ADD COLUMN tenant_id TEXT DEFAULT 'default'")
    conn.execute("UPDATE devices SET tenant_id='default' WHERE tenant_id IS NULL")
    conn.execute("UPDATE tasks SET tenant_id='default' WHERE tenant_id IS NULL")
    conn.execute("UPDATE alerts SET tenant_id='default' WHERE tenant_id IS NULL")
    conn.execute("UPDATE groups SET tenant_id='default' WHERE tenant_id IS NULL")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_devices_tenant ON devices(tenant_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_tenant ON tasks(tenant_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_tenant ON alerts(tenant_id)")
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


def get_all_devices(
    connected_only: bool = False, tenant_id: str = None, qp: QueryParams = None
) -> dict:
    if qp is None:
        qp = QueryParams()
    wheres = ["enabled=1"]
    params = []
    if connected_only:
        wheres.append("connected=1")
    if tenant_id:
        wheres.append("tenant_id=?")
        params.append(tenant_id)
    where_clause, params = qp.build_where(
        search_columns=["name", "serial", "model"], extra_wheres=wheres, params=params
    )
    sort_expr = qp.validate_sort(
        ["name", "serial", "model", "battery", "android_ver", "connected", "last_seen"]
    )
    return paginated_query("devices", where_clause, params, sort_expr, qp)


def insert_task(
    serial: str,
    device_name: str,
    task_type: str,
    success: bool,
    data: dict,
    error: str = "",
    duration_ms: int = 0,
    screenshot: str = "",
):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (serial, device_name, task_type, success, data_json, error, duration_ms, screenshot) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            serial,
            device_name,
            task_type,
            int(success),
            json.dumps(data),
            error,
            duration_ms,
            screenshot,
        ),
    )
    conn.commit()


def get_recent_tasks(
    serial: str = None,
    limit: int = 50,
    task_type: str = None,
    tenant_id: str = None,
    qp: QueryParams = None,
) -> dict:
    if qp is None:
        qp = QueryParams(limit=limit)
    extra = []
    params = []
    if serial:
        extra.append("serial=?")
        params.append(serial)
    if task_type:
        extra.append("task_type=?")
        params.append(task_type)
    if tenant_id:
        extra.append("tenant_id=?")
        params.append(tenant_id)
    where_clause, params = qp.build_where(
        search_columns=["task_type", "serial", "device_name", "error"],
        extra_wheres=extra,
        params=params,
    )
    sort_expr = qp.validate_sort(
        ["ts", "serial", "task_type", "success", "duration_ms"]
    )
    return paginated_query("tasks", where_clause, params, sort_expr, qp)


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


def get_recent_alerts(
    limit: int = 20,
    acked: bool = False,
    tenant_id: str = None,
    qp: QueryParams = None,
) -> dict:
    if qp is None:
        qp = QueryParams(limit=limit)
    extra = [f"acked={int(acked)}"]
    params = []
    if tenant_id:
        extra.append("tenant_id=?")
        params.append(tenant_id)
    where_clause, params = qp.build_where(
        search_columns=["serial", "alert_type", "message"],
        extra_wheres=extra,
        params=params,
    )
    sort_expr = qp.validate_sort(["ts", "serial", "alert_type"])
    return paginated_query("alerts", where_clause, params, sort_expr, qp)


def get_stats(tenant_id: str = None) -> dict:
    conn = get_conn()
    if tenant_id:
        total = conn.execute(
            "SELECT COUNT(*) FROM devices WHERE enabled=1 AND tenant_id=?", (tenant_id,)
        ).fetchone()[0]
        connected = conn.execute(
            "SELECT COUNT(*) FROM devices WHERE connected=1 AND enabled=1 AND tenant_id=?",
            (tenant_id,),
        ).fetchone()[0]
        tasks_ok = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE success=1 AND ts > ? AND tenant_id=?",
            (time.time() - 3600, tenant_id),
        ).fetchone()[0]
        tasks_fail = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE success=0 AND ts > ? AND tenant_id=?",
            (time.time() - 3600, tenant_id),
        ).fetchone()[0]
        alerts = conn.execute(
            "SELECT COUNT(*) FROM alerts WHERE acked=0 AND tenant_id=?", (tenant_id,)
        ).fetchone()[0]
    else:
        total = conn.execute("SELECT COUNT(*) FROM devices WHERE enabled=1").fetchone()[
            0
        ]
        connected = conn.execute(
            "SELECT COUNT(*) FROM devices WHERE connected=1 AND enabled=1"
        ).fetchone()[0]
        tasks_ok = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE success=1 AND ts > ?",
            (time.time() - 3600,),
        ).fetchone()[0]
        tasks_fail = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE success=0 AND ts > ?",
            (time.time() - 3600,),
        ).fetchone()[0]
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


# === Device Groups ===


def create_group(name: str, description: str = "") -> int:
    """Create a new device group. Returns group_id."""
    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO groups (name, description) VALUES (?, ?)",
        (name, description),
    )
    conn.commit()
    return cursor.lastrowid


def delete_group(group_id: int):
    """Delete a device group."""
    conn = get_conn()
    conn.execute("DELETE FROM groups WHERE id = ?", (group_id,))
    conn.commit()


def get_groups(tenant_id: str = None, qp: QueryParams = None) -> dict:
    if qp is None:
        qp = QueryParams(limit=200)
    extra = []
    params = []
    if tenant_id:
        extra.append("tenant_id=?")
        params.append(tenant_id)
    where_clause, params = qp.build_where(
        search_columns=["name", "description"],
        extra_wheres=extra,
        params=params,
    )
    sort_expr = qp.validate_sort(["name", "id", "created_at"])
    return paginated_query("groups", where_clause, params, sort_expr, qp)


def add_device_to_group(device_serial: str, group_id: int):
    """Add a device to a group."""
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO device_groups (device_serial, group_id) VALUES (?, ?)",
        (device_serial, group_id),
    )
    conn.commit()


def remove_device_from_group(device_serial: str, group_id: int):
    """Remove a device from a group."""
    conn = get_conn()
    conn.execute(
        "DELETE FROM device_groups WHERE device_serial = ? AND group_id = ?",
        (device_serial, group_id),
    )
    conn.commit()


def get_devices_by_group(group_id: int, qp: QueryParams = None) -> dict:
    if qp is None:
        qp = QueryParams(limit=200)
    where_clause, params = qp.build_where()
    sort_expr = qp.validate_sort(["name", "serial", "model"])
    join_table = "devices d JOIN device_groups dg ON d.serial = dg.device_serial"
    if where_clause:
        full_where = where_clause + " AND dg.group_id=?"
    else:
        full_where = " WHERE dg.group_id=?"
    return paginated_query(join_table, full_where, (*params, group_id), sort_expr, qp)


# === Device Tags ===


def create_tag(name: str, color: str = "#888888") -> int:
    """Create a new tag. Returns tag_id."""
    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO tags (name, color) VALUES (?, ?)",
        (name, color),
    )
    conn.commit()
    return cursor.lastrowid


def delete_tag(tag_id: int):
    """Delete a tag."""
    conn = get_conn()
    conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    conn.commit()


def get_tags(qp: QueryParams = None) -> dict:
    if qp is None:
        qp = QueryParams(limit=200)
    where_clause, params = qp.build_where(search_columns=["name"])
    sort_expr = qp.validate_sort(["name", "id", "color"])
    return paginated_query("tags", where_clause, params, sort_expr, qp)


def add_tag_to_device(device_serial: str, tag_id: int):
    """Add a tag to a device."""
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO device_tags (device_serial, tag_id) VALUES (?, ?)",
        (device_serial, tag_id),
    )
    conn.commit()


def remove_tag_from_device(device_serial: str, tag_id: int):
    """Remove a tag from a device."""
    conn = get_conn()
    conn.execute(
        "DELETE FROM device_tags WHERE device_serial = ? AND tag_id = ?",
        (device_serial, tag_id),
    )
    conn.commit()


def get_devices_by_tag(tag_id: int, qp: QueryParams = None) -> dict:
    if qp is None:
        qp = QueryParams(limit=200)
    where_clause, params = qp.build_where()
    sort_expr = qp.validate_sort(["name", "serial", "model"])
    join_table = "devices d JOIN device_tags dt ON d.serial = dt.device_serial"
    if where_clause:
        full_where = where_clause + " AND dt.tag_id=?"
    else:
        full_where = " WHERE dt.tag_id=?"
    return paginated_query(join_table, full_where, (*params, tag_id), sort_expr, qp)


def get_tags_for_device(device_serial: str) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT t.* FROM tags t
        JOIN device_tags dt ON t.id = dt.tag_id
        WHERE dt.device_serial = ?
        ORDER BY t.name
    """,
        (device_serial,),
    ).fetchall()
    return [dict(r) for r in rows]


def insert_screenshot(serial: str, path: str, thumbnail: str = "") -> int:
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO screenshots (serial, path, thumbnail) VALUES (?, ?, ?)",
        (serial, path, thumbnail),
    )
    conn.commit()
    return cur.lastrowid


def get_screenshots(
    serial: str = None,
    limit: int = 50,
    tenant_id: str = None,
    qp: QueryParams = None,
) -> dict:
    if qp is None:
        qp = QueryParams(limit=limit)
    extra = []
    params = []
    if serial:
        extra.append("serial=?")
        params.append(serial)
    if tenant_id:
        extra.append("tenant_id=?")
        params.append(tenant_id)
    where_clause, params = qp.build_where(extra_wheres=extra, params=params)
    sort_expr = qp.validate_sort(["ts", "serial"])
    return paginated_query("screenshots", where_clause, params, sort_expr, qp)


def insert_audit(
    tenant_id: str,
    user_id: str,
    method: str,
    path: str,
    status_code: int,
    ip: str = "",
    user_agent: str = "",
    duration_ms: int = 0,
):
    conn = get_conn()
    conn.execute(
        "INSERT INTO audit_log (tenant_id, user_id, method, path, status_code, ip, user_agent, duration_ms) VALUES (?,?,?,?,?,?,?,?)",
        (tenant_id, user_id, method, path, status_code, ip, user_agent, duration_ms),
    )
    conn.commit()


def get_audit_log(
    tenant_id: str = None,
    limit: int = 100,
    user_id: str = None,
    qp: QueryParams = None,
) -> dict:
    if qp is None:
        qp = QueryParams(limit=limit)
    extra = []
    params = []
    if tenant_id:
        extra.append("tenant_id=?")
        params.append(tenant_id)
    if user_id:
        extra.append("user_id=?")
        params.append(user_id)
    where_clause, params = qp.build_where(
        search_columns=["path", "method", "user_id", "ip"],
        extra_wheres=extra,
        params=params,
    )
    sort_expr = qp.validate_sort(["ts", "method", "path", "status_code", "user_id"])
    return paginated_query("audit_log", where_clause, params, sort_expr, qp)


# === User Authentication ===

import secrets


def create_user(email: str, name: str, password_hash: str, role: str = "user") -> str:
    """Create a new user. Returns user id."""
    user_id = f"user_{secrets.token_hex(8)}"
    conn = get_conn()
    now = time.time()
    conn.execute(
        "INSERT INTO users (id, email, name, password_hash, role, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, email, name, password_hash, role, now, now),
    )
    conn.commit()
    return user_id


def get_user_by_email(email: str) -> Optional[dict]:
    """Get user by email address."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user by id."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def update_user(user_id: str, **kwargs) -> bool:
    """Update user fields. Returns True if updated."""
    if not kwargs:
        return False
    kwargs["updated_at"] = time.time()
    set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    params = list(kwargs.values()) + [user_id]
    conn = get_conn()
    cursor = conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?", params)
    conn.commit()
    return cursor.rowcount > 0


def verify_password(email: str, password_hash: str) -> bool:
    """Verify password hash against stored hash for user."""
    user = get_user_by_email(email)
    if not user:
        return False
    return user.get("password_hash") == password_hash


# === Sessions ===


def create_session(user_id: str, token_hash: str, expires_at: float) -> str:
    """Create a new session. Returns session id."""
    session_id = secrets.token_hex(32)
    now = time.time()
    conn = get_conn()
    conn.execute(
        "INSERT INTO sessions (id, user_id, token_hash, expires_at, created_at) VALUES (?, ?, ?, ?, ?)",
        (session_id, user_id, token_hash, expires_at, now),
    )
    conn.commit()
    return session_id


def get_session(session_id: str) -> Optional[dict]:
    """Get session by id. Returns session if valid (not expired)."""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM sessions WHERE id = ? AND expires_at > ?",
        (session_id, time.time()),
    ).fetchone()
    return dict(row) if row else None


def delete_session(session_id: str) -> bool:
    """Delete a session."""
    conn = get_conn()
    cursor = conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    return cursor.rowcount > 0


def delete_expired_sessions():
    """Delete all expired sessions."""
    conn = get_conn()
    cursor = conn.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
    conn.commit()
    return cursor.rowcount


# === Password Reset Tokens ===


def create_password_reset_token(
    user_id: str, token_hash: str, expires_at: float
) -> str:
    """Create password reset token. Returns token (plaintext for email)."""
    import secrets

    token = secrets.token_hex(32)
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO password_reset_tokens (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
        (token_hash, user_id, expires_at),
    )
    conn.commit()
    return token


def get_password_reset_token(token_hash: str) -> Optional[str]:
    """Get user_id for valid password reset token."""
    conn = get_conn()
    row = conn.execute(
        "SELECT user_id FROM password_reset_tokens WHERE token_hash = ? AND expires_at > ?",
        (token_hash, time.time()),
    ).fetchone()
    return row[0] if row else None


def delete_password_reset_token(token_hash: str) -> bool:
    """Delete a password reset token."""
    conn = get_conn()
    cursor = conn.execute(
        "DELETE FROM password_reset_tokens WHERE token_hash = ?", (token_hash,)
    )
    conn.commit()
    return cursor.rowcount > 0


# === Earnings ===


def add_earning(user_id: str, device_serial: str, amount: float, task_type: str) -> int:
    """Add earning record. Returns earning id."""
    conn = get_conn()
    now = time.time()
    cursor = conn.execute(
        "INSERT INTO earnings (user_id, device_serial, amount, task_type, ts, ts_str) VALUES (?, ?, ?, ?, ?, ?)",
        (
            user_id,
            device_serial,
            amount,
            task_type,
            now,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    return cursor.lastrowid


def get_user_earnings(user_id: str, limit: int = 50) -> list[dict]:
    """Get earnings history for a user."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM earnings WHERE user_id = ? ORDER BY ts DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    return [dict(r) for r in rows]


def get_user_total_earnings(user_id: str) -> float:
    """Get total earnings for a user."""
    conn = get_conn()
    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM earnings WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return row[0] if row else 0


if __name__ == "__main__":
    init_db()
    print("DB initialized:", DB_PATH)
    print("Stats:", get_stats())
