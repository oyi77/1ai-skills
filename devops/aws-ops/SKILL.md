---
name: aws-ops
description: AWS operations — EC2, S3, Lambda, RDS, ECS, IAM, CloudFormation. Infrastructure and cost optimization
---

## Overview

AWS infrastructure management covering core services (EC2, S3, Lambda, RDS), IAM security, CloudFormation IaC, and cost optimization strategies.

## Capabilities

- EC2 instance management and auto-scaling
- S3 bucket policies and lifecycle
- Lambda function deployment
- IAM policy design
- CloudFormation templates
- Cost optimization (Spot, Reserved, Savings Plans)
- CloudWatch monitoring

## When to Use

- Cloud infrastructure management
- Web application hosting
- Data processing pipelines
- Cost optimization reviews

## Pseudo Code

### CloudFormation EC2
```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0abcdef1234567890
      SecurityGroupIds: [!Ref WebSG]
      Tags:
        - Key: Name
          Value: WebServer
```

## Common Patterns

- Tag everything for cost tracking
- Use IAM roles, not access keys
- Enable CloudTrail for audit
- S3 lifecycle rules for cost
