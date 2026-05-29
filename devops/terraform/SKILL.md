---
name: terraform
description: Infrastructure as Code with Terraform — HCL, modules, state management, providers, workspaces
---


## Overview

Infrastructure as Code using Terraform's HCL language. Covers modules, remote state, providers, workspaces, and drift detection.

## Capabilities

- HCL resource definitions
- Module creation and registry
- Remote state (S3, GCS, Terraform Cloud)
- Provider configuration
- Workspace management
- Import existing resources
- Plan/apply/destroy lifecycle

## When to Use

- Multi-cloud infrastructure
- Repeatable environment provisioning
- Infrastructure version control
- Compliance as code

## Pseudo Code

The terraform workflow follows a standard pipeline pattern.

Core flow:
```
# terraform primary flow
input = prepare(raw_data)
result = process(input, config={code, infrastructure, management, modules, providers})
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


### EC2 Instance
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
  tags = { Name = "WebServer" }
}

terraform {
  backend "s3" { bucket = "my-tf-state" key = "prod/terraform.tfstate" }
}
```

## Common Patterns

- Remote state with locking
- Use modules for reusability
- terraform plan before apply
- Workspaces for environments
- Import existing resources

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
