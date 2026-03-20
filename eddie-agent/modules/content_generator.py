"""
Content Generator
Generates product-specific captions using hook formulas.
Handles media selection and platform-specific formatting.
Uploads media via PostBridge for TikTok/Instagram.
"""

import os
import json
import random
import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger("eddie.content")

HOOK_FORMULAS = ["curiosity_gap", "contrarian", "number_based", "social_proof"]

HASHTAG_MAP = {
    "career":       ["#CareerTips", "#CVOptimasi", "#JobHunting", "#KarirImpian", "#JendralBot"],
    "marketing":    ["#IklanOnline", "#MarketingDigital", "#AdsStrategy", "#UMKM", "#JendralBot"],
    "food_business":["#BisnisKuliner", "#FoodBusiness", "#UMKM", "#UsahaKuliner", "#JendralBot"],
    "ecommerce":    ["#JualOnline", "#MarketplaceTips", "#TokopediaTips", "#ShopeeTips", "#JendralBot"],
    "creative":     ["#ContentCreator", "#AITools", "#DesainGratis", "#FreelancerIndonesia", "#JendralBot"],
    "education":    ["#GuruPintar", "#PendidikanAI", "#LesPribadi", "#BimbelOnline", "#JendralBot"],
    "affiliate":    ["#TikTokAffiliate", "#IncomePasif", "#AffiliateMarketing", "#TikTokShop", "#JendralBot"],
    "starter":      ["#BelanjaCerdas", "#CashbackKeren", "#HematBelanja", "#ShoppingHacks", "#JendralBot"]
}

PLATFORMS_NEEDING_MEDIA = {"tiktok", "instagram"}


