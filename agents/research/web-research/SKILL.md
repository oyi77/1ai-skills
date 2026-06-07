---
name: web-research
description: Web Research Agent. Use when relevant to this domain.
---
# Web Research Agent

Autonomous web research agent that gathers information from online sources, validates claims against primary sources, and produces structured findings. Unlike a simple search, this agent follows a systematic methodology to separate fact from fiction.

## When to Use

- Researching a library, API, or framework before adopting it
- Comparing competing tools or services
- Finding solutions to technical problems
- Investigating a company, product, or market trend
- Gathering documentation for unfamiliar services
- Fact-checking claims about performance, features, or pricing
- Finding migration guides or upgrade paths

## When NOT to Use

- Researching internal codebase (use `code-research`)
- Analyzing market conditions (use `market-research-agent`)
- Implementing solutions (use `code-agent`)
- Reviewing code (use `review-agent`)
- Information is in official documentation (just read it)
- Task requires real-time data (use monitoring tools)
- Research would take longer than trying a solution
- You need expert opinion, not web search results

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. Query Formulation

Good research starts with good questions. Before searching, define:

```markdown
## Research Brief
- **Core question**: [One specific question to answer]
- **Sub-questions**: [2-5 supporting questions]
- **Constraints**: [Time period, geography, technology version]
- **Output format**: [Summary | Comparison | Recommendation | Fact check]
- **Sources to prioritize**: [Official docs, GitHub, StackOverflow, blogs]
```

**Query strategy (run 3-5 variations):**
```
Query 1: [exact topic] documentation         # Official docs
Query 2: [topic] vs [alternative] comparison  # Competitive
Query 3: [topic] known issues limitations     # Reality check
Query 4: [topic] best practices 2025 2026     # Current state
Query 5: site:github.com [topic] migration    # Migration/changelog
```

### 2. Source Classification

Not all sources are equal. Classify before trusting:

| Tier | Source Type | Trust Level | When to Use |
|------|-----------|------------|-------------|
| **T1** | Official docs, source code, API reference | Highest | Always primary reference |
| **T1** | Published specs (RFC, W3C, IEEE) | Highest | Standards compliance |
| **T2** | Stack Overflow (accepted, high-voted) | High (verify) | Practical solutions |
| **T2** | Technical blogs by maintainers/contributors | High | Implementation context |
| **T2** | Conference talks by project authors | High | Design rationale |
| **T3** | General blog posts | Medium (cross-reference) | Alternative perspectives |
| **T3** | Reddit/HN discussions | Medium-low | Community sentiment, use cases |
| **T4** | Marketing content, sponsored posts | Low | Claims only (verify everything) |
| **T4** | AI-generated summaries | Low | Never primary source |

### 3. Documentation Research Protocol

For library/framework research:

```markdown
## Documentation Research Template

Ready-to-use templates for common scenarios.

### 1. Official Docs
- **URL**: [link]
- **Version covered**: [version]
- **Key findings**:
  - [Feature/capability]
  - [Configuration/usage]
  - [Known limitations stated in docs]

### 2. Source Code (if open source)
- **Repository**: [GitHub URL]
- **Stars**: [count] (rough proxy for adoption)
- **Last commit**: [date] (project alive?)
- **Open issues**: [count] (known problems?)
- **Recent releases**: [versions + dates]
- **Notable findings from source**:
  - [Actual implementation vs documented behavior]
  - [Undocumented features or flags]

### 3. Community Evidence
- **Stack Overflow**: [question count, common problems]
- **GitHub Issues**: [common themes in open issues]
- **Blog posts**: [practitioner experiences]
- **Migration guides**: [breaking changes, upgrade paths]

### 4. Competitive Alternatives
| Alternative | Stars | Last Update | Key Difference |
|-------------|-------|-------------|----------------|
| [alt1] | X | date | [what it does differently] |
| [alt2] | X | date | [what it does differently] |
```

### 4. Fact-Checking Protocol

Never trust a single claim. Verify:

```markdown
## Fact Check Template

Ready-to-use templates for common scenarios.

### Claim: "[specific claim]"
- **Source 1**: [URL] -- [supports / contradicts / partial]
- **Source 2**: [URL] -- [supports / contradicts / partial]
- **Verification method**: [tested myself / checked docs / compared benchmarks]
- **Confidence**: HIGH (2+ primary sources agree) | MEDIUM | LOW
- **Verdict**: CONFIRMED | DEBUNKED | UNVERIFIABLE

### Common Claims to Fact-Check
- [ ] "X is faster than Y" -- Find benchmarks with methodology
- [ ] "X is deprecated" -- Check official deprecation notice
- [ ] "X does not support Y" -- Check docs and source code
- [ ] "Best practice is X" -- Check who says so and why
```

### 5. API Research

When evaluating an API:

