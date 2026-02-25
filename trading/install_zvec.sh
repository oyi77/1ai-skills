#!/bin/bash
# VILONA ZVEC INSTALLATION

echo "================================================================================"
echo "ZVEC INSTALLATION FOR TRADING SYSTEM"
echo "================================================================================"
echo ""

# Try pip install from PyPI
echo "[1/4] Attempting pip install from PyPI..."
pip3 install zvec --quiet 2>&1 | head -10

if pip3 show zvec &> /dev/null; then
    echo "✅ ZVEC installed via pip!"
    python3 -c "import zvec; print('Version:', zvec.__version__)"
else
    echo "⚠️  pip install failed, trying from GitHub..."
    echo ""

    # Try installing from GitHub
    echo "[2/4] Cloning from GitHub..."
    git clone https://github.com/Zvc/binary.git /tmp/zvec_git 2>/dev/null || echo "❌ git clone failed (internet?)"

    # Try building from source
    echo "[3/4] Building from source..."
    cd /tmp/zvec_git 2>/dev/null || {
        echo "❌ git clone failed, creating directory..."
        mkdir -p /tmp/zvec_git
    }

    # Check if build files exist
    if [ -f "build.sh" ]; then
        echo "Found build.sh, running..."
        bash build.sh
    elif [ -f "setup.py" ]; then
        echo "Found setup.py, running..."
        pip3 install -e . --quiet
    else
        echo "❌ No build.sh or setup.py found"
        echo ""
        echo "[4/4] Installing zvec via pip with --break-system-packages..."
        pip3 install zvec --break-system-packages 2>&1 | head -10
fi

echo ""
echo "================================================================================"
echo "VERIFICATION"
echo "================================================================================"
echo ""

python3 -c "
try:
    import zvec
    print('✅ ZVEC installation SUCCESSFUL!')
    print('Version:', zvec.__version__)
    print()
    print('Available modules:')
    print('  - zvec.CollectionSchema')
    print('  - zvec.VectorSchema')
    print('  - zvec.create_and_open')
    print('  - zvec.open')
except ImportError as e:
    print('❌ ZVEC import FAILED:', e)
    print()
    print('Trying alternative installation...')
    import subprocess
    subprocess.run(['pip3', 'install', 'zvec', '--break-system-packages'], check=True)
"

echo ""
echo "================================================================================"
echo "COMPLETE"
echo "================================================================================"
