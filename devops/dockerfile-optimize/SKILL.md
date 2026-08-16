---
name: dockerfile-optimize
description: Use when dockerfile optimization — multi-stage builds, layer caching,
  security hardening, minimal images. Use when optimizing Docker builds or hardening
  container security.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- docker
- dockerfile
- infrastructure
- optimize
version: 1.0.0
category: devops
---


## Overview

Production Dockerfile optimization — multi-stage builds, layer caching, image size reduction, and security hardening for containerized applications. Measure, then optimize.

## When to Use

Use when writing or optimizing Dockerfiles for production — reducing image size, accelerating rebuilds via layer caching, hardening container security, implementing multi-stage builds, or selecting the right base image for your language stack. Also use when auditing existing Dockerfiles for common inefficiencies and anti-patterns.

## Workflow

1. **Analyze the current state** — run `docker history <image>` to inspect layer sizes, check for root user, and measure final image size.
2. **Add `.dockerignore`** — exclude `.git/`, `node_modules/`, `__pycache__/`, `.env*`, and other build artifacts from the build context.
3. **Apply multi-stage build** — split builder and runtime stages. Install compilers and dev dependencies in the builder; copy only the runtime artifact into a slim final stage.
4. **Order layers by change frequency** — place stable instructions before volatile ones to maximize layer cache reuse.

### Layer Ordering

| Instruction | Change frequency | Position |
|---|---|---|
| `FROM` | Never | Top |
| `RUN apt-get …` | Rare (tools) | After FROM |
| `COPY *_lock.json` | Rare (lock file) | Before source |
| `RUN install` | After lock change | After lock COPY |
| `COPY src/` | Every commit | Bottom |
| `RUN compile` | Every commit | After src COPY |

**Measure:** run `docker build --no-cache-filter=builder .` to invalidate only the builder stage while keeping runtime layer caches intact.

## Size Reduction

### `.dockerignore`

Prevent the build context from bloating the first COPY layer:

```
.git/
node_modules/
__pycache__/
.env
*.md
*.pyc
Dockerfile
.dockerignore
dist/
coverage/
```

### Base Image Selection

| Base Image | Size (approx) | Best For |
|---|---|---|
| `ubuntu:24.04` | 78 MiB | Maximum compatibility |
| `python:3.12-slim` | 122 MiB | Python with apt |
| `node:22-alpine` | 127 MiB | Node.js (fast install) |
| `alpine:3.21` | 8 MiB | Go / Rust statically linked |
| `gcr.io/distroless/base` | ~15 MiB | Minimal, no shell/packager |

**Distroless** images contain only the runtime and your binary — no shell, no package manager, no unnecessary tools. This reduces attack surface and image size simultaneously.

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs22-debian12
COPY --from=builder /build/dist/ /app/
USER 1001
CMD ["node", "/app/server.js"]
```

## Security Hardening

| Rule | Implementation |
|---|---|
| No root user | `USER app` (create user before switching) |
| Read-only root filesystem | `docker run --read-only --tmpfs /tmp …` |
| Drop capabilities | `docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE …` |
| HEALTHCHECK | Add to every production Dockerfile |
| Avoid `latest` tag | Pin to digest or explicit version (`python:3.12-slim@sha256:…`) |
| Minimize RUN chains | Combine `apt-get update && apt-get install` in one layer, clean apt cache |

```bash
# Run with read-only rootfs and minimal capabilities
docker run --read-only \
  --tmpfs /tmp \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt=no-new-privileges:true \
  myapp:1.0.0
```

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| Build context too large | Missing .dockerignore | Add .dockerignore excluding node_modules, .git, etc. |
| Layer cache invalidated | File COPY before dependency install | Copy package.json first, install deps, then copy source |
| Permission denied in container | Running as root | Add USER directive with non-root user |
| Image size bloated | Single-stage build | Use multi-stage build, copy only artifacts to final stage |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Alpine is always smaller than slim" | `python:3.12-alpine` (88 MiB) vs `python:3.12-slim` (122 MiB) — Alpine wins on size but misses musl compatibility for some wheels |
| "One big RUN chain is fastest" | True at build time, but every change invalidates the entire chain — split by change frequency |
| "Distroless is too hard to debug" | Debug with `docker run --entrypoint=sh` with a debug image; swap distroless for slim in dev |
| "COPY . . at the end doesn't matter for size" | It matters for build context speed and cache invalidation — always `.dockerignore` |
| "Multi-stage is only for compiled languages" | False — Python/Node benefit too by not shipping dev dependencies and compilers |
| "Security scanning at build is enough" | Scan both image and runtime; base image vulnerabilities change over time |
| "We don't need HEALTHCHECK" | Without it, orchestrators can't detect deadlocked or stuck containers |
