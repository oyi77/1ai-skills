---
name: vault-secrets
description: HashiCorp Vault — secrets management, dynamic secrets, encryption, auth methods, policies. Use when working with vault secrets.
domain: devops
tags:
- ci-cd
- devops
- infrastructure
- secrets
- vault
---


## Overview

Vault secures, stores, and controls access to tokens, passwords, certificates, API keys, and other secrets. Supports dynamic secret generation and data encryption.

## Capabilities

- KV secret storage (v1/v2)
- Dynamic database credentials
- Transit encryption (encryption-as-a-service)
- Multiple auth methods (AppRole, Kubernetes, LDAP, OIDC)
- Fine-grained ACL policies
- Audit logging

## When to Use
**Trigger phrases:**
- "vault secrets"
- "HashiCorp Vault — secrets management, dynamic secrets, encryption, auth methods,"


- Application secrets management
- Dynamic short-lived credentials
- Encryption without key management
- Compliance requirements for secret rotation
- Multi-cloud secret access

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The vault-secrets workflow follows a standard pipeline pattern.

Core flow:
```
# vault-secrets primary flow
input = prepare(raw_data)
result = process(input, config={auth, dynamic, encryption, hashicorp, management})
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


### KV Secrets
```bash
# Enable KV v2
vault secrets enable -path=secret kv-v2

# Write secret
vault kv put secret/myapp/config db_password="s3cret" api_key="abc123"

# Read secret
vault kv get secret/myapp/config
vault kv get -field=db_password secret/myapp/config

# Versioning
vault kv get -version=2 secret/myapp/config
vault kv rollback -version=1 secret/myapp/config
```

### Dynamic Database Credentials
```bash
# Enable database secrets
vault secrets enable database

# Configure connection
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db:5432/postgres" \
  allowed_roles="readonly" \
  username="vault" \
  password="vault_pass"

# Create role
vault write database/roles/readonly \
  db_name=postgres \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Get credentials
vault read database/creds/readonly
```

### AppRole Auth (for CI/CD)
```bash
# Enable AppRole
vault auth enable approle

# Create role
vault write auth/approle/role/ci \
  secret_id_ttl=10m \
  token_policies="app-policy" \
  token_ttl=1h \
  token_max_ttl=4h

# Get Role ID
vault read auth/approle/role/ci/role-id

# Get Secret ID
vault write -f auth/approle/role/ci/secret-id

# Login
vault write auth/approle/login role_id="xxx" secret_id="yyy"
```

### Policy
```hcl
# policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}
path "database/creds/readonly" {
  capabilities = ["read"]
}
```

## Common Patterns

- **Sidecar injection**: Vault Agent injects secrets into pods
- **Transit encryption**: encrypt/decrypt without storing data
- **Auto-unseal**: use cloud KMS for automatic unsealing
- **Namespaces**: multi-tenant secret isolation

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