---
name: legal-assistant
description: Use when legal assistant — contract review checklists, IP protection, business compliance, GDPR/privacy for digital products,
  DMCA, software licensing, employment law, and dispute resolution. Built for 1-person companies scaling to team.
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- legal
- compliance
- ip
- gdpr
- indonesia
- employment
- licensing
- dmca
version: 1.0.0

requires: []
---
# Legal Assistant

## When to Use
**Trigger phrases:**
- "legal assistant"
- "Legal assistant for BerkahKarya — contract review checklists, IP protection, Ind"


- Drafting legal documents (contracts, NDAs, agreements)
- Managing legal document templates
- Tracking legal compliance requirements
- Organizing legal document versions
- Automating legal document workflows


## When NOT to Use

- For processes that change daily (too much overhead)
- When the team is too small to benefit from SOPs
- For one-time events that will not repeat


## Overview

Legal Assistant streamlines operational efficiency for operational excellence.

## Workflow

```python
# Example: SOP execution tracker
def execute_sop(sop_name: str, steps: list[str]) -> dict:
    results = []
    for i, step in enumerate(steps, 1):
        try:
            result = execute_step(step)
            results.append({"step": i, "status": "ok", "result": result})
        except Exception as e:
            results.append({"step": i, "status": "error", "error": str(e)})
            break
    return {"sop": sop_name, "steps": results}
```

1. **Assess** — Evaluate current state and identify gaps
2. **Design** — Plan improved processes and workflows
3. **Implement** — Roll out changes with team alignment
4. **Measure** — Track operational KPIs
5. **Iterate** — Continuous improvement based on data
6. **Document** — Record templates, decisions, and evidence for audit readiness
7. **Review** — Schedule periodic legal health checks and update templates for regulatory changes

## SOP Template

- **Purpose** — Why this process exists
- **Scope** — Who and what it covers
- **Procedure** — Step-by-step instructions
- **Escalation** — When and how to escalate
- **Review** — Schedule for periodic updates

## Key Metrics

- Process completion time
- Error/rework rate
- Team satisfaction scores
- Cost per operation
- SLA compliance rate

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |
| "A template is good enough" | Templates miss jurisdiction-specific clauses and recent case law. Tailor every template to context. |
| "GDPR does not apply to small businesses" | GDPR applies if you process EU data subjects' personal data, regardless of company size. Fines scale but liability starts at day one. |
| "Open source means no licensing needed" | Open source licenses (MIT, GPL, Apache-2.0) have specific obligations. Violating terms can force product takedown or license revocation. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run legal assistant workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings

## Code Examples

### Contract Review Checklist Validator

```python
"""Validate contract review checklist for common omissions."""
from dataclasses import dataclass, field


@dataclass
class ContractClause:
    name: str
    present: bool = False
    notes: str = ""


@dataclass
class ContractReview:
    title: str
    clauses: list[ContractClause] = field(default_factory=list)
    jurisdiction: str = ""
    parties: list[str] = field(default_factory=list)

    def missing_clauses(self) -> list[str]:
        return [c.name for c in self.clauses if not c.present]

    def score(self) -> float:
        if not self.clauses:
            return 0.0
        return sum(1 for c in self.clauses if c.present) / len(self.clauses)


# Essential clauses for a software services agreement
ESSENTIAL_CLAUSES = [
    "Scope of Work", "Payment Terms", "IP Ownership",
    "Confidentiality", "Limitation of Liability", "Termination",
    "Data Processing", "Warranty Disclaimer", "Indemnification",
    "Dispute Resolution / Governing Law",
]


def review_contract(title: str, parties: list[str], present: list[str],
                    jurisdiction: str = "") -> ContractReview:
    clauses = [ContractClause(name=c, present=c in present) for c in ESSENTIAL_CLAUSES]
    review = ContractReview(title=title, clauses=clauses,
                            jurisdiction=jurisdiction, parties=parties)
    missing = review.missing_clauses()
    print(f"Contract: {review.title}")
    print(f"Score: {review.score():.0%} ({len(ESSENTIAL_CLAUSES) - len(missing)}/{len(ESSENTIAL_CLAUSES)})")
    if missing:
        print(f"Missing clauses: {', '.join(missing)}")
    if not jurisdiction:
        print("WARNING: No governing law/jurisdiction specified")
    return review
```

### GDPR Compliance Checker

