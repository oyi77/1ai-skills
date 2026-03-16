#!/usr/bin/env python3
"""
Create new Telegram bot via @BotFather using Telethon - with retry logic
"""

import asyncio
import os
import re
from telethon import TelegramClient

# Telegram API credentials
API_ID = 23913448
API_HASH = "78d168f985edf365a5cd9679a917a0b2"

# Session file path
SESSION_PATH = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo"

# Bot details - multiple username options
BOT_NAME = "OpenClaw SaaS Bot"
USERNAMES = [
    "berkahkarya_saas_bot",
    "bk_saas_bot",
    "clawd_saas_bot",
    "vilona_ai_bot",
    "openclaw_video_bot",
    "ai_video_saas_bot",
]

async def try_create_bot(client, botfather, username):
    """Try to create bot with specific username"""
    print(f"\n🔄 Trying username: @{username}")
    
    # Send /newbot command
    await client.send_message(botfather, '/newbot')
    await asyncio.sleep(2)
    
    # Send bot name
    await client.send_message(botfather, BOT_NAME)
    await asyncio.sleep(1)
    
    # Send bot username
    await client.send_message(botfather, username)
    await asyncio.sleep(3)
    
    # Get response
    responses = await client.get_messages(botfather, limit=1)
    final_response = responses[0].text
    
    # Check if success or taken
    if "Sorry, this username is already taken" in final_response:
        print(f"❌ @{username} is taken")
        return None, None
    
    # Extract token
    token_pattern = r'(\d{9,10}:[A-Za-z0-9_-]{35})'
    match = re.search(token_pattern, final_response)
    
    if match:
        token = match.group(1)
        print(f"✅ SUCCESS! Bot created: @{username}")
        return token, username
    
    print(f"❌ Unexpected response: {final_response[:100]}")
    return None, None

async def create_bot():
    """Create new bot via @BotFather"""
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    
    try:
        print("🔌 Connecting to Telegram...")
        await client.connect()
        
        if not await client.is_user_authorized():
            print("❌ Session not authorized!")
            return None, None
        
        me = await client.get_me()
        print(f"✅ Connected as: {me.first_name} (@{me.username})")
        
        # Get BotFather
        print("\n🤖 Contacting @BotFather...")
        botfather = await client.get_entity('BotFather')
        print(f"✅ Found @BotFather")
        
        # Try each username
        for username in USERNAMES:
            token, successful_username = await try_create_bot(client, botfather, username)
            
            if token:
                # Save to file
                token_file = '/home/openclaw/.openclaw/workspace/temp/saas_bot_token.txt'
                with open(token_file, 'w') as f:
                    f.write(f"BOT_TOKEN={token}\n")
                    f.write(f"BOT_USERNAME=@{successful_username}\n")
                    f.write(f"BOT_NAME={BOT_NAME}\n")
                
                print(f"\n✅ Token saved to: {token_file}")
                
                # Set bot description
                await client.send_message(botfather, '/setdescription')
                await asyncio.sleep(1)
                await client.send_message(botfather, f'@{successful_username}')
                await asyncio.sleep(1)
                await client.send_message(botfather, '🎬 AI Video Marketing SaaS Platform - Create viral marketing videos from product photos!')
                await asyncio.sleep(1)
                print("✅ Bot description set")
                
                return token, successful_username
        
        print("\n❌ All usernames are taken!")
        return None, None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None
    finally:
        await client.disconnect()

if __name__ == "__main__":
    print("="*50)
    print("🤖 OPENCLAW SAAS BOT CREATOR v2")
    print("="*50)
    print(f"Bot Name: {BOT_NAME}")
    print(f"Trying usernames: {', '.join(USERNAMES)}")
    print("="*50)
    
    token, username = asyncio.run(create_bot())
    
    if token:
        print("\n" + "="*50)
        print("🎉 SUCCESS! Bot created!")
        print("="*50)
        print(f"BOT_TOKEN={token}")
        print(f"BOT_USERNAME=@{username}")
        print("="*50)
