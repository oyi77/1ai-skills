---
name: drone-ci
description: Drone CI — container-native CI/CD, YAML pipelines, plugins, secrets, multi-machine builds
---

## Overview

Drone is a container-native CI/CD platform where each pipeline step runs in a Docker container. Simple YAML configuration, plugin ecosystem, and built-in secrets management.

## Capabilities

- Container-native steps (each step is a Docker container)
- YAML pipeline configuration (.drone.yml)
- Plugin ecosystem (Docker, Slack, S3, etc.)
- Encrypted secrets at repo/org level
- Multi-machine runners (Docker, SSH, Kubernetes)
- Matrix builds for testing across environments

## When to Use

- Want simple, container-based CI/CD
- Need lightweight CI that runs anywhere Docker runs
- Prefer YAML-driven pipelines over Groovy/scripted CI
- Self-hosted CI with minimal infrastructure

## Pseudo Code

### Basic Pipeline
```yaml
# .drone.yml
kind: pipeline
type: docker
name: default

steps:
  - name: test
    image: node:20
    commands:
      - npm ci
      - npm test

  - name: build
    image: plugins/docker
    settings:
      repo: myapp
      tags:
        - ${DRONE_COMMIT_SHA:0:8}
        - latest
      username:
        from_secret: docker_username
      password:
        from_secret: docker_password

  - name: deploy
    image: appleboy/drone-ssh
    settings:
      host: prod.example.com
      username: deploy
      key:
        from_secret: ssh_key
      script:
        - docker pull myapp:latest
        - docker-compose up -d
```

### Matrix Build
```yaml
kind: pipeline
type: docker
name: test

platform:
  os: linux
  arch: amd64

steps:
  - name: test
    image: node:${NODE_VERSION}
    commands:
      - npm ci
      - npm test

matrix:
  NODE_VERSION:
    - 18
    - 20
    - 22
```

### Multi-Pipeline (Dependency)
```yaml
---
kind: pipeline
type: docker
name: build
steps:
  - name: build
    image: plugins/docker
    settings:
      repo: myapp
      tags: latest

---
kind: pipeline
type: docker
name: deploy
depends_on: [build]
steps:
  - name: deploy
    image: appleboy/drone-ssh
    settings:
      host: prod.example.com
      script:
        - docker-compose up -d
```

## Common Patterns

- **Secrets**: `drone secret add --name docker_username --value admin myorg/myrepo`
- **Caching**: Use `drone-s3-cache` plugin for dependency caching
- **Concurrency**: `concurrency: { limit: 1 }` to prevent parallel deploys
- **Conditions**: `when: { branch: [main], event: [push] }` for conditional steps
- **Plugins**: Most integrations are Docker images — `plugins/docker`, `plugins/slack`, etc.
