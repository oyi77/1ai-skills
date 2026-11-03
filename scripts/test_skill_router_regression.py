#!/usr/bin/env python3
"""Regression check for skill router targeting and external delegation."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from skill_router import route, should_delegate_external


def run_checks() -> None:
    cases = [
        ("audit ai agent operational compliance boundaries", "agent-alignment-audit", False),
        ("create design md specification design tokens", "design-md", False),
        ("unslop vibecoded dashboard purple gradient", "unslop", False),
        ("evaluate agent reliability pass at k", "eval-harness", False),
        ("auto consolidate skills demote", "auto-consolidator", False),
        ("evolve skills from usage patterns", "auto-evolver", False),
        ("api key leak validation security", "api-key-leak-validation", False),
        ("debug agent stuck failing loop", "agent-debug-loop", False),
        ("test coverage pytest", "test-coverage-analyzer", False),
        ("security audit pentest", "cloudflare-security-audit", False),
        ("build pages consistent brand tokens design md", "design-md", False),
        ("quantum physics plasma confinement fusion", None, True),
        ("totally unregistered madeup capability", None, True),
    ]

    # Known accepted ambiguity: 'adhd design brainstorming' ranks generic
    # 'design' first (name part +50 + tag overlap), with 'adhd' at rank 3.
    # Pin adhd INSIDE top-3 (not rank 1) so future weight changes that drop
    # it entirely are caught, without over-fitting the exact order.
    amb = route("adhd design brainstorming", top=5)
    amb_names = [r["name"] for r in amb]
    assert "adhd" in amb_names[:3], (
        f"'adhd' fell out of top-3 for 'adhd design brainstorming': {amb_names}"
    )
    assert "design" in amb_names[:3], (
        f"'design' fell out of top-3 for 'adhd design brainstorming': {amb_names}"
)


    # Design-skill recall regression cases (added after trigger backfill).
    # 'revamp' previously returned zero results; must now return >=1.
    _rev = route("revamp", top=5)
    assert _rev, f"'revamp' returned no results: {_rev}"

    _rdlp = route("redesign the landing page", top=5)
    _rdlp_names = [r["name"] for r in _rdlp]
    assert any(n in _rdlp_names[:3] for n in ("hallmark", "unslop", "impeccable", "frontend-design")), (
        f"none of hallmark/unslop/impeccable/frontend-design in top-3 for 'redesign the landing page': {_rdlp_names}"
    )

    _rdui = route("redesign ui", top=5)
    _rdui_names = [r["name"] for r in _rdui]
    assert any(n in _rdui_names[:3] for n in ("unslop", "anti-slop-frontend", "impeccable", "ui-ux-pro-max")), (
        f"none of unslop/anti-slop-frontend/impeccable/ui-ux-pro-max in top-3 for 'redesign ui': {_rdui_names}"
    )

    _wca = route("wcag contrast audit", top=5)
    _wca_names = [r["name"] for r in _wca]
    assert "accessibility-audit" in _wca_names[:3], (
        f"'accessibility-audit' not in top-3 for 'wcag contrast audit': {_wca_names}"
    )

    _dt = route("design tokens", top=5)
    _dt_names = [r["name"] for r in _dt]
    assert any(n in _dt_names[:3] for n in ("design-tokens", "theme-factory")), (
        f"neither design-tokens nor theme-factory in top-3 for 'design tokens': {_dt_names}"
    )

    _rml = route("responsive mobile layout", top=5)
    _rml_names = [r["name"] for r in _rml]
    assert "responsive-design" in _rml_names[:3], (
        f"'responsive-design' not in top-3 for 'responsive mobile layout': {_rml_names}"
    )

    # 'refund request' must not surface a cybersecurity skill above the
    # customer-support cluster. Before the three-tier sort, the word
    # 'request' in an HTTP-smuggling description scored 18.5 and outranked
    # the 12.0-floored support cluster.
    _rf = route("refund request", top=10)
    _rf_names = [r["name"] for r in _rf]
    _support_idx = [
        i for i, r in enumerate(_rf)
        if "customer-support" in (r.get("roles") or [])
    ]
    assert _support_idx, f"no customer-support role skills for 'refund request': {_rf_names}"
    _first_cyber = next(
        (i for i, r in enumerate(_rf) if r.get("category") == "cybersecurity"), None
    )
    assert _first_cyber is None or _first_cyber > max(_support_idx[:3]), (
        f"cybersecurity outranks customer-support cluster for 'refund request': "
        f"{[(r['score'], r['name']) for r in _rf]}"
    )

    for query, expected_name, expected_delegate in cases:
        results = route(query, top=5)
        delegate = should_delegate_external(results, threshold=30.0)
        assert delegate == expected_delegate, (
            f"Query {query!r}: expected delegate={expected_delegate}, got {delegate} (score={results[0]['score'] if results else 0})"
        )
        if expected_name is not None:
            assert results, f"Query {query!r} returned no results"
            actual_name = results[0]["name"]
            assert actual_name == expected_name, (
                f"Query {query!r}: expected {expected_name}, got {actual_name} (score={results[0]['score']})"
            )

    print("ALL ROUTER REGRESSION CHECKS PASSED")


if __name__ == "__main__":
    run_checks()
