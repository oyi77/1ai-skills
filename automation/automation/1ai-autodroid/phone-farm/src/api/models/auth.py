"""Pydantic models for Auth API."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRoleEnum(str, Enum):
    """User role levels."""

    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class UserCreate(BaseModel):
    """Request model for creating a user."""

    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password")
    role: UserRoleEnum = Field(default=UserRoleEnum.USER, description="User role")
    tenant_id: str = Field(default="default", max_length=100, description="Tenant ID")


class UserUpdate(BaseModel):
    """Request model for updating a user."""

    username: Optional[str] = Field(
        default=None, min_length=3, max_length=50, description="Username"
    )
    email: Optional[EmailStr] = Field(default=None, description="Email address")
    password: Optional[str] = Field(
        default=None, min_length=8, max_length=100, description="Password"
    )
    role: Optional[UserRoleEnum] = Field(default=None, description="User role")


class UserResponse(BaseModel):
    """Response model for user."""

    id: Optional[str] = None
    username: str = ""
    email: str = ""
    role: UserRoleEnum = UserRoleEnum.USER
    tenant_id: str = "default"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Request model for login."""

    username: str = Field(..., min_length=1, description="Username or email")
    password: str = Field(..., min_length=1, description="Password")


class TokenResponse(BaseModel):
    """Response model for authentication token."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Request model for token refresh."""

    refresh_token: str = Field(..., description="Refresh token")


class APIKeyCreate(BaseModel):
    """Request model for creating API key."""

    name: str = Field(..., min_length=1, max_length=100, description="API key name")
    expires_in_days: int = Field(default=30, ge=1, le=365, description="Days until expiration")


class APIKeyResponse(BaseModel):
    """Response model for API key."""

    id: str
    name: str
    key: str
    expires_at: Optional[datetime] = None
    created_at: datetime
