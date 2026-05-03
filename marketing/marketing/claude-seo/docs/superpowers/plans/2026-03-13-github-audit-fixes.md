# GitHub Audit Fixes Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise the GitHub repo health score from 70/100 by closing all audit gaps identified in the 2026-03-13 audit.

**Architecture:** All changes are isolated file edits and net-new file creation, with no refactoring and no dependency changes. GitHub settings are updated via `gh repo edit`. The `.github/` directory does not yet exist; all files in it are created from scratch with zero conflict risk.

**Tech Stack:** Markdown, YAML, GitHub Actions, `gh` CLI

---

## Pre-flight Checklist (Verify Before Any Changes)

- [ ] Confirm `agents/` directory has exactly 7 files:
  `seo-content.md seo-geo.md seo-performance.md seo-schema.md seo-sitemap.md seo-technical.md seo-visual.md`
- [ ] Confirm CITATION.cff does NOT exist: `ls CITATION.cff 2>&1` → "No such file"
- [ ] Confirm `.github/` does NOT exist: `ls .github/ 2>&1` → "No such file"
- [ ] Confirm `plugin.json` version is `"1.3.2"` and agents array has 6 items (missing seo-geo)
- [ ] Confirm README line 181 says `Subagents (6 total)`
- [ ] Confirm CHANGELOG.md line 123 says "6 subagents" - **this is in the v1.0.0 historical entry, do NOT touch it**

---

## Task 1: Fix plugin.json (version bump + add seo-geo agent)

**Files:** Modify `plugin.json`

**What & Why:** Version is still `1.3.2` but the codebase is on v1.4.0. The `agents` array is missing `agents/seo-geo.md` which was added in v1.4.0.

**Safe to change:** Purely additive - adding one entry to the array and bumping a string.

- [ ] Open `plugin.json`, verify current state:
  - `"version": "1.3.2"` ← stale
  - agents array has 6 items, ends with `"agents/seo-visual.md"` ← missing seo-geo
- [ ] Change `"version"` from `"1.3.2"` to `"1.4.0"`
- [ ] Add `"agents/seo-geo.md"` to the `agents` array (after `"agents/seo-visual.md"`)
- [ ] Verify the JSON is valid: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"`
- [ ] Commit:
  ```bash
  git add .claude-plugin/plugin.json
  git commit -m "fix: bump plugin.json to v1.4.0 and add seo-geo agent"
  ```

---

## Task 2: Fix README.md (H1 keyword, ToC, version badge, architecture count)

**Files:** Modify `README.md`

**What & Why:**
- H1 is `# Claude SEO` (weak keyword signal) → add keyword suffix
- No Table of Contents (10+ sections, hard to navigate)
- Only 2 badges → add GitHub release version badge
- Architecture block says `Subagents (6 total)` → should be 7

**Safe to change:** All edits are in isolated sections. No cross-file references break.

- [ ] Strengthen H1 (line 5):
  - Change `# Claude SEO` -> `# Claude SEO: SEO Audit Skill for Claude Code`
- [ ] Add version badge after existing badges (line 12, after License badge):
  ```markdown
  [![Version](https://img.shields.io/github/v/release/AgriciDaniel/claude-seo)](https://github.com/AgriciDaniel/claude-seo/releases)
  ```
- [ ] Add Table of Contents between the intro paragraph and `## Installation` section.
  Insert after line 12 (the badges block), before line 14 (`## Installation`):
  ```markdown

  ## Table of Contents

  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Commands](#commands)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Extensions](#extensions)
  - [Documentation](#documentation)
  - [Requirements](#requirements)
  - [Uninstall](#uninstall)
  - [Contributing](#contributing)
  ```
- [ ] Fix architecture block (line 181 after ToC insertion - find by content):
  - Change `~/.claude/agents/seo-*.md     # Subagents (6 total)` → `~/.claude/agents/seo-*.md     # Subagents (7 total)`
- [ ] Verify no other "6 total" or "6 subagent" strings remain:
  `grep -n "6 total\|6 subagent" README.md`
- [ ] Commit:
  ```bash
  git add README.md
  git commit -m "docs: strengthen H1, add ToC and version badge, fix subagent count to 7"
  ```

---

## Task 3: Fix SECURITY.md (add response timeline)

