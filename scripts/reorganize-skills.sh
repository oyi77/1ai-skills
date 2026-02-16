#!/bin/bash

# Skills Reorganization Script
# This script reorganizes 44 skills into 9 grouped categories
# Preserves git history using 'git mv'

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Dry run flag
DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo -e "${YELLOW}Running in DRY RUN mode - no changes will be made${NC}"
fi

# Function to move skill
move_skill() {
    local from="$1"
    local to="$2"
    
    if [ ! -d "$ROOT_DIR/$from" ]; then
        echo -e "${RED}Warning: Source directory $from does not exist, skipping${NC}"
        return
    fi
    
    # Check if directory is empty (only contains . and ..)
    if [ -z "$(ls -A "$ROOT_DIR/$from")" ]; then
        echo -e "${YELLOW}Warning: Source directory $from is empty, skipping${NC}"
        return
    fi
    
    if $DRY_RUN; then
        echo -e "${GREEN}Would move: $from -> $to${NC}"
    else
        # Create parent directory if it doesn't exist
        mkdir -p "$(dirname "$ROOT_DIR/$to")"
        
        # Use git mv to preserve history
        git -C "$ROOT_DIR" mv "$from" "$to"
        echo -e "${GREEN}Moved: $from -> $to${NC}"
    fi
}

# Create backup
if ! $DRY_RUN; then
    echo -e "${YELLOW}Creating backup branch...${NC}"
    BACKUP_BRANCH="backup-before-reorganization-$(date +%Y%m%d-%H%M%S)"
    git -C "$ROOT_DIR" branch "$BACKUP_BRANCH"
    echo -e "${GREEN}Created backup branch: $BACKUP_BRANCH${NC}"
fi

echo -e "${YELLOW}Starting skills reorganization...${NC}"

# Create category directories
if ! $DRY_RUN; then
    mkdir -p "$ROOT_DIR"/{core,development,marketing,sales,operations,productivity,research,automation,content}
fi

# CORE (5 skills)
echo -e "\n${YELLOW}=== CORE ===${NC}"
move_skill "agent-docs" "core/agent-docs"
move_skill "joko-orchestrator" "core/joko-orchestrator"
move_skill "joko-proactive-agent" "core/joko-proactive-agent"
move_skill "self-improving-agent" "core/self-improving-agent"
move_skill "using-superpowers" "core/using-superpowers"

# DEVELOPMENT (10 skills)
echo -e "\n${YELLOW}=== DEVELOPMENT ===${NC}"
move_skill "systematic-debugging" "development/systematic-debugging"
move_skill "test-driven-development" "development/test-driven-development"
move_skill "subagent-driven-development" "development/subagent-driven-development"
move_skill "executing-plans" "development/executing-plans"
move_skill "writing-plans" "development/writing-plans"
move_skill "finishing-a-development-branch" "development/finishing-a-development-branch"
move_skill "requesting-code-review" "development/requesting-code-review"
move_skill "receiving-code-review" "development/receiving-code-review"
move_skill "using-git-worktrees" "development/using-git-worktrees"
move_skill "verification-before-completion" "development/verification-before-completion"

# MARKETING (4 skills, rename marketing to marketing-strategy)
echo -e "\n${YELLOW}=== MARKETING ===${NC}"
# Handle marketing -> marketing/marketing-strategy with temp directory
if [ -d "$ROOT_DIR/marketing" ] && [ ! -d "$ROOT_DIR/marketing/marketing-strategy" ]; then
    if $DRY_RUN; then
        echo -e "${GREEN}Would move: marketing -> marketing-temp${NC}"
        echo -e "${GREEN}Would move: marketing-temp -> marketing/marketing-strategy${NC}"
    else
        git -C "$ROOT_DIR" mv marketing marketing-temp
        mkdir -p "$ROOT_DIR/marketing"
        git -C "$ROOT_DIR" mv marketing-temp marketing/marketing-strategy
        echo -e "${GREEN}Moved: marketing -> marketing/marketing-strategy${NC}"
    fi
fi
move_skill "content-creator" "marketing/content-creator"
move_skill "market-research" "marketing/market-research"
move_skill "analytics-reporting" "marketing/analytics-reporting"

# SALES (3 skills, rename sales to sales-strategy)
echo -e "\n${YELLOW}=== SALES ===${NC}"
# Handle sales -> sales/sales-strategy with temp directory
if [ -d "$ROOT_DIR/sales" ] && [ ! -d "$ROOT_DIR/sales/sales-strategy" ]; then
    if $DRY_RUN; then
        echo -e "${GREEN}Would move: sales -> sales-temp${NC}"
        echo -e "${GREEN}Would move: sales-temp -> sales/sales-strategy${NC}"
    else
        git -C "$ROOT_DIR" mv sales sales-temp
        mkdir -p "$ROOT_DIR/sales"
        git -C "$ROOT_DIR" mv sales-temp sales/sales-strategy
        echo -e "${GREEN}Moved: sales -> sales/sales-strategy${NC}"
    fi
fi
move_skill "business-development" "sales/business-development"
move_skill "customer-support" "sales/customer-support"

# OPERATIONS (5 skills)
echo -e "\n${YELLOW}=== OPERATIONS ===${NC}"
move_skill "operations-team" "operations/operations-team"
move_skill "product-team" "operations/product-team"
move_skill "revenue-team" "operations/revenue-team"
move_skill "governance-team" "operations/governance-team"
move_skill "project-management" "operations/project-management"

# PRODUCTIVITY (5 skills)
echo -e "\n${YELLOW}=== PRODUCTIVITY ===${NC}"
move_skill "google-workspace" "productivity/google-workspace"
move_skill "google-canvas" "productivity/google-canvas"
move_skill "google-flow" "productivity/google-flow"
move_skill "email-automation" "productivity/email-automation"
move_skill "calendar-management" "productivity/calendar-management"

# RESEARCH (4 skills)
echo -e "\n${YELLOW}=== RESEARCH ===${NC}"
move_skill "mckinsey-research" "research/mckinsey-research"
move_skill "polymarket-analyst" "research/polymarket-analyst"
move_skill "brainstorming" "research/brainstorming"
move_skill "dispatching-parallel-agents" "research/dispatching-parallel-agents"

# AUTOMATION (4 skills)
echo -e "\n${YELLOW}=== AUTOMATION ===${NC}"
move_skill "jobhunter-master" "automation/jobhunter-master"
move_skill "moltbook-interact" "automation/moltbook-interact"
move_skill "joko-moltbook" "automation/joko-moltbook"
move_skill "clawild-moltbook" "automation/clawild-moltbook"

# CONTENT (4 skills)
echo -e "\n${YELLOW}=== CONTENT ===${NC}"
move_skill "humanizer" "content/humanizer"
move_skill "humanizer-zh" "content/humanizer-zh"
move_skill "gemini-image-generator" "content/gemini-image-generator"
move_skill "writing-skills" "content/writing-skills"

if $DRY_RUN; then
    echo -e "\n${YELLOW}Dry run complete. No changes were made.${NC}"
    echo -e "${YELLOW}Run without --dry-run to execute the reorganization.${NC}"
else
    echo -e "\n${GREEN}Reorganization complete!${NC}"
    echo -e "${GREEN}Backup branch created: $BACKUP_BRANCH${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Run: node scripts/update-skill-paths.js"
    echo -e "  2. Review changes with: git status"
    echo -e "  3. Commit changes with: git commit -m 'Reorganize skills into grouped categories'"
fi
