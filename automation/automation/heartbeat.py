#!/usr/bin/env python3
"""
Heartbeat Configuration Module
================================

Periodic health checks for the trading automation system.
Runs every 30 minutes to verify:
  1. Deadline check - upcoming task deadlines
  2. Signal check - new trading signals
  3. Credential check - API credentials validity
  4. Health check - system health status

Returns structured results with health score (0-100).
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# ─────────────────────────────────────────────────────────────────────────────
# Setup logging
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels."""

    CRITICAL = "critical"
    WARNING = "warning"
    HEALTHY = "healthy"


@dataclass
class CheckResult:
    """Result of a single health check."""

    name: str
    status: HealthStatus
    message: str
    details: Dict[str, Any]
    timestamp: str
    score: int  # 0-100 for this check


@dataclass
class HeartbeatReport:
    """Complete heartbeat report."""

    timestamp: str
    checks: List[CheckResult]
    overall_health: HealthStatus
    health_score: int  # 0-100 overall
    issues: List[str]


class DeadlineChecker:
    """Check for upcoming task deadlines."""

    def __init__(self, tasks_db_path: Optional[Path] = None):
        """
        Initialize deadline checker.

        Args:
            tasks_db_path: Path to tasks database. Defaults to data/tasks.db
        """
        if tasks_db_path is None:
            workspace_root = Path(__file__).resolve().parent.parent.parent
            tasks_db_path = (
                workspace_root / ".openclaw" / "workspace" / "data" / "tasks.db"
            )

        self.tasks_db_path = tasks_db_path
        self.warning_hours = 24  # Alert if deadline within 24 hours

    def check(self) -> CheckResult:
        """
        Check for upcoming task deadlines.

        Returns:
            CheckResult with deadline information
        """
        try:
            # Check if tasks database exists
            if not self.tasks_db_path.exists():
                return CheckResult(
                    name="deadline_check",
                    status=HealthStatus.HEALTHY,
                    message="No tasks database found (expected in early setup)",
                    details={"upcoming_tasks": 0, "urgent_tasks": 0},
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    score=100,
                )

            # Try to load tasks from database
            upcoming_tasks = self._get_upcoming_tasks()
            urgent_tasks = [t for t in upcoming_tasks if t["hours_until_deadline"] < 1]

            if urgent_tasks:
                status = HealthStatus.CRITICAL
                score = 40
                message = f"URGENT: {len(urgent_tasks)} task(s) due within 1 hour"
            elif upcoming_tasks:
                status = HealthStatus.WARNING
                score = 70
                message = f"{len(upcoming_tasks)} task(s) due within {self.warning_hours} hours"
            else:
                status = HealthStatus.HEALTHY
                score = 100
                message = "No urgent deadlines"

            return CheckResult(
                name="deadline_check",
                status=status,
                message=message,
                details={
                    "upcoming_tasks": len(upcoming_tasks),
                    "urgent_tasks": len(urgent_tasks),
                    "tasks": upcoming_tasks[:5],  # Top 5 upcoming
                },
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=score,
            )

        except Exception as e:
            logger.error(f"Deadline check failed: {e}")
            return CheckResult(
                name="deadline_check",
                status=HealthStatus.WARNING,
                message=f"Deadline check error: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=50,
            )

    def _get_upcoming_tasks(self) -> List[Dict[str, Any]]:
        """
        Get upcoming tasks from database.

        Returns:
            List of upcoming tasks with deadline info
        """
        try:
            import sqlite3

            conn = sqlite3.connect(str(self.tasks_db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Query tasks with deadlines in next 24 hours
            now = datetime.now(timezone.utc)
            deadline_threshold = now + timedelta(hours=self.warning_hours)

            cursor.execute(
                """
                SELECT id, title, deadline, priority, status
                FROM tasks
                WHERE deadline IS NOT NULL
                AND datetime(deadline) > datetime(?)
                AND datetime(deadline) <= datetime(?)
                AND status != 'completed'
                AND status != 'cancelled'
                ORDER BY deadline ASC
                LIMIT 10
            """,
                (now.isoformat(), deadline_threshold.isoformat()),
            )

            tasks = []
            for row in cursor.fetchall():
                deadline = datetime.fromisoformat(
                    row["deadline"].replace("Z", "+00:00")
                )
                hours_until = (deadline - now).total_seconds() / 3600

                tasks.append(
                    {
                        "id": row["id"],
                        "title": row["title"],
                        "deadline": row["deadline"],
                        "priority": row["priority"],
                        "status": row["status"],
                        "hours_until_deadline": round(hours_until, 1),
                    }
                )

            conn.close()
            return tasks

        except ImportError:
            logger.warning("sqlite3 not available, skipping database check")
            return []
        except Exception as e:
            logger.error(f"Error querying tasks: {e}")
            return []


class SignalChecker:
    """Check for new trading signals."""

    def __init__(self, signals_dir: Optional[Path] = None):
        """
        Initialize signal checker.

        Args:
            signals_dir: Path to signals directory. Defaults to trading/data/signals
        """
        if signals_dir is None:
            workspace_root = Path(__file__).resolve().parent.parent.parent
            signals_dir = (
                workspace_root
                / ".openclaw"
                / "workspace"
                / "trading"
                / "data"
                / "signals"
            )

        self.signals_dir = signals_dir

    def check(self) -> CheckResult:
        """
        Check for new trading signals.

        Returns:
            CheckResult with signal information
        """
        try:
            if not self.signals_dir.exists():
                return CheckResult(
                    name="signal_check",
                    status=HealthStatus.HEALTHY,
                    message="No signals directory (expected in early setup)",
                    details={"new_signals": 0, "active_signals": 0},
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    score=100,
                )

            # Check for signal files
            signal_files = list(self.signals_dir.glob("*.json"))
            new_signals = self._get_new_signals(signal_files)
            active_signals = self._get_active_signals(signal_files)

            if new_signals:
                status = HealthStatus.WARNING
                score = 80
                message = f"{len(new_signals)} new signal(s) detected"
            elif active_signals:
                status = HealthStatus.HEALTHY
                score = 90
                message = f"{len(active_signals)} active signal(s)"
            else:
                status = HealthStatus.HEALTHY
                score = 100
                message = "No active signals"

            return CheckResult(
                name="signal_check",
                status=status,
                message=message,
                details={
                    "new_signals": len(new_signals),
                    "active_signals": len(active_signals),
                    "signals": new_signals[:5],  # Top 5 new signals
                },
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=score,
            )

        except Exception as e:
            logger.error(f"Signal check failed: {e}")
            return CheckResult(
                name="signal_check",
                status=HealthStatus.WARNING,
                message=f"Signal check error: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=50,
            )

    def _get_new_signals(self, signal_files: List[Path]) -> List[Dict[str, Any]]:
        """Get signals created in last hour."""
        now = datetime.now(timezone.utc)
        new_signals = []

        for signal_file in signal_files:
            try:
                mtime = datetime.fromtimestamp(signal_file.stat().st_mtime)
                if (now - mtime).total_seconds() < 3600:  # Last hour
                    with open(signal_file) as f:
                        signal_data = json.load(f)
                        new_signals.append(
                            {
                                "file": signal_file.name,
                                "created": mtime.isoformat(),
                                "symbol": signal_data.get("symbol", "unknown"),
                                "type": signal_data.get("type", "unknown"),
                            }
                        )
            except Exception as e:
                logger.warning(f"Error reading signal file {signal_file}: {e}")

        return new_signals

    def _get_active_signals(self, signal_files: List[Path]) -> List[Dict[str, Any]]:
        """Get all active signals."""
        active_signals = []

        for signal_file in signal_files:
            try:
                with open(signal_file) as f:
                    signal_data = json.load(f)
                    if signal_data.get("status") == "active":
                        active_signals.append(
                            {
                                "file": signal_file.name,
                                "symbol": signal_data.get("symbol", "unknown"),
                                "type": signal_data.get("type", "unknown"),
                            }
                        )
            except Exception as e:
                logger.warning(f"Error reading signal file {signal_file}: {e}")

        return active_signals


class CredentialChecker:
    """Check API credentials validity."""

    def __init__(self, credentials_dir: Optional[Path] = None):
        """
        Initialize credential checker.

        Args:
            credentials_dir: Path to credentials directory. Defaults to credentials/
        """
        if credentials_dir is None:
            workspace_root = Path(__file__).resolve().parent.parent.parent
            credentials_dir = workspace_root / ".openclaw" / "workspace" / "credentials"

        self.credentials_dir = credentials_dir

    def check(self) -> CheckResult:
        """
        Check API credentials validity.

        Returns:
            CheckResult with credential information
        """
        try:
            if not self.credentials_dir.exists():
                return CheckResult(
                    name="credential_check",
                    status=HealthStatus.HEALTHY,
                    message="No credentials directory (expected in early setup)",
                    details={"credentials_found": 0, "valid_credentials": 0},
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    score=100,
                )

            # Check environment variables for credentials
            env_credentials = self._check_env_credentials()
            file_credentials = self._check_file_credentials()

            total_credentials = len(env_credentials) + len(file_credentials)
            valid_credentials = sum(
                1 for c in env_credentials + file_credentials if c.get("valid")
            )

            if total_credentials == 0:
                status = HealthStatus.HEALTHY
                score = 100
                message = "No credentials configured (expected in early setup)"
            elif valid_credentials == total_credentials:
                status = HealthStatus.HEALTHY
                score = 100
                message = f"All {total_credentials} credential(s) valid"
            elif valid_credentials > 0:
                status = HealthStatus.WARNING
                score = 60
                message = f"{valid_credentials}/{total_credentials} credential(s) valid"
            else:
                status = HealthStatus.CRITICAL
                score = 20
                message = f"No valid credentials found ({total_credentials} configured)"

            return CheckResult(
                name="credential_check",
                status=status,
                message=message,
                details={
                    "total_credentials": total_credentials,
                    "valid_credentials": valid_credentials,
                    "credentials": env_credentials + file_credentials,
                },
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=score,
            )

        except Exception as e:
            logger.error(f"Credential check failed: {e}")
            return CheckResult(
                name="credential_check",
                status=HealthStatus.WARNING,
                message=f"Credential check error: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=50,
            )

    def _check_env_credentials(self) -> List[Dict[str, Any]]:
        """Check environment variable credentials."""
        credentials = []
        env_keys = [
            "MT5_LOGIN",
            "MT5_PASSWORD",
            "MT5_SERVER",
            "CTRADER_LOGIN",
            "CTRADER_PASSWORD",
            "CTRADER_SERVER",
            "API_KEY",
            "API_SECRET",
        ]

        for key in env_keys:
            if key in os.environ:
                value = os.environ[key]
                # Check if credential is not empty
                valid = bool(value and len(value) > 0)
                credentials.append(
                    {
                        "source": "environment",
                        "name": key,
                        "valid": valid,
                        "length": len(value) if value else 0,
                    }
                )

        return credentials

    def _check_file_credentials(self) -> List[Dict[str, Any]]:
        """Check file-based credentials."""
        credentials = []

        try:
            # Check for .env files
            env_files = [
                self.credentials_dir / ".env",
                self.credentials_dir / ".env.local",
                Path.home() / ".openclaw" / ".env",
            ]

            for env_file in env_files:
                if env_file.exists():
                    try:
                        with open(env_file) as f:
                            content = f.read()
                            # Simple check: file has content
                            valid = len(content.strip()) > 0
                            credentials.append(
                                {
                                    "source": "file",
                                    "name": env_file.name,
                                    "path": str(env_file),
                                    "valid": valid,
                                    "size": len(content),
                                }
                            )
                    except Exception as e:
                        logger.warning(f"Error reading {env_file}: {e}")

        except Exception as e:
            logger.warning(f"Error checking file credentials: {e}")

        return credentials


class HealthChecker:
    """Check overall system health status."""

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize health checker.

        Args:
            workspace_root: Path to workspace root. Defaults to .openclaw/workspace
        """
        if workspace_root is None:
            workspace_root = Path(__file__).resolve().parent.parent.parent

        self.workspace_root = workspace_root

    def check(self) -> CheckResult:
        """
        Check overall system health.

        Returns:
            CheckResult with health information
        """
        try:
            health_metrics = {
                "disk_space": self._check_disk_space(),
                "log_files": self._check_log_files(),
                "database": self._check_database(),
                "trading_module": self._check_trading_module(),
            }

            # Calculate overall score
            scores = [m.get("score", 50) for m in health_metrics.values()]
            overall_score = sum(scores) // len(scores) if scores else 50

            if overall_score >= 80:
                status = HealthStatus.HEALTHY
            elif overall_score >= 50:
                status = HealthStatus.WARNING
            else:
                status = HealthStatus.CRITICAL

            issues = [m.get("issue") for m in health_metrics.values() if m.get("issue")]
            issues = [i for i in issues if i]  # Remove None values

            return CheckResult(
                name="health_check",
                status=status,
                message=f"System health: {overall_score}%",
                details={"metrics": health_metrics, "issues": issues},
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=overall_score,
            )

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return CheckResult(
                name="health_check",
                status=HealthStatus.WARNING,
                message=f"Health check error: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now(timezone.utc).isoformat(),
                score=50,
            )

    def _check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space."""
        try:
            import shutil

            stat = shutil.disk_usage(str(self.workspace_root))
            percent_free = (stat.free / stat.total) * 100

            if percent_free < 5:
                return {
                    "status": "critical",
                    "score": 20,
                    "issue": f"Low disk space: {percent_free:.1f}% free",
                    "percent_free": percent_free,
                }
            elif percent_free < 10:
                return {
                    "status": "warning",
                    "score": 60,
                    "issue": f"Disk space low: {percent_free:.1f}% free",
                    "percent_free": percent_free,
                }
            else:
                return {"status": "healthy", "score": 100, "percent_free": percent_free}
        except Exception as e:
            logger.warning(f"Error checking disk space: {e}")
            return {"status": "unknown", "score": 50, "error": str(e)}

    def _check_log_files(self) -> Dict[str, Any]:
        """Check log files for errors."""
        try:
            logs_dir = self.workspace_root / "logs"
            if not logs_dir.exists():
                return {"status": "healthy", "score": 100, "log_files": 0}

            log_files = list(logs_dir.glob("*.log"))
            error_count = 0

            for log_file in log_files:
                try:
                    with open(log_file) as f:
                        content = f.read()
                        error_count += content.count("ERROR")
                        error_count += content.count("CRITICAL")
                except Exception:
                    pass

            if error_count > 100:
                return {
                    "status": "warning",
                    "score": 60,
                    "issue": f"High error count in logs: {error_count}",
                    "error_count": error_count,
                    "log_files": len(log_files),
                }
            else:
                return {
                    "status": "healthy",
                    "score": 100,
                    "error_count": error_count,
                    "log_files": len(log_files),
                }

        except Exception as e:
            logger.warning(f"Error checking log files: {e}")
            return {"status": "unknown", "score": 50, "error": str(e)}

    def _check_database(self) -> Dict[str, Any]:
        """Check database integrity."""
        try:
            db_path = self.workspace_root / "data" / "tasks.db"
            if not db_path.exists():
                return {"status": "healthy", "score": 100, "database": "not_found"}

            # Try to open and query database
            import sqlite3

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()

            if table_count > 0:
                return {
                    "status": "healthy",
                    "score": 100,
                    "database": "ok",
                    "tables": table_count,
                }
            else:
                return {
                    "status": "warning",
                    "score": 70,
                    "issue": "Database has no tables",
                    "tables": 0,
                }

        except Exception as e:
            logger.warning(f"Error checking database: {e}")
            return {"status": "warning", "score": 60, "error": str(e)}

    def _check_trading_module(self) -> Dict[str, Any]:
        """Check trading module availability."""
        try:
            trading_dir = self.workspace_root / "trading"
            if not trading_dir.exists():
                return {
                    "status": "warning",
                    "score": 60,
                    "issue": "Trading module not found",
                }

            # Check for key trading files
            key_files = ["automated_trader.py", "broker_config.py", "exceptions.py"]

            found_files = sum(1 for f in key_files if (trading_dir / f).exists())

            if found_files == len(key_files):
                return {
                    "status": "healthy",
                    "score": 100,
                    "trading_module": "ok",
                    "key_files": found_files,
                }
            else:
                return {
                    "status": "warning",
                    "score": 70,
                    "issue": f"Missing trading files: {found_files}/{len(key_files)}",
                    "key_files": found_files,
                }

        except Exception as e:
            logger.warning(f"Error checking trading module: {e}")
            return {"status": "unknown", "score": 50, "error": str(e)}


class Heartbeat:
    """Main heartbeat orchestrator."""

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize heartbeat system.

        Args:
            workspace_root: Path to workspace root
        """
        if workspace_root is None:
            workspace_root = Path(__file__).resolve().parent.parent.parent

        self.workspace_root = workspace_root
        self.deadline_checker = DeadlineChecker()
        self.signal_checker = SignalChecker()
        self.credential_checker = CredentialChecker()
        self.health_checker = HealthChecker(workspace_root)

    def run(self) -> HeartbeatReport:
        """
        Run all health checks.

        Returns:
            HeartbeatReport with all check results
        """
        logger.info("Starting heartbeat checks...")

        # Run all checks in sequence
        checks = [
            self.deadline_checker.check(),
            self.signal_checker.check(),
            self.credential_checker.check(),
            self.health_checker.check(),
        ]

        # Calculate overall health
        scores = [c.score for c in checks]
        overall_score = sum(scores) // len(scores) if scores else 50

        # Determine overall status
        if overall_score >= 80:
            overall_health = HealthStatus.HEALTHY
        elif overall_score >= 50:
            overall_health = HealthStatus.WARNING
        else:
            overall_health = HealthStatus.CRITICAL

        # Collect issues
        issues = [c.message for c in checks if c.status != HealthStatus.HEALTHY]

        report = HeartbeatReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            checks=checks,
            overall_health=overall_health,
            health_score=overall_score,
            issues=issues,
        )

        logger.info(f"Heartbeat complete. Health score: {overall_score}%")
        return report

    def save_report(
        self, report: HeartbeatReport, output_path: Optional[Path] = None
    ) -> Path:
        """
        Save heartbeat report to file.

        Args:
            report: HeartbeatReport to save
            output_path: Path to save report. Defaults to logs/heartbeat.json

        Returns:
            Path to saved report
        """
        if output_path is None:
            logs_dir = self.workspace_root / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            output_path = logs_dir / "heartbeat.json"

        # Convert report to dict
        report_dict = {
            "timestamp": report.timestamp,
            "overall_health": report.overall_health.value,
            "health_score": report.health_score,
            "issues": report.issues,
            "checks": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "message": c.message,
                    "score": c.score,
                    "details": c.details,
                    "timestamp": c.timestamp,
                }
                for c in report.checks
            ],
        }

        with open(output_path, "w") as f:
            json.dump(report_dict, f, indent=2)

        logger.info(f"Report saved to {output_path}")
        return output_path


def main():
    """Run heartbeat checks and save report."""
    import argparse

    parser = argparse.ArgumentParser(description="Run heartbeat health checks")
    parser.add_argument(
        "--workspace", type=Path, default=None, help="Path to workspace root"
    )
    parser.add_argument("--output", type=Path, default=None, help="Path to save report")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Run heartbeat
    heartbeat = Heartbeat(workspace_root=args.workspace)
    report = heartbeat.run()

    # Save report
    report_path = heartbeat.save_report(report, output_path=args.output)

    # Output results
    if args.json:
        print(
            json.dumps(
                {
                    "timestamp": report.timestamp,
                    "overall_health": report.overall_health.value,
                    "health_score": report.health_score,
                    "issues": report.issues,
                },
                indent=2,
            )
        )
    else:
        print(f"\n{'=' * 60}")
        print(f"HEARTBEAT REPORT - {report.timestamp}")
        print(f"{'=' * 60}")
        print(f"Overall Health: {report.overall_health.value.upper()}")
        print(f"Health Score: {report.health_score}/100")
        print(f"\nChecks ({len(report.checks)}):")
        for check in report.checks:
            status_icon = (
                "✓"
                if check.status == HealthStatus.HEALTHY
                else "⚠"
                if check.status == HealthStatus.WARNING
                else "✗"
            )
            print(f"  {status_icon} {check.name}: {check.message} ({check.score}/100)")

        if report.issues:
            print(f"\nIssues ({len(report.issues)}):")
            for issue in report.issues:
                print(f"  - {issue}")

        print(f"\nReport saved to: {report_path}")
        print(f"{'=' * 60}\n")

    return 0 if report.overall_health != HealthStatus.CRITICAL else 1


if __name__ == "__main__":
    sys.exit(main())
