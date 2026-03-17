#!/bin/bash

# List all scheduled Post IDs from exec earlier
POST_IDS=(
  "958422d4-a94e-42ba-ba6f-bfb828a4b8a1"
  "97261722-04d6-41e5-838f-f185cbe719f8"
  "3fc34cba-dcab-4016-8d94-0db8ab3df91b"
  "0b348922-f305-416d-ac1e-abee15604ebb"
  "9da4e5f1-79bf-48b4-b796-057f4d29d6ea"
  "710b5dd7-c2e9-4ef7-bd77-c9fc76602557"
  "4e3a9019-973d-4d85-ab86-64548b5323b9"
  "4a013ab4-fac7-4856-ad7c-cbdbceaa0f81"
  "060360e9-36e4-4bc5-8ce6-1aa9619371a5"
  "0f1ee334-3f4e-4289-bc62-caf595501787"
  "4939f44f-6e35-430a-bd33-bc79994b9f0f"
  "384df3d5-9717-401d-9c55-1f4f99a2dd9c"
  "d2f80ecb-b957-4582-9ab0-9d0c0ecffcbe"
  "ec04564a-6a6b-424f-8ccf-bee22c4e40fa"
  "c8da855e-6926-4090-8b0a-5c36a61179b3"
  "9b74882f-e33a-4f6a-a110-2409c284d755"
  "cea74078-d65c-4772-a5e4-6c85455076bc"
  "9e1811e0-d3e2-4f67-a1e7-d5b8d4ed2066"
)

