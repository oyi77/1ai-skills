"""
Self-Healing System
===================

Detects failures in automated pipelines, applies recovery strategies
with exponential backoff, and escalates to humans when retries exhaust.

Recovery strategies:
  - restart_module: Re-import and re-execute a failed Python module
  - reset_connection: Clear cached connections (DB, API, broker)
  - clear_cache: Remove stale cache/lock files that block execution
  - restart_cron: Reinstall crontab entries for a stuck scheduler

All recovery attempts are logged to logs/recovery.log.
Integrates with Notifier for alert escalation.
"""

import importlib
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

LOGS_DIR = WORKSPACE_ROOT / "logs"
RECOVERY_LOG = LOGS_DIR / "recovery.log"
RECOVERY_STATE_FILE = LOGS_DIR / "recovery_state.json"

MAX_RETRIES = 3
BASE_DELAY_SECONDS = 2.0
MAX_DELAY_SECONDS = 30.0


# ─────────────────────────────────────────────────────────────────────────────
# Enums & Data Classes
# ─────────────────────────────────────────────────────────────────────────────


class FailureType(Enum):
    """Categories of detectable failures."""

    MODULE_CRASH = "module_crash"
    CONNECTION_ERROR = "connection_error"
    TIMEOUT = "timeout"
    DEPENDENCY_MISSING = "dependency_missing"
    CRON_STALLED = "cron_stalled"
    CACHE_CORRUPTION = "cache_corruption"
    UNKNOWN = "unknown"


class RecoveryStrategy(Enum):
    """Available automatic recovery strategies."""

    RESTART_MODULE = "restart_module"
    RESET_CONNECTION = "reset_connection"
    CLEAR_CACHE = "clear_cache"
    RESTART_CRON = "restart_cron"
    ESCALATE = "escalate"


class RecoveryStatus(Enum):
    """Outcome of a recovery attempt."""

    SUCCESS = "success"
    FAILED = "failed"
    ESCALATED = "escalated"


@dataclass
class FailureEvent:
    """Represents a detected failure."""

    job_id: str
    failure_type: FailureType
    error_message: str
    timestamp: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class RecoveryAttempt:
    """Record of a single recovery attempt."""

    job_id: str
    attempt_number: int
    strategy: RecoveryStrategy
    status: RecoveryStatus
    message: str
    duration_seconds: float
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class RecoveryResult:
    """Final outcome after all recovery attempts."""

    job_id: str
    failure: FailureEvent
    attempts: List[RecoveryAttempt]
    resolved: bool
    final_status: RecoveryStatus
    total_duration_seconds: float


# ─────────────────────────────────────────────────────────────────────────────
# Logger setup
# ─────────────────────────────────────────────────────────────────────────────


