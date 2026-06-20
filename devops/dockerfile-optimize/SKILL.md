---
name: dockerfile-optimize
description: Dockerfile optimization — multi-stage builds, layer caching, security hardening, minimal images. Use when optimizing
  Docker builds or hardening container security.
domain: devops
tags:
- ci-cd
- devops
- docker
- dockerfile
- infrastructure
- optimize
---


## Overview

Dockerfile optimization — multi-stage builds, layer caching, security hardening, minimal images. Use when optimizing Docker builds or hardening container security.

## Capabilities

- Multi-stage builds
- Layer ordering for cache
- .dockerignore patterns
- Non-root user configuration
- Distroless and Alpine base images

## When to Use

- Building and configuring this technology
- Integrating with existing workflows
- Optimizing performance and reliability

## Common Patterns

1. Start with official documentation and examples
2. Follow established community patterns
3. Test in staging before production deployment

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures
## Notes

- This skill integrates with the broader 1ai-skills ecosystem for devops workflows
- Combine with related skills for maximum impact across your pipeline
- Monitor output quality and iterate on configuration based on results
- Keep dependencies up to date for security and performance
- Document custom workflows and configurations for team knowledge sharing
## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Build context too large | Missing .dockerignore | Add .dockerignore excluding node_modules, .git, etc. |
| Layer cache invalidated | File COPY before dependency install | Copy package.json first, install deps, then copy source |
| Permission denied in container | Running as root | Add USER directive with non-root user |
| Image size bloated | Single-stage build | Use multi-stage build, copy only artifacts to final stage |

## Additional Resources

- Review the 1ai-skills repository for related devops skills
- Check the references/ directory for checklists and templates
- Join the community for best practices and support
- Contribute improvements via pull requests

## Verification

- Final image size is at least 50% smaller than a single-stage build of the same application
- `docker history` shows no sensitive files or build tools leaked into the final image layer
- Build cache hit rate exceeds 80% when only application source code changes
- Container runs as a non-root user confirmed by `docker exec whoami`
- All required health check endpoints respond correctly from within the built container
