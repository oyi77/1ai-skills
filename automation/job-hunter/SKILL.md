---
name: job-hunter
description: Use when autonomous job hunting agent with state tracking, tailored applications,
  ATS optimization, and multi-platform search across LinkedIn, Indeed, and Glassdoor.
  Use when working with job hunter.
domain: automation
author: oyi77
license: Apache-2.0
subdomain: workflow-automation
tags:
- ai-agent
- automation
- hunter
- job
- productivity
- workflow
version: 1.0.0
category: automation
---

# Job Hunter

## When to Use

**Trigger phrases:**
- "job hunter"
- "Help me with job hunter"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


I am an advanced, state-aware job hunting agent. I don't just search; I remember what I've seen, track what I've applied to, and tailor my approach for every single job.


## When NOT to Use

- For one-off tasks that will never repeat
- When the process requires human judgment at every step
- When the cost of automation exceeds the cost of manual execution


## Overview

Job Hunter automates workflow automation to reduce manual effort and increase reliability.

The modern job search is a funnel: discover → score → tailor → submit → follow up → analyze. Each stage has measurable KPIs — response rate per platform, interview conversion, offer rate — that compound when optimized systematically. A human juggling 20+ applications across LinkedIn, Indeed, and Glassdoor cannot track this state manually without errors and missed follow-ups.

An autonomous job-hunting agent maintains persistent state across the entire search. It remembers every job it has seen, scored, applied to, followed up on, and where each stands. This state prevents duplicate effort (the same job posted on LinkedIn and Indeed is caught once), enables trend analysis (which role titles convert best, which platforms yield the highest response rate), and powers automated follow-up sequences that increase callback rates by 30-50% over no follow-up.

The core technical stack involves web scraping or API-based integration with job platforms, a text-similarity scorer (TF-IDF or embedding-based) to match job descriptions against the target profile, a document generation engine for tailored resumes and cover letters, and a state database (SQLite, JSON-backed) for cross-session persistence. Optional additions include email open tracking (via tracking pixel) for follow-up analytics and a lightweight classifier to score job fit beyond simple keyword matching.

The architecture follows an event-driven pipeline: a new job is discovered during the daily sweep → scored against the user's profile → if above the high threshold, the agent generates a tailored resume and cover letter → submits via the platform's apply flow or external redirect → records the application in state → schedules the 7/14/21-day follow-up sequence → logs outcome for weekly analytics. This pipeline runs on a daily cron by default, with a weekly analytics summary and bi-weekly strategy adjustments based on conversion data.

## Workflow

```python
# Example: Workflow automation
import schedule
import time

def run_workflow():
    data = fetch_data()
    processed = transform(data)
    deliver(processed)

schedule.every().hour.do(run_workflow)
while True:
    schedule.run_pending()
    time.sleep(60)
```

1. **Define triggers** — Set up events or schedules that initiate the automation
2. **Configure inputs** — Specify data sources and parameters
3. **Design pipeline** — Define the sequence of automated steps
4. **Add error handling** — Set up retries, alerts, and fallback paths
5. **Test end-to-end** — Validate the full automation with realistic data
6. **Deploy and monitor** — Activate and track performance
7. **Analyze and iterate** — Review weekly metrics: applications per platform, interview rate, offer rate, acceptance rate. Adjust scoring thresholds, keyword bank, and platform allocation based on conversion data. Archive underperforming strategies. Run a monthly comp review against market rates to keep salary targets aligned.

## Configuration

