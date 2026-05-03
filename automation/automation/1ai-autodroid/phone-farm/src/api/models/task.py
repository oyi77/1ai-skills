"""Pydantic models for Task API."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatusEnum(str, Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskPriorityEnum(int, Enum):
    """Task priority levels."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TaskCreate(BaseModel):
    """Request model for creating a task."""

    serial: str = Field(..., min_length=1, max_length=200, description="Device serial number")
    device_name: str = Field(default="", max_length=100, description="Device name")
    task_type: str = Field(..., min_length=1, max_length=50, description="Task type")
    priority: TaskPriorityEnum = Field(default=TaskPriorityEnum.NORMAL, description="Task priority")
    data_json: str = Field(default="{}", description="Task data JSON")
    tenant_id: str = Field(default="default", max_length=100, description="Tenant ID")


class TaskUpdate(BaseModel):
    """Request model for updating a task."""

    status: Optional[TaskStatusEnum] = Field(default=None, description="Task execution status")
    success: Optional[bool] = Field(default=None, description="Task success flag")
    error: Optional[str] = Field(default=None, max_length=1000, description="Error message")
    duration_ms: Optional[int] = Field(default=None, ge=0, description="Execution duration in ms")
    screenshot: Optional[str] = Field(default=None, description="Screenshot path")


class TaskResponse(BaseModel):
    """Response model for task."""

    id: Optional[int] = None
    serial: str = ""
    device_name: str = ""
    task_type: str = ""
    status: TaskStatusEnum = TaskStatusEnum.PENDING
    success: bool = False
    data_json: str = "{}"
    error: str = ""
    duration_ms: int = 0
    screenshot: str = ""
    ts: Optional[datetime] = None
    ts_str: str = ""
    tenant_id: str = "default"

    class Config:
        from_attributes = True
