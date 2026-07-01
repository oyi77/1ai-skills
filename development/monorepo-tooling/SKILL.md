---
name: monorepo-tooling
description: Monorepo management — Turborepo, Nx, pnpm workspaces, shared packages, CI optimization. Use when working with monorepo tooling.
domain: development
tags:
- coding
- monorepo
- software-engineering
- testing
- tooling
---


## Overview

Manage monorepos with Turborepo/Nx — shared packages, task pipelines, caching, and CI optimization for multi-package repositories.

## Capabilities

- Turborepo/Nx task orchestration and caching
- pnpm/npm/yarn workspaces
- Shared library packages
- Incremental builds and affected-only testing
- CI optimization with remote caching
- Package dependency management
- Versioning and publishing strategies

## When to Use
**Trigger phrases:**
- "monorepo tooling"
- "Monorepo management — Turborepo, Nx, pnpm workspaces, shared packages, CI optimi"


- Multiple packages/apps sharing common code
- Microservices or micro-frontends in one repo
- Shared TypeScript types, utilities, configs
- Need fast CI with incremental builds
- Coordinated versioning across packages

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The monorepo-tooling workflow follows a standard pipeline pattern.

Core flow:
```
# monorepo-tooling primary flow
input = prepare(raw_data)
result = process(input, config={management, monorepo, optimization, packages, pnpm})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Turborepo Setup

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.ts", "test/**/*.ts"]
    },
    "lint": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### pnpm Workspace

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

```json
// packages/shared/package.json
{
  "name": "@myorg/shared",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc"
  }
}
```

### Run Commands

```bash
# Build all packages (respects dependency order, caches)
turbo run build

# Only build packages affected by changes
turbo run build --filter=...[HEAD^1]

# Run tests in parallel
turbo run test --concurrency=10

# Remote caching (Vercel)
turbo login
turbo link
turbo run build --remote-only
```

### Nx Equivalent

```json
// nx.json
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  }
}
```

```bash
# Only test affected projects
nx affected --target=test

# Dependency graph
nx graph
```

### Shared TypeScript Config

```json
// packages/tsconfig/base.json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

```json
// apps/web/tsconfig.json
{
  "extends": "@myorg/tsconfig/base.json",
  "compilerOptions": { "outDir": "dist" }
}
```

## Common Patterns

- **Package boundaries**: Enforce import rules with ESLint `no-restricted-imports`
- **Shared configs**: Centralize ESLint, TypeScript, Prettier configs
- **Remote caching**: Use Vercel/Turborepo remote cache for CI speed
- **Affected only**: Only build/test/lint packages that changed
- **Versioning**: Use Changesets or Lerna for coordinated releases

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |