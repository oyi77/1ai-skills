---
name: crypto-breaker
description: Cryptographic attack techniques for breaking implementations, side-channel
  attacks, and exploiting crypto weaknesses. Use when assessing crypto implementations,
  finding side-channel leaks, or breaking custom cryptography.
domain: cybersecurity
---

# Crypto Breaker

Cryptographic bugs are invisible to scanners but devastating in impact. One weak crypto implementation can compromise entire systems. These bugs pay $5k-$100k and most hunters miss them.

## When to Use

- Assessing cryptographic implementations
- Finding side-channel vulnerabilities
- Breaking custom/homegrown cryptography
- Analyzing TLS/SSL configurations
- Testing encryption in transit and at rest
- JWT/token security assessment

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### 1. Crypto Assessment Checklist

```
- [ ] What algorithm is used? (AES, RSA, ECDSA, etc.)
- [ ] What mode of operation? (ECB, CBC, GCM, etc.)
- [ ] How are keys generated? (random, derived, hardcoded?)
- [ ] How are keys stored? (file, env, HSM, hardcoded?)
- [ ] How is IV/nonce generated? (random, predictable, reused?)
- [ ] Is authenticated encryption used? (GCM, CCM, or MAC-then-encrypt?)
- [ ] Are there any custom crypto constructions?
- [ ] How is key rotation handled?
```

### 2. Common Crypto Vulnerabilities

#### ECB Mode
```python
# ECB encrypts identical blocks to identical ciphertext
# Pattern leakage, block rearrangement attacks

# If user input encrypted with ECB:
# Encrypted("admin=true") → block1|block2
# Attacker can rearrange blocks:
# block2|block1 → different plaintext

# Fix: Use CBC, GCM, or CTR mode
```

#### CBC Padding Oracle
```python
# If server reveals padding validity:
# Can decrypt any ciphertext byte-by-byte

# Attack:
# 1. Modify last byte of previous block
# 2. Send modified ciphertext
# 3. If padding valid → guessed byte is correct
# 4. Repeat for each byte

# Tools: PadBuster, PadBuster-ng
```

#### IV/Nonce Reuse
```python
# If same IV/nonce used with same key:
# C1 = P1 XOR keystream
# C2 = P2 XOR keystream
# C1 XOR C2 = P1 XOR P2
# Known plaintext → recover other plaintext

# In AES-GCM:
# Nonce reuse breaks authentication completely
# Can forge arbitrary messages
```

#### Weak Random Number Generation
```python
# Predictable PRNG for crypto:
import random  # NOT cryptographically secure
time.time()    # Predictable seed
Math.random()  # In JavaScript

# Attacks:
# Predict session tokens
# Predict password reset tokens
# Predict encryption keys

# Fix: Use os.urandom(), secrets, crypto.getRandomValues()
```

#### Hardcoded Keys
```python
# Keys in source code
KEY = b"supersecretkey123"
API_KEY = "sk-1234567890abcdef"

# Keys in environment variables (leaked in logs/errors)
# Keys in config files (committed to git)

# Fix: Use key management service (AWS KMS, HashiCorp Vault)
```

### 3. TLS/SSL Attacks

#### Weak Cipher Suites
```bash
# Test with testssl.sh
testssl.sh target.com

# Look for:
# SSLv2, SSLv3 (broken)
# RC4, DES, 3DES (weak)
# NULL, EXPORT ciphers (no encryption)
# CBC ciphers (BEAST, POODLE)

# Fix: TLS 1.2+ with AEAD ciphers (AES-GCM, ChaCha20)
```

#### Certificate Issues
```bash
# Self-signed certificates
# Expired certificates
# Wrong hostname in certificate
# Weak key size (< 2048 bit RSA)
# Weak hash algorithm (SHA-1)

# Fix: CA-signed, valid dates, correct hostname, strong keys
```

### 4. JWT/Token Attacks

#### Algorithm Confusion
```python
# RS256 → HS256 confusion
# Server uses public key to verify HMAC
# Attacker signs with public key as HMAC secret

# Tools: jwt_tool
python3 jwt_tool.py TOKEN -X k -pk public.pem
```

#### Weak Secret
```python
# If JWT signed with weak secret:
# Brute force with common secrets

hashcat -m 16500 jwt.txt wordlist.txt
jwt_tool.py TOKEN -C -d wordlist.txt
```

#### Key Injection
```python
# jwk/jku header injection
# Server fetches key from attacker-controlled URL
# Attacker provides their own key

{"jku": "https://evil.com/jwks.json", "alg": "RS256"}
```

### 5. Password Hashing Issues

```
# Weak algorithms:
MD5, SHA1, SHA256 (too fast, GPU-accelerated cracking)
NTLM (Windows, extremely fast to crack)

# Strong algorithms:
bcrypt (adaptive cost)
scrypt (memory-hard)
Argon2id (winner of Password Hashing Competition)

# Issues:
- No salt (rainbow table attacks)
- Weak salt (predictable)
- Low work factor (fast to crack)
- Using crypto hash instead of KDF
```

### 6. Side-Channel Attacks

#### Timing Attacks
```python
# If comparison takes longer for matching bytes:
# Measure response time for each guess
# Byte-by-byte recovery

# Example: HMAC comparison
if hmac == expected_hmac:  # Vulnerable (early exit)
    
# Fix: constant-time comparison
hmac.compare_digest(hmac, expected_hmac)
```

#### Power Analysis
```
# Measure power consumption during crypto operations
# Differential Power Analysis (DPA)
# Correlation Power Analysis (CPA)

# Requires physical access
# Can extract keys from smartcards, HSMs
```

#### Cache Timing
```
# CPU cache access patterns leak information
# Flush+Reload, Prime+Probe attacks
# Can extract AES keys from co-located VMs

# Requires shared hardware
# Cloud VMs on same physical host
```

### 7. Custom Crypto Attacks

```
# Homegrown crypto is ALWAYS broken
# Look for:
- Custom encryption "algorithms"
- XOR with static key
- Base64 "encryption"
- Simple substitution ciphers
- Custom hash functions
- Modified standard algorithms

# Attack patterns:
- Frequency analysis
- Known plaintext attacks
- Differential cryptanalysis
- Algebraic attacks
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Breaking crypto on production systems
- Extracting private keys without authorization
- Using side-channel attacks on shared infrastructure
- Not reporting crypto vulnerabilities responsibly

## Verification

- Crypto weakness demonstrated with working PoC
- Impact quantified (what can be decrypted/forged?)
- Remediation specific to the crypto library/implementation
- No production keys extracted during testing

## Revenue Potential

| Vulnerability | Payout Range |
|--------------|--------------|
| TLS misconfiguration | $500-$5,000 |
| Padding oracle | $2,000-$10,000 |
| JWT algorithm confusion | $2,000-$10,000 |
| Hardcoded keys | $1,000-$10,000 |
| Weak PRNG | $2,000-$10,000 |
| Side-channel (physical) | $10,000-$100,000 |
| Custom crypto break | $5,000-$50,000 |

## Tools

| Purpose | Tools |
|---------|-------|
| TLS testing | testssl.sh, sslyze, nmap ssl-enum-ciphers |
| JWT | jwt_tool, jwt-cracker, CyberChef |
| Hash cracking | hashcat, john |
| Padding oracle | PadBuster |
| Side-channel | ChipWhisperer |
| General | OpenSSL, Python cryptography lib |

## Practice

- CryptoHack (cryptohack.org)
- Cryptopals challenges
- OverTheWire Krypton
- Natas challenges
