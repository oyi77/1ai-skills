---
name: buildkite-pipelines
description: Buildkite CI pipelines — pipeline YAML, steps, agents, artifacts, test splitting, dynamic pipelines
---

## Overview

Buildkite is a CI/CD platform where pipelines are defined in YAML and executed by self-hosted agents. Known for speed, flexibility, and hybrid cloud/agent architecture.

## Capabilities

- YAML pipeline configuration
- Self-hosted agents (any OS, any cloud)
- Test splitting and parallelism
- Artifact upload/download between steps
- Dynamic pipeline generation
- Block steps for manual approval

## When to Use

- Need fast CI with self-hosted runners
- Want test splitting for parallel execution
- Need hybrid cloud CI (agents anywhere)
- Complex pipelines with manual gates

## Pseudo Code

### Pipeline Configuration
```yaml
# .buildkite/pipeline.yml
steps:
  - label: ":hammer: Test"
    command: npm ci && npm test
    agents:
      queue: default

  - wait

  - label: ":rocket: Deploy"
    command: ./deploy.sh
    branches: main
    agents:
      queue: production
```

### Test Splitting
```yaml
steps:
  - label: ":jest: Tests %n"
    command:
      - npm ci
      - TEST_FILES=$(buildkite-agent artifact search "tests/**" | split -n r/$BUILDKITE_PARALLEL_JOB)
      - jest $TEST_FILES
    parallelism: 4
    agents:
      queue: default
```

### Dynamic Pipeline
```bash
#!/bin/bash
# generate-pipeline.sh
echo "steps:"
for service in $(ls services/); do
  echo "  - label: ':docker: Build $service'"
  echo "    command: docker build services/$service"
done | buildkite-agent pipeline upload
```

### Manual Approval Gate
```yaml
steps:
  - label: ":rocket: Deploy to Production"
    block: "Approve Production Deploy"
    fields:
      - select: "Environment"
        key: "env"
        options:
          - label: "Production"
            value: "prod"
          - label: "Staging"
            value: "staging"

  - label: ":ship: Deploy"
    command: ./deploy.sh
    depends_on: "Deploy to Production"
```

## Common Patterns

- **Agents queue**: `agents: { queue: "deploy" }` routes to specific agent pools
- **Artifacts**: `buildkite-agent artifact upload build.zip` / `download build.zip`
- **Hooks**: Agent-level hooks in `~/.buildkite-agent/hooks/`
- **Plugins**: `plugins: [docker#v5.0.0: { image: "node:20" }]`
- **Notify**: Slack/email notifications on failure via `notify` block