def _setup_recovery_logger() -> logging.Logger:
    """Create a logger that writes to console and recovery_debug.log."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("self_healing")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        debug_log = LOGS_DIR / "recovery_debug.log"
        fh = logging.FileHandler(str(debug_log))
        fh.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
        )
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(ch)

    return logger


logger = _setup_recovery_logger()


# ─────────────────────────────────────────────────────────────────────────────
# Strategy → Failure Type mapping
# ─────────────────────────────────────────────────────────────────────────────

FAILURE_STRATEGY_MAP: Dict[FailureType, List[RecoveryStrategy]] = {
    FailureType.MODULE_CRASH: [
        RecoveryStrategy.RESTART_MODULE,
        RecoveryStrategy.CLEAR_CACHE,
    ],
    FailureType.CONNECTION_ERROR: [
        RecoveryStrategy.RESET_CONNECTION,
        RecoveryStrategy.RESTART_MODULE,
    ],
    FailureType.TIMEOUT: [
        RecoveryStrategy.RESTART_MODULE,
        RecoveryStrategy.RESET_CONNECTION,
    ],
    FailureType.DEPENDENCY_MISSING: [
        RecoveryStrategy.CLEAR_CACHE,
        RecoveryStrategy.RESTART_MODULE,
    ],
    FailureType.CRON_STALLED: [
        RecoveryStrategy.RESTART_CRON,
        RecoveryStrategy.RESTART_MODULE,
    ],
    FailureType.CACHE_CORRUPTION: [
        RecoveryStrategy.CLEAR_CACHE,
        RecoveryStrategy.RESTART_MODULE,
    ],
    FailureType.UNKNOWN: [
        RecoveryStrategy.RESTART_MODULE,
        RecoveryStrategy.CLEAR_CACHE,
        RecoveryStrategy.RESET_CONNECTION,
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# SelfHealing class
# ─────────────────────────────────────────────────────────────────────────────


class SelfHealing:
    """
    Detects pipeline failures and applies recovery strategies with
    exponential backoff.  Escalates to human via Notifier when retries
    are exhausted.

    Usage::

        healer = SelfHealing()

        # Option A: handle a known failure
        result = healer.handle_failure(
            job_id="content_pipeline",
            failure_type=FailureType.MODULE_CRASH,
            error_message="ImportError: No module named 'skills.content'",
        )

        # Option B: scan cron execution log for recent failures
        results = healer.scan_and_heal()
    """

    def __init__(
        self,
        max_retries: int = MAX_RETRIES,
        base_delay: float = BASE_DELAY_SECONDS,
        notify_channel: str = "telegram",
        notify_recipient: Optional[str] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.notify_channel = notify_channel
        self.notify_recipient = notify_recipient or os.environ.get(
            "TELEGRAM_CHAT_ID", ""
        )
        self._notifier: Optional[Any] = None

    # ------------------------------------------------------------------
    # Notifier integration (lazy-loaded)
    # ------------------------------------------------------------------

    @property
    def notifier(self):
        """Lazily import Notifier to avoid hard circular deps."""
        if self._notifier is None:
            try:
                from skills.task_manager.notifier import Notifier

                self._notifier = Notifier()
            except ImportError:
                logger.warning("Notifier not available — alerts will be logged only")
        return self._notifier

    # ------------------------------------------------------------------
    # Failure detection
    # ------------------------------------------------------------------

    @staticmethod
    def classify_failure(error_message: str) -> FailureType:
        """Classify an error message into a FailureType."""
        msg = error_message.lower()

        if any(kw in msg for kw in ("import", "module", "attributeerror")):
            return FailureType.MODULE_CRASH
        if any(
            kw in msg
            for kw in ("connection", "refused", "timeout", "unreachable", "socket")
        ):
            return FailureType.CONNECTION_ERROR
        if "timeout" in msg or "timed out" in msg:
            return FailureType.TIMEOUT
        if any(kw in msg for kw in ("not found", "missing", "no such file")):
            return FailureType.DEPENDENCY_MISSING
        if any(kw in msg for kw in ("cron", "scheduler", "stalled")):
            return FailureType.CRON_STALLED
        if any(kw in msg for kw in ("cache", "corrupt", "decode", "json")):
            return FailureType.CACHE_CORRUPTION
        return FailureType.UNKNOWN

    def detect_failures_from_log(self) -> List[FailureEvent]:
        """
        Scan the cron execution log for recent failures.

        Reads ``logs/cron/execution_log.json`` written by CronScheduler
        and returns FailureEvent objects for each unsuccessful entry that
        has not already been handled.
        """
        exec_log = WORKSPACE_ROOT / "logs" / "cron" / "execution_log.json"
        if not exec_log.exists():
            return []

        try:
            with open(exec_log) as f:
                entries = json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning("Could not read execution log")
            return []

        handled = self._load_handled_ids()

        failures: List[FailureEvent] = []
        for entry in entries:
            if entry.get("success"):
                continue
            entry_key = f"{entry.get('job_id')}:{entry.get('timestamp', '')}"
            if entry_key in handled:
                continue

            error_msg = entry.get("error", "Unknown error")
            failures.append(
                FailureEvent(
                    job_id=entry.get("job_id", "unknown"),
                    failure_type=self.classify_failure(error_msg),
                    error_message=error_msg,
                    timestamp=entry.get("timestamp", ""),
                    context={"source": "execution_log", "entry_key": entry_key},
                )
            )

        return failures

    # ------------------------------------------------------------------
    # Recovery strategies
    # ------------------------------------------------------------------

    def _strategy_restart_module(self, failure: FailureEvent) -> bool:
        """
        Attempt to re-import the failed module.

        This clears the module from sys.modules and re-imports it.
        Does NOT re-execute — only validates the module loads cleanly.
        """
        job_id = failure.job_id
        logger.info(f"[{job_id}] Strategy: restart_module")


        jobs_file = WORKSPACE_ROOT / "automation" / "jobs.json"
        module_path = None
        if jobs_file.exists():
            try:
                with open(jobs_file) as f:
                    config = json.load(f)
                for job in config.get("jobs", []):
                    if job["id"] == job_id and job.get("module"):
                        module_path = job["module"]
                        break
            except (json.JSONDecodeError, KeyError):
                pass

        if not module_path:
            logger.warning(f"[{job_id}] No module path found — cannot restart")
            return False


        try:
            if module_path in sys.modules:
                del sys.modules[module_path]
                logger.info(f"[{job_id}] Cleared cached module: {module_path}")

            importlib.import_module(module_path)
            logger.info(f"[{job_id}] Module re-imported successfully: {module_path}")
            return True
        except Exception as exc:
            logger.error(f"[{job_id}] restart_module failed: {exc}")
            return False

    def _strategy_reset_connection(self, failure: FailureEvent) -> bool:
        """
        Reset cached network connections.

        Clears urllib/requests connection pools and resets environment
        proxies.  Safe and non-destructive.
        """
        job_id = failure.job_id
        logger.info(f"[{job_id}] Strategy: reset_connection")

        try:

            import urllib.request

            urllib.request.install_opener(urllib.request.build_opener())
            logger.info(f"[{job_id}] urllib opener reset")


            try:
                import requests

                requests.Session().close()
                logger.info(f"[{job_id}] requests session closed")
            except ImportError:
                pass


            try:
                import socket

                socket.getaddrinfo.cache_clear()  # type: ignore[attr-defined]
            except (AttributeError, TypeError):
                pass

            logger.info(f"[{job_id}] Connection state reset complete")
            return True
        except Exception as exc:
            logger.error(f"[{job_id}] reset_connection failed: {exc}")
            return False

    def _strategy_clear_cache(self, failure: FailureEvent) -> bool:
        """
        Remove stale cache and lock files that may block execution.

        Targets: __pycache__, .pyc files, lock files in automation dir.
        Does NOT touch production data.
        """
        job_id = failure.job_id
        logger.info(f"[{job_id}] Strategy: clear_cache")

        cleared = 0
        try:
            automation_dir = WORKSPACE_ROOT / "automation"


            for pycache in automation_dir.rglob("__pycache__"):
                if pycache.is_dir():
                    import shutil

                    shutil.rmtree(pycache, ignore_errors=True)
                    cleared += 1
                    logger.info(f"[{job_id}] Removed: {pycache}")


            for lock_file in automation_dir.rglob("*.lock"):
                lock_file.unlink(missing_ok=True)
                cleared += 1
                logger.info(f"[{job_id}] Removed lock: {lock_file}")


            logs_dir = WORKSPACE_ROOT / "logs"
            if logs_dir.exists():
                for tmp_file in logs_dir.rglob("*.tmp"):
                    tmp_file.unlink(missing_ok=True)
                    cleared += 1

            logger.info(f"[{job_id}] Cleared {cleared} cache/lock items")
            return True
        except Exception as exc:
            logger.error(f"[{job_id}] clear_cache failed: {exc}")
            return False

    def _strategy_restart_cron(self, failure: FailureEvent) -> bool:
        """
        Reinstall crontab entries via CronScheduler.

        This re-reads jobs.json and regenerates the system crontab.
        Safe: uses the marker-based install from cron_setup.py.
        """
        job_id = failure.job_id
        logger.info(f"[{job_id}] Strategy: restart_cron")

        try:
            from automation.cron_setup import CronScheduler

            scheduler = CronScheduler()
            result = scheduler.install_crontab()

            if result.get("success"):
                logger.info(f"[{job_id}] Crontab reinstalled successfully")
                return True
            else:
                logger.error(
                    f"[{job_id}] Crontab install failed: {result.get('error')}"
                )
                return False
        except Exception as exc:
            logger.error(f"[{job_id}] restart_cron failed: {exc}")
            return False

    # Map strategy enum to implementation
    def _get_strategy_fn(
        self, strategy: RecoveryStrategy
    ) -> Optional[Callable[[FailureEvent], bool]]:
        """Return the implementation function for a strategy."""
        mapping: Dict[RecoveryStrategy, Callable[[FailureEvent], bool]] = {
            RecoveryStrategy.RESTART_MODULE: self._strategy_restart_module,
            RecoveryStrategy.RESET_CONNECTION: self._strategy_reset_connection,
            RecoveryStrategy.CLEAR_CACHE: self._strategy_clear_cache,
            RecoveryStrategy.RESTART_CRON: self._strategy_restart_cron,
        }
        return mapping.get(strategy)

    # ------------------------------------------------------------------
    # Core healing loop
    # ------------------------------------------------------------------

    def _calculate_delay(self, attempt: int) -> float:
        """Exponential backoff: base * 2^attempt, capped at MAX_DELAY."""
        delay = self.base_delay * (2**attempt)
        return min(delay, MAX_DELAY_SECONDS)

    def handle_failure(
        self,
        job_id: str,
        failure_type: Optional[FailureType] = None,
        error_message: str = "",
    ) -> RecoveryResult:
        """
        Handle a single failure with retry + exponential backoff.

        Tries up to ``max_retries`` recovery strategies.  Each attempt
        uses the next strategy in the priority list for the failure type.
        If all retries fail, escalates via Notifier.

        Args:
            job_id: Identifier of the failed job.
            failure_type: Category (auto-classified from error if None).
            error_message: Raw error string.

        Returns:
            RecoveryResult with full attempt history.
        """
        if failure_type is None:
            failure_type = self.classify_failure(error_message)

        failure = FailureEvent(
            job_id=job_id,
            failure_type=failure_type,
            error_message=error_message,
        )

        logger.info(
            f"[{job_id}] Failure detected: {failure_type.value} — {error_message[:120]}"
        )

        strategies = FAILURE_STRATEGY_MAP.get(failure_type, [])
        attempts: List[RecoveryAttempt] = []
        start_time = time.time()
        resolved = False

        for attempt_num in range(1, self.max_retries + 1):

            strategy = (
                strategies[(attempt_num - 1) % len(strategies)]
                if strategies
                else RecoveryStrategy.RESTART_MODULE
            )


            if attempt_num > 1:
                delay = self._calculate_delay(attempt_num - 1)
                logger.info(
                    f"[{job_id}] Waiting {delay:.1f}s before attempt {attempt_num}..."
                )
                time.sleep(delay)

            logger.info(
                f"[{job_id}] Attempt {attempt_num}/{self.max_retries} "
                f"— strategy: {strategy.value}"
            )

            attempt_start = time.time()
            strategy_fn = self._get_strategy_fn(strategy)

            if strategy_fn is None:

                attempt = RecoveryAttempt(
                    job_id=job_id,
                    attempt_number=attempt_num,
                    strategy=strategy,
                    status=RecoveryStatus.FAILED,
                    message=f"No implementation for strategy: {strategy.value}",
                    duration_seconds=0.0,
                )
                attempts.append(attempt)
                self._log_attempt(attempt)
                continue

            try:
                success = strategy_fn(failure)
                elapsed = round(time.time() - attempt_start, 2)

                status = RecoveryStatus.SUCCESS if success else RecoveryStatus.FAILED
                message = (
                    f"Strategy {strategy.value} succeeded"
                    if success
                    else f"Strategy {strategy.value} did not resolve the issue"
                )

                attempt = RecoveryAttempt(
                    job_id=job_id,
                    attempt_number=attempt_num,
                    strategy=strategy,
                    status=status,
                    message=message,
                    duration_seconds=elapsed,
                )
                attempts.append(attempt)
                self._log_attempt(attempt)

                if success:
                    resolved = True
                    logger.info(
                        f"[{job_id}] Recovered on attempt {attempt_num} "
                        f"via {strategy.value}"
                    )
                    break

            except Exception as exc:
                elapsed = round(time.time() - attempt_start, 2)
                attempt = RecoveryAttempt(
                    job_id=job_id,
                    attempt_number=attempt_num,
                    strategy=strategy,
                    status=RecoveryStatus.FAILED,
                    message=f"Exception during {strategy.value}: {exc}",
                    duration_seconds=elapsed,
                )
                attempts.append(attempt)
                self._log_attempt(attempt)
                logger.error(f"[{job_id}] Attempt {attempt_num} exception: {exc}")

        total_duration = round(time.time() - start_time, 2)


        if not resolved:
            self._escalate(failure, attempts)
            final_status = RecoveryStatus.ESCALATED
        else:
            final_status = RecoveryStatus.SUCCESS

        result = RecoveryResult(
            job_id=job_id,
            failure=failure,
            attempts=attempts,
            resolved=resolved,
            final_status=final_status,
            total_duration_seconds=total_duration,
        )


        entry_key = failure.context.get("entry_key")
        if entry_key:
            self._mark_handled(entry_key)

        self._save_result(result)
        return result

    # ------------------------------------------------------------------
    # Scan & heal — batch mode
    # ------------------------------------------------------------------

    def scan_and_heal(self) -> List[RecoveryResult]:
        """
        Scan execution log for failures and attempt recovery for each.

        Returns a list of RecoveryResult objects.
        """
        failures = self.detect_failures_from_log()

        if not failures:
            logger.info("No failures detected — all systems nominal")
            return []

        logger.info(f"Detected {len(failures)} failure(s) — beginning recovery")

        results: List[RecoveryResult] = []
        for failure in failures:
            result = self.handle_failure(
                job_id=failure.job_id,
                failure_type=failure.failure_type,
                error_message=failure.error_message,
            )

            if failure.context.get("entry_key"):
                self._mark_handled(failure.context["entry_key"])
            results.append(result)

        return results

    # ------------------------------------------------------------------
    # Alerting / escalation
    # ------------------------------------------------------------------

    def _escalate(self, failure: FailureEvent, attempts: List[RecoveryAttempt]) -> None:
        """Send alert via Notifier when all retries are exhausted."""
        logger.warning(
            f"[{failure.job_id}] All {len(attempts)} recovery attempts failed "
            f"— escalating to human"
        )

        summary_lines = [
            f"🚨 <b>Self-Healing Escalation</b>",
            f"",
            f"<b>Job:</b> {failure.job_id}",
            f"<b>Failure:</b> {failure.failure_type.value}",
            f"<b>Error:</b> {failure.error_message[:200]}",
            f"<b>Attempts:</b> {len(attempts)}",
            f"",
        ]
        for att in attempts:
            icon = "✓" if att.status == RecoveryStatus.SUCCESS else "✗"
            summary_lines.append(
                f"  {icon} Attempt {att.attempt_number}: "
                f"{att.strategy.value} → {att.status.value} "
                f"({att.duration_seconds:.1f}s)"
            )
        summary_lines.append("")
        summary_lines.append(
            "⚠️ Human intervention required. "
            "The system will NOT make further automatic decisions."
        )

        message = "\n".join(summary_lines)

        if self.notifier and self.notify_recipient:
            result = self.notifier.send(
                channel=self.notify_channel,
                recipient=self.notify_recipient,
                subject=f"[ALERT] Self-Healing Failed: {failure.job_id}",
                message=message,
            )
            if result.get("ok"):
                logger.info(f"[{failure.job_id}] Alert sent via {self.notify_channel}")
            else:
                logger.error(
                    f"[{failure.job_id}] Alert send failed: {result.get('error')}"
                )
        else:
            logger.warning(
                f"[{failure.job_id}] No notifier/recipient configured — "
                f"escalation logged only"
            )

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _log_attempt(self, attempt: RecoveryAttempt) -> None:
        """Append a recovery attempt to recovery.log as structured JSON line."""
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": attempt.timestamp,
            "job_id": attempt.job_id,
            "attempt": attempt.attempt_number,
            "strategy": attempt.strategy.value,
            "status": attempt.status.value,
            "message": attempt.message,
            "duration_seconds": attempt.duration_seconds,
        }

        with open(RECOVERY_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _save_result(self, result: RecoveryResult) -> None:
        """Persist recovery result to recovery_state.json."""
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        state = self._load_state()
        state_entry = {
            "job_id": result.job_id,
            "resolved": result.resolved,
            "final_status": result.final_status.value,
            "total_duration_seconds": result.total_duration_seconds,
            "attempts_count": len(result.attempts),
            "failure_type": result.failure.failure_type.value,
            "error_message": result.failure.error_message[:300],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if "history" not in state:
            state["history"] = []
        state["history"].append(state_entry)


        state["history"] = state["history"][-200:]
        state["last_updated"] = datetime.now(timezone.utc).isoformat()

        with open(RECOVERY_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def _load_state(self) -> Dict[str, Any]:
        """Load recovery state from disk."""
        if RECOVERY_STATE_FILE.exists():
            try:
                with open(RECOVERY_STATE_FILE) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"history": [], "handled_ids": []}

    def _load_handled_ids(self) -> set:
        """Load set of already-handled failure entry keys."""
        state = self._load_state()
        return set(state.get("handled_ids", []))

    def _mark_handled(self, entry_key: str) -> None:
        """Mark a failure entry as handled to prevent re-processing."""
        state = self._load_state()
        handled = state.get("handled_ids", [])
        if entry_key not in handled:
            handled.append(entry_key)

        state["handled_ids"] = handled[-500:]
        state["last_updated"] = datetime.now(timezone.utc).isoformat()

        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        with open(RECOVERY_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    # ------------------------------------------------------------------
    # Status / reporting
    # ------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        """
        Return a summary of recent recovery activity.

        Useful for the heartbeat system or dashboards.
        """
        state = self._load_state()
        history = state.get("history", [])

        recent = history[-10:]
        total = len(history)
        resolved_count = sum(1 for h in history if h.get("resolved"))
        escalated_count = sum(
            1 for h in history if h.get("final_status") == "escalated"
        )

        return {
            "total_recoveries": total,
            "resolved": resolved_count,
            "escalated": escalated_count,
            "success_rate": (
                round(resolved_count / total * 100, 1) if total > 0 else 100.0
            ),
            "recent": recent,
            "last_updated": state.get("last_updated"),
        }

    def get_recovery_history(
        self, job_id: Optional[str] = None, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get recent recovery history, optionally filtered by job_id."""
        state = self._load_state()
        history = state.get("history", [])

        if job_id:
            history = [h for h in history if h.get("job_id") == job_id]

        return history[-limit:]


