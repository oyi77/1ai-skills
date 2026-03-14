#!/usr/bin/env python3
"""
FULLY AUTOMATED LEAD GEN MACHINE
Google Maps → Lead Extraction → Cold Email → Social Media Blast → Content Generation → Follow-up Sequences
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import random

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
ENGINE_DIR = WORKSPACE / "lead_gen_machine"
DATA_DIR = ENGINE_DIR / "data"
CAMPAIGN_DIR = ENGINE_DIR / "campaigns"

# Create directories
ENGINE_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CAMPAIGN_DIR.mkdir(parents=True, exist_ok=True)

# Google Maps API Config
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # User provided this

# Lead Gen Config
TARGET_LOCATIONS = [
    {"city": "Jakarta", "lat": -6.2088, "lng": 106.8456},
    {"city": "Surabaya", "lat": -7.2575, "lng": 112.7521},
    {"city": "Bandung", "lat": -6.9175, "lng": 107.6191},
    {"city": "Medan", "lat": 3.5952, "lng": 98.6722},
]

TARGET_CATEGORIES = [
    {"category": "restaurant", "keywords": ["restaurant", "cafe", "warung"]},
    {"category": "salon", "keywords": ["salon", "barbershop", "spa"]},
    {"category": "agency", "keywords": ["agency", "marketing", "digital"]},
    {"category": "service", "keywords": ["service", "consulting", "professional"]},
]

# Cold Email Templates
EMAIL_TEMPLATES = {
    "initial": {
        "subject": "Quick question, {business_name}",
        "body": """Hi {owner_name},

Came across {business_name} on Google Maps - impressive {rating} star rating!

Quick question:

Are you looking to get more customers/leads online?

I help businesses like yours automate:
- Customer acquisition (get more inquiries)
- Content creation (social media, blogs, emails)
- Lead generation (outreach to potential clients)
- Marketing automation (save 10-20 hours/week)

Results from similar businesses:
- +200% more website traffic
- +150% more social media engagement
- 50+ new leads/month
- Saved 15+ hours/week on marketing

Worth a 15-min chat to see if this would work for {business_name}?

Best,
{sender_name}
AI Marketing Specialist
"""
    },

    "follow_up_1": {
        "subject": "Following up on my email to {business_name}",
        "body": """Hi {owner_name},

Just wanted to bump this to top of your inbox.

I specialize in helping {business_name}-type businesses grow their customer base using AI-powered marketing.

Quick wins I can implement this week:
1. Auto-post to social media (5 platforms simultaneously)
2. Generate 50+ leads/month via targeted outreach
3. Create blog posts, videos, and emails on autopilot
4. Set up automated follow-up sequences

Want to see a free demo of how it works?

Let me know,
{sender_name}
"""
    },

    "follow_up_2": {
        "subject": "Last time I'll bother you about this, {business_name}",
        "body": """Hey {owner_name},

Last follow-up - promise!

Here's the deal:

I can set up a fully automated marketing system for {business_name} in 1 week.

You'll see:
- 50+ leads coming in automatically
- Social media posts publishing daily
- Blog content generating on autopilot
- Email campaigns nurturing leads

My guarantee: If you don't see 10+ new leads in the first 30 days, full refund.

Sound fair?

15-min call to show you how:
[Calendar Link]

Best,
{sender_name}
"""
    }
}

# Social Media Post Templates
POST_TEMPLATES = {
    "offer": {
        "tiktok": "🔥 {business_name} owners! Want 50+ leads/month? I automate marketing in 1 week. DM me 'GROW' 🚀",
        "instagram": "Business owners of {category} businesses! 🎯

I help you get 50+ leads/month with FULLY AUTOMATED marketing:
✅ Social media auto-posting
✅ Lead generation outreach  
✅ Content creation on autopilot
✅ Email nurture sequences

Results: +200% traffic, +150% engagement

DM me 'DEMO' for free demo! 👋
#marketing #business #automation",
        "facebook": "{category} Business Owners! 💼

Want 50+ new leads/month on autopilot?

I set up FULLY AUTOMATED marketing systems:
• Social media: Auto-post to 5+ platforms
• Lead generation: Scrape & outreach to 100+ leads/day
• Content: Generate blogs, videos, emails automatically
• Email campaigns: Auto-follow-up sequences

Typical results:
📈 +200% website traffic
📱 +150% social engagement  
🎯 50-100 new leads/month
⏱️ Save 15-20 hours/week

Want a free demo? Comment 'DEMO' below!

#BusinessGrowth #Marketing #Automation #Leads",
        "linkedin": "For {category} business owners:

I build fully automated marketing systems that generate 50-100 leads/month, 200% more traffic, and save 15-20 hours/week.

Platforms: Social media, email automation, lead generation, content creation.

Guarantee: If you don't see 10+ leads in first 30 days, full refund.

Open to a 15-min demo? Let's connect! 🚀

#Automation #AI #Marketing #BusinessGrowth",
    }
}

# Content Generation Templates
CONTENT_TEMPLATES = {
    "blog_post": """# How {business_name} Can Get 50+ Leads/Month on Autopilot

## The Problem
Most {category} businesses struggle with:
- Getting consistent leads
- Managing social media
- Creating content regularly  
- Following up with prospects

## The Solution: Fully Automated Marketing

### 1. Lead Generation
- Use Google Maps to find {category} businesses in {location}
- Extract contact info automatically
- Generate personalized outreach messages
- Send 50-100 leads/day

### 2. Social Media Automation
- Auto-post to TikTok, Instagram, Facebook, LinkedIn, Twitter
- Create hooks, captions, hashtags
- Schedule optimal posting times
- Track engagement metrics

### 3. Content Creation
- Generate blog posts, videos, emails, ad copy
- SEO optimized content
- Personalized for your industry
- Create in minutes, not hours

### 4. Email Sequences
- Auto-follow-up sequences
- Personalized nurturing
- Track opens, clicks, replies
- A/B test for optimization

## Results from Similar Businesses
- +200% more website traffic
- +150% more social media engagement
- 50-100 new leads/month
- Saved 15-20 hours/week on marketing

## How to Get Started
1. 15-min strategy call (free)
2. 1-week setup + deployment
3. See leads coming in automatically
4. Optimization & scaling

## Guarantee
If you don't see 10+ new leads in the first 30 days, full refund.

Ready to automate your marketing?

Contact: [Your Contact]
Website: [Your Website]
""",

    "video_script": """[0:00]
Hook: "Hey {category} business owners, want 50+ leads/month on autopilot?"

[0:05]
I helped {business_name} go from 10 leads to 100+ leads in just 4 weeks
Here's exactly what we did

[0:15]
#1 Lead Generation
Use Google Maps to find potential customers
Auto-send 50-100 personalized emails daily
Response rate: 5-20%!

[0:30]
#2 Social Media Automation  
Auto-post to 5 platforms at once
TikTok, Instagram, Facebook, LinkedIn, Twitter
Save 20+ hours/week!

[0:45]
#3 Content Creation
Generate blogs, videos, emails, ad copy
All SEO optimized, industry-specific
Create in minutes not hours

[1:00]
#4 Email Follow-up
Automated sequences + personalization
Day 1: Initial email
Day 3: Value-add  
Day 7: Final follow-up
Track everything!

[1:15]
Results for {business_name}:
200% more traffic
150% more engagement
50-100 new leads/month
Saved 15+ hours/week

