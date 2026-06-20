---
name: circleci-config
description: CircleCI configuration — workflows, jobs, orbs, caching, contexts, dynamic config
domain: devops
tags:
- ci-cd
- circleci
- config
- devops
- infrastructure
- workflow
---


## Overview

CircleCI uses YAML-based `.circleci/config.yml` for CI/CD pipelines. Orbs provide reusable packages of jobs, commands, and executors. Workflows orchestrate jobs with dependency graphs.

## Capabilities

- Job and workflow orchestration with dependency graphs
- Orbs for reusable CI components
- Workspace persistence between jobs
- Context-based secret management
- Dynamic config with setup workflows
- Matrix/parameterized builds

## When to Use

- GitHub/GitLab repos needing fast CI/CD
- Projects benefiting from orb ecosystem
- Need matrix builds across multiple environments
- Teams wanting managed CI with minimal setup

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The circleci-config workflow follows a standard pipeline pattern.

Core flow:
```
# circleci-config primary flow
input = prepare(raw_data)
result = process(input, config={caching, circleci, config, configuration, contexts})
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


### Basic Pipeline
```yaml
# .circleci/config.yml
version: 2.1

orbs:
  node: circleci/node@6
  docker: circleci/docker@25

jobs:
  test:
    executor:
      name: node/default
      tag: '20'
    steps:
      - checkout
      - node/install-packages
      - run: npm test
      - run: npm run lint

  build-and-push:
    docker:
      - image: cimg/base:current
    steps:
      - checkout
      - setup_remote_docker:
          version: default
      - run: docker build -t $DOCKERHUB_USERNAME/app:$CIRCLE_SHA1 .
      - run: echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USERNAME --password-stdin
      - run: docker push $DOCKERHUB_USERNAME/app:$CIRCLE_SHA1

workflows:
  build-test-deploy:
    jobs:
      - test
      - build-and-push:
          context: docker-creds
          requires:
            - test
          filters:
            branches:
              only: main
```

### Matrix Builds
```yaml
jobs:
  test:
    parameters:
      node-version:
        type: string
      os:
        type: executor
    executor: << parameters.os >>
    steps:
      - checkout
      - run: nvm use << parameters.node-version >>
      - run: npm test

workflows:
  matrix-test:
    jobs:
      - test:
          matrix:
            parameters:
              node-version: ['18', '20', '22']
              os: [linux, macos]
```

### Dynamic Config
```yaml
# .circleci/config.yml
setup: true
orbs:
  path-filtering: circleci/path-filtering@1

workflows:
  setup:
    jobs:
      - path-filtering/filter:
          mapping: |
            backend/.* backend-changed true
            frontend/.* frontend-changed true
```

## Common Patterns

- **Caching**: `save_cache`/`restore_cache` with checksum keys
- **Workspaces**: persist files between jobs with `persist_to_workspace`
- **Contexts**: share environment variables across projects
- **Orbs**: circleci/node, circleci/docker, circleci/aws-cli (install via `circleci orb pack`)

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
