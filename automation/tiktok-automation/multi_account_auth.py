#!/usr/bin/env python3
"""
JENDRALBOT Multi-Account TikTok Auth
Login satu-satu ke 12 TikTok accounts
Handle OTP/Email verification manual
"""

import asyncio
import json
from pathlib import Path

# Config
CONFIG_FILE = Path(
    "/home/openclaw/.openclaw/workspace/skills/tiktok-automation/multi_account_config.json"
)
SELECTORS_FILE = Path(
    "/home/openclaw/.openclaw/workspace/skills/tiktok-automation/selectors.json"
)
ASSETS_DIR = Path("/home/openclaw/.openclaw/workspace/skills/tiktokautomation/assets")


def load_config():
    """Load multi-account config"""
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


async def login_single_account(account: dict, playwright_context):
    """
    Login ke satu TikTok account
    Return session data atau error
    """
    username = account["username"]
    password = account["password"]

    try:
        # Set viewport mobile portrait 9:16
        await playwright_context.set_viewport_size(1080, 1920)
        await playwright_context.set_user_agent(
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        )

        # Buat browser context
        browser = await playwright_context.new_browser(
            headless=False,  # Visible untuk OTP/Email verification
            slow_mo=1000,  # Sedikit delay agar visible
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            viewport={"width": 1080, "height": 1920},
            locale="id-ID",
            timezone="Asia/Jakarta",
        )

        page = await context.new_page()

        print(f"🌐 Navigating ke TikTok login...")
        await page.goto(
            "https://www.tiktok.com/login", wait_until="networkidle", timeout=30000
        )

        # Tunggu halaman login load
        await asyncio.sleep(3)

        # Input username
        print(f"📝 Input username: {username}")
        username_input = await page.wait_for_selector(
            'input[name="username"]', timeout=10000
        )
        if username_input:
            await username_input.click()
            await username_input.type(username)
        else:
            # Alternative selector
            await page.fill('input[placeholder*="Username"]', username)

        # Input password
        print(f"🔑 Input password: {'*' * 10}")  # Masked
        password_input = await page.wait_for_selector(
            'input[name="password"]', timeout=10000
        )
        if password_input:
            await password_input.click()
            await password_input.type(password)
        else:
            # Alternative selector
            await page.fill('input[placeholder*="Password"]', password)

        # Submit login
        print(f"📤 Submit login...")
        submit_button = await page.wait_for_selector(
            'button[type="submit"]', timeout=10000
        )
        if submit_button:
            await submit_button.click()
        else:
            # Alternative - press Enter di password field
            await page.keyboard.press("Enter")

        # Tunggu login proses
        print(f"⏳ Waiting for login process...")
        await asyncio.sleep(5)

        # Cek apakah butuh OTP/Email verification
        current_url = page.url
        current_content = await page.content()

        need_otp = False
        need_email = False

        # Check OTP indicators
        if "otp" in current_url.lower() or "verification" in current_url.lower():
            need_otp = True
        elif (
            "two-factor" in current_content.lower() or "2fa" in current_content.lower()
        ):
            need_otp = True

        # Check Email indicators
        if "email" in current_url.lower() and "verify" in current_url.lower():
            need_email = True
        elif (
            "check your email" in current_content.lower()
            or "email code" in current_content.lower()
        ):
            need_email = True

        if need_otp:
            print(f"\n⚠️ OTP VERIFICATION REQUIRED!")
            print(f"   Account: @{username}")
            print(f"   Boss, cek email/hp untuk OTP code")
            print(f"   Input OTP code manual:")

            # Input OTP manual
            otp_input = input("   OTP CODE: ")

            # Submit OTP
            otp_field = await page.wait_for_selector(
                'input[placeholder*="code"]', timeout=10000
            )
            if otp_field:
                await otp_field.type(otp_input)
                submit_otp = await page.wait_for_selector(
                    'button[type="submit"]', timeout=10000
                )
                if submit_otp:
                    await submit_otp.click()

            await asyncio.sleep(5)

        if need_email:
            print(f"\n⚠️ EMAIL VERIFICATION REQUIRED!")
            print(f"   Account: @{username}")
            print(f"   Boss, cek email untuk verification code/link")
            print(f"   Lalu continue di browser.")

            # Tunggu boss manual verification di browser
            print(f"\n   ⏳ Menunggu boss complete verification...")
            print(f"   Tekan ENTER setelah verification complete:")
            input("   (TEKAN ENTER)")

            await asyncio.sleep(3)

        # Cek login success
        await asyncio.sleep(3)
        final_url = page.url

        if "login" not in final_url.lower():
            # Login success!
            print(f"✅ LOGIN SUKSES: @{username}")

            # Save session
            session_data = await context.storage_state()
            session_file = Path(
                f"/home/openclaw/.openclaw/workspace/skills/tiktok-automation/sessions/{username}_session.json"
            )
            session_file.parent.mkdir(parents=True, exist_ok=True)

            with open(session_file, "w") as f:
                json.dump(session_data, f, indent=2)

            print(f"💾 Session saved: {session_file}")

            return {
                "username": username,
                "success": True,
                "session_file": str(session_file),
            }
        else:
            print(f"❌ LOGIN GAGAL: @{username}")
            return {
                "username": username,
                "success": False,
                "error": "Login failed - please try manual login",
            }

        # Close browser
        await browser.close()

    except Exception as e:
        print(f"❌ ERROR pada @{username}: {str(e)}")
        return {"username": username, "success": False, "error": str(e)}


