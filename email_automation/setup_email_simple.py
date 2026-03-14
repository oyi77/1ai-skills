#!/usr/bin/env python3
"""
EMAIL AUTOMATION SETUP - Fixed Version
Prepare email templates for sending
"""

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
LEAD_GEN_DIR = WORKSPACE / "lead_gen_machine"
EMAIL_DIR = WORKSPACE / "email_automation"

EMAIL_DIR.mkdir(parents=True, exist_ok=True)

print("="*70)
print("📧 EMAIL AUTOMATION SETUP")
print("="*70)
print()

# Load latest campaign
campaigns = list((LEAD_GEN_DIR / "campaigns").glob("campaign_*.json"))
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

generated_content = campaign.get('generated_content', [])

print("[INFO] Preparing email automation...")
print()

# Simple email queue - avoid complex comprehension
email_queue = []

if generated_content:
    for item in generated_content:
        business_name = item.get('business_name', '')
        
        if 'emails' in item:
            for email in item['emails']:
                # Filter by type manually
                email_type = email.get('type', 'initial')
                if email_type:
                    email_queue.append({
                        "to": "business@example.com",  # Would need real email
                        "to_name": business_name,
                        "subject": email.get('subject', ''),
                        "body": email.get('body', ''),
                        "type": email_type,
                        "business_name": business_name
                    })

print(f"[INFO] Email queue: {len(email_queue)} emails")
print()

# Count by type (manual counting)
initial_count = sum(1 for e in email_queue if e['type'] == 'initial')
followup_1_count = sum(1 for e in email_queue if e['type'] == 'followup_1')
followup_2_count = sum(1 for e in email_queue if e['type'] == 'followup_2')

print(f"[INFO] Email breakdown:")
print(f"   Initial: {initial_count}")
print(f"   Follow-up 1: {followup_1_count}")
print(f"   Follow-up 2: {followup_2_count}")
print()

# Save simple config
config_file = EMAIL_DIR / "email_config.json"

config = {
    "mode": "MANUAL_START",
    "campaign_id": campaign.get('campaign_id'),
    "queue_ready": True,
    "queue_size": len(email_queue),
    "batch_schedule": {
        "day_1": {"emails": initial_count},
        "day_3": {"emails": followup_1_count},
        "day_7": {"emails": followup_2_count}
    },
    "setup_at": datetime.now().isoformat()
}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ Email config saved: {config_file}")
print()

# Create email batch files for easy manual sending
batch_file = EMAIL_DIR / f"batch_day1_initial_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

with open(batch_file, 'w') as f:
    f.write("="*70 + "\n")
    f.write("EMAIL BATCH - INITIAL EMAILS (DAY 1)\n")
    f.write("="*70 + "\n\n")
    f.write(f"Campaign: {campaign.get('campaign_id')}\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Emails in this batch: {initial_count}\n\n")
    f.write("="*70 + "\n\n")
    f.write("INSTRUCTIONS:\n")
    f.write("1. Copy each email below\n")
    f.write("2. Replace [Your Name] with your actual name\n")
    f.write("3. Replace [Your Phone Number] with your phone\n")
    f.write("4. Update [Your Calendar Link] with your calendar link\n")
    f.write("5. Send via your email (Gmail preferred)\n")
    f.write("6. Track responses in spreadsheet\n")
    f.write("7. Send next batch in 3 days if no response\n")
    f.write("8. Send final batch in 7 days if still no response\n\n")
    f.write("="*70 + "\n\n")

    initial_emails = [e for e in email_queue if e['type'] == 'initial']
    for i, email in enumerate(initial_emails[:20], 1):  # First 20
        f.write(f"{'─'*70}\n")
        f.write(f"EMAIL {i}: {email['business_name']}\n")
        f.write(f"{'─'*70}\n\n")
        f.write(f"TO: [INSERT ACTUAL EMAIL or DM via Instagram]\n")
        f.write(f"OR Find & DM via: ")
        matching_restaurant = next((r for r in restaurants if r['business_name'] == email['business_name']), None)
        if matching_restaurant and 'website' in matching_restaurant:
            f.write(f"{matching_restaurant.get('website', 'Search on Google')}\n")
        f.write(f"\n")
        f.write(f"SUBJECT:\n{email['subject']}\n\n")
        f.write(f"BODY:\n\n{email['body']}\n\n")
        f.write(f"{'='*70}\n\n")

