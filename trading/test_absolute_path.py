#!/usr/bin/env python3
import os
import subprocess
import json

venv_python = os.path.expanduser('~/.trading-venv/bin/python')
abs_path = os.path.abspath('strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py')

print('Testing ABSOLUTE PATH with full date range...')
print(f'Path: {abs_path}')
print(f'Backslashes: {abs_path.count(chr(92))}')
print()

result = subprocess.run(
    [venv_python, abs_path, 'backtest', '2025-01-01', '2025-12-31', '--initial-balance', '100'],
    capture_output=True,
    text=True,
    timeout=120
)

if result.returncode == 0:
    # Find JSON in output
    for line in result.stdout.split('\n'):
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            try:
                data = json.loads(line)
                if 'win_rate' in data:
                    print('✅ SUCCESS with ABSOLUTE PATH (with backslashes)')
                    print(f'   Win Rate: {data["win_rate"]}%')
                    print(f'   PNL: ${data["pnl"]["usd"]}')
                    print(f'   Trades: {data["total_trades"]}')
                    print()
                    print('CONCLUSION: Backslash in path IS NOT THE PROBLEM!')
                    break
            except:
                pass
else:
    print(f'❌ FAILED')
    print(result.stderr[:200])
