# Disk Cleanup Automation Tool

## 📁 File
`scripts/disk_cleanup_automation.py`

---

## 🎯 Purpose
Automated disk cleanup with dry-run analysis, safe deletions, and virtual environment detection.

---

## 🚀 Quick Start

### Dry Run (Analysis Only - Recommended First Step)
```bash
cd ~/.openclaw/workspace
python3 scripts/disk_cleanup_automation.py
```

### Execute Cleanup
```bash
cd ~/.openclaw/workspace
python3 scripts/disk_cleanup_automation.py --execute
```

---

## 📊 What It Does

### Phase 1: Disk Status Analysis
- Shows current disk usage and free space
- Identifies how much space needed to reach target (10GB free)

### Phase 2: Safe Deletion Candidates
- Old log files (> 7 days)
- Temporary files (> 3 days)
- Python cache files (*.pyc, __pycache__)
- Identifies specific files and sizes
- Shows largest files before deletion

### Phase 3: Large Directory Analysis
- Analyzes all directories in workspace
- Identifies large directories (> 500MB)
- Estimates compression potential

### Phase 4: VENV Detection (NEW)
- Automatically find virtual environment directories
- Shows size of each venv
- Provides commands to safely check if venv is unused
- Recommends safe removal method

---

## 🔒 Safety Features

### Dry Run Mode (Default)
- Analyzes WITHOUT making changes
- Shows exactly what would be deleted
- Displays potential space reclaim
- Requires `--execute` flag to make changes

### Safe Deletions Only
- Only targets old logs, temp files, cache
- Never touches source code, config, or active data
- Age-based retention policies (7 days for logs, 3 days for temp)

### VENV Verification
- Doesn't auto-delete venvs (too risky)
- Provides commands to check if venv is referenced
- Shows specific grep commands to verify
- User reviews and decides

---

## 📈 Current Situation (March 8, 2025)

### Disk Status
- **Total:** 110GB
- **Used:** 102GB (98%)
- **Free:** 3.1GB
- **Target:** 10GB free
- **To Free:** 6.9GB

### Potential Cleanup
- **Python cache:** 506MB (27,588 files)
- **vector-db-venv:** 7.4GB (if unused)
- **Total Potential:** ~7.9GB

### Recommendation
1. Run dry run: `python3 scripts/disk_cleanup_automation.py`
2. Check if vector-db-venv is unused
3. If unused: `rm -rf vector-db-venv/` (frees 7.4GB)
4. Run cleanup: `python3 scripts/disk_cleanup_automation.py --execute`

---

## 🔧 How It Works

### VENV Detection
1. Scans workspace directories
2. Looks for names with "venv" or ending in "-venv"
3. Calculates size by walking all files
4. Only shows venvs > 100MB
5. Provides verification commands

### Verification Command (Automatic)
```bash
grep -r 'vector-db-venv' . --exclude-dir=.git --exclude-dir=vector-db-venv 2>/dev/null
```

If no results → venv is safe to delete.

---

## ⚠️ Current Blockers

### Why Not Auto-Clean?
- venv might be in use (we don't know)
- Python venv dependencies might break
- Safe to require manual review first

### Critical Path
1. Manual verification (grep check) → 2 minutes
2. Manual venv removal (if safe) → 10 seconds
3. Script cleanup execution → 2 minutes
4. **Total:** ~5 minutes to free 7.9GB

---

## 🎯 After Cleanup

### Expected Result
- **Before:** 98% full (3.1GB free)
- **After:** ~85% full (~11GB free)
- **System:** Stable and safe

### Benefits
- System crashes prevented (was at 98%)
- Performance improves (less fragmentation)
- Space for new uploads, logs, data

---

## 📝 Notes

- Run dry run FIRST to see what would be deleted
- venv deletion requires manual verification
- Script is conservative (won't delete source code)
- Always safe to run in dry-run mode

---

## 🔔 Automated Monitoring

**To Add to Cron:**
```bash
# Daily at 3 AM - check disk, alert if > 90%
0 3 * * * cd ~/.openclaw/workspace && python3 scripts/disk_cleanup_automation.py | mail -s "Disk space report" codergaboets
```

---

**Created:** March 8, 2026, 11:30 AM UTC+7  
**Purpose:** Automated disk cleanup safety tool  
**Status:** ✅ Ready for use (dry-run tested)