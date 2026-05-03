"""Tenant isolation middleware for FastAPI.

Extracts tenant_id from JWT token and sets it on request.state.
Public endpoints bypass tenant isolation.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.infrastructure.auth.jwt import JWTHandler

# Public paths that don't require tenant isolation
PUBLIC_PATHS = {
    "/health",
    "/health/ready",
    "/health/live",
    "/auth/login",
    "/auth/register",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
}

jwt_handler = JWTHandler()


class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware that extracts tenant_id from JWT and enforces tenant isolation."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip tenant check for public paths
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # Extract Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Missing or invalid Authorization header"},
            )

        token = auth_header[7:]

        # Verify token and extract tenant_id
        try:
            payload = jwt_handler.verify_token(token)
        except Exception:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid or expired token"},
            )

        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            return JSONResponse(
                status_code=403,
                content={"error": "No tenant_id in token"},
            )

        # Set tenant_id on request state for downstream use
        request.state.tenant_id = tenant_id
        request.state.user_id = payload.get("sub", "")
        request.state.role = payload.get("role", "user")

        return await call_next(request)
