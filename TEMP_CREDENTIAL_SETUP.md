# TIKTOK CREDENTIAL SETUP
**Phase 1 - Step 1.2**

---

## INSTRUCTIONS

TikTok account information needed for automation setup.

---

## REQUIRED CREDENTIALS

```
Username: _________________________
Password: _________________________
```

---

## CONFIGURATION FILE

Edit: `skills/tiktok-automation/config.json`

```json
{
  "credentials": {
    "username": "YOUR_USERNAME_HERE",
    "password": "YOUR_PASSWORD_HERE",
    "sessionFile": "tiktok-session.json"
  },
  "upload": {
    "defaultPrivacy": "public",
    "allowComments": true,
    "allowDuet": true,
    "allowStitch": true
  },
  "browser": {
    "headless": false,
    "timeout": 30000
  }
}
```

---

## SECURITY NOTES

⚠️ **IMPORTANT:** These credentials will be stored in `config.json`
- Make sure this file is NOT committed to git
- File is in: `skills/tiktok-automation/config.json`
- Git ignore should be configured properly

---

## ACCOUNT INFORMATION

**Current Status:**
- Existing TikTok: ✅ (mentioned in context)
- Automation access: ⏳ Needs verification
- API access: ⏳ Not required (using browser automation)

---

## NEXT STEPS

After credentials added:
1. Test manual login via browser
2. Run automation skill test
3. Verify session persistence
4. Proceed to Step 1.3-1.4

---

**Fill in credentials below or add directly to config.json**

**Username:** `_____________________`
**Password:** `_____________________`

*Note: Password will be saved in clear text in config.json*