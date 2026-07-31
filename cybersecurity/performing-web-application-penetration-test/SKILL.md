---
name: performing-web-application-penetration-test
description: Performs systematic security testing of web applications following the OWASP Web Security Testing Guide (WSTG)
  methodology to identify vulnerabilities in authentication, authorization, input validation, session management, and business
  logic. The tester uses Burp Suite as the primary interception proxy alongside manual testing techniques to find flaws that
  automated scanners miss.
domain: cybersecurity
tags:
- web-application-pentest
- OWASP
- Burp-Suite
- WSTG
- application-security
- money
subdomain: penetration-testing
version: 1.1.0
author: oyi77
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
---
# Performing Web Application Penetration Test

## Overview

Web application penetration testing is the #1 billable cybersecurity service for independent consultants. Every business with a website, SaaS product, or internal web app is a potential client — and most of them know they need testing but don't know where to start.

This skill follows the OWASP Web Security Testing Guide (WSTG) methodology and covers the full engagement lifecycle: scoping, reconnaissance, automated scanning, manual exploitation, and professional reporting. You deliver a vulnerability assessment that translates technical findings into business risk the client can act on.

## When to Use
**Trigger phrases:**
- "performing web application penetration test"
- "Performs systematic security testing of web applications following the OWASP Web"
- "web app pentest"
- "test my website for vulnerabilities"
- "security audit for our SaaS"

**Use cases:**
- Testing web applications before production deployment to identify exploitable vulnerabilities
- Conducting compliance-driven security assessments (PCI-DSS requirement 6.6, SOC 2 Type II)
- Validating remediation of previously identified web application vulnerabilities during retesting
- Assessing third-party web applications before integration into the organization's environment
- Evaluating custom-developed web applications where automated scanning alone is insufficient

**Do not use** against web applications without written authorization, against production systems during peak traffic hours without explicit approval, or for denial-of-service testing of web infrastructure.

## When NOT to Use

- When you lack proper authorization (signed Statement of Work)
- For production systems during peak hours without explicit change window approval
- When the client needs a full red-team engagement or source code audit instead
- When the application uses protocols you haven't validated (e.g., thick client binaries, non-HTTP services)

## Money-Making Overview

**Buyer Persona:** Small-to-medium business owners (10-200 employees), startup CTOs, e-commerce operators, agencies that build client websites, SaaS founders preparing for compliance certification.

These buyers know they need a pentest but:
- Can't afford $15K-50K enterprise vendors (Rapid7, CrowdStrike)
- Don't know the difference between a vulnerability scan and a real pentest
- Want a simple answer: "Is my app safe? What do I fix first?"
- Usually need a report for compliance (PCI, SOC 2, ISO 27001) or a customer questionnaire

**Pricing Model (USD):**

| Tier | What They Get | Price | Delivery |
|------|-------------|-------|----------|
| **Basic** — Quick Scan | Automated OWASP Top 10 scan, 1-page executive summary, CSV of findings | $500-1,000 | 2-3 days |
| **Pro** — Standard Pentest | Full manual WSTG-based testing (auth, session, injection, logic), verified findings with PoC, PDF report with exec summary and fix guidance | $1,500-3,000 | 5-10 days |
| **Enterprise** — Deep Dive | Pro scope + business logic testing, API/GraphQL testing, retest of all findings, 30-day ticket-based remediation support, 1-hour closeout call | $3,000-5,000 | 10-15 days |

**First-Dollar Timeline:** You can close a Basic engagement within 48 hours of your first outreach. Pro and Enterprise deals close in 1-2 weeks. Price for Indonesia/SE Asia at 60-70% of US rates and you outcompete every local firm.

## Prerequisites

- Signed statement of work (SoW) defining the target application URLs, environments (staging/production), and testing boundaries
- Burp Suite Professional license with up-to-date extensions (Active Scan++, Autorize, JSON Beautifier, Logger++)
- Valid test accounts at each privilege level (unauthenticated, standard user, administrator) for authorization testing
- Application documentation including API specifications (OpenAPI/Swagger), sitemap, and technology stack details
- Browser configured with Burp Suite proxy (FoxyProxy recommended) and Burp CA certificate installed
- Python 3.8+ with `requests`, `fpdf2`, `urllib3` for automated scan scripts

