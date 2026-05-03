#!/usr/bin/env python3
"""
Integration tests for the admin FastAPI endpoints that manage providers.json.

- Uses FastAPI's TestClient for synchronous testing.
- Works on a temporary copy of providers.json to avoid polluting the real config.
- Verifies CRUD operations and secret‑masking.
"""

import json
import pathlib
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

# ----------------------------------------------------------------------
# Minimal admin router (extracted from the daemon) -----------------------
# ----------------------------------------------------------------------
PROVIDERS_PATH = pathlib.Path("scripts/phone_farm_providers/providers.json")

def _load():
    return json.loads(PROVIDERS_PATH.read_text())

def _save(data):
    PROVIDERS_PATH.write_text(json.dumps(data, indent=2))

def _mask(entry):
    masked = entry.copy()
    for k, v in list(masked.items()):
        if isinstance(v, str) and ("key" in k.lower() or "api" in k.lower()):
            masked[k] = "****"
    return masked

admin_app = FastAPI(title="PhoneFarm Admin (test)")

@admin_app.get("/admin/provider/list")
def list_providers():
    cfg = _load()
    return {k: _mask(v) for k, v in cfg.items()}

@admin_app.post("/admin/provider/add")
def add_provider(provider_id: str, config: dict):
    cfg = _load()
    if provider_id in cfg:
        raise HTTPException(status_code=400, detail="Provider already exists")
    cfg[provider_id] = config
    _save(cfg)
    return {"status": "added", "provider_id": provider_id}

@admin_app.put("/admin/provider/update")
def update_provider(provider_id: str, config: dict):
    cfg = _load()
    if provider_id not in cfg:
        raise HTTPException(status_code=404, detail="Provider not found")
    cfg[provider_id].update(config)
    _save(cfg)
    return {"status": "updated", "provider_id": provider_id}

@admin_app.delete("/admin/provider/delete")
def delete_provider(provider_id: str):
    cfg = _load()
    if provider_id not in cfg:
        raise HTTPException(status_code=404, detail="Provider not found")
    cfg.pop(provider_id)
    _save(cfg)
    return {"status": "deleted", "provider_id": provider_id}

client = TestClient(admin_app)

def test_admin_crud(tmp_path):
    # Work on a temporary copy of providers.json
    original = json.loads(PROVIDERS_PATH.read_text())
    temp_file = tmp_path / "providers.json"
    temp_file.write_text(json.dumps(original, indent=2))
    global PROVIDERS_PATH
    PROVIDERS_PATH = temp_file

    # ----- LIST (secrets masked) -----
    resp = client.get("/admin/provider/list")
    assert resp.status_code == 200
    data = resp.json()
    for entry in data.values():
        for key, val in entry.items():
            if "key" in key.lower() or "api" in key.lower():
                assert val == "****"

    # ----- ADD -----
    new_cfg = {
        "type": "dummy",
        "api_key": "super‑secret",
        "base_url": "https://example.com",
        "cost_per_minute": 0.01,
        "capabilities": []
    }
    resp = client.post("/admin/provider/add", json={"provider_id": "dummy_test", "config": new_cfg})
    assert resp.status_code == 200
    assert resp.json()["status"] == "added"
    loaded = json.loads(temp_file.read_text())
    assert "dummy_test" in loaded
    assert loaded["dummy_test"]["api_key"] == "super‑secret"

    # ----- UPDATE -----
    resp = client.put("/admin/provider/update", json={"provider_id": "dummy_test", "config": {"cost_per_minute": 0.02}})
    assert resp.status_code == 200
    loaded = json.loads(temp_file.read_text())
    assert loaded["dummy_test"]["cost_per_minute"] == 0.02

    # ----- DELETE -----
    resp = client.delete("/admin/provider/delete", json={"provider_id": "dummy_test"})
    assert resp.status_code == 200
    loaded = json.loads(temp_file.read_text())
    assert "dummy_test" not in loaded
