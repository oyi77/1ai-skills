#!/usr/bin/env python3
"""
OpenFang-Style Hand: LEAD
Runs daily. Discovers prospects matching your ICP, enriches them with web research,
scores 0-100, deduplicates against existing database, delivers qualified leads in CSV/JSON/Markdown.

Features:
- ICP (Ideal Customer Profile) definition
- Prospect discovery via web search
- Lead enrichment (company info, contacts, etc.)
- Lead scoring (0-100)
- Deduplication against existing database
- Export to CSV, JSON, Markdown
"""

import json
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/openclaw/.openclaw/workspace")
HAND_DIR = BASE_DIR / "hands" / "lead"
WORK_DIR = HAND_DIR / "workspace"
LOGS_DIR = BASE_DIR / "logs"
EXPORT_DIR = HAND_DIR / "exports"

# Ensure directories exist
HAND_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "lead_hand.log"
ICP_FILE = HAND_DIR / "icp.json"
DATABASE_FILE = HAND_DIR / "leads_db.json"

def log(message, level="INFO"):
    """Log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}\n"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

def load_icp():
    """Load Ideal Customer Profile"""
    try:
        if ICP_FILE.exists():
            with open(ICP_FILE, 'r') as f:
                return json.load(f)

        # Create default ICP for BerkahKarya
        default_icp = {
            "name": "BerkahKarya Lead Generation",
            "version": "1.0",
            "target_profile": {
                "company_type": ["SME", "e-commerce", "digital business", "content creators"],
                "size": ["small", "medium"],
                "industry": ["technology", "marketing", "e-commerce", "digital products"],
                "location": ["Indonesia"],
                "keywords": ["digital marketing", "AI tools", "automation", "social media", "content creation"]
            },
            "enrichment_fields": [
                "company_website",
                "company_size",
                "industry",
                "location",
                "contact_email",
                "contact_name",
                "social_media",
                "revenue_estimate"
            ]
        }

        with open(ICP_FILE, 'w') as f:
            json.dump(default_icp, f, indent=2)

        return default_icp
    except Exception as e:
        log(f"❌ Error loading ICP: {e}")
        return None

def load_leads_database():
    """Load existing leads database for deduplication"""
    try:
        if DATABASE_FILE.exists():
            with open(DATABASE_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        log(f"❌ Error loading database: {e}")
        return []

def save_leads_database(leads):
    """Save leads database"""
    try:
        with open(DATABASE_FILE, 'w') as f:
            json.dump(leads, f, indent=2)
        log(f"✅ Database saved: {len(leads)} leads")
        return True
    except Exception as e:
        log(f"❌ Error saving database: {e}")
        return False

def discover_prospects(icp, max_prospects=10):
    """Discover prospects matching ICP"""
    log(f"Discovering prospects (max {max_prospects})...")

    # In full implementation, this would:
    # 1. Use web search APIs (Google, LinkedIn, etc.)
    # 2. Search for terms matching ICP keywords
    # 3. Extract company URLs and basic info

    # For now, generate sample prospects based on ICP
    sample_prospects = []

    base_prospects = [
        {
            "name": "Digital Nusantara Agency",
            "website": "https://digitalnusantara.com",
            "industry": "Digital Marketing",
            "location": "Jakarta",
            "size": "Small (10-50 employees)"
        },
        {
            "name": "Indonesian E-Commerce Solutions",
            "website": "https://iecs.co.id",
            "industry": "Technology",
            "location": "Bandung",
            "size": "Medium (50-200 employees)"
        },
        {
            "name": "Content Creator Hub",
            "website": "https://creatorhub.id",
            "industry": "Content Creation",
            "location": "Surabaya",
            "size": "Small (5-20 employees)"
        },
        {
            "name": "AI Tools Indonesia",
            "website": "https://aitoolsindo.com",
            "industry": "Technology",
            "location": "Jakarta",
            "size": "Start-up"
        },
        {
            "name": "Social Media Automation",
            "website": "https://social-auto.id",
            "industry": "Marketing",
            "location": "Jakarta",
            "size": "Small (10-30 employees)"
        }
    ]

    for i, prospect in enumerate(base_prospects[:max_prospects]):
        prospect['discovered'] = datetime.now().isoformat()
        sample_prospects.append(prospect)

    log(f"✅ Discovered {len(sample_prospects)} prospects")
    return sample_prospects

def enrich_prospect(prospect):
    """Enrich prospect with additional research"""
    # In full implementation, this would:
    # 1. Visit company website
    # 2. Scrape for contact info
    # 3. Check social media presence
    # 4. Estimate company size, revenue
    # 5. Extract additional details

    # For now, add mock enrichment data
    enriched = prospect.copy()

    # Add enrichment based on keywords
    if "marketing" in enriched.get('industry', '').lower():
        enriched['contact_email'] = f"contact@{enriched['name'].lower().replace(' ', '')}.com"
        enriched['social_media'] = {
            'linkedin': f"linkedin.com/company/{enriched['name'].lower().replace(' ', '')}",
            'instagram': f"instagram.com/{enriched['name'].lower().replace(' ', '')}"
        }
        enriched['revenue_estimate'] = "IDR 500M - 5B"
        enriched['enrichment_details'] = {
            'website_status': 'Active',
            'social_presence': 'High',
            'content_frequency': 'Daily posts'
        }

    elif "technology" in enriched.get('industry', '').lower() or "ai" in enriched.get('name', '').lower():
        enriched['contact_email'] = f"business@{enriched['name'].lower().replace(' ', '')}.com"
        enriched['social_media'] = {
            'linkedin': f"linkedin.com/company/{enriched['name'].lower().replace(' ', '')}",
            'github': f"github.com/{enriched['name'].lower().replace(' ', '-')}"
        }
        enriched['revenue_estimate'] = "IDR 1B - 20B"
        enriched['enrichment_details'] = {
            'website_status': 'Active',
            'social_presence': 'Medium',
            'tech_stack': 'Modern'
        }

    enriched['enriched'] = True
    enriched['enriched_at'] = datetime.now().isoformat()

    return enriched

def score_prospect(prospect, icp):
    """Score prospect 0-100 based on ICP match"""

    score = 50  # Base score

    # Industry match
    industry = prospect.get('industry', '').lower()
    icp_industries = [i.lower() for i in icp['target_profile'].get('industry', [])]
    if any(ind in industry for ind in icp_industries):
        score += 20
        log(f"  + Industry match: {prospect['industry']}")
    else:
        log(f"  - No industry match: {prospect['industry']}")

    # Keywrod match
    keywords = icp['target_profile'].get('keywords', [])
    name = prospect.get('name', '').lower()

    for keyword in keywords:
        if keyword.lower() in name:
            score += 10
            log(f"  + Keyword match: {keyword}")

    # Location match
    location = prospect.get('location', '').lower()
    icp_locations = [l.lower() for l in icp['target_profile'].get('location', [])]
    if any(loc in location for loc in icp_locations):
        score += 10
        log(f"  + Location match: {prospect['location']}")

    # Enrichment completeness
    required_fields = icp.get('enrichment_fields', [])
    if required_fields:
        filled_fields = sum(1 for field in required_fields if field in prospect and prospect[field])
        completeness_score = (filled_fields / len(required_fields)) * 10

        log(f"  Data completeness: {filled_fields}/{len(required_fields)} = {completeness_score:.1f}")
        score = score * (0.8 + (completeness_score / 100))  # Boost by completeness
    else:
        completeness_score = 0

    # Cap score at 100
    score = min(100, int(score))

    log(f"  Final score: {score}/100")

    return score

def deduplicate_prospects(new_prospects, existing_database):
    """Deduplicate against existing database"""
    log(f"Deduplicating {len(new_prospects)} prospects against {len(existing_database)} existing...")

    deduplicated = []

    for prospect in new_prospects:
        is_duplicate = False

        for existing in existing_database:
            # Check by website or name
            if (prospect.get('website') == existing.get('website') or
                prospect.get('name') == existing.get('name')):
                is_duplicate = True
                log(f"  - Duplicate skipped: {prospect['name']}")
                break

        if not is_duplicate:
            deduplicated.append(prospect)

    log(f"✅ {len(deduplicated)} new prospects (from {len(new_prospects)} total)")
    return deduplicated

def export_leads_csv(leads, filename=None):
    """Export leads to CSV"""
    if not filename:
        filename = EXPORT_DIR / f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        with open(filename, 'w', newline='') as f:
            if leads:
                fieldnames = list(leads[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(leads)

        log(f"✅ CSV exported: {filename}")
        return str(filename)
    except Exception as e:
        log(f"❌ CSV export error: {e}")
        return None

def export_leads_json(leads, filename=None):
    """Export leads to JSON"""
    if not filename:
        filename = EXPORT_DIR / f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(filename, 'w') as f:
            json.dump(leads, f, indent=2)

        log(f"✅ JSON exported: {filename}")
        return str(filename)
    except Exception as e:
        log(f"❌ JSON export error: {e}")
        return None

def export_leads_markdown(leads, filename=None):
    """Export leads to Markdown"""
    if not filename:
        filename = EXPORT_DIR / f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    try:
        with open(filename, 'w') as f:
            f.write(f"# Leads Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Session: {datetime.now().strftime('%Y%m%d_%H%M%S')}\n")
            f.write(f"Collector: {load_icp()['name']}\n")
            f.write(f"Total Leads: {len(leads)}\n\n")

            # Sort by score
            sorted_leads = sorted(leads, key=lambda x: x.get('score', 0), reverse=True)

            for i, lead in enumerate(sorted_leads, 1):
                f.write(f"## {i}. {lead.get('name', 'Unknown')}\n\n")
                f.write(f"- **Score:** {lead.get('score', 0)}/100\n")
                f.write(f"- **Website:** {lead.get('website', 'N/A')}\n")
                f.write(f"- **Industry:** {lead.get('industry', 'N/A')}\n")
                f.write(f"- **Location:** {lead.get('location', 'N/A')}\n")
                f.write(f"- **Size:** {lead.get('size', 'N/A')}\n")
                f.write(f"- **Revenue Estimate:** {lead.get('revenue_estimate', 'N/A')}\n")
                f.write(f"- **Contact:** {lead.get('contact_email', 'N/A')}\n\n")

        log(f"✅ Markdown exported: {filename}")
        return str(filename)
    except Exception as e:
        log(f"❌ Markdown export error: {e}")
        return None

def run_lead_hand():
    """Main LEAD hand execution"""
    log("="*70)
    log("OpenFang Hand: LEAD")
    log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("="*70)
    log(" ") 

    # Load ICP
    icp = load_icp()
    if not icp:
        log("❌ Cannot proceed without ICP")
        return {'status': 'failed', 'error': 'No ICP loaded'}

    log(f"ICP loaded: {icp['name']}")
    log(" ") 

    # Load existing database
    existing_database = load_leads_database()
    log(f"Existing database: {len(existing_database)} leads")

    # Discover prospects
    prospects = discover_prospects(icp, max_prospects=5)
    if not prospects:
        log("❌ No prospects discovered")
        return {'status': 'failed', 'error': 'No prospects found'}

    # Deduplicate
    new_prospects = deduplicate_prospects(prospects, existing_database)

    # Enrich and score each prospect
    qualified_leads = []

    for prospect in new_prospects:
        log(f"\nProcessing: {prospect['name']}")

        # Enrich
        enriched = enrich_prospect(prospect)

        # Score
        score = score_prospect(enriched, icp)
        enriched['score'] = score

        # Only include qualified leads (score >= 60)
        if score >= 60:
            qualified_leads.append(enriched)
            log(f"✅ Qualified ({score}/100): {prospect['name']}")
        else:
            log(f"❌ Not qualified ({score}/100): {prospect['name']}")

    log(" ") 
    log(f"Qualified leads: {len(qualified_leads)}")

    # Export leads
    if qualified_leads:
        csv_file = export_leads_csv(qualified_leads)
        json_file = export_leads_json(qualified_leads)
        md_file = export_leads_markdown(qualified_leads)

        # Update database
        updated_database = existing_database + qualified_leads
        save_leads_database(updated_database)

        log(" ")
        log("="*70)
        log(f"LEAD HAND COMPLETE")
        log(f"Qualified leads: {len(qualified_leads)}")
        log(f"Total database: {len(updated_database)}")
        log(f"CSV: {csv_file}")
        log(f"JSON: {json_file}")
        log(f"MD: {md_file}")
        log("="*70)

        return {
            'status': 'success',
            'qualified_leads': len(qualified_leads),
            'total_database': len(updated_database),
            'exports': {
                'csv': csv_file,
                'json': json_file,
                'markdown': md_file
            }
        }
    else:
        log("No qualified leads to export")
        return {
            'status': 'success',
            'qualified_leads': 0,
            'message': 'No qualified leads discovered'
        }

def main():
    """Main entry point"""
    run_lead_hand()
    return 0

if __name__ == "__main__":
    main()