print(f"✅ Email batch file created: {batch_file}")
print()

# Also create follow-up batches
followup_1_file = EMAIL_DIR / f"batch_day3_followup1_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

with open(followup_1_file, 'w') as f:
    f.write("="*70 + "\n")
    f.write("EMAIL BATCH - FOLLOW-UP EMAILS (DAY 3)\n")
    f.write("="*70 + "\n\n")
    f.write(f"Send these 3 days after initial email (if no response)\n\n")
    f.write("="*70 + "\n\n")

    followup_1_emails = [e for e in email_queue if e['type'] == 'followup_1']
    for i, email in enumerate(followup_1_emails[:20], 1):
        f.write(f"{'─'*70}\n")
        f.write(f"EMAIL {i}: {email['business_name']}\n")
        f.write(f"{'─'*70}\n\n")
        f.write(f"SUBJECT: {email['subject']}\n\n")
        f.write(f"BODY:\n\n{email['body']}\n\n")
        f.write(f"{'='*70}\n\n")

print(f"✅ Follow-up 1 batch created: {followup_1_file}")
print()

followup_2_file = EMAIL_DIR / f"batch_day7_followup2_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

with open(followup_2_file, 'w') as f:
    f.write("="*70 + "\n")
    f.write("EMAIL BATCH - FOLLOW-UP EMAILS (DAY 7)\n")
    f.write("="*70 + "\n\n")
    f.write(f"Send these 7 days after initial email (final follow-up)\n")
    f.write(f"If still no response, stop pursuing this lead\n")
    f.write(f"Focus on new leads\n\n")
    f.write("="*70 + "\n\n")

    followup_2_emails = [e for e in email_queue if e['type'] == 'followup_2']
    for i, email in enumerate(followup_2_emails[:20], 1):
        f.write(f"{'─'*70}\n")
        f.write(f"EMAIL {i}: {email['business_name']}\n")
        f.write(f"{'─'*70}\n\n")
        f.write(f"SUBJECT: {email['subject']}\n\n")
        f.write(f"BODY:\n\n{email['body']}\n\n")
        f.write(f"{'='*70}\n\n")

print(f"✅ Follow-up 2 batch created: {followup_2_file}")
print()

print("="*70)
print("📧 EMAIL AUTOMATION SETUP COMPLETE!")
print("="*70)
print()
print("MODE: MANUAL START (Ready to upgrade to full automation)")
print()
print(f"Total Emails: {len(email_queue)}")
print(f"  Day 1 (Initial): {initial_count}")
print(f"  Day 3 (Follow-up 1): {followup_1_count}")
print(f"  Day 7 (Follow-up 2): {followup_2_count}")
print()
print("📁 Files Created:")
print(f"  • Config: {config_file}")
print(f"  • Day 1 Initial: {batch_file}")
print(f"  • Day 3 Follow-up: {followup_1_file}")
print(f"  • Day 7 Follow-up: {followup_2_file}")
print()
print("🚀 NEXT STEPS:")
print()
print("1. Open batch_day1_initial_*.txt")
print("2. Customize with your name/contact")
print("3. Send emails via Gmail")
print("4. Track responses in spreadsheet")
print("5. Send follow-up emails on day 3 and day 7")
print()
print("⚡ TO UPGRADE TO FULL AUTOMATION:")
print("   - Setup Gmail API")
print("   - Configure Himalaya")
print("   - Integrate ESP (Mailchimp, SendGrid)")
print()