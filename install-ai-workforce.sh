#!/bin/bash
# One-Person AI Company - Skills & MCP Installation Script
# Run this to complete your AI workforce setup

set -e

echo "🤖 Setting up your AI Company Workforce..."

# ============================================
# PART 1: Install External Skills from skills.sh
# ============================================
echo ""
echo "📦 Installing skills.sh ecosystem..."

# Browser automation
npx skills add vercel-labs/agent-browser --skill agent-browser 2>/dev/null || true
npx skills add browser-use/browser-use --skill browser-use 2>/dev/null || true

# Marketing skills
npx skills add coreyhaines31/marketingskills --skill copywriting 2>/dev/null || true
npx skills add coreyhaines31/marketingskills --skill content-strategy 2>/dev/null || true
npx skills add coreyhaines31/marketingskills --skill social-content 2>/dev/null || true
npx skills add coreyhaines31/marketingskills --skill seo-audit 2>/dev/null || true
npx skills add coreyhaines31/marketingskills --skill analytics-tracking 2>/dev/null || true
npx skills add coreyhaines31/marketingskills --skill competitor-alternatives 2>/dev/null || true

# Skill discovery
npx skills add vercel-labs/skills --skill find-skills 2>/dev/null || true

echo "✅ Skills installation complete!"

# ============================================
# PART 2: Install MCP Servers (Optional)
# ============================================
echo ""
echo "🔌 Installing MCP servers..."

# Browser automation
npx -y @anthropic/playwright server &
npx -y browser-use &

# Web scraping
npx -y @anthropic/firecrawl &

# Development
npx -y @anthropic/github &

# Wait for background processes
wait

echo "✅ MCP servers initiated!"

# ============================================
# PART 3: Environment Setup
# ============================================
echo ""
echo "⚙️  Setting up environment..."

# Create env file if it doesn't exist
mkdir -p ~/.ai-company
cat > ~/.ai-company/env << 'EOF'
# Add your API keys below:
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
BROWSER_USE_API_KEY=bu-your-key-here
GITHUB_TOKEN=ghp-your-token-here
SLACK_BOT_TOKEN=xoxb-your-token-here
NOTION_API_KEY=secret-your-key-here
EOF

echo "✅ Environment file created at ~/.ai-company/env"
echo "⚠️  Please add your actual API keys to ~/.ai-company/env"

# ============================================
# PART 4: Verify Installation
# ============================================
echo ""
echo "🔍 Verifying installation..."

# Check if skills are installed
echo "Local skills in this repo:"
ls -d */ | grep -v "^\." | wc -l | xargs -I {} echo "  - {} skill directories"

# Check config files
echo ""
echo "Config files:"
[ -f SKILL_INDEX.json ] && echo "  ✅ SKILL_INDEX.json" || echo "  ❌ SKILL_INDEX.json missing"
[ -f .agentrc ] && echo "  ✅ .agentrc" || echo "  ❌ .agentrc missing"
[ -d docs ] && echo "  ✅ docs/" || echo "  ❌ docs/ missing"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your API keys to ~/.ai-company/env"
echo "2. Configure MCP servers in your AI agent config"
echo "3. Load skills: 'Load using-superpowers skill'"
echo "4. Test: 'Load content-creator skill and create a LinkedIn post'"
