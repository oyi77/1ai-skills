---
name: social-engineer
description: Social engineering and phishing for authorized security assessments. Use when testing human attack vectors, conducting phishing simulations, or assessing organizational security awareness.
---

# Social Engineer

The weakest link is always human. This skill covers authorized social engineering assessments — phishing, pretexting, physical access testing. Only use with explicit written authorization.

## When to Use

- Authorized phishing simulations
- Social engineering assessments
- Security awareness training
- Physical security testing
- Pretexting for authorized penetration tests

**WARNING**: Social engineering without authorization is illegal. Always have written authorization before testing.

## The Process

### 1. Reconnaissance

#### Target Research
```
# OSINT on organization
- LinkedIn: employees, roles, technologies used
- Twitter/X: company culture, events, announcements
- GitHub: leaked credentials, internal URLs
- Job postings: technology stack, internal tools
- News: recent events, acquisitions, layoffs
- Corporate website: org chart, contact info

# OSINT on individuals
- Social media profiles
- Public records
- Professional publications
- Conference presentations
- Personal interests and hobbies
```

#### Attack Vector Identification
```
# Email patterns
- firstname.lastname@company.com
- firstinitial.lastname@company.com
- firstname@company.com

# Common services
- Email provider (Google Workspace, Microsoft 365)
- Collaboration tools (Slack, Teams, Discord)
- Cloud services (AWS, Azure, GCP)
- VPN and remote access
- SSO providers
```

### 2. Phishing Campaigns

#### Email Phishing
```
# Pretext types
- IT support: "Your password expires today"
- HR: "Updated benefits enrollment required"
- Finance: "Invoice attached - payment due"
- Executive: "Urgent: Review this document"
- Delivery: "Package delivery notification"
- Security: "Suspicious activity detected"

# Technical elements
- Sender spoofing (lookalike domains)
- HTML emails with tracking pixels
- Credential harvesting pages
- Malicious attachments (with authorization)
- Link shorteners for tracking
```

#### Spear Phishing
```
# Personalized attacks
- Reference real company events
- Use actual employee names
- Mention real projects/initiatives
- Timing around known events (mergers, conferences)
- Impersonate trusted vendors/partners
```

#### SMS Phishing (Smishing)
```
# Text message attacks
- "Your package is delayed: [link]"
- "Your account is locked: [link]"
- "Security alert: [link]"
- "Your verification code is: [code]"
```

#### Voice Phishing (Vishing)
```
# Phone call attacks
- IT support pretext
- Vendor impersonation
- Executive impersonation
- Technical support scam
- Survey/research pretext
```

### 3. Pretexting Scenarios

#### Common Pretexts
```
# IT Support
"I'm from IT and we need to verify your credentials for the
system upgrade. Can you confirm your username and password?"

# New Employee
"Hi, I'm starting next week and IT told me to contact you
about getting access set up. Can you help me with the VPN?"

# Vendor/Partner
"I'm calling from [vendor] and we need to verify your account
for our annual security audit. Can you confirm your details?"

# Executive
"This is [CEO name] and I need you to wire $50,000 to this
account immediately. Don't tell anyone, it's confidential."
```

### 4. Physical Social Engineering

#### Tailgating
```
# Following authorized person through secure door
- Carry boxes/props to look busy
- Time with shift changes
- Use distraction techniques
- Badge cloning if possible
```

#### Impersonation
```
# Dress the part
- Vendor uniform/ID
- Delivery person
- IT technician
- Maintenance worker
- New employee

# Props
- Clipboard with forms
- Tool bag
- Lanyard with fake badge
- Laptop bag
- Stack of boxes
```

#### Physical Access Testing
```
# What to test
- Reception desk procedures
- Badge access controls
- Visitor management
- Secure area access
- Clean desk policy
- Document disposal
- Screen locking
```

### 5. Credential Harvesting

#### Fake Login Pages
```
# Clone target login page
# Host on lookalike domain
# Track submitted credentials
# Redirect to real site after capture

# Tools: Gophish, King Phisher, SET
```

#### Evil Twin WiFi
```
# Create rogue access point
# Mimic legitimate SSID
# Capture credentials via captive portal
# SSL strip if possible

# Tools: Wifiphisher, Fluxion
```

### 6. Reporting

#### Phishing Simulation Report
```
# Metrics to track
- Emails sent vs delivered
- Links clicked
- Credentials submitted
- Reports to security team
- Time to first click
- Click rate by department

# Recommendations
- Training needs by department
- Policy improvements
- Technical controls
- Awareness program improvements
```

## Red Flags

- Testing without written authorization
- Collecting real credentials (simulate, don't capture)
- Causing actual harm or disruption
- Targeting individuals outside scope
- Using fear/intimidation tactics
- Not following agreed-upon rules of engagement
- Testing during sensitive business periods

## Verification

- Written authorization obtained before testing
- Scope and rules clearly defined
- No real credentials collected
- All phishing infrastructure cleaned up after test
- Report includes metrics and recommendations
- Debrief conducted with target organization
- Lessons learned documented

## Tools

| Purpose | Tools |
|---------|-------|
| Phishing | Gophish, King Phisher, SET |
| OSINT | Maltego, theHarvester, Recon-ng |
| Email | GoPhish, PhishMe |
| Physical | Lockpick set, badge cloner |
| WiFi | Wifiphisher, Fluxion |
| Reporting | Custom dashboards, metrics tools |

## Legal Considerations

```
# Always obtain written authorization
# Define scope and limitations
# Do not collect real credentials
# Do not cause actual harm
# Follow responsible disclosure
# Comply with local laws (CFAA, GDPR, etc.)
# Document everything for legal protection
```

## Revenue Potential

Social engineering assessments pay well:
- Phishing simulation: $2000-$10000
- Full social engineering assessment: $5000-$25000
- Physical security testing: $3000-$15000
- Security awareness training: $1000-$5000 per session
- Red team engagement (includes SE): $10000-$50000
