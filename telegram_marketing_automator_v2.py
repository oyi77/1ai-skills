#!/usr/bin/env python3
"""
Telegram Marketing Automator V2 - Human-Like Bot
Features:
- Problem Solver Logic (auto-help for errors)
- Upsell Logic (product recommendations)
- Master Channel Consolidation
- Smart Keyword Detection
"""

import os
import json
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# Configuration
BOT_TOKEN = "8665546627:AAFp6SSBasBcpN3tGf1jNSpRPotMYwM8DEM"
MASTER_CHANNEL_ID = -100157228659  # Replace with actual master channel ID

# Keyword Database
PROBLEM_KEYWORDS = ["gagal", "error", "ga jalan", "fix bug", "tidak bekerja", "not working", "failed"]
UPSELL_KEYWORDS = ["agency os", "aura beauty", "guru pintar", "guru ai", "automation", "ads"]
HELLO_KEYWORDS = ["halo", "hai", "halo", "siang", "pagi", "malam", "hello", "hi", "salam"]

# Products Database - UPDATED WITH LYNK.ID/JENDRALBOT
PRODUCTS = {
    "agency_os": {
        "name": "Agency Performance Ad OS",
        "price": "Rp 750.000",
        "features": [
            "📊 Dashboard Ads Performance",
            "🎯 ROAS Tracker & Optimization",
            "📈 Campaign Scaling AI",
            "💰 Budget Allocation Automation",
            "🔔 Real-time Alerts"
        ],
        "cta": "Dapatkan sekarang: https://lynk.id/jendralbot"
    },
    "aura_beauty": {
        "name": "AURA Beauty Studio",
        "price": "Rp 499.000",
        "features": [
            "✨ AI Photo Enhancement",
            "🎨 Professional Color Grading",
            "👸 Virtual Try-On",
            "📱 Batch Processing",
            "🖼️ Background Removal"
        ],
        "cta": "Dapatkan sekarang: https://lynk.id/jendralbot"
    },
    "guru_pintar": {
        "name": "Guru Pintar AI",
        "price": "Rp 399.000",
        "features": [
            "📚 Auto Content Generator",
            "🎬 Video Script Writer",
            "📝 Blog Post Creator",
            "🎙️ Voice Over AI",
            "📱 Social Media Post Generator"
        ],
        "cta": "Dapatkan sekarang: https://lynk.id/jendralbot"
    },
    "all_access": {
        "name": "BerkahKarya All-Access Pass",
        "price": "Rp 499.000 (DARI Rp 2.499.000)",
        "features": [
            "🚀 Akses ke SEMUA produk (14+ tools)",
            "🎓 Blueprint Scaling Veris (Ads Mastery)",
            "💬 Weekly Live Support dari Veris",
            "📦 Free Updates Selamanya",
            "🏆 Private Community Access"
        ],
        "cta": "AMBATIL SEKARANG (LIMITED): https://lynk.id/jendralbot"
    }
}

# Problem Solver Templates
PROBLEM_SOLUTIONS = {
    "login": """
🔧 **Cara Mengatasi Masalah Login:**

1. ✅ Pastikan email & password benar
2. ✅ Cek koneksi internet
3. ✅ Clear cache browser
4. ✅ Coba browser lain
5. ✅ Reset password kalau lupa

Masih gagal? Hubungi support: @support_bot
""",
    "payment": """
💳 **Cara Mengatasi Masalah Pembayaran:**

1. ✅ Pastikan saldo kartu cukup
2. ✅ Cek expiry date kartu
3. ✅ Pastikan CVV benar
4. ✅ Coba metode pembayaran lain (OVO, Dana, BCA)
5. ✅ Cek halaman pembayaran manual

Butuh bantuan? Chat: @payment_support
""",
    "download": """
📥 **Cara Mengunduh File:**

1. ✅ Pastikan login sudah aktif
2. ✅ Klik tombol "Download"
3. ✅ Tunggu file selesai loading
4. ✅ Cek folder "Downloads"
5. ✅ Kalau error, coba restart browser

Masih tidak bisa? Hubungi: @tech_support
""",
    "general": """
🤔 **Bantuan Umum:**

Halo! Saya adalah asisten AI BerkahKarya. Saya bisa bantu:

📌 **Produk & Fitur**
- Info produk apa saja yang tersedia
- Cara pakai setiap tool
- Promo & diskon terbaru

📌 **Teknis**
- Masalah login
- Masalah pembayaran
- Masalah download

📌 **Konsultasi**
- Strategy ads
- Tips marketing
- Scaling campaign

Silakan jelaskan masalahmu, saya akan bantu! 🚀
"""
}

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBotV2:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all message handlers"""
        # Start command
        self.application.add_handler(CommandHandler("start", self.start_command))

        # Help command
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Products command
        self.application.add_handler(CommandHandler("produk", self.products_command))

        # Message handler for text
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user

        welcome_message = f"""
👋 *Selamat Datang, {user.first_name}*!

Saya adalah **Asisten AI BerkahKarya** 🤖

Saya bisa membantu:
📌 Info produk & fitur
📌 Solusi masalah teknis
📌 Rekomendasi produk
📌 Konsultasi marketing

Silakan ketik pertanyaanmu atau pilih menu di bawah:
"""

        keyboard = [
            [InlineKeyboardButton("📦 Lihat Semua Produk", callback_data="products")],
            [InlineKeyboardButton("🆘 Butuh Bantuan?", callback_data="help")],
            [InlineKeyboardButton("🎁 Promo Spesial", callback_data="promo")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

        logger.info(f"User {user.id} ({user.username}) started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📚 **Menu Bantuan**

🤖 **Perintah yang tersedia:**

/start - Mulai bot
/produk - Lihat semua produk
/help - Bantuan ini

💬 **Tanya apa saja tentang:**
- Info produk
- Solusi masalah (gagal, error, dll)
- Rekomendasi produk
- Tips marketing

👨‍💻 **Contoh pertanyaan:**
- "Gagal login gimana caranya?"
- "Ada produk untuk ads?"
- "Error waktu download"
- "Rekomendasi buat beginner"

Silakan ketik pertanyaanmu! 🚀
"""

        await update.message.reply_text(help_message, parse_mode="Markdown")

    async def products_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /produk command - Show all products"""
        products_message = "📦 **Semua Produk BerkahKarya:**\n\n"

        for key, product in PRODUCTS.items():
            products_message += f"🔹 *{product['name']}*\n"
            products_message += f"   💰 Harga: {product['price']}\n\n"

        products_message += """
