#!/usr/bin/env python3
"""
Unit tests for all cloud‑phone provider stubs.

- Uses httpx’s MockTransport to simulate HTTP responses.
- Verifies that each provider correctly parses the mocked JSON payloads.
- Checks that the ProviderFactory loads a provider from providers.json.
- Confirms that placeholder providers (AWS Device Farm, Firebase Test Lab)
  raise NotImplementedError for unimplemented methods.
"""

import json
import pytest
import httpx
from httpx import Response, Request

# Import the provider package (registration happens on import)
from scripts.phone_farm_providers import factory
from scripts.phone_farm_providers.base import DeviceInfo

# ----------------------------------------------------------------------
# Helper to build a mock transport that returns the supplied mapping
# ----------------------------------------------------------------------
def build_transport(mapping: dict[str, Response]) -> httpx.MockTransport:
    def handler(request: Request):
        key = f"{request.method} {request.url.path}"
        return mapping.get(key, Response(404, json={"error": "not found"}))
    return httpx.MockTransport(handler)

# ----------------------------------------------------------------------
# PCloudy Provider ------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_pcloudy_list_devices(monkeypatch):
    mock_json = {
        "deviceList": [
            {
                "deviceId": "pc-001",
                "deviceName": "Pixel 5",
                "deviceModel": "Pixel 5",
                "osVersion": "12",
                "batteryLevel": 85,
                "status": "online",
            }
        ]
    }
    transport = build_transport({"GET /devices": Response(200, json=mock_json)})
    monkeypatch.setattr(
        "scripts.phone_farm_providers.pcloudy_provider.httpx.AsyncClient",
        lambda **kwargs: httpx.AsyncClient(transport=transport, **kwargs),
    )
    from scripts.phone_farm_providers.pcloudy_provider import PCloudyProvider
    cfg = {
        "api_key": "dummy",
        "base_url": "https://api.pcloudy.com",
        "cost_per_minute": 0.02,
        "capabilities": ["adb", "screenshot", "launch"],
    }
    prov = PCloudyProvider(cfg)
    devices = await prov.list_devices()
    assert isinstance(devices, list)
    assert len(devices) == 1
    dev = devices[0]
    assert isinstance(dev, DeviceInfo)
    assert dev.serial == "pc-001"
    assert dev.name == "Pixel 5"
    assert dev.model == "Pixel 5"
    assert dev.os_version == "12"
    assert dev.battery == 85
    assert dev.connected is True
    await prov.close()

# ----------------------------------------------------------------------
# BrowserStack Provider -------------------------------------------------
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_browserstack_list_devices(monkeypatch):
    mock_json = {
        "devices": [
            {"id": "bs-123", "device": "iPhone 13", "os_version": "15.0"}
        ]
    }
    transport = build_transport({"GET /automate/devices.json": Response(200, json=mock_json)})
    monkeypatch.setattr(
        "scripts.phone_farm_providers.browserstack_provider.httpx.AsyncClient",
        lambda **kwargs: httpx.AsyncClient(transport=transport, **kwargs),
    )
    from scripts.phone_farm_providers.browserstack_provider import BrowserStackProvider
    cfg = {
        "username": "user",
        "access_key": "key",
        "base_url": "https://api.browserstack.com",
        "cost_per_minute": 0.07,
        "capabilities": ["adb", "screenshot", "launch"],
    }
    prov = BrowserStackProvider(cfg)
    devices = await prov.list_devices()
    assert len(devices) == 1
    dev = devices[0]
    assert dev.serial == "bs-123"
    assert dev.name == "iPhone 13"
    assert dev.os_version == "15.0"
    await prov.close()

# ----------------------------------------------------------------------
# SauceLabs Provider ----------------------------------------------------
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_saucelabs_list_devices(monkeypatch):
    mock_json = {
        "devices": [
            {"id": "sl-777", "device_name": "Samsung Galaxy S22", "platform_version": "13.0"}
        ]
    }
    transport = build_transport({"GET /v1/ondemand/devices": Response(200, json=mock_json)})
    monkeypatch.setattr(
        "scripts.phone_farm_providers.saucelabs_provider.httpx.AsyncClient",
        lambda **kwargs: httpx.AsyncClient(transport=transport, **kwargs),
    )
    from scripts.phone_farm_providers.saucelabs_provider import SauceLabsProvider
    cfg = {
        "username": "user",
        "access_key": "key",
        "base_url": "https://api.us-west-1.saucelabs.com",
        "cost_per_minute": 0.08,
        "capabilities": ["adb", "screenshot", "launch"],
    }
    prov = SauceLabsProvider(cfg)
    devices = await prov.list_devices()
    assert len(devices) == 1
    dev = devices[0]
    assert dev.serial == "sl-777"
    assert dev.name == "Samsung Galaxy S22"
    assert dev.os_version == "13.0"
    await prov.close()

