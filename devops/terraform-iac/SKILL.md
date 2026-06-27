---
name: terraform-iac
description: Infrastructure as Code with Terraform — providers, modules, state management, workspaces, multi-cloud deployments
domain: devops
tags:
- ci-cd
- devops
- iac
- infrastructure
- terraform
---


## Overview

Terraform enables declarative infrastructure management across AWS, GCP, Azure, and 1000+ providers. Use when provisioning cloud resources, managing multi-cloud infrastructure, implementing GitOps workflows, or enforcing infrastructure standards.

## Capabilities

- Define infrastructure in HCL (HashiCorp Configuration Language)
- Manage state with remote backends (S3, GCS, Terraform Cloud)
- Create reusable modules for standardized infrastructure
- Use workspaces for multi-environment deployments
- Import existing resources and detect drift
- Integrate with CI/CD pipelines

## When to Use

- Provisioning new cloud infrastructure
- Migrating from manual to IaC management
- Enforcing infrastructure standards across teams
- Multi-cloud deployments
- Detecting configuration drift

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The terraform-iac workflow follows a standard pipeline pattern.

Core flow:
```
# terraform-iac primary flow
input = prepare(raw_data)
result = process(input, config={cloud, code, deployments, iac, infrastructure})
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


### Basic resource provisioning
```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  tags = { Name = "web-server" }
}
```

### Module pattern
```hcl
# modules/vpc/main.tf
variable "cidr_block" { type = string }
variable "environment" { type = string }

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
  tags = { Environment = var.environment }
}

output "vpc_id" { value = aws_vpc.main.id }

# Usage
module "vpc" {
  source      = "./modules/vpc"
  cidr_block  = "10.0.0.0/16"
  environment = "production"
}
```

### CLI operations
```bash
# Initialize and plan
terraform init
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Detect drift
terraform plan -refresh-only

# Destroy
terraform destroy -target=aws_instance.web
```

### Workspace management
```bash
# Create and switch workspaces
terraform workspace new staging
terraform workspace select production

# List workspaces
terraform workspace list

# Use in config
resource "aws_instance" "web" {
  instance_type = terraform.workspace == "production" ? "t3.large" : "t3.micro"
}
```

### CI/CD integration
```yaml
# GitHub Actions
- name: Terraform Plan
  run: |
    terraform init
    terraform plan -out=tfplan
- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: terraform apply -auto-approve tfplan
```

## Common Patterns

Proven patterns for terraform-iac usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### State management
```
Remote backend (S3/GCS) + state locking (DynamoDB/Consul)
Never commit .tfstate to git
Use separate state files per environment
```

### Module structure
```
modules/
  vpc/
  ecs/
  rds/
  monitoring/
envs/
  dev/main.tf   → calls modules with dev variables
  staging/
  prod/
```

### Security best practices
```
- Use sensitive = true for secrets
- Store secrets in Vault/Secrets Manager, not in tfvars
- Enable state encryption at rest
- Use least-privilege IAM for Terraform execution
- Review plan output before apply
```

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

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |