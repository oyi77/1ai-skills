#!/usr/bin/env python3
"""Regression tests for the UserPromptSubmit role-router hook.

Run: python3 scripts/test_skill_router_hook.py
Uses Node to exercise the real hooks/skill-router-prompt.js contract.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "skill-router-prompt.js"

CASES = [
    ("production is down and payment gateway failing", "role-incident-commander"),
    ("a journalist sent a press inquiry about the outage", "role-crisis-communications"),
    ("we received a GDPR data export request", "role-legal-counsel"),
    ("cash runway is down to two months", "role-cfo"),
    ("the board wants a strategy update", "role-ceo"),
    ("an employee filed a harassment complaint", "role-people-operations"),
    ("AWS renewal has a 40 percent price increase", "role-vendor-and-partnerships"),
    ("I have an idea for a new product line", "role-owner-idea-intake"),
    ("record the decision in the decision log", "role-owner-decision-log"),
    ("get all departments into this stakeholder discussion", "role-multi-department-brainstorm"),
    ("fix the Python traceback in the parser", "role-software-engineer"),
    ("implement a pytest for the payment service", "role-software-engineer"),
    ("debug the Docker deployment", "role-software-engineer"),
    ("the database is returning 500 errors", "role-incident-commander"),
    ("we got hacked and customer data is leaking", "role-incident-commander"),
    ("the CEO tweeted an offensive statement", "role-crisis-communications"),
    ("review the contract terms and NDA", "role-legal-counsel"),
    ("approve the budget cut", "role-cfo"),
    ("the team is burning out and morale is low", "role-people-operations"),
    ("our strategic partner wants exclusivity", "role-vendor-and-partnerships"),
    ("should we build something like Notion", "role-owner-idea-intake"),
    ("write up the verdict in the audit trail", "role-owner-decision-log"),
    ("brainstorm across teams about the launch", "role-multi-department-brainstorm"),
]

NO_ROUTE = [
    "what is the weather tomorrow",
    "tell me a joke",
    "summarize this paragraph",
    "translate hello into Indonesian",
    "what is two plus two",
    "explain photosynthesis",
]


def route(prompt: str) -> dict:
    proc = subprocess.run(
        ["node", str(HOOK)],
        input=json.dumps({"prompt": prompt}),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=8,
        check=True,
    )
    return json.loads(proc.stdout or "{}")


def main() -> int:
    for prompt, expected in CASES:
        out = route(prompt)
        msg = out.get("systemMessage", "")
        assert expected in msg, f"{prompt!r}: expected {expected}, got {out!r}"
        assert msg.startswith("1ai-skills role detected:"), msg
        assert "Load skill:" in msg, msg

    for prompt in NO_ROUTE:
        out = route(prompt)
        assert out == {}, f"{prompt!r}: expected silent {{}} got {out!r}"

    # Contract edge cases: empty, malformed, and oversized input never crash.
    assert route("") == {}
    assert route("not-json-shaped user input") == {}
    assert isinstance(route("x" * 70000), dict)
    print(f"ALL ROUTER HOOK CHECKS PASSED ({len(CASES)} routed, {len(NO_ROUTE)} silent, 3 edge)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
