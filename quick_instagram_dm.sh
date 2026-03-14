#!/bin/bash
# Quick Instagram DM Helper - Generate DM scripts

echo "📱 INSTAGRAM DM HELPER"
echo ""

# Get Instagram handles from campaign
echo "Finding Instagram handles from campaign..."
grep -i "instagram" lead_gen_machine/campaigns/campaign_traveloka_manual_20260307_004753.json | grep -oP '(?<="instagram": ")[^,}]+(?=",")|' | head -5
echo ""

# Generate DM script for top 3 restaurants
cat << 'EOF'
INSTAGRAM DM SCRIPT

Copy this and send to restaurant owners via Instagram:

---

Hi [RESTAURANT NAME]! 👋

Saya lihat [RESTAURANT NAME] di Traveloka - rating [RATING]⭐ dengan [REVIEWS] reviews! Mengesankan! 🎉

Quick question: Apakah Anda ingin meningkatkan jumlah reservasi dan mendapatkan lebih banyak customer?

Saya bantu restoran Jakarta sepenuhnya mengotomatisasi marketing mereka:

✅ Social media automation (5 platforms sekaligus)
✅ Customer acquisition (50-100+ new inquiries/reservasi per bulan)
✅ Content creation (food photography, video reviews, menu highlights, stories)
✅ Marketing automation (hemat 15+ jam/minggu waktu marketing)

Hasil nyata dari restoran Jakarta sejenis:
• +250% lebih banyak reservasi dan order
• +200% engagement di social media
• 50-100+ customer baru per bulan
• Hemat 15-20 jam/minggu waktu marketing

Worth a quick 15-min chat untuk lihat apa yang bisa saya lakukan untuk [RESTAURANT NAME]?

Hubungi:
• WhatsApp: +62 XXX XXX XXX [YOUR NUMBER]
• Email: [YOUR_EMAIL]
• Calendar: [YOUR CALENDAR LINK]

Tunggu balasan! 🚀

---

EOF