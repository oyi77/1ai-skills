---
name: oh-my-opencode-installation
description: Smart installation and configuration for OpenCode with oh-my-opencode harness - detects existing installation
  and only installs if needed
domain: integrations
tags:
- api
- installation
- integrations
- opencode
- third-party
---

# Oh My OpenCode Installation

## Overview

This skill provides intelligent installation and configuration guidance for OpenCode and the oh-my-opencode harness. **It first detects what's already installed and only proceeds with installation if needed.**

## When to Use

- **First-time setup** – When OpenCode and oh-my-opencode need to be installed from scratch
- **Reinstall/upgrade** – When reinstalling or updating oh-my-opencode to latest version
- **Migration** – When moving OpenCode configuration to new machine or environment
- **Troubleshooting** – When installation issues need to be diagnosed and resolved
- **Automated setup** – When scripting OpenCode and oh-my-opencode installation for CI/CD
- **Mixed environments** – When OpenCode is installed but oh-my-opencode is not, or vice versa

## Detection First
This section covers detection first for the oh-my-opencode-installation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Step 1: Detect Existing Installation

**Check if OpenCode is installed**:
```bash
# Check OpenCode installation
if command -v opencode &> /dev/null; then
    OPENCODE_VERSION=$(opencode --version 2>/dev/null || echo "unknown")
    echo "✓ OpenCode is already installed: $OPENCODE_VERSION"
    OPENCODE_INSTALLED=true
else
    echo "✗ OpenCode is not installed"
    OPENCODE_INSTALLED=false
fi
```

**Check if oh-my-opencode is installed**:
```bash
# Check oh-my-opencode installation
if command -v oh-my-opencode &> /dev/null; then
    OMO_VERSION=$(oh-my-opencode --version 2>/dev/null || echo "unknown")
    echo "✓ oh-my-opencode is already installed: $OMO_VERSION"
    OMO_INSTALLED=true
elif npm list -g oh-my-opencode &> /dev/null; then
    OMO_VERSION=$(npm list -g oh-my-opencode --depth=0 2>/dev/null | grep oh-my-opencode || echo "installed")
    echo "✓ oh-my-opencode npm package is installed"
    OMO_INSTALLED=true
else
    echo "✗ oh-my-opencode is not installed"
    OMO_INSTALLED=false
fi
```

**Check Node.js version**:
```bash
# Verify Node.js requirements
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo "✓ Node.js version: $NODE_VERSION (meets requirement)"
    else
        echo "✗ Node.js version: $NODE_VERSION (need 18+)"
    fi
else
    echo "✗ Node.js is not installed"
fi
```

### Step 2: Conditional Installation

**Only install if detected as missing**:

```bash
# Installation decision tree
if [ "$OPENCODE_INSTALLED" = true ] && [ "$OMO_INSTALLED" = true ]; then
    echo "✓ Both OpenCode and oh-my-opencode are installed. Skipping installation."
    echo "Run 'opencode' to start or 'oh-my-opencode --help' for options."
elif [ "$OPENCODE_INSTALLED" = true ]; then
    echo "→ OpenCode is installed. Installing oh-my-opencode only..."
    install_oh_my_opencode
elif [ "$OMO_INSTALLED" = true ]; then
    echo "→ oh-my-opencode is installed. Installing OpenCode only..."
    install_opencode
else
    echo "→ Neither is installed. Installing both..."
    install_opencode
    install_oh_my_opencode
fi
```

## Prerequisites
This section covers prerequisites for the oh-my-opencode-installation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### System Requirements
- **Platform**: macOS, Linux, Windows (WSL recommended)
- **Terminal**: WezTerm, Alacritty, Ghostty, or Kitty
- **Node.js**: Version 18+ (required for oh-my-opencode)
- **API Keys**: For LLM providers you want to use

### Recommended Setup
- **Terminal**: WezTerm (cross-platform, excellent performance)
- **Shell**: zsh or bash with oh-my-zsh
- **Git**: Latest version with proper configuration

## Installation Functions
This section covers installation functions for the oh-my-opencode-installation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### install_opencode()

```bash
install_opencode() {
    echo "Installing OpenCode..."

    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install anomalyco/tap/opencode
        else
            curl -fsSL https://opencode.ai/install | bash
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v pacman &> /dev/null; then
            sudo pacman -S opencode
        elif command -v apt &> /dev/null; then
            curl -fsSL https://opencode.ai/install | bash
        else
            curl -fsSL https://opencode.ai/install | bash
        fi
    else
        # Windows or other
        curl -fsSL https://opencode.ai/install | bash
    fi

    # Verify installation
    if command -v opencode &> /dev/null; then
        echo "✓ OpenCode installed successfully: $(opencode --version)"
    else
        echo "✗ OpenCode installation failed"
        return 1
    fi
}
```

### install_oh_my_opencode()