## Workflow

### 1. Reconnaissance & Scope Validation
- Map the entire application manually: walk through every feature, form, API call, and user flow
- Identify hidden endpoints, debug pages, admin panels via directory brute-force (ffuf, dirb)
- Fingerprint the tech stack using Wappalyzer, WhatWeb, or manual response header analysis
- Confirm scope boundaries with the client — any subdomain or API not in scope = out of scope

### 2. Automated Scanning (Phase 1)
- Run authenticated Burp Active Scan against all in-scope pages and APIs
- Run a second scanner (ZAP, Nikto, nuclei) from a different vantage point
- Cross-reference scanner findings; discard false positives immediately
- Export raw findings into a working spreadsheet

### 3. Manual OWASP WSTG Testing
For each finding from the scan and each category below, test manually:

| WSTG Category | Key Checks |
|---------------|------------|
| **Authentication** | Credential stuffing, weak password policy, 2FA bypass, forgot-password flaws, session fixation |
| **Authorization** | IDOR (object IDs in URLs/params), privilege escalation, forced browsing, missing function-level checks |
| **Input Validation** | SQL injection (reflected, blind, time-based), XSS (reflected, stored, DOM), command injection, SSRF |
| **Session Management** | Cookie attributes (Secure/HttpOnly/SameSite), session timeout, token predictability, CSRF |
| **Business Logic** | Workflow bypass, rate limiting gaps, race conditions, parameter tampering, coupon/pricing manipulation |
| **Data Exposure** | Sensitive data in URLs, debug endpoints leaking PII, verbose error messages, insecure direct object references |
| **API Security** | GraphQL introspection enabled, mass assignment, broken object-level authorization (BOLA), missing rate limiting |

### 4. Validation & Retesting
- Re-test every finding to confirm it is exploitable (no theoreticals)
- Capture proof-of-concept screenshots or request/response pairs for each confirmed finding
- Attempt to chain low-severity findings into higher-impact attack scenarios
- Test any fix the client deploys during the engagement window

### 5. Report Writing
- Structure findings by business risk (Critical/High/Medium/Low/Info)
- Each finding must include: title, OWASP/WSTG reference, CVSS 3.1 score, affected URL, description, PoC evidence, remediation recommendation
- Write the executive summary last — it must stand alone for a non-technical reader

## First Action in 60 Minutes

Run this script to deliver your first OWASP Top 10 quick scan. Point it at any target URL and it produces a client-ready PDF report — you can deliver this as a Basic tier engagement immediately.

```bash
pip install requests fpdf2 urllib3
```

