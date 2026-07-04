# -*- coding: utf-8 -*-
"""
Comprehensive test suite for multi-platform channel extraction.

Tests cover:
- Shopee (e-commerce, SEA)
- TikTok Shop (social commerce, global)
- WeChat (messaging, China/APAC)

All channels follow unified interface contract.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import channels
from shopee import ShopeeChannel, ExtractionResult as ShopeeResult
from tiktok_shop import TikTokShopChannel, ExtractionResult as TikTokResult
from wechat import WeChatChannel, ExtractionResult as WeChatResult


class TestShopeeChannel:
    """Test Shopee e-commerce channel."""
    
    def setup_method(self):
        self.channel = ShopeeChannel()
        self.sample_urls = [
            "https://shopee.co.id/product/123456",
            "https://shopee.com.my/p/456789",
            "https://shopee.ph/product/789012",
            "https://shopee.sg/item/234567",
        ]
    
    def test_can_handle_shopee_urls(self):
        """Test URL detection for Shopee."""
        for url in self.sample_urls:
            assert self.channel.can_handle(url), f"Should handle {url}"
    
    def test_cannot_handle_non_shopee_urls(self):
        """Test rejection of non-Shopee URLs."""
        non_shopee = [
            "https://amazon.com/dp/123456",
            "https://tiktok.com/@user",
            "https://google.com",
            "",
            None,
        ]
        for url in non_shopee:
            assert not self.channel.can_handle(url), f"Should reject {url}"
    
    def test_check_returns_status_tuple(self):
        """Test that check() returns (status, message) tuple."""
        status, msg = self.channel.check()
        assert status in ["ok", "fail"], f"Invalid status: {status}"
        assert isinstance(msg, str), "Message must be string"
        assert len(msg) > 0, "Message cannot be empty"
    
    @patch("subprocess.run")
    def test_extract_with_cli_success(self, mock_run):
        """Test successful extraction with CLI backend."""
        # Mock CLI response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([
            {"id": "123", "title": "Product 1", "price": "99.99"},
            {"id": "124", "title": "Product 2", "price": "149.99"}
        ])
        mock_run.return_value = mock_result
        
        self.channel.active_backend = "shopee-cli"
        result = self.channel.extract(self.sample_urls[0])
        
        assert result.success is True
        assert result.backend_used == "shopee-cli"
        assert result.item_count == 2
        assert len(result.data) == 2
    
    @patch("subprocess.run")
    def test_extract_with_cli_failure(self, mock_run):
        """Test extraction failure with CLI backend."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Connection failed"
        mock_run.return_value = mock_result
        
        self.channel.active_backend = "shopee-cli"
        result = self.channel.extract(self.sample_urls[0])
        
        assert result.success is False
        assert result.error is not None
        assert "Connection failed" in result.error
    
    def test_extract_invalid_url(self):
        """Test extraction with invalid URL."""
        result = self.channel.extract("https://invalid.com/page")
        
        assert result.success is False
        assert "Not a Shopee URL" in result.error
    
    def test_extract_returns_extraction_result(self):
        """Test that extract() always returns ExtractionResult."""
        result = self.channel.extract("https://invalid.com")
        
        assert isinstance(result, ShopeeResult)
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert hasattr(result, "error")
        assert hasattr(result, "backend_used")
        assert hasattr(result, "item_count")
    
    def test_product_id_extraction(self):
        """Test product ID parsing from Shopee URLs."""
        test_cases = [
            ("https://shopee.co.id/product/123456", "123456"),
            ("https://shopee.com.my/p/789012", "789012"),
            ("https://shopee.sg/item/555555", "555555"),
        ]
        
        for url, expected_id in test_cases:
            extracted = self.channel._extract_product_id(url)
            assert extracted == expected_id, f"Failed for {url}"


