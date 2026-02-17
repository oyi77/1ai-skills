# Installation

This repository contains a collection of skills for AI agents.

---

## Agent-Specific Installation

Each AI agent has its own skills directory. Choose your agent below:

---

### For OpenCraw (OpenClaw)

**Skills Directory**: `~/.openclaw/workspace/skills/`

```bash
# Navigate to OpenCraw skills directory
cd ~/.openclaw/workspace/skills

# Clone the repository
git clone https://github.com/oyi77/1ai-skills.git

# Install dependencies
cd 1ai-skills
npm install
```

**Skill Path**: `~/.openclaw/workspace/skills/1ai-skills/`

---

### For OpenCode

**Skills Directory**: `~/.opencode/skills/` or `~/.config/opencode/skills/`

```bash
# Navigate to OpenCode skills directory
cd ~/.opencode/skills

# Or if using config directory
cd ~/.config/opencode/skills

# Clone the repository
git clone https://github.com/oyi77/1ai-skills.git

# Install dependencies
cd 1ai-skills
npm install
```

**Alternative using OpenCode CLI**:
```bash
opencode skills install oyi77/1ai-skills
```

**Skill Path**: `~/.opencode/skills/1ai-skills/` or `~/.config/opencode/skills/1ai-skills/`

---

### For Claude Code

**Skills Directory**: Claude Code uses npm packages. Install globally:

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Install skills package
claude install paijo/1ai-skills

# Or install specific skill
claude install paijo/1ai-skills --skill trading
```

**Alternative: Manual Clone**
```bash
# Claude Code may use different locations
# Check Claude settings for custom skills path

# Common locations:
cd ~/.claude/skills
# or
cd ~/.config/claude/skills

# Clone
git clone https://github.com/oyi77/1ai-skills.git
```

**Skill Path**: Varies by Claude Code version - check with `claude settings`

---

### For Other Agents (Cursor, Windsurf, etc.)

```bash
# Find your agent's skills directory
# Common locations:
# - ~/.cursor/skills
# - ~/.windsurf/skills
# - ~/.github/skills

# Clone to your agent's skills directory
cd YOUR_AGENT_SKILLS_DIR
git clone https://github.com/oyi77/1ai-skills.git
```

---

## Quick Install (All Agents)

If you're unsure which agent you're using, try this universal method:

```bash
# Try OpenCraw location first
mkdir -p ~/.openclaw/workspace/skills
cd ~/.openclaw/workspace/skills
git clone https://github.com/oyi77/1ai-skills.git
cd 1ai-skills
npm install
```

---

## Verification

After installation, verify by checking:

```bash
# Check SKILL_INDEX.json exists
ls -la 1ai-skills/SKILL_INDEX.json

# Or check trading skills
ls -la 1ai-skills/trading/
```

---

## Dependencies

Some skills require additional packages:

```bash
# Install globally for trading skills
pip install MetaTrader5    # For MT5 broker
pip install ccxt          # For crypto exchanges
pip install pandas pytz   # For data analysis
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skills not loading | Check agent's skill directory path |
| npm install fails | Use Node.js 18+ |
| Trading skills don't work | Install required Python packages |
| Path issues | Verify you're in the correct agent's skills directory |

---

## Skill Categories Available

After installation, you'll have access to:

- **Trading**: trading, trading-researcher, trading-strategist, trading-risk-manager, trading-executor, trading-team, xauusd-asia-7c-breakout
- **Planning**: brainstorming, writing-plans, executing-plans
- **Development**: test-driven-development, systematic-debugging, subagent-driven-development
- **Marketing**: marketing, sales, seo-audit, competitor-alternatives
- **Content**: humanizer, writing-skills, content-creator
- **Research**: mckinsey-research, polymarket-analyst
- **Operations**: customer-support, project-management
- **Productivity**: google-workspace, email-automation
- **And 70+ more skills...**
