---
name: writeup-cash
description: Monetize bug bounty findings through writeups, tools, and consulting. Use when turning security research into
  income streams, writing paid writeups, or building a security brand.
domain: cybersecurity
author: oyi77
license: Apache-2.0
subdomain: general-cybersecurity
tags:
- cash
- cybersecurity
- money
- security
- threat-defense
- writeup
version: 1.0.0
---

# Writeup Cash

## Overview

Cybersecurity skill for writeup cash. Follows industry best practices and security standards.
Turn your bug bounty findings, vulnerability research, and security tooling into multiple income
streams: paid writeups on platforms like PentesterLand and Infosec Writeups, commercial security
tools sold on GitHub Marketplace or Gumroad, and consulting upsells to organizations that read
your published research.

## Money-Making Overview

**Buyer personas:** Bug bounty hunters with validated findings but no monetization pipeline;
penetration testers who want to build a public brand; security researchers sitting on unpublished
tooling.

**Three revenue tiers:**

| Tier | Product | Price Range | Time to First Dollar |
|------|---------|-------------|---------------------|
| Writeups | Published technical writeups on paid platforms (PentesterLand, InfoSec Writeups, personal blog with ad/affiliate revenue) | $100-$1,000 / writeup | 2-7 days |
| Tools | CLI tools, PoC scripts, BurpSuite extensions, automation frameworks | $500-$5,000 / tool | 7-30 days |
| Consulting | Brand-driven security consulting, code review, pentest subcontracting | $2,000-$10,000 / engagement | 30-90 days |

**Stacking path:** Publish 1 writeup/week on paid platforms → bundle 3-5 related PoCs into a
$497 tool → use published work as portfolio to land $5K retainer clients.

## When to Use

**Trigger phrases:**
- "writeup cash"
- "Have accepted bug bounty reports to share"
- "Want to build passive income from security research"
- "Building a personal brand in security"


- Have accepted bug bounty reports to share
- Want to build passive income from security research
- Building a personal brand in security
- Creating content for paid platforms
- Developing and selling security tools


## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope
- When the finding is already publicly documented by someone else (commoditized)
- When the vulnerability disclosure agreement prohibits publication (always verify NDAs/VDP terms first)

## Prerequisites

- Access to relevant log sources and security tools
- Understanding of cash fundamentals
- Appropriate permissions for data access and tool operation
- A validated, non-disclosed vulnerability finding (CVE, bug bounty report, or pentest finding)
- A publisher account on at least one paid platform (Medium Partner Program, PentesterLand, or self-hosted blog with Stripe)

## First Action in 60 Minutes

Run this script to convert a raw finding into a publishable writeup:

