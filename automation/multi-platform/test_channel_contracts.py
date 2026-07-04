# -*- coding: utf-8 -*-
"""
Test fixtures and contracts for Agent-Reach channel integration.

Each channel MUST pass these contracts before shipping.
"""

import pytest
from typing import Dict, Any
from datetime import datetime
from base import Channel, ExtractionResult


# ============================================================================
# CONTRACT TESTS (every channel must pass)
# ============================================================================

class TestChannelContract:
    """Universal contract every channel must satisfy."""
    
    def test_channel_has_required_attributes(self, channel: Channel):
        """Channel must define name, description, backends, tier."""
        assert channel.name is not None, f"{channel.__class__.__name__}.name not set"
        assert channel.description is not None, f"{channel.__class__.__name__}.description not set"
        assert isinstance(channel.backends, list), f"{channel.__class__.__name__}.backends must be list"
        assert isinstance(channel.tier, int), f"{channel.__class__.__name__}.tier must be int (0-2)"
        assert 0 <= channel.tier <= 2, f"{channel.__class__.__name__}.tier must be 0-2"
    
    def test_can_handle_returns_bool(self, channel: Channel):
        """can_handle() must return bool."""
        result = channel.can_handle("https://example.com")
        assert isinstance(result, bool), f"{channel.__class__.__name__}.can_handle() returned {type(result)}, not bool"
    
    def test_check_returns_tuple(self, channel: Channel):
        """check() must return (status: str, message: str)."""
        status, message = channel.check()
        assert isinstance(status, str), f"status={type(status)}, expected str"
        assert isinstance(message, str), f"message={type(message)}, expected str"
        assert status in ["ok", "warn", "off", "error"], f"status='{status}' not in allowed values"
    
    def test_extract_returns_result_or_none(self, channel: Channel):
        """extract() must return ExtractionResult or None."""
        result = channel.extract("https://example.com/nonexistent")
        assert result is None or isinstance(result, ExtractionResult), \
            f"extract() returned {type(result)}, expected ExtractionResult or None"
    
    def test_extraction_result_has_platform(self, channel: Channel):
        """ExtractionResult.platform must match channel.name."""
        result = ExtractionResult(
            platform=channel.name,
            url="https://example.com",
            title="Test"
        )
        assert result.platform == channel.name, \
            f"result.platform='{result.platform}', expected '{channel.name}'"
    
    def test_extraction_result_serializable(self):
        """ExtractionResult must be JSON-serializable."""
        result = ExtractionResult(
            platform="test",
            url="https://example.com",
            title="Test Title",
            engagement={"likes": 100},
            data={"custom": "value"}
        )
        json_str = result.to_json()
        assert json_str is not None
        assert "test" in json_str
        assert "Test Title" in json_str


# ============================================================================
# PLATFORM-SPECIFIC FIXTURES
# ============================================================================

@pytest.fixture
def shopee_test_urls() -> Dict[str, str]:
    """Valid Shopee URLs for testing."""
    return {
        "product_id": "https://shopee.co.id/product/123456789/",
        "with_shop": "https://shopee.co.id/shop/official-apple-store/product/123456789/",
        "my_region": "https://shopee.com.my/product/987654321/",
        "ph_region": "https://shopee.com.ph/product/111111111/",
        "invalid": "https://example.com/not-shopee",
    }


@pytest.fixture
def tiktok_shop_test_urls() -> Dict[str, str]:
    """Valid TikTok Shop URLs for testing."""
    return {
        "product": "https://www.tiktok.com/products/123456789",
        "shop": "https://www.tiktok.com/@seller_name/shop",
        "video_with_shop": "https://www.tiktok.com/@seller/video/987654321",
        "invalid": "https://example.com",
    }


@pytest.fixture
def wechat_test_urls() -> Dict[str, str]:
    """Valid WeChat URLs for testing."""
    return {
        "article": "https://mp.weixin.qq.com/s/abc123def456ghi789",
        "official": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=Mz123",
        "invalid": "https://example.com",
    }


@pytest.fixture
def youtube_test_urls() -> Dict[str, str]:
    """Valid YouTube URLs for testing."""
    return {
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "short": "https://youtu.be/dQw4w9WgXcQ",
        "channel": "https://www.youtube.com/c/ChannelName",
        "invalid": "https://example.com",
    }


