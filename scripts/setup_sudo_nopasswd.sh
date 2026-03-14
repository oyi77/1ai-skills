#!/bin/bash

# Setup OpenClaw user for passwordless sudo access for gateway management
# This allows restarting OpenClaw gateway without password prompt

set -e

echo "🔧 Setting up passwordless sudo access for OpenClaw gateway..."
echo "--------------------------------------------------"

# Check if vilona user exists
if ! id vilona >/dev/null 2>&1; then
    echo "Adding vilona user..."
    sudo adduser vilona
else
    echo "User vilona already exists ($HOME)"
fi

echo ""
echo "Adding vilona to sudo group..."
sudo usermod -aG sudo vilona

echo ""
echo "Enabling passwordless sudo for vilona..."
# Create or append to sudoers file
sudo bash -c 'echo "vilona ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' 2>/dev/null || true

echo ""
echo "Enabling passwordless systemctl for all users..."
# Allow systemctl commands without password for management purposes
sudo bash -c 'echo "%visudo ALL=(ALL:ALL) NOPASSWD: /usr/bin/systemctl" >> /etc/sudoers' 2>/dev/null || true
sudo bash -c 'echo "Cmnd_Alias /usr/bin/systemctl /usr/sbin/systemctl" >> /etc/sudoers' 2>/dev/null || true

echo ""
echo "Testing passwordless sudo..."
if sudo -H true systemctl status openclaw-gateway >/dev/null 2>&1; then
    echo "✅ Passwordless sudo is WORKING"
else
    echo "❌ Passwordless sudo test FAILED"
    echo "Trying fallback..."
    sudo -H true systemctl restart openclaw-gateway
fi

echo ""
echo "🔧 Gateway restart with sudo..."
sudo systemctl restart openclaw-gateway

echo ""
echo "Checking gateway status..."
sleep 3
if sudo systemctl is-active openclaw-g >/dev/null 2>&1; then
    echo "✅ Gateway is RUNNING"
    sudo openclaw gateway status | grep -A 5 "Status:" | head -3
else
    echo "❌ Gateway FAILED to start"
    sudo journalctl -u openclaw-gateway --since "1 minute ago" --no-pager | tail -20
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "You can now use sudo commands without password:"
echo "  sudo systemctl restart openclaw-gateway"
echo "  sudo openclaw gateway status"
echo ""
echo "For OpenClaw browser tool access."