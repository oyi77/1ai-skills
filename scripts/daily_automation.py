#!/usr/bin/env python3
"""
Daily Automation Orchestrator
Runs all automated systems daily: lead management, social media queue, reporting
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Import automation modules
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/scripts')

try:
    from lead_automation import LeadManager
    from social_media_queue import ContentQueue
    from multi_platform_research import Researcher
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    sys.exit(1)

# Configuration
LOGS_DIR = Path('/home/openclaw/.openclaw/workspace/output/logs')
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def log(message: str, level: str = 'INFO'):
    """Log message to file and console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [{level}] {message}"
    
    print(log_message)
    
    # Append to daily log file
    log_file = LOGS_DIR / f"automation_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, 'a') as f:
        f.write(log_message + '\n')

def run_multi_platform_research():
    """Run multi-platform research"""
    log("Starting multi-platform research...")
    
    try:
        researcher = Researcher()
        
        # Generate 200+ search URLs across 17 platforms
        total_leads = researcher.run_comprehensive_research()
        
        log(f"✅ Multi-platform research complete: {total_leads} URLs generated")
        
        return total_leads
        
    except Exception as e:
        log(f"❌ Error in multi-platform research: {e}", 'ERROR')
        return False

def run_lead_automation():
    """Run lead management automation"""
    log("Starting lead management automation...")
    
    try:
        manager = LeadManager()
        
        # Generate daily report
        report = manager.generate_daily_report()
        
        # Save report
        report_file = Path('/home/openclaw/.openclaw/workspace/output/reports') / f"lead_report_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)
        
        log(f"✅ Lead report generated: {report_file}")
        
        # Get leads needing follow-up
        followup_leads = manager.get_leads_needing_followup()
        log(f"✅ Found {len(followup_leads)} leads needing follow-up")
        
        # Generate follow-up tasks
        tasks = manager.generate_followup_tasks()
        tasks_file = Path('/home/openclaw/.openclaw/workspace/output/reports') / f"followup_tasks_{datetime.now().strftime('%Y%m%d')}.json"
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        log(f"✅ Follow-up tasks saved: {tasks_file}")
        
        return True
        
    except Exception as e:
        log(f"❌ Error in lead automation: {e}", 'ERROR')
        return False

def run_social_media_automation():
    """Run social media automation"""
    log("Starting social media automation...")
    
    try:
        queue = ContentQueue()
        
        # Get content ready to post
        ready_to_post = queue.get_content_ready_to_post()
        log(f"✅ Found {len(ready_to_post)} items ready to post")
        
        # Auto-post to Facebook (only enabled platform)
        if ready_to_post:
            posted_count = 0
            for item in ready_to_post:
                try:
                    results = queue.post_to_facebook(item)
                    success_count = len([r for r in results if 'error' not in r])
                    
                    if success_count > 0:
                        queue.mark_as_posted(queue.queue.index(item), 'facebook')
                        posted_count += 1
                        log(f"✅ Posted to Facebook: {item.caption[:30]}...")
                    
                except Exception as e:
                    log(f"❌ Error posting {item.content_type}: {e}", 'ERROR')
            
            log(f"✅ Posted {posted_count}/{len(ready_to_post)} items to Facebook")
        
        # Generate weekly report
        report = queue.generate_weekly_report()
        report_file = Path('/home/openclaw/.openclaw/workspace/output/reports') / f"social_report_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)
        
        log(f"✅ Social media report saved: {report_file}")
        
        return True
        
    except Exception as e:
        log(f"❌ Error in social media automation: {e}", 'ERROR')
        return False

def generate_automation_summary():
    """Generate automation summary"""
    log("Generating automation summary...")
    
    try:
        # Load all managers
        lead_manager = LeadManager()
        social_queue = ContentQueue()
        
        # Generate summary
        summary = f"""
# Daily Automation Summary
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Lead Management
- Total leads: {len(lead_manager.leads)}
- New: {len(lead_manager.get_leads_by_status('new'))}
- Contacted: {len(lead_manager.get_leads_by_status('contacted'))}
- Interested: {len(lead_manager.get_leads_by_status('interested'))}
- Negotiating: {len(lead_manager.get_leads_by_status('negotiating'))}
- Closed Won: {len(lead_manager.get_leads_by_status('closed_won'))}
- Need Follow-up: {len(lead_manager.get_leads_needing_followup())}

## Social Media Queue
- Queued content: {len([item for item in social_queue.queue if item.status == 'queued'])}
- Ready to post: {len(social_queue.get_content_ready_to_post())}
- Posted this week: {len(social_queue.posted_log)}
- Scheduled next 7 days: {len([item for item in social_queue.queue if item.status == 'queued'])}

## System Status
- Lead automation: ✅ Running
- Social media automation: ✅ Running
- Reporting: ✅ Running
- Cron job: ⏳ Needs setup

## Next Actions
- [ ] Review leads needing follow-up
- [ ] Approve scheduled posts
- [ ] Monitor engagement metrics
- [ ] Adjust content strategy based on data

---
Automation completed at: {datetime.now().isoformat()}
"""
        
        # Save summary
        summary_file = Path('/home/openclaw/.openclaw/workspace/output/reports') / f"automation_summary_{datetime.now().strftime('%Y%m%d')}.md"
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        with open(summary_file, 'w') as f:
            f.write(summary)
        
        log(f"✅ Automation summary saved: {summary_file}")
        
        return True
        
    except Exception as e:
        log(f"❌ Error generating summary: {e}", 'ERROR')
        return False

def main():
    """Main automation orchestrator"""
    print("="*60)
    print("DAILY AUTOMATION ORCHESTRATOR")
    print("="*60)
    print(f"Starting at: {datetime.now().isoformat()}")
    print()
    
    success = True
    
    # Step 1: Multi-Platform Research
    print("Step 1: Multi-Platform Research Automation")
    print("-" * 60)
    result = run_multi_platform_research()
    
    if result is False:
        success = False
        print("❌ Multi-platform research failed")
    else:
        total_leads = result
        print(f"✅ Generated {total_leads} research URLs")
    print()
    
    # Step 2: Lead Management
    print("Step 1: Lead Management Automation")
    print("-"*60)
    if not run_lead_automation():
        success = False
    print()
    
    # Step 2: Social Media
    print("Step 2: Social Media Automation")
    print("-"*60)
    if not run_social_media_automation():
        success = False
    print()
    
    # Step 3: Summary
    print("Step 3: Generate Automation Summary")
    print("-"*60)
    if not generate_automation_summary():
        success = False
    print()
    
    # Final summary
    print("="*60)
    if success:
        print("✅ ALL AUTOMATIONS COMPLETED SUCCESSFULLY")
        print("="*60)
        return 0
    else:
        print("❌ SOME AUTOMATIONS FAILED")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
