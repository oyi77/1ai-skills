#!/usr/bin/env python3
"""
Lead Management Automation System
Automated lead tracking, follow-ups, and reporting for TikTok Content Agency
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Add skills to path
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/skills/1ai-skills/marketing')

try:
    from post_bridge_client import PostBridgeClient
except:
    PostBridgeClient = None

# Configuration
CRM_SHEET_ID = '1VLUiuI46mP4EYtJ418bj9pgY4sQzrJqaNhhlvfILHC0'
GMAIL_ACCOUNT = 'muchammadizzuddin@gmail.com'

# Data files
LEADS_DB = Path('/home/openclaw/.openclaw/workspace/output/leads_db.json')
REPORTS_DIR = Path('/home/openclaw/.openclaw/workspace/output/reports')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class Lead:
    def __init__(self, shop_name: str, shop_url: str, email: str = None, status: str = 'new'):
        self.shop_name = shop_name
        self.shop_url = shop_url
        self.email = email
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.last_contacted = None
        self.follow_ups = []
        self.assigned_free_videos = False
        self.signed_package = None

    def to_dict(self):
        return {
            'shop_name': self.shop_name,
            'shop_url': self.shop_url,
            'email': self.email,
            'status': self.status,
            'created_at': self.created_at,
            'last_contacted': self.last_contacted,
            'follow_ups': self.follow_ups,
            'assigned_free_videos': self.assigned_free_videos,
            'signed_package': self.signed_package
        }

class LeadManager:
    def __init__(self):
        self.leads = self.load_leads()

    def load_leads(self) -> List[Lead]:
        """Load leads from database"""
        if LEADS_DB.exists():
            with open(LEADS_DB, 'r') as f:
                data = json.load(f)
                return [Lead(**lead) for lead in data]
        return []

    def save_leads(self):
        """Save leads to database"""
        data = [lead.to_dict() for lead in self.leads]
        with open(LEADS_DB, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_lead(self, shop_name: str, shop_url: str, email: str = None) -> Lead:
        """Add new lead"""
        lead = Lead(shop_name=shop_name, shop_url=shop_url, email=email)
        self.leads.append(lead)
        self.save_leads()
        return lead

    def update_lead_status(self, shop_name: str, status: str):
        """Update lead status"""
        for lead in self.leads:
            if lead.shop_name == shop_name:
                lead.status = status
                lead.last_contacted = datetime.now().isoformat()
                break
        self.save_leads()

    def add_follow_up(self, shop_name: str, message: str):
        """Add follow-up to lead"""
        for lead in self.leads:
            if lead.shop_name == shop_name:
                lead.follow_ups.append({
                    'date': datetime.now().isoformat(),
                    'message': message
                })
                lead.last_contacted = datetime.now().isoformat()
                break
        self.save_leads()

    def get_leads_by_status(self, status: str) -> List[Lead]:
        """Get leads by status"""
        return [lead for lead in self.leads if lead.status == status]

    def get_leads_needing_followup(self) -> List[Lead]:
        """Get leads that need follow-up (3+ days since last contact)"""
        leads_needing_followup = []
        now = datetime.now()
        
        for lead in self.leads:
            if lead.status in ['contacted', 'interested', 'negotiating']:
                last_contact = datetime.fromisoformat(lead.last_contacted or lead.created_at)
                days_since_contact = (now - last_contact).days
                
                if days_since_contact >= 3:
                    leads_needing_followup.append(lead)
        
        return leads_needing_followup

    def assign_free_videos(self, shop_name: str):
        """Mark that free videos were assigned"""
        for lead in self.leads:
            if lead.shop_name == shop_name:
                lead.assigned_free_videos = True
                lead.status = 'videos_sent'
                break
        self.save_leads()

    def record_sale(self, shop_name: str, package: str, amount: int):
        """Record successful sale"""
        for lead in self.leads:
            if lead.shop_name == shop_name:
                lead.status = 'closed_won'
                lead.signed_package = {
                    'package': package,
                    'amount': amount,
                    'date': datetime.now().isoformat()
                }
                break
        self.save_leads()

    def generate_daily_report(self) -> str:
        """Generate daily report"""
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        
        leads_new = self.get_leads_by_status('new')
        leads_contacted = self.get_leads_by_status('contacted')
        leads_interested = self.get_leads_by_status('interested')
        leads_negotiating = self.get_leads_by_status('negotiating')
        leads_closed = self.get_leads_by_status('closed_won')
        leads_lost = self.get_leads_by_status('closed_lost')
        leads_needing_followup = self.get_leads_needing_followup()

        report = f"""
