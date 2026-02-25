#!/usr/bin/env python3
import os
import subprocess
import json

venv_python = os.path.expanduser('~/.trading-venv/bin/python')
abs_path = os.path.abspath('strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py')

print(f'Path: {abs_path}')
print(f'Backslashes: {abs_path.count(chr(92))}')
print()

result = subprocess.run(
    [venv_python, abs_path, 'backtest', '2025-01-01', '2025-12-31', '--initial-balance', '100'],
    capture_output=True,
    text=True,
    timeout=300
)

# Save all output
with open('path_test_output.txt', 'w') as f:
    f.write('STDOUT:\n')
    f.write(result.stdout)
    f.write('\n\nSTDERR:\n')
    f.write(result.stderr)

if result.returncode == 0:
    print(f'Exit code: {result.returncode}')
    print(f'Output saved to: path_test_output.txt')

    # Find JSON
    for line in result.stdout.split('\n'):
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            try:
                data = json.loads(line)
                if 'win_rate' in data:
                    print('\n' + '='*80)
                    print('✅ SUCCESS: ABSOLUTE PATH WITH BACKSLASHES WORKS!')
                    print('='*80)
                    print(f'Win Rate: {data["win_rate"]}%')
                    print(f'PNL: ${data["pnl"]["usd"]}')
                    print(f'Trades: {data["total_trades"]}')
                    print('='*80)
                    break
            except:
                pass
else:
    print(f'Exit code: {result.returncode}')
    print(f'Error: {result.stderr[:200]}')
