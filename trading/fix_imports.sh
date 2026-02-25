#!/bin/bash
# Fix all relative imports in trading package

TRADING_DIR="/home/openclaw/.openclaw/workspace/skills/1ai-skills/trading"

echo "Fixing relative imports..."

# Fix "from brokers." to "from ..brokers."
find "$TRADING_DIR" -name "*.py" -type f -exec sed -i 's/^from brokers\./from ..brokers./g' {} \;

# Fix "from indicators." to "from ..indicators." (in strategy files)
find "$TRADING_DIR/strategy" -name "*.py" -type f -exec sed -i 's/^from indicators\./from ...indicators./g' {} \;

# Fix "from data." to "from ..data."
find "$TRADING_DIR" -name "*.py" -type f -exec sed -i 's/^from data\./from ..data./g' {} \;

# Fix "from risk." to "from ..risk."
find "$TRADING_DIR" -name "*.py" -type f -exec sed -i 's/^from risk\./from ..risk./g' {} \;

# Fix "from utils." to "from ...utils." (in strategy files) or "..utils." (in trading root)
find "$TRADING_DIR/strategy" -name "*.py" -type f -exec sed -i 's/^from utils\./from ...utils./g' {} \;
find "$TRADING_DIR" -maxdepth 1 -name "*.py" -type f -exec sed -i 's/^from utils\./from .utils./g' {} \;

echo "✅ Imports fixed!"
