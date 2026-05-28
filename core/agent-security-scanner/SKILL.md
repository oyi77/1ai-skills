---
name: agent-security-scanner
description: Agentic security patterns for AI agent systems including attack vector defense, sandboxing, input sanitization, security scanning, CVE awareness, and least-privilege tool access. Use when securing agent configurations, scanning for vulnerabilities, hardening agent tool access, or defending against prompt injection and data exfiltration.
domain: core
tags: [security, prompt-injection, sandboxing, agentshield, least-privilege, cve, scanning]
persona:
  name: "AgentShield"
  title: "Agentic Security Engineer"
  expertise: ["AI Agent Attack Vectors", "Sandboxing", "Prompt Injection Defense", "Tool Permission Hardening", "CVE Analysis", "Security Scanning"]
  philosophy: "Trust nothing. Verify everything. Sandbox what you cannot trust. Limit what you cannot sandbox."
---

## Overview

AI agents present a unique attack surface: they read untrusted input, execute code, access files, call APIs, and spawn subagents -- all with elevated privileges. Traditional application security applies, but new agent-specific vectors (prompt injection, tool abuse, data exfiltration via agent actions) require dedicated defense patterns. This skill covers the full agentic security lifecycle: threat modeling, hardening, scanning, and continuous monitoring.

## When to Use

- Setting up security scanning for agent configurations (.claude/, settings.json, MCP configs)
- Hardening agent tool permissions after modification
- Auditing hooks and MCP servers for injection or exfiltration risks
- Defending against prompt injection in agent inputs
- Implementing sandboxed execution for untrusted code
- Reviewing agent dependency CVEs
- Before committing agent configuration changes to production
- Onboarding to a repository with existing agent configurations

## Process / Steps

### 1. Attack Vector Inventory

Know the threats before defending against them:

**Prompt Injection**
| Vector | Attack | Defense |
|--------|--------|---------|
| CLAUDE.md / AGENTS.md | Hidden instructions in project files override agent behavior | Scan for auto-run directives, hidden text, conflicting instructions |
| User input | Crafted prompts bypass safety guardrails | Input sanitization, instruction hierarchy enforcement |
| File content | Malicious code comments or strings inject instructions | Content scanning before agent reads untrusted files |
| MCP responses | MCP server returns injected instructions | Validate MCP response format, strip instruction-like content |
| Subagent output | Subagent returns instructions instead of data | Treat subagent output as data, never as instructions |

**Tool Abuse**
| Vector | Attack | Defense |
|--------|--------|---------|
| Bash execution | Agent runs arbitrary shell commands from untrusted input | Sandbox with allowlists, never interpolate untrusted input into commands |
| File write | Agent writes malicious files (backdoors, exfiltration scripts) | Restrict write paths, validate file content before write |
| File read | Agent reads sensitive files (credentials, secrets, keys) | Denylist for sensitive paths (.env, credentials, private keys) |
| Network access | Agent makes outbound requests to exfiltrate data | Block outbound HTTP from hooks, validate URLs in tool calls |
| MCP tools | Agent calls MCP tools with malicious parameters | Validate MCP tool parameters, rate-limit tool calls |

**Data Exfiltration**
| Vector | Attack | Defense |
|--------|--------|---------|
| Commit content | Secrets committed to git | Pre-commit secret scanning (gitleaks, truffleHog) |
| Tool output | Agent includes sensitive data in tool responses | Redact sensitive patterns from tool outputs |
| Subagent delegation | Sensitive context passed to subagent that logs it | Minimize context, exclude secrets from subagent payloads |
| Hook logs | Hooks log sensitive data to files | Sanitize hook output, exclude secrets from logs |

### 2. Sandboxing Untrusted Code Execution

**Principle**: Never execute untrusted code in the main agent environment.

**Layer 1: Allowlist-Based Execution**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run build)",
      "Bash(npx tsc --noEmit)",
      "Bash(git status)",
      "Bash(git diff)"
    ],
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(rm -rf *)",
      "Bash(chmod 777 *)",
      "Bash(eval *)",
      "Bash(sudo *)"
    ]
  }
}
```

**Layer 2: Container Isolation**
```bash
# Run untrusted code in ephemeral container
docker run --rm --network none --read-only \
  --memory 512m --cpus 1 \
  -v "$(pwd)/src:/app:ro" \
  node:20-alpine \
  node /app/untrusted-script.js
```

**Layer 3: Process Sandboxing**
```bash
# Use bubblewrap or firejail for process isolation
bwrap --ro-bind / / \
      --dev /dev \
      --tmpdir /tmp \
      --unshare-net \
      --die-with-parent \
      node untrusted-script.js
```

### 3. Input Sanitization for Agent Inputs

**Sanitization Pipeline**
```
Untrusted Input -> Strip Instructions -> Validate Format -> Length Limit -> Pass to Agent
```

**Strip Injection Patterns**
```python
INJECTION_PATTERNS = [
    r'ignore\s+(previous|above|all)\s+instructions',
    r'you\s+are\s+now\s+',
    r'system\s*:\s*',
    r'<\s*system\s*>',
    r'```system',
    r'IMPORTANT:\s*override',
    r'DISREGARD\s+(all|previous)',
]

def sanitize_input(text: str) -> str:
    for pattern in INJECTION_PATTERNS:
        text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)
    return text[:MAX_INPUT_LENGTH]
```

**File Content Scanning**
```python
def scan_file_before_read(filepath: str) -> bool:
    """Return True if safe to read, False if suspicious."""
    content = read_file(filepath)

    # Check for embedded instructions
    if contains_instruction_patterns(content):
        return False

    # Check for encoded payloads (base64, hex)
    if contains_encoded_payloads(content):
        return False

    # Check for excessively long lines (potential payload)
    if any(len(line) > 10000 for line in content.split('\n')):
        return False

    return True
```

### 4. Security Scanning Integration

**AgentShield Scan Workflow**
```bash
# Install AgentShield
npm install -g ecc-agentshield

# Scan agent configuration
npx ecc-agentshield scan

# Scan with severity filter
npx ecc-agentshield scan --min-severity medium

# Output formats
npx ecc-agentshield scan --format json    # CI/CD integration
npx ecc-agentshield scan --format markdown # Documentation
npx ecc-agentshield scan --format html     # Review reports

# Auto-fix safe issues
npx ecc-agentshield scan --fix

# Deep analysis with multi-agent red/blue team
npx ecc-agentshield scan --opus --stream
```

**What Gets Scanned**

| Component | Checks |
|-----------|--------|
| CLAUDE.md / AGENTS.md | Hardcoded secrets, auto-run instructions, prompt injection patterns |
| settings.json / config.json | Overly permissive allow lists, missing deny lists, dangerous bypass flags |
| mcp.json | Risky MCP servers, hardcoded env secrets, npx supply chain risks |
| hooks/ | Command injection via interpolation, data exfiltration, silent error suppression |
| agents/*.md | Unrestricted tool access, prompt injection surface, missing model specs |
| Package dependencies | Known CVEs, outdated packages, suspicious dependencies |

**CI/CD Integration**
```yaml
# .github/workflows/agent-security.yml
- name: Agent Security Scan
  run: |
    npx ecc-agentshield scan --format json --min-severity high > scan-results.json
    if jq -e '.summary.high > 0 or .summary.critical > 0' scan-results.json; then
      echo "Security scan failed: critical or high severity issues found"
      exit 1
    fi
```

### 5. CVE Awareness for Agent Dependencies

**Dependency Audit Workflow**
```bash
# Node.js
npm audit --production
npm audit fix --force  # Only in isolated branch, review changes

# Python
pip-audit
safety check