class ContentGenerator:
    """
    Generates platform-specific captions from product data.
    Selects matching media assets and uploads via PostBridge when needed.
    """

    def __init__(self, config: dict, postbridge_client=None):
        self.config = config
        self.pb = postbridge_client
        self.assets_dir = Path(config["media"]["assets_dir"])
        self.products = self._load_products()
        self.templates = self._load_templates()

    def _load_products(self) -> list:
        skill_dir = Path(__file__).parent.parent
        products_path = skill_dir / "data" / "products.json"
        with open(products_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_templates(self) -> dict:
        skill_dir = Path(__file__).parent.parent
        templates_path = skill_dir / "data" / "caption_templates.json"
        with open(templates_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_product(self, product_id: str) -> Optional[dict]:
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None

    def get_random_product(self) -> dict:
        return random.choice(self.products)

    def find_media_for_product(self, product: dict, platform: str) -> Optional[Path]:
        """
        Find the best matching image from assets_dir for this product.
        Tries hook_frames_prefix match first, then category, then any available.
        """
        if not self.assets_dir.exists():
            logger.warning(f"Assets dir not found: {self.assets_dir}")
            return None

        prefix = product.get("hook_frames_prefix", "")
        all_images = list(self.assets_dir.glob("*.png")) + \
                     list(self.assets_dir.glob("*.jpg")) + \
                     list(self.assets_dir.glob("*.jpeg"))

        if not all_images:
            logger.warning("No images found in assets directory")
            return None

        # Try prefix match first
        if prefix:
            matched = [f for f in all_images if f.name.startswith(prefix)]
            if matched:
                chosen = random.choice(matched)
                logger.info(f"Found media by prefix '{prefix}': {chosen.name}")
                return chosen

        # Fallback: random from any available
        chosen = random.choice(all_images)
        logger.info(f"Fallback media selection: {chosen.name}")
        return chosen

    def build_caption(self, product: dict, platform: str,
                      hook_formula: Optional[str] = None) -> str:
        """
        Build a platform-optimized caption using product-specific hooks.
        """
        if not hook_formula or hook_formula not in HOOK_FORMULAS:
            hook_formula = random.choice(HOOK_FORMULAS)

        hooks = product.get("hooks", {})
        captions = product.get("captions", {})
        category = product.get("category", "starter")
        hashtags = HASHTAG_MAP.get(category, ["#JendralBot"])

        hook_text = hooks.get(hook_formula, "")
        platform_caption = captions.get(platform, "")

        if platform == "tiktok":
            tags = " ".join(hashtags[:5])
            # Use product-specific TikTok caption if available, else build from hook
            if platform_caption:
                return platform_caption
            return f"{hook_text}\n\n👇 Link di bio! {tags}"

        elif platform == "instagram":
            tags = " ".join(hashtags)
            if platform_caption:
                return platform_caption
            engagement = random.choice([
                "Save post ini biar nggak lupa!",
                "Tag teman yang butuh ini!",
                "Setuju? Drop ✅ di komentar!"
            ])
            return f"{hook_text}\n\n{engagement}\n\n➡️ Link di bio untuk akses sekarang!\n\n{tags}"

        elif platform == "facebook":
            if platform_caption:
                return platform_caption
            return (
                f"{hook_text}\n\n"
                f"Produk: {product['name']}\n"
                f"Harga: {product['price_label']}\n\n"
                f"Ambil sekarang → {product['lynk_url']}"
            )

        else:
            return f"{hook_text}\n\n{product['lynk_url']}"

    def upload_media_for_post(self, product: dict, platform: str) -> Optional[str]:
        """
        Find and upload media for TikTok/Instagram post.
        Returns media_id or None if upload fails / not needed.
        """
        if platform not in PLATFORMS_NEEDING_MEDIA:
            return None

        if not self.pb:
            logger.error("PostBridge client not configured — cannot upload media")
            return None

        media_path = self.find_media_for_product(product, platform)
        if not media_path:
            logger.error(f"No media found for product '{product['id']}' on {platform}")
            return None

        try:
            media_id = self.pb.upload_media(str(media_path))
            logger.info(f"Uploaded media for {product['id']} on {platform}: media_id={media_id}")
            return media_id
        except Exception as e:
            logger.error(f"Media upload failed for {product['id']} on {platform}: {e}")
            return None

    def generate_post(
        self,
        product_id: Optional[str] = None,
        platform: str = "tiktok",
        hook_formula: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict:
        """
        Generate a complete post dict ready for PostBridge.
        Includes media upload if required.

        Returns:
            {
                product: dict,
                platform: str,
                caption: str,
                media_id: str|None,
                media_path: str|None,
                hook_formula: str,
                ready: bool  (False if media required but upload failed)
            }
        """
        product = self.get_product(product_id) if product_id else self.get_random_product()
        if not product:
            raise ValueError(f"Product not found: {product_id}")

        if not hook_formula:
            hook_formula = random.choice(HOOK_FORMULAS)

        caption = self.build_caption(product, platform, hook_formula)
        media_id = None
        media_path = None
        ready = True

        if platform in PLATFORMS_NEEDING_MEDIA:
            media_file = self.find_media_for_product(product, platform)
            if media_file:
                media_path = str(media_file)
                if not dry_run:
                    media_id = self.upload_media_for_post(product, platform)
                    if not media_id:
                        logger.warning(f"Media upload failed — post for {platform} not ready")
                        ready = False
                else:
                    logger.info(f"[DRY RUN] Would upload: {media_file.name}")
            else:
                logger.error(f"No media found for {platform} post — REQUIRED!")
                ready = False

        return {
            "product": product,
            "platform": platform,
            "caption": caption,
            "media_id": media_id,
            "media_path": media_path,
            "hook_formula": hook_formula,
            "ready": ready,
            "dry_run": dry_run
        }

    def generate_batch(
        self,
        platforms: List[str],
        product_id: Optional[str] = None,
        hook_formula: Optional[str] = None,
        dry_run: bool = False
    ) -> List[Dict]:
        """Generate posts for multiple platforms. Uses same product across platforms."""
        product = self.get_product(product_id) if product_id else self.get_random_product()
        results = []
        for platform in platforms:
            try:
                post = self.generate_post(
                    product_id=product["id"],
                    platform=platform,
                    hook_formula=hook_formula,
                    dry_run=dry_run
                )
                results.append(post)
            except Exception as e:
                logger.error(f"Failed to generate post for {platform}: {e}")
                results.append({
                    "product": product,
                    "platform": platform,
                    "error": str(e),
                    "ready": False
                })
        return results