```python
#!/usr/bin/env python3
"""web_pentest_quick.py — OWASP Top 10 Quick Scan + PDF Report Generator

Usage: python web_pentest_quick.py https://target.com

Produces: pentest-report-<target>.pdf
"""
import sys, json, socket, ssl, datetime
from urllib.parse import urlparse
import requests
from fpdf import FPDF

# Disable SSL warnings for testing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QuickPentest:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.domain = urlparse(base_url).netloc
        self.report = {
            "target": base_url,
            "scanned_at": datetime.datetime.utcnow().isoformat(),
            "findings": [],
            "recommendations": [],
            "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
        }
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 15

    def _add_finding(self, title, severity, description, evidence, remediation):
        self.report["summary"][severity.lower()] += 1
        self.report["findings"].append({
            "title": title, "severity": severity,
            "description": description,
            "evidence": evidence[:500],  # truncate
            "remediation": remediation,
        })

    # === Security Header Checks (A6:2021 – Security Misconfiguration) ===
    def check_security_headers(self):
        try:
            r = self.session.get(self.base_url)
            headers = r.headers
            checks = [
                ("Strict-Transport-Security", "Missing HSTS header — exposes users to downgrade attacks",
                 "Add `Strict-Transport-Security: max-age=31536000; includeSubDomains`"),
                ("X-Frame-Options", "Missing clickjacking protection",
                 "Add `X-Frame-Options: DENY` or `SAMEORIGIN`"),
                ("X-Content-Type-Options", "Missing MIME-sniffing protection",
                 "Add `X-Content-Type-Options: nosniff`"),
                ("Content-Security-Policy", "No CSP header — XSS risk is higher",
                 "Implement a Content-Security-Policy header restricting script sources"),
                ("X-XSS-Protection", "Missing XSS filter header",
                 "Add `X-XSS-Protection: 1; mode=block`"),
            ]
            for header, desc, fix in checks:
                if header not in headers:
                    self._add_finding(f"Missing {header}", "medium", desc, "", fix)
            if "Server" in headers:
                self._add_finding("Server header disclosure", "low",
                    f"Server: {headers['Server']} — reveals technology stack",
                    headers["Server"], "Remove or obfuscate the Server header")
        except Exception as e:
            self._add_finding("Connection failed", "high",
                f"Could not connect to {self.base_url}: {e}", str(e),
                "Verify the target is reachable and responds to HTTP requests")

    # === SSL/TLS Strength (A2:2021 – Cryptographic Failures) ===
    def check_ssl(self):
        try:
            host, port = self.domain, 443
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((host, port), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    ver = ssock.version()
                    cipher = ssock.cipher()
                    if ver and ver.startswith("TLSv1"):
                        sev = "high" if "1.0" in ver or "1.1" in ver else "medium"
                        self._add_finding(f"Weak TLS version: {ver}", sev,
                            f"Server supports {ver} which is deprecated",
                            f"Protocol: {ver}, Cipher: {cipher}", "Disable TLS 1.0/1.1, enforce TLS 1.2+")
        except Exception as e:
            self._add_finding("SSL check failed", "medium",
                f"Could not assess TLS: {e}", str(e), "Verify SSL certificate is valid and port 443 is open")

    # === Common Paths & Endpoints (A1:2021 – Broken Access Control) ===
    def check_common_paths(self):
        common = [
            "/admin", "/.env", "/.git/config", "/wp-admin", "/backup",
            "/robots.txt", "/sitemap.xml", "/crossdomain.xml", "/phpinfo.php",
            "/.well-known/security.txt",
        ]
        for path in common:
            url = f"{self.base_url}{path}"
            try:
                r = self.session.get(url, allow_redirects=False)
                codes = {200: "accessible without auth", 301: "redirects (check destination)",
                         302: "redirects (check destination)", 403: "exists but blocked (403 — may leak info)",
                         401: "exists with auth required"}
                if r.status_code in codes:
                    self._add_finding(f"Sensitive path discovered: {path}", "high" if r.status_code == 200 else "medium",
                        f"{path} returned HTTP {r.status_code} ({codes.get(r.status_code, 'unknown')})",
                        f"GET {url} -> {r.status_code}",
                        f"Restrict access to {path} or remove if unintended")
            except requests.RequestException:
                pass

    # === CORS Misconfiguration (A1:2021 / A7:2021) ===
    def check_cors(self):
        try:
            r = self.session.get(self.base_url, headers={"Origin": "https://evil.com"})
            acao = r.headers.get("Access-Control-Allow-Origin", "")
            if "evil.com" in acao or acao == "*":
                self._add_finding("CORS misconfiguration", "high",
                    f"Origin 'https://evil.com' is reflected in ACAO header",
                    f"Origin sent: https://evil.com, ACAO: {acao}",
                    "Do not reflect untrusted origins. Use an allowlist.")
        except Exception:
            pass

    # === Cookie Security (A4:2021 – Insecure Design) ===
    def check_cookies(self):
        try:
            r = self.session.get(self.base_url)
            for cookie in self.session.cookies:
                issues = []
                attrs = cookie.__dict__
                if not cookie.secure:
                    issues.append("Missing Secure flag")
                if cookie.path and not cookie.has_nonstandard_attr("HttpOnly"):
                    issues.append("Missing HttpOnly flag")
                if not attrs.get("_rest", {}).get("samesite"):
                    issues.append("Missing SameSite attribute")
                if issues:
                    self._add_finding(f"Insecure cookie: {cookie.name}", "medium",
                        f"Cookie '{cookie.name}' has issues: {', '.join(issues)}",
                        f"Cookie: {cookie.name}={cookie.value}", f"Set {', '.join(issues)}")
        except Exception:
            pass

    # === Server Info Leakage (A5:2021 – Security Misconfiguration) ===
    def check_verbose_errors(self):
        test_paths = ["/nonexistent123", "/api/../../etc/passwd"]
        for tp in test_paths:
            try:
                r = self.session.get(f"{self.base_url}{tp}")
                if any(sig in r.text.lower() for sig in ["stack trace", "traceback", "file_get_contents",
                                                          "syntax error", "unexpected t_", "mysql_fetch"]):
                    self._add_finding(f"Verbose error on {tp}", "medium",
                        f"Application leaks internal error details at {tp}",
                        f"HTTP {r.status_code}: snippet visible",
                        "Disable debug output in production. Use generic error pages.")
            except Exception:
                pass

    def run(self):
        print(f"[*] Scanning {self.base_url} ...")
        print("[1/7] Security headers..."); self.check_security_headers()
        print("[2/7] SSL/TLS..."); self.check_ssl()
        print("[3/7] Common endpoints..."); self.check_common_paths()
        print("[4/7] CORS..."); self.check_cors()
        print("[5/7] Cookies..."); self.check_cookies()
        print("[6/7] Error handling..."); self.check_verbose_errors()

        s = self.report["summary"]
        print(f"[7/7] Done. Found: {s['critical']} critical, {s['high']} high, {s['medium']} medium, {s['low']} low, {s['info']} info")
        self._generate_pdf()
        print(f"[+] Report saved: pentest-report-{self.domain}.pdf")

    def _generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", "B", 22)
        pdf.cell(0, 14, "Web Application Security Assessment", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"Target: {self.base_url}", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, f"Date: {self.report['scanned_at'][:10]}", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(8)

        # Executive Summary
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        s = self.report["summary"]
        total = sum(s.values())
        pdf.multi_cell(0, 6,
            f"This report summarizes the automated security scan of {self.base_url}. "
            f"A total of {total} findings were identified. "
            f"Of these, {s['critical'] + s['high']} are high-severity issues requiring immediate attention, "
            f"{s['medium']} are medium-severity, and {s['low']} are low-severity. "
            "A full manual penetration test is recommended to identify business logic, "
            "authentication, and authorization vulnerabilities that automated scanners miss.")
        pdf.ln(4)

        # Finding Summary Table
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Finding Summary", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(30, 7, "Severity", border=1, align="C")
        pdf.cell(30, 7, "Count", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        for sev in ["critical", "high", "medium", "low", "info"]:
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(30, 7, sev.capitalize(), border=1)
            pdf.cell(30, 7, str(s[sev]), border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

        # Detailed Findings
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Detailed Findings", new_x="LMARGIN", new_y="NEXT")
        for i, f in enumerate(self.report["findings"], 1):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(200, 0, 0) if f["severity"] in ("critical", "high") else pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 6, f"#{i} [{f['severity'].upper()}] {f['title']}")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 5, f"Description: {f['description']}", new_x="LMARGIN", new_y="NEXT")
            if f["evidence"]:
                pdf.set_font("Courier", "", 8)
                pdf.multi_cell(0, 5, f"Evidence: {f['evidence']}")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 5, f"Remediation: {f['remediation']}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # Recommendations
        pdf.set_font("Helvetica", "B", 14)
        pdf.add_page()
        pdf.cell(0, 10, "Recommendations", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        if not self.report["findings"]:
            pdf.multi_cell(0, 6, "No significant issues detected by the automated scan. A manual pentest is still recommended.")
        else:
            pdf.multi_cell(0, 6,
                "1. Fix all Critical and High severity findings immediately.\n"
                "2. Schedule a follow-up manual penetration test for business logic and authorization flaws.\n"
                "3. Implement a Content Security Policy to mitigate XSS risk.\n"
                "4. Enforce HTTPS with HSTS across all subdomains.\n"
                "5. Restrict access to administrative and debug endpoints.\n"
                "6. Conduct regular automated scanning (monthly) and manual pentesting (quarterly or before major releases).")

        pdf.output(f"pentest-report-{self.domain}.pdf")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_pentest_quick.py https://target.com")
        sys.exit(1)
    QuickPentest(sys.argv[1]).run()
```

Run it:
```bash
python web_pentest_quick.py https://staging.example.com
```

The script generates `pentest-report-staging.example.com.pdf` — a branded, client-ready PDF containing executive summary, severity breakdown, and per-finding detail. Deliver this as your Basic tier deliverable.

## Deliverable Format

Every engagement produces one file: a professional PDF report. Use this structure for Pro and Enterprise engagements.

**Report Structure:**

1. **Cover Page** — Client name, target URL, assessment date, your company/name, engagement ID
2. **Executive Summary** — 1-page non-technical overview: risk posture, critical findings count, bottom-line recommendation (must stand alone for the CEO)
3. **Scope & Methodology** — URLs in scope, testing dates, OWASP WSTG reference, tools used (Burp Suite, nuclei, custom scripts)
4. **Finding Summary Table** — Severity distribution with counts, CVSS score range
5. **Detailed Findings** — Each finding on 1-2 pages:
   - Title, Severity (Critical/High/Medium/Low/Info), CVSS 3.1 vector & score
   - WSTG reference (e.g., WSTG-ATHN-01)
   - affected URL(s) with HTTP request/response
   - Description of the vulnerability and its business impact
   - Proof of concept (screenshot or request/response pair)
   - Remediation guidance (specific, actionable, prioritized)
6. **Recurring Recommendations** — Comprehensive fix guidance grouped by category (authentication, input validation, configuration, etc.)
7. **Retest Policy** — Terms for one free retest within 30 days of fix completion

