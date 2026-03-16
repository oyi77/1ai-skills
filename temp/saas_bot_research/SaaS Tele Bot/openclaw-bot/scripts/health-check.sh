#!/bin/bash
# =============================================================================
# OPENCLAW BOT - HEALTH CHECK SCRIPT
# =============================================================================
# This script performs comprehensive health checks on the system
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =============================================================================
# CONFIGURATION
# =============================================================================

API_URL="${API_URL:-http://localhost:3000}"
TIMEOUT=10
VERBOSE=false

# =============================================================================
# FUNCTIONS
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                 OPENCLAW BOT HEALTH CHECK                     ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo "API URL: $API_URL"
    echo "Time: $(date)"
    echo ""
}

print_summary() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ All checks passed!${NC}"
    else
        echo -e "${RED}✗ $FAILED check(s) failed${NC}"
    fi
    
    echo ""
    echo "Summary:"
    echo "  Passed: $PASSED"
    echo "  Failed: $FAILED"
    echo "  Warnings: $WARNINGS"
    echo ""
}

# =============================================================================
# CHECK FUNCTIONS
# =============================================================================

PASSED=0
FAILED=0
WARNINGS=0

check_http() {
    local endpoint=$1
    local name=$2
    local expected_code=${3:-200}
    
    log_info "Checking $name..."
    
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$API_URL$endpoint" 2>/dev/null || echo "000")
    
    if [ "$RESPONSE" = "$expected_code" ]; then
        log_success "$name is healthy (HTTP $RESPONSE)"
        ((PASSED++))
        return 0
    else
        log_error "$name failed (HTTP $RESPONSE, expected $expected_code)"
        ((FAILED++))
        return 1
    fi
}

check_port() {
    local host=$1
    local port=$2
    local name=$3
    
    log_info "Checking $name on $host:$port..."
    
    if nc -z -w $TIMEOUT "$host" "$port" 2>/dev/null; then
        log_success "$name is reachable"
        ((PASSED++))
        return 0
    else
        log_error "$name is not reachable"
        ((FAILED++))
        return 1
    fi
}

check_command() {
    local cmd=$1
    local name=$2
    
    log_info "Checking $name..."
    
    if command -v "$cmd" &> /dev/null; then
        local version=$($cmd --version 2>&1 | head -1)
        log_success "$name is installed ($version)"
        ((PASSED++))
        return 0
    else
        log_error "$name is not installed"
        ((FAILED++))
        return 1
    fi
}

check_process() {
    local process=$1
    local name=$2
    
    log_info "Checking $name process..."
    
    if pgrep -x "$process" > /dev/null; then
        log_success "$name is running"
        ((PASSED++))
        return 0
    else
        log_error "$name is not running"
        ((FAILED++))
        return 1
    fi
}

check_disk_space() {
    local threshold=${1:-90}
    
    log_info "Checking disk space (threshold: ${threshold}%)..."
    
    USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ "$USAGE" -lt "$threshold" ]; then
        log_success "Disk usage is at ${USAGE}%"
        ((PASSED++))
        return 0
    else
        log_error "Disk usage is at ${USAGE}% (threshold: ${threshold}%)"
        ((FAILED++))
        return 1
    fi
}

check_memory() {
    local threshold=${1:-90}
    
    log_info "Checking memory usage (threshold: ${threshold}%)..."
    
    if command -v free &> /dev/null; then
        USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    else
        # macOS
        USAGE=$(vm_stat | awk '/Pages active/ {print $3}' | sed 's/\.//')
        TOTAL=$(vm_stat | awk '/Pages free/ {print $3}' | sed 's/\.//')
        USAGE=$((USAGE * 100 / (USAGE + TOTAL)))
    fi
    
    if [ "$USAGE" -lt "$threshold" ]; then
        log_success "Memory usage is at ${USAGE}%"
        ((PASSED++))
        return 0
    else
        log_error "Memory usage is at ${USAGE}% (threshold: ${threshold}%)"
        ((FAILED++))
        return 1
    fi
}

# =============================================================================
# MAIN CHECKS
# =============================================================================

print_header

# System checks
echo -e "${BLUE}--- System Checks ---${NC}"
check_disk_space 80
check_memory 80
echo ""

# Service checks
echo -e "${BLUE}--- Service Checks ---${NC}"
check_process "node" "Node.js"
check_process "postgres" "PostgreSQL"
check_process "redis-server" "Redis"
echo ""

# Port checks
echo -e "${BLUE}--- Port Checks ---${NC}"
check_port "localhost" "3000" "Bot API"
check_port "localhost" "5432" "PostgreSQL"
check_port "localhost" "6379" "Redis"
echo ""

# HTTP endpoint checks
echo -e "${BLUE}--- HTTP Endpoint Checks ---${NC}"
check_http "/health" "Health Endpoint"
check_http "/health/db" "Database Health"
check_http "/health/queue" "Queue Health"
echo ""

# External service checks (if configured)
if [ -n "$CHECK_EXTERNAL" ]; then
    echo -e "${BLUE}--- External Service Checks ---${NC}"
    
    # Check AI API
    AI_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "${GEMINIGEN_API_URL:-https://api.geminigen.ai}/health" 2>/dev/null || echo "000")
    if [ "$AI_STATUS" = "200" ]; then
        log_success "AI API (GeminiGen) is healthy"
        ((PASSED++))
    else
        log_warning "AI API (GeminiGen) returned HTTP $AI_STATUS"
        ((WARNINGS++))
    fi
    
    # Check Payment Gateway
    PAYMENT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "https://api.midtrans.com/v2/ping" 2>/dev/null || echo "000")
    if [ "$PAYMENT_STATUS" = "200" ] || [ "$PAYMENT_STATUS" = "401" ]; then
        log_success "Payment Gateway (Midtrans) is reachable"
        ((PASSED++))
    else
        log_warning "Payment Gateway (Midtrans) returned HTTP $PAYMENT_STATUS"
        ((WARNINGS++))
    fi
    
    echo ""
fi

# =============================================================================
# SUMMARY
# =============================================================================

print_summary

# Exit with appropriate code
if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