# ─────────────────────────────────────────────────────────────────────────────
# Convenience function for external callers
# ─────────────────────────────────────────────────────────────────────────────


def heal(
    job_id: str,
    error_message: str,
    failure_type: Optional[FailureType] = None,
) -> RecoveryResult:
    """
    One-shot convenience function.

    Can be called from cron_setup.py or heartbeat.py::

        from automation.self_healing import heal, FailureType
        result = heal("content_pipeline", "ImportError: ...")
    """
    healer = SelfHealing()
    return healer.handle_failure(
        job_id=job_id,
        failure_type=failure_type,
        error_message=error_message,
    )


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def main():
    """CLI entry point for self-healing system."""
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw Self-Healing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python self_healing.py scan          # Scan logs and auto-heal failures
  python self_healing.py status        # Show recovery statistics
  python self_healing.py history       # Show recovery history
  python self_healing.py heal <job_id> <error_msg>  # Heal a specific failure
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")


    subparsers.add_parser("scan", help="Scan execution logs and auto-heal")


    subparsers.add_parser("status", help="Show recovery statistics")


    hist_parser = subparsers.add_parser("history", help="Show recovery history")
    hist_parser.add_argument("--job-id", help="Filter by job ID")
    hist_parser.add_argument("--limit", type=int, default=20, help="Max entries")


    heal_parser = subparsers.add_parser("heal", help="Heal a specific failure")
    heal_parser.add_argument("job_id", help="Job ID to heal")
    heal_parser.add_argument("error_message", help="Error message")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    healer = SelfHealing()

    if args.command == "scan":
        results = healer.scan_and_heal()
        if not results:
            print("No failures detected.")
        else:
            for r in results:
                icon = "✓" if r.resolved else "✗"
                print(
                    f"  {icon} {r.job_id}: {r.final_status.value} "
                    f"({len(r.attempts)} attempts, {r.total_duration_seconds:.1f}s)"
                )

    elif args.command == "status":
        s = healer.status()
        print(f"\n{'=' * 50}")
        print(f"  Self-Healing Status")
        print(f"{'=' * 50}")
        print(f"  Total recoveries: {s['total_recoveries']}")
        print(f"  Resolved: {s['resolved']}")
        print(f"  Escalated: {s['escalated']}")
        print(f"  Success rate: {s['success_rate']}%")
        print(f"  Last updated: {s.get('last_updated', 'never')}")
        print(f"{'=' * 50}\n")

    elif args.command == "history":
        entries = healer.get_recovery_history(args.job_id, args.limit)
        print(json.dumps(entries, indent=2))

    elif args.command == "heal":
        result = healer.handle_failure(
            job_id=args.job_id,
            error_message=args.error_message,
        )
        icon = "✓" if result.resolved else "✗"
        print(
            f"{icon} {result.job_id}: {result.final_status.value} "
            f"({len(result.attempts)} attempts, {result.total_duration_seconds:.1f}s)"
        )


if __name__ == "__main__":
    main()
