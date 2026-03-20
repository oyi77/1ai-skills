#!/usr/bin/env python3
"""Multi-Agent Team Router - routes messages to domain-specialized agents via OmniRoute."""
import json, sys, os
from urllib.request import Request, urlopen

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"

DOMAIN_KEYWORDS = {
    "strategy": ["revenue", "plan", "vision", "roadmap", "goal", "okr", "quarter", "strategi"],
    "dev": ["code", "bug", "build", "api", "deploy", "server", "database", "git", "error", "fix"],
    "marketing": ["content", "post", "ads", "tiktok", "instagram", "twitter", "viral", "campaign", "konten"],
    "business": ["cost", "contract", "partner", "invoice", "pricing", "deal", "client", "vendor", "biaya"],
    "trading": ["xauusd", "gold", "polymarket", "trade", "signal", "chart", "emas", "forex", "candle"],
}

SYSTEM_PROMPTS = {
    "strategy": "You are a strategic advisor for a digital business. Focus on revenue growth, product roadmap, and business vision. Respond in the user's language.",
    "dev": "You are a senior software engineer. Help with code, debugging, architecture, and deployment. Be precise and provide code examples when relevant.",
    "marketing": "You are a digital marketing expert specializing in social media, content creation, and viral growth. Focus on actionable tactics for Indonesian and global audiences.",
    "business": "You are a business operations consultant. Help with costs, contracts, partnerships, and vendor management. Be practical and numbers-oriented.",
    "trading": "You are a trading analyst specializing in XAUUSD (gold), forex, and prediction markets. Provide analysis, not financial advice. Include risk disclaimers.",
}


def detect_domain(message):
    """Detect the domain of a message based on keyword matching."""
    message_lower = message.lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > 0:
            scores[domain] = score

    if not scores:
        return "strategy"  # default fallback
    return max(scores, key=scores.get)


def route_to_agent(domain, message):
    """Route message to the appropriate agent via OmniRoute LLM."""
    system_prompt = SYSTEM_PROMPTS.get(domain, SYSTEM_PROMPTS["strategy"])

    payload = json.dumps({
        "model": OMNIROUTE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }).encode()

    req = Request(
        f"{OMNIROUTE_BASE}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OMNIROUTE_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error routing to {domain} agent: {e}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Agent Team Router")
    parser.add_argument("message", nargs="?", help="Message to route")
    parser.add_argument("--domain", help="Force a specific domain instead of auto-detect")
    args = parser.parse_args()

    if not args.message:
        print("Usage: python team_router.py \"your message here\"")
        sys.exit(1)

    domain = args.domain if args.domain else detect_domain(args.message)
    print(f"[Router] Detected domain: {domain}")
    print(f"[Router] Routing to {domain} agent...\n")

    response = route_to_agent(domain, args.message)
    print(response)
