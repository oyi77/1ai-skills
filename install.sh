#!/bin/bash

# Clear screen
clear

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Display 1AI-SKILL Banner
echo -e "${BLUE}"
echo "  __  ___  ___      __   __   __   __   __      "
echo " /  |/ _ \/ _ \    / /  / /  / /  / /  / /      "
echo "/ /|  / _  / _ \  / /  / /__/ /__/ /__/ /___    "
echo "/_/ |_/_/ |_/_/ \_\/_/  /____/____/____/_____/    "
echo "                                                  "
echo "    1   A   I   -   S   K   I   L   L             "
echo -e "${NC}"
echo ""

# Progress Messages
echo "Powering Up..."
sleep 1

echo "Learning the things..."
sleep 1.5

echo -e "${RED}F*ck this world...${NC}"
sleep 1

# Simulate skill installation loop
SKILLS=("marketing" "operations" "content" "core" "development" "productivity" "research" "growth")
TOTAL=${#SKILLS[@]}

for i in "${!SKILLS[@]}"; do
    CURRENT=$((i + 1))
    SKILL=${SKILLS[$i]}
    echo -ne "Installing skill module: $SKILL ($CURRENT/$TOTAL)...\r"
    sleep 0.5
    echo -e "${GREEN}Installed $SKILL ($CURRENT/$TOTAL)        ${NC}"
done

echo ""
echo "All Skills installed...."
sleep 1

echo "Booting up the mind...."
sleep 2

echo ""
echo -e "${GREEN}ALL DONE, ENJOY YOUR LIFE!${NC}"
echo ""

# Actual installation logic check (optional verification)
if [ -d "marketing" ] && [ -f "SKILL_INDEX.json" ]; then
    echo "Files verified locally."
fi
