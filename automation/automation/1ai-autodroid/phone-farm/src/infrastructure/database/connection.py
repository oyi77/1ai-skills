"""
Database connection layer using aiosqlite.

Provides async database access with WAL mode enabled.
Reuses existing schema from db.py.
"""

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import aiosqlite

# Database path - same as db.py
DB_PATH = Path(__file__).parent.parent.parent / "logs" / "phone-farm" / "farm.db"

# Connection pool - single connection for simplicity
_db_connection: aiosqlite.Connection | None = None
_lock = asyncio.Lock()


async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """
    Async generator that yields a database connection.

    Yields:
        aiosqlite.Connection: Database connection with WAL mode enabled.

    Example:
        async for db in get_db():
            await db.execute("SELECT * FROM devices")
    """
    global _db_connection

    async with _lock:
        if _db_connection is None:
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            _db_connection = await aiosqlite.connect(str(DB_PATH))
            _db_connection.row_factory = aiosqlite.Row
            # Enable WAL mode
            await _db_connection.execute("PRAGMA journal_mode=WAL")
            await _db_connection.execute("PRAGMA synchronous=NORMAL")
            await _db_connection.execute("PRAGMA cache_size=10000")
            await _db_connection.execute("PRAGMA foreign_keys=ON")

    yield _db_connection


async def close_db():
    """Close the database connection."""
    global _db_connection
    if _db_connection is not None:
        await _db_connection.close()
        _db_connection = None


async def init_db():
    """
    Initialize database tables if they don't exist.

    Creates all tables from the existing db.py schema:
    - tenants, devices, tasks, alerts, groups, device_groups
    - tags, device_tags, usage, screenshots, audit_log
    - users, sessions, password_reset_tokens, earnings
    """
    async for db in get_db():
        await db.executescript("""
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
        await db.commit()

        # Run migrations for tenant_id columns
        await _migrate_tenant_ids(db)
        break


async def _migrate_tenant_ids(db: aiosqlite.Connection):
    """Migrate tenant_id columns if they don't exist."""
    # Get existing columns for devices table
    cursor = await db.execute("PRAGMA table_info(devices)")
    cols = {row[1] for row in await cursor.fetchall()}

    if "tenant_id" not in cols:
        await db.execute("ALTER TABLE devices ADD COLUMN tenant_id TEXT DEFAULT 'default'")

    cursor = await db.execute("PRAGMA table_info(tasks)")
    cols = {row[1] for row in await cursor.fetchall()}
    if "tenant_id" not in cols:
        await db.execute("ALTER TABLE tasks ADD COLUMN tenant_id TEXT DEFAULT 'default'")

    cursor = await db.execute("PRAGMA table_info(alerts)")
    cols = {row[1] for row in await cursor.fetchall()}
    if "tenant_id" not in cols:
        await db.execute("ALTER TABLE alerts ADD COLUMN tenant_id TEXT DEFAULT 'default'")

    cursor = await db.execute("PRAGMA table_info(groups)")
    cols = {row[1] for row in await cursor.fetchall()}
    if "tenant_id" not in cols:
        await db.execute("ALTER TABLE groups ADD COLUMN tenant_id TEXT DEFAULT 'default'")

    # Update NULL values
    await db.execute("UPDATE devices SET tenant_id='default' WHERE tenant_id IS NULL")
    await db.execute("UPDATE tasks SET tenant_id='default' WHERE tenant_id IS NULL")
    await db.execute("UPDATE alerts SET tenant_id='default' WHERE tenant_id IS NULL")
    await db.execute("UPDATE groups SET tenant_id='default' WHERE tenant_id IS NULL")

    # Create tenant indexes
    await db.execute("CREATE INDEX IF NOT EXISTS idx_devices_tenant ON devices(tenant_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_tasks_tenant ON tasks(tenant_id)")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_alerts_tenant ON alerts(tenant_id)")

    await db.commit()


if __name__ == "__main__":
    import asyncio

    async def main():
        await init_db()
        print("DB initialized:", DB_PATH)

        # Quick stats check
        async for db in get_db():
            cursor = await db.execute("SELECT COUNT(*) FROM devices")
            row = await cursor.fetchone()
            print("Devices count:", row[0] if row else 0)
            break

    asyncio.run(main())
