---
name: terraform-iac
description: Infrastructure as Code with Terraform — providers, modules, state management, workspaces, multi-cloud deployments
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

## Pseudo Code

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
