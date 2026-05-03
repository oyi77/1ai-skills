#!/usr/bin/env python3
"""
JENDRALBOT TikTok Hook Frame Auto-Uploader - DEMO VERSION

Fungsi: Upload hook frame ke TikTok sebagai foto post dengan caption + hashtags
"""

import asyncio
import glob
from pathlib import Path

# Config
ASSETS_DIR = Path("/home/openclaw/.openclaw/.openclaw/workspace/skills/tiktokautomation/assets")
CONFIG_PATH = Path("/home/openclaw/.openclaw/workspace/skills/tiktok-automation/config.json")

# JENDRALBOT PRODUCTS dengan caption dan hashtags
PRODUCTS = [
    {
        "name": "Belanja Tetap Jalan Tapi Du Tetap Balik",
        "price": "FREE",
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "caption": "GILA! BELANJA DU TETAP BALIK!",
        "hashtags": "#cashback #belanja #duitbalik #gratis #affiliate #viral #tiktok #fyp",
        "file": "belanja_duit_balik_hook1_shock.png"
    },
    {
        "name": "Belanja Tetap Jalan Tapi Du Tetap Balik",
        "price": "FREE",
        "link": "https://ynk.id/jendralbot/kkjk0mv1vg7o",
        "caption": "BELANJA PASTI HABIS DU?",
        "hashtags": "#cashbackbelanja #duit #cashback #solusi #affiliate",
        "file": "belanja_duit_balik_hook2_problem.png"
    },
    {
        "name": "Belanja Tetap Jalan Tapi Du Tetap Balik",
        "price": "FREE",
        "link": "https://ynk.id/jendralbot/kkjk0mv1vg7o",
        "caption": "Sistem Cashback Otomatis!",
        "hashtags": "#cashback #affiliate #gratis #viral",
        "file": "belanja_duit_balik_hook3_solution.png"
    },
    {
        "name": "Guru Pintar Ai",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/6821op5e24kn",
        "caption": "RAHASIA AI UNTUK GURU MODERN! 🤫",
        "hashtags": "#guru #pendidikan #ai #edukasi #guruai #panduan #teacher #viral",
        "file": "guru_pintar_ai_hook1_shock.png"
    },
    {
        "name": "Guru Pintar Ai",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/6821op5e24kn",
        "caption": "GURU PINTER TAPI NGGAK KENA AI?",
        "hashtags": "#guru #gurupintar #education #pedagok #gurukai",
        "file": "guru_pintar_ai_hook2_problem.png"
    },
    {
        "name": "Guru Pintar Ai",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/6821op5e24kn",
        "caption": "GURU PINTAR AI - 50+ template, auto-grading!",
        "hashtags": "#guru #gurupintar #education #ai #edukasi",
        "file": "guru_pintar_ai_hook3_solution.png"
    },
    {
        "name": "Studio Marketplace Pro",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/emne05mm7v25",
        "caption": "BIKIN PRODUK AI SEHARI JADI! 🚀",
        "hashtags": "#marketplace #produkai #jualan #jualan #bisnisonline #affiliate #dropship",
        "file": "studio_marketplace_pro_hook1_shock.png"
    },
    {
        "name": "Studio Marketplace Pro",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/emne05mm7v25",
        "caption": "PENGEN JUAL PRODUK AI TAPI?",
        "hashtags": "#marketplace #jualan #bisnisonline",
        "file": "studio_marketplace_pro_hook2_problem.png"
    },
    {
        "name": "Studio Marketplace Pro",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/emne05mm7v25",
        "captiom": "STUDIO MARKETPLACE PRO - 100+ Template!",
        "hashtags": "#marketplace #jualan",
        "file": "studio_marketpro_hook3_solution.png"
    },
    {
        "name": "Mesin Cetak Bisnis Kulinermu",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/x8g6m3p9q1r2",
        "caption": "BISNIS KULINER TANPA MODAL BESAR! 🔥",
        "hashtags": "#kuliner #bisniskuliner #bisnis #jualan #makanan #kulinermu",
        "file": "mesin_cetak_kuliner_hook1_shock.png"
    },
    {
        "name": "Mesin Cetak Bisnis Kulinermu",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/x8g6m3p9q1r2",
        "caption": "MAU BISNIS KULINER TAPI?",
        "hashtags": "#kuliner #kuliner #bisnis #jualan #makanan",
        "file": "mesin_cetak_kuliner_hook2_problem.png"
    },
    {
        "name": "Mesin Cetak Bisnis Kulinermu",
        "price": "IDR 75K",
        "link": "https://ynk.id/jendralbot/x8g6m3p9q1r2",
        "caption": "MESIN CETAK BISNIS KULINER!",
        "hashtags": "#kuliner #bisniskuliner",
        "file": "mesin_cetak_kuliner_hook3_solution.png"
    },
    {
        "name": "AI Content Pro Seller 4K",
        "price": "IDR 89K",
        "link": "https://ynk.id/jendralbot/y5h7j8k9l0m1",
        "caption": "BLOK WRITING? 4000+ KONTEN SIAP PAKAI! 📱",
        "hashtags": "#contentcreator #viral #tiktok #instagram #youtube #ai #affiliatemarketing",
        "file": "ai_content_pro_seller_hook1_shock.png"
    },
    {
        "name": "AI Content Pro Seller 4K",
        "price": "IDR 89K",
        "link": "https://ynk.id/jendralbot/y5h7j8k9l0m1",
        "caption": "CONTENT CREATOR SUSAH BUAT KONTEN?",
        "hashtags": "#contentcreator #viral #tiktok #instagram",
        "file": "ai_content_pro_seller_hook2_problem.png"
    },
    {
        "name": "AI Content Pro Seller 4K",
        "price": "IDR 89K",
        "link": "https://ynk.id/jendralbot/y5h7j8k9l0m1",
        "caption": "AI CONTENT PRO SELLER 4K - 4000+ Template Viral!",
        "hashtags": "#contentcreator #viral #tiktok #instagram",
        "file": "ai_content_pro_seller_hook3_solution.png"
    },
    {
        "name": "Starter AI Content 4K",
        "price": "IDR 49K",
        "link": "https://ynk.id/jendralbot/n2o3p4q5r6s7",
        "caption": "MAU KONTEN TAI? MODAL 49K! 💰",
        "hashtags": "#contentcreator #pemula #viral #tiktok #affiliatemarketing #beginner",
        "file": "starter_content_4k_hook1_shock.png"
    },
    {
        "name": "Starter AI Content 4K",
        "price": "IDR 49K",
        "link": "https://ynk.id/jendralbot/n2o3p4q5r6s7",
        "caption": "PENGEN KONTEN TAPI BUDGET MEPEK?",
        "hashtags": "#contentcreator #pemula #viral #tiktok",
        "file": "starter_content_4k_hook2_problem.png"
    },
    {
        "name": "Starter AI Content 4K",
        "price": "IDR 49K",
        "link": "https://ynk.id/jendralbot/n2o3p4q5r6s7",
        "captiom": "STARTER AI CONTENT 4K - 4000+ Templates!",
        "hashtags": "#contentcreator #pemula #viral #tiktok",
        "file": "starter_content_4k_hook3_solution.png"
    }
]

print(f"📦 Found {len(PRODUCTS)} products dengan {sum(len(p['assets'])} assets total")