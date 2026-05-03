"""Pydantic models for the API layer."""

from .device import (
    DeviceCreate,
    DeviceInfo,
    DeviceResponse,
    DeviceStatusEnum,
    DeviceUpdate,
)
from .task import (
    TaskCreate,
    TaskPriorityEnum,
    TaskResponse,
    TaskStatusEnum,
    TaskUpdate,
)
from .auth import (
    APIKeyCreate,
    APIKeyResponse,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
    UserRoleEnum,
    UserUpdate,
)
from .common import (
    ErrorResponse,
    HealthResponse,
    PaginationParams,
    PaginatedResponse,
    SuccessResponse,
    TenantCreate,
    TenantResponse,
    TenantUpdate,
)

__all__ = [
    # Device models
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceResponse",
    "DeviceInfo",
    "DeviceStatusEnum",
    # Task models
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskStatusEnum",
    "TaskPriorityEnum",
    # Auth models
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserRoleEnum",
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "APIKeyCreate",
    "APIKeyResponse",
    # Common models
    "ErrorResponse",
    "SuccessResponse",
    "PaginationParams",
    "PaginatedResponse",
    "TenantCreate",
    "TenantUpdate",
    "TenantResponse",
    "HealthResponse",
]
