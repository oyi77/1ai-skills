# -*- coding: utf-8 -*-
"""Tests for new channels: Shopee, TikTok Shop, WeChat."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agent_reach.channels.shopee import ShopeeChannel
from agent_reach.channels.tiktok_shop import TikTokShopChannel
from agent_reach.channels.wechat import WeChatChannel


class TestShopeeChannel:
    """Shopee e-commerce channel tests."""

    def test_can_handle_shopee_indonesia(self):
        """Should handle Shopee Indonesia URLs."""
        channel = ShopeeChannel()
        assert channel.can_handle("https://shopee.co.id/product/123")
        assert channel.can_handle("https://shopee.co.id/p/456")

    def test_can_handle_shopee_malaysia(self):
        """Should handle Shopee Malaysia URLs."""
        channel = ShopeeChannel()
        assert channel.can_handle("https://shopee.com.my/product/789")

    def test_can_handle_shopee_philippines(self):
        """Should handle Shopee Philippines URLs."""
        channel = ShopeeChannel()
        assert channel.can_handle("https://shopee.com.ph/product/111")

    def test_reject_non_shopee_urls(self):
        """Should reject non-Shopee URLs."""
        channel = ShopeeChannel()
        assert not channel.can_handle("https://amazon.com/product/123")
        assert not channel.can_handle("https://lazada.co.id/product/456")

    def test_check_backend_available(self):
        """Check method returns status tuple."""
        channel = ShopeeChannel()
        status, msg = channel.check()
        assert status in ("ok", "warn", "fail")
        assert isinstance(msg, str)

    @patch("subprocess.run")
    def test_extract_product_id(self, mock_run):
        """Should extract product ID from Shopee URL."""
        channel = ShopeeChannel()
        product_id = channel._extract_product_id("https://shopee.co.id/p/123456789")
        assert product_id == "123456789"

    @patch("subprocess.run")
    def test_extract_with_cli_success(self, mock_run):
        """Should extract data using shopee-cli."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='[{"id": "123", "name": "Product", "price": 100000}]'
        )
        channel = ShopeeChannel()
        channel.active_backend = "shopee-cli"
        result = channel._extract_with_cli("https://shopee.co.id/p/123")
        assert isinstance(result, list)

    def test_extract_invalid_url(self):
        """Should handle invalid URLs gracefully."""
        channel = ShopeeChannel()
        result = channel.extract("not-a-url")
        assert isinstance(result, list)


class TestTikTokShopChannel:
    """TikTok Shop e-commerce channel tests."""

    def test_can_handle_tiktok_shop_urls(self):
        """Should handle TikTok Shop URLs."""
        channel = TikTokShopChannel()
        assert channel.can_handle("https://www.tiktok.com/@seller/shop/product/123")
        assert channel.can_handle("https://www.tiktok.com/live/456")

    def test_can_handle_regional_tiktok_shop(self):
        """Should handle regional TikTok Shop URLs."""
        channel = TikTokShopChannel()
        assert channel.can_handle("https://www.tiktok.com/shop/product/789")
        assert channel.can_handle("https://www.tiktok.com/@seller/profile")

    def test_reject_non_tiktok_shop_urls(self):
        """Should reject non-TikTok Shop URLs."""
        channel = TikTokShopChannel()
        assert not channel.can_handle("https://tiktok.com/product/123")
        assert not channel.can_handle("https://amazon.com/product/456")

    def test_check_backend_available(self):
        """Check method returns status tuple."""
        channel = TikTokShopChannel()
        status, msg = channel.check()
        assert status in ("ok", "warn", "fail")
        assert isinstance(msg, str)

    @patch("selenium.webdriver.Chrome")
    def test_extract_with_selenium(self, mock_chrome):
        """Should extract data using Selenium."""
        channel = TikTokShopChannel()
        channel.active_backend = "selenium"
        # Mock Selenium driver
        result = channel.extract("https://tiktokshop.com/product/123")
        assert isinstance(result, list)

    def test_extract_invalid_url(self):
        """Should handle invalid URLs gracefully."""
        channel = TikTokShopChannel()
        result = channel.extract("not-a-url")
        assert isinstance(result, list)


class TestWeChatChannel:
    """WeChat messaging channel tests."""

    def test_can_handle_wechat_urls(self):
        """Should handle WeChat URLs and links."""
        channel = WeChatChannel()
        assert channel.can_handle("https://mp.weixin.qq.com/s/article123")
        assert channel.can_handle("https://weixin.qq.com/profile")
        assert channel.can_handle("myweichatlid")  # WeChat ID pattern

    def test_reject_non_wechat_urls(self):
        """Should reject non-WeChat URLs."""
        channel = WeChatChannel()
        assert not channel.can_handle("https://twitter.com/status/123")
        assert not channel.can_handle("https://facebook.com/post/456")

    def test_check_backend_available(self):
        """Check method returns status tuple."""
        channel = WeChatChannel()
        status, msg = channel.check()
        assert status in ("ok", "warn", "fail")
        assert isinstance(msg, str)

    @patch("requests.get")
    def test_extract_official_account_article(self, mock_get):
        """Should extract WeChat Official Account article."""
        mock_get.return_value = MagicMock(
            status_code=200,
            text="<title>Article Title</title><div>Article content</div>"
        )
        channel = WeChatChannel()
        channel.active_backend = "web_scraping"
        result = channel.extract("https://mp.weixin.qq.com/s/article123")
        assert isinstance(result, list)

    def test_extract_group_message_link(self):
        """Should handle WeChat group message links."""
        channel = WeChatChannel()
        result = channel.extract("https://mp.weixin.qq.com/s?__biz=MzI0")
        assert isinstance(result, list)

    def test_extract_invalid_url(self):
        """Should handle invalid URLs gracefully."""
        channel = WeChatChannel()
        result = channel.extract("not-a-url")
        assert isinstance(result, list)


class TestChannelIntegration:
    """Integration tests across all 3 new channels."""

    def test_all_channels_have_name(self):
        """All channels should have name attribute."""
        channels = [ShopeeChannel(), TikTokShopChannel(), WeChatChannel()]
        for ch in channels:
            assert hasattr(ch, "name")
            assert isinstance(ch.name, str)
            assert len(ch.name) > 0

    def test_all_channels_have_description(self):
        """All channels should have description."""
        channels = [ShopeeChannel(), TikTokShopChannel(), WeChatChannel()]
        for ch in channels:
            assert hasattr(ch, "description")
            assert isinstance(ch.description, str)

    def test_all_channels_have_backends(self):
        """All channels should list available backends."""
        channels = [ShopeeChannel(), TikTokShopChannel(), WeChatChannel()]
        for ch in channels:
            assert hasattr(ch, "backends")
            assert isinstance(ch.backends, list)
            assert len(ch.backends) > 0

    def test_all_channels_implement_can_handle(self):
        """All channels should implement can_handle method."""
        channels = [ShopeeChannel(), TikTokShopChannel(), WeChatChannel()]
        for ch in channels:
            assert hasattr(ch, "can_handle")
            assert callable(ch.can_handle)

    def test_all_channels_implement_extract(self):
        """All channels should implement extract method."""
        channels = [ShopeeChannel(), TikTokShopChannel(), WeChatChannel()]
        for ch in channels:
            assert hasattr(ch, "extract")
            assert callable(ch.extract)

    def test_all_channels_implement_check(self):
        """All channels should implement check method."""
        channels = [ShopeeChannel(), TikTokShopChannel(), WeChatChannel()]
        for ch in channels:
            assert hasattr(ch, "check")
            assert callable(ch.check)
