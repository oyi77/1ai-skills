#!/bin/bash
# Vector DB Sync - Heartbeat Wrapper
# Run this every 30 minutes via HEARTBEAT.md

cd /home/openclaw/.openclaw/workspace
python3 scripts/vector_db_sync.py 2>&1 | tail -20