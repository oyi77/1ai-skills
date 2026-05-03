# POST AI Automation

**Author:** Veris (BerkahKarya Ads Master)
**Version:** 1.0.0
**License:** MIT

Automate TikTok/Instagram video generation and posting using POST AI platform.

## 🚀 Quick Start

### 1. Install Setup

```bash
cd ~/.openclaw/workspace/skills/postai-automation

# Create config
cp config.example.json config.json

# Edit config with your credentials
nano config.json
```

### 2. Get POST AI Access

1. Visit: https://postai.myscalev.com/
2. Purchase subscription (Rp 349,000 lifetime)
3. Wait for credentials via email
4. Fill in `postai` section in `config.json`

### 3. Generate Your First Video

```bash
python scripts/generate_videos.py \
  --image produk.jpg \
  --count 10 \
  --platform tiktok
```

### 4. Upload to TikTok

```bash
python scripts/auto_upload.py \
  --source outputs/20260304_162200/*.mp4 \
  --platform tiktok
```

## 📋 Features

- ✅ Generate 10+ videos from 1 image
- ✅ Auto-caption & voice-over
- ✅ Multi-platform support (TikTok, Instagram, Threads)
- ✅ Batch processing from CSV
- ✅ Scheduled posting
- ✅ A/B testing variants
- ✅ Performance tracking

## 🎯 Use Cases

**1. Affiliate Marketing**
```bash
# 1 product = 10 videos = 3 posting times/day = 30 posts/day
python scripts/batch_process.py \
  --input products.csv \
  --platforms tiktok,instagram \
  --videos-per-product 10 \
  --schedule "08:00,14:00,20:00"
```

**2. E-commerce Store**
```bash
# Launch 50 new products with 5 videos each
python scripts/batch_process.py \
  --input new_products.csv \
  --videos-per-product 5
```

**3. Content Agency**
```bash
# Process multiple clients in one go
for client in clients/*; do
  python scripts/batch_process.py \
    --input "$client/products.csv" \
    --schedule "08:00,12:00,16:00,20:00"
done
```

## 📁 CSV Format

Create `products.csv` with these columns:

```csv
product_name,image_url,image_path,price,affiliate_link,caption_template
T-Shirt Merah,https://example.com/shirt.jpg,/local/path/shirt.jpg,150000,https://shope.ee/shirt,Promo {price}!
Kemeja Hijau,https://example.com/kemeja.jpg,,200000,https://shope.ee/kemeja,Fashion terbaru!
```

**Columns:**
- `product_name` - Product name (required)
- `image_url` - Image URL for download (optional)
- `image_path` - Local image path (optional, overrides url)
- `price` - Price (formatted as number)
- `affiliate_link` - Affiliate link (required)
- `caption_template` - Custom caption template (optional)

**Caption Template Variables:**
- `{name}` - Product name
- `{price}` - Price formatted
- `{link}` - Affiliate link
- `{hashtags}` - Auto-generated hashtags

## 🔧 Configuration

Edit `config.json`:

```json
{
  "postai": {
    "api_key": "your_post_ai_api_key",
    "account_id": "your_account_id",
    "endpoint": "https://api.postai.com/v1"
  },
  "tiktok": {
    "account": "@your_tiktok_account",
    "cookie_file": "/path/to/tiktok_cookies.json",
    "session_id": "your_session_id",
    "enabled": true
  },
  "defaults": {
    "language": "id",
    "videos_per_product": 10,
    "posting_schedule": ["08:00", "14:00", "20:00"]
  }
}
```

## 📊 Integration with Other Skills

**Content Generator:**
```bash
# Generate script ideas first
content-generator --topic "fashion" --count 5 > scripts.txt

# Use scripts in POST AI videos
python scripts/generate_videos.py --image produk.jpg --script-file scripts.txt
```

**Analytics Dashboard:**
```bash
# Track performance
python scripts/track_performance.py --days 7 --export analytics/
```

**Social Media Upload:**
```bash
# Cross-platform posting
social-media-upload --source videos/*.mp4 --platforms tiktok,instagram,threads
```

## ⚡ Performance Tips

1. **Batch at night**: Generate all videos at night, upload during peak hours
2. **A/B test**: Generate multiple styles (hype, calm, professional)
3. **Track metrics**: Use `track_performance.py` to find winning patterns
4. **Rotate styles**: Don't use same style every day
5. **Schedule smart**: Post 8AM, 2PM, 8PM for maximum reach

## 🐛 Troubleshooting

**"Config file not found"**
```bash
cp config.example.json config.json
```

**"API key not configured"**
- Check POST AI email for credentials
- Verify `config.json` has correct `postai.api_key`

**"No videos found"**
- Check glob pattern uses correct path format
- Verify videos were generated successfully

**"TikTok upload failed"**
- Re-export cookies from browser
- Check account is not banned/limited
- Verify session_id is correct

## 📈 Scaling Up

**Manual (1 user):**
- Process 10 products/day
- ~100 videos/day
- Manage by yourself

**Team (3 people):**
- Process 50 products/day
- ~500 videos/day
- Split by platform

**Agency (10+ clients):**
- Process 200+ products/day
- ~2000+ videos/day
- Automate with cron jobs + monitoring

## 🆘 Support

- **POST AI Platform**: https://postai.myscalev.com/
- **BerkahKarya**: Open issue in workspace
- **Contact Veris**: Direct message for skill support

## 📝 Changelog

### v1.0.0 (2026-03-04)
- Initial release
- Video generation
- Auto upload to TikTok/Instagram
- Batch processing from CSV
- Scheduled posting
- Performance tracking

## 📄 License

MIT License - Use freely for commercial and personal projects.

---

**Made with ❤️ by Veris @ BerkahKarya**
*Automate your affiliate marketing empire*