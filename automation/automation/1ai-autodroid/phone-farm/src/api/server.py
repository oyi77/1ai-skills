"""FastAPI application factory."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.config import get_settings
from src.infrastructure.database.connection import init_db, close_db
from src.api.middleware.tenant import TenantMiddleware
from src.api.routes.devices import router as devices_router
from src.api.routes.tasks import router as tasks_router
from src.api.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    await init_db()
    yield
    await close_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Phone Farm API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Tenant isolation
    app.add_middleware(TenantMiddleware)

    # Health endpoint
    @app.get("/health")
    async def health():
        return {"status": "ok"}

    # Exception handlers
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc) if settings.debug else None,
            },
        )

    # Register routers
    app.include_router(devices_router, prefix="/api/v1")
    app.include_router(tasks_router, prefix="/api/v1")
    app.include_router(auth_router)

    return app
