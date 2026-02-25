#!/bin/bash
# MT5 SETUP COMMAND - JALANKAN INI DI SERVER ANDA

echo "================================================================================"
echo "MT5 LINUX DOCKER SETUP - MANUAL INSTRUCTIONS"
echo "================================================================================"
echo

echo "STEP 1: Login ke server Anda"
echo "   ssh root@5.189.138.144"
echo "   Password: raimuasu"
echo

echo "STEP 2: Copy paste script di bawah ini ke server"
echo "   Atau download dari: [URL jika ada]"
echo

echo "================================================================================"
echo "SCRIPT YANG PERLU DIJALANKAN DI SERVER:"
echo "================================================================================"
echo

cat mt5_remote_setup.sh | base64 -w0

echo
echo "================================================================================"
echo "CARA JALANKAN SCRIPT DI SERVER:"
echo "================================================================================"
echo

echo "Option 1: Copy paste langsung"
echo "   1. Copy script di atas (base64 encoded)"
echo "   2. Login ke server: ssh root@5.189.138.144"
echo "   3. Paste dan jalankan: echo 'PASTE_BASE64_HERE' | base64 -d | bash"
echo

echo "Option 2: Transfer file"
echo "   1. Copy file ini ke server:"
echo "      scp mt5_remote_setup.sh root@5.189.138.144:/root/"
echo "   2. Login ke server: ssh root@5.189.138.144"
echo "   3. Jalankan: bash /root/mt5_remote_setup.sh"
echo

echo "Option 3: Download dari web (jika available)"
echo "   1. Jalankan di server:"
echo "      curl -fsSL [URL_SCRIPT] | bash"
echo

echo
echo "================================================================================"
echo "SETELAH SETUP SELESAI:"
echo "================================================================================"
echo

echo "✅ Docker akan terinstall"
echo "✅ MT5 container akan berjalan"
echo "✅ Python MetaTrader5 API akan terinstall"
echo "✅ Trading bot akan siap"
echo

echo
echo "================================================================================"
echo "NEXT STEPS:"
echo "================================================================================"
echo

echo "1. Update trading bot dengan Account ID Fusion Markets:"
echo "   - Login ke Fusion Markets cTrader/MT5 Webtrader"
echo "   - Cari Account ID di Settings/Account"
echo "   - Edit: /root/mt5/xauusd_asia7c_bot.py"
echo "   - Ganti: LOGIN = 12345678"
echo "   - Dengan: LOGIN = [ACCOUNT_ID_FUSION_MARKETS]"
echo

echo "2. Jalankan bot:"
echo "   - docker exec -it mt5 bash"
echo "   - python3 /root/mt5/xauusd_asia7c_bot.py"
echo

echo "3. Bot akan berjalan 24/7 dan trade otomatis!"
echo

echo
echo "================================================================================"
echo "READY TO SETUP MT5 AUTOMATED TRADING!"
echo "================================================================================"
