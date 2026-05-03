"""
Cron Jobs Setup - Automation Scheduler
Configures and manages automated job execution for OpenClaw.

Jobs are defined in jobs.json and executed on schedule via system cron
or the built-in scheduler. Supports dry-run, dependency validation,
and structured logging.
"""

import importlib
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure workspace root is importable
WORKSPACE_ROOT = "/home/openclaw/.openclaw/workspace"
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

JOBS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs.json")
LOG_DIR = os.path.join(WORKSPACE_ROOT, "logs", "cron")


class CronScheduler:
    """
    Manages automated job scheduling and execution.

    Reads job definitions from jobs.json, validates dependencies,
    and supports dry-run mode for safe testing.
    """

    def __init__(self, jobs_file: str = JOBS_FILE, dry_run: bool = False):
        self.jobs_file = jobs_file
        self.dry_run = dry_run
        self.config = self._load_config()
        self.jobs: List[Dict] = self.config.get("jobs", [])
        self.defaults: Dict = self.config.get("defaults", {})
        self.logger = self._setup_logger()

    # ------------------------------------------------------------------
    # Config loading
    # ------------------------------------------------------------------

    def _load_config(self) -> Dict:
        """Load jobs configuration from JSON file."""
        if not os.path.exists(self.jobs_file):
            raise FileNotFoundError(f"Jobs config not found: {self.jobs_file}")
        with open(self.jobs_file) as f:
            return json.load(f)

    def _setup_logger(self) -> logging.Logger:
        """Configure logging for cron jobs."""
        os.makedirs(LOG_DIR, exist_ok=True)
        logger = logging.getLogger("cron_scheduler")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # File handler
            log_file = os.path.join(LOG_DIR, f"scheduler_{datetime.now():%Y-%m-%d}.log")
            fh = logging.FileHandler(log_file)
            fh.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )
            logger.addHandler(fh)

            # Console handler
            ch = logging.StreamHandler()
            ch.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )
            logger.addHandler(ch)

        return logger

    # ------------------------------------------------------------------
    # Job retrieval
    # ------------------------------------------------------------------

    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get a job definition by ID."""
        for job in self.jobs:
            if job["id"] == job_id:
                return job
        return None

    def list_jobs(
        self, enabled_only: bool = False, tag: Optional[str] = None
    ) -> List[Dict]:
        """
        List jobs with optional filtering.

        Args:
            enabled_only: Only return enabled jobs.
            tag: Filter by tag.
        """
        result = self.jobs
        if enabled_only:
            result = [j for j in result if j.get("enabled", True)]
        if tag:
            result = [j for j in result if tag in j.get("tags", [])]
        return result

    # ------------------------------------------------------------------
    # Dependency validation
    # ------------------------------------------------------------------

    def validate_dependencies(self, job: Dict) -> Dict[str, Any]:
        """
        Check if all dependency files exist before running a job.

        Returns:
            {"valid": bool, "missing": [...], "found": [...]}
        """
        deps = job.get("dependencies", [])
        missing = []
        found = []

        for dep in deps:
            dep_path = os.path.join(WORKSPACE_ROOT, dep)
            if os.path.exists(dep_path):
                found.append(dep)
            else:
                missing.append(dep)

        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "found": found,
        }

    def validate_all_jobs(self) -> Dict[str, Dict]:
        """Validate dependencies for all enabled jobs."""
        results = {}
        for job in self.list_jobs(enabled_only=True):
            results[job["id"]] = {
                "name": job["name"],
                "schedule": job["schedule_human"],
                **self.validate_dependencies(job),
            }
        return results

    # ------------------------------------------------------------------
    # Job execution
    # ------------------------------------------------------------------

    def _resolve_effective(self, job: Dict, key: str) -> Any:
        """Get job-level value or fall back to defaults."""
        return job.get(key, self.defaults.get(key))

    def run_job(self, job_id: str) -> Dict[str, Any]:
        """
        Execute a single job by ID.

        In dry-run mode, validates and logs without executing.

        Returns:
            {
                "job_id": str,
                "success": bool,
                "dry_run": bool,
                "duration_seconds": float,
                "output": str | None,
                "error": str | None
            }
        """
        job = self.get_job(job_id)
        if job is None:
            return {"job_id": job_id, "success": False, "error": "Job not found"}

        if not job.get("enabled", True):
            return {"job_id": job_id, "success": False, "error": "Job is disabled"}

        # Validate dependencies
        dep_check = self.validate_dependencies(job)
        if not dep_check["valid"]:
            msg = f"Missing dependencies: {dep_check['missing']}"
            self.logger.error(f"[{job_id}] {msg}")
            return {"job_id": job_id, "success": False, "error": msg}

        timeout = self._resolve_effective(job, "timeout_seconds") or 300

        # Dry-run mode
        if self.dry_run:
            self.logger.info(f"[DRY-RUN] [{job_id}] Would execute: {job['name']}")
            self.logger.info(f"[DRY-RUN] [{job_id}] Schedule: {job['schedule_human']}")
            self.logger.info(f"[DRY-RUN] [{job_id}] Timeout: {timeout}s")
            self.logger.info(
                f"[DRY-RUN] [{job_id}] Dependencies OK: {dep_check['found']}"
            )

            if job.get("module"):
                self.logger.info(
                    f"[DRY-RUN] [{job_id}] Module: {job['module']}.{job['class']}.{job['method']}"
                )
            else:
                self.logger.info(f"[DRY-RUN] [{job_id}] Command: {job['command']}")

            return {
                "job_id": job_id,
                "success": True,
                "dry_run": True,
                "duration_seconds": 0.0,
                "output": "Dry-run: validation passed",
                "error": None,
            }

        # Real execution
        return self._execute_job(job, timeout)

    def _execute_job(self, job: Dict, timeout: int) -> Dict[str, Any]:
        """Execute a job, either via Python import or shell command."""
        job_id = job["id"]
        start = time.time()
        result: Dict[str, Any] = {
            "job_id": job_id,
            "success": False,
            "dry_run": False,
            "duration_seconds": 0.0,
            "output": None,
            "error": None,
        }

        max_retries = self._resolve_effective(job, "max_retries") or 0
        attempt = 0

        while attempt <= max_retries:
            attempt += 1
            try:
                if job.get("module") and job.get("class") and job.get("method"):
                    output = self._execute_python(job, timeout)
                else:
                    output = self._execute_command(job["command"], timeout)

                elapsed = time.time() - start
                result.update(
                    success=True,
                    duration_seconds=round(elapsed, 2),
                    output=str(output)[:5000] if output else None,
                )
                self.logger.info(
                    f"[{job_id}] Completed in {elapsed:.1f}s (attempt {attempt})"
                )
                break

            except Exception as exc:
                elapsed = time.time() - start
                error_msg = f"{type(exc).__name__}: {exc}"
                result.update(
                    duration_seconds=round(elapsed, 2),
                    error=error_msg,
                )

                if attempt <= max_retries:
                    self.logger.warning(
                        f"[{job_id}] Attempt {attempt} failed: {error_msg}. Retrying..."
                    )
                    time.sleep(2)
                else:
                    self.logger.error(
                        f"[{job_id}] Failed after {attempt} attempt(s): {error_msg}"
                    )

        self._log_execution(result)
        return result

    def _execute_python(self, job: Dict, timeout: int) -> Any:
        """Execute a job by importing its Python module and calling the method."""
        module_path = job["module"]
        class_name = job["class"]
        method_name = job["method"]
        args = job.get("args", {})

        self.logger.info(
            f"[{job['id']}] Importing {module_path}.{class_name}.{method_name}"
        )

        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        instance = cls()
        method = getattr(instance, method_name)

        if args:
            return method(args)
        return method()

    def _execute_command(self, command: str, timeout: int) -> str:
        """Execute a shell command with timeout."""
        self.logger.info(f"Executing command: {command[:100]}...")

        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE_ROOT,
            env={**os.environ, "PYTHONPATH": WORKSPACE_ROOT},
        )

        if proc.returncode != 0:
            raise RuntimeError(
                f"Command exited with code {proc.returncode}: {proc.stderr[:500]}"
            )

        return proc.stdout

    # ------------------------------------------------------------------
    # Execution log
    # ------------------------------------------------------------------

    def _log_execution(self, result: Dict):
        """Append execution result to the execution log file."""
        log_file = os.path.join(LOG_DIR, "execution_log.json")
        os.makedirs(LOG_DIR, exist_ok=True)

        entry = {
            "timestamp": datetime.now().isoformat(),
            **result,
        }

        log_data = []
        if os.path.exists(log_file):
            try:
                with open(log_file) as f:
                    log_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                log_data = []

        log_data.append(entry)

        # Keep last 500 entries
        log_data = log_data[-500:]

        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)

    def get_execution_history(
        self, job_id: Optional[str] = None, limit: int = 20
    ) -> List[Dict]:
        """Get recent execution history, optionally filtered by job_id."""
        log_file = os.path.join(LOG_DIR, "execution_log.json")
        if not os.path.exists(log_file):
            return []

        with open(log_file) as f:
            log_data = json.load(f)

        if job_id:
            log_data = [e for e in log_data if e.get("job_id") == job_id]

        return log_data[-limit:]

    # ------------------------------------------------------------------
    # System cron installation
    # ------------------------------------------------------------------

    def generate_crontab(self) -> str:
        """
        Generate crontab entries for all enabled jobs.

        Returns a string ready for `crontab -l` replacement.
        """
        lines = [
            "# OpenClaw Automated Jobs",
            f"# Generated: {datetime.now().isoformat()}",
            f"# Source: {self.jobs_file}",
            f"PYTHONPATH={WORKSPACE_ROOT}",
            "",
        ]

        for job in self.list_jobs(enabled_only=True):
            command = job.get("command", "")
            if not command:
                continue

            log_path = os.path.join(LOG_DIR, f"{job['id']}.log")
            cron_line = (
                f"{job['schedule']} cd {WORKSPACE_ROOT} && {command} >> {log_path} 2>&1"
            )
            lines.append(f"# {job['name']} - {job['schedule_human']}")
            lines.append(cron_line)
            lines.append("")

        return "\n".join(lines)

    def install_crontab(self) -> Dict[str, Any]:
        """
        Install generated crontab entries into the system crontab.

        Uses a marker to manage only OpenClaw entries.
        """
        if self.dry_run:
            crontab = self.generate_crontab()
            self.logger.info("[DRY-RUN] Would install crontab:")
            for line in crontab.splitlines():
                self.logger.info(f"  {line}")
            return {"success": True, "dry_run": True, "crontab": crontab}

        marker_start = "# >>> OPENCLAW CRON START <<<"
        marker_end = "# >>> OPENCLAW CRON END <<<"

        # Read existing crontab
        try:
            existing = subprocess.run(
                ["crontab", "-l"], capture_output=True, text=True
            ).stdout
        except Exception:
            existing = ""

        # Remove old OpenClaw entries
        new_lines = []
        in_block = False
        for line in existing.splitlines():
            if marker_start in line:
                in_block = True
                continue
            if marker_end in line:
                in_block = False
                continue
            if not in_block:
                new_lines.append(line)

        # Insert new block
        generated = self.generate_crontab()
        new_lines.append("")
        new_lines.append(marker_start)
        new_lines.extend(generated.splitlines())
        new_lines.append(marker_end)

        final_crontab = "\n".join(new_lines) + "\n"

        # Install
        proc = subprocess.run(
            ["crontab", "-"],
            input=final_crontab,
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            return {"success": False, "error": proc.stderr}

        self.logger.info("Crontab installed successfully")
        return {"success": True, "dry_run": False, "crontab": generated}

    # ------------------------------------------------------------------
    # Job management
    # ------------------------------------------------------------------

    def enable_job(self, job_id: str) -> bool:
        """Enable a job by ID and save config."""
        return self._set_job_enabled(job_id, True)

    def disable_job(self, job_id: str) -> bool:
        """Disable a job by ID and save config."""
        return self._set_job_enabled(job_id, False)

    def _set_job_enabled(self, job_id: str, enabled: bool) -> bool:
        """Toggle job enabled state and persist to config."""
        for job in self.jobs:
            if job["id"] == job_id:
                job["enabled"] = enabled
                self._save_config()
                self.logger.info(f"[{job_id}] {'Enabled' if enabled else 'Disabled'}")
                return True
        return False

    def _save_config(self):
        """Save current config back to jobs.json."""
        self.config["jobs"] = self.jobs
        self.config["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        with open(self.jobs_file, "w") as f:
            json.dump(self.config, f, indent=2)

    # ------------------------------------------------------------------
    # Status / summary
    # ------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        """
        Get full scheduler status.

        Returns summary of all jobs, their validation state, and recent history.
        """
        jobs_status = []
        for job in self.jobs:
            dep_check = self.validate_dependencies(job)
            recent = self.get_execution_history(job["id"], limit=1)
            last_run = recent[0] if recent else None

            jobs_status.append(
                {
                    "id": job["id"],
                    "name": job["name"],
                    "schedule": job["schedule_human"],
                    "enabled": job.get("enabled", True),
                    "dependencies_valid": dep_check["valid"],
                    "missing_deps": dep_check["missing"],
                    "last_run": last_run,
                }
            )

        enabled_count = sum(1 for j in jobs_status if j["enabled"])
        valid_count = sum(
            1 for j in jobs_status if j["enabled"] and j["dependencies_valid"]
        )

        return {
            "total_jobs": len(jobs_status),
            "enabled": enabled_count,
            "ready": valid_count,
            "dry_run": self.dry_run,
            "jobs": jobs_status,
        }

    def print_status(self):
        """Print a formatted status report to stdout."""
        s = self.status()
        print(f"\n{'=' * 60}")
        print(f"  OpenClaw Cron Scheduler Status")
        print(f"  Mode: {'DRY-RUN' if s['dry_run'] else 'LIVE'}")
        print(f"  Jobs: {s['enabled']}/{s['total_jobs']} enabled, {s['ready']} ready")
        print(f"{'=' * 60}\n")

        for job in s["jobs"]:
            icon = "✅" if job["enabled"] and job["dependencies_valid"] else "❌"
            enabled_str = "ON " if job["enabled"] else "OFF"
            print(f"  {icon} [{enabled_str}] {job['name']}")
            print(f"       Schedule: {job['schedule']}")
            if job["missing_deps"]:
                print(f"       ⚠ Missing: {', '.join(job['missing_deps'])}")
            if job["last_run"]:
                lr = job["last_run"]
                status_str = "✓" if lr.get("success") else "✗"
                print(f"       Last run: {lr.get('timestamp', '?')} [{status_str}]")
            print()


# ------------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------------


def main():
    """CLI entry point for cron_setup.py."""
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw Cron Job Scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cron_setup.py status                 # Show all jobs status
  python cron_setup.py validate               # Validate all dependencies
  python cron_setup.py run content_pipeline   # Run a specific job
  python cron_setup.py run-all                # Run all enabled jobs
  python cron_setup.py --dry-run run-all      # Dry-run all jobs
  python cron_setup.py crontab                # Generate crontab
  python cron_setup.py install                # Install to system crontab
  python cron_setup.py enable trading_signal_check
  python cron_setup.py disable trading_signal_check
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and log without executing",
    )
    parser.add_argument(
        "--jobs-file",
        default=JOBS_FILE,
        help=f"Path to jobs.json (default: {JOBS_FILE})",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # status
    subparsers.add_parser("status", help="Show scheduler status")

    # validate
    subparsers.add_parser("validate", help="Validate all job dependencies")

    # run <job_id>
    run_parser = subparsers.add_parser("run", help="Run a specific job")
    run_parser.add_argument("job_id", help="Job ID to execute")

    # run-all
    subparsers.add_parser("run-all", help="Run all enabled jobs")

    # crontab
    subparsers.add_parser("crontab", help="Generate crontab entries")

    # install
    subparsers.add_parser("install", help="Install to system crontab")

    # enable/disable
    enable_parser = subparsers.add_parser("enable", help="Enable a job")
    enable_parser.add_argument("job_id", help="Job ID to enable")

    disable_parser = subparsers.add_parser("disable", help="Disable a job")
    disable_parser.add_argument("job_id", help="Job ID to disable")

    # history
    history_parser = subparsers.add_parser("history", help="Show execution history")
    history_parser.add_argument("--job-id", help="Filter by job ID")
    history_parser.add_argument("--limit", type=int, default=10, help="Max entries")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    scheduler = CronScheduler(jobs_file=args.jobs_file, dry_run=args.dry_run)

    if args.command == "status":
        scheduler.print_status()

    elif args.command == "validate":
        results = scheduler.validate_all_jobs()
        print(json.dumps(results, indent=2))

    elif args.command == "run":
        result = scheduler.run_job(args.job_id)
        print(json.dumps(result, indent=2))

    elif args.command == "run-all":
        results = {}
        for job in scheduler.list_jobs(enabled_only=True):
            results[job["id"]] = scheduler.run_job(job["id"])
        print(json.dumps(results, indent=2))

    elif args.command == "crontab":
        print(scheduler.generate_crontab())

    elif args.command == "install":
        result = scheduler.install_crontab()
        print(json.dumps(result, indent=2))

    elif args.command == "enable":
        ok = scheduler.enable_job(args.job_id)
        print(f"{'Enabled' if ok else 'Job not found'}: {args.job_id}")

    elif args.command == "disable":
        ok = scheduler.disable_job(args.job_id)
        print(f"{'Disabled' if ok else 'Job not found'}: {args.job_id}")

    elif args.command == "history":
        entries = scheduler.get_execution_history(args.job_id, args.limit)
        print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
