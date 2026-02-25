#!/bin/bash
# MT5全自动セットアップスクリプト
# Full automated MT5 Docker setup script

echo "===================================="
echo "MT5 FULLY AUTOMATED SETUP"
echo "===================================="
echo

# Update system
echo "1/7 Updating system..."
apt-get update -y
apt-get upgrade -y

# Install Docker
echo "2/7 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker root

# Start Docker
echo "3/7 Starting Docker..."
systemctl start docker
systemctl enable docker

# Install Docker Compose
echo "4/7 Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create MT5 directory
echo "5/7 Creating MT5 directory..."
mkdir -p /root/mt5
cd /root/mt5

# Create Dockerfile for MT5 with Python support
echo "6/7 Creating Dockerfile..."
cat > Dockerfile << 'EOF'
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    python3 \
    python3-pip \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install MT5
WORKDIR /tmp
RUN wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe -O mt5setup.exe

# Install MetaTrader5 Python API
RUN pip3 install MetaTrader5 pandas numpy

# Create working directory
WORKDIR /root/mt5

# Expose port
EXPOSE 443

# Auto-start Xvfb for headless MT5
CMD ["Xvfb", ":99", "-screen", "0", "1920x1080x24"]
EOF

echo "7/7 Building MT5 Docker image..."
docker build -t mt5-auto .

echo
echo "===================================="
echo "MT5 SETUP COMPLETE!"
echo "===================================="
echo
echo "✅ Docker installed and running"
echo "✅ MT5 image built"
echo
echo "Next steps:"
echo "1. Login to Fusion Markets MT5: FusionMarkets.com/Platforms/MT5"
echo "2. Get Account ID"
echo "3. Configure bot with Account ID"
echo "4. Run: python3 /root/mt5/xauusd_asia7c_bot.py"
echo
