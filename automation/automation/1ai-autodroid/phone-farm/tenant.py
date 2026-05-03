#!/usr/bin/env python3
"""
Phone Farm — Tenant Management

Multi-tenant isolation for the SaaS platform.
Each tenant has isolated devices, tasks, alerts, and usage data.
"""

import hashlib
import secrets
import time
import db


def create_tenant(
    tenant_id: str = None, name: str = "", email: str = "", plan: str = "free"
) -> dict:
    if tenant_id is None:
        tenant_id = f"tenant_{secrets.token_hex(8)}"
    conn = db.get_conn()
    now = time.time()
    try:
        conn.execute(
            "INSERT INTO tenants (id, name, email, plan, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tenant_id, name, email, plan, now, now),
        )
        conn.commit()
    except Exception:
        pass
    return get_tenant(tenant_id) or {"id": tenant_id, "name": name, "plan": plan}


def get_tenant(tenant_id: str):
    conn = db.get_conn()
    row = conn.execute(
        "SELECT id, name, email, stripe_customer_id, api_key_hash, plan, rate_limit, "
        "created_at, updated_at FROM tenants WHERE id=?",
        (tenant_id,),
    ).fetchone()
    return dict(row) if row else None


def get_tenant_by_api_key_hash(api_key_hash: str):
    conn = db.get_conn()
    row = conn.execute(
        "SELECT id, name, email, stripe_customer_id, api_key_hash, plan, rate_limit, "
        "created_at, updated_at FROM tenants WHERE api_key_hash=?",
        (api_key_hash,),
    ).fetchone()
    return dict(row) if row else None


def list_tenants() -> list:
    conn = db.get_conn()
    rows = conn.execute(
        "SELECT id, name, email, plan, rate_limit, created_at FROM tenants ORDER BY created_at"
    ).fetchall()
    return [dict(r) for r in rows]


def update_tenant(tenant_id: str, **kwargs) -> bool:
    if not kwargs:
        return False
    kwargs["updated_at"] = time.time()
    cols = ", ".join([f"{k}=excluded.{k}" for k in kwargs.keys()])
    params = list(kwargs.values()) + [tenant_id]
    conn = db.get_conn()
    conn.execute(f"UPDATE tenants SET {cols} WHERE id=?", params)
    conn.commit()
    return True


def delete_tenant(tenant_id: str) -> bool:
    if tenant_id == "default":
        return False
    conn = db.get_conn()
    cursor = conn.execute(
        "DELETE FROM tenants WHERE id=? AND id != 'default'", (tenant_id,)
    )
    conn.commit()
    return cursor.rowcount > 0


def generate_api_key() -> tuple[str, str]:
    """Generate a new API key. Returns (full_key, key_hash)."""
    full_key = f"pf_tenant_{secrets.token_hex(32)}"
    key_hash = hashlib.sha256(full_key.encode("utf-8")).hexdigest()
    return full_key, key_hash


def get_tenant_stats(tenant_id: str) -> dict:
    """Get device/task counts for a tenant."""
    devices_result = db.get_all_devices(tenant_id=tenant_id)
    devices = devices_result["items"]
    tasks_result = db.get_recent_tasks(tenant_id=tenant_id, limit=10000)
    tasks = tasks_result["items"]
    return {
        "devices_total": len(devices),
        "devices_connected": sum(1 for d in devices if d.get("connected")),
        "tasks_total": len(tasks),
        "tasks_ok": sum(1 for t in tasks if t.get("success")),
        "tasks_fail": sum(1 for t in tasks if not t.get("success")),
    }


def init_default_tenant():
    """Ensure default tenant exists."""
    existing = get_tenant("default")
    if not existing:
        create_tenant(
            tenant_id="default",
            name="Default",
            plan="free",
        )


if __name__ == "__main__":
    db.init_db()
    init_default_tenant()
    print("Tenants:", list_tenants())
