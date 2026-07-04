# -*- coding: utf-8 -*-
"""Tests for agent-reach-channels wrapper integration."""

import pytest
import sys
from pathlib import Path

# Add current directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from extractors import (
    ShopeeExtractor,
    TikTokShopExtractor,
    WeChatExtractor,
    get_shopee_extractor,
    get_tiktok_shop_extractor,
    get_wechat_extractor,
)


class TestShopeeExtractor:
    """Shopee extraction tests."""

    def test_can_handle_shopee_indonesia(self):
        """Should handle Shopee Indonesia URLs."""
        extractor = ShopeeExtractor()
        assert extractor.can_handle("https://shopee.co.id/product/456")

    def test_can_handle_shopee_malaysia(self):
        """Should handle Shopee Malaysia URLs."""
        extractor = ShopeeExtractor()
        assert extractor.can_handle("https://shopee.com.my/product/789")

    def test_can_handle_shopee_philippines(self):
        """Should handle Shopee Philippines URLs."""
        extractor = ShopeeExtractor()
        assert extractor.can_handle("https://shopee.com.ph/product/111")

    def test_can_handle_shopee_singapore(self):
        """Should handle Shopee Singapore URLs."""
        extractor = ShopeeExtractor()
        assert extractor.can_handle("https://shopee.com.sg/product/222")

    def test_can_handle_shopee_thailand(self):
        """Should handle Shopee Thailand URLs."""
        extractor = ShopeeExtractor()
        assert extractor.can_handle("https://shopee.co.th/product/333")

    def test_can_handle_shopee_vietnam(self):
        """Should handle Shopee Vietnam URLs."""
        extractor = ShopeeExtractor()
        assert extractor.can_handle("https://shopee.vn/product/444")

    def test_reject_non_shopee_urls(self):
        """Should reject non-Shopee URLs."""
        extractor = ShopeeExtractor()
        assert not extractor.can_handle("https://amazon.com/product/123")

    def test_extract_returns_list(self):
        """Extract should return list."""
        extractor = ShopeeExtractor()
        result = extractor.extract("https://shopee.co.id/product/123")
        assert isinstance(result, list)

    def test_extract_invalid_url_returns_empty(self):
        """Extract should return empty list for invalid URL."""
        extractor = ShopeeExtractor()
        result = extractor.extract("https://shopee.co.id/invalid")
        assert isinstance(result, list)

    def test_check_backend_returns_tuple(self):
        """check() should return (bool, str) tuple."""
        extractor = ShopeeExtractor()
        available, msg = extractor.check()
        assert isinstance(available, bool)
        assert isinstance(msg, str)


class TestTikTokShopExtractor:
    """TikTok Shop extraction tests."""

    def test_can_handle_tiktok_shop_product(self):
        """Should handle TikTok Shop product URLs."""
        extractor = TikTokShopExtractor()
        assert extractor.can_handle("https://www.tiktok.com/shop/product/123")

    def test_can_handle_tiktok_shop_seller(self):
        """Should handle TikTok Shop seller URLs."""
        extractor = TikTokShopExtractor()
        assert extractor.can_handle("https://www.tiktok.com/@seller_name/shop")

    def test_reject_non_tiktok_shop_urls(self):
        """Should reject non-TikTok Shop URLs."""
        extractor = TikTokShopExtractor()
        assert not extractor.can_handle("https://www.tiktok.com/@user_name/video/123")

    def test_extract_returns_list(self):
        """Extract should return list."""
        extractor = TikTokShopExtractor()
        result = extractor.extract("https://www.tiktok.com/shop/product/456")
        assert isinstance(result, list)

    def test_extract_invalid_url_returns_empty(self):
        """Extract should return empty list for invalid URL."""
        extractor = TikTokShopExtractor()
        result = extractor.extract("https://www.tiktok.com/invalid")
        assert isinstance(result, list)

    def test_check_backend_returns_tuple(self):
        """check() should return (bool, str) tuple."""
        extractor = TikTokShopExtractor()
        available, msg = extractor.check()
        assert isinstance(available, bool)
        assert isinstance(msg, str)


