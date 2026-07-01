---
name: buildkite-pipelines
description: Buildkite CI pipelines — pipeline YAML, steps, agents, artifacts, test splitting, dynamic pipelines
domain: devops
tags:
- ai-agent
- buildkite
- ci-cd
- devops
- infrastructure
- machine-learning
- pipeline
- pipelines
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
**Trigger phrases:**
- "buildkite pipelines"
- "Buildkite CI pipelines — pipeline YAML, steps, agents, artifacts, test splitting"


- Need fast CI with self-hosted runners
- Want test splitting for parallel execution
- Need hybrid cloud CI (agents anywhere)
- Complex pipelines with manual gates

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The buildkite-pipelines workflow follows a standard pipeline pattern.

Core flow:
```
# buildkite-pipelines primary flow
input = prepare(raw_data)
result = process(input, config={agents, artifacts, buildkite, dynamic, pipeline})
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

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |