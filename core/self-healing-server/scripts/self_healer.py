#!/usr/bin/env python3
"""
Self-Healing Home Server
Monitors and auto-repairs critical services on Kali Linux / OpenClaw setup
"""
import subprocess, sys, os, json
from datetime import datetime
from pathlib import Path

CRITICAL_SERVICES = {
    "openclaw-gateway": {"type": "user", "restart": True},
    "omniroute": {"type": "system", "restart": True},
    "cloudflared": {"type": "system", "restart": True},
    "xvfb": {"type": "system", "restart": True},
}

DISK_WARN = 90
DISK_CRIT = 95
MEM_WARN_MB = 500

def run(cmd, **kwargs):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    return r.stdout.strip(), r.returncode

def check_services():
    issues = []
    for svc, cfg in CRITICAL_SERVICES.items():
        flag = "--user" if cfg["type"] == "user" else ""
        _, code = run(f"systemctl {flag} is-active {svc} >/dev/null 2>&1")
        if code != 0:
            issues.append({"service": svc, "type": cfg["type"], "status": "down"})
    return issues

def check_disk():
    out, _ = run("df / --output=pcent | tail -1 | tr -d '%'")
    pct = int(out.strip())
    if pct >= DISK_CRIT:
        return {"level": "critical", "usage": pct, "action": "cleanup"}
    elif pct >= DISK_WARN:
        return {"level": "warning", "usage": pct, "action": "monitor"}
    return {"level": "ok", "usage": pct}

def check_memory():
    out, _ = run("free -m | awk '/^Mem:/{print $7}'")
    avail = int(out.strip())
    if avail < MEM_WARN_MB:
        return {"level": "warning", "available_mb": avail}
    return {"level": "ok", "available_mb": avail}

def check_network():
    _, code = run("ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1")
    return {"level": "ok" if code == 0 else "down"}

def auto_repair(issues):
    repaired = []
    for issue in issues:
        svc = issue["service"]
        flag = "--user" if issue["type"] == "user" else ""
        _, code = run(f"systemctl {flag} restart {svc}")
        repaired.append({"service": svc, "restarted": code == 0})
    return repaired

def send_alert(text):
    run(f'openclaw system event --text "{text}" --mode now 2>/dev/null')

def generate_report():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    svc_issues = check_services()
    disk = check_disk()
    mem = check_memory()
    net = check_network()
    
    alerts = []
    repaired = []
    
    if svc_issues:
        repaired = auto_repair(svc_issues)
        alerts.append(f"⚠️ Services down: {[i['service'] for i in svc_issues]}")
    
    if disk["level"] != "ok":
        alerts.append(f"💾 Disk {disk['level']}: {disk['usage']}%")
        if disk["level"] == "critical":
            run("find /home/openclaw/.openclaw/workspace/logs -name '*.log' -size +10M -exec truncate -s 5M {} \\;")
    
    if mem["level"] != "ok":
        alerts.append(f"🧠 Memory low: {mem['available_mb']}MB available")
    
    if net["level"] != "ok":
        alerts.append("🌐 Network DOWN")

    report = f"""# System Health Report — {now}

## Services: {"✅ All OK" if not svc_issues else f"⚠️ {len(svc_issues)} down, {len([r for r in repaired if r['restarted']])} repaired"}
## Disk: {disk['usage']}% used {"✅" if disk['level']=='ok' else '⚠️'}
## Memory: {mem['available_mb']}MB available {"✅" if mem['level']=='ok' else '⚠️'}
## Network: {"✅ OK" if net['level']=='ok' else '❌ DOWN'}

{"## Alerts:\\n" + chr(10).join(alerts) if alerts else "## All systems healthy ✅"}
"""
    
    if alerts:
        send_alert(f"🚨 Self-Healer: {len(alerts)} issues detected and auto-repaired where possible")
    
    return report

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["check","repair","report"], default="report")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    
    if args.action == "check":
        issues = check_services()
        print(json.dumps({"services": issues, "disk": check_disk(), "memory": check_memory(), "network": check_network()}, indent=2))
    elif args.action == "repair":
        issues = check_services()
        repaired = auto_repair(issues)
        print(json.dumps(repaired, indent=2))
    else:
        report = generate_report()
        if not args.quiet:
            print(report)
        log_path = Path("logs/self_healer.log")
        log_path.parent.mkdir(exist_ok=True)
        log_path.write_text(report)
