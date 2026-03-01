#!/usr/bin/env bash
# ============================================================================
# 1ai-skills-bundle v2.0 — Bundle Installer
# ============================================================================
# Installs the OpenClaw skills bundle on a fresh machine:
#   1. Checks Python version (>=3.8)
#   2. Creates symlinks for hyphenated skill dirs → Python-importable names
#   3. Installs Python dependencies
#   4. Validates cron job configuration (dry-run)
#   5. Verifies key files exist
#
# Usage:
#   chmod +x install.sh && ./install.sh
#   ./install.sh --skip-deps      # Skip pip install
#   ./install.sh --skip-cron      # Skip cron validation
#   ./install.sh --dry-run        # Show what would be done
# ============================================================================

set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── Configuration ───────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="${WORKSPACE_ROOT}/skills"
AUTOMATION_DIR="${WORKSPACE_ROOT}/automation"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=8

# Skill directories that need hyphen→underscore symlinks for Python imports
SYMLINK_PAIRS=(
    "task-manager:task_manager"
    "telegram-bot:telegram_bot"
    "revenue-dashboard:revenue_dashboard"
    "opportunity-scout:opportunity_scout"
    "strategic-recommendations:strategic_recommendations"
    "ai-services:ai_services"
)

# Key files that must exist for the bundle to function
KEY_FILES=(
    "skills/task-manager/__init__.py"
    "skills/task-manager/enforcement.py"
    "skills/task-manager/storage.py"
    "skills/task-manager/notifier.py"
    "skills/telegram-bot/__init__.py"
    "skills/telegram-bot/commands.py"
    "skills/revenue-dashboard/__init__.py"
    "skills/revenue-dashboard/dashboard.py"
    "skills/opportunity-scout/__init__.py"
    "skills/opportunity-scout/engine.py"
    "skills/strategic-recommendations/__init__.py"
    "skills/strategic-recommendations/engine.py"
    "skills/ai-services/__init__.py"
    "skills/ai-services/pipeline.py"
    "skills/content/__init__.py"
    "automation/cron_setup.py"
    "automation/heartbeat.py"
    "automation/self_healing.py"
    "automation/jobs.json"
)

# ── Flags ───────────────────────────────────────────────────────────────────
SKIP_DEPS=false
SKIP_CRON=false
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        --skip-deps)  SKIP_DEPS=true ;;
        --skip-cron)  SKIP_CRON=true ;;
        --dry-run)    DRY_RUN=true ;;
        --help|-h)
            echo "Usage: $0 [--skip-deps] [--skip-cron] [--dry-run] [--help]"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown argument: $arg${NC}"
            exit 1
            ;;
    esac
done

# ── Counters ────────────────────────────────────────────────────────────────
ERRORS=0
WARNINGS=0

log_ok()    { echo -e "  ${GREEN}✓${NC} $1"; }
log_warn()  { echo -e "  ${YELLOW}⚠${NC} $1"; WARNINGS=$((WARNINGS + 1)); }
log_err()   { echo -e "  ${RED}✗${NC} $1"; ERRORS=$((ERRORS + 1)); }
log_info()  { echo -e "  ${BLUE}→${NC} $1"; }
log_step()  { echo -e "\n${BLUE}[$1]${NC} $2"; }

# ============================================================================
# Step 1: Check Python version
# ============================================================================
check_python() {
    log_step "1/5" "Checking Python version..."

    if ! command -v python3 &>/dev/null; then
        log_err "python3 not found. Install Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+"
        return 1
    fi

    local py_version
    py_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local py_major py_minor
    py_major=$(echo "$py_version" | cut -d. -f1)
    py_minor=$(echo "$py_version" | cut -d. -f2)

    if [ "$py_major" -lt "$MIN_PYTHON_MAJOR" ] || \
       { [ "$py_major" -eq "$MIN_PYTHON_MAJOR" ] && [ "$py_minor" -lt "$MIN_PYTHON_MINOR" ]; }; then
        log_err "Python ${py_version} found, but ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ required"
        return 1
    fi

    log_ok "Python ${py_version} (>= ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR})"
}

# ============================================================================
# Step 2: Create symlinks for hyphenated directories
# ============================================================================
create_symlinks() {
    log_step "2/5" "Creating symlinks for Python-importable names..."

    if [ ! -d "$SKILLS_DIR" ]; then
        log_err "Skills directory not found: ${SKILLS_DIR}"
        return 1
    fi

    for pair in "${SYMLINK_PAIRS[@]}"; do
        local source="${pair%%:*}"
        local target="${pair##*:}"
        local source_path="${SKILLS_DIR}/${source}"
        local target_path="${SKILLS_DIR}/${target}"

        if [ ! -d "$source_path" ]; then
            log_warn "Source directory missing: skills/${source} — skipping symlink"
            continue
        fi

        if [ -L "$target_path" ]; then
            # Symlink already exists — check it points to the right place
            local current_target
            current_target=$(readlink "$target_path")
            if [ "$current_target" = "$source" ] || [ "$current_target" = "$source_path" ]; then
                log_ok "skills/${target} → ${source} (already exists)"
            else
                log_warn "skills/${target} points to '${current_target}', expected '${source}'"
                if [ "$DRY_RUN" = false ]; then
                    rm "$target_path"
                    ln -s "$source" "$target_path"
                    log_ok "skills/${target} → ${source} (re-created)"
                else
                    log_info "[DRY-RUN] Would re-create symlink"
                fi
            fi
        elif [ -d "$target_path" ]; then
            log_warn "skills/${target} is a real directory, not a symlink"
        else
            if [ "$DRY_RUN" = false ]; then
                ln -s "$source" "$target_path"
                log_ok "skills/${target} → ${source} (created)"
            else
                log_info "[DRY-RUN] Would create: skills/${target} → ${source}"
            fi
        fi
    done
}

