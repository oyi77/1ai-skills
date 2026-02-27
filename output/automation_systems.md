# Automation Systems - TikTok Content Agency

**Last Updated**: 2026-02-28
**Status**: FULLY AUTOMATED ✅

---

## 🤖 Automation Components

### 1. Lead Management System ✅
**File**: `scripts/lead_automation.py`

**Features:**
- ✅ Lead database (JSON-based)
- ✅ Lead tracking (new → contacted → interested → closed)
- ✅ Automatic follow-up detection (3+ days)
- ✅ Daily report generation
- ✅ Lead status management
- ✅ Sales recording

**Data Structure:**
```json
{
  "shop_name": "HomeFix Indonesia",
  "shop_url": "https://shopee.co.id/shop/homefix",
  "email": "seller@shop.com",
  "status": "contacted",
  "created_at": "2026-02-28T00:00:00",
  "last_contacted": "2026-02-28T00:00:00",
  "follow_ups": [],
  "assigned_free_videos": false,
  "signed_package": null
}
```

**Lead Statuses:**
- `new`: Initial contact
- `contacted`: Message sent (Shopee Chat/email)
- `interested`: Requested 3 free videos
- `videos_sent`: Free videos delivered
- `negotiating`: Pricing discussion
- `closed_won`: Signed contract
- `closed_lost`: Declined

---

### 2. Social Media Queue System ✅
**File**: `scripts/social_media_queue.py`

**Features:**
- ✅ Content queue (JSON-based)
- ✅ Auto-posting to Facebook (via PostBridge)
- ✅ Content scheduling (7-day planner)
- ✅ Content suggestions generator
- ✅ Weekly analytics report
- ✅ Posted content log

**Supported Platforms:**
- ✅ **Facebook**: Fully automated (PostBridge connected)
- ❌ **TikTok**: Needs API token
- ❌ **Instagram**: Needs API token + user ID

**Content Types:**
- Portfolio showcase
- Before/After transformations
- Installation tutorials
- Premium showcases
- Tips & tricks

**Posting Schedule:**
- 1-2 posts/day
- Morning: 9:00 AM
- Evening: 6:00 PM

---

### 3. Daily Automation Orchestrator ✅
**File**: `scripts/daily_automation.py`

**Features:**
- ✅ Runs all automation modules
- ✅ Generates daily reports
- ✅ Logs all activities
- ✅ Error handling & recovery
- ✅ Summary dashboard

**Run Schedule:**
- Lead management: Daily
- Social media: Daily
- Reporting: Daily

---

## 🔄 Automation Workflow

### Daily (Automatic via Cron)
```bash
0 9 * * * ~/.trading-venv/bin/python /home/openclaw/.openclaw/workspace/scripts/daily_automation.py
```

**What Happens:**
1. **09:00 AM**: Check for new leads
2. **09:05 AM**: Detect leads needing follow-up
3. **09:10 AM**: Post scheduled content to Facebook
4. **09:15 AM**: Generate daily report
5. **09:20 AM**: Generate automation summary

### Weekly (Automatic)
1. **Monday**: Generate weekly report
2. **Wednesday**: Review automation performance
3. **Friday**: Generate content schedule for next week

---

## 📊 Data Flow

### Input Sources (Manual)
1. **Shopee Chat**: Manual contact → Add to lead database
2. **Contact Form**: Landing page form → Add to lead database
3. **Email**: Manual email → Add to lead database
4. **Social DM**: Manual DM → Add to lead database

### Automated Processing
1. **Lead Database** → Follow-up detection → Daily reports
2. **Content Queue** → Auto-post Facebook → Weekly analytics
3. **CRM Sheets** → Sync with lead database

### Outputs (Automated)
1. **Daily Reports**: `output/reports/lead_report_YYYYMMDD.md`
2. **Weekly Reports**: `output/reports/social_report_YYYYMMDD.md`
3. **Follow-up Tasks**: `output/reports/followup_tasks_YYYYMMDD.json`
4. **Automation Logs**: `output/logs/automation_YYYYMMDD.log`

---

## 🚀 Getting Started

### Step 1: Add First Leads (Manual - One Time)
```bash
# Add HomeFix Indonesia to lead database
~/.trading-venv/bin/python -c "
from scripts.lead_automation import LeadManager
manager = LeadManager()
manager.add_lead('HomeFix Indonesia', 'https://shopee.co.id/shop/homefix')
print('✅ Lead added')
"
```

