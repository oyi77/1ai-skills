#!/usr/bin/env python3
"""
Phone Farm — Stripe Billing Integration

Usage-based billing with Stripe metered billing.
Gracefully degrades if Stripe is unavailable.
"""

import json
import os
import time
import threading

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
STRIPE_API_BASE = "https://api.stripe.com/v1"

_price_per_api_call = 0.001
_price_per_task = 0.01

_stripe_available = False
_stripe_checked = False


def _check_stripe():
    global _stripe_available, _stripe_checked
    if _stripe_checked:
        return _stripe_available
    _stripe_checked = True
    _stripe_available = bool(STRIPE_SECRET_KEY)
    return _stripe_available


def is_available() -> bool:
    return _check_stripe()


def create_stripe_customer(
    tenant_id: str, email: str = "", name: str = ""
) -> str | None:
    if not is_available():
        return None
    try:
        import urllib.request

        data = json.dumps(
            {"email": email, "name": name, "metadata": {"tenant_id": tenant_id}}
        ).encode()
        req = urllib.request.Request(
            f"{STRIPE_API_BASE}/customers",
            data=data,
            headers={
                "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
        return result.get("id")
    except Exception:
        return None


def report_usage(tenant_id: str, api_calls: int = 0, tasks: int = 0):
    if not is_available():
        return False
    try:
        import urllib.request

        data = json.dumps(
            {
                "tenant_id": tenant_id,
                "api_calls": api_calls,
                "tasks": tasks,
            }
        ).encode()
        req = urllib.request.Request(
            f"{STRIPE_API_BASE}/usage_reports",
            data=data,
            headers={
                "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
        return True
    except Exception:
        return False


def handle_webhook(payload: dict, sig: str = "") -> dict:
    if not STRIPE_WEBHOOK_SECRET:
        return {"status": "skipped", "reason": "no webhook secret configured"}
    import hmac
    import hashlib

    expected = hmac.new(
        STRIPE_WEBHOOK_SECRET.encode(), sig.encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return {"status": "invalid", "reason": "signature mismatch"}
    event_type = payload.get("type", "")
    if event_type == "invoice.payment_succeeded":
        return {
            "status": "ok",
            "event": "payment_succeeded",
            "amount": payload.get("data", {}).get("object", {}).get("amount"),
        }
    if event_type == "invoice.payment_failed":
        return {
            "status": "ok",
            "event": "payment_failed",
            "amount": payload.get("data", {}).get("object", {}).get("amount"),
        }
    return {"status": "ok", "event": event_type}


def get_billing_info(tenant_id: str) -> dict:
    from usage_tracker import get_total

    total_calls = get_total(tenant_id)
    return {
        "plan": "usage",
        "total_api_calls": total_calls,
        "estimated_cost": total_calls * _price_per_api_call,
        "price_per_api_call": _price_per_api_call,
        "price_per_task": _price_per_task,
        "stripe_configured": is_available(),
    }


if __name__ == "__main__":
    print("Stripe available:", is_available())
    print("Billing info:", get_billing_info("default"))