# MCP servers (often overlooked)
# Check each MCP server's npm/pip dependencies independently
npx npm-check-updates --dep prod -u
```

**MCP Server Supply Chain Risks**
- MCP servers run with agent privileges -- a compromised MCP server is a compromised agent
- Pin MCP server versions, do not use `@latest` or `@next`
- Audit MCP server dependencies separately from project dependencies
- Prefer MCP servers from verified publishers with security policies
- Monitor for typosquatting in MCP server package names

### 6. Principle of Least Privilege for Agent Tools

**Permission Tier Design**

| Tier | Tools Allowed | Use Case |
|------|--------------|----------|
| Read-Only | Read, Grep, Glob, LSP tools | Code exploration, research |
| Standard | Read-Only + Edit, Write, Bash (allowlisted) | Daily development |
| Admin | Standard + unrestricted Bash, file system | Infrastructure, CI/CD |
| Superuser | All tools including MCP admin tools | Emergency only, requires approval |

**Settings.json Hardening**
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep",
      "Glob",
      "Edit",
      "Write",
      "Bash(npm test *)",
      "Bash(npm run build *)",
      "Bash(git *)"
    ],
    "deny": [
      "Bash(curl * | bash)",
      "Bash(wget * | sh)",
      "Bash(rm -rf /)",
      "Bash(sudo *)",
      "Bash(eval *)",
      "Bash(echo * > ~/.ssh/*)",
      "Bash(env | grep -i key)",
      "Bash(printenv)"
    ]
  }
}
```

**Hook Security Hardening**
```bash
# BAD: Command injection via untrusted variable
echo "Processing $USER_INPUT" | bash

# GOOD: Sanitized, no shell interpolation
echo "Processing sanitized input" >> /var/log/agent.log

# BAD: Logging sensitive data
echo "API_KEY=$API_KEY" >> debug.log

# GOOD: Log presence, not value
[ -n "$API_KEY" ] && echo "API_KEY is set" >> debug.log
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "My agent only runs locally, security is not a concern" | Local agents still read untrusted files, execute code, and can exfiltrate data via git commits or network calls |
| "Prompt injection is theoretical, not a real threat" | Real-world prompt injection attacks have been documented in production agent systems; OWASP ranks it as a top LLM risk |
| "The agent is smart enough to avoid dangerous commands" | Agents follow instructions, including injected ones; defense must be at the harness layer, not the model layer |
| "I trust all my MCP servers" | Supply chain attacks compromise trusted packages; trust but verify with pinned versions and dependency audits |
| "Scanning slows down my workflow" | A 10-second scan prevents hours of incident response; automate it in CI to keep the workflow fast |
| "Allowlists are too restrictive" | Start tight, loosen only when a specific legitimate use is blocked; the inverse (start loose, try to tighten) never works |

## Red Flags

- settings.json has wildcard permissions (`Bash(*)`, `Write(*)`)
- CLAUDE.md contains "auto-run" or "always execute" instructions without justification
- MCP server versions not pinned (`@latest`, `@next`, no version)
- Hooks using shell interpolation with untrusted variables
- No deny list configured (only allow list, or neither)
- Agent has access to ~/.ssh, ~/.aws, or credential directories
- Secrets visible in agent configuration files or hook scripts
- No pre-commit secret scanning configured
- Agent dependencies have known critical CVEs with no mitigation plan
- Subagent receives full project context including secrets and credentials

## Verification

- [ ] AgentShield scan passes with zero critical and zero high severity findings
- [ ] settings.json deny list blocks dangerous Bash patterns (curl|bash, sudo, eval, rm -rf)
- [ ] No hardcoded secrets in any agent configuration file
- [ ] MCP server versions pinned to specific versions (not @latest)
- [ ] Hooks sanitized: no shell interpolation with untrusted variables, no sensitive data in logs
- [ ] CLAUDE.md/AGENTS.md scanned for prompt injection patterns
- [ ] Agent permission tier documented and appropriate for each role
- [ ] Pre-commit secret scanning configured (gitleaks or equivalent)
- [ ] Dependency audit clean: npm audit, pip-audit pass with no critical CVEs
- [ ] Subagent context packages exclude secrets and sensitive paths