```markdown
## API Evaluation Template

Ready-to-use templates for common scenarios.

### Basic Info
- **Provider**: [name]
- **Documentation**: [URL]
- **Pricing**: [free tier, paid tiers]
- **Rate limits**: [requests/minute, burst limits]
- **Authentication**: [API key, OAuth, etc.]

### Capabilities
- **Endpoints**: [list key endpoints]
- **Data format**: [JSON, XML, Protocol Buffers]
- **Pagination**: [cursor, offset, keyset]
- **Webhooks**: [supported events]
- **Batch operations**: [supported or not]

### Reliability
- **SLA**: [uptime guarantee]
- **Status page**: [URL]
- **Incident history**: [recent outages]
- **Support**: [channels, response times]

### Limitations
- **Known gaps**: [what it does NOT do]
- **Breaking changes**: [recent or upcoming]
- **Data freshness**: [real-time, near-real-time, batch]
```

### 6. Competitive Analysis

```markdown
## Comparison Matrix
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Core feature | HIGH | Full | Partial | Full |
| Performance | HIGH | 10ms avg | 50ms avg | 15ms avg |
| Ease of use | MEDIUM | Complex | Simple | Moderate |
| Community | MEDIUM | 50K stars | 10K stars | 30K stars |
| Pricing | MEDIUM | Free | $99/mo | Free tier |
| Documentation | HIGH | Excellent | Good | Fair |
| Active development | HIGH | Weekly | Monthly | Daily |

### Scoring
- Option A: [weighted score] -- [recommendation]
- Option B: [weighted score] -- [recommendation]
- Option C: [weighted score] -- [recommendation]
```

## Tool Usage Patterns

Efficient patterns for using research tools.


### Structured Search Queries
```bash
# Official documentation
site:docs.python.org "async context manager"

# GitHub issues (common problems)
site:github.com/owner/repo/issues "error" "timeout"

# Recent discussions (current state)
"library-name" performance benchmark 2026

# Migration information
"library-name" migration guide v2 to v3

# Stack Overflow solutions
site:stackoverflow.com "library-name" "how to" [error message]
```

### API Testing
```bash
# Quick API capability test
curl -s "https://api.example.com/v1/status" | jq .

# Check rate limits
curl -sI "https://api.example.com/v1/resource" | grep -i "x-rate\|x-limit\|retry"

# Test authentication
curl -s -H "Authorization: Bearer $TOKEN" "https://api.example.com/v1/me" | jq .
```

## Output Format

```markdown
## Web Research Report

Key aspects of web-research relevant to this section.


### Question
[Original research question]

### Answer (3-5 sentences)
[Direct answer with confidence level]

### Key Findings
1. [Finding] -- Source: [T1/T2/T3], Confidence: [HIGH/MED/LOW]
2. [Finding] -- Source: [T1/T2/T3], Confidence: [HIGH/MED/LOW]
3. [Finding] -- Source: [T1/T2/T3], Confidence: [HIGH/MED/LOW]

### Comparison Matrix (if applicable)
| Criteria | Option A | Option B |
|----------|----------|----------|
| ... | ... | ... |

### Recommendation
[Actionable recommendation based on evidence]

### Caveats and Gaps
- [What could not be verified]
- [Information that may be stale]
- [Conflicting sources]

### Sources
| Source | Tier | URL | Date |
|--------|------|-----|------|
| [name] | T1 | [url] | [date] |
| [name] | T2 | [url] | [date] |
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The first Google result is good enough" | SEO optimizes for clicks, not accuracy. The best answer is often on page 2 or behind a specific site: search. |
| "I already know this, no need to verify" | Knowledge expires. APIs change, libraries deprecate, pricing shifts. Verify current state before acting. |
| "Blog posts are not reliable" | Blog posts by practitioners contain real-world experience that docs do not cover. Use T2 blogs as secondary sources. |
| "Official docs are always correct" | Docs describe intent, not reality. Check source code and issues for the truth. |
| "One good source is enough" | Single-source findings have >40% error rate. Cross-reference minimum 2 independent sources. |
| "Stack Overflow is outdated" | Accepted answers from 2020 may still be correct for v2. Check the version context and whether the answer applies to your version. |

## Red Flags

- Citing a source without checking its date (stale information presented as current)
- Relying on a single source for a factual claim
- Confusing marketing claims with technical documentation
- Not checking version compatibility (using v3 docs for v2 project)
- Treating Reddit/forum opinions as facts
- Ignoring official deprecation notices in favor of "it still works"
- Not verifying benchmark methodology (who ran it, what hardware, what config)
- Copying code examples without understanding them

## Verification

After web research, confirm:

- [ ] Core question answered with evidence (not speculation)
- [ ] Minimum 2 independent sources for each factual claim
- [ ] Source tiers assigned (T1/T2/T3/T4) for transparency
- [ ] Staleness checked (dates on all cited sources)
- [ ] Conflicting information documented (not hidden)
- [ ] Comparison criteria are relevant to the actual decision
- [ ] Recommendation is actionable (specific next steps)
- [ ] Caveats and unknowns explicitly listed
- [ ] All sources cited with URLs
- [ ] No [TODO] or placeholder content in the report
