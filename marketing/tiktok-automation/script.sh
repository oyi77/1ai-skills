#!/bin/bash
# =============================================================================
# TikTok Automation Script (Cross-Platform)
# Works on: Linux, macOS, Windows (via WSL/Git Bash/Cygwin)
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_PATH="$SCRIPT_DIR/config.json"
SELECTORS_PATH="$SCRIPT_DIR/selectors.json"
LOG_PATH="$SCRIPT_DIR/tiktok-automation.log"

# Default values
VIDEO_PATH=""
CAPTION=""
TAGS=""
UPDATE_SELECTORS=false
HEADLESS=false

# Colors (cross-platform)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    GRAY='\033[0;90m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    GRAY=''
    NC=''
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --video)
            VIDEO_PATH="$2"
            shift 2
            ;;
        --caption)
            CAPTION="$2"
            shift 2
            ;;
        --tags)
            TAGS="$2"
            shift 2
            ;;
        --update-selectors)
            UPDATE_SELECTORS=true
            shift
            ;;
        --headless)
            HEADLESS=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [$level] $message"
    
    case $level in
        INFO) echo -e "${GREEN}$log_entry${NC}" ;;
        WARN) echo -e "${YELLOW}$log_entry${NC}" ;;
        ERROR) echo -e "${RED}$log_entry${NC}" ;;
        DEBUG) echo -e "${GRAY}$log_entry${NC}" ;;
    esac
    
    echo "$log_entry" >> "$LOG_PATH"
}

check_requirements() {
    log "INFO" "Checking requirements..."
    
    if ! command -v node &> /dev/null; then
        log "ERROR" "Node.js not found. Please install Node.js 16+"
        return 1
    fi
    
    local node_version=$(node --version)
    log "INFO" "Node.js found: $node_version"
    
    if ! npx playwright --version &> /dev/null; then
        log "WARN" "Playwright not found. Installing..."
        npm install -g playwright
    fi
    
    local pw_version=$(npx playwright --version 2>&1 | head -1)
    log "INFO" "Playwright found: $pw_version"
    
    return 0
}

run_automation() {
    log "INFO" "Starting TikTok automation..."
    log "INFO" "Video: $VIDEO_PATH"
    log "INFO" "Caption: $CAPTION"
    log "INFO" "Tags: $TAGS"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log "ERROR" "Node.js is required but not installed"
        exit 1
    fi
    
    # Create Playwright script
    cat > "$SCRIPT_DIR/tiktok-upload.tmp.js" << 'PLAYWRIGHT_EOF'
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const videoPath = args.find(a => a.startsWith('--video='))?.split('=')[1] || '';
const caption = args.find(a => a.startsWith('--caption='))?.split('=')[1] || '';
const tags = args.find(a => a.startsWith('--tags='))?.split('=')[1] || '';
const headless = args.includes('--headless');

(async () => {
    console.log('Launching browser...');
    
    const browser = await chromium.launch({
        headless: headless,
        slowMo: 100
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    try {
        console.log('Navigating to TikTok...');
        await page.goto('https://www.tiktok.com/login', { waitUntil: 'networkidle' });
        
        // Check if already logged in
        const isLoggedIn = await page.isVisible('[data-e2e="upload-btn"]');
        if (!isLoggedIn) {
            console.log('Please login manually first, then run again');
        }
        
        console.log('Navigating to upload page...');
        await page.goto('https://www.tiktok.com/upload', { waitUntil: 'networkidle' });
        
        console.log('Uploading video...');
        const fileInput = await page.$('input[type="file"]');
        if (fileInput && videoPath) {
            await fileInput.setInputFiles(videoPath);
        } else {
            console.log('No video file specified. Add --video path/to/video.mp4');
        }
        
        console.log('Automation completed');
        
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
})();
PLAYWRIGHT_EOF
    
    log "INFO" "Running Playwright script..."
    
    local pw_args="--video=$VIDEO_PATH --caption=$CAPTION --tags=$TAGS"
    if [ "$HEADLESS" = true ]; then
        pw_args="$pw_args --headless"
    fi
    
    node "$SCRIPT_DIR/tiktok-upload.tmp.js" $pw_args
    
    rm -f "$SCRIPT_DIR/tiktok-upload.tmp.js"
}

# Main
echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}TikTok Automation - Berkah Karya ⚡${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""

if ! check_requirements; then
    log "ERROR" "Requirements check failed. Exiting."
    exit 1
fi

if [ -z "$VIDEO_PATH" ]; then
    echo "Usage: $0 --video path/to/video.mp4 [--caption 'caption'] [--tags '#tag1 #tag2'] [--headless]"
    echo ""
    echo "Options:"
    echo "  --video FILE          Video file path (required)"
    echo "  --caption TEXT        Caption for the video"
    echo "  --tags TAGS           Hashtags (space-separated)"
    echo "  --headless            Run browser in headless mode"
    echo "  --update-selectors   Re-learn element selectors"
    exit 1
fi

if [ ! -f "$VIDEO_PATH" ]; then
    log "ERROR" "Video file not found: $VIDEO_PATH"
    exit 1
fi

run_automation

echo ""
log "INFO" "Automation completed!"