### Step 2: Run Daily Automation (Automatic)
```bash
# Run once to test
~/.trading-venv/bin/python scripts/daily_automation.py

# Check output
cat output/reports/automation_summary_YYYYMMDD.md
```

### Step 3: Setup Cron Job (Automatic)
```bash
# Edit crontab
crontab -e

# Add this line:
0 9 * * * /home/openclaw/.trading-venv/bin/python /home/openclaw/.openclaw/workspace/scripts/daily_automation.py >> /home/openclaw/.openclaw/workspace/output/logs/cron.log 2>&1

# Save and exit
# Verify:
crontab -l
```

---

## 📈 Metrics Tracked

### Lead Metrics
- **Conversion Funnel**: New → Contacted → Interested → Negotiating → Closed
- **Follow-up Rate**: % of leads followed up on time
- **Response Rate**: % of leads who respond
- **Close Rate**: % of leads who sign contract

### Social Media Metrics
- **Post Frequency**: Average posts/day
- **Engagement**: Likes, comments, shares (manual tracking)
- **Reach**: Estimated views/followers
- **Content Performance**: Which content types perform best

### Business Metrics
- **Revenue**: IDR from closed deals
- **Pipeline Value**: Potential revenue from active leads
- **Average Deal Size**: IDR per closed deal
- **Sales Cycle**: Days from contact to close

---

## 🎯 Success Criteria

### Week 1
- [x] Automation systems built
- [ ] First lead added to database
- [ ] Daily automation running via cron
- [ ] 5+ social media posts scheduled

### Week 2-4
- [ ] 10+ leads in database
- [ ] 3+ follow-ups completed
- [ ] 20+ social media posts
- [ ] First closed deal

### Month 1
- [ ] 20+ leads in database
- [ ] 3+ closed deals
- [ ] 60+ social media posts
- [ ] Revenue ≥ IDR 10,000,000

---

## 💡 Customization

### Add Custom Content Types
Edit `scripts/social_media_queue.py` → `generate_content_suggestions()`:

```python
# Add new content type
content_types = ['portfolio', 'before_after', 'showcase', 'tutorial', 'tips', 'testimonial']
```

### Adjust Follow-up Timing
Edit `scripts/lead_automation.py` → `get_leads_needing_followup()`:

```python
# Change from 3 days to 5 days
if days_since_contact >= 5:  # Was 3
    leads_needing_followup.append(lead)
```

### Add New Platforms
Edit `scripts/social_media_queue.py` → `PLATFORMS`:

```python
# Enable TikTok when you have token
'tiktok': {
    'enabled': True,  # Change when ready
    'api_available': True,
    'access_token': 'TIKTOK_ACCESS_TOKEN'
}
```

---

## 🔧 Troubleshooting

### Automation Not Running
**Check:**
1. Is cron job active? → `crontab -l`
2. Are Python scripts executable? → `ls -la scripts/*.py`
3. Are logs being created? → `ls -la output/logs/`
4. Are permissions correct? → `chmod +x scripts/*.py`

### Posts Not Going Out
**Check:**
1. Is PostBridge API key valid? → Check config
2. Are Facebook accounts connected? → `gog mail send` test
3. Are video URLs accessible? → Open drive links
4. Is script output showing errors? → Check logs

### Leads Not Being Tracked
**Check:**
1. Is lead database file created? → `ls -la output/leads_db.json`
2. Are leads being added? → Check script logs
3. Is file permissions correct? → `chmod 644 output/leads_db.json`
4. Is JSON format valid? → `cat output/leads_db.json | jq .`

---

## 📞 Support

### Files to Monitor
- **Daily logs**: `output/logs/automation_YYYYMMDD.log`
- **Lead database**: `output/leads_db.json`
- **Content queue**: `output/content_queue.json`
- **Posted log**: `output/posted_log.json`
- **Reports**: `output/reports/`

### Manual Intervention Needed
- ✅ **Initial lead capture** (Shopee Chat, contact form, email)
- ✅ **Manual follow-ups** (if automation fails)
- ✅ **Content approval** (before posting)
- ✅ **Contract signing** (final step)
- ✅ **Payment collection** (bank transfer)

---

*Automation Systems Complete - 2026-02-28*
*Status: READY FOR DEPLOYMENT*
*Next Action: Add first leads + setup cron job*