```python
"""Check a digital product's GDPR compliance posture."""
from dataclasses import dataclass, field


@dataclass
class GDPRCheck:
    requirement: str
    met: bool = False
    evidence: str = ""


@dataclass
class GDPRStatus:
    product_name: str
    checks: list[GDPRCheck] = field(default_factory=list)

    def compliance_pct(self) -> float:
        if not self.checks:
            return 0.0
        return sum(1 for c in self.checks if c.met) / len(self.checks) * 100

    def gaps(self) -> list[str]:
        return [c.requirement for c in self.checks if not c.met]


GDPR_REQUIREMENTS = [
    ("Lawful basis documented (Art. 6)", "Record of processing activity"),
    ("Privacy notice provided (Art. 13-14)", "Published privacy policy"),
    ("Data retention schedule defined (Art. 5(1)(e))", "Retention policy"),
    ("Data Subject Access Request process (Art. 15)", "DSAR workflow"),
    ("Consent mechanism auditable (Art. 7)", "Consent records"),
    ("Data Processing Agreement with subprocessors (Art. 28)", "DPA signed"),
    ("Security measures documented (Art. 32)", "Security policy"),
    ("Breach notification procedure (Art. 33-34)", "Incident response plan"),
]


def assess_gdpr(product_name: str, met_requirements: list[str]) -> GDPRStatus:
    checks = [GDPRCheck(req, met=req in met_requirements, evidence=ev)
              for req, ev in GDPR_REQUIREMENTS]
    status = GDPRStatus(product_name=product_name, checks=checks)
    print(f"GDPR Assessment: {status.product_name}")
    print(f"Compliance: {status.compliance_pct():.0f}%")
    if gaps := status.gaps():
        print(f"Gaps ({len(gaps)}):")
        for g in gaps:
            print(f"  [ ] {g}")
    return status
```

### DMCA Takedown Notice Generator

```python
"""Generate a DMCA takedown notice for infringing content."""
from datetime import date


def generate_dmca_notice(
    copyright_holder: str,
    infringing_url: str,
    original_work_url: str,
    platform_name: str,
    platform_agent: str = "Copyright Agent",
    email: str = "",
) -> str:
    today = date.today().isoformat()
    notice = f"""
DATE: {today}

TO: {platform_name}
ATTN: {platform_agent}

DMCA TAKEDOWN NOTICE — 17 U.S.C. § 512(c)

1. IDENTIFICATION OF COPYRIGHTED WORK:
   {original_work_url}

2. IDENTIFICATION OF INFRINGING MATERIAL:
   {infringing_url}

3. CONTACT INFORMATION:
   Name: {copyright_holder}
   Email: {email or '[email required]'}

4. GOOD FAITH STATEMENT:
   I hereby state that I have a good faith belief that the disputed use
   is not authorized by the copyright owner, its agent, or the law.

5. ACCURACY STATEMENT UNDER PENALTY OF PERJURY:
   The information in this notification is accurate, and I swear under
   penalty of perjury that I am the copyright owner or authorized to
   act on behalf of the owner of an exclusive right that is infringed.

SIGNATURE: _________________________
"""
    return notice.strip()
```

### Software License Compatibility Checker

```python
"""Check compatibility between two open-source licenses."""

# SPDX license expression compatibility matrix (simplified)
_COMPATIBLE = {
    ("MIT", "MIT"): True,
    ("MIT", "Apache-2.0"): True,
    ("MIT", "GPL-2.0-only"): True,
    ("MIT", "GPL-3.0-only"): True,
    ("Apache-2.0", "MIT"): True,
    ("Apache-2.0", "Apache-2.0"): True,
    ("Apache-2.0", "GPL-3.0-only"): True,  # Apache 2.0 → GPL 3.0 (compatible one-way)
    ("Apache-2.0", "GPL-2.0-only"): False,  # NOT compatible
    ("GPL-3.0-only", "MIT"): True,
    ("GPL-3.0-only", "Apache-2.0"): True,
    ("GPL-3.0-only", "GPL-3.0-only"): True,
    ("GPL-2.0-only", "MIT"): True,
    ("GPL-2.0-only", "GPL-2.0-only"): True,
    ("GPL-2.0-only", "Apache-2.0"): False,
}


def check_license_compatibility(license_a: str, license_b: str,
                                combined_license: str = "") -> str:
    key = (license_a, license_b)
    if key in _COMPATIBLE:
        ok = _COMPATIBLE[key]
        if ok:
            return f"✓ {license_a} and {license_b} are compatible"
        else:
            return f"✗ {license_a} and {license_b} are NOT compatible — review obligations"
    # Try reverse
    rev_key = (license_b, license_a)
    if rev_key in _COMPATIBLE:
        ok = _COMPATIBLE[rev_key]
        if ok:
            return f"✓ {license_a} and {license_b} are compatible (reverse direction)"
        else:
            return f"✗ {license_a} and {license_b} are NOT compatible — review obligations"
    return f"? No known compatibility data for {license_a} × {license_b}"


# Example: npm package using MIT code inside an Apache-2.0 project
result = check_license_compatibility("MIT", "Apache-2.0")
print(result)
```

