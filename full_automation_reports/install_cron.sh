#!/bin/bash

# Full Automation Cron Jobs
# Run this to install crontab entries

echo "Installing full automation cron jobs..."

(crontab -l 2>/dev/null | grep -v "full_automation"; cat << 'EOF'

# FULL AUTOMATION COORDINATOR
# Morning workflow: 08:00 WIB
0 8 * * * cd /home/openclaw/.openclaw/workspace && python3 full_automation_coordinator.py morning >> ~/full_automation.log 2>&1

# Evening workflow: 20:00 WIB
0 20 * * * cd /home/openclaw/.openclaw/workspace && python3 full_automation_coordinator.py evening >> ~/full_automation.log 2>&1

# Weekly refresh: Sunday 23:00 WIB
0 23 * * 0 cd /home/openclaw/.openclaw/workspace && python3 full_automation_coordinator.py weekly >> ~/full_automation.log 2>&1

EOF
) | crontab -

echo "Cron jobs installed successfully!"
crontab -l
