# 1ai-skills-bundle

Install all 80+ 1ai-skills with a single command. AI workforce for one-person companies.

## Overview

1ai-skills-bundle is a meta-package that provides instant access to 80+ specialized AI skills across multiple domains including development, marketing, trading, operations, and productivity. Install once and have all skills available to your AI agents.

## Supported Platforms

- **NPM**: `@1ai/1ai-skills-bundle`
- **PyPI**: `1ai-skills-bundle`

## Installation

### NPM (Node.js)

```bash
# Global install
npm install -g @1ai/1ai-skills-bundle

# Or as a project dependency
npm install @1ai/1ai-skills-bundle
```

### PyPI (Python)

```bash
# Install via pip
pip install 1ai-skills-bundle

# Or with specific version
pip install 1ai-skills-bundle==1.0.0
```

## What's Included

The bundle includes 80+ skills across these categories:

| Category | Skills Count |
|----------|-------------|
| Planning | 3 |
| Development | 13 |
| Marketing & Sales | 20+ |
| Content | 6 |
| Research | 4 |
| Operations | 7 |
| Productivity | 6 |
| Trading | 7+ |
| Orchestration | 5 |

### Key Skills

- **Planning**: brainstorming, writing-plans, executing-plans
- **Development**: test-driven-development, systematic-debugging, subagent-driven-development, finishing-a-development-branch, using-git-worktrees
- **Marketing**: copywriting, content-strategy, email-sequence, social-content, seo-audit, analytics-tracking, paid-ads, launch-strategy
- **Trading**: trading, trading-researcher, trading-strategist, trading-risk-manager, trading-executor, trading-team
- **Productivity**: google-canvas, google-workspace, email-automation, calendar-management
- **Content**: humanizer, humanizer-zh, writing-skills, gemini-image-generator, content-creator

See `skill-index.json` for the complete list.

## Agent Platform Integration

### OpenCode

```bash
# Skills are installed to your OpenCode skills directory
# After install, skills are auto-discovered

# Verify installation
npm run verify
```

### Claude Code

```bash
# Install to Claude Code skills directory
claude install paijo/1ai-skills-bundle
```

### OpenCraw

```bash
# Skills are available in the OpenCraw workspace
cd ~/.openclaw/workspace/skills
npm install @1ai/1ai-skills-bundle
```

## Usage

After installation, skills are automatically available to your AI agents. Simply reference them by name:

```
Use the trading skills to analyze XAUUSD market conditions.
Use the copywriting skill to write landing page copy.
Use systematic-debugging to fix this bug.
```

## Command Line Tools

### NPM

```bash
# List all installed skills
npm run list-skills

# Verify installation
npm run verify
```

### Python

```bash
# List all skills
python -m 1ai_skills_bundle list
```

## Directory Structure

```
1ai-skills-bundle/
├── package.json          # NPM package config
├── setup.py              # PyPI package config
├── MANIFEST.in           # Package files manifest
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── install-skills.js     # NPM postinstall script
├── list-skills.js        # Skill listing script
├── verify-install.js     # Installation verification
├── install.py            # Python install helper
└── skill-index.json     # Complete skill index
```

## Development

### Local Development

```bash
# Clone the repository
git clone https://github.com/paijo/1ai-skills.git
cd 1ai-skills/1ai-skills-bundle

# Install for local development
npm install
# or
pip install -e .
```

### Publishing to NPM

```bash
npm login
npm publish --access public
```

### Publishing to PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

## Troubleshooting

### Skills not appearing

1. Verify installation completed successfully:
   ```bash
   npm run verify
   # or
   python -m 1ai_skills_bundle verify
   ```

2. Check skill directory exists:
   - OpenCode: `~/.opencode/skills/`
   - Claude Code: `~/.claude/skills/`
   - OpenCraw: `~/.openclaw/workspace/skills/`

3. Restart your AI agent session

### Permission errors

```bash
# Fix npm permissions
sudo npm install -g @1ai/1ai-skills-bundle

# Or use a node version manager
nvm use default
npm install -g @1ai/1ai-skills-bundle
```

## License

MIT License - see LICENSE file for details.

## Support

- Issues: https://github.com/paijo/1ai-skills/issues
- Documentation: https://github.com/paijo/1ai-skills#readme

## Version History

### 1.0.0 (2026-02-19)
- Initial release
- 80+ skills across all categories
- NPM and PyPI distribution support
- Automatic skill installation and verification
