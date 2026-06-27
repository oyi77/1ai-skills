# Reddit Post: r/ChatGPTCoding

## Title
Stop your AI agent from being lazy — 1337 tested skills with anti-rationalization tables

## Body

Every AI coding agent has the same bad habits:
- "I'll add tests later" (never does)
- "This placeholder works fine" (it doesn't)
- "Security is a nice-to-have" (until you get breached)

I built [1ai-skills](https://github.com/oyi77/1ai-skills) to fix this. It's a library of 1337 SKILL.md files that force agents to follow real workflows.

The key feature: **Anti-Rationalization Tables**. Every skill has a table like:

```
| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. |
| "I will refactor later" | Technical debt compounds. |
| "It works on my machine" | If it is not in CI, it does not work. |
```

When your agent loads a skill, it sees this table and cannot use those excuses.

**What's included:**
- 1337 skills across 19 categories
- Every skill has code examples, workflows, and verification checklists
- 8-dimension test suite, 100% pass rate
- Works with Claude Code, Cursor, Gemini CLI, Windsurf

**Categories:** Cybersecurity (786), Development (92), Content (64), Mindset (55), Marketing (45), and 14 more.

Install for Claude Code:
```
/plugin marketplace add oyi77/1ai-skills
/plugin install 1ai-skills@1ai-skills
```

GitHub: https://github.com/oyi77/1ai-skills

Feedback welcome. What skills are you missing?
