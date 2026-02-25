#!/bin/bash
# Setup MT5Linux on remote server

echo "============================================"
echo "MT5Linux Docker Setup"
echo "============================================"
echo

# Clone repository
cd /root
git clone https://github.com/lucas-campagna/mt5linux.git
cd mt5linux/docker

# Build Docker image
echo "Building MT5Linux Docker image..."
docker build -t mt5linux .

# Run container
echo "Running MT5Linux container..."
docker run -d \
  --name mt5linux \
  -p 6080:6080 \
  -v /root/mt5_data:/mt5 \
  mt5linux

echo
echo "============================================"
echo "MT5Linux Setup Complete!"
echo "============================================"
echo
echo "Access MT5 via browser:"
echo "  http://5.189.138.144:6080"
echo
echo "Next steps:"
echo "1. Open browser to the URL above"
echo "2. Login to Fusion Markets MT5"
echo "3. Install MetaTrader5 Python package"
echo "4. Run automated trading bot"
echo