**Files:** Modify `SECURITY.md`

**What & Why:** Missing acknowledgment and resolution timeline, required for full Community Standards score.

**Safe to change:** Pure addition to existing section.

- [ ] Add response timeline to the "Reporting a Vulnerability" section.
  After the 3-item list and before `## Supported Versions`, insert:
  ```markdown

  ## Response Timeline

  - **Acknowledgment**: Within 72 hours of report
  - **Status update**: Within 7 days with initial assessment
  - **Resolution**: We aim to release a fix within 30 days for confirmed vulnerabilities
  ```
- [ ] Commit:
  ```bash
  git add SECURITY.md
  git commit -m "docs: add vulnerability response timeline to SECURITY.md"
  ```

---

## Task 4: Create CITATION.cff

**Files:** Create `CITATION.cff`

**What & Why:** File doesn't exist. Enables academic citation. Required for GitHub Community Standards full score.

- [ ] Create `CITATION.cff` at repo root:
  ```yaml
  cff-version: 1.2.0
  title: Claude SEO
  message: >-
    If you use this software, please cite it using the metadata from this file.
  type: software
  authors:
    - alias: AgriciDaniel
      given-names: Daniel
      family-names: Agricidaniel
  repository-code: 'https://github.com/AgriciDaniel/claude-seo'
  url: 'https://github.com/AgriciDaniel/claude-seo'
  license: MIT
  version: 1.4.0
  date-released: '2026-03-12'
  keywords:
    - seo
    - claude-code
    - ai-tools
    - schema-markup
    - e-e-a-t
    - geo
  ```
- [ ] Commit:
  ```bash
  git add CITATION.cff
  git commit -m "docs: add CITATION.cff for academic citation support"
  ```

---

## Task 5: Create .github/ directory infrastructure

**Files:** Create 8 new files under `.github/`

**What & Why:** No `.github/` directory exists. This single gap zeros out: issue templates (20pts), PR template (10pts), devcontainer/Dependabot (15pts) in Community Health scoring. Creating these closes the biggest single scoring gap.

**Safe to create:** Directory doesn't exist at all, so zero conflict risk.

### 5a: Issue Templates

- [ ] Create `.github/ISSUE_TEMPLATE/bug_report.yml`:
  ```yaml
  name: Bug Report
  description: Report a bug or unexpected behavior in Claude SEO
  title: "[Bug]: "
  labels: ["bug"]
  body:
    - type: markdown
      attributes:
        value: |
          Thanks for reporting a bug! Please fill in as much detail as possible.
    - type: input
      id: os
      attributes:
        label: Operating System
        description: e.g. macOS 14, Ubuntu 24.04, Windows 11
      validations:
        required: true
    - type: input
      id: python-version
      attributes:
        label: Python Version
        description: Run `python3 --version`
      validations:
        required: true
    - type: input
      id: command
      attributes:
        label: Command that failed
        description: e.g. `/seo audit https://example.com`
      validations:
        required: true
    - type: textarea
      id: error-output
      attributes:
        label: Full error output
        description: Copy the complete terminal output
        render: shell
      validations:
        required: true
    - type: textarea
      id: expected
      attributes:
        label: Expected behavior
        description: What did you expect to happen?
      validations:
        required: true
  ```

- [ ] Create `.github/ISSUE_TEMPLATE/feature_request.yml`:
  ```yaml
  name: Feature Request
  description: Suggest a new feature or improvement for Claude SEO
  title: "[Feature]: "
  labels: ["enhancement"]
  body:
    - type: markdown
      attributes:
        value: |
          Have a great idea? We'd love to hear it! For general discussion, consider using [GitHub Discussions](https://github.com/AgriciDaniel/claude-seo/discussions) instead.
    - type: textarea
      id: problem
      attributes:
        label: Problem statement
        description: What problem does this feature solve?
      validations:
        required: true
    - type: textarea
      id: solution
      attributes:
        label: Proposed solution
        description: Describe how you'd like it to work
      validations:
        required: true
    - type: textarea
      id: alternatives
      attributes:
        label: Alternatives considered
        description: Any alternative solutions or features you've considered?
  ```

- [ ] Create `.github/ISSUE_TEMPLATE/config.yml`:
  ```yaml
  blank_issues_enabled: false
  contact_links:
    - name: Question or Discussion
      url: https://github.com/AgriciDaniel/claude-seo/discussions
      about: Ask questions and discuss ideas in GitHub Discussions
  ```

- [ ] Commit:
  ```bash
  git add .github/ISSUE_TEMPLATE/
  git commit -m "ci: add YAML issue templates for bug reports and feature requests"
  ```

### 5b: PR Template

- [ ] Create `.github/PULL_REQUEST_TEMPLATE.md`:
  ```markdown
  ## Summary

  <!-- What does this PR do? Why is it needed? -->

  ## Type of Change

  - [ ] Bug fix
  - [ ] New feature / sub-skill
  - [ ] Documentation update
  - [ ] Refactor / code quality
  - [ ] Other (describe below)

  ## Checklist

  - [ ] Tested with a real URL before submitting
  - [ ] SKILL.md files stay under 500 lines (if modified)
  - [ ] Python scripts output JSON (if modified)
  - [ ] Reference files stay under 200 lines (if modified)
  - [ ] `set -euo pipefail` used in any new shell scripts
  - [ ] CHANGELOG.md updated with the change
  ```
- [ ] Commit:
  ```bash
  git add .github/PULL_REQUEST_TEMPLATE.md
  git commit -m "ci: add PR template with checklist"
  ```

### 5c: GitHub Actions CI

**What:** Python syntax validation for scripts in `scripts/`. No test suite exists, so this is the minimum viable CI. It validates that all scripts are syntactically correct Python 3.10+.

- [ ] Create `.github/workflows/ci.yml`:
  ```yaml
  name: CI

  on:
    push:
      branches: [main]
    pull_request:
      branches: [main]

  jobs:
    lint:
      name: Python Syntax Check
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4

        - name: Set up Python 3.10
          uses: actions/setup-python@v5
          with:
            python-version: "3.10"

        - name: Check Python syntax
          run: |
            python3 -m py_compile scripts/fetch_page.py
            python3 -m py_compile scripts/parse_html.py
            python3 -m py_compile scripts/analyze_visual.py
            python3 -m py_compile scripts/capture_screenshot.py
            echo "All scripts passed syntax check"
  ```
- [ ] Commit:
  ```bash
  git add .github/workflows/ci.yml
  git commit -m "ci: add GitHub Actions workflow for Python syntax validation"
  ```

### 5d: Dependabot

- [ ] Create `.github/dependabot.yml`:
  ```yaml
  version: 2
  updates:
    - package-ecosystem: "pip"
      directory: "/"
      schedule:
        interval: "weekly"
      labels:
        - "dependencies"

    - package-ecosystem: "github-actions"
      directory: "/"
      schedule:
        interval: "weekly"
      labels:
        - "dependencies"
  ```
- [ ] Commit:
  ```bash
  git add .github/dependabot.yml
  git commit -m "ci: add Dependabot for pip and GitHub Actions updates"
  ```

### 5e: FUNDING and Release Config

- [ ] Create `.github/FUNDING.yml`:
  ```yaml
  # Funding links for this project
  # See: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository
  custom:
    - https://www.skool.com/ai-marketing-hub-pro
  ```

- [ ] Create `.github/release.yml`:
  ```yaml
  changelog:
    exclude:
      labels:
        - ignore-for-release
    categories:
      - title: Security
        labels:
          - security
      - title: New Features
        labels:
          - enhancement
          - feature
      - title: Bug Fixes
        labels:
          - bug
          - fix
      - title: Documentation
        labels:
          - documentation
          - docs
      - title: Dependencies
        labels:
          - dependencies
      - title: Other Changes
        labels:
          - "*"
  ```

- [ ] Commit:
  ```bash
  git add .github/FUNDING.yml .github/release.yml
  git commit -m "ci: add FUNDING.yml and release.yml for auto-generated release notes"
  ```

---

## Task 6: Update GitHub Repository Settings

**What & Why:** These are GitHub UI settings that can be set via `gh repo edit`. Cannot be done via file commits; must use the CLI.

**Changes:**
1. Enable Discussions (currently off, but CONTRIBUTING.md tells users to use it)
2. Disable Wiki (currently on but unused, misleads visitors)
3. Fix description ("6 subagents" → "7 subagents")
4. Add topics: `python`, `skill`

**IMPORTANT:** These changes take effect immediately on the remote repo. Verify with `gh repo view` after each change.

- [ ] Enable Discussions:
  ```bash
  gh repo edit AgriciDaniel/claude-seo --enable-discussions
  ```
  Verify: `gh repo view AgriciDaniel/claude-seo --json hasDiscussionsEnabled --jq .hasDiscussionsEnabled`
  Expected: `true`

- [ ] Disable Wiki:
  ```bash
  gh repo edit AgriciDaniel/claude-seo --enable-wiki=false
  ```
  Verify: `gh repo view AgriciDaniel/claude-seo --json hasWikiEnabled --jq .hasWikiEnabled`
  Expected: `false`

- [ ] Fix description (replace "6 subagents" with "7 subagents"):
  ```bash
  gh repo edit AgriciDaniel/claude-seo --description "Universal SEO skill for Claude Code. 13 sub-skills, 7 subagents, extensions system with DataForSEO MCP integration. Technical SEO, E-E-A-T, schema, GEO/AEO, and strategic planning."
  ```
  Verify: `gh repo view AgriciDaniel/claude-seo --json description --jq .description`

- [ ] Add topics `python` and `skill`:
  ```bash
  gh repo edit AgriciDaniel/claude-seo --add-topic python --add-topic skill
  ```
  Verify: `gh repo view AgriciDaniel/claude-seo --json repositoryTopics --jq '.repositoryTopics | map(.name)'`
  Expected: 15 topics including `python` and `skill`

- [ ] Push all committed changes:
  ```bash
  git push origin main
  ```

---

## Task 7: Final Verification

- [ ] Confirm all 8 `.github/` files exist:
  ```bash
  find .github/ -type f | sort
  ```
  Expected 8 files: 3 under ISSUE_TEMPLATE/, PR template, ci.yml, dependabot.yml, FUNDING.yml, release.yml

- [ ] Confirm CITATION.cff exists and is valid YAML:
  ```bash
  python3 -c "import yaml; yaml.safe_load(open('CITATION.cff'))" && echo "valid"
  ```

- [ ] Confirm plugin.json is valid JSON and has 7 agents:
  ```bash
  python3 -c "import json; d=json.load(open('.claude-plugin/plugin.json')); print(d['version'], len(d['agents']))"
  ```
  Expected: `1.4.0 7`

- [ ] Confirm no stale "6 subagent/total" strings remain in actively-versioned content:
  ```bash
  grep -rn "6 subagent\|subagents (6\|6 total" --include="*.md" --include="*.json" . \
    --exclude-dir=".git" --exclude-dir="claude-seo-main" --exclude-dir="claude-ads-main"
  ```
  Expected: Only line 123 in CHANGELOG.md (v1.0.0 historical entry, correct, do not touch)

- [ ] Confirm GitHub settings applied:
  ```bash
  gh repo view AgriciDaniel/claude-seo --json description,hasDiscussionsEnabled,hasWikiEnabled,repositoryTopics
  ```

- [ ] Confirm CI workflow is visible on GitHub:
  ```bash
  gh workflow list --repo AgriciDaniel/claude-seo
  ```

---

## Do NOT Change

- `CHANGELOG.md` line 123: "6 subagents" is in the v1.0.0 historical entry. It was accurate when written.
- `seo/SKILL.md`: already correctly says "7 subagents"
- `CLAUDE.md`: already correctly says "7 parallel subagents"
- `docs/ARCHITECTURE.md`, `docs/COMMANDS.md`: no stale counts found
- `scripts/mobile_analysis.py`: already in `.gitignore` as a generated file

## Expected Score Impact

| Category | Before | Expected After |
|----------|--------|---------------|
| README Quality | 79 | ~84 (H1, ToC, badge) |
| Metadata & Discovery | 79 | ~87 (description, topics, Discussions) |
| Legal Compliance | 78 | ~88 (CITATION.cff, SECURITY timeline) |
| Community Health | 38 | ~68 (issue templates, PR template, dependabot) |
| Release & Maintenance | 67 | ~80 (CI, dependabot, release.yml, badge) |
| SEO & Discoverability | 73 | ~79 (Discussions, keyword H1) |
| **Overall** | **70** | **~81** |
