---
name: product-team
description: Use when orchestrating product development workflows - building, shipping, QA, and deployment coordination.
---

# product-team Orchestrator

## What It Does

Orchestrates product development - building, shipping, and maintaining products. Coordinates development workflows, QA, and deployment.

## When to Use

- Build new features
- Ship products
- Deploy updates
- Run development workflows
- Maintain code quality

## Team Members (Skills)

| Skill | Role |
|-------|------|
| subagent-driven-development | Multi-agent development |
| finishing-a-development-branch | Merge and release |
| verification-before-completion | Quality assurance |
| systematic-debugging | Issue resolution |
| test-driven-development | Quality-first development |

## Workflows

### Feature Development

```
1. Plan: Use writing-plans to create implementation plan
2. Develop: Use subagent-driven-development to build
3. Test: Use test-driven-development for quality
4. Review: Use requesting-code-review for feedback
5. Verify: Use verification-before-completion to validate
6. Finish: Use finishing-a-development-branch to merge
```

### Bug Fix

```
1. Diagnose: Use systematic-debugging to find root cause
2. Fix: Implement solution
3. Test: Verify fix works
4. Review: Get code review
5. Deploy: Merge and release
```

### Product Launch

```
1. Plan: Create launch plan
2. Build: Coordinate development
3. Test: QA all features
4. Review: Final approval
5. Deploy: Ship to production
6. Monitor: Track launch metrics
```

## Trigger Phrases

- "build feature"
- "ship product"
- "develop"
- "product"
- "deploy"
- "release"

## Coordination Pattern

When triggered, the orchestrator:
1. Understands product requirements
2. Creates development plan
3. Coordinates development tasks
4. Ensures quality gates pass
5. Manages deployment
6. Monitors post-launch

## Quality Gates

- All tests passing
- Code review approved
- Verification complete
- Deployment successful
- Monitoring in place
