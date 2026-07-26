# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| ≥ 3.x   | ✅ Active          |
| < 3.0   | ❌ Not maintained  |

## Secret Detection

This repository uses **gitleaks** (v8.30.1) for pre-commit and CI secret scanning.

### CI Integration

Secret scanning runs in two CI workflows:

- **validate.yml** — runs on every push/PR to main; scans both the working tree and the full git history
- **auto-release.yml** — runs on tag push as a release gate; blocks release if secrets are found

### Current status (as of v3.26.0)

- `gitleaks detect --no-git` — **0 leaks found** (exit 0)
- `gitleaks detect` (full git history) — to be verified per baseline

### False positives in `.gitleaksignore`

| File | Rule | Reason |
|------|------|--------|
| `operations/jira/SKILL.md` | `curl-auth-user` | Documentation example showing truncated token format (`ATATT3xFfGF0...`) |
| `trading/smart-contract-dev/SKILL.md` | `generic-api-key` | Solidity error constant `ERC20InsufficientBalance` |

## Reporting a Vulnerability

This is a **skill library** — it contains documentation, examples, and code patterns for AI agents.
It is NOT a production application or service.

If you discover a security issue:

1. **DO NOT** open a public GitHub issue
2. **DO** email the maintainer directly (see `package.json` for contact)
3. Include the scope and reproduction steps

We aim to respond within 48 hours.

## Supply Chain

- All CI actions are pinned to SHA digests (see `.github/workflows/`)
- Python dependencies: `pyyaml` only (installed fresh each CI run)
- npm dependencies: minimal production dependencies (see `package.json`)
- No runtime secrets or credentials stored in the repository

## Cryptographic Key Handling

Skills in this repo may reference API keys, tokens, or cryptographic material in **documentation examples only**.
All such examples use truncated or placeholder values. Real credentials must never be committed.

## Related Documentation

- [SKILL_STANDARD.md](./SKILL_STANDARD.md) — Skill content standards
- [SKILL_QUALITY_RUBRIC.md](./SKILL_QUALITY_RUBRIC.md) — Quality rubric
