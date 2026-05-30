---
name: ci-cd-pipeline
description: CI/CD pipeline design with GitHub Actions, GitLab CI — build, test, deploy automation. Use when setting up CI/CD pipelines or automating deployments.
---


## Overview

CI/CD pipeline design with GitHub Actions, GitLab CI — build, test, deploy automation. Use when setting up CI/CD pipelines or automating deployments.

## Capabilities

- Workflow syntax and job dependencies
- Caching strategies
- Secrets management
- Deployment strategies (blue-green, canary)
- Matrix builds for multi-env testing

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
| Pipeline fails on deploy | Missing environment variables | Validate all env vars before deploy step |
| Build cache miss | Cache key changed or expired | Use consistent cache keys with lockfile hash |
| Secret not found | Wrong context or environment | Verify secret is in correct context/environment |
| Matrix build inconsistency | Different runner versions | Pin runner images and tool versions |

## Additional Resources

- Review the 1ai-skills repository for related devops skills
- Check the references/ directory for checklists and templates
- Join the community for best practices and support
- Contribute improvements via pull requests

## Verification

- Pipeline executes end-to-end on a clean branch with no cached artifacts
- All secret references resolve correctly in every environment (staging and production)
- Deployment rollback completes within the documented RTO target
- Matrix builds pass on all specified OS and runtime version combinations
- Build artifacts are reproducible when rebuilt from the same commit SHA
