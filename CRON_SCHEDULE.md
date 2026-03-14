# JENDRALBOT CRON SCHEDULE
**Automated Daily Execution & Monitoring**

---

## ⏰ CRON JOBS SETUP

### **Job 1: Daily Heartbeat**
**Description:** Check revenue, automation status, rate limits  
**Frequency:** Every 2 hours  
**Command:** Daily heartbeat + report

```bash
0 */2 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py --heartbeat >> logs/daily_heartbeat.log 2>&1
```

**Triggers:**
- 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00
- 16:00, 18:00, 20:00, 22:00 UTC

**Function:**
- Check LYNK dashboard metrics
- Check revenue status (views, clicks, conversions)
- Check rate limit status (HTTP 500 errors)
- Generate daily report
- Send alerts if needed

---

### **Job 2: Instagram Upload Resume**
**Description:** Automatically resume Instagram uploads after rate limit  
**Frequency:** Daily at 12:00 PM UTC+7 (after rate limit likely reset)  
**Command:** Resume Instagram uploads with rate limiting

```bash
0 5 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py --resume instagram >> logs/daily_Instagram.log 2>&1
```

**Triggers:**
- 12:00 PM UTC+7 (5:00 UTC)
- Checks if rate limit cleared
- Resumes 20-30 Instagram posts
- Rate limiting prevents errors

---

### **Job 3: Facebook Upload Start**
**Description:** Start Facebook uploads after Instagram complete  
**Frequency:** Daily at 6:00 PM UTC+7  
**Condition:** When Instagram ≥ 150 posts

```bash
0 11 * * * cd ~/.openclaw/workspace && bash scripts/automation_scheduler.sh >> logs/automator.log 2>&1
```

**Triggers:**
- 6:00 PM UTC+7 (11:00 UTC)
- Checks Instagram completion status
- Starts Facebook batch uploads
- Full 156 posts upload with automation

---

## ⏱️ EXECUTION TIMELINE

### **Today (Day 1):**
- **Now:** Monitor 55 Instagram posts
- **Wait:** 24-48 hours for rate limit
- **Heartbeat:** Every 2 hours checking revenue & status

### **Day 2 (24 hours later):**
- **12:00 PM:** Cron resumes Instagram uploads (20 posts)
- **Check:** Rate limit status cleared?
- **Action:** Resume with rate_limit_aware_upload.py

### **Day 2-3:**
- **Every 2 hours:** Heartbeat checks
- **Daily at 12:00 PM:** More Instagram batches
- **Progress Instagram:** 55 → 156 posts (target)

### **Day 3-4:**
- **Instagram complete:** 156 posts scheduled
- **6:00 PM:** Facebook automation starts
- **Progress Facebook:** 0 → 156 posts (target)

### **Day 5:**
- **All automation complete:** 312 posts scheduled
- **Monitoring:** Daily heartbeat checks
- **Optimization:** Based on revenue data

---

## 📊 MONITORING CHECKLIST

### **Daily (Every 12 Hours):**
- [ ] LYNK dashboard: https://lynk.id/jendralbot
- [ ] Views count checking
- [ ] Clicks tracking
- [ ] Conversions monitoring
- [ ] Revenue confirmation

### **Weekly (Every 7 Days):**
- [ ] Total views across all posts
- [ ] Click-through rate (CTR) analysis
- [ ] Conversion rate optimization
- [ ] Top-performing hooks identification
- [ ] Worst-performing hooks removal

### **Alerts (Automatic):**
- [ ] Revenue generation (first signup)
- [ ] High CTR posts (>2%)
- [ ] Zero conversion posts (>48h)
- [ ] Rate limit cleared status

---

## 🔔 NOTIFICATION SYSTEM

### **Automatic Alerts (via Daily Heartbeat):**

**Status Updates:**
- [ ] Instagram upload resume started
- [ ] Facebook upload started
- [ ] Instagram phase complete
- [ ] Facebook phase complete
- [ ] All automation complete

**Revenue Alerts:**
- [ ] First conversion detected
- [ ] Revenue milestone: IDR 1M
- [ ] Revenue milestone: IDR 5M
- [ ] Revenue milestone: IDR 10M

---

## 💡 AUTOMATION FLOW

```
Heartbeat (Every 2 hours)
    ↓
Check LYNK dashboard metrics
    ↓
Check rate limit status
    ↓
[If rate limit cleared] → Resume uploads
[If not] → Continue monitoring
```

---

## 📋 CRON FILE INSTALLATION

```bash
# Edit crontab
crontab -e

# Add these lines:

# Job 1: Daily heartbeat (every 2 hours)
0 */2 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py --heartbeat >> logs/daily_heartbeat.log 2>&1

# Job 2: Instagram upload resume (daily at 12:00 PM)
0 5 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py --resume instagram >> logs/daily_Instagram.log 2>&1

# Job 3: Facebook automation start (daily at 6:00 PM)
0 11 * * * cd ~/.openclaw/workspace && bash scripts/automation_scheduler.sh >> logs/automator.log 2>&1
```

---

## ⚡ EXECUTION SCRIPTS

### **Manual Execution (Any Time):**

```bash
# Run heartbeat now
cd ~/.openclaw/workspace
python3 scripts/daily_schedule.py --heartbeat

# Resume Instagram uploads now
cd ~/.openclaw/workspace
python3 scripts/daily_schedule.py --resume instagram

# Resume Facebook uploads now
cd ~/.openclaw/workspace
python3 scripts/daily_schedule.py --resume facebook

# Check all statuses
cd ~/.openclaw/workspace
python3 scripts/daily_schedule.py
```

---

## 🎯 COMPLETE AUTOMATION SCHEDULE

**What It Does:**
- ✅ Auto-monitors LYNK dashboard every 2 hours
- ✅ Auto-resumes Instagram when rate limit clears
- ✅ Auto-starts Facebook when Instagram complete
- ✅ Auto-generates daily reports
- ✅ Auto-sends revenue alerts

**Manual Work Required:**
- Only: Install cron jobs (one-time setup)
- Then: Fully automatic execution

---

## 🔥 STATUS

**Automation Schedule:** ✅ READY
**Heartbeat Function:** ✅ READY
**Resume Logic:** ✅ READY
**Full Automation:** ⏳ NEEDS CRON INSTALLATION

---

**Tinggal install cron untuk full automation!** 🚀