async def multi_account_login():
    """
    Login ke semua 12 TikTok accounts satu-satu
    """
    config = load_config()
    accounts = config["accounts"]

    print("\n" + "=" * 80)
    print("🚀 JENDRALBOT - MULTI-ACCOUNT TIKTOK AUTH")
    print("=" * 80)
    print(f"📱 Total accounts: {len(accounts)}")
    print(f"⏱️ Estimated time: {len(accounts) * 2-3} minutes")
    print("=" * 80 + "\n")

    from playwright.async_api import async_playwright

    async with async_playwright() as playwright_context:
        results = []

        for i, account in enumerate(accounts):
            print(f"\n🔐 ACCOUNT {i+1}/{len(accounts)}")
            print(f"   Username: @{account['username']}")
            print(f"   Niche: {account['niche']}")

            result = await login_single_account(account, playwright_context)
            results.append(result)

            # Delay sebelum next account
            if i < len(accounts) - 1:
                print(f"\n⏸️ Waiting 3 seconds before next account...")
                await asyncio.sleep(3)

        # Summary
        print("\n" + "=" * 80)
        print("📊 MULTI-ACCOUNT LOGIN SUMMARY")
        print("=" * 80)

        success_count = sum(1 for r in results if r["success"])
        fail_count = len(results) - success_count

        print(f"✅ Successful logins: {success_count}/{len(accounts)}")
        print(f"❌ Failed logins: {fail_count}/{len(accounts)}")

        if fail_count > 0:
            print(f"\n⚠️ Failed accounts:")
            for result in results:
                if not result["success"]:
                    print(
                        f"   - @{result['username']}: {result.get('error', 'Unknown error')}"
                    )

        print("\n💾 Session files saved to:")
        print(
            f"   /home/openclaw/.openclaw/workspace/skills/tiktok-automation/sessions/"
        )

        print("\n✅ Ready untuk batch upload JENDRALBOT hooks!")
        print(
            "📈 Next step: Run multi_account_upload.py untuk upload semua hook frames\n"
        )


async def main():
    print("🎯 MULTI-ACCOUNT TIKTOK AUTH STARTING...")
    print("⚠️ Boss: Kalau butuh OTP/Email verification, siapkan kode/link!")

    try:
        await multi_account_login()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
