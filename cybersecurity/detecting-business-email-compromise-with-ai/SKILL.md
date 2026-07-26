---
name: detecting-business-email-compromise-with-ai
description: "Quick reference for AI/ML-powered BEC detection — NLP models, behavioral baselines, and automated classification. Use when detecting business email compromise with ai."
domain: cybersecurity
tags: [bec, ai, nlp, email-security, phishing, machine-learning]
version: 1.1.0
---

# Quick Reference: AI-Powered BEC Detection

> **Full BEC detection workflow**: See `../detecting-business-email-compromise/SKILL.md` for comprehensive detection including rule-based, behavioral, and financial controls. This page focuses specifically on AI/ML-based detection techniques.

## Overview

Business Email Compromise (BEC) attacks often contain no malicious links or attachments — they rely purely on social engineering language, making traditional signature-based detection ineffective. AI/ML detection uses transformer-based NLP models (BERT, RoBERTa) and behavioral baselines to identify impersonation, urgency manipulation, and anomalous request patterns. Modern AI detectors achieve 95-98% accuracy on BEC classification, a 25%+ improvement over keyword-only rules.

## When to Use

- You need to detect BEC attacks that contain no malicious URLs, attachments, or known IOCs
- You're deploying NLP-based email analysis to catch sophisticated impersonation
- You want to build behavioral baselines per user to detect anomalous sending patterns
- You need to reduce false positives from rule-heavy email security filters

## Quick Start

1. **Train a classifier** — Fine-tune a lightweight transformer (distilBERT) on a corpus of BEC vs. legitimate email samples; focus on urgency language, sender-role mismatch, and payment-request patterns
2. **Deploy behavioral baselines** — Profile each user's typical senders, communication frequency, and writing style over a 48-hour historical window; flag deviations
3. **Configure response actions** — Auto-quarantine confidence scores >90%, add warning banners for 70-90%, route 50-70% to SOC analyst queue, and feed all verdicts back as training data

## Code Example: NLP BEC Score Classifier

```python
import re, json
from typing import Optional

# Lightweight BEC scoring — no GPU required.
# For production, replace with a fine-tuned transformer (distilBERT).

BEC_SIGNALS = {
    "urgency": r"\b(urgent|immediately|asap|time.?sensitive|today|now|deadline)\b",
    "payment": r"\b(wire|transfer|pay|payment|invoice|ach|bank|account.?number)\b",
    "secrecy": r"\b(confidential|private|do not discuss|secret|discreet?)\b",
    "impersonation": r"\b(ceo|president|director|owner|founder|attorney|legal)\b",
    "auth_change": r"\b(update.?payment|change.?bank|new.?account|routing)\b",
    "blocked_domain": r"\b(gmail\.com|yahoo\.com|aol\.com|outlook\.com)\b",
}

def score_bec(email_subject: str, email_body: str, display_name: str,
              sender_domain: str, known_domain: str) -> dict:
    """
    Score an email for BEC indicators. Returns confidence 0-1 and signal breakdown.
    In production, replace with a transformer model fine-tuned on your email corpus.
    """
    text = f"{email_subject} {email_body}".lower()
    domain_mismatch = sender_domain != known_domain
    signals = {}
    total_score = 0.0

    for signal_name, pattern in BEC_SIGNALS.items():
        matches = re.findall(pattern, text)
        if matches:
            signals[signal_name] = len(matches)
            total_score += min(len(matches) * 0.15, 0.6)

    if domain_mismatch:
        signals["domain_mismatch"] = 1
        # Heavier weight when VIP display name from external domain
        is_vip_display = any(w in display_name.lower()
                             for w in ["ceo", "cf0", "vp", "president", "founder"])
        total_score += 0.4 if is_vip_display else 0.2

    confidence = min(total_score, 1.0)

    return {
        "confidence": round(confidence, 3),
        "verdict": "block" if confidence > 0.9
                    else ("warn" if confidence > 0.7
                          else ("review" if confidence > 0.5 else "pass")),
        "signals": signals,
        "domain_mismatch": domain_mismatch
    }

# Example:
# result = score_bec(
#     email_subject="URGENT: Wire transfer needed TODAY",
#     email_body="Please transfer $50,000 to the attached invoice immediately. Confidential.",
#     display_name="CEO John Smith",
#     sender_domain="ceo-johnsmith.ru",
#     known_domain="company.com"
# )
# print(json.dumps(result, indent=2))
# → {"confidence": 1.0, "verdict": "block", "signals": {...}, "domain_mismatch": true}
```

## Verification Checklist

- [ ] NLP classifier achieves >90% precision on BEC test corpus (benchmark against known BEC dataset)
- [ ] Behavioral baselines are established per user over a minimum 48-hour window
- [ ] Confidence thresholds are tuned to minimize SOC fatigue (aim for <5 false positives/1000 emails)
- [ ] AI verdicts are fed back as training data for continuous model improvement (closed-loop)
- [ ] Domain mismatch detection catches lookalike domains (e.g., `company.co` vs `company.com`)
- [ ] Writing-style anomaly detection identifies account compromise even without domain mismatch
- [ ] False positive rate is measured weekly and compared against keyword-only baseline (target 25%+ improvement)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "AI will catch all BEC automatically, no tuning needed" | Out-of-the-box models miss industry-specific language and produce 20-30% false positives. Fine-tune on your email corpus and tune confidence thresholds per department. |
| "Rule-based filters are enough for BEC" | Pure social-engineering BEC contains zero malicious indicators. Only NLP/behavioral AI can detect requests that look legitimate on the surface but deviate from normal communication patterns. |
| "One model fits all — train once, deploy everywhere" | BEC language varies by industry (finance vs healthcare vs manufacturing), region, and organizational culture. Retrain quarterly on your specific email flows. |
| "High confidence = always block" | Even 95% confidence means 5 in 100 legitimate emails may be blocked. Use graduated responses: block >90%, warn 70-90%, flag 50-70%. |

## Workflow
Redirected to parent skill at `../detecting-business-email-compromise/SKILL.md`.
