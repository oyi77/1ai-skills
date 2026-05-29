---
name: legal-compliance
description: Contract generation, terms of service, privacy policies, GDPR/CCPA compliance checks, regulatory monitoring, entity management
---

## Overview

Automate legal and compliance tasks that solo entrepreneurs spend disproportionate time on — or worse, skip entirely and face liability. Generate contracts from templates, monitor regulatory changes, ensure GDPR/CCPA compliance, and manage business entities. This skill does NOT replace legal counsel for complex matters but handles 80% of routine legal work.

## Required Tools

- **Document Generation**: Pandoc, DOCX/PDF templating (Handlebars, Jinja2)
- **Compliance**: OneTrust API, Cookiebot, or custom compliance scanners
- **Monitoring**: RSS feeds for regulatory changes, Google Alerts for legal keywords
- **Storage**: Encrypted document storage (S3 with encryption, or local encrypted vault)
- **E-Signature**: DocuSign API, HelloSign API, or PandaDoc
- **Entity Management**: Stripe Atlas, Clerky, or custom tracking
- **Python 3.10+** or **Node.js 18+** for automation scripts

## Capabilities

- Generate contracts, NDAs, ToS, and privacy policies from templates
- Run GDPR/CCPA compliance scans on websites and apps
- Monitor regulatory changes in relevant jurisdictions
- Manage business entities and annual filings
- Automate e-signature workflows
- Track compliance deadlines and renewals
- Generate data processing agreements (DPA)
- Audit cookie consent and data collection practices

## When to Use

- Starting a new business and need legal documents
- Launching a SaaS product requiring ToS and privacy policy
- Onboarding clients who need contracts signed
- Operating in EU/California and need GDPR/CCPA compliance
- Annual entity filings and compliance renewals
- Adding new data collection that requires privacy review

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Entity Setup & Management

```python
ENTITIES = {
  "main_llc": {
    "name": "My AI Company LLC",
    "state": "Wyoming",  # Privacy-friendly, no state income tax
    "formation_date": "2026-01-15",
    "ein": "XX-XXXXXXX",
    "registered_agent": "Northwest Registered Agent",
    "annual_report_due": "2027-01-15",
    "franchise_tax_due": "2027-04-15"
  }
}

# Track compliance deadlines
COMPLIANCE_CALENDAR = [
  {"entity": "main_llc", "task": "Annual Report", "due": "2027-01-15", "recurring": "yearly"},
  {"entity": "main_llc", "task": "Franchise Tax", "due": "2027-04-15", "recurring": "yearly"},
  {"entity": "main_llc", "task": "BOI Report Update", "due": "on_change", "recurring": "event"},
  {"entity": "main_llc", "task": "Operating Agreement Review", "due": "2026-07-15", "recurring": "yearly"}
]

def check_upcoming_deadlines(days_ahead=30):
    upcoming = []
    for item in COMPLIANCE_CALENDAR:
        if item["due"] != "on_change":
            due = datetime.strptime(item["due"], "%Y-%m-%d")
            if 0 < (due - datetime.now()).days <= days_ahead:
                upcoming.append(item)
    return upcoming
```

### Contract Generation

```python
CONTRACT_TEMPLATES = {
  "nda_mutual": "templates/nda_mutual.md",
  "nda_one_way": "templates/nda_one_way.md",
  "service_agreement": "templates/service_agreement.md",
  "consulting_agreement": "templates/consulting_agreement.md",
  "independent_contractor": "templates/independent_contractor.md",
  "dpa": "templates/data_processing_agreement.md"
}

def generate_contract(template_name, variables):
    """
    Generate a contract from template with variables.
    Output: DOCX and PDF
    """
    template_path = CONTRACT_TEMPLATES[template_name]

    # Load template
    with open(template_path) as f:
        template = f.read()

    # Fill variables
    for key, value in variables.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))

    # Add legal boilerplate
    template = add_governing_law(template, variables.get("jurisdiction", "Delaware"))
    template = add_dispute_resolution(template, variables.get("dispute_method", "arbitration"))

    # Generate documents
    docx_path = f"output/{template_name}_{date.today()}.docx"
    pdf_path = f"output/{template_name}_{date.today()}.pdf"

    # Markdown → DOCX → PDF
    pandoc_convert(template, docx_path)
    docx_to_pdf(docx_path, pdf_path)

    return {"docx": docx_path, "pdf": pdf_path}

# Example usage
contract = generate_contract("nda_mutual", {
    "party_a_name": "My AI Company LLC",
    "party_a_address": "123 Main St, Cheyenne, WY 82001",
    "party_b_name": "Client Corp",
    "party_b_address": "456 Oak Ave, San Francisco, CA 94102",
    "effective_date": "May 19, 2026",
    "term_years": "2",
    "jurisdiction": "Delaware"
})
```