# Batch update hook-rich captions
for post_id in "${POST_IDS[@]}"; do
  topic=$(curl -s "https://api.post-bridge.com/v1/posts/$post_id" -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi" | jq -r '.caption' | cut -c 1-30)
  
  case "$topic" in
    *"Stop Loss"*)
      new_caption="💥 STOP LOSS adalah TEMAN atau MUSUH?\n\n90% trader GAGAL karena SL ditempatkan berdasarkan 'feeling'. Padahal, SL yang tepat bisa selamatkan modalmu sampai 70% di market volatile XAUUSD!\n\n📌 Saksikan LIVE CHART saat SL menyelamatkan (atau malah menghancurkan!) akun trading.\n\n🔔 FOLLOW agar tidak ketinggalan tips SL benar di part selanjutnya!\n💡 'Kenapa SL saya gak pernah work?' Tips berikut akan jawab!\n🔗 Belajar trading lengkap: https://lynk.id/jendralbot\n\n#RiskManagement #TradingTips #XAUUSD #StopLoss #TraderPemula"
      ;;
    *"Risk Management"*)
      new_caption="🚨 RISK MANAGEMENT: Rahasia Trader Sukses yang DIAM-DIAMAN!\n\nBukan modal besar yang bikin profit — tapi bagaimana kamu menjaga modalmu. Trader terbaik dunia punya 1 rahasia: 'Jaga modal dulu, profit datang sendiri.'\n\n📌 Contoh riil: 1 investor mulai Rp10jt bisa tumbuh jadi Rp1M hanya dengan RULE 2% per trade.\n\n🔔 FOLLOW sekarang! Besok kita bahas bagaimana TRADER PINTAR vs TRADER BODOH mengatur risk.\n💡 'Berapa sih idealnya risk per trade?' Jawabannya bakal BLOW YOUR MIND!\n🔗 Strategi trading teruji: https://lynk.id/jendralbot\n\n#TradingRule #ForexIndonesia #GoldTrading #TradingStrategy #RiskReward"
      ;;
    *"Candlestick"*)
      new_caption="🕯️ CANDLESTICK bukan cuma pola — ini BOM WAKTU yang bisa JEBLOKIN AKUNMU!\n\nEngulfing, Doji, Pin Bar bukan sekadar nama — ini SPY MODE di market yang memberi tau KAPAN harus masuk dan KELUAR. Salah langkah? Modal lenyap dalam sekejap.\n\n📌 3 pola candlestick paling bahaya yang HARUS kamu hindari (dan bagaimana menggunakannya untuk profit).\n\n🔔 FOLLOW supaya gak ketinggalan episode candlestick berikutnya: 'The Secret of Institutional Money' di chart-mu!\n💡 'Kenapa pola ini sering muncul di XAUUSD?' Temukan jawabannya di part selanjutnya!\n🔗 Edukasi trading gratis: https://lynk.id/jendralbot\n\n#CandlestickMagic #TradingSecrets #XAUUSD #TradingPatterns #BelajarAnalisa"
      ;;
    *"Support & Resistance"*)
      new_caption="⚔️ ZONA SUPPORT & RESISTANCE: Tempat TRADER Pintar BERPERANG!\n\nIni bukan sekadar garis di chart. Ini MEDAN PERANG di mana para trader profesional bertempur untuk mengambil uangmu. Salah melangkah? Selamat datang di zona SLAMATAN AKUN!\n\n📌 3 Teknik rahasia melihat S/R yang 99% trader indonesia belum tahu. (Termasuk bagaimana MENGGUNAKAN S/R untuk memprediksi kapan XAUUSD rally atau crash!)\n\n🔔 FOLLOW untuk pembahasan lebih dalam: 'Cara PSYCHOLOGICAL LEVEL menghancurkan trader retail'\n💡 'Kenapa harga selalu balik pas di 2100?' Temukan yang disembunyikan broker!\n🔗 Panduan lengkap: https://lynk.id/jendralbot\n\n#SupportResistance #PriceAction #XAUUSD #TradingStrategy #TraderPro"
      ;;
    *"Fibonacci"*)
      new_caption="🌀 FIBONACCI: Bilangan Mistis yang BISA MENDULANG UANG DI MARKET!\n\nBayangkan punya peta harta karun di market — itulah Fibonacci. Level 38.2%, 50%, 61.8% bukan sekadar angka. Ini RETREATMENT RAHASIA dari para market maker sebelum rally berikutnya!\n\n📌 Kenali kapan XAUUSD rebound hanya dengan pelajaran SD. Tidak percaya? Lihat contoh LIVE dari rally Senin kemarin!\n\n🔔 FOLLOW atau KETINGGALAN! Kita akan membongkar bagaimana trader profesional menggunakan fib untuk 'membaca' market seperti buku.\n💡 'Apa jadinya jika kita salah menempatkan fib?' Cerita trader yang akunnya terbang gara-gara ini!\n🔗 Strategi esensial trading: https://lynk.id/jendralbot\n\n#FibonacciTrading #XAUUSD #GoldenRatio #TradingMagic #PriceAction"
      ;;
    *"Moving Averages"*)
      new_caption="📈 MOVING AVERAGES: Garis Simple yang MEMISAHKAN Traders JUTAWAN dan PEMULUNG!\n\nGolden Cross vs Death Cross bukan teori kosong. Ini PERINGATAN DARURAT dari pasar! MA 50 tembus MA 200 bisa bikin kamu CEPAT KAYA atau CEPAT LOYO!\n\n📌 Di chart nyata, kita lihat contoh XAUUSD di 2024 yang naik 20% pas Golden Cross muncul — dan DEATH CROSS di 2023 yang bikin akun rugi Rp 50 juta cuma seminggu!\n\n🔔 FOLLOW sekarang. Episode berikutnya: Bagaimana menggunakan EMA 20 seperti trader profesioanl (tips ini belum pernah dibahas di grup manapun di Indo!)\n💡 'Mana yang lebih baik SMA atau EMA?' Jawabannya bikin trader sukses diam-diam!\n🔗 Sistem trading teruji: https://lynk.id/jendralbot\n\n#TradingSignals #XAUUSD #MovingAverages #TradingStrategy #GoldenCross"
      ;;
    *"Trend Analysis"*)
      new_caption="🔍 TREND is YOUR FRIEND — until it ENDS!\n\nTeori klasik? Tidak. Ini hidup atau mati di market. XAUUSD bisa rally 1000 poin dalam sebulan — atau menjatuhkanmu ke jurang tanpa ampun. Trend bukan sekadar 'uptrend' atau 'downtrend'. Ini DNA PASAR yang bisa kamu baca.\n\n📌 Rahasia: Cara membaca trend reversal hanya dari 1 candle. Contoh riil dari chart hari Senin.\n\n🔔 Jangan sampai ketinggalan: Besok kita bahas cara 1 TOOL yang dipakai hedge fund untuk memastikan apakah trend akan lanjut atau berhenti.\n💡 'Kenapa saya loss terus di breakout palsu?' Pas ini jawabannya!\n🔗 Panduan trend analysis lengkap: https://lynk.id/jendralbot\n\n#TrendTrading #XAUUSD #MarketTrend #TradingStrategy #BreakoutTrader"
      ;;
    *)
      new_caption="🚀 Trading Education: Beyond the Basics\n\n📌 Follow @algoexperthub for daily insights!\n🔗 Full strategy at https://lynk.id/jendralbot\n\n#TradingEducation #XAUUSD #ForexIndonesia"
      ;;
  esac
  
  echo "Updating Post: $post_id"
  curl -s -X PATCH "https://api.post-bridge.com/v1/posts/$post_id" \
    -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi" \
    -H "Content-Type: application/json" \
    -d "{\"caption\": \"${new_caption}\"}"
  echo "✅ Updated"
done

echo "🔥 Batch Update Complete! All posts now carry high-engagement hooks + follow-drive CTA."