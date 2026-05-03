"""Task repository for task entity persistence."""

import json
from datetime import datetime
from typing import Any, Optional

import aiosqlite

from src.domain.entities.task import Task, TaskStatus
from src.infrastructure.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entity operations."""

    def __init__(self, db: aiosqlite.Connection):
        super().__init__(db, table="tasks", pk_column="id")

    def to_entity(self, row: dict[str, Any]) -> Task:
        """Convert database row to Task entity."""
        # Infer status from success field
        success = bool(row.get("success", 0))
        if success:
            status = TaskStatus.SUCCESS
        else:
            # Check if there's an error to determine failed vs pending
            error = row.get("error", "")
            status = TaskStatus.FAILED if error else TaskStatus.PENDING

        return Task(
            id=row.get("id"),
            serial=row.get("serial", ""),
            device_name=row.get("device_name", ""),
            task_type=row.get("task_type", ""),
            status=status,
            success=success,
            data_json=row.get("data_json", "{}"),
            error=row.get("error", ""),
            duration_ms=row.get("duration_ms", 0),
            screenshot=row.get("screenshot", ""),
            ts=self._parse_datetime(row.get("ts")),
            ts_str=row.get("ts_str", ""),
            tenant_id=row.get("tenant_id", "default"),
        )

    def from_entity(self, task: Task) -> dict[str, Any]:
        """Convert Task entity to database row dict."""
        data = {
            "serial": task.serial,
            "device_name": task.device_name,
            "task_type": task.task_type,
            "success": 1 if task.success else 0,
            "data_json": task.data_json
            if isinstance(task.data_json, str)
            else json.dumps(task.data_json),
            "error": task.error,
            "duration_ms": task.duration_ms,
            "screenshot": task.screenshot,
            "ts": task.ts.timestamp() if task.ts else datetime.now().timestamp(),
            "ts_str": task.ts_str
            or (
                task.ts.strftime("%Y-%m-%d %H:%M:%S")
                if task.ts
                else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            "tenant_id": task.tenant_id,
        }
        if task.id is not None:
            data["id"] = task.id
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

    async def get_by_id(self, task_id: int, tenant_id: str = None) -> Optional[Task]:
        """Get task by ID with optional tenant isolation."""
        row = await self.get(task_id)
        if row and tenant_id and row.get("tenant_id") != tenant_id:
            return None
        return self.to_entity(row) if row else None

    async def list_by_tenant(self, tenant_id: str, limit: int = 100, offset: int = 0) -> list[Task]:
        """List all tasks for a specific tenant."""
        rows = await self.get_all(
            where="tenant_id = ?",
            params=[tenant_id],
            order_by="ts DESC",
            limit=limit,
            offset=offset,
        )
        return [self.to_entity(row) for row in rows]

    async def update_status(self, task_id: int, status: TaskStatus, tenant_id: str = None) -> bool:
        """Update task status by ID."""
        # Check tenant isolation if tenant_id provided
        if tenant_id:
            task = await self.get_by_id(task_id, tenant_id)
            if not task:
                return False

        # Map status to success bool
        success = status in (TaskStatus.SUCCESS, TaskStatus.RUNNING)
        return await self.update(task_id, {"success": 1 if success else 0})

    async def list_by_device(
        self, serial: str, tenant_id: str = None, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        """List all tasks for a specific device."""
        if tenant_id:
            rows = await self.get_all(
                where="serial = ? AND tenant_id = ?",
                params=[serial, tenant_id],
                order_by="ts DESC",
                limit=limit,
                offset=offset,
            )
        else:
            rows = await self.get_all(
                where="serial = ?",
                params=[serial],
                order_by="ts DESC",
                limit=limit,
                offset=offset,
            )
        return [self.to_entity(row) for row in rows]

    async def list_all(
        self, tenant_id: str = None, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        """List all tasks, optionally filtered by tenant."""
        if tenant_id:
            return await self.list_by_tenant(tenant_id, limit, offset)

        rows = await self.get_all(
            order_by="ts DESC",
            limit=limit,
            offset=offset,
        )
        return [self.to_entity(row) for row in rows]
