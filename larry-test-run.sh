#!/bin/bash
# Larry Playbook Demo Run - Quick test

echo "🚀 LARRY PLAYBOOK — DEMO RUN"
echo "=============================="
echo ""

# Set API keys
export POST_BRIDGE_API_KEY="pb_live_Kyc2gafDF7Qc8c2ALELtEC"
export LARRY_PLAYBOOK_PATH="/home/openclaw/.openclaw/workspace/skills/larry-playbook"

# Check skill status
echo "📋 Checking Larry Playbook status..."
python3 "$LARRY_PLAYBOOK_PATH/larry-demo.py"

echo ""
echo "✅ Demo complete!"
echo "Video ready at: ~/.openclaw/.openclaw/workspace/output/larry_slideshows/"
echo ""
echo "To run in production mode:"
echo "  export POST_BRIDGE_API_KEY=\"pb_live_Kyc2gafDF7Qc8c2ALELtEC\""
echo "  python3 skills/larry-playbook/larry-continuous-system.py"
echo ""
