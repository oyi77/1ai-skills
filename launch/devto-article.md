# Dev.to Article

## Title
How I Built and Tested 1337 AI Agent Skills (And Why Anti-Rationalization Tables Matter)

## Tags
ai, agents, claude, opensource, productivity

## Body

Every AI coding agent has the same bad habits. It says "I'll add tests later" and never does. It writes placeholder code and calls it done. It skips security because "it works on my machine."

I got tired of fighting my agent, so I built [1ai-skills](https://github.com/oyi77/1ai-skills) — the largest open-source AI agent skill library with 1337 production-grade skills across 19 categories.

## The Problem: AI Agents Are Lazy

AI coding agents are powerful, but they have a fundamental problem: they optimize for speed, not quality. They will:

- Skip writing tests because "the code looks correct"
- Ignore security because "it's not in scope"
- Write placeholder content and call it done
- Use generic patterns instead of domain-specific best practices

This is not a model problem — it's a context problem. Agents don't have enough structured context to make good decisions.

## The Solution: Anti-Rationalization Tables

Every skill in 1ai-skills includes an **Anti-Rationalization Table** — a structured argument that prevents the agent from cutting corners:

```markdown
| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |
```

When your agent loads a skill, it sees this table and cannot use those excuses. It's not just a prompt — it's a structured argument that the agent must address.

## What Every Skill Has

Every one of the 1337 skills includes:

1. **YAML frontmatter** — Machine-readable metadata (name, description, domain, tags)
2. **Anti-Rationalization Table** — Prevents agents from cutting corners
3. **Code Examples** — Concrete, runnable code (Python, JS, Bash, SQL)
4. **Workflow** — Step-by-step instructions with bold labels
5. **When to Use** — 3+ trigger conditions
6. **When NOT to Use** — 2+ contraindications
7. **Verification Checklist** — Success criteria you can check

## 19 Categories

| Category | Skills | Focus |
|---|---|---|
| Cybersecurity | 786 | Threat hunting, forensics, pen testing, SOC ops |
| Development | 92 | TDD, debugging, code review, engineering workflows |
| Content | 64 | Video, audio, design, writing, document generation |
| Mindset | 55 | Negotiation, leadership, critical thinking |
| Marketing | 45 | SEO, viral content, email, ads, growth |
| Core | 44 | AI infrastructure, memory, model routing |
| Integrations | 36 | GitHub, Discord, Notion, Slack, Stripe |
| DevOps | 33 | Docker, Kubernetes, CI/CD, cloud ops |
| Automation | 28 | Bots, workflows, scrapers |
| Research | 23 | Deep research, market analysis |
| Trading | 20 | Crypto, DeFi, Polymarket |
| Operations | 19 | Business ops, governance, HR |
| Agents | 16 | AI agent orchestration |
| MCP | 14 | Model Context Protocol servers |
| Meta | 13 | Self-evolving meta-skills |
| Financial | 15 | Finance analysis, valuation |
| Sales | 14 | Lead generation, CRM |
| Data | 10 | Data pipelines, analysis |
| Productivity | 10 | Calendars, email, meetings |

## Testing: 8 Dimensions

I built a comprehensive test suite that validates every skill across 8 dimensions:

1. **Structure** — YAML frontmatter, required fields
2. **Content** — Sections present, no placeholders, depth score
3. **Code Syntax** — Python `ast.parse`, JS/TS, Bash
4. **Internal Links** — All `/skills/` links resolve
5. **Description Quality** — 50-200 chars, action-oriented
6. **Quality Markers** — Anti-rationalization, code examples, verification
7. **SDK Availability** — Referenced imports are installable
8. **Workflow Completeness** — Has workflow section

**Result: 1337/1337 PASS · 0 warnings · 0 failures**

```bash
python3 scripts/test-skills.py           # Full test
python3 scripts/test-skills.py --quick   # Skip SDK checks
python3 scripts/test-skills.py --json    # JSON output
```

## How It Works

Skills are SKILL.md files with YAML frontmatter. When your agent loads a skill, it reads the full content and follows the workflow:

```yaml
---
name: detecting-lateral-movement-with-splunk
description: Detect adversary lateral movement across networks using Splunk SPL queries.
domain: cybersecurity
tags:
- threat-hunting
- splunk
- lateral-movement
---
```

The agent sees the anti-rationalization table, the workflow, the code examples, and the verification checklist. It cannot skip steps because the skill explicitly tells it what to do and what NOT to do.

## Compatibility

Works with:
- Claude Code (recommended)
- Cursor
- Gemini CLI / Antigravity
- Windsurf
- OpenCode
- GitHub Copilot
- Kiro
- Any agent that reads SKILL.md files

## Complementary to addyosmani/agent-skills

[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (67K stars) provides 24 engineering lifecycle commands (/spec, /build, /test). 1ai-skills provides 1337 domain-specific knowledge skills. Use both.

His skills tell your agent HOW to build (the SDLC). My skills tell your agent WHAT to build (domain expertise).

## Try It

```bash
# Claude Code
/plugin marketplace add oyi77/1ai-skills
/plugin install 1ai-skills@1ai-skills

# Cursor
git clone https://github.com/oyi77/1ai-skills.git
cp -r 1ai-skills/cybersecurity/* .cursor/rules/

# Gemini CLI
gemini skills install https://github.com/oyi77/1ai-skills.git --path skills
```

## What's Next

- Adding more product-specific skills (AWS, GCP, Azure)
- Improving depth of existing skills
- Building a skill recommendation engine
- Community contributions welcome

GitHub: https://github.com/oyi77/1ai-skills
Website: https://oyi77.is-a.dev/1ai-skills/

---

*If this helps your agent stop being lazy, star the repo. It helps more developers find it.*
