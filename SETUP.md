# AI Company Workforce - Setup Guide

This guide walks you through completing the remaining setup items.

## Current Status: 69/73 Complete (95%)

The following items require your action to complete - they are BLOCKED by environment-specific setup:

## User Action Required

### 1. Install MCP Servers
```bash
# Browser automation (use OpenCode's built-in Playwright)
# browser-use is available via uvx
uvx browser-use --remote

# Other MCPs - check mcpservers.org for correct package names
# The plan had incorrect package names - verify at mcpservers.org
```

### 2. Configure Environment Variables
Create `~/.ai-company/env` with your API keys:
```bash
mkdir -p ~/.ai-company
cat > ~/.ai-company/env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-xxx
BROWSER_USE_API_KEY=bu_xxx
GITHUB_TOKEN=ghp_xxx
SLACK_BOT_TOKEN=xoxb-xxx
NOTION_API_KEY=secret_xxx
EOF
```

### 3. Configure OpenCode MCP
Add to your OpenCode config (`~/.opencode/mcp.yaml`):
```yaml
mcpServers:
  playwright:
    command: npx
    args: ["-y", "@anthropic/playwright", "server"]
  browser-use:
    command: npx
    args: ["-y", "browser-use"]
```

### 4. Verify Skills Load
After setup, test with:
```
Load content-creator skill
Load self-improving-agent skill
Load google-workspace skill
```

### 5. Test Auto-Activation
Try directives like:
- "Create a LinkedIn post about AI" → activates content-creator
- "Research our competitors" → activates market-research
- "Fix this bug" → activates systematic-debugging
- "Send an email to..." → activates email-automation
- "Schedule a meeting..." → activates calendar-management

## Files Created

| File | Purpose |
|------|---------|
| README.md | Project overview |
| LLM.md | Installation guide |
| SKILL_INDEX.json | All skills metadata |
| .agentrc | Auto-activation config |
| docs/handbook.md | Company handbook |
| docs/workforce.md | Team structure |
| docs/policies.md | AI policies |
| docs/auto-activation.md | Activation guide |
| content-creator/ | Multi-platform content |
| google-canvas/ | Canvas workspace automation |
| google-workspace/ | Docs/Sheets/Slides automation |
| email-automation/ | Gmail browser automation |
| calendar-management/ | Calendar browser automation |
| customer-support/ | Support automation |
| self-improving-agent/ | Continuous learning |
| market-research/ | Intelligence gathering |
| project-management/ | Task coordination |
| analytics-reporting/ | Data & reporting |
| joko-orchestrator/ | Unified orchestration |
| revenue-team/ | Revenue orchestrator |
| operations-team/ | Operations orchestrator |
| product-team/ | Product orchestrator |
| governance-team/ | Governance orchestrator |

## Quick Start

1. Run: `chmod +x install-ai-workforce.sh && ./install-ai-workforce.sh`
2. Add API keys to `~/.ai-company/env`
3. Configure MCP servers in your AI agent
4. Test with: "Load content-creator skill"

---

*This file created to document remaining setup steps.*
