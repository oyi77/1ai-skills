"""Application configuration from environment variables."""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    jwt_secret: str = field(
        default_factory=lambda: os.environ.get("PHONEFARM_JWT_SECRET", "change-me-in-production")
    )
    server_host: str = field(default_factory=lambda: os.environ.get("PHONEFARM_HOST", "0.0.0.0"))
    server_port: int = field(default_factory=lambda: int(os.environ.get("PHONEFARM_PORT", "8889")))
    debug: bool = field(
        default_factory=lambda: os.environ.get("PHONEFARM_DEBUG", "false").lower() == "true"
    )
    db_path: Path = field(
        default_factory=lambda: Path(os.environ.get("PHONEFARM_DB_PATH", "logs/phone-farm/farm.db"))
    )
    log_level: str = field(default_factory=lambda: os.environ.get("PHONEFARM_LOG_LEVEL", "INFO"))
    workers: int = field(default_factory=lambda: int(os.environ.get("PHONEFARM_WORKERS", "16")))


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get singleton settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