### Website Compliance Scan

```python
def scan_website_compliance(url):
    """
    Scan website for GDPR/CCPA compliance issues.
    """
    issues = []

    # 1. Cookie consent check
    cookies = scan_cookies(url)
    if not cookies.has_consent_banner:
        issues.append({
            "severity": "critical",
            "category": "cookies",
            "issue": "No cookie consent banner detected",
            "fix": "Add cookie consent banner (Cookiebot, OneTrust, or custom)"
        })

    # 2. Privacy policy check
    privacy = check_privacy_policy(url)
    if not privacy.exists:
        issues.append({
            "severity": "critical",
            "category": "privacy",
            "issue": "No privacy policy page found",
            "fix": "Create privacy policy covering data collection, usage, and rights"
        })
    elif privacy.last_updated_days_ago > 365:
        issues.append({
            "severity": "warning",
            "category": "privacy",
            "issue": f"Privacy policy not updated in {privacy.last_updated_days_ago} days",
            "fix": "Review and update privacy policy annually"
        })

    # 3. Data collection audit
    forms = scan_forms(url)
    for form in forms:
        if form.collects_pii and not form.has_consent_checkbox:
            issues.append({
                "severity": "high",
                "category": "data_collection",
                "issue": f"Form '{form.name}' collects PII without consent checkbox",
                "fix": "Add explicit consent checkbox with link to privacy policy"
            })

    # 4. Third-party scripts
    scripts = scan_third_party(url)
    for script in scripts:
        if script.tracks_users and not script.in_consent_manager:
            issues.append({
                "severity": "medium",
                "category": "tracking",
                "issue": f"Script '{script.domain}' tracks users without consent",
                "fix": "Add script to consent manager or load conditionally"
            })

    # 5. GDPR-specific checks
    if targets_eu(url):
        if not has_data_deletion_process(url):
            issues.append({
                "severity": "critical",
                "category": "gdpr",
                "issue": "No data deletion request process (Right to Erasure)",
                "fix": "Add data deletion request form or email process"
            })
        if not has_data_export_process(url):
            issues.append({
                "severity": "high",
                "category": "gdpr",
                "issue": "No data export process (Right to Portability)",
                "fix": "Add data export feature or manual request process"
            })

    return {
        "url": url,
        "scan_date": datetime.now().isoformat(),
        "issues": issues,
        "score": calculate_compliance_score(issues),
        "status": "pass" if len([i for i in issues if i["severity"] == "critical"]) == 0 else "fail"
    }
```

### Regulatory Monitoring

```python
REGULATORY_SOURCES = [
    # GDPR
    {"name": "EDPB", "url": "https://edpb.europa.eu/news/news_en", "region": "EU"},
    {"name": "ICO", "url": "https://ico.org.uk/action-and-policy/", "region": "UK"},

    # CCPA/US Privacy
    {"name": "CPPA", "url": "https://cppa.ca.gov/announcements/", "region": "US-CA"},
    {"name": "FTC", "url": "https://www.ftc.gov/news-events", "region": "US"},

    # Industry-specific
    {"name": "SEC", "url": "https://www.sec.gov/news", "region": "US", "industry": "finance"},
    {"name": "HIPAA", "url": "https://www.hhs.gov/hipaa/", "region": "US", "industry": "health"}
]

def monitor_regulatory_changes():
    """
    Check regulatory sources for new announcements.
    Alert on changes relevant to business operations.
    """
    for source in REGULATORY_SOURCES:
        updates = fetch_rss(source["url"])

        for update in updates:
            relevance = assess_relevance(update, business_profile)

            if relevance.score > 0.7:
                alert = {
                    "source": source["name"],
                    "title": update.title,
                    "summary": update.summary,
                    "relevance": relevance.reason,
                    "action_required": relevance.action,
                    "deadline": relevance.deadline,
                    "url": update.link
                }

                # Send alert
                send_slack_alert(alert)
                send_email_alert(alert)

                # Log for tracking
                log_regulatory_alert(alert)
```

