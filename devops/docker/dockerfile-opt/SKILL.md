---
name: dockerfile-opt
description: Optimize Dockerfiles with multi-stage builds, layer caching, image size reduction, and security hardening. Use when writing production Dockerfiles.
domain: devops
tags: [devops, docker, dockerfile]
version: 1.0.0
---
# Dockerfile OptProduction Dockerfile optimization — multi-stage builds, layer caching, image size reduction, and security hardening for containerized applications.
## When to Use
Use when writing or optimizing Dockerfiles for production — reducing image size, accelerating rebuilds via layer caching, hardening container security, implementing multi-stage builds, or selecting the right base image for your language stack. Also use when auditing existing Dockerfiles for common inefficiencies and anti-patterns.## Workflow
1. **Analyze the current state** — run `docker history <image>` to inspect layer sizes, check for root user, and measure final image size.2. **Add `.dockerignore`** — exclude `.git/`, `node_modules/`, `__pycache__/`, `.env*`, and other build artifacts from the build context.3. **Apply multi-stage build** — split builder and runtime stages. Install compilers and dev dependencies in the builder; copy only the runtime artifact into a slim final stage.4. **Order layers by change frequency** — place stable instructions (`FROM`, `RUN apt-get`, `COPY package*.json`) before volatile ones (`COPY src/`, `RUN compile`). This maximizes layer cache reuse on rebuilds.5. **Select the minimal base image** — match distroless, slim, or alpine variants to your language and compatibility needs.6. **Harden security** — add a non-root `USER`, set `HEALTHCHECK`, drop unnecessary capabilities with `--cap-drop=ALL --cap-add=NET_BIND_SERVICE`, and consider read-only rootfs.7. **Verify and measure** — confirm non-root user context, scan with `docker scout` or `trivy`, compare before/after size, and test with `--read-only` to catch runtime issues.## Multi-Stage Build PatternSeparate build-time dependencies from runtime. The builder stage installs compilers and dev packages; the runtime stage copies only the compiled artifact.```dockerfile# === BUILDER STAGE ===FROM python:3.12-slim AS builderWORKDIR /buildCOPY requirements.txt .RUN pip install --no-cache-dir -r requirements.txtCOPY src/ src/RUN python -m compileall src/# === RUNTIME STAGE ===FROM python:3.12-slimWORKDIR /appCOPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packagesCOPY --from=builder /build/src/ src/COPY --from=builder /build/__pycache__/ src/__pycache__/```## Language-Specific Examples### Python — pip install → copy app → non-root user```dockerfileFROM python:3.12-slim AS builderRUN apt-get update && apt-get install -y --no-install-recommends \   build-essential libpq-dev && rm -rf /var/lib/apt/lists/*WORKDIR /buildCOPY requirements.txt .RUN pip install --no-cache-dir -r requirements.txtCOPY . .RUN python -m compileall -b .FROM python:3.12-slimRUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin appWORKDIR /appCOPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packagesCOPY --from=builder /build/ ./USER appHEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \   CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1CMD ["python", "-m", "gunicorn", "app:app", "--bind", "0.0.0.0:8000"]```### Node.js — npm ci → prune dev deps```dockerfileFROM node:22-alpine AS builderWORKDIR /buildCOPY package*.json ./RUN npm ci --only=productionFROM node:22-alpineRUN addgroup -S app && adduser -S -G app appWORKDIR /appCOPY --from=builder /build/node_modules node_modules/COPY . .RUN npm prune --productionUSER appHEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \   CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1CMD ["node", "dist/server.js"]```## Layer CachingEvery RUN / COPY / ADD instruction creates a cacheable layer. Order them by change frequency — stable first, volatile last — so rebuilds reuse cached layers.```dockerfile# Best (frequent hits)                     # WorstFROM base                                   FROM baseCOPY package*.json ./      <-- slow         COPY . .RUN npm install            <-- slow         RUN npm install    <-- re-runs every timeCOPY . .                  <-- fast```Caching rules:| Instruction        | Change Frequency  | Place Near       ||---
----
----
----
----
-|---
----
----
----
----
|---
----
----
----
---|| `FROM`             | Never             | Top              || `RUN apt-get …`    | Rare (tools)      | After FROM       || `COPY *_lock.json` | Rare (lock file)  | Before source    || `RUN install`      | After lock change | After lock COPY  || `COPY src/`        | Every commit      | Bottom           || `RUN compile`      | Every commit      | After src COPY   |> **Measure:** run `docker build --no-cache-filter=builder .` to invalidate only the builder stage while keeping runtime layer caches intact.## Size Reduction### `.dockerignore`Prevent the build context from bloating the first COPY layer:```dockerignore.git/node_modules/__pycache__/.env**.md*.pycDockerfile.dockerignoredist/coverage/```### Base Image Selection| Base Image          | Size (approx) | Best For                        ||---
----
----
----
----
--|---
----
----
----
|---
----
----
----
----
----
----
----
--|| `ubuntu:24.04`      | 78 MiB        | Maximum compatibility           || `python:3.12-slim`  | 122 MiB       | Python with apt                 || `node:22-alpine`    | 127 MiB       | Node.js (fast install)          || `alpine:3.21`       | 8 MiB         | Go / Rust statically linked     || `gcr.io/distroless/base` | ~15 MiB | Minimal, no shell/packager      |Distroless images contain only the runtime and your binary — no shell, no package manager, no unnecessary tools. This reduces attack surface and image size simultaneously.```dockerfileFROM node:22-alpine AS builderWORKDIR /buildCOPY package*.json ./RUN npm ci --only=productionCOPY . .RUN npm run buildFROM gcr.io/distroless/nodejs22-debian12COPY --from=builder /build/dist/ /app/COPY --from=builder /build/node_modules/ /app/node_modules/CMD ["/app/server.js"]```## Security Hardening| Rule                        | Implementation                                                       ||---
----
----
----
----
----
----
--|---
----
----
----
----
----
----
----
----
----
----
----
----
----
----
----
----
---|| No root user                | `USER app` (create user before switching)                            || Read-only root filesystem   | `docker run --read-only --tmpfs /tmp …`                              || Drop capabilities           | `docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE …`             || HEALTHCHECK                 | Add to every production Dockerfile                                   || Avoid `latest` tag          | Pin to digest or explicit version (`python:3.12-slim@sha256:…`)      || Minimize RUN chains         | Combine `apt-get update && apt-get install` in one layer, clean apt  |```bash# Run with read-only rootfs and minimal capabilitiesdocker run --read-only \   --tmpfs /tmp \   --cap-drop=ALL \   --cap-add=NET_BIND_SERVICE \   my-app:latest```## Verification1. **Check layers:** `docker history <image>` — list each layer and its size; look for unexpectedly large or duplicated layers.2. **Scan for vulnerabilities:** `docker scout quickview <image>` (or `trivy image <image>`).3. **Test user context:** `docker run --rm <image> whoami` must return the non-root user name; a root result means the `USER` directive is missing.4. **Measure size:** `docker images <image>` — compare before/after optimization.5. **Verify build cache reuse:** rebuild after a trivial source change; the compile step should re-run but install steps should hit cache.6. **Read-only test:** `docker run --read-only --tmpfs /tmp <image>` should start and serve requests normally.## Anti-Rationalization Table| Rationalization                                      | Reality                                                     ||---
----
----
----
----
----
----
----
----
----
----
----
----
---|---
----
----
----
----
----
----
----
----
----
----
----
----
----
----
--|| "Alpine is always smaller than slim"                 | `python:3.12-alpine` (88 MiB) vs `python:3.12-slim` (122 MiB) — Alpine wins on size but misses musl compatibility for some wheels || "One big RUN chain is fastest"                       | True at build time, but every change invalidates the entire chain — split by frequency || "Distroless is too hard to debug"                    | Debug with `docker run --entrypoint=sh` on a debug image; swap distroless for slim in dev || "COPY . . at the end doesn't matter for size"       | It matters for build context speed and cache invalidation — always `.dockerignore` || "Multi-stage is only for compiled languages"         | False — Python/Node benefit by not shipping dev deps and compilers || "Security scanning is for production only"           | Scan in CI on every push; catching a CVE before merge saves a hotfix cycle |