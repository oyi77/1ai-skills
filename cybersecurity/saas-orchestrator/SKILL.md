---
name: saas-orchestrator
description: Wraps the existing 23 security skills into a sellable security-as-a-Service
  offering — automated pentest reports, compliance checking, client management
domain: cybersecurity
---

## Overview

Orchestration layer that packages the existing 23 security skills (bug-hunting, vulnerability-scanner, recon-automation, api-destroyer, auth-killer, cloud-hunter, etc.) into a sellable Security-as-a-Service business. Handles the full client lifecycle: onboarding, scope definition, scan orchestration, report generation, delivery, and billing. Transforms security skills from ad-hoc hunting into a repeatable revenue stream.

## Required Tools

- **Client Management**: Supabase/Firebase for client database, or simple JSON/YAML files
- **Scheduling**: cron jobs or Temporal/Prefect for scan orchestration
- **Reporting**: Markdown → PDF (pandoc or md-to-pdf), email delivery (SendGrid)
- **Billing**: Stripe Subscriptions API or Lemon Squeezy
- **Notifications**: Slack webhooks, email alerts
- **Storage**: S3/R2 for scan results, reports, and evidence
- **CLI**: All existing security skills are invoked via their SKILL.md patterns

## Capabilities

- Onboard clients with automated scope definition
- Schedule and orchestrate scans across multiple security skills
- Aggregate findings from multiple skills into unified reports
- Generate professional PDF reports with severity ratings, PoCs, and remediation
- Manage client tiers (basic scan, full pentest, continuous monitoring)
- Handle billing and subscription management
- Track client scan history and trend analysis
- Compliance mapping (OWASP Top 10, CIS Benchmarks, SOC2)

## When to Use

- You want to monetize the existing security skills as a recurring service
- Clients request security assessments or pentests
- You need to run the same security checks across multiple targets regularly
- You want to offer tiered security packages (basic, standard, premium)
- Building a security consulting or audit business

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

This section covers pseudo code for saas orchestrator.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Phase 1: Client Onboarding

```yaml
# Client configuration file: clients/{client-slug}/config.yaml
client:
  name: "Acme Corp"
  slug: "acme-corp"
  tier: "premium"  # basic | standard | premium
  contact:
    email: "security@acme.com"
    name: "John Doe"
  billing:
    stripe_customer_id: "cus_xxx"
    subscription_id: "sub_xxx"
    plan: "monthly_premium"

scope:
  domains:
    - "acme.com"
    - "*.acme.com"
    - "api.acme.com"
  exclude:
    - "legacy.acme.com"
    - "*.staging.acme.com"
  ips:
    - "203.0.113.0/24"
  apis:
    - base_url: "https://api.acme.com/v2"
      auth_type: "bearer"
      endpoints_file: "endpoints.json"

compliance:
  frameworks: ["owasp-top10", "cis-benchmark"]
  report_format: "pdf"
  delivery: "email"
```

```python
# Client onboarding flow
def onboard_client(client_data):
    # 1. Create client directory
    client_dir = f"clients/{client_data['slug']}"
    os.makedirs(client_dir, exist_ok=True)

    # 2. Generate config.yaml
    config = {
        'client': client_data,
        'scope': define_scope(client_data),
        'compliance': get_compliance_requirements(client_data['tier'])
    }
    write_yaml(f"{client_dir}/config.yaml", config)

    # 3. Set up Stripe subscription
    subscription = create_stripe_subscription(
        customer_email=client_data['contact']['email'],
        plan=client_data['tier']
    )

    # 4. Schedule recurring scans
    schedule_scans(client_data['slug'], client_data['tier'])

    # 5. Send welcome email with onboarding guide
    send_welcome_email(client_data)

    return client_dir
```

### Phase 2: Scan Orchestration by Tier