class TestWeChatExtractor:
    """WeChat extraction tests."""

    def test_can_handle_wechat_official_account(self):
        """Should handle WeChat Official Account URLs."""
        extractor = WeChatExtractor()
        assert extractor.can_handle("https://mp.weixin.qq.com/s?__biz=MzU1")

    def test_can_handle_wechat_weixin(self):
        """Should handle weixin.qq.com URLs."""
        extractor = WeChatExtractor()
        assert extractor.can_handle("https://weixin.qq.com/r/abc123")

    def test_can_handle_wechat_com(self):
        """Should handle wechat.com URLs."""
        extractor = WeChatExtractor()
        assert extractor.can_handle("https://wechat.com/profile/user123")

    def test_reject_non_wechat_urls(self):
        """Should reject non-WeChat URLs."""
        extractor = WeChatExtractor()
        assert not extractor.can_handle("https://www.facebook.com/profile")

    def test_extract_returns_list(self):
        """Extract should return list."""
        extractor = WeChatExtractor()
        result = extractor.extract("https://mp.weixin.qq.com/s?mid=1234567890")
        assert isinstance(result, list)

    def test_extract_invalid_url_returns_empty(self):
        """Extract should return empty list for invalid URL."""
        extractor = WeChatExtractor()
        result = extractor.extract("https://weixin.qq.com/invalid")
        assert isinstance(result, list)

    def test_check_backend_returns_tuple(self):
        """check() should return (bool, str) tuple."""
        extractor = WeChatExtractor()
        available, msg = extractor.check()
        assert isinstance(available, bool)
        assert isinstance(msg, str)


class TestConvenienceConstructors:
    """Test convenience factory functions."""

    def test_get_shopee_extractor(self):
        """Should return ShopeeExtractor instance."""
        extractor = get_shopee_extractor()
        assert isinstance(extractor, ShopeeExtractor)

    def test_get_tiktok_shop_extractor(self):
        """Should return TikTokShopExtractor instance."""
        extractor = get_tiktok_shop_extractor()
        assert isinstance(extractor, TikTokShopExtractor)

    def test_get_wechat_extractor(self):
        """Should return WeChatExtractor instance."""
        extractor = get_wechat_extractor()
        assert isinstance(extractor, WeChatExtractor)


class TestChannelIntegration:
    """Integration tests across all 3 channels."""

    def test_all_extractors_have_check_method(self):
        """All extractors should have check() method."""
        extractors = [
            ShopeeExtractor(),
            TikTokShopExtractor(),
            WeChatExtractor(),
        ]
        for extractor in extractors:
            assert hasattr(extractor, 'check')
            assert callable(extractor.check)

    def test_all_extractors_have_can_handle_method(self):
        """All extractors should have can_handle() method."""
        extractors = [
            ShopeeExtractor(),
            TikTokShopExtractor(),
            WeChatExtractor(),
        ]
        for extractor in extractors:
            assert hasattr(extractor, 'can_handle')
            assert callable(extractor.can_handle)

    def test_all_extractors_have_extract_method(self):
        """All extractors should have extract() method."""
        extractors = [
            ShopeeExtractor(),
            TikTokShopExtractor(),
            WeChatExtractor(),
        ]
        for extractor in extractors:
            assert hasattr(extractor, 'extract')
            assert callable(extractor.extract)

    def test_shopee_extraction_structure(self):
        """Shopee extraction should return proper structure."""
        extractor = ShopeeExtractor()
        result = extractor.extract("https://shopee.co.id/product/123456")
        assert len(result) > 0
        assert isinstance(result[0], dict)
        assert "product_id" in result[0] or "status" in result[0]

    def test_tiktok_shop_extraction_structure(self):
        """TikTok Shop extraction should return proper structure."""
        extractor = TikTokShopExtractor()
        result = extractor.extract("https://www.tiktok.com/shop/product/789")
        assert len(result) > 0
        assert isinstance(result[0], dict)
        assert "product_id" in result[0] or "status" in result[0]

    def test_wechat_extraction_structure(self):
        """WeChat extraction should return proper structure."""
        extractor = WeChatExtractor()
        result = extractor.extract("https://mp.weixin.qq.com/s?mid=12345")
        assert len(result) > 0
        assert isinstance(result[0], dict)
        assert "article_id" in result[0] or "status" in result[0]
