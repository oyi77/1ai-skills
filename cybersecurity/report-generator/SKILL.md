---
name: report-generator
description: Generate professional security vulnerability reports for bug bounty platforms. Use when documenting security
  findings, preparing bug bounty submissions, or creating assessment reports.
domain: cybersecurity
tags:
- cybersecurity
- generator
- report
- security
- threat-defense
---

# Report Generator Skill

## Overview

Impact-first report generation for bug bounty platforms and security assessments. Generates submission-ready reports with clear reproduction steps, proof-of-concept code, and remediation guidance. Supports multiple platform formats (HackerOne, Bugcrowd, Intigriti, Immunefi) with consistent quality standards. Every claim requires evidence, every severity rating requires CVSS calculation.

## When to Use

**Trigger phrases:**
- "report generator"
- "After validating a security finding and confirming it is not a false positive"
- "Preparing bug bounty submissions for any platform"
- "Creating penetration test reports for clients"


- After validating a security finding and confirming it is not a false positive
- Preparing bug bounty submissions for any platform
- Creating penetration test reports for clients
- Documenting security assessment results
- Generating executive summaries for non-technical stakeholders
- Converting raw findings into structured, professional deliverables

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Finding Summary

- Write a clear, descriptive title (e.g., "Stored XSS in user profile bio field allows account takeover")
- Calculate severity using CVSS v3.1 vector string (do not guess -- use the calculator)
- Identify the affected asset/endpoint precisely (full URL, parameter, component)
- Classify vulnerability type using CWE ID (e.g., CWE-79 for XSS)

### Step 2: Impact Analysis

- Assess business impact: what data is at risk, what operations can be disrupted
- Describe realistic attack scenarios an adversary would use
- Estimate affected user population (all users, admin only, specific role)
- Quantify potential financial/reputational damage where possible
- Compare against the program's disclosed impact expectations

### Step 3: Reproduction Steps

Write numbered, reproducible steps that anyone can follow from scratch:

```
1. Navigate to https://target.com/login
2. Log in with test credentials (user@test.com / Password123)
3. Navigate to https://target.com/settings/profile
4. In the "Bio" field, enter: <script>alert(document.domain)</script>
5. Click "Save Changes"
6. Navigate to https://target.com/profile/user@test.com
7. Observe: JavaScript alert fires showing the domain
```

Each step must include: exact URLs, HTTP requests (curl/fetch), screenshots, browser console output, or network traffic captures. Every step must be actionable and verifiable by a triager with no prior context.

### Step 4: Proof of Concept

- Provide working exploit code or demonstration
- Keep it non-destructive (no data exfiltration, no denial of service)
- Clearly show the vulnerability in action
- Include cleanup steps if the PoC modifies any state
- Use code blocks with syntax highlighting

```python
# PoC: Stored XSS via profile bio (non-destructive)
import requests
SESSION_TOKEN = "your_session_cookie"
resp = requests.post("https://target.com/api/v1/profile",
    headers={"Cookie": f"session={SESSION_TOKEN}"},
    json={"bio": '<img src=x onerror=alert(document.domain)>'})
print(f"Status: {resp.status_code}")
# Visit https://target.com/profile/testuser to trigger
```

### Step 5: Remediation

- Provide specific fix recommendations with code examples
- Reference OWASP guidelines and CWE mappings
- Prioritize recommendations by effort vs. impact
- Include both immediate mitigations and long-term fixes

```
**Immediate**: Sanitize input with whitelist-based HTML sanitizer.
**Long-term**: Implement Content-Security-Policy headers.
**Reference**: CWE-79, OWASP XSS Prevention Cheat Sheet
```

### Step 6: Platform Formatting

Adapt the report for the target platform:

**HackerOne**: Title, Severity, Weakness (CWE), Summary, Steps To Reproduce, Impact, Supporting Material (attachments)

**Bugcrowd**: Title, Description, Steps to Reproduce, Impact, Remediation

**Intigriti**: Title, Type, Severity, Description, Steps, Impact, Fix

**Immunefi**: Title, Severity, Target, Vulnerability Type, Impact, Proof of Concept, Fix (focus on smart contract / DeFi specifics when applicable)

## 7-Question Validation Gate

Every report must pass all seven checks before submission:

1. **Is the vulnerability real?** -- Not a false positive, not a known behavior, not informational-only
2. **Is it exploitable?** -- Works in a realistic attack scenario, not just theoretical
3. **What is the actual impact?** -- Concrete harm to the business and its users, not hypothetical
4. **Is the asset in-scope?** -- Verified against the program's scope and bounty table
5. **Can it be reproduced?** -- A stranger can follow your steps and get the same result
6. **Is the severity correct?** -- CVSS v3.1 score calculated, not guessed; matches program guidelines
7. **Is the PoC clean?** -- Non-destructive, clearly demonstrates the issue, includes cleanup if needed

If any answer is "no" or "unclear", do not submit. Fix the gap first.

## Report Formats

| Format  | Use Case                          | Notes                              |
|---------|-----------------------------------|------------------------------------|
| Markdown| Default, platform submissions     | Portable, easy to edit             |
| HTML    | Client deliverables               | Syntax highlighting for code       |
| PDF     | Formal submissions, compliance    | Use for executive summaries        |

## Quality Standards

- No vague terms: never write "might", "could potentially", "possibly" -- state facts with evidence
- Every impact claim must include proof (screenshot, log, output)
- CVSS score must be calculated with a vector string, not estimated
- Reproduction steps must work on a fresh session with no prior state
- Code examples must be syntactically correct and runnable

## Common Mistakes

- Overstating impact without evidence (triagers will downgrade or close)
- Missing screenshots for visual bugs or UI-based vulnerabilities
- Unclear reproduction steps that assume prior knowledge
- Wrong severity rating (using CVSS incorrectly or guessing)
- Not including remediation guidance
- Including destructive payloads in PoC (never exfiltrate real data)
- Submitting duplicates without searching for existing reports first

## Report Templates

**HackerOne**: Summary (what/where/impact) -> Steps to Reproduce (numbered) -> Impact (evidence) -> Supporting Material (attachments)

**Bugcrowd**: Description (vuln + location) -> Steps to Reproduce (numbered) -> Impact (attacker capability) -> Remediation (fix with code)

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Vague impact claims without evidence
- Non-reproducible steps (triagers cannot verify)
- Missing proof of concept entirely
- Copy-pasting generic vulnerability descriptions
- Overstating severity to inflate bounty
- Including destructive payloads in PoC
- Not including cleanup steps when PoC modifies state
- Submitting to out-of-scope assets
- Ignoring program-specific rules and safe harbor terms

## Verification

Before marking a report as submission-ready, confirm:

- [ ] All reproduction steps work from a clean state
- [ ] Impact is clearly articulated with supporting evidence
- [ ] CVSS severity rating is calculated with full vector string
- [ ] Format matches the target platform's requirements
- [ ] Proof of concept is non-destructive and demonstrates the issue
- [ ] Remediation guidance is specific and actionable
- [ ] Report passes the 7-question validation gate
- [ ] No typos, broken links, or missing screenshots

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