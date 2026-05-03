"""Pydantic models for common API responses."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(..., description="Error message")
    code: str = Field(default="internal_error", description="Error code")
    details: Optional[Any] = Field(default=None, description="Additional error details")
    request_id: Optional[str] = Field(default=None, description="Request ID for debugging")


class SuccessResponse(BaseModel):
    """Standard success response model."""

    message: str
    data: Optional[Any] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""

    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class TenantCreate(BaseModel):
    """Request model for creating a tenant."""

    name: str = Field(..., min_length=1, max_length=100, description="Tenant name")
    email: str = Field(..., max_length=255, description="Tenant email")


class TenantUpdate(BaseModel):
    """Request model for updating a tenant."""

    name: Optional[str] = Field(default=None, max_length=100, description="Tenant name")
    email: Optional[str] = Field(default=None, max_length=255, description="Tenant email")
    plan: Optional[str] = Field(default=None, max_length=50, description="Subscription plan")
    rate_limit: Optional[float] = Field(default=None, ge=1, description="Rate limit per minute")


class TenantResponse(BaseModel):
    """Response model for tenant."""

    id: str
    name: str = ""
    email: str = ""
    plan: str = "free"
    rate_limit: float = 100.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