```python
#!/usr/bin/env python3
"""writeupify.py — Turn a bug bounty finding into a publication-ready writeup."""
import sys, json, datetime, re

TEMPLATE = """---
title: "{title}"
published: {published}
date: {date}
tags: [{tags_str}]
canonical_url: ""
seo_keywords: [{seo_str}]
---

# {title}

**Vulnerability Type:** {vuln_type}
**Target:** {target}
**Severity:** {severity} (CVSS: {cvss})
**Reported:** {reported_date}
**Bounty:** ${bounty}

## TL;DR

{tldr}

## Background

{background}

## Reproduction Steps

1. {step1}
2. {step2}
3. {step3}

## Impact

{impact}

## Remediation

{remediation}

## Timeline

- **Discovery:** {disc_date}
- **Reported:** {rep_date}
- **Triaged:** {tri_date}
- **Bounty Paid:** {pay_date}
- **Disclosure:** {disc_date}

## References

- {ref1}
- {ref2}
"""

def prompt_finding():
    print("=== Writeupify — Interactive Finding to Writeup ===", file=sys.stderr)
    fields = {}
    prompts = [
        ("title", "Title"),
        ("vuln_type", "Vulnerability Type (e.g. SQLi, XSS, IDOR)"),
        ("target", "Target Application / Program"),
        ("severity", "Severity (Critical/High/Medium/Low)"),
        ("cvss", "CVSS Score (e.g. 7.5)"),
        ("bounty", "Bounty Amount (USD)"),
        ("tldr", "TL;DR (one-sentence summary)"),
        ("background", "Background (2-3 sentences on the component)"),
        ("step1", "Step 1 of reproduction"),
        ("step2", "Step 2 of reproduction"),
        ("step3", "Step 3 of reproduction"),
        ("impact", "Impact description"),
        ("remediation", "Remediation recommendation"),
        ("disc_date", "Discovery date (YYYY-MM-DD)"),
        ("rep_date", "Report date (YYYY-MM-DD)"),
        ("tri_date", "Triage date (YYYY-MM-DD)"),
        ("pay_date", "Bounty paid date (YYYY-MM-DD)"),
        ("pub_date", "Publication date (YYYY-MM-DD)"),
        ("ref1", "Reference URL 1"),
        ("ref2", "Reference URL 2"),
    ]
    for key, prompt_text in prompts:
        val = input(f"  {prompt_text}: ").strip() if sys.stdin.isatty() else ""
        fields[key] = val or "TBD"

    fields["tags_str"] = ", ".join([fields["vuln_type"], fields["severity"], "bug-bounty", "writeup", "infosec"])
    fields["seo_str"] = ", ".join([
        f"{fields['vuln_type']} writeup",
        f"bug bounty {fields['vuln_type']}",
        fields["target"],
        "how to find " + fields["vuln_type"],
        f"{fields['severity']} vulnerability example",
    ])
    fields["date"] = fields.get("pub_date", datetime.date.today().isoformat())
    fields["published"] = "false"
    return fields

if __name__ == "__main__":
    page = prompt_finding()
    t = TEMPLATE.format(**page)
    slug = re.sub(r"[^a-z0-9]+", "-", page["title"].lower()).strip("-")
    path = f"writeups/{slug}.md"
    with open(path, "w") as f:
        f.write(t)
    print(f"[+] Wrote {path} ({len(t)} bytes)")
    print(f"[+] SEO keywords: {page['seo_str']}")
    print(f"[+] Tags: {page['tags_str']}")
    print(f"[+] Next: edit {path}, set published: true, and post to Medium/PentesterLand")
```

**Usage:**
```bash
python3 writeupify.py
# fills interactively, outputs writeups/<title-slug>.md
```

## Deliverable Format

Use this writeup template as your invoice-ready deliverable for paid platforms. Publish on
Medium (Partner Program), PentesterLand, or your own blog with Substack/Stripe:

**File: `writeups/TEMPLATE_WRITEUP.md`**