Ketik nama produk untuk detail, atau pilih di bawah:
"""

        keyboard = [
            [InlineKeyboardButton("🚀 Agency Performance Ad OS", callback_data="product_agency_os")],
            [InlineKeyboardButton("✨ AURA Beauty Studio", callback_data="product_aura_beauty")],
            [InlineKeyboardButton("🧠 Guru Pintar AI", callback_data="product_guru_pintar")],
            [InlineKeyboardButton("👑 ALL-ACCESS PASS (BEST VALUE)", callback_data="product_all_access")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            products_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages with smart keyword detection"""
        user = update.effective_user
        text = update.message.text.lower()

        logger.info(f"Message from {user.id} ({user.username}): {update.message.text}")

        # Check for hello/hi
        if any(keyword in text for keyword in HELLO_KEYWORDS):
            await self.send_hello_response(update)
            return

        # Check for problem keywords
        if any(keyword in text for keyword in PROBLEM_KEYWORDS):
            await self.handle_problem(update, text)
            return

        # Check for upsell keywords
        if any(keyword in text for keyword in UPSELL_KEYWORDS):
            await self.handle_upsell(update, text)
            return

        # Default response - offer help
        await self.send_default_response(update)

    async def send_hello_response(self, update: Update):
        """Send response for hello/greeting messages"""
        greeting_message = """
👋 Hai! Senang bertemu denganmu!

Saya siap membantu. Mau info apa?

📦 Info produk
🆘 Solusi masalah
🎓 Konsultasi marketing
💡 Tips & trick

Silakan ketik atau pilih menu di bawah:
"""

        keyboard = [
            [InlineKeyboardButton("📦 Lihat Produk", callback_data="products")],
            [InlineKeyboardButton("🆘 Bantuan", callback_data="help")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            greeting_message,
            reply_markup=reply_markup
        )

    async def handle_problem(self, update: Update, text: str):
        """Handle problem keywords with auto-help"""
        # Try to detect specific problem type
        problem_type = None

        if "login" in text or "masuk" in text:
            problem_type = "login"
        elif "payment" in text or "bayar" in text or "transfer" in text:
            problem_type = "payment"
        elif "download" in text or "unduh" in text:
            problem_type = "download"
        else:
            problem_type = "general"

        # Get solution
        solution = PROBLEM_SOLUTIONS.get(problem_type, PROBLEM_SOLUTIONS["general"])

        # Send solution
        await update.message.reply_text(
            solution,
            parse_mode="Markdown"
        )

        # Offer human support
        keyboard = [[InlineKeyboardButton("💬 Hubungi Support", url="https://t.me/berkahkarya_support")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Masih tidak bisa diselesaikan? Hubungi support kami:",
            reply_markup=reply_markup
        )

    async def handle_upsell(self, update: Update, text: str):
        """Handle upsell keywords with product recommendations"""
        # Determine which product to recommend
        recommended_product = None

        if "agency" in text and "os" in text:
            recommended_product = PRODUCTS["agency_os"]
        elif "aura" in text and "beauty" in text:
            recommended_product = PRODUCTS["aura_beauty"]
        elif "guru" in text and ("pintar" in text or "ai" in text):
            recommended_product = PRODUCTS["guru_pintar"]
        else:
            # Recommend all-access bundle as default
            recommended_product = PRODUCTS["all_access"]

        # Send product recommendation
        message = f"""
🎯 *Rekomendasi Produk Buat Kamu:*

📦 **{recommended_product['name']}**
💰 Harga: {recommended_product['price']}

✨ Fitur Utama:
"""
        for feature in recommended_product['features']:
            message += f"   {feature}\n"

        message += f"\n🔗 {recommended_product['cta']}"

        keyboard = [
            [InlineKeyboardButton("🛒 Beli Sekarang", url=recommended_product['cta'].split(": ")[1])],
            [InlineKeyboardButton("📦 Lihat Semua Produk", callback_data="products")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

        # Suggest master channel
        await update.message.reply_text(
            "💡 *Tips:* Join master channel kami untuk update terbaru & tips gratis!",
            parse_mode="Markdown"
        )

    async def send_default_response(self, update: Update):
        """Send default response when no keywords match"""
        default_message = """
Hmm, saya belum paham maksudmu 😅

Coba tanya tentang:
- "Gagal login gimana?"
- "Ada produk buat ads?"
- "Error waktu download"
- "Rekomendasi buat beginner"

Atau pilih menu di bawah:
"""

        keyboard = [
            [InlineKeyboardButton("📦 Lihat Produk", callback_data="products")],
            [InlineKeyboardButton("🆘 Bantuan", callback_data="help")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            default_message,
            reply_markup=reply_markup
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "products":
            await self.products_command(update, context)
        elif data == "help":
            await self.help_command(update, context)
        elif data == "promo":
            await self.send_promo(update)
        elif data.startswith("product_"):
            product_key = data.replace("product_", "")
            await self.show_product_detail(update, product_key)

    async def send_promo(self, update: Update):
        """Send promo message"""
        promo_message = """
🎉 **PROMO SPESIAL TERBATAS!**

🔥 **BerkahKarya All-Access Pass**

💥 DARI Rp 2.499.000 → HANYA Rp 499.000!
💥 Akses SEUMUR HIDUP ke 14+ Tools AI
💥 Bonus Blueprint Scaling Veris
💥 Private Community Access

⏰ *SISA 7 SLOT LISENSI!*

Ambil sekarang sebelum harga naik:
"""

        keyboard = [[InlineKeyboardButton("👑 AMBIL SEKARANG", url="https://lynk.id/jendralbot")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(
            promo_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    async def show_product_detail(self, update: Update, product_key: str):
        """Show detailed product information"""
        product = PRODUCTS.get(product_key)

        if not product:
            await update.callback_query.message.reply_text("Produk tidak ditemukan")
            return

        detail_message = f"""
📦 **{product['name']}**
💰 Harga: {product['price']}

✨ **Fitur Lengkap:**
"""
        for feature in product['features']:
            detail_message += f"   {feature}\n"

        detail_message += f"\n🔗 {product['cta']}"

        keyboard = [
            [InlineKeyboardButton("🛒 Beli Sekarang", url=product['cta'].split(": ")[1])],
            [InlineKeyboardButton("📦 Lihat Semua Produk", callback_data="products")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(
            detail_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    def run(self):
        """Run the bot"""
        logger.info("Starting Telegram Bot V2...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramBotV2()
    bot.run()