class TestTikTokShopChannel:
    """Test TikTok Shop channel."""
    
    def setup_method(self):
        self.channel = TikTokShopChannel()
        self.sample_urls = [
            "https://tiktok.com/shop/product/123456",
            "https://www.tiktok.com/shop/seller/user123",
            "https://tiktok.com/@seller/shop",
        ]
    
    def test_can_handle_tiktok_shop_urls(self):
        """Test URL detection for TikTok Shop."""
        for url in self.sample_urls:
            assert self.channel.can_handle(url), f"Should handle {url}"
    
    def test_cannot_handle_regular_tiktok_urls(self):
        """Test rejection of non-shop TikTok URLs."""
        non_shop = [
            "https://tiktok.com/@user/video/123",
            "https://tiktok.com/discover/trending",
            "https://tiktok.com",
        ]
        for url in non_shop:
            assert not self.channel.can_handle(url), f"Should reject {url}"
    
    def test_check_returns_status_tuple(self):
        """Test that check() returns (status, message) tuple."""
        status, msg = self.channel.check()
        assert status in ["ok", "fail"]
        assert isinstance(msg, str)
    
    @patch("subprocess.run")
    def test_extract_with_cli_success(self, mock_run):
        """Test successful extraction with CLI backend."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([
            {"id": "t1", "name": "Item 1", "price": "29.99"},
        ])
        mock_run.return_value = mock_result
        
        self.channel.active_backend = "tiktok-shop-cli"
        result = self.channel.extract(self.sample_urls[0])
        
        assert result.success is True
        assert result.item_count == 1
    
    def test_extract_returns_extraction_result(self):
        """Test return type contract."""
        result = self.channel.extract("https://invalid.com")
        
        assert isinstance(result, TikTokResult)
        assert hasattr(result, "success")


class TestWeChatChannel:
    """Test WeChat channel."""
    
    def setup_method(self):
        self.channel = WeChatChannel()
        self.sample_urls = [
            "https://mp.weixin.qq.com/profile_ext?action=home&__biz=MzA123",
            "https://wx.qq.com/mini?appid=wx123",
            "weixin://dl/chat/group123",
        ]
    
    def test_can_handle_wechat_urls(self):
        """Test URL detection for WeChat."""
        for url in self.sample_urls:
            assert self.channel.can_handle(url), f"Should handle {url}"
    
    def test_cannot_handle_non_wechat_urls(self):
        """Test rejection of non-WeChat URLs."""
        non_wechat = [
            "https://qq.com",
            "https://tencent.com",
            "https://facebook.com",
        ]
        for url in non_wechat:
            assert not self.channel.can_handle(url), f"Should reject {url}"
    
    def test_check_returns_status_tuple(self):
        """Test that check() returns (status, message) tuple."""
        status, msg = self.channel.check()
        assert status in ["ok", "fail"]
        assert isinstance(msg, str)
    
    @patch("subprocess.run")
    def test_extract_with_cli_success(self, mock_run):
        """Test successful extraction with CLI backend."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([
            {"id": "m1", "content": "Post 1", "timestamp": 1234567890},
        ])
        mock_run.return_value = mock_result
        
        self.channel.active_backend = "wechat-cli"
        result = self.channel.extract(self.sample_urls[0])
        
        assert result.success is True
        assert result.item_count == 1
    
    def test_parse_wechat_target_official_account(self):
        """Test parsing Official Account ID from URL."""
        url = "https://mp.weixin.qq.com/profile_ext?action=home&__biz=MzA5NzAwODg4Mg=="
        target = self.channel._parse_wechat_target(url)
        assert target == "MzA5NzAwODg4Mg=="
    
    def test_parse_wechat_target_mini_program(self):
        """Test parsing Mini Program ID from URL."""
        url = "https://wx.qq.com/mini?appid=wx1234567890abcdef"
        target = self.channel._parse_wechat_target(url)
        assert target == "wx1234567890abcdef"
    
    def test_extract_returns_extraction_result(self):
        """Test return type contract."""
        result = self.channel.extract("https://invalid.com")
        
        assert isinstance(result, WeChatResult)
        assert hasattr(result, "success")


class TestChannelContract:
    """Test unified channel interface contract."""
    
    @pytest.mark.parametrize("channel_class", [
        ShopeeChannel,
        TikTokShopChannel,
        WeChatChannel,
    ])
    def test_channel_has_required_attributes(self, channel_class):
        """Test that all channels have required class attributes."""
        channel = channel_class()
        assert hasattr(channel, "name")
        assert hasattr(channel, "description")
        assert hasattr(channel, "backends")
        assert hasattr(channel, "tier")
        assert isinstance(channel.name, str)
        assert isinstance(channel.backends, list)
        assert isinstance(channel.tier, int)
    
    @pytest.mark.parametrize("channel_class", [
        ShopeeChannel,
        TikTokShopChannel,
        WeChatChannel,
    ])
    def test_channel_has_required_methods(self, channel_class):
        """Test that all channels implement required methods."""
        channel = channel_class()
        assert callable(getattr(channel, "can_handle", None))
        assert callable(getattr(channel, "check", None))
        assert callable(getattr(channel, "extract", None))
    
    @pytest.mark.parametrize("channel_class", [
        ShopeeChannel,
        TikTokShopChannel,
        WeChatChannel,
    ])
    def test_check_returns_status_message_tuple(self, channel_class):
        """Test that check() always returns (str, str) tuple."""
        channel = channel_class()
        status, msg = channel.check()
        assert isinstance(status, str)
        assert isinstance(msg, str)
        assert status in ["ok", "fail"]
    
    @pytest.mark.parametrize("channel_class", [
        ShopeeChannel,
        TikTokShopChannel,
        WeChatChannel,
    ])
    def test_extract_returns_extraction_result(self, channel_class):
        """Test that extract() returns ExtractionResult."""
        channel = channel_class()
        result = channel.extract("https://invalid.url")
        
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert hasattr(result, "error")
        assert hasattr(result, "backend_used")
        assert hasattr(result, "item_count")
        assert isinstance(result.success, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
