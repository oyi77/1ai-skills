"""Pydantic models for Device API."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DeviceStatusEnum(str, Enum):
    """Device connection status."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    UNKNOWN = "unknown"


class DeviceInfo(BaseModel):
    """Device hardware and software information."""

    model: str = ""
    android_ver: str = ""
    connection: str = "usb"
    battery: int = -1
    screen_on: bool = False
    current_app: str = ""


class DeviceCreate(BaseModel):
    """Request model for creating a device."""

    serial: str = Field(..., min_length=1, max_length=200, description="Device serial number")
    name: str = Field(default="", max_length=100, description="Device friendly name")
    enabled: bool = Field(default=True, description="Whether device is enabled")
    config_json: str = Field(default="{}", description="Device configuration JSON")
    tenant_id: str = Field(default="default", max_length=100, description="Tenant ID")


class DeviceUpdate(BaseModel):
    """Request model for updating a device."""

    name: Optional[str] = Field(default=None, max_length=100, description="Device friendly name")
    enabled: Optional[bool] = Field(default=None, description="Whether device is enabled")
    config_json: Optional[str] = Field(default=None, description="Device configuration JSON")
    status: Optional[DeviceStatusEnum] = Field(default=None, description="Device connection status")
    error_count: Optional[int] = Field(default=None, ge=0, description="Error count")
    last_error: Optional[str] = Field(
        default=None, max_length=500, description="Last error message"
    )


class DeviceResponse(BaseModel):
    """Response model for device."""

    serial: str
    name: str = ""
    status: DeviceStatusEnum = DeviceStatusEnum.UNKNOWN
    info: DeviceInfo = Field(default_factory=DeviceInfo)
    error_count: int = 0
    last_error: str = ""
    last_seen: Optional[datetime] = None
    enabled: bool = True
    config_json: str = "{}"
    tenant_id: str = "default"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
