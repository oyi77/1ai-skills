---
name: vault-secrets
description: HashiCorp Vault — secrets management, dynamic secrets, encryption, auth methods, policies
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

- Application secrets management
- Dynamic short-lived credentials
- Encryption without key management
- Compliance requirements for secret rotation
- Multi-cloud secret access

## Pseudo Code

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
