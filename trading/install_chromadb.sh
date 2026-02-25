#!/bin/bash
# VILONA CHROMADB INSTALLATION FOR TRADING

echo "================================================================================"
echo "CHROMADB INSTALLATION - BERKAHKARYA QUANT FUND"
echo "================================================================================"
echo ""

# Install ChromaDB
echo "[1/3] Installing ChromaDB..."
pip3 install chromadb --break-system-packages 2>&1 | grep -E "(Successfully|ERROR|error)" | head -5

# Verify installation
if pip3 show chromadb &> /dev/null; then
    echo "✅ ChromaDB installed successfully!"
    python3 -c "import chromadb; print('Version:', chromadb.__version__)"
else
    echo "❌ ChromaDB installation failed"
    exit 1
fi

echo ""
echo "[2/3] Testing ChromaDB..."

# Quick test
python3 -c "
import chromadb
import chromadb.utils as embedding_functions

# Create temporary client
client = chromadb.Client()

# Create collection
print('Creating test collection...')
test_collection = client.get_or_create_collection(name='trading_test')

# Add document
print('Adding test document...')
test_collection.add(
    documents=['XAUUSD Asia 7-Candle Breakout Strategy'],
    metadatas={'strategy': 'asia_7candle', 'pair': 'XAUUSD', 'win_rate': 61.4},
    ids=['test_doc_1']
)

print('✅ ChromaDB test successful!')
client.delete_collection('trading_test')
"

if [ $? -eq 0 ]; then
    echo "✅ ChromaDB test passed!"
else
    echo "❌ ChromaDB test failed"
    exit 1
fi

echo ""
echo "[3/3] Import XAUUSD backtest to ChromaDB..."

# Run Chroma integration script
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
~/.trading-venv/bin/python chroma_trading_db.py insert-xauusd --db-path ./chroma_trading_db 2>&1 | tail -20

echo ""
echo "================================================================================"
echo "INSTALLATION COMPLETE"
echo "================================================================================"
echo ""
echo "ChromaDB installed and initialized!"
echo ""
echo "Next steps:"
echo "1. Search best strategies: python3 chroma_trading_db.py search-best --pair XAUUSD"
echo "2. Search strategy code: python3 chroma_trading_db.py search-code --query 'breakout'"
echo "3. Insert trade journal: python3 chroma_trading_db.py insert-journal --pair XAUUSD ..."
echo "4. Search similar trades: python3 chroma_trading_db.py search-similar --pair XAUUSD ..."
echo ""
echo "================================================================================"
