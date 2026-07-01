---
name: tracking-threat-actor-infrastructure
description: Threat actor infrastructure tracking involves monitoring and mapping adversary-controlled assets including command-and-control
  (C2) servers, phishing domains, exploit kit hosts, bulletproof hosting, a. Use when working with tracking threat actor infrastructure.
domain: cybersecurity
subdomain: threat-intelligence
tags:
- threat-intelligence
- cti
- ioc
- mitre-attack
- stix
- infrastructure-tracking
- shodan
- censys
- passive-dns
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
---
# Tracking Threat Actor Infrastructure

## Overview

Threat actor infrastructure tracking involves monitoring and mapping adversary-controlled assets including command-and-control (C2) servers, phishing domains, exploit kit hosts, bulletproof hosting, and staging servers. This skill covers using passive DNS, certificate transparency logs, Shodan/Censys scanning, WHOIS analysis, and network fingerprinting to discover, track, and pivot across threat actor infrastructure over time.


## When to Use
**Trigger phrases:**
- "tracking threat actor infrastructure"
- "Threat actor infrastructure tracking involves monitoring and mapping adversary-c"


- When managing security operations that require tracking threat actor infrastructure
- When improving security program maturity and operational processes
- When establishing standardized procedures for security team workflows
- When integrating threat intelligence or vulnerability data into operations

## Prerequisites

- Python 3.9+ with `shodan`, `censys`, `requests`, `stix2` libraries
- API keys: Shodan, Censys, VirusTotal, SecurityTrails, PassiveTotal
- Understanding of DNS, TLS/SSL certificates, IP allocation, ASN structure
- Familiarity with passive DNS and certificate transparency concepts
- Access to domain registration (WHOIS) lookup services

## Key Concepts

This section covers key concepts for tracking threat actor infrastructure.

- Ensure all prerequisites are met before proceeding
- Follow the documented workflow steps in sequence
- Record results and any anomalies encountered during this phase
### Infrastructure Pivoting
Pivoting is the technique of using one known indicator to discover related infrastructure. Starting from a known C2 IP address, analysts can pivot via: passive DNS (find domains), reverse WHOIS (find related registrations), SSL certificates (find shared certs), SSH key fingerprints, HTTP response fingerprints, JARM/JA3S hashes, and WHOIS registrant data.

### Passive DNS
Passive DNS databases record DNS query/response data observed at recursive resolvers. This allows analysts to find historical domain-to-IP mappings, discover domains hosted on a known C2 IP, and identify fast-flux or domain generation algorithm (DGA) behavior.

### Certificate Transparency
Certificate Transparency (CT) logs publicly record all SSL/TLS certificates issued by CAs. Monitoring CT logs reveals new certificates registered for suspicious domains, helping identify phishing sites and C2 infrastructure before they become active.

### Network Fingerprinting
- **JARM**: Active TLS server fingerprint (hash of TLS handshake responses)
- **JA3S**: Passive TLS server fingerprint (hash of Server Hello)
- **HTTP Headers**: Server banners, custom headers, response patterns
- **Favicon Hash**: Hash of HTTP favicon for server identification

## Workflow

1. **Scope the task** — define objectives, boundaries, and success criteria
2. **Gather information** — collect all necessary data and context before proceeding
3. **Execute the core workflow** — follow the domain-specific steps methodically
4. **Validate results** — verify outputs against expected outcomes or baselines
5. **Document findings** — record results, anomalies, and recommendations
### Step 1: Shodan Infrastructure Discovery

```python
import shodan

api = shodan.Shodan("YOUR_SHODAN_API_KEY")

def discover_infrastructure(ip_address):
    """Discover services and metadata for a target IP."""
    try:
        host = api.host(ip_address)
        return {
            "ip": host["ip_str"],
            "org": host.get("org", ""),
            "asn": host.get("asn", ""),
            "isp": host.get("isp", ""),
            "country": host.get("country_name", ""),
            "city": host.get("city", ""),
            "os": host.get("os"),
            "ports": host.get("ports", []),
            "vulns": host.get("vulns", []),
            "hostnames": host.get("hostnames", []),
            "domains": host.get("domains", []),
            "tags": host.get("tags", []),
            "services": [
                {
                    "port": svc.get("port"),
                    "transport": svc.get("transport"),
                    "product": svc.get("product", ""),
                    "version": svc.get("version", ""),
                    "ssl_cert": svc.get("ssl", {}).get("cert", {}).get("subject", {}),
                    "jarm": svc.get("ssl", {}).get("jarm", ""),
                }
                for svc in host.get("data", [])
            ],
        }
    except shodan.APIError as e:
        print(f"[-] Shodan error: {e}")
        return None

def search_c2_framework(framework_name):
    """Search Shodan for known C2 framework signatures."""
    c2_queries = {
        "cobalt-strike": 'product:"Cobalt Strike Beacon"',
        "metasploit": 'product:"Metasploit"',
        "covenant": 'http.html:"Covenant" http.title:"Covenant"',
        "sliver": 'ssl.cert.subject.cn:"multiplayer" ssl.cert.issuer.cn:"operators"',
        "havoc": 'http.html_hash:-1472705893',
    }

    query = c2_queries.get(framework_name.lower(), framework_name)
    results = api.search(query, limit=100)

    hosts = []
    for match in results.get("matches", []):
        hosts.append({
            "ip": match["ip_str"],
            "port": match["port"],
            "org": match.get("org", ""),
            "country": match.get("location", {}).get("country_name", ""),
            "asn": match.get("asn", ""),
            "timestamp": match.get("timestamp", ""),
        })

    return hosts
```

