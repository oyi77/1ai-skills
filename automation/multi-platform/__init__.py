# -*- coding: utf-8 -*-
"""
1ai-Ecosystem Multi-Platform Channel Extraction

Unified data extraction across 19+ platforms:
- E-commerce: Shopee, TikTok Shop, Amazon, eBay
- Messaging: WeChat, Telegram, Discord
- Social: Twitter/X, Reddit, TikTok, Instagram
- Aggregators: Google Shopping, Alibaba, AliExpress

Ported from: https://github.com/Panniantong/Agent-Reach
License: MIT (original repo), adapted for 1ai-ecosystem
"""

from .base import Channel, ChannelResult, ExtractionResult
from .shopee import ShopeeChannel
from .tiktok_shop import TikTokShopChannel
from .wechat import WeChatChannel

__all__ = [
    "Channel",
    "ChannelResult",
    "ExtractionResult",
    "ShopeeChannel",
    "TikTokShopChannel",
    "WeChatChannel",
]

__version__ = "1.0.0"
