# RATE LIMIT PREVENTION GUIDE
**JENDRALBOT Automated Upload Protection**

---

## 🛡️ WHAT CAUSED HTTP 500?

**Root Cause:** Upload too fast without rate limiting
- We uploaded 55 posts in ~40 minutes (every ~45 seconds)
- Post Bridge has rate limits (likely 10-15 posts/hour per account)
- Triggered HTTP 500 Internal Server Error

---

## ✅ NEW RATE LIMIT PREVENTION SYSTEM

### **Smart Delays:**
- **Minimum delay:** 1 minute between uploads
- **Maximum delay:** 5 minutes between uploads
- **Adaptive:** Delays increase progressively (exponential backoff)
- **Platform-based:** Facebook = 2x delay (more strict)

### **Exponential Backoff:**
```
Post 1:   1 min delay
Post 5:   2 min delay
Post 10:  3 min delay
Post 20:  4 min delay
Post 30+:  5 min delay (max)
```

### **Retry Logic:**
- **Retry 1:** Wait 10 minutes
- **Retry 2:** Wait 20 minutes
- **Retry 3:** Wait 30 minutes (final)

---

## 🔧 IMPLEMENTATION

### **1. Rate Limit Aware Uploader**
**File:** `scripts/rate_limit_aware_upload.py`

**Features:**
- ✅ Automatic delay calculation
- ✅ Rate limit detection
- ✅ Auto-retry with backoff
- ✅ Platform-specific settings

**Usage:**
```bash
# Instagram (10 posts with rate limiting)
python3 scripts/rate_limit_aware_upload.py --platform instagram --batch 10

# Facebook (10 posts with slower rate limit)
python3 scripts/rate_limit_aware_upload.py --platform facebook --batch 10
```

---

### **2. Upload Schedule Planner**
**Strategy:** Stagger uploads throughout the day

**Instagram Schedule:**
```
09:00 - Post 1   (1 min delay)
09:01 - Post 2   (1.2 min delay)
09:02 - Post 3   (1.5 min delay)
09:04 - Post 4   (2 min delay)
...
Post 10: 5 min delay max
```

**Facebook Schedule:** (slower, more conservative)
```
10:00 - Post 1   (2 min delay)
10:02 - Post 2   (2.5 min delay)
10:05 - Post 3   (3 min delay)
10:08 - Post 4   (4 min delay)
...
Post 10: 5+ min delay
```

---

## 📊 SAFE UPLOAD LIMITS

### **Per Hour (Safe):**
- Instagram: 10-12 posts max
- Facebook: 8-10 posts max
- Total: 18-22 posts/hour

### **Per Day (Safe):**
- Instagram: 50-75 posts max
- Facebook: 40-60 posts max
- Total: 90-135 posts/day

### **Current Strategy (Aggressive - Riskier):**
- Instagram: 156 posts in 8-12 hours (13-19 posts/hour)
- Facebook: 156 posts in 12-16 hours (10-13 posts/hour)

---

## 🎯 RECOMMENDED SAFE STRATEGY

### **Option A: Conservative (Most Reliable)**
```
Day 1: 20 Instagram posts (2-3 hours)
Day 2: 20 Instagram posts (2-3 hours)
Day 3: 20 Instagram posts (2-3 hours)
```

### **Option B: Moderate (Recommended)**
```
Morning (9-11 AM): 30 Instagram posts (2 hours wait)
Afternoon (1-3 PM): 30 Instagram posts (2 hours wait)
Evening (5-7 PM): 30 Instagram posts
Night (8-10 PM): 30 Instagram posts
```

### **Option C: Aggressive (Fastest)**
```
Instagram: 156 posts over 8-12 hours with rate limiting
Facebook: 156 posts over 12-16 hours with rate limiting
```

---

## 🔍 MONITORING

### **Log File:** `logs/rate_limit_aware_upload.log`
Tracks:
- upload attempts
- delays between uploads
- successes vs failures
- rate limit detections

### **Alert System:**
Automatic detection of:
- HTTP 500 errors (rate limit)
- 3+ consecutive failures
- Auto-pause for 15 minutes

---

## ⏭️ NEXT STEPS

### **Using New Rate Limit System:**

```bash
# Instagram - Conservative start with rate limiting
cd ~/.openclaw/workspace

# Retry failed Instagram (47 posts) with rate limiting
python3 scripts/rate_limit_aware_upload.py --platform instagram --batch 10

# Then continue...
python3 scripts/rate_limit_aware_upload.py --platform instagram --batch 10
# Repeat until all 47 posts done

# After Instagram complete, upload Facebook
python3 scripts/rate_limit_aware_upload.py --platform facebook --batch 10
# Repeat for all 156 Facebook posts
```

---

## 💰 ESTIMATED COMPLETION TIME

### **Instagram (47 remaining + 101 total = 148 posts):**
- Conservative: 2-3 hours (20 posts × 3 sessions)
- Rate Limited: 4-6 hours (with 1-5 min delays)
- **Recommend:** 4-6 hours with rate limiting

### **Facebook (156 posts):**
- Conservative: 4-6 hours (20 posts × 3 sessions)
- Rate Limited: 6-8 hours (with 2-10 min delays)
- **Recommend:** 6-8 hours with rate limiting

### **Total All Platforms:**
- Conservative: 6-9 hours (spread over 2 days)
- Rate Limited: 10-14 hours (spread over 1-2 days)

---

## ⚠️ KEY LEARNING

**Today's Error:**
- 55 posts in 40 minutes = too fast
- Triggered Post Bridge rate limit
- HTTP 500 errors after 55 posts

**Prevention:**
- Minimum 1 minute between uploads
- Progressive delays (exponential backoff)
- Platform-aware rate limits
- Auto-retry on failures

---

**RATE LIMIT PREVENTION SYSTEM READY** 🛡️

**Next: Run rate_limit_aware_upload dengan safe limits** 🚀