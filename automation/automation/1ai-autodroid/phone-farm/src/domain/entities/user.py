"""Domain entity for User."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(Enum):
    """User role levels."""

    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


@dataclass
class User:
    """User entity representing a system user."""

    id: Optional[str] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    role: UserRole = UserRole.USER
    tenant_id: str = "default"
    api_key_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.role, str):
            self.role = UserRole(self.role)
