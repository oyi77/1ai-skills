"""Domain entity for Task."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskPriority(Enum):
    """Task priority levels."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Task entity representing an automation task execution."""

    id: Optional[int] = None
    serial: str = ""
    device_name: str = ""
    task_type: str = ""
    status: TaskStatus = TaskStatus.PENDING
    success: bool = False
    data_json: str = "{}"
    error: str = ""
    duration_ms: int = 0
    screenshot: str = ""
    ts: Optional[datetime] = None
    ts_str: str = ""
    tenant_id: str = "default"

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
        if self.id is None:
            # Will be set by database
            pass
