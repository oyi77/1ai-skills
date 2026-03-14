# Disk Analysis Report
**Generated:** 2026-03-09 12:35 UTC+7

---

## **📊 Current Disk Status**

**Filesystem:** /dev/sda2
**Total:** 110 GB
**Used:** 94 GB (91%)
**Available:** 11 GB
**Status:** ⚠️ WARNING - Approaching Critical (95%)

---

## **🔍 Analysis Findings**

### **Largest Directories Analyzed:**

#### **1. Workspace Directories (~8.7 GB total)**
- `workspace/plugins/`: **7.2 GB** (vector-db directory)
- `workspace/skills/`: 442 MB
- `workspace/output/`: 333 MB
- `workspace/berkahkarya-compro/`: 159 MB
- `workspace/hands/`: 56 MB (video clips)
- `workspace/venv|venv-lynk/`: 19 MB + 6 MB
- `workspace/autopilot_affiliate_engine/`: 9.5 MB
- `workspace/logs/`: 1.7 MB
- `workspace/content/`: 1.8 MB
- `workspace/trading/`: 2.2 MB

#### **2. System Directories**
- `/home/openclaw/go`: **916 MB** (Go installation)
- `/home/openclaw/node_modules`: **897 MB** (Node.js dependencies)
- `/home/openclaw/Videos`: 253 MB (video files)

#### **3. OpenClaw Data**
- `~/.openclaw/plugins/vector_db`: Reported **7.5 GB** (but actual files show ~2 MB - possible du reporting issue)
- `~/.openclaw/workspace/`: **8.7 GB**
- `~/.openclaw/vector-cache`: 26 MB
- `~/.openclaw/browser/`: 114 MB
- `~/.openclaw/agents/`: 61 MB
- `~/.openclaw/chroma_db/`: 17 MB

---

## **⚠️ POTENTIAL CANDIDATES FOR CLEANUP**

### **HIGH PRIORITY**

**1. Duplicate/Symlinked Vector DB**
- `~/.openclaw/plugins/vector_db`: 7.5 GB
- `~/.openclaw/workspace/plugins/vector-db`: 7.2 GB
- **Issue:** May be duplicate or hardlink issue
- **Action:** Investigate and remove if duplicate
- **Potential Savings:** 7.2 GB

**2. Node Dependencies**
- `/home/openclaw/node_modules`: 897 MB
- **Context:** Node.js dependencies for development
- **Action:** Remove if not actively used
- **Potential Savings:** 897 MB

**3. Go Installation**
- `/home/openclaw/go`: 916 MB
- **Context:** Go programming language installation
- **Action:** Move to system `/usr/local/go` if possible
- **Potential Savings:** 916 MB (if relocated)

### **MEDIUM PRIORITY**

**4. Video Clips in Workspace**
- `workspace/hands/clip/workspace/`: 56 MB (growing)
- `workspace/output/`: 333 MB
- `workspace/videos/`: 19 MB
- **Context:** Generated video clips for social media
- **Action:** Archive old clips to external storage
- **Potential Savings:** 200-400 MB

**5. Skills Directory**
- `workspace/skills/`: 442 MB
- **Context:** OpenClaw skills (community + custom)
- **Action:** Review unused skills and remove
- **Potential Savings:** 100-200 MB

**6. Compro Directory**
- `workspace/berkahkarya-compro/`: 159 MB
- **Context:** Company presentation materials
- **Action:** Archive if not needed
- **Potential Savings:** 159 MB

### **LOW PRIORITY**

**7. Log Files**
- `workspace/logs/`: 1.7 MB
- **Action:** Compress old logs (already automated)
- **Potential Savings:** Small (<100 MB)

---

## **🎯 Recommended Actions**

### **IMMEDIATE (Critical)**

1. **Investigate Vector DB Duplication**
   ```bash
   # Check if they are same directory (hardlink/symlink)
   ls -li ~/.openclaw/plugins/vector_db
   ls -li ~/.openclaw/workspace/plugins/vector-db

   # Check inode numbers - if same, it's the same files
   ```

2. **Remove Node Dependencies (if not used)**
   ```bash
   rm -rf /home/openclaw/node_modules
   # Or use npm to clean
   npm cache clean --force
   ```

### **URGENT (Before 95%)**

3. **Relocate Go Installation**
   ```bash
   # If not using local Go
   rm -rf /home/openclaw/go
   ```

4. **Archive Old Video Clips**
   ```bash
   # Move clips older than 7 days to archive
   find workspace/hands/clip/workspace/ -mtime +7 -exec mv {} archive/ \;
   ```

### **MAINTENANCE**

5. **Review and Clean Skills**
   ```bash
   # List unused custom skills
   ls workspace/skills/
   # Remove unused ones
   ```

6. **Compress Logs (already automated)**
   - Runs daily at 03:00 AM
   - Old logs auto-compressed

---

## **📈 Estimated Space Savings**

| Action | Potential Savings | Risk | Effort |
|--------|------------------|------|--------|
| Vector DB duplicate removal | **7.2 GB** | Low | Medium |
| Remove node_modules | 897 MB | Low if unused | Low |
| Relocate/Remove Go | 916 MB | Low if unused | Low |
| Archive old videos | 200-400 MB | Low | Medium |
| Cleanup unused skills | 100-200 MB | Medium | Medium |
| Total | **9.3-9.8 GB** | | |

**With Vector DB cleanup: 9.3-9.8 GB → Disk would be ~81% (down from 91%)**
**Without Vector DB:** Only ~2.1 GB → Disk would be ~89% (minimal improvement)

---

## **🚨 CRITICAL FINDING**

The **vector-db directory reporting issue** is the biggest concern:
- `du -sh` shows **7.5 GB**
- Actual files inside show **~2 MB**
- This suggests either:
  1. Hardlinks causing double-counting
  2. `du` command reporting issue
  3. Deleted files still open (process holding references)

**Diagnosis commands:**
```bash
# Check for open but deleted files
lsof +L1 | grep deleted

# Check for hardlinks
find ~/.openclaw/plugins/vector_db -inum $(ls -i ~/.openclaw/workspace/plugins/vector-db | head -1)

# Alternative disk check
ncdu ~/.openclaw/.openclaw/workspace/plugins/vector-db
```

---

## **✅ Next Steps**

1. Run diagnosis on vector-db (HIGH PRIORITY)
2. Check if duplicate (hardlink/symlink)
3. Remove if confirmed duplicate
4. Clean node_modules if not used
5. Monitor disk space trend

---

**Generated by:** Vilona Disk Analysis
**Status:** Investigation required on vector-db
**Follow-up:** Manual diagnosis recommended