## Setup / Configuration

### Requirements

```txt
# core requirements
jinja2>=3.1        # template rendering for contracts
python-docx>=1.1   # .docx contract generation
weasyprint>=60     # PDF generation from HTML templates
cryptography>=41   # signature verification / document hashing
```

### Directory Structure

```
legal-assistant/
├── templates/          # Contract and notice templates (Jinja2)
│   ├── nda.j2
│   ├── services-agreement.j2
│   ├── dmca-notice.j2
│   └── privacy-policy.j2
├── checks/             # Compliance checklists
│   ├── gdpr.yaml
│   ├── dmca.yaml
│   └── licensing.yaml
├── output/             # Generated documents
└── config.yaml         # Jurisdiction defaults, company info
```

### Configuration

Create `config.yaml` with your base settings:

```yaml
# config.yaml
company:
  name: "Your Company"
  jurisdiction: "ID"            # ISO country code for default governing law
  registered_address: ""
  tax_id: ""

compliance:
  gdpr_representative: ""       # EU representative if outside EEA
  dpo_email: ""                 # Data Protection Officer contact
  dmca_agent_name: ""           # Registered DMCA agent name
  dmca_agent_email: ""          # DMCA agent email for filings

templates:
  default_language: "en"
  signature_lines: 2
  include_recitals: true
```

## Common Issues / Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| Template variable not rendered | Missing key in data dict | Run `jinja2.Environment undefined=DebugUndefined` to surface missing keys |
| GDPR compliance gap detected | No DPA with subprocessors | Sign DPA with all cloud providers (AWS, Stripe, etc.) before processing begins |
| DMCA notice rejected by platform | Missing required fields per 17 U.S.C. § 512(c)(3) | Verify all 6 elements: work ID, infringing URL, contact, good faith, accuracy, signature |
| Contract signature line mismatch | Template configured for N signatures but only M parties exist | Set `signature_lines` to match number of parties in config |
| WeasyPrint PDF rendering fails | Missing system dependency (libpango, cairo) | Install: `apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0` |
| Document version confusion | No version tracking on templates | Add `version` field to YAML frontmatter of each template file |
| Cross-border data transfer not covered | Standard clauses missing for EU→non-EU transfers | Add Standard Contractual Clauses (SCCs) or Binding Corporate Rules (BCRs) to DPA |
| Open source license incompatibility | Mixing GPL-2.0 code with Apache-2.0 project | Check compatibility matrix before adding dependencies; use LGPL or dual-license alternatives |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Document Template Marketplace | 2-4 weeks | Sell jurisdiction-specific contract templates (NDAs, SaaS terms, privacy policies) on Gumroad or GitHub Marketplace. Price per template: $29-$99. |
| Compliance-as-a-Service | 1-3 months | Monthly subscription for GDPR/DMCA compliance monitoring. Includes quarterly review of privacy policies, data mapping updates, and breach notification templates. $200-$500/mo per client. |
| Contract Review Automation | 2-6 weeks | Fixed-price engagement to audit existing contracts, build automated review checklists, and train team on template usage. $1,000-$5,000 per engagement. |
| IP Protection Audit | 2-4 weeks | Audit client's IP portfolio — trademarks, copyrights, patents, trade secrets. Deliver actionable protection roadmap and registration checklist. $2,000-$8,000 per audit. |
| DMCA Takedown Agency | Ongoing | Handle DMCA takedown notices for content creators and SaaS platforms. Per-takedown fee ($50-$200) or monthly retainer ($500-$2,000). |
| Employment Law Compliance Pack | 1-3 weeks | Package of employment contracts, independent contractor agreements, and HR policy templates customized for Indonesian labor law (UU Cipta Kerja). $500-$2,000 per client. |

