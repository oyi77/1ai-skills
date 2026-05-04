#!/usr/bin/env python3
"""Automated Discord Server Creator using Discord API"""

import requests
import json
import os

def create_discord_server():
    """Create Discord server via API"""
    
    token = os.environ.get('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ Need Discord bot token")
        print("Create at: https://discord.com/developers/applications")
        return
    
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    
    # Create guild
    guild_data = {
        "name": "1ai-Skills Hub",
        "region": "us-west",
        "icon": None  # Could add base64 icon
    }
    
    response = requests.post(
        "https://discord.com/api/v10/guilds",
        headers=headers,
        json=guild_data
    )
    
    if response.status_code == 201:
        guild = response.json()
        print(f"✅ Server created: {guild['name']}")
        print(f"ID: {guild['id']}")
        
        # Create categories
        categories = [
            "📢 INFORMATION",
            "💬 DISCUSSION", 
            "🎯 SKILL CATEGORIES",
            "🔧 SUPPORT",
            "🎓 ADVANCED"
        ]
        
        for category in categories:
            requests.post(
                f"https://discord.com/api/v10/guilds/{guild['id']}/channels",
                headers=headers,
                json={
                    "name": category,
                    "type": 4  # Category
                }
            )
        
        print("✅ Categories created")
        print("📝 Manual steps:")
        print("   1. Set up channels in each category")
        print("   2. Configure permissions")
        print("   3. Create invite link")
        
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    create_discord_server()
