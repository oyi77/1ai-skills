#!/bin/bash
# Full Production Deployment - ALL IN MODE

echo "========================================="
echo "🚀 FULL PRODUCTION DEPLOY - ALL IN"
echo "========================================="
echo ""
echo "Loading API Key..."

GOOGLE_MAPS_API_KEY=$(cat /home/openclaw/.openclaw/workspace/google_maps_api_key.txt)
export GOOGLE_MAPS_API_KEY

echo "API Key: ${GOOGLE_MAPS_API_KEY:0:20}...${GOOGLE_MAPS_API_KEY: -4}"
echo ""

echo "Running Production Campaign..."
python3 /home/openclaw/.openclaw/workspace/lead_gen_machine/all_in_production.py