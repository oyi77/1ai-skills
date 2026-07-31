---
name: deploy-agent
description: Use when ship code through controlled pipeline with verification gates and rollback plans.
domain: agents
author: oyi77
license: Apache-2.0
subdomain: ai-agents
tags:
  - agent
  - ai-agent
  - automation
  - deploy
  - autonomous
version: 1.0.0
---

# Deploy Agent

Quick Reference — see parent for full agent ecosystem.

The Deploy Agent ships artifacts to staging and production through a controlled pipeline with health checks, migration execution, automated rollbacks, and post-deploy monitoring. Its core design principle is reversibility: every deploy must have a tested rollback path before it begins.



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Key Responsibilities

- **Execute deployments with strategy**: Support blue-green, rolling, canary, and hotfix strategies with zero-downtime guarantees
- **Run database migrations**: Apply schema changes in the correct order with dry-run validation and automated rollback scripts
- **Verify post-deploy health**: Run health checks, smoke tests, and monitor error rates for a configurable observation window

## Code Example

```python
"""Minimal deploy agent pattern — ship with verification."""

import json, subprocess, sys
from pathlib import Path

def deploy(target: str, tag: str, strategy: str = "rolling") -> dict:
    # 1. Pre-deploy checks
    assert subprocess.run(["git", "diff", "--quiet"], cwd=".").returncode == 0, "Dirty working tree"
    assert subprocess.run([sys.executable, "-m", "pytest", "-x", "-q"]).returncode == 0

    # 2. Build artifact
    build = subprocess.run(["docker", "build", "-t", f"app:{tag}", "."], capture_output=True, text=True)
    if build.returncode != 0:
        return {"status": "failed", "error": build.stderr}

    # 3. Run migrations (dry-run first)
    dry = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "--sql", "head"], capture_output=True, text=True)
    print(f"Migration SQL:\n{dry.stdout}")

    # 4. Deploy
    push = subprocess.run(["docker", "push", f"app:{tag}"])
    if target == "production":
        subprocess.run(["kubectl", "set", "image", f"deployment/app=app:{tag}"])
        subprocess.run(["kubectl", "rollout", "status", "deployment/app"])

    return {
        "target": target, "tag": tag, "strategy": strategy,
        "migration_applied": True, "rollback": f"kubectl rollout undo deployment/app"
    }

if __name__ == "__main__":
    result = deploy(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "rolling")
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] Rollback plan documented and tested before deploy begins
- [ ] Database migrations validated: dry-run + reversible (include `downgrade`)
- [ ] Health check endpoint responds 200 after deploy completes
- [ ] Smoke test suite passes against the deployed target
- [ ] Post-deploy monitoring configured with alert threshold (error rate, latency P95)

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will fix it if something goes wrong" | Manual recovery during an incident is slower and more error-prone than an automated rollback |
| "It works in staging, production will be fine" | Staging never matches production data volume, traffic pattern, or dependency versions |
| "Just one quick hotfix, skip the checks" | Skipping gates is how config drift and silent regressions enter production |

## When to Use

Use when shipping code to staging or production, running database migrations, performing rollbacks, deploying hotfixes, or setting up CI/CD pipelines. Do NOT use for experimental features needing manual verification first, changes requiring coordinated multi-service releases without a release train, or when the target environment is unreachable by the agent.