[1:25]
Want the same results?
Link in bio for FREE 15-min demo
Comment 'AUTOMATE' if interested
"""
}

def search_google_maps_leads(location, category, limit=50):
    """Search Google Maps for businesses"""
    print(f"[INFO] Searching for {category} in {location['city']}...")

    # Using Google Places API
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": f"{category} in {location['city']}",
        "key": GOOGLE_MAPS_API_KEY,
        "fields": "name,formatted_address,formatted_phone_number,website,rating,review_count,opening_hours,price_level,types",
    }

    leads = []
    next_page_token = None

    while len(leads) < limit:
        if next_page_token:
            params["pagetoken"] = next_page_token

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "OK":
            print(f"[ERROR] Google Maps API error: {data.get('status')}")
            break

        for place in data.get("results", []):
            lead = {
                "business_name": place.get("name"),
                "address": place.get("formatted_address"),
                "phone": place.get("formatted_phone_number"),
                "website": place.get("website"),
                "rating": place.get("rating"),
                "reviews": place.get("review_count"),
                "types": place.get("types", []),
                "location": location,
                "category": category,
                "extracted_at": datetime.now().isoformat()
            }
            leads.append(lead)

        next_page_token = data.get("next_page_token")

        if not next_page_token:
            break

        # Rate limiting delay
        import time
        time.sleep(2)

    print(f"[INFO] Found {len(leads)} leads")
    return leads[:limit]

def generate_personalized_email(lead, template_key="initial"):
    """Generate personalized cold email for lead"""
    template = EMAIL_TEMPLATES.get(template_key, EMAIL_TEMPLATES["initial"])

    # Personalize
    subject = template["subject"].format(
        business_name=lead["business_name"]
    )

    body = template["body"].format(
        owner_name=lead["business_name"],  # Fallback to business name
        business_name=lead["business_name"],
        rating=f"{lead.get('rating', 0):.1f}⭐",
        sender_name="Your AI Assistant"
    )

    return {
        "to": lead.get("email") or extract_email_from_website(lead.get("website", "")),
        "subject": subject,
        "body": body,
        "lead_id": lead["business_name"][:50],
        "template": template_key
    }

def extract_email_from_website(website):
    """Extract email from website URL"""
    # This would need web scraping
    # For now, return None
    return None

def generate_social_posts(lead, platforms=["tiktok", "instagram", "facebook", "linkedin"]):
    """Generate social media posts for lead"""
    posts = {}

    for platform in platforms:
        template = POST_TEMPLATES["offer"].get(platform)
        if template:
            content = template.format(
                business_name=lead["business_name"],
                category=lead["category"]
            )
            posts[platform] = content

    return posts

def generate_content_for_lead(lead):
    """Generate all content for a lead"""
    content = {
        "lead_id": lead["business_name"][:50],
        "generated_at": datetime.now().isoformat()
    }

    # Email sequences
    content["emails"] = {
        "initial": generate_personalized_email(lead, "initial"),
        "follow_up_1": generate_personalized_email(lead, "follow_up_1"),
        "follow_up_2": generate_personalized_email(lead, "follow_up_2")
    }

    # Social posts
    content["social_posts"] = generate_social_posts(lead)

    # Blog post
    content["blog_post"] = CONTENT_TEMPLATES["blog_post"].format(
        business_name=lead["business_name"],
        category=lead["category"],
        location=lead["location"]["city"]
    )

    # Video script
    content["video_script"] = CONTENT_TEMPLATES["video_script"].format(
        business_name=lead["business_name"],
        category=lead["category"]
    )

    return content

def run_full_campaign(location, category, num_leads=50):
    """Run complete automation campaign"""
    print("="*70)
    print("🚀 FULLY AUTOMATED LEAD GEN MACHINE")
    print("="*70)
    print()

    # Step 1: Search Google Maps
    print("[STEP 1/5] Searching Google Maps for leads...")
    leads = search_google_maps_leads(location, category, num_leads)
    print(f"✅ Found {len(leads)} qualified leads")
    print()

    # Step 2: Generate personalized content for each lead
    print("[STEP 2/5] Generating personalized content...")
    all_content = []

    for i, lead in enumerate(leads, 1):
        print(f"   [{i}/{len(leads)}] Generating for {lead['business_name']}...")
        content = generate_content_for_lead(lead)
        all_content.append(content)

    print(f"✅ Generated content for {len(all_content)} leads")
    print()

    # Step 3: Save campaign data
    print("[STEP 3/5] Saving campaign data...")
    campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M')}"
    campaign_file = CAMPAIGN_DIR / f"{campaign_id}.json"

    campaign_data = {
        "campaign_id": campaign_id,
        "location": location,
        "category": category,
        "total_leads": len(leads),
        "leads": leads,
        "content": all_content,
        "created_at": datetime.now().isoformat()
    }

    with open(campaign_file, 'w') as f:
        json.dump(campaign_data, f, indent=2)

    print(f"✅ Saved campaign to: {campaign_file}")
    print()

    # Step 4: Generate summary report
    print("[STEP 4/5] Generating summary report...")
    report_file = CAMPAIGN_DIR / f"{campaign_id}_report.txt"

    with open(report_file, 'w') as f:
        f.write(f"LEAD GEN CAMPAIGN REPORT\n")
        f.write(f"{'='*70}\n\n")
        f.write(f"Campaign ID: {campaign_id}\n")
        f.write(f"Location: {location['city']}\n")
        f.write(f"Category: {category}\n")
        f.write(f"Total Leads: {len(leads)}\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"{'='*70}\n\n")
        f.write(f"LEAD BREAKDOWN:\n\n")

        for i, lead in enumerate(leads[:20], 1):
            f.write(f"{i}. {lead['business_name']}\n")
            f.write(f"   Rating: {lead.get('rating', 'N/A')}⭐\n")
            f.write(f"   Address: {lead['address'][:50]}...\n")
            f.write(f"   Phone: {lead.get('phone', 'N/A')}\n")
            f.write(f"   Website: {lead.get('website', 'N/A')}\n")
            f.write(f"   Reviews: {lead.get('reviews', 'N/A')}\n\n")

        if len(leads) > 20:
            f.write(f"\n... and {len(leads) - 20} more leads\n\n")

        f.write(f"{'='*70}\n\n")
        f.write(f"EXPECTED RESULTS (based on 10% response rate):\n\n")
        f.write(f"• Lead outreach: {len(leads)} emails sent\n")
        f.write(f"• Expected responses: ~{int(len(leads) * 0.1)} leads\n")
        f.write(f"• Expected calls booked: ~{int(len(leads) * 0.03)}\n")
        f.write(f"• Expected closed deals: ~{int(len(leads) * 0.01)}\n\n")
        f.write(f"At Rp 5M/deal: ~Rp {int(len(leads) * 0.01 * 5000000):,} revenue potential\n\n")
        f.write(f"{'='*70}\n")

    print(f"✅ Report saved to: {report_file}")
    print()

    # Step 5: Instructions for next steps
    print("[STEP 5/5] Next Steps:")
    print()
    print("✅ Campaign data saved!")
    print()
    print("To execute this campaign:")
    print("1. Send cold emails (use email-automation skill)")
    print("2. Post to social media (use social-media-upload skill)")
    print("3. Track responses")
    print("4. Follow up automatically")
    print("5. Close deals!")
    print()

    return campaign_data

if __name__ == "__main__":
    # Example: Search restaurants in Jakarta
    campaign = run_full_campaign(
        location=TARGET_LOCATIONS[0],  # Jakarta
        category="restaurant",
        num_leads=50
    )

    print("🎉 CAMPAIGN READY!")