```bash
install_oh_my_opencode() {
    echo "Installing oh-my-opencode..."

    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "✗ Node.js is required but not installed. Please install Node.js 18+ first."
        return 1
    fi

    # Check Node.js version
    NODE_MAJOR=$(node --version | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -lt 18 ]; then
        echo "✗ Node.js 18+ is required. Current version: $(node --version)"
        return 1
    fi

    # Check if npm is available
    if ! command -v npm &> /dev/null; then
        echo "✗ npm is required but not installed."
        return 1
    fi

    # Install via npm
    echo "Installing oh-my-opencode via npm..."
    npm install -g oh-my-opencode

    # Verify installation
    if command -v oh-my-opencode &> /dev/null; then
        echo "✓ oh-my-opencode installed successfully: $(oh-my-opencode --version)"
    else
        echo "✗ oh-my-opencode installation failed"
        return 1
    fi
}
```

### full_installation()

```bash
full_installation() {
    echo "========================================="
    echo "Oh My OpenCode Smart Installation"
    echo "========================================="

    # Detection phase
    echo ""
    echo "Phase 1: Detection"
    echo "------------------"
    detect_installation

    # Installation phase
    echo ""
    echo "Phase 2: Installation"
    echo "---------------------"
    install_if_needed

    # Configuration phase
    echo ""
    echo "Phase 3: Configuration"
    echo "----------------------"
    configure_installation

    # Verification phase
    echo ""
    echo "Phase 4: Verification"
    echo "---------------------"
    verify_installation

    echo ""
    echo "========================================="
    echo "Installation Complete!"
    echo "========================================="
}
```

## Installation Methods
This section covers installation methods for the oh-my-opencode-installation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Method 1: Quick Install (Recommended)

For humans:
```bash
# Detection + Installation in one command
curl -fsSL https://opencode.ai/install | bash

# Then install oh-my-opencode
npm install -g oh-my-opencode
```

### Method 2: Node.js Installation

```bash
# npm
npm install -g opencode-ai oh-my-opencode

# Bun
bun install -g opencode-ai oh-my-opencode

# pnpm
pnpm install -g opencode-ai oh-my-opencode
```

### Method 3: Homebrew (macOS)

```bash
brew install anomalyco/tap/opencode
npm install -g oh-my-opencode
```

### Method 4: For LLM Agents

```bash
# Detection + Installation
bash -c "$(curl -fsSL https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.sh)"
```

## Configuration
```json
{
  "enabled": true,
  "autoRun": false,
  "timeout": 30000,
  "retries": 3
}
```

Set environment variables as needed for authentication and endpoints.


### Initial Setup After Installation

1. **Verify installation worked**:
   ```bash
   opencode --version
   oh-my-opencode --version
   ```

2. **Initialize a project**:
   ```bash
   cd /path/to/project
   opencode
   /init
   ```

3. **Configure LLM provider**:
   ```bash
   /connect
   ```

4. **Configure oh-my-opencode**:
   ```bash
   oh-my-opencode install
   ```

### Config File Locations

| Level | Location |
|-------|----------|
| Project | `.opencode/opencode.jsonc` |
| User | `~/.config/opencode/opencode.jsonc` |
| oh-my-opencode Project | `.opencode/oh-my-opencode.jsonc` |
| oh-my-opencode User | `~/.config/opencode/oh-my-opencode.jsonc` |

### Basic Configuration

```jsonc
{
  "plugin": ["oh-my-opencode"],
  "model": {
    "main": "openai/gpt-4o",
    "fallback": ["anthropic/claude-3-5-sonnet-20241022"]
  }
}
```

## Verification
This section covers verification for the oh-my-opencode-installation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Quick Verification Checklist

```bash
# 1. Check versions
opencode --version && echo "✓ OpenCode OK"
oh-my-opencode --version && echo "✓ oh-my-opencode OK"

# 2. Test OpenCode starts
opencode --help > /dev/null 2>&1 && echo "✓ OpenCode CLI OK"

# 3. Check config exists
[ -f ~/.config/opencode/opencode.json ] && echo "✓ Config OK"

# 4. Verify Node.js (for oh-my-opencode)
node --version && echo "✓ Node.js OK"
npm --version && echo "✓ npm OK"
```

### Test Basic Functionality

```bash
# Start OpenCode and run basic commands
opencode --eval "/help"

# Check agent availability
opencode --eval "/status"
```

## Integration with OpenClaw
- Connects with existing toolchain via standard interfaces
- Supports webhook-based event notifications
- Compatible with CI/CD pipelines for automated workflows
- Provides structured output for downstream consumption


### For OpenClaw Integration

```bash
# 1. Verify OpenCode is in PATH
which opencode && echo "✓ OpenCode in PATH"

# 2. Configure OpenClaw
mkdir -p ~/.config/opencode

# 3. Copy oh-my-opencode config
cat > ~/.config/opencode/oh-my-opencode.jsonc << 'EOF'
{
  "agents": {
    "sisyphus": { "model": "openai/gpt-4o" },
    "hephaestus": { "model": "openai/gpt-4o" },
    "oracle": { "model": "anthropic/claude-3-5-sonnet-20241022" }
  }
}
EOF

# 4. Load oh-my-opencode skill in OpenClaw
echo "✓ OpenClaw integration configured"
```

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |


### Detection Issues

**"Command not found" after installation**:
```bash
# Reload shell
exec $SHELL

# Or add to PATH manually
export PATH="/usr/local/bin:$PATH"

# Verify installation
ls -la /usr/local/bin/opencode
ls -la /usr/local/bin/oh-my-opencode
```

**Wrong version detected**:
```bash
# Check exact installation
which -a opencode
which -a oh-my-opencode

# Check npm global
npm list -g --depth=0
```

### Installation Issues

**npm install fails**:
```bash
# Clear npm cache
npm cache clean --force

# Check npm permissions
npm config get prefix

# Fix permissions if needed
sudo chown -R $(whoami) ~/.npm
```

**Permission denied**:
```bash
# Use sudo for system-wide install
sudo npm install -g oh-my-opencode

# Or use nvm for local installation
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
npm install -g oh-my-opencode
```

### Configuration Issues

**Config not loading**:
```bash
# Check config syntax
cat ~/.config/opencode/opencode.jsonc | python3 -m json.tool > /dev/null && echo "✓ Config valid"

# Check config location
ls -la ~/.config/opencode/

# View config errors
opencode --debug config
```

## Security Considerations
This section covers security considerations for the oh-my-opencode-installation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Safe Installation

- ✓ Download from official sources only
- ✓ Verify checksums when available
- ✓ Review installation scripts
- ✓ Use environment variables for API keys
- ✓ Set restrictive file permissions (600 for configs)

### Security Checks

```bash
# Verify download source
echo "Checking installation sources..."

# OpenCode
[ "$(curl -sI https://opencode.ai/install | head -1)" =~ "200" ] && echo "✓ OpenCode source OK"

# oh-my-opencode npm package
npm view oh-my-opencode version && echo "✓ npm package verified"
```

## Post-Installation Checklist

- [ ] OpenCode installed and `opencode --version` works
- [ ] oh-my-opencode installed and `oh-my-opencode --version` works
- [ ] Node.js 18+ installed (check with `node --version`)
- [ ] npm installed (check with `npm --version`)
- [ ] LLM provider configured (run `/connect` in OpenCode)
- [ ] Config files created at `~/.config/opencode/`
- [ ] Test a basic command in OpenCode
- [ ] Load oh-my-opencode skill in OpenClaw

## Quick Reference

| Task | Command |
|------|---------|
| Check installation | `opencode --version && oh-my-opencode --version` |
| Full install | `curl -fsSL https://opencode.ai/install | bash && npm install -g oh-my-opencode` |
| Reinstall | `npm uninstall -g oh-my-opencode && npm install -g oh-my-opencode` |
| Get help | `oh-my-opencode --help` |
| Update | `npm update -g oh-my-opencode` |

## The Process

1. **Detect existing installation** – Check if OpenCode and oh-my-opencode are already installed (skip steps if found)
2. **Verify prerequisites** – Ensure Node.js 18+ is installed, check npm availability
3. **Choose installation method** – Select one: Humans (curl script), LLM Agents (bash script), or Manual (curl + npm)
4. **Execute installation** – Run chosen method and verify output shows success
5. **Configure** – Set up configuration file at project-level or user-level
6. **Verify** – Run `opencode --version` and `oh-my-opencode --version` to confirm both install
7. **Test agents** – Run `/agent sisyphus` or `/agent hephaestus` to verify agents load
8. **Initialize project** – Run `/init` inside OpenCode to create AGENTS.md

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Installing without checking** – Not running detection first causing duplicate installs or conflicts
- **Wrong Node.js version** – Installing on Node.js < 18 causing runtime errors
- **Permission denied** – Installing globally without proper permissions, or trying to install system-wide without sudo
- **Mixing installation methods** – Using curl for OpenCode but npm for oh-my-opencode causing version mismatch
- **Skipping verification** – proceeding to use OpenCode without confirming version output
- **Network failures** – Assuming installation succeeded without checking network connectivity
- **Config not created** – Trying to use oh-my-opencode without creating configuration file first

## Verification

- **Version commands work**: `opencode --version` shows version, `oh-my-opencode --version` shows version
- **Agents load**: `/agent` command switches to sisyphus, hephaestus, oracle, librarian, explore without errors
- **Config loads**: Configuration file is found at project/user level, values returned via config get
- **Hooks working**: Hook commands execute at expected times without errors
- **MCPs respond**: MCP servers installed and responding to tool calls
- **Project init works**: `/init` creates AGENTS.md in project root
- **No errors in logs**: `opencode logs` shows no installation errors or warnings

## References

- OpenCode Docs: https://opencode.ai/docs/
- Oh My OpenCode: https://github.com/code-yeongyu/oh-my-opencode
- Installation Guide: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/guide/installation.md

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |

## Related Skills

- oh-my-opencode: Overall integration
- oh-my-opencode-agents: Agent usage guide
- oh-my-opencode-usage: Daily usage patterns
- oh-my-opencode-configuration: Advanced configuration

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
