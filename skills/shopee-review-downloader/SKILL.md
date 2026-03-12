# Shopee Review Video Downloader

Download product review videos from Shopee pages with automated browser navigation and metadata extraction.

## Description

The Shopee Review Video Downloader skill automates the process of extracting review videos from Shopee product pages. It navigates to Shopee product URLs, scrapes user-generated review videos with their associated metadata, downloads them to organized directories, and generates comprehensive product information files.

**Key Features:**
- Automated browser navigation to Shopee product pages
- Extracts review video URLs from customer reviews
- Downloads videos to organized directory structure
- Captures product information (name, price, description, images)
- Generates JSON metadata files with product and review details
- Handles pagination to get all reviews
- Preserves review timestamps and star ratings

## Usage

### Prerequisites

1. **Browser Tool Access** - Ensure the browser tool is available and configured
2. **Python 3.8+** installed
3. **curl** or **wget** for downloading videos
4. **BeautifulSoup4** for HTML parsing

### Installation

```bash
# Install Python dependencies
pip3 install beautifulsoup4 requests lxml

# Verify browser tool access
browser status
```

### Basic Usage

Download all review videos from a Shopee product:

```bash
cd ~/.openclaw/workspace/skills/shopee-review-downloader
python3 scripts/download_reviews.py https://shopee.co.id/product-url
```

The script will:
1. Open the Shopee product page
2. Extract all review video URLs
3. Download videos to `./downloads/{product-id}/` directory
4. Save product info to `product_info.json`
5. Save review metadata to `reviews.json`

### Advanced Usage

#### Download with Maximum Reviews

```bash
python3 scripts/download_reviews.py https://shopee.co.id/product-url --max-reviews 50
```

#### Custom Output Directory

```bash
python3 scripts/download_reviews.py https://shopee.co.id/product-url --output /path/to/output
```

#### Only Extract URLs (No Download)

```bash
python3 scripts/download_reviews.py https://shopee.co.id/product-url --extract-only
```

#### Include Product Images

```bash
python3 scripts/download_reviews.py https://shopee.co.id/product-url --download-images
```

## Dependencies

### Required

- **Browser Tool** - For automated Shopee page navigation and interaction
- **Python 3.8+** - Script execution
- **curl/wget** - Video downloading

### Python Libraries

```bash
pip3 install beautifulsoup4 requests lxml
```

## Examples

### Example 1: Basic Download

```bash
# Download reviews from a Shopee product
python3 scripts/download_reviews.py \
  https://shopee.co.id/product-i123456789-s123456789

# Output:
# downloads/123456789/
#   ├── reviews/
#   │   ├── review_001.mp4
#   │   ├── review_002.mp4
#   │   └── review_003.mp4
#   ├── product_info.json
#   └── reviews.json
```

### Example 2: Download with Product Images

```bash
python3 scripts/download_reviews.py \
  https://shopee.co.id/product-i123456789-s123456789 \
  --download-images \
  --max-reviews 20

# Output:
# downloads/123456789/
#   ├── reviews/
#   │   ├── review_001.mp4
#   │   └── ...
#   ├── images/
#   │   ├── product_001.jpg
#   │   └── ...
#   ├── product_info.json
#   └── reviews.json
```

### Example 3: Extract URLs Only

```bash
# Extract video URLs without downloading
python3 scripts/download_reviews.py \
  https://shopee.co.id/product-i123456789-s123456789 \
  --extract-only

# Output:
# downloads/123456789/
#   ├── product_info.json
#   └── reviews.json (contains video URLs)
```

### Sample Product URLs

```
https://shopee.co.id/product-i123456789-s123456789
https://shopee.co.id/product-i987654321-s987654321
https://shopee.co.id/product-i192837465-s192837465
```

## Output Structure

```
downloads/
└── {product-id}/
    ├── reviews/
    │   ├── review_001.mp4
    │   ├── review_002.mp4
    │   └── review_003.mp4
    ├── images/ (if --download-images)
    │   ├── product_001.jpg
    │   ├── product_002.jpg
    │   └── product_003.jpg
    ├── product_info.json
    └── reviews.json
```