### E-Signature Workflow

```javascript
async function sendForSignature(document, recipients) {
  // DocuSign integration
  const envelope = await docusign.createEnvelope({
    emailSubject: `Please sign: ${document.name}`,
    documents: [{
      documentId: "1",
      name: document.name,
      documentBase64: document.base64
    }],
    recipients: {
      signers: recipients.map((r, i) => ({
        email: r.email,
        name: r.name,
        recipientId: String(i + 1),
        routingOrder: String(i + 1),
        tabs: {
          signHereTabs: [{
            documentId: "1",
            pageNumber: document.signaturePage,
            xPosition: "200",
            yPosition: "400"
          }]
        }
      }))
    },
    status: "sent"
  });

  // Track envelope
  await trackEnvelope(envelope.envelopeId, {
    document: document.name,
    recipients: recipients.map(r => r.email),
    sent_at: new Date()
  });

  return envelope.envelopeId;
}
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `TEMPLATE_NOT_FOUND` | Contract template missing | Use fallback generic template, flag for review |
| `COMPLIANCE_SCAN_FAIL` | Website blocked scanner | Use headless browser, retry with different user-agent |
| `ENVELOPE_DECLINED` | Recipient declined to sign | Log reason, contact recipient, modify terms if needed |
| `REGULATORY_ALERT_FALSE` | Irrelevant alert triggered | Update relevance model, add to ignore list |
| `ENTITY_OVERDUE` | Missed filing deadline | File immediately, pay late fees, set better reminders |
| `PDF_GENERATION_FAIL` | Pandoc conversion error | Fall back to DOCX only, alert for manual PDF creation |

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### Privacy Policy Auto-Generation
```python
privacy_policy = generate_privacy_policy({
    "company": "My AI Company LLC",
    "website": "https://mysite.com",
    "data_collected": ["email", "name", "usage_analytics", "cookies"],
    "third_parties": ["Stripe (payments)", "Google Analytics", "Intercom (support)"],
    "retention_period": "2 years or until account deletion",
    "user_rights": ["access", "delete", "export", "opt-out"],
    "jurisdiction": ["GDPR (EU)", "CCPA (California)"],
    "contact_email": "privacy@mysite.com",
    "dpo_required": false
})
```

### Compliance Checklist per Jurisdiction
| Requirement | GDPR (EU) | CCPA (CA) | PIPEDA (CA) |
|-------------|-----------|-----------|-------------|
| Consent before collection | Explicit opt-in | Opt-out only | Implied consent OK |
| Right to delete | Yes (30 days) | Yes (45 days) | Yes |
| Right to export | Yes | Yes | Yes |
| Data breach notification | 72 hours | "Without unreasonable delay" | "As soon as feasible" |
| DPO required | Sometimes | No | No |
| Cookie consent | Required | Not required | Implied OK |

### Annual Compliance Calendar
- January: Annual report filing, privacy policy review
- April: Tax filings, DPA renewals
- July: Mid-year compliance audit, cookie scan
- October: Pre-year-end entity review, regulatory update check
- December: Year-end compliance report, renew expiring agreements

## Red Flags

- Claiming completion without running verification
- Skipping the analysis phase and jumping to implementation
- Ignoring existing codebase patterns and conventions

## Verification

- [ ] Output matches the original requirements
- [ ] All code or content runs without errors
- [ ] Edge cases have been considered and handled
- [ ] No placeholder content or TODOs remain