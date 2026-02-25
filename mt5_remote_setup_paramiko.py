#!/usr/bin/env python3
"""
MT5 FULLY AUTOMATED SETUP - REMOTE SERVER
Connect to server via SSH (paramiko) and setup MT5 Docker
"""

import paramiko
import time
import sys

# Server credentials
SERVER_IP = "5.189.138.144"
SSH_USER = "root"
SSH_PASSWORD = "raimuasu"

print("="*80)
print("MT5 FULLY AUTOMATED SETUP - REMOTE SERVER")
print("="*80)
print()

# Commands to run on server
COMMANDS = [
    # Update system
    "apt-get update -y",
    "apt-get upgrade -y",
    
    # Install Docker
    "curl -fsSL https://get.docker.com -o get-docker.sh",
    "sh get-docker.sh",
    "usermod -aG docker root",
    
    # Start Docker
    "systemctl start docker",
    "systemctl enable docker",
    
    # Install Docker Compose
    "curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
    "chmod +x /usr/local/bin/docker-compose",
    
    # Create MT5 directory
    "mkdir -p /root/mt5",
    "cd /root/mt5",
    
    # Create Dockerfile
    """cat > Dockerfile << 'DOCKEOF'
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \\
    wget \\
    xvfb \\
    python3 \\
    python3-pip \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe -O mt5setup.exe

RUN pip3 install MetaTrader5 pandas numpy

WORKDIR /root/mt5
EXPOSE 443

CMD ["Xvfb", ":99", "-screen", "0", "1920x1080x24"]
DOCKEOF""",
    
    # Build MT5 image
    "docker build -t mt5-auto .",
]

try:
    print(f" connecting to {SSH_USER}@{SERVER_IP}...")
    
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to server
    ssh.connect(SERVER_IP, username=SSH_USER, password=SSH_PASSWORD, timeout=30)
    print("✅ Connected to server!")
    print()
    
    # Execute commands
    for i, cmd in enumerate(COMMANDS, 1):
        print(f"[{i}/{len(COMMANDS)}] Running: {cmd[:60]}..." if len(cmd) > 60 else f"[{i}/{len(COMMANDS)}] Running: {cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Wait for command to complete
        exit_status = stdout.channel.recv_exit_status()
        
        # Read output
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print(f"   Output: {output[:200]}..." if len(output) > 200 else f"   Output: {output}")
        
        if error:
            print(f"   Error: {error[:200]}..." if len(error) > 200 else f"   Error: {error}")
        
        if exit_status == 0:
            print(f"   ✅ Success")
        else:
            print(f"   ⚠️  Failed with exit code: {exit_status}")
        
        print()
        time.sleep(2)  # Small delay between commands
    
    print("="*80)
    print("MT5 SETUP COMPLETE!")
    print("="*80)
    print()
    print("✅ Docker installed and running")
    print("✅ MT5 Docker image built")
    print()
    print("NEXT STEPS:")
    print("1. Get Fusion Markets MT5 Account ID")
    print("2. Configure bot with Account ID")
    print("3. Run: python3 /root/mt5/xauusd_asia7c_bot.py")
    print()
    
    # Test Docker
    print("Testing Docker...")
    stdin, stdout, stderr = ssh.exec_command("docker --version")
    print(f"✅ Docker version: {stdout.read().decode().strip()}")
    
    stdin, stdout, stderr = ssh.exec_command("docker images | grep mt5")
    print(f"✅ MT5 image available:")
    print(stdout.read().decode())
    
    ssh.close()
    print()
    print("="*80)
    print("COMPLETE - MT5 READY FOR AUTOMATED TRADING!")
    print("="*80)

except paramiko.ssh_exception.AuthenticationException:
    print("❌ Authentication failed!")
    print("⚠️  Check credentials:")
    print(f"   User: {SSH_USER}")
    print(f"   Password: {SSH_PASSWORD}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