# ----------------------------------------------------------------------
# Kobiton Provider ------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_kobiton_list_devices(monkeypatch):
    mock_json = {
        "devices": [
            {
                "deviceId": "kb-42",
                "deviceName": "OnePlus 9",
                "deviceModel": "OnePlus 9",
                "osVersion": "12",
                "batteryLevel": 73,
                "status": "ONLINE",
            }
        ]
    }
    transport = build_transport({"GET /v1/devices": Response(200, json=mock_json)})
    monkeypatch.setattr(
        "scripts.phone_farm_providers.kobiton_provider.httpx.AsyncClient",
        lambda **kwargs: httpx.AsyncClient(transport=transport, **kwargs),
    )
    from scripts.phone_farm_providers.kobiton_provider import KobitonProvider
    cfg = {
        "api_key": "dummy",
        "base_url": "https://api.kobiton.com",
        "cost_per_minute": 0.06,
        "capabilities": ["adb", "screenshot", "launch"],
    }
    prov = KobitonProvider(cfg)
    devices = await prov.list_devices()
    assert len(devices) == 1
    dev = devices[0]
    assert dev.serial == "kb-42"
    assert dev.name == "OnePlus 9"
    assert dev.battery == 73
    assert dev.connected is True
    await prov.close()

# ----------------------------------------------------------------------
# LambdaTest Provider ---------------------------------------------------
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_lambdatest_list_devices(monkeypatch):
    mock_json = {
        "devices": [
            {"id": "lt-555", "device": "Google Pixel 6", "os_version": "13.0"}
        ]
    }
    transport = build_transport({"GET /automate/devices.json": Response(200, json=mock_json)})
    monkeypatch.setattr(
        "scripts.phone_farm_providers.lambdatest_provider.httpx.AsyncClient",
        lambda **kwargs: httpx.AsyncClient(transport=transport, **kwargs),
    )
    from scripts.phone_farm_providers.lambdatest_provider import LambdaTestProvider
    cfg = {
        "username": "user",
        "access_key": "key",
        "base_url": "https://api.lambdatest.com",
        "cost_per_minute": 0.07,
        "capabilities": ["adb", "screenshot", "launch"],
    }
    prov = LambdaTestProvider(cfg)
    devices = await prov.list_devices()
    assert len(devices) == 1
    dev = devices[0]
    assert dev.serial == "lt-555"
    assert dev.name == "Google Pixel 6"
    await prov.close()

# ----------------------------------------------------------------------
# Factory loading -------------------------------------------------------
# ----------------------------------------------------------------------
def test_factory_loads_all_providers(tmp_path):
    # Create a temporary providers.json with a subset of entries
    original = json.loads((Path("scripts/phone_farm_providers/providers.json")).read_text())
    subset = {k: original[k] for k in ("pcloudy", "browserstack", "swarmote")}
    temp_file = tmp_path / "providers.json"
    temp_file.write_text(json.dumps(subset, indent=2))

    from scripts.phone_farm_providers import ProviderFactory
    factory = ProviderFactory(config_path=str(temp_file))

    assert factory.get("pcloudy").__class__.__name__ == "PCloudyProvider"
    assert factory.get("browserstack").__class__.__name__ == "BrowserStackProvider"
    assert factory.get("swarmote").__class__.__name__ == "SwarmoteProvider"

# ----------------------------------------------------------------------
# Placeholder providers (AWS Device Farm, Firebase Test Lab) -------------
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_placeholder_providers_raise():
    from scripts.phone_farm_providers.aws_devicefarm_provider import AWSDeviceFarmProvider
    from scripts.phone_farm_providers.firebase_testlab_provider import FirebaseTestLabProvider

    aws_cfg = {"aws_access_key_id": "id", "aws_secret_access_key": "secret", "region": "us-west-2"}
    fb_cfg = {"api_key": "dummy", "base_url": "https://testing.googleapis.com/v1"}

    aws = AWSDeviceFarmProvider(aws_cfg)
    fb = FirebaseTestLabProvider(fb_cfg)

    with pytest.raises(NotImplementedError):
        await aws.list_devices()
    with pytest.raises(NotImplementedError):
        await fb.list_devices()

    await aws.close()
    await fb.close()