```python
TIER_SCANS = {
    "basic": {
        "skills": ["recon-automation", "vulnerability-scanner"],
        "frequency": "monthly",
        "max_targets": 3
    },
    "standard": {
        "skills": [
            "recon-automation", "vulnerability-scanner",
            "api-destroyer", "auth-killer"
        ],
        "frequency": "bi-weekly",
        "max_targets": 10
    },
    "premium": {
        "skills": [
            "recon-automation", "vulnerability-scanner",
            "api-destroyer", "auth-killer", "bug-hunting",
            "cloud-hunter", "supply-chain-attacker"
        ],
        "frequency": "weekly",
        "max_targets": -1  # unlimited
    },
    "pentest": {
        "skills": [
            "recon-automation", "vulnerability-scanner",
            "api-destroyer", "auth-killer", "bug-hunting",
            "cloud-hunter", "fuzz-master", "bug-chain-builder",
            "mobile-hacking", "supply-chain-attacker"
        ],
        "frequency": "one-time",
        "max_targets": -1
    }
}

def orchestrate_scan(client_slug):
    """Run a full security assessment for a client."""
    config = load_client_config(client_slug)
    tier = config['client']['tier']
    scan_config = TIER_SCANS[tier]

    results = {
        'client': client_slug,
        'tier': tier,
        'started_at': datetime.utcnow().isoformat(),
        'findings': [],
        'scan_results': {}
    }

    # Phase 1: Reconnaissance (always first)
    recon_result = invoke_skill(
        skill="recon-automation",
        targets=config['scope']['domains'],
        output_dir=f"clients/{client_slug}/scans/recon/"
    )
    results['scan_results']['recon'] = recon_result

    # Phase 2: Run tier-specific skills
    for skill_name in scan_config['skills']:
        if skill_name == "recon-automation":
            continue  # Already done

        skill_result = invoke_skill(
            skill=skill_name,
            targets=recon_result.get('discovered_assets', config['scope']),
            output_dir=f"clients/{client_slug}/scans/{skill_name}/"
        )
        results['scan_results'][skill_name] = skill_result

        # Aggregate findings
        for finding in skill_result.get('findings', []):
            results['findings'].append({
                'skill': skill_name,
                'severity': finding['severity'],
                'title': finding['title'],
                'description': finding['description'],
                'evidence': finding.get('evidence'),
                'remediation': finding.get('remediation')
            })

    # Phase 3: Deduplicate and prioritize
    results['findings'] = deduplicate_findings(results['findings'])
    results['findings'].sort(key=lambda f: severity_order(f['severity']))

    results['completed_at'] = datetime.utcnow().isoformat()
    results['summary'] = generate_summary(results)

    # Save results
    save_results(client_slug, results)
    return results

def invoke_skill(skill, targets, output_dir):
    """Invoke a security skill with proper parameters."""
    # Each skill follows its SKILL.md interface
    # This is the orchestration point
    os.makedirs(output_dir, exist_ok=True)

    # Load skill definition
    skill_def = load_skill(skill)

    # Execute skill-specific logic
    # Skills return structured results with findings
    return skill_def.execute(targets=targets, output_dir=output_dir)
```

### Phase 3: Report Generation

```python
def generate_report(client_slug, results):
    """Generate professional security assessment report."""

    config = load_client_config(client_slug)

    report = f"""---
title: "Security Assessment Report"
client: "{config['client']['name']}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
tier: "{config['client']['tier']}"
---

# Security Assessment Report

**Client:** {config['client']['name']}
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Assessment Type:** {config['client']['tier'].title()}
**Scope:** {', '.join(config['scope']['domains'])}

## Executive Summary

{generate_executive_summary(results)}

## Risk Overview

| Severity | Count |
|----------|-------|
| Critical | {count_by_severity(results, 'critical')} |
| High | {count_by_severity(results, 'high')} |
| Medium | {count_by_severity(results, 'medium')} |
| Low | {count_by_severity(results, 'low')} |
| Info | {count_by_severity(results, 'info')} |

## Findings

"""

    for i, finding in enumerate(results['findings'], 1):
        report += f"""### {i}. {finding['title']}

**Severity:** {finding['severity'].upper()}
**Category:** {finding['skill']}
**CVSS Score:** {finding.get('cvss', 'N/A')}

**Description:**
{finding['description']}

**Evidence:**
```
{finding.get('evidence', 'No direct evidence captured')}
```

**Remediation:**
{finding.get('remediation', 'Contact security team for remediation guidance')}

---

"""

    # Compliance mapping section
    if config['compliance']['frameworks']:
        report += generate_compliance_section(results, config['compliance']['frameworks'])

    # Save as markdown and convert to PDF
    report_path = f"clients/{client_slug}/reports/{datetime.now().strftime('%Y-%m-%d')}-assessment.md"
    write_file(report_path, report)

    # Convert to PDF
    pdf_path = report_path.replace('.md', '.pdf')
    subprocess.run(['pandoc', report_path, '-o', pdf_path,
                    '--pdf-engine=wkhtmltopdf',
                    '-V', 'margin-top=20mm'])

    return pdf_path
```

### Phase 4: Delivery & Billing