- Set trigger conditions (schedule, webhook, event)
- Define input validation rules
- Configure notification channels for alerts
- Set retry policies and timeout limits
- **Python install**: `pip install requests beautifulsoup4 lxml sqlite3` — for scraping, ATS parsing, and state persistence
- **Node.js install**: `npm install puppeteer better-sqlite3 nodemailer` — for browser automation, app tracking DB, and follow-up dispatch
- **System deps**: `sudo apt install libreoffice-writer` (converts .docx for ATS re-parsing) or `brew install pandoc`
- **Resume validation**: Run every modified resume through `python ats_validate.py resume.docx` before each submission batch
- **Email SMTP config**: Set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` in `.env` for automated follow-up dispatch
- **State DB init**: `python init_db.py` creates SQLite tables for applications, follow-ups, interviews, analytics
- **Scoring thresholds** in `config.yaml`: `score_threshold_high: 0.80`, `score_threshold_medium: 0.55`, `score_threshold_low: 0.30`

## Best Practices

- Start with simple automations and iterate
- Add logging at every step for debugging
- Use idempotent operations where possible
- Test with edge cases before deploying

## Code Examples

### Python — Job Search Aggregator with Dedup and Scoring

```python
import json
import hashlib
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class JobPosting:
    company: str
    title: str
    location: str
    url: str
    platform: str
    description: str
    posted: str

    def dedup_hash(self) -> str:
        """Normalize duplicate jobs across platforms by company+title+location."""
        return hashlib.sha256(
            f"{self.company.lower().strip()}|{self.title.lower().strip()}|{self.location.lower().strip()}".encode()
        ).hexdigest()

class JobHuntTracker:
    def __init__(self, db_path: str = "job_hunt.json"):
        self.seen: set[str] = set()
        self.applications: list[dict] = []
        self.db_path = db_path

    def score_job(self, job: JobPosting, keywords: list[str]) -> float:
        """Score a job description against target keywords (0.0 - 1.0)."""
        desc = job.description.lower()
        matches = sum(1 for kw in keywords if kw.lower() in desc)
        return min(matches / len(keywords), 1.0) if keywords else 0.0

    def submit_if_qualified(self, job: JobPosting, threshold: float = 0.65):
        h = job.dedup_hash()
        if h in self.seen:
            return  # already processed
        self.seen.add(h)
        score = self.score_job(job, ["machine learning", "python", "aws", "kubernetes", "pytorch"])
        if score >= threshold:
            record = asdict(job) | {"score": score, "status": "applied", "applied_at": datetime.utcnow().isoformat()}
            self.applications.append(record)
            # generate_tailored_resume(job)  # integration point
            # submit_application(job)          # integration point
        elif score >= threshold - 0.2:
            self.applications.append(asdict(job) | {"score": score, "status": "flagged"})
```

### JavaScript — Application State Tracking with Follow-up Scheduler

```javascript
import Database from 'better-sqlite3';

export class ApplicationTracker {
  private db: Database.Database;

