# Threat Model — 1ai-skills Repository

## Scope

This threat model covers the **1ai-skills repository** and its CI/CD pipeline.
It does NOT cover runtime environments where skills are executed — skills are documentation
and code patterns consumed by AI agents, which have their own security boundaries.

## Asset Inventory

| Asset | Description | Sensitivity |
|-------|-------------|-------------|
| SKILLS.json | Registry of all 1309+ skills | Medium — integrity critical |
| SKILL.md files | Domain-specific playbooks with code examples | Low-medium — examples may reference APIs |
| CI/CD pipeline | Automated validation + release | High — supply chain risk |
| Package registry access | npm + GitHub Packages tokens | Critical — credential exposure |
| GitHub Pages deploy | Public documentation site | Low — static content |

## Trust Boundaries

```
[Developer Workstation] → [GitHub] → [CI Workflows] → [npm/GitHub Packages]
                              ↓
                     [SKILLS.json + .md files]
                              ↓
                     [AI Agent consumption]
```

1. **Developer → GitHub**: authenticated pushes via SSH/HTTPS
2. **GitHub → CI**: GitHub Actions with minimal token scope
3. **CI → Package registries**: scoped npm/GitHub Packages tokens
4. **Repo → AI Agents**: read-only consumption of markdown content

## Threat List

### T1 — Secret Leakage in Skill Content

**Risk**: Skills contain documentation examples with API keys, tokens, or credentials that get committed.

**Mitigations**:
- gitleaks CI gate in `validate.yml` and `auto-release.yml`
- `.gitleaksignore` for documented false positives
- `.gitleaks.toml` custom rules for repo-specific patterns
- **Residual**: Low — gitleaks covers 180+ built-in rules

### T2 — Supply Chain via CI/CD

**Risk**: Compromised GitHub Actions workflow or pinned action SHA bypass.

**Mitigations**:
- All 3rd-party actions pinned to SHA digests (`actions/checkout@v4` → SHA)
- `contents: write` on release workflow scoped to tag creation only
- npm publish uses `NPM_TOKEN` secret (not hardcoded)
- **Residual**: Low — standard GitHub Actions hardening

### T3 — SKILLS.json Integrity

**Risk**: Malicious PR modifies SKILLS.json to inject misleading registry entries.

**Mitigations**:
- `validate.yml` runs frontmatter validation on every push
- `audit-skills.sh --write` ensures SKILLS.json reflects filesystem state
- PR review required for `main` branch
- **Residual**: Low — validation catches schema violations

### T4 — Malicious Skill Content

**Risk**: A skill contains instructions for harmful actions (prompt injection, social engineering).

**Mitigations**:
- All skills are documentation/code patterns — no runtime execution in repo
- Code examples in skills are illustrative, not auto-executed
- Human review in PR process
- **Residual**: Medium — content review relies on human judgment

### T5 — npm Package Compromise

**Risk**: Compromised npm token published malicious package.

**Mitigations**:
- `NPM_TOKEN` stored as GitHub secret, never in repo
- auto-release.yml runs gitleaks gate before publish
- npm 2FA enabled on account
- **Residual**: Low — standard npm security

### T6 — Dependency Version Drift

**Risk**: Unpinned CI dependencies (pip install, action versions) introduce breaking changes.

**Mitigations**:
- All GitHub Actions pinned to specific major versions (v4, v6, etc.)
- Python dependency `pyyaml` version-fixed in CI (currently latest — see `validate.yml`)
- **Residual**: Low-Medium — pip packages not pinned to exact versions

## Risk Matrix

| ID | Threat | Likelihood | Impact | Risk | Mitigation |
|----|--------|-----------|--------|------|-----------|
| T1 | Secret leakage | Low | High | Medium | gitleaks CI gate |
| T2 | CI/CD supply chain | Low | Critical | Medium | SHA-pinned actions |
| T3 | SKILLS.json integrity | Low | Medium | Low | Validation + PR review |
| T4 | Malicious skill content | Low | Medium | Low | Human review |
| T5 | npm compromise | Very Low | Critical | Low | Secret token + 2FA |
| T6 | Dependency drift | Medium | Low | Low | Version-pinned actions |

## Recommended Improvements

1. Pin `pyyaml` version in `validate.yml` (`pip install pyyaml==6.0.2`)
2. Pin `gitleaks` install to exact SHA in addition to version tag
3. Add Dependabot config for `github-actions` ecosystem
4. Consider `pip-audit` or `safety` check in CI for Python dependencies

## Review Cadence

This threat model should be reviewed:
- When CI/CD pipeline changes significantly
- When new release automation is added
- At minimum, every 6 months