```python
def deliver_report(client_slug, report_path):
    """Deliver report to client and handle billing."""
    config = load_client_config(client_slug)

    # 1. Send report via email
    send_email(
        to=config['client']['contact']['email'],
        subject=f"Security Assessment Report - {datetime.now().strftime('%B %Y')}",
        body=f"Your {config['client']['tier']} security assessment is complete. See attached report.",
        attachments=[report_path]
    )

    # 2. Upload to client portal (S3/R2)
    s3_key = f"reports/{client_slug}/{os.path.basename(report_path)}"
    upload_to_s3(report_path, s3_key)

    # 3. Create Stripe invoice item for usage-based billing
    if config['client']['tier'] == 'pentest':
        # One-time pentest billing
        stripe.InvoiceItem.create(
            customer=config['billing']['stripe_customer_id'],
            amount=get_tier_price(config['client']['tier']),
            currency='usd',
            description=f"Security Assessment - {datetime.now().strftime('%B %Y')}"
        )

    # 4. Notify via Slack
    notify_slack(
        f"Report delivered to {config['client']['name']} "
        f"({count_findings(results)} findings, "
        f"{count_critical(results)} critical)"
    )

def schedule_scans(client_slug, tier):
    """Schedule recurring scans based on tier."""
    frequency = TIER_SCANS[tier]['frequency']

    if frequency == "weekly":
        cron = "0 2 * * 1"  # Monday 2 AM
    elif frequency == "bi-weekly":
        cron = "0 2 1,15 * *"  # 1st and 15th
    elif frequency == "monthly":
        cron = "0 2 1 *"  # 1st of month
    else:
        return  # One-time, no scheduling

    # Add to cron
    add_cron_job(
        cron=cron,
        command=f"python -m orchestrator.scan --client {client_slug}",
        job_id=f"scan-{client_slug}"
    )
```

### Phase 5: Client Dashboard Data

```python
def get_client_dashboard(client_slug):
    """Generate dashboard data for client portal."""
    config = load_client_config(client_slug)
    history = load_scan_history(client_slug)

    return {
        "client": config['client']['name'],
        "tier": config['client']['tier'],
        "last_scan": history[-1]['completed_at'] if history else None,
        "next_scan": get_next_scan_time(client_slug),
        "trend": {
            "total_findings": [h['summary']['total'] for h in history[-6:]],
            "critical_findings": [h['summary']['critical'] for h in history[-6:]],
            "months": [h['completed_at'][:7] for h in history[-6:]]
        },
        "current_risk_score": calculate_risk_score(history[-1] if history else None),
        "compliance_status": get_compliance_status(client_slug)
    }
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Skill invocation timeout | Target too large or skill hung | Set per-skill timeout (30min default), retry once |
| No findings from skill | Wrong targets or skill misconfigured | Validate target format, check skill dependencies |
| PDF generation fails | pandoc not installed or template error | `brew install pandoc wkhtmltopdf`, verify markdown |
| Stripe billing fails | Invalid customer ID | Verify Stripe customer exists, check API key |
| Report delivery fails | Email bounce or S3 permissions | Check email validity, verify S3 bucket policy |
| Duplicate findings | Same vuln found by multiple skills | Deduplicate by title+target+port before reporting |
| Client scope exceeds tier | Too many targets for plan | Enforce target limits, suggest tier upgrade |

## Common Patterns

- **Follow the principle of least privilege** — use the minimum permissions needed for each task
- **Document everything** — maintain logs of all actions, configurations, and findings
- **Verify before acting** — confirm assumptions about the environment before making changes
- **Automate repetitive steps** — script common workflows to reduce human error
### Tiered Pricing Structure
```yaml
# Stripe price objects
plans:
  basic:
    price_id: "price_basic_monthly"
    amount: 49900  # $499/mo
    features: ["monthly_scan", "basic_report", "email_support"]
  standard:
    price_id: "price_standard_monthly"
    amount: 149900  # $1,499/mo
    features: ["biweekly_scan", "full_report", "api_testing", "slack_support"]
  premium:
    price_id: "price_premium_monthly"
    amount: 499900  # $4,999/mo
    features: ["weekly_scan", "full_report", "all_skills", "priority_support", "compliance"]
  pentest:
    price_id: "price_pentest_onetime"
    amount: 999900  # $9,999 one-time
    features: ["full_pentest", "all_skills", "manual_review", "executive_report"]
```

### Finding Severity Mapping
```python
SEVERITY_CVSS = {
    "critical": (9.0, 10.0),
    "high": (7.0, 8.9),
    "medium": (4.0, 6.9),
    "low": (0.1, 3.9),
    "info": (0.0, 0.0)
}

def map_severity(cvss_score):
    for severity, (low, high) in SEVERITY_CVSS.items():
        if low <= cvss_score <= high:
            return severity
    return "info"
```

### Compliance Report Template
```python
def generate_compliance_section(results, frameworks):
    section = "## Compliance Mapping\n\n"
    for framework in frameworks:
        controls = load_framework_controls(framework)
        section += f"### {framework.upper()}\n\n"
        section += "| Control | Status | Findings |\n|---------|--------|----------|\n"
        for control in controls:
            related = find_related_findings(results, control)
            status = "PASS" if not related else "FAIL"
            section += f"| {control['id']} | {status} | {len(related)} |\n"
    return section
```
## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Exceeding the authorized scope of the engagement
- Leaving persistent access mechanisms without explicit approval
- Causing denial-of-service on production systems during testing
## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- All exploited vulnerabilities documented with reproduction steps
- Scope boundaries confirmed — only authorized targets were tested
- Remediation recommendations included for every finding
