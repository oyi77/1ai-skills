#!/bin/bash
# =============================================================================
# 1AI-SKILLS INSTALLATION VERIFICATION (Cross-Platform)
# Works on: Linux, macOS, Windows (via WSL/Git Bash/Cygwin)
# =============================================================================

# Get script directory (cross-platform)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="$(dirname "$SCRIPT_DIR")"

# Colors (cross-platform)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color
else
    GREEN=''
    YELLOW=''
    RED=''
    CYAN=''
    NC=''
fi

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}1AI-SKILLS INSTALLATION VERIFICATION${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check main directory
if [ -d "$REPO_PATH" ]; then
    echo -e "${GREEN}[OK]${NC} Repository installed at: $REPO_PATH"
    
    # List skill directories
    echo ""
    echo -e "${YELLOW}Installed Skills:${NC}"
    if [ -d "$REPO_PATH/skills" ]; then
        for dir in "$REPO_PATH"/*; do
            if [ -d "$dir" ] && [ "$(basename "$dir")" != "node_modules" ] && [ "$(basename "$dir")" != ".git" ]; then
                echo -e "  - $(basename "$dir")"
            fi
        done
    else
        echo -e "  ${RED}(No skill directories found)${NC}"
    fi
    
    # List key files
    echo ""
    echo -e "${YELLOW}Key Files:${NC}"
    KEY_FILES=('LLM.md' 'README.md' 'INSTALL.md' 'SKILL_INDEX.json' 'package.json')
    for file in "${KEY_FILES[@]}"; do
        if [ -f "$REPO_PATH/$file" ]; then
            echo -e "  [OK] $file"
        else
            echo -e "  [MISSING] $file"
        fi
    done
    
    # Check node_modules
    if [ -d "$REPO_PATH/node_modules" ]; then
        echo ""
        echo -e "${GREEN}[OK]${NC} Dependencies installed (node_modules exists)"
    else
        echo ""
        echo -e "${YELLOW}[WARNING]${NC} node_modules not found - run 'npm install'"
    fi
    
else
    echo -e "${RED}[FAILED]${NC} Repository not found at: $REPO_PATH"
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "1. Skills are now available in: $REPO_PATH"
echo -e "2. Skills auto-activate based on keywords in your requests"
echo -e "3. Check SKILL_INDEX.json for keyword mappings"
echo -e "4. See README.md for usage examples"
echo -e "${CYAN}========================================${NC}"
