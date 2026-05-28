#!/usr/bin/env python3
"""
Ring a Telegram user (alert call) — rings for N seconds then auto-hangs up.
Usage: python3 ring_call.py @username 10
"""
import asyncio, hashlib, random, sys
from telethon import TelegramClient
from telethon.tl.functions.phone import RequestCallRequest, DiscardCallRequest
from telethon.tl.types import (
    PhoneCallProtocol, PhoneCallDiscardReasonHangup, InputPhoneCall
)

SESSION = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session"
API_ID = 23913448
API_HASH = "REDACTED_ROTATED_CREDENTIAL"

# Telegram's standard 2048-bit DH prime
DH_PRIME = int(
    "C71CAEB9C6B1C9048E6C522F70F13F73980D40238E3E21C14934D037563D930F"
    "48198A0AA7C14058229493D22530F4DBFA336F6E0AC925139543AED44CCE7C37"
    "20FD51F69458705AC68CD4FE6B6B13ABDC9746512969328454F18FAF8C595F64"
    "2477FE96BB2A941D5BCD1D4AC8CC49880708FA9B378E3C4F3A9060BEE67CF9A4"
    "A4A695811051907E162753B56B0F6B410DBA74D8A84B2A14B3144E0EF1284754"
    "FD17ED950D5965B4B9DD46582DB1178D169C6BC465B0D6FF9CA3928FEF5B9AE4"
    "E418FC15E83EBEA0F87FA9FF5EED70050DED2849F47BF959D956850CE929851F"
    "0D8115F635B105EE2E4E15D04B2454BF6F4FADF034B10403119CD8E3B92FCC5B", 16
)


async def ring(username: str, ring_seconds: int = 8):
    """Ring a Telegram user for N seconds then hang up."""
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    user = await client.get_input_entity(username)

    # DH key exchange setup
    a = random.randint(2, DH_PRIME - 2)
    g_a = pow(3, a, DH_PRIME)
    g_a_bytes = g_a.to_bytes(256, 'big')
    g_a_hash = hashlib.sha256(g_a_bytes).digest()

    protocol = PhoneCallProtocol(
        min_layer=92, max_layer=92,
        udp_p2p=True, udp_reflector=True,
        library_versions=["3.0.0"]
    )

    result = await client(RequestCallRequest(
        user_id=user,
        g_a_hash=g_a_hash,
        protocol=protocol,
        video=False,
        random_id=random.randint(0, 0x7FFFFFFF)
    ))

    call = result.phone_call
    print(f"🔔 RINGING {username} (id={call.id})...", flush=True)
    await asyncio.sleep(ring_seconds)

    await client(DiscardCallRequest(
        peer=InputPhoneCall(id=call.id, access_hash=call.access_hash),
        duration=0,
        reason=PhoneCallDiscardReasonHangup(),
        connection_id=0
    ))
    print(f"📵 Hung up after {ring_seconds}s", flush=True)
    await client.disconnect()


async def ring_with_dm(username: str, message: str, ring_seconds: int = 8):
    """Send DM then ring as escalation."""
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    await client.send_message(username, message)
    print(f"💬 DM sent to {username}", flush=True)

    await client.disconnect()
    await ring(username, ring_seconds)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "@alwayscuanbos"
    seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    asyncio.run(ring(target, seconds))
