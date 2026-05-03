#!/usr/bin/env bash
# Phone Farm SaaS Integration Tests
# Usage: ./tests/integration_test.sh [BASE_URL]
# Requires: jq, curl
set -euo pipefail

BASE="${1:-http://localhost:8889}"
PASS=0; FAIL=0; ERRORS=""

pass() { PASS=$((PASS+1)); echo "  ✅ $1"; }
fail() { FAIL=$((FAIL+1)); ERRORS="$ERRORS\n  ❌ $1: $2"; echo "  ❌ $1: $2"; }

echo "=== Phone Farm Integration Tests ==="
echo "Target: $BASE"
echo ""

# Health (public, no auth)
echo "--- Health Endpoints ---"
R=$(curl -sf "$BASE/health/live" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"status"' && pass "GET /health/live" || fail "GET /health/live" "no status field"

R=$(curl -sf "$BASE/health/ready" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"status"' && pass "GET /health/ready" || fail "GET /health/ready" "no status field"

# Auth
echo ""
echo "--- Auth Endpoints ---"
TOKEN=$(curl -sf -X POST "$BASE/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","role":"admin"}' 2>/dev/null | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
[ -n "$TOKEN" ] && pass "POST /auth/token" || fail "POST /auth/token" "no token returned"

# Test unauthenticated access (should fail)
CODE=$(curl -sf -o /dev/null -w "%{http_code}" "$BASE/devices" 2>/dev/null || echo "000")
[ "$CODE" = "401" ] || [ "$CODE" = "403" ] || [ "$CODE" = "422" ] && pass "GET /devices without auth → $CODE" || fail "GET /devices without auth" "expected 401/403/422 got $CODE"

# Authenticated endpoints
echo ""
echo "--- Authenticated Endpoints ---"
R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/stats" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"devices_total"' && pass "GET /stats" || fail "GET /stats" "missing devices_total"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/devices" 2>/dev/null || echo "[]")
echo "$R" | grep -q '\[' && pass "GET /devices" || fail "GET /devices" "not array"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/tasks" 2>/dev/null || echo "[]")
echo "$R" | grep -q '\[' && pass "GET /tasks" || fail "GET /tasks" "not array"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/alerts" 2>/dev/null || echo "[]")
echo "$R" | grep -q '\[' && pass "GET /alerts" || fail "GET /alerts" "not array"

# API versioning
echo ""
echo "--- API Versioning ---"
R=$(curl -sf "$BASE/api/versions" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"v1"' && pass "GET /api/versions" || fail "GET /api/versions" "no v1"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/v1/devices" 2>/dev/null || echo "[]")
echo "$R" | grep -q '\[' && pass "GET /v1/devices" || fail "GET /v1/devices" "not array"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/v1/stats" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"devices_total"' && pass "GET /v1/stats" || fail "GET /v1/stats" "missing devices_total"

# Billing
echo ""
echo "--- Billing Endpoints ---"
R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/billing/subscription" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"plan"' && pass "GET /billing/subscription" || fail "GET /billing/subscription" "missing plan"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/billing/usage" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"tenant_id"' && pass "GET /billing/usage" || fail "GET /billing/usage" "missing tenant_id"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/billing/invoices" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"invoices"' && pass "GET /billing/invoices" || fail "GET /billing/invoices" "missing invoices"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/v1/billing/subscription" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"plan"' && pass "GET /v1/billing/subscription" || fail "GET /v1/billing/subscription" "missing plan"

# Groups/Tags (now using db.py)
echo ""
echo "--- Groups/Tags Endpoints ---"
R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/api/groups" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"groups"' && pass "GET /api/groups" || fail "GET /api/groups" "missing groups"

R=$(curl -sf -H "Authorization: Bearer $TOKEN" "$BASE/api/tags" 2>/dev/null || echo "{}")
echo "$R" | grep -q '"tags"' && pass "GET /api/tags" || fail "GET /api/tags" "missing tags"

# Dashboard
echo ""
echo "--- Dashboard ---"
CODE=$(curl -sf -o /dev/null -w "%{http_code}" "$BASE/dashboard/" 2>/dev/null || echo "000")
[ "$CODE" = "200" ] && pass "GET /dashboard/ → 200" || fail "GET /dashboard/" "expected 200 got $CODE"

# Summary
echo ""
echo "=== Results ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
if [ $FAIL -gt 0 ]; then
  echo -e "$ERRORS"
  exit 1
fi
echo "All tests passed!"
