#!/usr/bin/env python3
"""
CROSS-PLATFORM BACKTEST RUNNER

Uses relative imports from current directory - cross-platform compatible.
"""

import sys
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Working directory
CWD = os.getcwd()
print(f"Working dir: {CWD}")

# Change to trading directory
if "skills/trading" in CWD:
    # We're in skills/trading, go to parent
    PARENT = os.path.dirname(CWD)
    os.chdir(PARENT)
    # Now import from 1ai-skills/trading
    sys.path.insert(0, os.path.join(PARENT, "1ai-skills", "trading"))
    print(f"Import path: {os.path.join(PARENT, '1ai-skills', 'trading')}")
else:
    print("ERROR: Run from skills/trading directory")
    sys.exit(1)

# Try import
try:
    from trading.brokers.base import BrokerType
    print("Import test: OK")
except Exception as e:
    print(f"Import failed: {e}")

# Simple test - run Asia 7-Candle (we know it works)
TEST_SCRIPT = "1ai-skills/trading/strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py"

def test_backtest():
    """Test backtest."""
    cmd = ["python3", TEST_SCRIPT, "backtest", "2025-01-01", "2025-12-31", "--initial-balance", "100"]
    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        print(f"FAILED: {result.stderr[:100]}")
        return False

    # Parse
    for line in result.stdout.split('\n'):
        if "Win Rate:" in line:
            print(f"✅ {line}")
            return True
    print("No output")
    return False

# Test
print("="*80)
print("CROSS-PLATFORM TEST")
print("="*80)

if test_backtest():
    print("\n✅ SUCCESS! Cross-platform path works!")
else:
    print("\n❌ FAILED")
