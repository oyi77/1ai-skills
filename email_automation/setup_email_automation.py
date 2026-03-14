#!/usr/bin/env python3
"""
EMAIL AUTOMATION SETUP - Configure Email Sending
Supports Gmail API, Himalaya, and manual options
"""

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
LEAD_GEN_DIR = WORKSPACE / "lead_gen_machine"
AUTOMATION_DIR = WORKSPACE / "email_automation"

AUTOMATION_DIR.mkdir(parents=True, exist_ok=True)

print("="*70)
print("📧 EMAIL AUTOMATION SETUP")
print("="*70)
print()

# Load latest campaign data
campaigns = list(LEAD_GEN_DIR / "campaigns").glob("campaign_*.json")
latest_campaign = max(campaigns, key=lambda f: f.stat().st_mtime)

print(f"[INFO] Loading campaign: {latest_campaign.name}")
with open(latest_campaign) as f:
    campaign = json.load(f)

restaurants = campaign.get('restaurants', []) or campaign.get('leads', [])

if not restaurants:
    print("[ERROR] No restaurants found in campaign")
    exit(1)

print(f"[INFO] Found {len(restaurants)} businesses")
print()

# Email templates from campaign
generated_content = campaign.get('generated_content', [])

print("[INFO] Preparing email automation...")
print()

# Create email batch file
email_queue = []
for item in generated_content:
    restaurants = campaign.get('restaurants', campaign.get('leads', []))
    if not restaurants:
        continue
        
    business_name = item.get('business_name', '')
    matching_restaurant = next((r for r in restaurants if r['business_name'] == business_name), None)
    
    if matching_restaurant and 'emails' in item:
        # Get emails from generated content
        for email in item['emails']:
            email_queue.append({
                "to": "business@example.com",  # Would need real email
                "to_name": item.get('business_name', ''),
                "subject": email.get('subject', ''),
                "body": email.get('body', ''),
                "type": email.get('type', 'initial'),
                "business_name": item.get('business_name', ''),
                "category": matching_restaurant.get('type', 'restaurant') if matching_restaurant else 'restaurant',
                "source": campaign.get('campaign_id', 'unknown')
            })

print(f"[INFO] Email queue: {len(email_queue)} emails")
print()

# Save email automation config
config_file = AUTOMATION_DIR / "email_config.json"

config = {
    "mode": "MANUAL_START",  # Can be: GMAIL_API, HIMALAYA, MANUAL
    "campaign_id": campaign.get('campaign_id'),
    "queue_ready": True,
    "queue_size": len(email_queue),
    "emails": email_queue[:10],  # First 10 batch
    "batch_schedule": {
        "initial": {"day": 1, "emails": len([e for e in email_queue if e['type'] == 'initial'])]},
        "followup_1": {"day": 3, "emails": len([e for e in email_queue if e['type'] == 'followup_1'])]},
        "followup_2": {"day": 7, "emails": len([e for e in email_queue if e['type'] == 'followup_2'])]},
    },
    "setup_at": datetime.now().isoformat()
}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ Email config saved: {config_file}")
print()

# Create email batch files for easy manual sending
batch_file = AUTOMATION_DIR / f"batch_1_initial_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

with open(batch_file, 'w') as f:
    f.write("="*70 + "\n")
    f.write("EMAIL BATCH 1 - INITIAL EMAILS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Campaign: {campaign.get('campaign_id')}\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Emails in batch: {len(email_queue)}\n\n")
    f.write("="*70 + "\n\n")
    f.write("INSTRUCTIONS:\n")
    f.write("1. Copy each email below\n")
    f.write("2. personalize with your name and contact info\n")
    f.write("3. Update [Your Calendar Link] with your actual calendar\n")
    f.write("4. Send via your email (Gmail/Outlook/etc)\n")
    f.write("5. Track responses in a spreadsheet\n\n")
    f.write("="*70 + "\n\n")

    initial_emails = [e for e in email_queue if e['type'] == 'initial']
    for i, email in enumerate(initial_emails[:10], 1):
        f.write(f"{'─'*70}\n")
        f.write(f"EMAIL {i}: {email['business_name']}\n")
        f.write(f"{'─'*70}\n\n")
        f.write(f"TO: [INSERT ACTUAL EMAIL OR DM VIA INSTAGRAM]\n\n")
        f.write(f"SUBJECT: {email['subject']}\n\n")
        f.write(f"BODY:\n\n")
        f.write(f"{email['body']}\n\n")
        f.write(f"{'='*70}\n\n")

print(f"✅ Email batch file saved: {batch_file}")
print()

# Create follow-up batches
for day_num in [3, 7]:
    followup_type = f"followup_{day_num}"
    followup_emails = [e for e in email_queue if e['type'] == followup_type]
    
    if followup_emails:
        followup_file = AUTOMATION_DIR / f"batch_{day_num}_{followup_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        with open(followup_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"EMAIL BATCH {day_num} - FOLLOW-UP EMAILS (Day {day_num})\n")
            f.write("="*70 + "\n\n")
            f.write(f"Send these only after initial response (or no response)\n")
            f.write(f"Day {day_num}: Send these {len(followup_emails)} follow-up emails\n\n")
            f.write("="*70 + "\n\n")
            
            for i, email in enumerate(followup_emails, 1):
                f.write(f"{'─'*70}\n")
                f.write(f"EMAIL {i}: {email['business_name']}\n")
                f.write(f"{'─'*70}\n\n")
                f.write(f"TO: [INSERT ACTUAL EMAIL OR DM VIA INSTAGRAM]\n\n")
                f.write(f"SUBJECT: {email['subject']}\n\n")
                f.write(f"BODY:\n\n")
                f.write(f"{email['body']}\n\n")
                f.write(f"{'='*70}\n\n")
        
        print(f"✅ Follow-up batch saved: {followup_file}")

print()
print("="*70)
print("📧 EMAIL AUTOMATION SETUP COMPLETE!")
print("="*70)
print()
print("MODE: MANUAL START (Ready to upgrade to full automation)")
print()
print("📁 Files generated:")
print(f"• Config: {config_file}")
print(f"• Initial batch: {batch_file}")
print(f"• Follow-ups: See above for day 3 and day 7 batches")
print()
print("🚀 NEXT STEPS:")
print()
print("1. Review email batch files")
print("2. Customize with your name/contact info")
print("3. Send initial emails (batch_1)")
print("4. Track responses in spreadsheet")
print("5. Send follow-up emails on day 3 and day 7")
print()
print("⚡ TO UPGRADE TO FULL AUTOMATION:")
print("   - Setup Gmail API")
print("   - Configure Himalaya")
print("   - Or integrate with existing ESP (Mailchimp, SendGrid, etc.)")
print()