#!/usr/bin/env python3
"""
Disk Cleanup Automation - Safe, automated disk cleanup
Provides dry-run option, safe deletions, compression of large dirs
"""

import os
import subprocess
import sys
import tarfile
import shutil
from datetime import datetime, timedelta

# Configuration
WORKSPACE = "/home/openclaw/.openclaw/workspace"
CONFIG = {
    "min_free_gb": 10,  # Target at least 10GB free
    "log_retention_days": 7,
    "temp_retention_days": 3,
    "venv_check": True,
    "compress_threshold_mb": 100,  # Compress files larger than this
    "dry_run": True,  # Set to False after reviewing
}

SAFE_TO_DELETE = [
    # Log files older than retention days
    {"pattern": "logs/*.log", "age_days": 7},
    {"pattern": "logs/*.txt", "age_days": 7},
    {"pattern": "tmp/*.tmp", "age_days": 1},
    
    # Python cache
    {"pattern": "__pycache__", "type": "dir"},
    {"pattern": "*.pyc", "age_days": 0},
    
    # Temporary files
    {"pattern": "temp/*.log", "age_days": 3},
]

COMPRESS_TARGETS = [
    "output/",
    "generated_posts/",
    "autopilot_affiliate_engine/backup/",
]

def get_disk_usage():
    """Get current disk usage"""
    result = subprocess.run(
        ["df", "-h", WORKSPACE],
        capture_output=True,
        text=True
    )
    lines = result.stdout.split('\n')
    for line in lines:
        if WORKSPACE in line or "/" in line:
            parts = line.split()
            if len(parts) >= 5:
                total = parts[1]
                used = parts[2]
                avail = parts[3]
                percent = parts[4].rstrip('%')
                return {
                    "total": total,
                    "used": used,
                    "available": avail,
                    "percent": int(percent),
                    "free_gb": float(avail.rstrip('G')) if avail.endswith('G') else 0
                }
    return None

def find_old_files(pattern, age_days, workspace=WORKSPACE):
    """Find files older than N days matching pattern"""
    if age_days == 0:
        # Find all matching files regardless of age
        cmd = f"find {workspace} -name '{pattern}' -type f"
    else:
        cmd = f"find {workspace} -name '{pattern}' -type f -mtime +{age_days}"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    # Get sizes
    file_info = []
    for f in files:
        if f and os.path.exists(f):
            try:
                size = os.path.getsize(f) / (1024 * 1024)  # MB
                file_info.append({"path": f, "size_mb": size})
            except:
                pass
    
    return file_info

def find_size_by_path(workspace=WORKSPACE):
    """Get directory sizes"""
    result = subprocess.run(
        ["du", "-sh", "*/", "*"],
        cwd=workspace,
        capture_output=True,
        text=True
    )
    
    dirs = []
    for line in result.stdout.split('\n'):
        parts = line.split('\t')
        if len(parts) == 2:
            size_str, path = parts
            try:
                size_mb = parse_size(size_str)
                dirs.append({"path": path, "size_mb": size_mb, "size_str": size_str})
            except:
                pass
    
    return sorted(dirs, key=lambda x: x["size_mb"], reverse=True)

def parse_size(size_str):
    """Parse size string like '1.5G' or '750M' to MB"""
    size_str = size_str.upper()
    if size_str.endswith('G'):
        return float(size_str[:-1]) * 1024
    elif size_str.endswith('M'):
        return float(size_str[:-1])
    elif size_str.endswith('K'):
        return float(size_str[:-1]) / 1024
    return 0