# Daily Report - TikTok Content Agency
Date: {date_str}

## Summary
- Total Leads: {len(self.leads)}
- New Leads: {len(leads_new)}
- Contacted: {len(leads_contacted)}
- Interested: {len(leads_interested)}
- Negotiating: {len(leads_negotiating)}
- Closed Won: {len(leads_closed)}
- Closed Lost: {len(leads_lost)}
- Need Follow-up: {len(leads_needing_followup)}

## Leads Needing Follow-up
"""
        
        for lead in leads_needing_followup:
            last_contact = datetime.fromisoformat(lead.last_contacted or lead.created_at)
            days_since = (now - last_contact).days
            report += f"\n- {lead.shop_name} ({days_since} days since contact)"

        report += f"""

## All Leads Status
"""
        
        for lead in self.leads:
            report += f"\n### {lead.shop_name}"
            report += f"- Status: {lead.status}"
            report += f"- Email: {lead.email or 'Not provided'}"
            report += f"- Last Contacted: {lead.last_contacted or 'Never'}"
            report += f"- Free Videos Sent: {lead.assigned_free_videos}"
            if lead.signed_package:
                report += f"- Package: {lead.signed_package['package']} (IDR {lead.signed_package['amount']:,})"

        return report

    def generate_followup_tasks(self) -> List[Dict]:
        """Generate follow-up tasks for leads needing attention"""
        leads = self.get_leads_needing_followup()
        tasks = []
        
        for lead in leads:
            tasks.append({
                'shop_name': lead.shop_name,
                'email': lead.email,
                'task': 'Send follow-up email',
                'priority': 'high',
                'due_date': datetime.now().strftime('%Y-%m-%d')
            })
        
        return tasks

def update_gmail_leads():
    """Update Gmail contacts with new leads"""
    pass  # Would require Gmail API setup

def send_automated_emails():
    """Send automated follow-up emails"""
    pass  # Would require Gmail API setup

def send_daily_report_via_telegram():
    """Send daily report via Telegram"""
    # Load Telegram token from config
    # Send report
    pass  # Would require Telegram bot setup

def main():
    """Main automation loop"""
    manager = LeadManager()
    
    # Generate daily report
    report = manager.generate_daily_report()
    
    # Save report
    report_file = REPORTS_DIR / f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Daily report generated: {report_file}")
    
    # Generate follow-up tasks
    tasks = manager.generate_followup_tasks()
    print(f"✅ Generated {len(tasks)} follow-up tasks")
    
    # Summary
    print(f"\n{'='*60}")
    print("LEAD MANAGEMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Total leads: {len(manager.leads)}")
    print(f"New leads: {len(manager.get_leads_by_status('new'))}")
    print(f"Contacted: {len(manager.get_leads_by_status('contacted'))}")
    print(f"Interested: {len(manager.get_leads_by_status('interested'))}")
    print(f"Negotiating: {len(manager.get_leads_by_status('negotiating'))}")
    print(f"Closed won: {len(manager.get_leads_by_status('closed_won'))}")
    print(f"Needing follow-up: {len(manager.get_leads_needing_followup())}")

if __name__ == '__main__':
    main()
