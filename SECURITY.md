# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 3.x | ✅ Active |
| < 3.0 | ❌ No |

## Reporting a Vulnerability

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, email [security@1ai.dev](mailto:security@1ai.dev) with:

1. Description of the vulnerability
2. Steps to reproduce
3. Affected skills/components
4. Potential impact assessment

### Response Timeline

| Step | SLA |
|---|---|
| Acknowledgment | 48 hours |
| Initial assessment | 5 business days |
| Fix/patch | 14 business days |
| Public disclosure | After fix is released |

### Scope

In scope:
- SKILL.md injection attacks (prompt injection via skill content)
- Malicious code execution through skill hooks
- Credential/data leakage through skill outputs
- Supply chain attacks on skill dependencies

Out of scope:
- Skills that behave as documented (even if suboptimal)
- Third-party MCP server vulnerabilities (report to their maintainers)
- Social engineering attacks

## Best Practices for Skill Consumers

1. **Review before loading** — Read SKILL.md content before invoking unfamiliar skills
2. **Sandbox execution** — Run skill hooks in isolated environments
3. **Audit hooks** — Review `hooks/` scripts before installing
4. **Pin versions** — Use specific skill versions, not `latest`
5. **Report suspicious skills** — Flag skills that request unnecessary permissions
