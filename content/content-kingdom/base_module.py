"""
base_module.py — Dependency Inversion foundation for Content Kingdom.

Every phase module inherits BaseModule and implements run().
Orchestrator depends on this abstraction, not concrete implementations.

SOLID: D — Depend on abstractions.
KISS: Minimal interface. run() in, PhaseResult out. That's it.
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PhaseStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PhaseResult:
    """Standardised output from any phase module."""

    phase: str
    status: PhaseStatus
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_seconds: float = 0.0
    timestamp: str = ""

    def succeeded(self) -> bool:
        return self.status == PhaseStatus.SUCCESS

    def to_dict(self) -> dict:
        return {
            "phase": self.phase,
            "status": self.status.value,
            "data": self.data,
            "error": self.error,
            "duration_seconds": round(self.duration_seconds, 2),
            "timestamp": self.timestamp,
        }


class BaseModule(ABC):
    """
    Abstract base for all Content Kingdom phase modules.

    Contract:
    - __init__ accepts config dict
    - run(**kwargs) returns PhaseResult
    - name property returns phase identifier
    """

    def __init__(self, config: dict):
        self.config = config
        self.log = logging.getLogger(self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        """Phase identifier, e.g. 'research', 'schedule'."""
        ...

    @abstractmethod
    def _execute(self, **kwargs) -> dict[str, Any]:
        """Core logic. Return a data dict on success. Raise on failure."""
        ...

    def run(self, **kwargs) -> PhaseResult:
        """
        Wraps _execute with timing, error handling, logging.
        Do NOT override this in subclasses.
        """
        import datetime

        start = time.monotonic()
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.log.info("▶ Phase [%s] starting", self.name)

        try:
            data = self._execute(**kwargs)
            elapsed = time.monotonic() - start
            self.log.info("✅ Phase [%s] completed in %.1fs", self.name, elapsed)
            return PhaseResult(
                phase=self.name,
                status=PhaseStatus.SUCCESS,
                data=data or {},
                duration_seconds=elapsed,
                timestamp=ts,
            )
        except Exception as exc:  # noqa: BLE001
            elapsed = time.monotonic() - start
            self.log.error("❌ Phase [%s] failed: %s", self.name, exc, exc_info=True)
            return PhaseResult(
                phase=self.name,
                status=PhaseStatus.FAILED,
                error=str(exc),
                duration_seconds=elapsed,
                timestamp=ts,
            )