@pytest.fixture
def reddit_test_urls() -> Dict[str, str]:
    """Valid Reddit URLs for testing."""
    return {
        "post": "https://www.reddit.com/r/python/comments/abc123/",
        "comment": "https://www.reddit.com/r/python/comments/abc123/_/xyz789",
        "subreddit": "https://www.reddit.com/r/python/",
        "invalid": "https://example.com",
    }


# ============================================================================
# REAL-DATA VALIDATION TEMPLATE
# ============================================================================

class RealDataValidation:
    """
    Template for validating real data extraction.
    
    Before marking channel DONE, subclass this and implement validate_*() methods.
    """
    
    @pytest.fixture
    def real_test_urls(self) -> Dict[str, str]:
        """MUST override: return dict of real URLs to test against."""
        raise NotImplementedError("Implement real_test_urls() in subclass")
    
    def test_real_extraction_returns_data(self, channel: Channel, real_test_urls: Dict[str, str]):
        """Extract from real URL and verify output structure."""
        for key, url in real_test_urls.items():
            if key == "invalid":
                continue  # skip invalid URLs
            
            result = channel.extract(url)
            assert result is not None, f"extract('{url}') returned None"
            assert isinstance(result, ExtractionResult), f"expected ExtractionResult, got {type(result)}"
            assert result.error is None or result.error == "", f"extraction error: {result.error}"
            assert result.platform == channel.name, f"platform mismatch"
            assert result.url is not None, f"result.url is None"
    
    def test_invalid_url_returns_error(self, channel: Channel, real_test_urls: Dict[str, str]):
        """Invalid URL should return error or None."""
        if "invalid" not in real_test_urls:
            pytest.skip("no invalid URL in test fixture")
        
        url = real_test_urls["invalid"]
        result = channel.extract(url)
        
        if result is not None:
            assert not channel.can_handle(url), f"can_handle() should be False for invalid URL"


# ============================================================================
# EXAMPLE: Shopee Channel Real Data Test
# ============================================================================

class TestShopeeRealData(RealDataValidation):
    """
    Real-world validation for Shopee channel.
    
    BEFORE RUNNING:
      export SHOPEE_API_KEY=your_key
      or ensure shopee-cli is installed and authenticated
    """
    
    @pytest.fixture
    def real_test_urls(self) -> Dict[str, str]:
        return {
            # Real Shopee product URL (Indonesia)
            "product_id": "https://shopee.co.id/product/123456789/",
            # Can add more real URLs here
            "invalid": "https://shopee.co.id/not-a-product",
        }
    
    def test_shopee_extraction_has_required_fields(self, channel: Channel):
        """Shopee extraction must have product-specific fields."""
        if channel.name != "shopee":
            pytest.skip("not a Shopee channel")
        
        # This will be implemented when Shopee channel is ported
        # result = channel.extract("https://shopee.co.id/product/...")
        # assert result.data.get("product_id") is not None
        # assert result.data.get("price") is not None
        # assert result.data.get("seller") is not None
        pass


# ============================================================================
# INTEGRATION TEST HARNESS
# ============================================================================

def test_all_channels_registered():
    """Verify all channels can be instantiated and checked."""
    from channels import (
        ShopeeChannel, TikTokShopChannel, WeChatChannel,
        YouTubeChannel, RedditChannel,
        # add more imports as channels are ported
    )
    
    channels = [
        ShopeeChannel(),
        TikTokShopChannel(),
        WeChatChannel(),
        YouTubeChannel(),
        RedditChannel(),
    ]
    
    for channel in channels:
        status, message = channel.check()
        print(f"{channel.name:20} | {status:10} | {message}")
        assert status in ["ok", "warn", "off", "error"], f"unexpected status: {status}"


def test_channel_routing():
    """Test that can_handle() correctly routes URLs to channels."""
    from channels import CHANNELS_BY_PLATFORM
    
    test_cases = [
        ("https://shopee.co.id/product/123", "shopee"),
        ("https://www.tiktok.com/video/456", "tiktok"),
        ("https://youtu.be/abc123", "youtube"),
        ("https://reddit.com/r/python", "reddit"),
    ]
    
    for url, expected_channel in test_cases:
        for channel in CHANNELS_BY_PLATFORM.values():
            if channel.can_handle(url):
                assert channel.name == expected_channel, \
                    f"URL {url} routed to {channel.name}, expected {expected_channel}"
                break
        else:
            pytest.fail(f"No channel found for {url}")
