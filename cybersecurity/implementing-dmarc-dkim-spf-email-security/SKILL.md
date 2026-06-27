---
name: implementing-dmarc-dkim-spf-email-security
description: SPF, DKIM, and DMARC form the three pillars of email authentication. Together they prevent domain spoofing, validate
  message integrity, and define policies for handling unauthenticated mail. Proper im
domain: cybersecurity
subdomain: phishing-defense
tags:
- phishing
- email-security
- social-engineering
- dmarc
- awareness
- dkim
- spf
- dns
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.AT-01
- DE.CM-09
- RS.CO-02
- DE.AE-02
---
# Implementing DMARC, DKIM, and SPF Email Security

## Overview
SPF, DKIM, and DMARC form the three pillars of email authentication. Together they prevent domain spoofing, validate message integrity, and define policies for handling unauthenticated mail. Proper implementation drastically reduces phishing attacks that impersonate your organization's domain.


## When to Use

- When deploying or configuring implementing dmarc dkim spf email security capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites
- DNS management access for your domain
- Access to email server/MTA configuration (Postfix, Exchange, Google Workspace, Microsoft 365)
- Basic understanding of DNS TXT records
- Python 3.8+ for validation scripts

## Key Concepts

This section covers key concepts for implementing dmarc dkim spf email security.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### SPF (Sender Policy Framework)
Publishes a DNS TXT record listing authorized IP addresses and mail servers that can send email on behalf of your domain. Receiving servers check the envelope sender's IP against this list.

### DKIM (DomainKeys Identified Mail)
Adds a cryptographic signature to outgoing emails using a private key. The corresponding public key is published in DNS. Receivers verify the signature to ensure the message was not altered in transit.

### DMARC (Domain-based Message Authentication, Reporting and Conformance)
Builds on SPF and DKIM by specifying a policy (none/quarantine/reject) for messages that fail authentication, and provides a reporting mechanism to monitor spoofing attempts.

## Workflow

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Audit Current State
```bash
# Check existing SPF record
dig TXT example.com | grep spf

# Check existing DKIM selector
dig TXT selector1._domainkey.example.com

# Check existing DMARC record
dig TXT _dmarc.example.com
```

### Step 2: Implement SPF
```
# DNS TXT record for example.com
v=spf1 ip4:203.0.113.0/24 include:_spf.google.com include:spf.protection.outlook.com -all
```

Key SPF mechanisms:
- `ip4:` / `ip6:` - Authorize specific IP ranges
- `include:` - Include another domain's SPF record
- `a` - Authorize domain's A record IPs
- `mx` - Authorize domain's MX record IPs
- `-all` - Hard fail all others (recommended)
- `~all` - Soft fail (monitoring phase)

### Step 3: Implement DKIM
```bash
# Generate DKIM key pair (2048-bit RSA)
openssl genrsa -out dkim_private.pem 2048
openssl rsa -in dkim_private.pem -pubout -out dkim_public.pem

# Format public key for DNS (remove headers, join lines)
grep -v "PUBLIC KEY" dkim_public.pem | tr -d '\n'
```

DNS TXT record at `selector1._domainkey.example.com`:
```
v=DKIM1; k=rsa; p=MIIBIjANBgkqhki...
```

### Step 4: Implement DMARC
```
# DNS TXT record at _dmarc.example.com
# Phase 1 (Monitor):
v=DMARC1; p=none; rua=mailto:dmarc-aggregate@example.com; ruf=mailto:dmarc-forensic@example.com; pct=100

# Phase 2 (Quarantine):
v=DMARC1; p=quarantine; rua=mailto:dmarc-aggregate@example.com; pct=25

# Phase 3 (Reject):
v=DMARC1; p=reject; rua=mailto:dmarc-aggregate@example.com; pct=100
```

### Step 5: Monitor and Analyze DMARC Reports
Use the `scripts/process.py` to parse DMARC aggregate XML reports and identify authentication failures, unauthorized senders, and spoofing attempts.

## When NOT to Use

- You need to test the implementation (use performing-* skills)
- Task is about configuring existing tools (use configuring-* skills)
- You need to analyze security events (use analyzing-* skills)
- Task is about building detection rules (use building-* skills)
- You don't have access to the target environment
- Task requires vendor-specific expertise (consult vendor docs)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Sharing sensitive findings or credentials in unencrypted communications
- Failing to properly scope and contain the assessment before starting

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## Tools & Resources
- **MXToolbox**: https://mxtoolbox.com/SuperTool.aspx
- **DMARC Analyzer (dmarcian)**: https://dmarcian.com/
- **Google Postmaster Tools**: https://postmaster.google.com/
- **Valimail DMARC Monitor**: https://www.valimail.com/
- **DMARC Report Analyzer**: https://dmarc.postmarkapp.com/

## Validation
- SPF record passes validation at mxtoolbox.com
- DKIM signature verified on test emails
- DMARC record properly formatted and reporting enabled
- Test emails pass all three checks in recipient's Authentication-Results header

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |