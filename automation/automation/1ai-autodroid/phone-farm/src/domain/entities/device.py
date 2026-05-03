"""Domain entity for Device."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class DeviceStatus(Enum):
    """Device connection status."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class DeviceInfo:
    """Device hardware and software information."""

    model: str = ""
    android_ver: str = ""
    connection: str = "usb"  # usb or wireless
    battery: int = -1
    screen_on: bool = False
    current_app: str = ""


@dataclass
class Device:
    """Device entity representing an Android device in the farm."""

    serial: str
    name: str = ""
    status: DeviceStatus = DeviceStatus.UNKNOWN
    info: DeviceInfo = field(default_factory=DeviceInfo)
    error_count: int = 0
    last_error: str = ""
    last_seen: Optional[datetime] = None
    enabled: bool = True
    config_json: str = "{}"
    tenant_id: str = "default"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = DeviceStatus(self.status)
        if isinstance(self.info, dict):
            self.info = DeviceInfo(**self.info)
