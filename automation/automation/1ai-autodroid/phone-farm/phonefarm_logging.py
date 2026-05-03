#!/usr/bin/env python3
"""
Phone Farm Structured Logging Module

Provides JSON-formatted logging to file with human-readable console output.
"""

import json
import logging
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs as JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra context fields (context dict)
        if hasattr(record, "context") and record.context:
            log_entry["context"] = record.context

        # Add any other extra fields
        for key, value in record.__dict__.items():
            if key not in (
                "args",
                "exc_info",
                "exc_text",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "msg",
                "created",
                "funcName",
                "message",
                "context",
            ):
                if not key.startswith("_"):
                    log_entry[key] = value

        return json.dumps(log_entry, default=str)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter for console output."""

    def __init__(self):
        super().__init__(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def setup_logger(
    name: str = "phone-farm",
    log_dir: Path | None = None,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Set up a logger with both console and JSON file handlers.

    Args:
        name: Logger name
        log_dir: Directory for log files (defaults to logs/phone-farm/)
        console_level: Logging level for console output
        file_level: Logging level for file output
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured logger instance
    """
    # Determine log directory
    if log_dir is None:
        base_path = Path(__file__).parent.parent
        log_dir = base_path / "logs" / "phone-farm"

    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)

    # Get or create logger
    logger = logging.getLogger(name)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Set overall level
    logger.setLevel(logging.DEBUG)

    # Console handler - human-readable output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(HumanReadableFormatter())
    logger.addHandler(console_handler)

    # File handler - JSON output with rotation
    log_file = log_dir / "app.log"
    file_handler = RotatingFileHandler(
        log_file,
        mode="a",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "phone-farm") -> logging.Logger:
    """
    Get or create a logger instance.

    Args:
        name: Logger name (can include context like "phone-farm.device")

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        return setup_logger(name)

    return logger


# Convenience function for logging with context
def log_with_context(
    logger: logging.Logger,
    level: int,
    message: str,
    context: dict[str, Any] | None = None,
    **extra,
) -> None:
    """
    Log a message with additional context.

    Args:
        logger: Logger instance
        level: Logging level (logging.INFO, logging.ERROR, etc.)
        message: Log message
        context: Additional context dictionary
        **extra: Additional extra fields
    """
    extra["context"] = context or {}

    # Create a LogRecord with the extra context
    # Using standard logging's _log method
    logger.log(level, message, extra=extra)


# Export common logging functions at module level
def debug(
    logger: logging.Logger, message: str, context: dict[str, Any] | None = None, **extra
):
    log_with_context(logger, logging.DEBUG, message, context, **extra)


def info(
    logger: logging.Logger, message: str, context: dict[str, Any] | None = None, **extra
):
    log_with_context(logger, logging.INFO, message, context, **extra)


def warning(
    logger: logging.Logger, message: str, context: dict[str, Any] | None = None, **extra
):
    log_with_context(logger, logging.WARNING, message, context, **extra)


def error(
    logger: logging.Logger, message: str, context: dict[str, Any] | None = None, **extra
):
    log_with_context(logger, logging.ERROR, message, context, **extra)


def critical(
    logger: logging.Logger, message: str, context: dict[str, Any] | None = None, **extra
):
    log_with_context(logger, logging.CRITICAL, message, context, **extra)
