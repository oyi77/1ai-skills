---
name: bounty-target-finder
description: Find and prioritize high-paying bug bounty programs. Use when discovering
  new targets, comparing bounty payouts, filtering programs by scope, or building
  a target pipeline for continuous hunting.
domain: cybersecurity
---

# Bounty Target Finder

Finds the highest-value bug bounty programs and builds a prioritized target pipeline. The difference between earning $0 and $10k/month is often just target selection.

## When to Use

- Starting a new bug bounty hunting cycle
- Looking for fresh targets with less competition
- Comparing payouts across platforms
- Building a continuous hunting pipeline
- Finding programs that match your skill set

## The Process

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### 1. Platform Aggregation

Pull programs from all major platforms:

| Platform | URL | Strengths |
|----------|-----|-----------|
| **HackerOne** | hackerone.com/directory | Largest, most transparent payouts |
| **Bugcrowd** | bugcrowd.com/programs | Good enterprise programs |
| **Intigriti** | intigriti.com | EU-focused, growing fast |
| **Immunefi** | immunefi.com | Web3/crypto, highest payouts ($100k+) |
| **YesWeHack** | yeswehack.com | EU/Asia, good for mobile |
| **HackenProof** | hackenproof.com | Crypto-focused |

### 2. Target Filtering Criteria

Rank programs by **money per effort**:

```
Score = (avg_payout × scope_size) / (competition × program_age)
```

**High-Value Signals:**
- Bounties > $500 for low/medium severity
- Bounties > $5000 for critical
- Wide scope (all *.target.com, not just specific endpoints)
- New programs (< 3 months old) — less competition
- Recently expanded scope — new attack surface, few hunters on it
- Web3 programs — $10k-$1M payouts for critical smart contract bugs
- "No known issues" programs — fresh, untested surface

**Low-Value Signals (avoid):**
- Capped bounties with tiny maximums (< $100)
- Narrow scope (single endpoint)
- "Informational" only payouts
- Programs with many public reports (surface already hammered)
- Programs that close reports as "informative" or "N/A" frequently

### 3. Target Research Pipeline

For each candidate target:

1. **Tech stack detection** — What frameworks, languages, cloud providers?
2. **Scope enumeration** — What's in scope? What's explicitly out?
3. **Historical reports** — What bugs have been found before? What patterns?
4. **Asset inventory** — Subdomains, APIs, mobile apps, acquisitions
5. **Competition analysis** — How many hunters? How active?

### 4. Continuous Monitoring

Set up watchers for:
- New program launches (platform RSS/APIs)
- Scope expansions on existing programs
- Program policy changes (new asset types, higher payouts)
- Public disclosures (learn from others' findings)
- M&A activity (acquired companies = new attack surface)

### 5. Target Portfolio Strategy

Don't put all eggs in one basket:

| Category | Count | Focus |
|----------|-------|-------|
| **Primary targets** | 2-3 | Deep focus, know them inside-out |
| **Secondary targets** | 5-10 | Periodic scans, catch low-hanging fruit |
| **Opportunistic** | 20+ | Automated monitoring, instant triage |

## Quick Money Patterns

These consistently pay well with moderate skill:

1. **IDOR on new programs** — Automated scanner + manual validation = $500-$5000 each
2. **Subdomain takeover** — Automated discovery = $250-$2000 each
3. **Exposed .git/.env** — Automated scanning = $250-$1000 each
4. **Missing rate limits** — Auth endpoints, password reset = $500-$2000
5. **CORS misconfiguration** — Automated check = $250-$1500
6. **Open redirect → OAuth** — Chain for account takeover = $1000-$5000
7. **Web3 reentrancy** — Smart contract bugs = $10,000-$100,000+
8. **GraphQL introspection** — Information disclosure → chain to IDOR = $500-$3000

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Testing programs you haven't verified are active
- Ignoring program rules (testing out-of-scope assets)
- Spending too long on low-payout programs
- Not checking if a finding has already been reported (duplicate = $0)
- Hunting on programs with bad payout history

## Verification

- Target list has at least 10 active programs
- Each target has documented scope, tech stack, and payout history
- Portfolio balances high-value deep targets with broad automated coverage
- Monitoring alerts configured for new programs and scope changes
- Historical payout data analyzed before committing time

## Automation

```bash
# Pull new programs from HackerOne
curl -s "https://api.hackerone.com/v1/hackers/programs?page[size]=100" | jq '.data[] | {name: .attributes.name, bounty: .attributes.offers_bounties, state: .attributes.state}'

# Filter for bounty programs with wide scope
# Check scope, parse for *.domain.com patterns, rank by breadth

# Monitor for scope changes
# diff previous scope snapshot with current
```
