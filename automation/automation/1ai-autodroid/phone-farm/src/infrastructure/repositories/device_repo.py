"""Device repository for device entity persistence."""

from datetime import datetime
from typing import Any, Optional

import aiosqlite

from src.domain.entities.device import Device, DeviceInfo, DeviceStatus
from src.infrastructure.repositories.base import BaseRepository


class DeviceRepository(BaseRepository[Device]):
    """Repository for Device entity operations."""

    def __init__(self, db: aiosqlite.Connection):
        super().__init__(db, table="devices", pk_column="serial")

    def to_entity(self, row: dict[str, Any]) -> Device:
        """Convert database row to Device entity."""
        return Device(
            serial=row.get("serial", ""),
            name=row.get("name", ""),
            status=DeviceStatus(row.get("status", "unknown")),
            info=DeviceInfo(
                model=row.get("model", ""),
                android_ver=row.get("android_ver", ""),
                connection=row.get("connection", "usb"),
                battery=row.get("battery", -1),
                screen_on=bool(row.get("screen_on", 0)),
                current_app=row.get("current_app", ""),
            ),
            error_count=row.get("error_count", 0),
            last_error=row.get("last_error", ""),
            last_seen=self._parse_datetime(row.get("last_seen")),
            enabled=bool(row.get("enabled", 1)),
            config_json=row.get("config_json", "{}"),
            tenant_id=row.get("tenant_id", "default"),
            created_at=self._parse_datetime(row.get("created_at")),
            updated_at=self._parse_datetime(row.get("updated_at")),
        )

    def from_entity(self, device: Device) -> dict[str, Any]:
        """Convert Device entity to database row dict."""
        data = {
            "serial": device.serial,
            "name": device.name,
            "status": device.status.value,
            "model": device.info.model,
            "android_ver": device.info.android_ver,
            "connection": device.info.connection,
            "battery": device.info.battery,
            "screen_on": 1 if device.info.screen_on else 0,
            "current_app": device.info.current_app,
            "error_count": device.error_count,
            "last_error": device.last_error,
            "last_seen": device.last_seen.isoformat() if device.last_seen else None,
            "enabled": 1 if device.enabled else 0,
            "config_json": device.config_json,
            "tenant_id": device.tenant_id,
            "created_at": device.created_at.isoformat() if device.created_at else None,
            "updated_at": device.updated_at.isoformat() if device.updated_at else None,
        }
        return {k: v for k, v in data.items() if v is not None}

    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse datetime from database value."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None

    async def get_by_serial(self, serial: str, tenant_id: str = None) -> Optional[Device]:
        """Get device by serial number with optional tenant isolation."""
        row = await self.get(serial)
        if row and tenant_id and row.get("tenant_id") != tenant_id:
            return None
        return self.to_entity(row) if row else None

    async def list_by_tenant(
        self, tenant_id: str, limit: int = 100, offset: int = 0
    ) -> list[Device]:
        """List all devices for a specific tenant."""
        rows = await self.get_all(
            where="tenant_id = ?",
            params=[tenant_id],
            order_by="name ASC",
            limit=limit,
            offset=offset,
        )
        return [self.to_entity(row) for row in rows]

    async def update_status(self, serial: str, status: DeviceStatus, tenant_id: str = None) -> bool:
        """Update device status."""
        # Check tenant isolation if tenant_id provided
        if tenant_id:
            device = await self.get_by_serial(serial, tenant_id)
            if not device:
                return False

        return await self.update(serial, {"status": status.value})

    async def list_all(
        self, tenant_id: str = None, limit: int = 100, offset: int = 0
    ) -> list[Device]:
        """List all devices, optionally filtered by tenant."""
        if tenant_id:
            return await self.list_by_tenant(tenant_id, limit, offset)

        rows = await self.get_all(
            order_by="name ASC",
            limit=limit,
            offset=offset,
        )
        return [self.to_entity(row) for row in rows]