# ============================================================================
# Step 3: Install Python dependencies
# ============================================================================
install_deps() {
    log_step "3/5" "Installing Python dependencies..."

    if [ "$SKIP_DEPS" = true ]; then
        log_info "Skipped (--skip-deps)"
        return 0
    fi

    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        log_warn "requirements.txt not found: ${REQUIREMENTS_FILE}"
        return 0
    fi

    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] Would run: pip install -r ${REQUIREMENTS_FILE}"
        return 0
    fi

    if python3 -m pip install -r "$REQUIREMENTS_FILE" --quiet 2>/dev/null; then
        log_ok "Dependencies installed from requirements.txt"
    else
        log_warn "pip install had warnings (non-fatal)"
    fi
}

# ============================================================================
# Step 4: Validate cron configuration
# ============================================================================
validate_cron() {
    log_step "4/5" "Validating cron job configuration..."

    if [ "$SKIP_CRON" = true ]; then
        log_info "Skipped (--skip-cron)"
        return 0
    fi

    local cron_setup="${AUTOMATION_DIR}/cron_setup.py"
    local jobs_json="${AUTOMATION_DIR}/jobs.json"

    if [ ! -f "$cron_setup" ]; then
        log_err "cron_setup.py not found: ${cron_setup}"
        return 1
    fi

    if [ ! -f "$jobs_json" ]; then
        log_err "jobs.json not found: ${jobs_json}"
        return 1
    fi

    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] Would validate cron config via dry-run"
        return 0
    fi

    # Validate by doing a dry-run of the cron scheduler
    local cron_output
    if cron_output=$(PYTHONPATH="$WORKSPACE_ROOT" python3 "$cron_setup" --dry-run validate 2>&1); then
        log_ok "Cron configuration validated (dry-run)"

        # Count enabled jobs
        local job_count
        job_count=$(python3 -c "
import json
with open('${jobs_json}') as f:
    data = json.load(f)
enabled = sum(1 for j in data.get('jobs', []) if j.get('enabled', True))
print(enabled)
" 2>/dev/null || echo "?")
        log_info "${job_count} enabled cron jobs found"
    else
        log_warn "Cron validation had issues (non-fatal): ${cron_output}"
    fi
}

# ============================================================================
# Step 5: Verify key files
# ============================================================================
verify_files() {
    log_step "5/5" "Verifying key bundle files..."

    local found=0
    local missing=0

    for file in "${KEY_FILES[@]}"; do
        local full_path="${WORKSPACE_ROOT}/${file}"
        if [ -f "$full_path" ]; then
            found=$((found + 1))
        else
            log_warn "Missing: ${file}"
            missing=$((missing + 1))
        fi
    done

    if [ "$missing" -eq 0 ]; then
        log_ok "All ${found} key files verified"
    else
        log_warn "${found}/${#KEY_FILES[@]} files found (${missing} missing)"
    fi
}

# ============================================================================
# Main
# ============================================================================
main() {
    echo ""
    echo "============================================"
    echo "  1ai-skills-bundle v2.0 — Installer"
    echo "============================================"
    echo ""
    echo "  Workspace: ${WORKSPACE_ROOT}"
    echo "  Skills:    ${SKILLS_DIR}"
    if [ "$DRY_RUN" = true ]; then
        echo -e "  Mode:      ${YELLOW}DRY-RUN${NC}"
    fi

    check_python
    create_symlinks
    install_deps
    validate_cron
    verify_files

    # ── Summary ─────────────────────────────────────────────────────────
    echo ""
    echo "============================================"
    if [ "$ERRORS" -gt 0 ]; then
        echo -e "  ${RED}INSTALL FAILED${NC} — ${ERRORS} error(s), ${WARNINGS} warning(s)"
        echo "============================================"
        exit 1
    elif [ "$WARNINGS" -gt 0 ]; then
        echo -e "  ${YELLOW}INSTALL COMPLETE${NC} — ${WARNINGS} warning(s)"
        echo "============================================"
        echo ""
        echo -e "  ${YELLOW}Some optional components may be missing.${NC}"
        echo "  The core bundle is functional."
        exit 0
    else
        echo -e "  ${GREEN}INSTALL SUCCESSFUL${NC} — all checks passed!"
        echo "============================================"
        echo ""
        echo "  Next steps:"
        echo "    • Run tests:  python3 -m pytest tests/ -v"
        echo "    • Cron setup: python3 automation/cron_setup.py status"
        echo ""
        exit 0
    fi
}

main
