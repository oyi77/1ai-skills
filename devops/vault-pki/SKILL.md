---
name: vault-pki
description: Vault PKI secrets engine — certificate authority, dynamic certificates, certificate rotation
---

## Overview

HashiCorp Vault PKI secrets engine acts as a certificate authority (CA), issuing dynamic X.509 certificates on demand. Enables short-lived certificates with automatic rotation.

## Capabilities

- Root and intermediate CA generation
- Dynamic certificate issuance with configurable TTL
- Certificate revocation (CRL, OCSP)
- Role-based certificate policies
- Automatic rotation via Consul Template or sidecar
- Cross-signed intermediate CAs

## When to Use

- Need internal PKI without managing a traditional CA
- Want short-lived certificates (hours, not years)
- Microservices need TLS certificates automatically
- Replacing self-signed certificates with a proper CA

## Pseudo Code

### Enable PKI Backend
```bash
# Enable PKI engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write pki/root/generate/internal \
  common_name="My Root CA" \
  ttl=87600h

# Configure URLs
vault write pki/config/urls \
  issuing_certificates="http://vault:8200/v1/pki/ca" \
  crl_distribution_points="http://vault:8200/v1/pki/crl"
```

### Create Role
```bash
vault write pki/roles/web-server \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl=72h \
  key_type=ec \
  key_bits=256
```

### Issue Certificate
```bash
# Request a certificate
vault write pki/issue/web-server \
  common_name="api.example.com" \
  ttl=24h

# Response includes: certificate, private_key, issuing_ca, serial_number
```

### Certificate Rotation Script
```bash
#!/bin/bash
CERT=$(vault write -format=json pki/issue/web-server common_name="api.example.com" ttl=1h)
echo "$CERT" | jq -r '.data.certificate' > /etc/ssl/cert.pem
echo "$CERT" | jq -r '.data.private_key' > /etc/ssl/key.pem
systemctl reload nginx
```

## Common Patterns

- **Short TTL**: Issue 1h-24h certs, automate rotation
- **Intermediate CA**: Create intermediate for signing, keep root offline
- **Consul Template**: Auto-rotate certs with `{{ with secret "pki/issue/..." }}`
- **Vault Agent**: Sidecar that auto-fetches and rotates certs
- **Role constraints**: `allowed_domains`, `allow_bare_domains`, `not_before_duration`