  constructor(dbPath = './job_hunt.db') {
    this.db = new Database(dbPath);
    this.db.pragma('journal_mode = WAL');
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL, title TEXT NOT NULL,
        platform TEXT, url TEXT,
        status TEXT DEFAULT 'applied',
        applied_at TEXT NOT NULL,
        followup_day7 INTEGER DEFAULT 0,
        followup_day14 INTEGER DEFAULT 0,
        notes TEXT
      );
      CREATE INDEX IF NOT EXISTS idx_status ON applications(status);
    `);
  }

  recordApplication(company: string, title: string, platform: string, url: string) {
    const stmt = this.db.prepare(
      'INSERT INTO applications (company, title, platform, url, applied_at) VALUES (?, ?, ?, ?, ?)'
    );
    return stmt.run(company, title, platform, url, new Date().toISOString()).lastInsertRowid;
  }

  scheduleFollowUps() {
    const now = Date.now();
    const pending = this.db.prepare(
      `SELECT * FROM applications WHERE status = 'applied' AND (followup_day7 = 0 OR followup_day14 = 0)`
    ).all() as any[];

    for (const app of pending) {
      const daysSince = (now - new Date(app.applied_at).getTime()) / 86_400_000;
      if (daysSince >= 7 && !app.followup_day7) {
        // sendFollowUpEmail(app, 7);  // integration point
        this.db.prepare('UPDATE applications SET followup_day7 = 1 WHERE id = ?').run(app.id);
      }
      if (daysSince >= 14 && !app.followup_day14) {
        // sendFollowUpEmail(app, 14);  // integration point
        this.db.prepare('UPDATE applications SET followup_day14 = 1 WHERE id = ?').run(app.id);
      }
    }
  }

  weeklyReport() {
    const stats = this.db.prepare(`
      SELECT status, COUNT(*) as count FROM applications GROUP BY status
    `).all();
    console.table(stats);
  }
}
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |
| "ATS optimization is one-time" | Job descriptions change weekly as market demands shift. Re-optimize keyword bank and resume bullets every 2 weeks to stay relevant. |
| "I'll remember which jobs I applied to" | After 20+ applications across 3+ platforms, human recall fails. A state database catches dedup, tracks status per job, and never forgets a follow-up deadline. |
| "Cover letters don't matter anymore" | 47% of hiring managers skip applications without a cover letter. A personalized first paragraph referencing recent company news can double your callback rate. |


## Process

### Preparation

1. **Profile assembly** — Create a structured profile JSON with current resume text, skills inventory, target roles, seniority level, salary floor/ceiling, location preferences, work authorization status, and links to portfolio/GitHub/LinkedIn.
2. **Platform reconnaissance** — Determine which job boards cover your target industry. Tech: LinkedIn + Indeed + Stack Overflow Jobs. Finance: LinkedIn + Glassdoor + eFinancialCareers. Creative: LinkedIn + Behance + Dribbble. Configure credentials accordingly.
3. **ATS baseline test** — Run your base resume through an ATS simulator (e.g., Jobscan, ResumeWorded). Fix parsing issues: no columns, no tables, no graphics, no headers/footers with text, standard section names. Establish a baseline score.
4. **Keyword bank curation** — Collect 50-100 role-specific keywords from 10-15 ideal job descriptions. Organize by category (languages, frameworks, methodologies, soft skills, domain knowledge). These feed the tailoring engine.
5. **State database initialization** — Set up the state tracking database with tables for applications, follow-ups, interviews, and analytics. Configure the first-run to prompt for missing information.

### Execution

1. **Daily discovery sweep** — Run searches across all configured platforms. Deduplicate against the seen set. Score new listings against the profile. For high-score jobs (≥ threshold), generate tailored resume + cover letter. For medium-score jobs, flag for manual review. For low-score jobs, archive silently.
2. **Tailored submission** — For each qualified job: (a) rewrite resume swapping generic bullets for role-specific achievements using keywords; (b) generate cover letter referencing company's recent product/blog/news; (c) submit via platform or external link; (d) record in state database with submission timestamp.
3. **Manual intervention handoff** — Jobs requiring referrals, portfolio uploads, writing samples, or multi-step applications get flagged. The agent prepares a briefing packet (job description, company research, tailored resume, cover letter draft) for the human to complete.
4. **Follow-up waves** — Day 7: polite re-express-interest email referencing the application. Day 14: brief update mentioning any recent relevant achievement. Day 21: graceful close — ask to be kept in mind for future roles. Track open rates if email tracking is enabled.

### Stewardship

1. **Weekly analytics review** — Generate a report: applications sent, response rate by platform, interview invite rate, offer rate, average salary offered vs expected. Compare week-over-week trends.
2. **Profile refresh** — Every 2 weeks, ask: new skills learned? projects completed? certifications earned? Updated the profile and re-run keyword analysis on recent ideal jobs to catch shifting market demands.
3. **Strategy pivot** — If response rate < 5% on a platform, reduce allocation. If interview conversion < 10%, audit resume quality. If a particular role title or industry consistently converts well, increase targeting weight.
4. **Network amplification** — Notify about applications where the human has a 2nd-degree connection at the target company. Suggest mutual connection warm intros.
5. **Offer negotiation support** — When an offer arrives, compile market rate data for the role, company, and location. Generate a negotiation brief with talking points.

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| LinkedIn rate limits block searches after ~50 profile views/day | Rotate between 2-3 accounts with staggered activity patterns. Use LinkedIn's saved-searches RSS feed as a fallback when the API throttles. Submit rate-limited queries 60-90 seconds apart. |
| Indeed blocks automated submissions mid-apply | Switch to the Indeed Apply API (where available) for direct applications. For external redirects, use Playwright with randomized human-like delays (2-4s between fields, 20-30s per application). |
| ATS strips resume formatting and loses keywords | Submit resumes as plain .docx (not PDF) with standard section headers (Experience, Education, Skills). Run through an ATS simulator (Jobscan, ResumeWorded) before each submission batch. No columns, tables, or graphics. |
| Cover letter reads as generic template | Pin the last 3 company news items (Google News, Crunchbase) to the cover letter prompt. Always reference a specific product, blog post, or recent hire in the first paragraph. Keep body paragraphs role-specific. |
| State database resets after session restart | Use SQLite with WAL mode for persistence. Write a simple JSON backup to `~/.job_hunter/backup.json` on every successful application record. Monitor startup for the backup file and restore on first missing-table error. |
| Same job posting has different IDs across platforms | Normalize by `company_name + job_title + location` triple. If two records match on all three fields, treat as duplicate regardless of platform ID. Maintain a `seen_hashes` set in the state database. |
| Follow-up emails land in spam | Configure SPF/DKIM/DMARC for your sending domain. Use a dedicated subdomain (jobs@apply.yourdomain.com). Pre-warm the inbox by sending 5-10 low-priority messages before the first follow-up batch. Keep email copy below 60% link-to-text ratio. |

## Verification

- [ ] Profile JSON is complete and reflects current skills, targets, and preferences
- [ ] Platform credentials (LinkedIn, Indeed, Glassdoor) work and rate limits are known
- [ ] Resume template passes an ATS simulator (plain text extraction preserves all content)
- [ ] Cover letter template personalizes company research in paragraph 1
- [ ] Score threshold set appropriately (not too low = spam, not too high = missed opportunities)
- [ ] State database persists correctly across sessions (applied jobs aren't re-submitted)
- [ ] Follow-up sequence fires at correct intervals without duplicate messages
- [ ] Dedup hash catches same job on different platforms
- [ ] Salary tracking captures offer stage numbers for negotiation leverage
- [ ] Weekly analytics report summarizes response rate, interview conversion, and strategy adjustments

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Job-Hunting-as-a-Service | Immediate — 4 weeks to first client | Run the agent for clients end-to-end. Charge per application cycle ($200-500/mo) or per placement (5-10% of first-year salary). Target professionals who hate the job search process but need a new role. |
| Resume Optimization Consulting | 2 weeks | Use the ATS scoring system to audit and rewrite client resumes. Package as a one-time service ($150-300 per audit) with a 30-day follow-up re-score. |
| Job Search Course / Template | 6 weeks | Package the agent's methodology — keyword bank curation, ATS optimization playbook, follow-up sequences, state tracking templates — as a Notion/Teachable course ($47-97). Scale without time-for-money tradeoff. |
| Talent Acquisition White-Label | 8-12 weeks | License the multi-platform search and dedup engine to niche job boards or recruiting agencies. Recurring SaaS revenue ($500-2,000/mo per client). Requires wrapping the core in a REST API. |
| Chrome Extension (Freemium) | 6 weeks | Wrap state tracking, follow-up automation, and ATS scoring as a browser extension. Free tier: 5 active applications. Premium ($9.99/mo): unlimited + cover letter generation. |
| Outplacement B2B | 12+ weeks | Sell to companies laying off staff. Offer a 90-day job-hunting agent subscription for departing employees ($1,000-3,000 per head). High-volume, enterprise sales cycle.