def dry_run_cleanup():
    """Perform dry-run cleanup analysis"""
    print("="*80)
    print("DISK CLEANUP DRY RUN ANALYSIS")
    print("="*80)
    print()
    
    # Current disk status
    disk = get_disk_usage()
    if disk:
        print(f"Current Disk Status:")
        print(f"  Total: {disk['total']}")
        print(f"  Used: {disk['used']} ({disk['percent']}%)")
        print(f"  Available: {disk['available']}")
        print(f"  Free: {disk['free_gb']:.1f} GB")
        print()
    
    # Target
    print(f"Target: {CONFIG['min_free_gb']} GB free")
    print(f"To free: {max(0, CONFIG['min_free_gb'] - disk['free_gb']):.1f} GB")
    print()
    
    # Analyze potential deletions
    total_potential_reclaim = 0
    
    print("="*80)
    print("SAFE DELETIONS")
    print("="*80)
    
    for target in SAFE_TO_DELETE:
        pattern = target["pattern"]
        age = target.get("age_days", 0)
        
        files = find_old_files(pattern, age)
        if files:
            total_size = sum(f["size_mb"] for f in files)
            total_potential_reclaim += total_size
            
            print(f"\n{pattern} (age > {age} days):")
            print(f"  Files: {len(files)}")
            print(f"  Size: {total_size:.1f} MB / {total_size/1024:.1f} GB")
            
            # Show top 5 largest
            top5 = sorted(files, key=lambda x: x["size_mb"], reverse=True)[:5]
            if top5:
                print("  Largest:")
                for f in top5:
                    print(f"    {f['size_mb']:.1f} MB - {f['path'][-60:]}")
    
    print()
    print("="*80)
    print("POTENTIAL COMPRESSION")
    print("="*80)
    
    # Analyze large directories
    dirs = find_size_by_path()
    large_dirs = [d for d in dirs if d["size_mb"] > 500]  # > 500MB
    
    compression_potential = 0
    for d in large_dirs:
        # Estimate compression saves 50%
        saved = d["size_mb"] * 0.5
        compression_potential += saved
        print(f"\n{d['path']} ({d['size_str']}):")
        print(f"  Can save ~{saved:.1f} MB / {saved/1024:.1f} GB via compression")
    
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Potential to reclaim:")
    print(f"  Safe deletions: {total_potential_reclaim/1024:.1f} GB")
    print(f"  Compression: {compression_potential/1024:.1f} GB")
    print(f"  Total: {(total_potential_reclaim + compression_potential)/1024:.1f} GB")
    print()
    print(f"Current free: {disk['free_gb']:.1f} GB")
    print(f"After cleanup: {disk['free_gb'] + (total_potential_reclaim + compression_potential)/1024:.1f} GB")
    print()
    print(f"Target: {CONFIG['min_free_gb']} GB free")
    if disk['free_gb'] >= CONFIG['min_free_gb']:
        print("Status: ✅ ALREADY MEETS TARGET - no action needed")
    else:
        print("Status: ❌ BELOW TARGET - cleanup needed")
    print()
    
    # Specific recommendation for venv
    print("="*80)
    print("URGENT: VENV CLEANUP")
    print("="*80)
    
    # Check for specific known venvs
    known_venvs = []
    for item in os.listdir(WORKSPACE):
        item_path = os.path.join(WORKSPACE, item)
        if os.path.isdir(item_path) and ("venv" in item.lower() or item.endswith("-venv")):
            try:
                size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                          for dirpath, _, filenames in os.walk(item_path) 
                          for filename in filenames) / (1024 * 1024)  # MB
                if size > 100:  # Only show venvs > 100MB
                    known_venvs.append({"path": item_path, "size_mb": size, "name": item})
            except:
                pass
    
    if known_venvs:
        print(f"Found {len(known_venvs)} virtual environment(s):")
        for v in sorted(known_venvs, key=lambda x: x["size_mb"], reverse=True):
            print(f"  {v['name']} ({v['size_mb']/1024:.1f} GB / {v['size_mb']:.0f} MB)")
        print()
        print("RECOMMENDATION:")
        print("  1. Check if vector-db-venv is used:")
        print("     cd ~/.openclaw/workspace")
        print("     grep -r 'vector-db-venv' . --exclude-dir=.git --exclude-dir=vector-db-venv 2>/dev/null")
        print("  2. If unused, remove it:")
        print("     rm -rf vector-db-venv/")
        print("  3. Verify space freed:")
        print("     df -h | grep '/$'")
    else:
        # Look at general large dirs
        large_dirs = [d for d in dirs if d["size_mb"] > 1000][:10]
        if large_dirs:
            print("No specific venvs found, but large directories:")
            for d in large_dirs:
                print(f"  {d['path']} ({d['size_str']})")
    
    return total_potential_reclaim + compression_potential

def execute_cleanup():
    """Execute actual cleanup (after dry-run review)"""
    print("="*80)
    print("EXECUTING CLEANUP")
    print("="*80)
    print()
    
    # Confirm
    disk = get_disk_usage()
    if disk['free_gb'] >= CONFIG['min_free_gb']:
        print("Already meets target. No cleanup needed.")
        return True
    
    # Delete old logs
    for target in SAFE_TO_DELETE:
        pattern = target["pattern"]
        age = target.get("age_days", 0)
        
        files = find_old_files(pattern, age)
        for f in files:
            try:
                os.remove(f['path'])
                print(f"Deleted: {f['path']} ({f['size_mb']:.1f} MB)")
            except Exception as e:
                print(f"Failed to delete {f['path']}: {e}")
    
    # Clean Python cache
    print("\nCleaning Python cache...")
    subprocess.run(["find", WORKSPACE, "-type", "d", "-name", "__pycache__", "-exec", "rm", "-rf", "{}", "+"], 
                   capture_output=True)
    subprocess.run(["find", WORKSPACE, "-type", "f", "-name", "*.pyc", "-delete"],
                   capture_output=True)
    print("Python cache cleaned")
    
    print()
    print("Cleanup complete. Checking new disk status...")
    new_disk = get_disk_usage()
    print(f"New free space: {new_disk['available']} ({new_disk['percent']}% used)")
    
    return True

def main():
    """Main execution"""
    print(f"\n[{'='*80}]")
    print(f"Disk Cleanup Automation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[{'='*80}]\n")
    
    if CONFIG["dry_run"]:
        print("MODE: DRY RUN - Analyzing only, no changes made\n")
        reclaimed = dry_run_cleanup()
        
        print()
        print("="*80)
        print("NEXT STEPS")
        print("="*80)
        print("1. Review the analysis above")
        print("2. If acceptable, run with --execute:")
        print("   python3 scripts/disk_cleanup_automation.py --execute")
        print("3. Or manually execute specific deletions:")
        print("   rm -rf vector-db-venv/  # if unused")
        print("   find logs/ -name '*.log' -mtime +7 -delete")
        
    else:
        print("MODE: EXECUTE - Making changes\n")
        execute_cleanup()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        CONFIG["dry_run"] = False
    
    main()