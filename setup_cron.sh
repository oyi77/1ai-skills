#!/bin/bash
# Viral Research Pipeline - Cron Runner
# Run this to set up hourly cron job

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIRAL_SCRIPT="$SCRIPT_DIR/viral_research_pipeline.py"

# Create cron entry
CRON_ENTRY="0 * * * * cd $SCRIPT_DIR && python3 $VIRAL_SCRIPT --full --cookies \"\${KALODATA_COOKIES}\" >> logs/viral_cron.log 2>&1"

echo "Setting up hourly cron job for viral research..."
echo

# Display current cron
echo "Current crontab:"
crontab -l 2>/dev/null || echo "(empty)"
echo

# Add new cron job
(crontab -l 2>/dev/null | grep -v "viral_research_pipeline"; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job added:"
echo "$CRON_ENTRY"
echo

# Create logs directory
mkdir -p $SCRIPT_DIR/logs

echo "To run manually:"
echo "  python3 viral_research_pipeline.py --full --cookies 'YOUR_COOKIES'"
echo
echo "To test research only:"
echo "  python3 viral_research_pipeline.py --research-only --cookies 'YOUR_COOKIES'"
