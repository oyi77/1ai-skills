#!/bin/bash
# =============================================================================
# Gemini Image Generator - Quick Launcher (Cross-Platform)
# Works on: Linux, macOS, Windows (via WSL/Git Bash/Cygwin)
# =============================================================================

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "Gemini Image Generator"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.6+"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Function to run prompt optimizer
run_category() {
    local category=$1
    local product=$2
    
    if [ -z "$product" ]; then
        read -p "Enter product name: " product
    fi
    
    $PYTHON_CMD prompt_optimizer.py --category "$category" --product "$product"
}

# Function to run batch processing
run_batch() {
    echo ""
    echo "Batch processing all images in input folder..."
    $PYTHON_CMD workflow_runner.py --batch
}

# Main menu
if [ -z "$1" ]; then
    echo "Choose category:"
    echo "1. Fashion"
    echo "2. Electronics"
    echo "3. Food"
    echo "4. Beauty"
    echo "5. Home"
    echo "6. Batch Process"
    echo ""
    read -p "Enter choice (1-6): " choice
    
    case $choice in
        1) run_category "fashion" "" ;;
        2) run_category "electronics" "" ;;
        3) run_category "food" "" ;;
        4) run_category "beauty" "" ;;
        5) run_category "home" "" ;;
        6) run_batch ;;
        *) echo "Invalid choice" ;;
    esac
else
    # Command line arguments
    case $1 in
        fashion) run_category "fashion" "$2" ;;
        electronics) run_category "electronics" "$2" ;;
        food) run_category "food" "$2" ;;
        beauty) run_category "beauty" "$2" ;;
        home) run_category "home" "$2" ;;
        batch) run_batch ;;
        *) echo "Invalid argument. Use: fashion, electronics, food, beauty, home, batch" ;;
    esac
fi