## Metadata Files

### product_info.json

```json
{
  "product_id": "123456789",
  "name": "Product Name",
  "price": "IDR 99.000",
  "currency": "IDR",
  "price_numeric": 99000,
  "description": "Product description text...",
  "shop_name": "Shop Name",
  "shop_id": "12345678",
  "total_reviews": 150,
  "rating": 4.8,
  "images": [
    "https://cf.shopee.co.id/file/image1.jpg",
    "https://cf.shopee.co.id/file/image2.jpg"
  ],
  "product_url": "https://shopee.co.id/product-i123456789-s123456789",
  "downloaded_at": "2026-03-11T16:53:00+07:00"
}
```

### reviews.json

```json
{
  "product_id": "123456789",
  "total_reviews": 150,
  "downloaded_reviews": 5,
  "reviews": [
    {
      "review_id": "001",
      "rating": 5,
      "comment": "Great product!",
      "video_url": "https://cf.shopee.co.id/file/review001.mp4",
      "video_path": "downloads/123456789/reviews/review_001.mp4",
      "author": "username",
      "review_date": "2026-03-10",
      "timestamp": "2026-03-10T14:30:00+07:00",
      "helpful_count": 10
    }
  ]
}
```

## Technical Details

### Browser Automation

The skill uses the browser tool to:
1. Navigate to Shopee product URLs
2. Parse page HTML to extract product information
3. Locate review video elements in the review section
4. Handle Shopee's dynamic content loading (if applicable)
5. Paginate through multiple review pages

### Video Extraction Logic

Review videos are extracted by:
1. Scanning the review section for video containers
2. Identifying video tags and their `src` attributes
3. Extracting video URLs from Shopee's CDN (cf.shopee.co.id)
4. Checking for video thumbnails and preview images
5. Validating video URLs before download

### Download Strategy

Videos are downloaded using:
- **curl** (primary) with resume support (`-C -`)
- **wget** as fallback if curl not available
- **Browser download** as last resort (using browser automation)

Each download includes:
- Retry logic (3 attempts)
- Progress display
- Timeout handling (30 seconds)
- File size validation

### Product Information Extraction

Extracted from product page:
- **Product ID**: From URL or page meta
- **Name**: Product title element
- **Price**: Current price with currency
- **Description**: Product description text
- **Shop Info**: Shop name and ID
- **Images**: All product image URLs
- **Rating**: Overall rating (numeric)
- **Total Reviews**: Review count

### Directory Organization

Files are organized by product ID for easy management:
```
downloads/{product-id}/
  ├── reviews/       # Video files
  ├── images/        # Product images (optional)
  ├── *.json         # Metadata files
  └── log.txt        # Download log
```

## Limitations

1. **Shopee Anti-Scraping**: May need delay between requests
2. **Login Required**: Some reviews may require account login
3. **Video Availability**: Not all reviews have videos
4. **Regional Restrictions**: Some content may be geo-blocked
5. **API Changes**: Shopee may update page structure without notice

## Troubleshooting

### Issue: No reviews found
- **Solution**: Check if product has reviews with videos. Some products only have text reviews.

### Issue: Videos don't download
- **Solution**: Verify curl/wget is installed. Check URL accessibility manually.

### Issue: Browser tool fails
- **Solution**: Check browser tool status with `browser status`. Ensure Vivaldi is running.

### Issue: Shopee blocks scraping
- **Solution**: Add longer delays between requests. Use `--delay` parameter.

## Security & Ethics

This skill is for **educational and research purposes only**. When using:
- Respect Shopee's Terms of Service
- Don't overwhelm servers with rapid requests
- Use downloaded content responsibly
- Obtain permission before republishing
- Respect user privacy and intellectual property

## Contributing

To extend this skill:
1. Add new features to `scripts/download_reviews.py`
2. Update documentation in SKILL.md
3. Test with various product types
4. Share improvements with the community

## License

MIT License - Use freely, modify as needed, provide attribution.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-11
**Skill Type:** Web Scraping / Automation
**Complexity:** Intermediate
**Estimated Time per Product:** 2-5 minutes (depends on review count)