### Step 2: Passive DNS Pivoting

```python
import requests

def passive_dns_lookup(indicator, api_key, indicator_type="ip"):
    """Query SecurityTrails for passive DNS records."""
    base_url = "https://api.securitytrails.com/v1"
    headers = {"APIKEY": api_key, "Accept": "application/json"}

    if indicator_type == "ip":
        url = f"{base_url}/search/list"
        payload = {
            "filter": {"ipv4": indicator}
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
    else:
        url = f"{base_url}/domain/{indicator}/subdomains"
        resp = requests.get(url, headers=headers, timeout=30)

    if resp.status_code == 200:
        return resp.json()
    return None


def query_passive_total(indicator, user, api_key):
    """Query PassiveTotal for passive DNS and WHOIS data."""
    base_url = "https://api.passivetotal.org/v2"
    auth = (user, api_key)

    # Passive DNS
    pdns_resp = requests.get(
        f"{base_url}/dns/passive",
        params={"query": indicator},
        auth=auth,
        timeout=30,
    )

    # WHOIS
    whois_resp = requests.get(
        f"{base_url}/whois",
        params={"query": indicator},
        auth=auth,
        timeout=30,
    )

    results = {}
    if pdns_resp.status_code == 200:
        results["passive_dns"] = pdns_resp.json().get("results", [])
    if whois_resp.status_code == 200:
        results["whois"] = whois_resp.json()

    return results
```

### Step 3: Certificate Transparency Monitoring

```python
import requests

def search_ct_logs(domain):
    """Search Certificate Transparency logs via crt.sh."""
    resp = requests.get(
        f"https://crt.sh/?q=%.{domain}&output=json",
        timeout=30,
    )

    if resp.status_code == 200:
        certs = resp.json()
        unique_domains = set()
        cert_info = []

        for cert in certs:
            name_value = cert.get("name_value", "")
            for name in name_value.split("\n"):
                unique_domains.add(name.strip())

            cert_info.append({
                "id": cert.get("id"),
                "issuer": cert.get("issuer_name", ""),
                "common_name": cert.get("common_name", ""),
                "name_value": name_value,
                "not_before": cert.get("not_before", ""),
                "not_after": cert.get("not_after", ""),
                "serial_number": cert.get("serial_number", ""),
            })

        return {
            "domain": domain,
            "total_certificates": len(certs),
            "unique_domains": sorted(unique_domains),
            "certificates": cert_info[:50],
        }
    return None


def monitor_new_certs(domains, interval_hours=1):
    """Monitor for newly issued certificates for a list of domains."""
    from datetime import datetime, timedelta

    cutoff = (datetime.utcnow() - timedelta(hours=interval_hours)).isoformat()
    new_certs = []

    for domain in domains:
        result = search_ct_logs(domain)
        if result:
            for cert in result.get("certificates", []):
                if cert.get("not_before", "") > cutoff:
                    new_certs.append({
                        "domain": domain,
                        "cert": cert,
                    })

    return new_certs
```

### Step 4: Infrastructure Correlation and Timeline

```python
from datetime import datetime

def build_infrastructure_timeline(indicators):
    """Build a timeline of infrastructure changes."""
    timeline = []

    for ind in indicators:
        if "passive_dns" in ind:
            for record in ind["passive_dns"]:
                timeline.append({
                    "timestamp": record.get("firstSeen", ""),
                    "event": "dns_resolution",
                    "source": record.get("resolve", ""),
                    "target": record.get("value", ""),
                    "record_type": record.get("recordType", ""),
                })

        if "certificates" in ind:
            for cert in ind["certificates"]:
                timeline.append({
                    "timestamp": cert.get("not_before", ""),
                    "event": "certificate_issued",
                    "domain": cert.get("common_name", ""),
                    "issuer": cert.get("issuer", ""),
                })

    timeline.sort(key=lambda x: x.get("timestamp", ""))
    return timeline
```

## Validation Criteria

- Shodan/Censys queries return infrastructure details for target IPs
- Passive DNS reveals historical domain-IP mappings
- Certificate transparency search finds associated domains
- Infrastructure pivoting discovers new related indicators
- Timeline shows infrastructure evolution over time
- Results are exportable as STIX 2.1 Infrastructure objects

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Performing actions without explicit written authorization from the asset owner
- Testing against production systems without a defined scope and rules of engagement
- Acting on threat intelligence without validating source reliability
- Sharing classified or sensitive indicators without proper handling procedures
- Alerting threat actors to detection capabilities through visible response actions

## Verification

- All steps executed successfully against a test environment before production use
- Output documented with screenshots or logs demonstrating expected behavior
- Results validated against known-good baselines or reference implementations
- Documentation complete enough for another analyst to reproduce findings

## References

- [Shodan API Documentation](https://developer.shodan.io/api)
- [Censys Search API](https://search.censys.io/api)
- [SecurityTrails API](https://securitytrails.com/corp/api)
- [crt.sh Certificate Transparency](https://crt.sh/)
- [PassiveTotal API](https://api.passivetotal.org/api/docs/)
- [JARM Fingerprinting](https://github.com/salesforce/jarm)

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We are too small to be targeted" | Automated attacks target everyone. Size does not matter. |
| "Security slows us down" | A breach slows you down 100x more. Build security in from the start. |
| "We will fix it after launch" | Vulnerabilities in production are exploited within hours. Fix before deploy. |