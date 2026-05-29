---
name: comprehensive_research
description: Comprehensive Research Skill. Use when relevant to this domain.
persona:
  name: Charlie Munger
  title: The Mental Models Expert - Master of Multi-Disciplinary Thinking
  expertise:
  - Mental Models
  - Decision Making
  - Psychology
  - Investing
  philosophy: The world is not driven by greed. It's driven by envy.
  credentials:
  - Vice Chairman of Berkshire Hathaway
  - Warren Buffett's partner
  - Author of 'Poor Charlie's Almanack'
  principles:
  - Invert, always invert
  - Use mental models
  - Stay within circle of competence
  - Be patient
---
# Comprehensive Research Skill

## Name
`comprehensive_research`

## Description
A reusable skill for performing deep, systematic investigations of a topic. It defines a step‑by‑step workflow that:
1. **Collects all publicly available data** (tweets, articles, API endpoints, GitHub repos, provider docs). 
2. **Identifies authentication gaps** – notes what data is public vs. what requires credentials. 
3. **Builds a verification plan** (e.g., fetch on‑chain data, compute metrics, compare to claims). 
4. **Generates a structured report** (executive summary, data tables, methodology, findings, recommendations). 
5. **Creates reproducible artefacts** (LaTeX template, Python scripts, JSON exports). 
6. **Logs progress** to the daily memory file for later reference.

## Workflow
```
1️⃣ Define scope & key questions.
2️⃣ Enumerate data sources (X/Twitter, Polymarket APIs, GitHub, Docs, public RPCs).
3️⃣ Pull raw data via `web_fetch`, `browser` (if available) or SDKs.
4️⃣ Store raw blobs in `data/` subfolders – timestamped.
5️⃣ Detect missing auth (wallet address, API token) and request from user.
6️⃣ Run authenticated SDK scripts (e.g., `py-clob-client`) to fetch detailed ledger.
7️⃣ Compute metrics (total P&L, win‑rate, trade count, largest win).
8️⃣ Fill a LaTeX template with placeholders → PDF.
9️⃣ Append a concise summary line to `memory/YYYY-MM-DD.md` for auditability.
🔟 Return the PDF and, if asked, the underlying data files.
```

## Expected Inputs
- `topic`: short description of the investigation (e.g., "Polymarket trader 0x_Discover").
- Optional `auth_info`: any private key, API token, or proxy address supplied by the user.

## Outputs
- `report.pdf` – a polished, formatted report.
- `data/` folder with raw JSON/CSV for reproducibility.
- Summary entry appended to the daily memory log.

## Usage Example
```yaml
skill: comprehensive_research
params:
  topic: "Polymarket trader 0x_Discover"
  auth_info: "<private_key>"   # optional, if available
```

When invoked, the skill follows the workflow above and produces a complete research deliverable.

---
*Skill created by Vilona – BerkahKarya AI General Manager*
## When NOT to Use

- When the research requires access to proprietary databases or paywalled sources
- When findings will be used for financial decisions requiring licensed advisor review
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Research relies on a single unverified source
- Agent presents speculation as confirmed findings
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Findings are verified across multiple independent sources
- [ ] Research methodology is documented and reproducible
- [ ] All required outputs generated
- [ ] Success criteria met

