"""Pytest configuration and fixtures for phonefarm tests."""

import sqlite3
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def test_db_path(tmp_path: Path) -> Path:
    return tmp_path / "test_phonefarm.db"


@pytest.fixture
def test_db_connection(test_db_path: Path) -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(str(test_db_path))
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            tenant_id TEXT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            tenant_id TEXT,
            serial TEXT UNIQUE NOT NULL,
            name TEXT,
            status TEXT DEFAULT 'offline',
            model TEXT,
            os_version TEXT,
            battery INTEGER,
            last_seen TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            tenant_id TEXT,
            device_id TEXT,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            priority INTEGER DEFAULT 0,
            result TEXT,
            error TEXT,
            started_at TEXT,
            completed_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (device_id) REFERENCES devices(id)
        );
        
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        
        CREATE TABLE IF NOT EXISTS api_keys (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            name TEXT NOT NULL,
            key_hash TEXT NOT NULL,
            expires_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS device_groups (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS tags (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            name TEXT NOT NULL,
            color TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS alerts (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            device_id TEXT,
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (device_id) REFERENCES devices(id)
        );
        
        CREATE TABLE IF NOT EXISTS webhooks (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            url TEXT NOT NULL,
            events TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS billing_usage (
            id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            api_calls INTEGER DEFAULT 0,
            tasks_run INTEGER DEFAULT 0,
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        );
        
        CREATE TABLE IF NOT EXISTS device_tags (
            device_id TEXT NOT NULL,
            tag_id TEXT NOT NULL,
            PRIMARY KEY (device_id, tag_id),
            FOREIGN KEY (device_id) REFERENCES devices(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id)
        );
        
        CREATE TABLE IF NOT EXISTS device_group_devices (
            group_id TEXT NOT NULL,
            device_id TEXT NOT NULL,
            PRIMARY KEY (group_id, device_id),
            FOREIGN KEY (group_id) REFERENCES device_groups(id),
            FOREIGN KEY (device_id) REFERENCES devices(id)
        );
    """)

    yield conn

    conn.close()


@pytest.fixture
def test_db_cursor(test_db_connection: sqlite3.Connection) -> sqlite3.Cursor:
    return test_db_connection.cursor()


@pytest.fixture
def mock_adb_pool():
    mock = MagicMock()
    mock.connect = MagicMock(return_value=True)
    mock.disconnect = MagicMock(return_value=True)
    mock.get_device = MagicMock(return_value=MagicMock(serial="MOCK_SERIAL"))
    mock.list_devices = MagicMock(return_value=[])
    return mock


@pytest.fixture
def mock_jwt_handler():
    mock = MagicMock()
    mock.create_token = MagicMock(return_value="test.jwt.token")
    mock.verify_token = MagicMock(return_value={"sub": "test_user", "tenant_id": "test_tenant"})
    return mock


@pytest.fixture
def mock_password_handler():
    mock = MagicMock()
    mock.hash_password = MagicMock(return_value="$2b$12$hashed_password")
    mock.verify_password = MagicMock(return_value=True)
    return mock


@pytest.fixture
def test_tenant(test_db_connection: sqlite3.Connection) -> dict:
    cursor = test_db_connection.cursor()
    tenant_id = "test_tenant_001"
    cursor.execute(
        "INSERT INTO tenants (id, name, api_key) VALUES (?, ?, ?)",
        (tenant_id, "Test Tenant", "test_api_key_123"),
    )
    test_db_connection.commit()
    return {"id": tenant_id, "name": "Test Tenant", "api_key": "test_api_key_123"}


@pytest.fixture
def test_user(test_db_connection: sqlite3.Connection, test_tenant: dict) -> dict:
    cursor = test_db_connection.cursor()
    user_id = "test_user_001"
    cursor.execute(
        "INSERT INTO users (id, tenant_id, username, password_hash, role) VALUES (?, ?, ?, ?, ?)",
        (user_id, test_tenant["id"], "testuser", "$2b$12$hashed", "admin"),
    )
    test_db_connection.commit()
    return {"id": user_id, "tenant_id": test_tenant["id"], "username": "testuser", "role": "admin"}


@pytest.fixture
def test_device(test_db_connection: sqlite3.Connection, test_tenant: dict) -> dict:
    cursor = test_db_connection.cursor()
    device_id = "test_device_001"
    cursor.execute(
        "INSERT INTO devices (id, tenant_id, serial, name, status) VALUES (?, ?, ?, ?, ?)",
        (device_id, test_tenant["id"], "SERIAL123", "Test Device", "online"),
    )
    test_db_connection.commit()
    return {
        "id": device_id,
        "tenant_id": test_tenant["id"],
        "serial": "SERIAL123",
        "name": "Test Device",
        "status": "online",
    }


@pytest.fixture
def test_task(test_db_connection: sqlite3.Connection, test_tenant: dict, test_device: dict) -> dict:
    cursor = test_db_connection.cursor()
    task_id = "test_task_001"
    cursor.execute(
        "INSERT INTO tasks (id, tenant_id, device_id, name, status, priority) VALUES (?, ?, ?, ?, ?, ?)",
        (task_id, test_tenant["id"], test_device["id"], "health_check", "pending", 1),
    )
    test_db_connection.commit()
    return {
        "id": task_id,
        "tenant_id": test_tenant["id"],
        "device_id": test_device["id"],
        "name": "health_check",
        "status": "pending",
    }
