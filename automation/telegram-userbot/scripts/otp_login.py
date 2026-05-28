#!/usr/bin/env python3
"""
One-time MTProto login with base64 OTP trick.
Run this, wait for WAITING status, then:
  echo -n "OTPCODE" | base64   → encode
  echo "BASE64STR" | base64 -d > /tmp/tg_code.txt  → inject
"""
import asyncio, os, time
from telethon import TelegramClient

SESSION = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session"
API_ID = 23913448
API_HASH = "REDACTED_ROTATED_CREDENTIAL"
PHONE = "+6281347241993"


async def main():
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"ALREADY_LOGGED_IN|{me.first_name}|@{me.username}")
        await client.disconnect()
        return

    r = await client.send_code_request(PHONE)
    h = r.phone_code_hash
    open("/tmp/tg_hash.txt", "w").write(h)
    open("/tmp/tg_status.txt", "w").write(f"WAITING|{h}")
    print(f"OTP_SENT|hash={h}", flush=True)
    print("WAITING_CODE — encode OTP with: echo -n 'CODE' | base64", flush=True)
    print("Then inject: echo 'BASE64' | base64 -d > /tmp/tg_code.txt", flush=True)

    deadline = time.time() + 110
    while time.time() < deadline:
        if os.path.exists("/tmp/tg_code.txt"):
            code = open("/tmp/tg_code.txt").read().strip()
            os.remove("/tmp/tg_code.txt")
            print(f"GOT_CODE:{code}", flush=True)
            try:
                await client.sign_in(PHONE, code, phone_code_hash=h)
                me = await client.get_me()
                result = f"OK|{me.first_name}|@{me.username}|{me.id}"
                open("/tmp/tg_result.txt", "w").write(result)
                open("/tmp/tg_status.txt", "w").write(result)
                print(f"SUCCESS:{result}", flush=True)
            except Exception as e:
                open("/tmp/tg_status.txt", "w").write(f"ERR|{e}")
                print(f"ERR:{e}", flush=True)
            break
        await asyncio.sleep(1)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
