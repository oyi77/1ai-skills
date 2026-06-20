---
name: kyc-screener
description: Parses onboarding docs, runs rules engine, flags compliance gaps. Use when user says "KYC check", "onboard client",
  "screen company".
domain: financial
tags:
- analysis
- compliance
- finance
- investment
- kyc
- screener
---

# KYC Screener

## Persona:

**Compliance Officer** — Inspired by the `kyc-screener` agent from anthropics/financial-services. Masters document parsing, rules engines, and risk flagging.

**Core Philosophy:** Every onboarding is a risk decision. The-quality of your KYC determines whether you're building a quality book or a regulatory nightmare.

## Overview:

Parses onboarding documents, runs compliance rules engine, and flags gaps. Handles the full KYC workflow: ingest → parse → screen → flag → report.

## When to Use

- New client onboarding (PE/Venture/Wealth Management)
- Annual KYC refresh required
- Suspicious activity flagged mid-relationship
- M&A due diligence on target companies)
- Regulatory audit preparation)

## When NOT to Use:

- Earnings analysis (use `financial/earnings-viewer`)
- Pitch deck creation (use `financial/pitch-deck`)
- Trading strategy (use `trading/alphaear-strategy`)

## Implementation:


The implementation follows a phased approach: ingest onboarding documents, run compliance rules engine, flag risk ratings, and generate KYC reports.


### Phase 1: Document Ingestion

**Supported Formats:**
```python
document_types = {
    "identity": ["passport", "drivers_license", "national_id"],
    "financial": ["bank_statement", "tax_return", "payslip"],
    "corporate": ["articles_of_incorporation", "board_resolution"],
    "pe": ["cap_table", "investment_agreement", "subscription_agreement"]
}
```

**Parsing Pipeline:**
```python
parsed_data = {
    "entity_name": extract_entity_name(doc),
    "registration": verify_registration_number(doc),
    "directors": extract_directors(doc),
    "beneficial_owners": identify_ubo(doc),  # >25% ownership
    "sanctions_check": run_sanctions_screening(entity),
    "pep_status": check_pep_lists(entity)  # Politically Exposed Person
}
```

### Phase 2: Rules Engine

**Compliance Rules Grid:**
```python
rules = {
    "ubos_identified": {"threshold": "all >25%", "action": "flag"},
    "sanctions_hit": {"list": ["OFAC", "EU", "UN"], "action": "block"},
    "pep_exposure": {"position": ["ceo", "cfo"], "action": "escalate"},
    "document_age": {"max_days": 90, "action": "reject"},
    "address_mismatch": {"sources": 3, "action": "investigate"}
}
```

### Phase 3: Risk Flagging

**Red/Amber/Green Rating:**
```python
risk_assessment = {
    "overall_risk": calculate_composite_risk(parsed_data, rules),
    "red_flags": [
        {"rule": "sanctions_hit", "detail": " Entity on OFAC list"},
        {"rule": "missing_ubo", "detail": "3 owners >25% not documented"}
    ],
    "amber_flags": [
        {"rule": "document_age", "detail": "Tax return > 12 months old"}
    ],
    "green_flags": [
        {"rule": "audited_fs", "detail": "Big 4 audited last 2 years"}
    ]
}
```

### Phase 4: Report Generation

**Output Format:**
```markdown
# KYC Report: [Entity Name]

## Overall Risk Rating: 🔴 RED / 🟡 AMBER / ✅ GREEN


Composite risk rating based on sanctions hits, UBO completeness, PEP status, and document freshness.


## Entity Details
- Name: [Entity]
- Jurisdiction: [Country]
- Registration: [Number, Verified ✅/❌]

## UBOs (>25% Ownership)
| Name | Ownership % | Status |
|------|--------------|--------|
| [Name] | 35% | Sanctions check ✅ |

## Red Flags
1. [Flag detail] — **Action Required**
2. [Flag detail] — **Action Required**

## Amber Flags
1. [Flag detail] — **Monitor**

## Compliance Actions
- [ ] Sanctions cleared (OFAC, EU, UN)
- [ ] All UBOs documented with proof
- [ ] PEP screening completed
- [ ] Documents < 90 days old
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Small client, skip deep KYC" | Small clients = higher fraud risk % |
| "Documents are old, but trustworthy" | >90 days = stale, re-fresh required |
| "UBO not relevant for this jurisdiction" | UBO rules are global AML standard |
| "Sanctions check takes too long" | Automated APIs respond < 2 seconds |
| "PEP doesn't apply here" | PEP applies to all senior political positions |

## Red Flags

- Sanctions hit but proceeding anyway
- UBOs incomplete (>25% unaccounted)
- Documents > 90 days old
- PEP status ignored
- Revenue > $5M but no beneficial ownership
- Approving with active red flags

## Verification

After completing KYC screening, confirm:

- [ ] All documents parsed: entity name, registration, directors verified
- [ ] UBOs: all >25% owners identified with proof
- [ ] Sanctions screening: OFAC, EU, UN lists checked
- [ ] PEP status checked for senior positions
- [ ] Document age: all < 90 days (or flagged amber)
- [ ] Risk rating assigned: Red/Amber/Green with rationale
- [ ] Compliance report generated with action items
- [ ] Regulatory audit trail: all decisions logged

## Integration Points:

**Cross-Skill References:**
- `financial/pitch-deck` — For PE onboarding (cap table review)
- `trading/black-edge` — For adverse media screening
- `operations/finance-ops` — For financial statement verification
- `references/trading-checklist.md` — For risk management validation

**MCP Server Integrations:**
- World-Check MCP — For sanctions & PEP screening
- Refinitiv MCP — For adverse media checks
- Company House MCP — For UK entity verification

Load `references/trading-checklist.md` for complete trading checklists.

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).
