# 🚀 QUICK SETUP - Ostium Paper Trading

**ETA: 5 menit**

## Step 1: Export Private Key dari MetaMask (2 menit)

1. Buka MetaMask di browser
2. Klik nama akun kamu (top right)
3. Pilih **"Account Details"**
4. Klik **"Export Private Key"**
5. Masukkan password MetaMask kamu
6. Copy private key (biasanya mulai dengan `0x`)

⚠️ **PENTING:** Simpan private key dengan aman! Jangan share ke siapapun.

## Step 2: Paste Private Key (30 detik)

Edit file ini:
```bash
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading
nano .env.ostium
```

Ganti `YOUR_PRIVATE_KEY_HERE` dengan private key dari MetaMask:
```env
OSTIUM_PRIVATE_KEY=0x_AB_CDEF_123456_...  <-- Paste di sini
OSTIUM_RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
OSTIUM_TESTNET=true
```

Save: `Ctrl+O` lalu `Enter`, exit: `Ctrl+X`

## Step 3: Test Connection (30 detik)

```bash
~/.trading-venv/bin/python test_ostium_connector.py
```

Kalau sukses, kamu akan lihat:
```
✅ Connection successful
Wallet: 0x1234...
Balance: 0.00 USDC
```

## Step 4: Get Testnet USDC (2 menit)

Buka chat ini lagi setelah test berhasil, saya akan minta testnet USDC via faucet.

---

**YANG SUDAH SEDIA:**
- ✅ Ostium connector (FULLY UPDATED)
- ✅ Public RPC URL (gratis, ga perlu Alchemy)
- ✅ Test script siap jalan
- ✅ .env.ostium file sudah dibuat

**YANG KAMU PERLU:**
- ⏳ Private key dari MetaMask (Step 1)

---

**Mau saya bantu setup Alchemy account dengan browser automation setelah ini?**
(Butuh kamu klik extension OpenClaw di Chrome dulu)