**Invoice Template (send with the report):**

```
INVOICE #[ID]

TO: [Client Name]
FROM: [Your Name / Company]
DATE: [Issue Date]
ENGAGEMENT: Web Application Penetration Test — [Target URL]

DESCRIPTION                                     AMOUNT
────────────────────────────────────────────────────────
Web Application Security Assessment             $[Tier Price]
  (Pro tier: manual WSTG-based testing,
   verified findings, PoC evidence,
   and remediation guidance)

Subtotal                                       $[TOTAL]
────────────────────────────────────────────────────────
Payment due within 15 days. Wire / PayPal / Crypto.

Bank: [Optional]
PAYPAL: [Optional]
```

## Verification

- [ ] Signed statement of work and scope confirmation received before testing begins
- [ ] All in-scope pages and APIs enumerated manually — not just crawled
- [ ] Every scanner finding manually validated — no automated false positives in the report
- [ ] Each confirmed finding includes proof-of-concept evidence (request/response pair or screenshot)
- [ ] Executive summary written for a non-technical reader — no jargon
- [ ] Report branded with your company name/logo
- [ ] Report delivered as password-protected PDF (password sent separately)
- [ ] All test data, screenshots, and notes archived for minimum 90 days (client confidentiality agreement applies)
- [ ] Invoice sent with the report
- [ ] Follow-up scheduled: retest window offered (30 days), next engagement proposed (quarterly cadence)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I need OSCP/OSWE first before I can charge for a pentest" | You need one paying client, not one more cert. The cert is education; closing a $1,500 Basic engagement proves you are a consultant. |
| "Burp Suite Pro is too expensive" | Burp Pro is $449/year. Your first Basic engagement pays for 3 years. Use OWASP ZAP (free) until you close your first deal. |
| "The market is saturated with pentesters" | The market is saturated with scan-reporters who dump a DAST output and call it a pentest. Manual analysis + clear remediation advice is rare and commands premium pricing. |
| "I'll undercut on price to get my first client" | Charging $200 attracts the worst clients who argue every finding. Price at $1,500+ and you attract serious business owners who value the report. |
| "What if I miss something critical?" | You are a consultant, not an insurance policy. Scope limits liability. Your SoW explicitly states this is a point-in-time assessment and does not guarantee finding all vulnerabilities. |
| "I don't have a fancy report template" | The script above generates a professional PDF. Your first client doesn't care about your template — they care about knowing what to fix. |
| "Clients only want credentialed testers with insurance" | 80% of SME buyers have never hired a pentester. They want someone who explains risk in business terms. Insurance matters at enterprise scale, not for your first 20 clients. |