```markdown
---
title: "Vulnerability Title — {VulnType} in {Target}"
published: false
date: YYYY-MM-DD
tags: [vuln-type, bug-bounty, writeup, infosec, poc]
canonical_url: ""
seo_keywords: ["vuln type writeup", "bug bounty vuln type", "target", "how to find vuln type", "severity vulnerability example"]
---

# Vulnerability Title — {VulnType} in {Target}

**Vulnerability Type:** SQL Injection / XSS / IDOR / SSRF / etc.
**Target:** program.tld / app-name
**Severity:** Critical / High / Medium / Low (CVSS: X.X)
**Bounty:** $500

## TL;DR

One sentence capturing the root cause and business impact.

## Background

- What is the target? What does it do?
- Where is the vulnerable component located?
- Why is it interesting from a security perspective?

## Discovery Methodology

1. **Recon phase:** what endpoints/scopes were enumerated
2. **Testing approach:** tools used, payloads crafted, manual vs automated
3. **Trigger:** exact request/parameter that exposed the bug

## Reproduction Steps (with Evidence)

**Step 1:** Authenticate / navigate to the vulnerable page.

```
REQUEST: GET /api/users?id=1 HTTP/1.1
Host: target.com
Cookie: session=...
```

**Step 2:** Inject the attack payload.

```
REQUEST: GET /api/users?id=1' UNION SELECT ... --
```

**Step 3:** Observe the response.

```
RESPONSE 200:
{"id":1,"email":"admin@target.com","password_hash":"..."}
```

**Screenshot:** [POC.png](link-to-evidence)

## Impact

- Data exposed / accounts compromised / RCE achieved
- CVSS vector string and score
- Real-world damage scenario

## Remediation

- Specific fix: parameterized queries / input validation / access control check
- Code snippet showing the patch
- Defense-in-depth recommendations

## Timeline

| Date | Event |
|------|-------|
| YYYY-MM-DD | Discovery |
| YYYY-MM-DD | Reported to vendor |
| YYYY-MM-DD | Triaged / acknowledged |
| YYYY-MM-DD | Fix confirmed |
| YYYY-MM-DD | Bounty paid ($X) |
| YYYY-MM-DD | Public disclosure |

## References

- CVE-YYYY-NNNN (if applicable)
- OWASP page for this vulnerability class
- Related H1/Intigriti reports

## Tools Used

- Burp Suite / Caido / ZAP
- Custom script (link to GitHub)
- Nuclei template (link)

---

**Want this finding checked by a professional?** I offer code review and pentest services.
Email: researcher@example.com / Twitter: @handle
```

**SEO checklist for each publish:**
- [ ] `title` contains primary keyword + target name
- [ ] `seo_keywords` has 5 terms matching actual search queries
- [ ] First 200 characters include the vulnerability type and target
- [ ] `canonical_url` points to your primary domain
- [ ] Post includes at least 3 internal links to other writeups
- [ ] Social preview image (screenshot of POC) attached

**Monetization checklist:**
- [ ] Posted on Medium with Partner Program enabled
- [ ] Cross-posted to PentesterLand (paid per view)
- [ ] Shared on Twitter with "writeup" and "bug bounty" hashtags
- [ ] PoC script extracted and listed on Gumroad / GitHub Marketplace ($29-$97)
- [ ] CTA at bottom: "Need a deep-dive audit? DM me for consulting rates"

## Process

1. **Prepare** — Verify finding is publishable (non-confidential, novel or well-demonstrated)
2. **Write** — Run `writeupify.py`, fill template, add screenshots and request/response pairs
3. **SEO** — Optimize title, keywords, description, canonical URL for search discovery
4. **Publish** — Post to paid platform (Medium Partner Program, PentesterLand, self-hosted with ads)
5. **Promote** — Tweet the writeup, post on Reddit r/netsec, cross-post on dev.to
6. **Monetize** — Offer consulting, bundle PoC into a tool, create a video walkthrough for YouTube

## Verification

- [ ] Written finding is non-confidential and legally publishable
- [ ] Writeup includes reproduction steps with request/response evidence
- [ ] SEO metadata populated; canonical URL set
- [ ] PoC script ready for standalone sale
- [ ] Cross-published on at least 2 platforms
- [ ] CTA for consulting / tool sales included in footer

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "My finding is too small for a paid writeup." | Every writeup builds your portfolio. A $100 writeup today leads to a $5K client tomorrow. Publish anyway. |
| "Someone else already wrote about this bug class." | Your specific target, methodology, and payload variations are unique. Nobody has your exact writeup. |
| "I don't have time to write polished content." | The writeupify script generates a publishable draft in 10 minutes. Polish adds 30 min. That's <1 hour for $100-500. |
| "I'll give away my competitive edge by publishing PoCs." | Public PoCs establish expertise, attract clients, and signal to programs that you understand disclosure. The edge is your brain, not one payload. |
| "Tool sales are passive income — just build it once." | Tools require documentation, support, updates for new versions, and marketing. Budget 5h/week per tool for maintenance and sales. |
| "Consulting clients will find me through my writeups automatically." | Passive discoverability is low. You must add a CTA, tweet every writeup, and DM program managers. No CTA = no leads. |
