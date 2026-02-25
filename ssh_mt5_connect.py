#!/usr/bin/env python3
"""
SSH CONNECT TO MT5 SERVER
Automate SSH connection with password using pexpect
"""

import pexpect
import sys

# Server credentials
SERVER_IP = "5.189.138.144"
SSH_USER = "root"
SSH_PASSWORD = "raimuasu"

print("="*80)
print("SSH CONNECT TO MT5 SERVER")
print("="*80)
print()

print(f"🌐 Connecting to: {SSH_USER}@{SERVER_IP}")
print()

try:
    # Spawn SSH
    child = pexpect.spawn(f'ssh {SSH_USER}@{SERVER_IP}')
    
    # Wait for password prompt
    i = child.expect(['password:', 'Password:', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
    
    if i == 0 or i == 1:
        # Send password
        child.sendline(SSH_PASSWORD)
        print("✅ Password sent")
        
        # Wait for shell prompt
        child.expect(['#', '$', '>', ']', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        
        # Get hostname and OS info
        child.sendline('hostname')
        child.sendline('whoami')
        child.sendline('uname -a')
        child.sendline('cat /etc/os-release | head -5')
        
        # Wait and get output
        child.expect(['#', '$', '>', ']', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        output = child.before.decode()
        
        print()
        print("="*80)
        print("✅ CONNECTION SUCCESSFUL!")
        print("="*80)
        print()
        print("Server Information:")
        print(output)
        print()
        
        # Check if Docker is installed
        print("="*80)
        print("CHECKING DOCKER")
        print("="*80)
        print()
        
        child.sendline('which docker')
        child.expect(['#', '$', '>', ']', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        docker_check = child.before.decode()
        
        if 'docker' in docker_check.lower():
            print("✅ Docker is already installed")
            child.sendline('docker --version')
            child.expect(['#', '$', '>', ']', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
            docker_version = child.before.decode()
            print(docker_version)
        else:
            print("⚠️  Docker is NOT installed")
            print()
            print("📋 Installing Docker...")
            child.sendline('curl -fsSL https://get.docker.com -o get-docker.sh')
            child.sendline('sh get-docker.sh')
            child.expect(['#', '$', '>', ']', pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        
        print()
        print("="*80)
        print("MT5 DOCKER SETUP")
        print("="*80)
        print()
        print("📋 NEXT STEPS:")
        print()
        print("1. Pull MT5 Docker image:")
        print("   docker pull troyharvey/mt5:latest")
        print()
        print("2. Run MT5 in Docker:")
        print("   docker run -d \\")
        print("     --name mt5 \\")
        print("     --network host \\")
        print("     -e DISPLAY=$DISPLAY \\")
        print("     troyharvey/mt5:latest")
        print()
        print("3. Configure MT5:")
        print("   - Login to Fusion Markets MT5")
        print("   - Username: Openclaw@12")
        print("   - Password: 10100262")
        print("   - Server: FusionMarkets-Demo")
        print()
        print("4. Install Python API:")
        print("   pip install MetaTrader5")
        print()
        print("5. Implement Strategy:")
        print("   - XAUUSD Asia 7-Candle Breakout")
        print("   - Run 24/7 automated trading")
        print()
        print("="*80)
        print("CONNECTED - READY FOR MT5 SETUP")
        print("="*80)
        print()
        print("⏳ Keeping SSH session open...")
        print("   Type 'exit' to disconnect")
        print()
        
        # Interact with shell
        child.interact()
        
    elif i == 2:
        print("❌ Connection closed or timeout")
        sys.exit(1)
    elif i == 3:
        print("❌ Timeout while waiting for password prompt")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
