# Reddit Post: r/ClaudeAI

## Title
I built the largest AI agent skill library — 1337 skills, all tested, all with anti-rationalization tables

## Body

Your AI agent says "I'll add tests later" and never does. It writes placeholder code and calls it done. It skips security because "it works on my machine."

I got tired of this, so I built [1ai-skills](https://github.com/oyi77/1ai-skills) — 1337 production-grade skills that force agents to follow real workflows.

**Every skill includes:**
- Anti-Rationalization Table (prevents the agent from cutting corners)
- Code examples (Python, JS, Bash)
- Step-by-step workflow
- Verification checklist
- When to Use / When NOT to Use

**19 categories:** Cybersecurity (786), Development (92), Content (64), Mindset (55), Marketing (45), and 14 more.

**Tested:** 8-dimension test suite, 1337/1337 pass, 0 warnings, 0 failures.

**Quick start for Claude Code:**
```
/plugin marketplace add oyi77/1ai-skills
/plugin install 1ai-skills@1ai-skills
```

Also works with Cursor, Gemini CLI, Windsurf, and any agent that reads SKILL.md files.

GitHub: https://github.com/oyi77/1ai-skills
Website: https://oyi77.is-a.dev/1ai-skills/

Would love feedback on the skill quality. Which categories need more skills?
