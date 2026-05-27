---
name: circleci-config
description: CircleCI configuration — workflows, jobs, orbs, caching, contexts, dynamic config
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

## Pseudo Code

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
- **Orbs**: `circleci/node`, `circleci/docker`, `circleci/aws-cli`
