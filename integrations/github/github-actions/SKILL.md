---
name: github-actions
description: Use when gitHub Actions — CI/CD pipelines, composite actions, matrix builds, self-hosted runners. See parent skill for all GitHub automation capabilities.
domain: integrations
tags:
- actions
- api
- ci-cd
- github
- integrations
version: 1.0.0
---

# GitHub Actions

## Quick Reference

The GitHub Actions sub-skill covers CI/CD pipeline construction, composite and Docker actions, matrix builds, self-hosted runners, and OIDC-based cloud auth. This layers on the parent [GitHub Automation Hub](../SKILL.md) which covers the full Actions+Issues+PR ecosystem and money-making protocols.

**Use this when** you need to build, test, or deploy code automatically on push, schedule, or external trigger.

## Overview

GitHub Actions is a CI/CD platform built into GitHub. Workflows are YAML files in `.github/workflows/` that define jobs running on GitHub-hosted or self-hosted runners. Key capabilities beyond basic CI:
- **Composite actions** — reusable step bundles callable from any workflow (share across repos)
- **Docker actions** — full container environment for complex tooling
- **Matrix builds** — test across OS/node/python version combinations in parallel
- **Self-hosted runners** — run workflows on your own hardware (GPU access, internal networks)
- **OIDC** — authenticate to AWS/GCP/Azure without storing cloud credentials

The parent skill's `ci.yml` CI pipeline, composite action patterns, and `audit-ci.sh` are the canonical templates.

## Quick Start

### 1. Create a Workflow File
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci && npm run build
      - run: npm test
```

### 2. Add a Matrix Strategy
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test
```

### 3. Wire OIDC for Cloud Deploy
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # required for OIDC
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/GitHubActionsRole
          aws-region: us-east-1
      - run: aws s3 sync ./dist s3://my-bucket
```

## Code Snippet: Composite Action

```yaml
# .github/actions/setup-and-lint/action.yml
name: "Setup and Lint"
description: "Shared Node.js setup + lint step"
inputs:
  node-version:
    description: "Node version"
    default: "20"
runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
      shell: bash
    - run: npm run lint
      shell: bash
```

Reference from any workflow: `uses: ./.github/actions/setup-and-lint`

## Verification Checklist

- [ ] Workflow triggers on correct events (push, PR, schedule, workflow_dispatch)
- [ ] Matrix strategy covers all required OS/runtime combinations
- [ ] Secrets injected via `${{ secrets.* }}`, never hardcoded in YAML
- [ ] Caching configured (`actions/cache` or `actions/setup-*` native cache)
- [ ] Self-hosted runner label matches in job config (`runs-on: self-hosted`)

## When to Use

Use when gitHub Actions — CI/CD pipelines, composite actions, matrix builds, self-hosted runners. See parent skill for all GitHub automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Create a Workflow File
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci && npm run build
      - run: npm test
```

### 2. Add a Matrix Strategy
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test
```

### 3. Wire OIDC for Cloud Deploy
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # required for OIDC
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/GitHubActionsRole
          aws-region: us-east-1
      - run: aws s3 sync ./dist s3://my-bucket
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll copy-paste CI config between projects" | Composite actions eliminate duplication. Extract shared steps once, reuse across all repos. |
| "Matrix builds are overkill for my project" | A single uncaught version incompatibility costs more than 3 extra CI minutes. Matrix builds catch regressions silently. |
| "Storing cloud keys as secrets is fine" | OIDC eliminates long-lived cloud credentials entirely. Set it up once per account; never rotate keys again. |
