"""
Content Kingdom Self-Heal
Runs after pipeline failure. Diagnoses issue and attempts recovery.
"""
import json, os, subprocess, sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
LOG_FILE = SKILL_DIR / "logs" / "self_heal.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run():
    log("Self-heal starting...")

    # Find latest pipeline log
    logs = sorted((SKILL_DIR / "logs").glob("pipeline_*.log"), reverse=True)
    if not logs:
        log("No pipeline logs found — nothing to analyze")
        return

    latest_log = logs[0].read_text()
    log(f"Analyzing: {logs[0].name}")

    # Diagnose common failures
    heals_applied = []

    if "ModuleNotFoundError" in latest_log or "ImportError" in latest_log:
        log("🔧 Missing module detected — attempting pip install")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=False)
        heals_applied.append("pip install requests")

    if "Connection refused" in latest_log or "ConnectionError" in latest_log:
        log("🔧 Connection issue — API endpoint may be down, will retry next cycle")
        heals_applied.append("noted connection error — retry scheduled")

    if "JSONDecodeError" in latest_log or "json.decoder" in latest_log:
        log("🔧 Bad JSON in output — clearing output cache")
        for f in (SKILL_DIR / "output").glob("*.json"):
            if f.stat().st_mtime < (datetime.now().timestamp() - 86400):
                f.unlink()
                heals_applied.append(f"removed stale: {f.name}")

    if "Disk quota" in latest_log or "No space left" in latest_log:
        log("🔧 Disk full — clearing old logs and outputs")
        import glob
        old_logs = sorted(glob.glob(str(SKILL_DIR / "logs" / "pipeline_*.log")))[:-5]
        for f in old_logs:
            os.unlink(f)
            heals_applied.append(f"removed old log: {os.path.basename(f)}")

    if not heals_applied:
        log("No auto-heal applied — issue requires manual review")
        log(f"Last 20 lines of failed log:\n{''.join(latest_log.splitlines()[-20:])}")
    else:
        log(f"✅ Heals applied: {heals_applied}")

if __name__ == "__main__":
    run()
