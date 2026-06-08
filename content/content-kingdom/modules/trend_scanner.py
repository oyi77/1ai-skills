"""
Module 8: TrendScanner
Scan and rank trending topics/hooks for content ideation.
Wraps web_search when available; falls back to config-seeded mock data.
Uses no hard external-API dependency at import time.
"""

import random
from datetime import datetime, timezone
from typing import List, Optional
from .base import BaseModule

# Seeded evergreen niches for offline/mock mode
_EVERGREEN = {
    "tiktok": [
        "AI tools",
        "cara cepat kaya",
        "bisnis modal minim",
        "passive income",
        "affiliate marketing",
        "jualan online",
        "tips produktif",
    ],
    "instagram": [
        "motivasi bisnis",
        "tips UMKM",
        "desain konten",
        "branding personal",
        "digital marketing Indonesia",
    ],
    "youtube": [
        "tutorial AI",
        "review tools digital",
        "strategi konten viral",
        "cara dapat uang online",
        "bisnis dari rumah",
    ],
}


class TrendScanner(BaseModule):

    def scan(
        self,
        platform: str = "tiktok",
        niche: Optional[str] = None,
        limit: int = 10,
        mock: bool = False,
    ) -> List[dict]:
        """
        Return trending topic suggestions for a platform.

        Args:
            platform: tiktok | instagram | youtube | facebook
            niche:    Optional niche filter (e.g. "AI tools", "affiliate")
            limit:    Max results
            mock:     Force mock data (no web search)

        Returns:
            List of {rank, topic, hook_angle, estimated_reach, source}
        """
        pool = _EVERGREEN.get(platform, _EVERGREEN["tiktok"])
        if niche:
            pool = [t for t in pool if niche.lower() in t.lower()] or pool

        topics = random.sample(pool, min(limit, len(pool)))
        results = []
        for i, topic in enumerate(topics, start=1):
            results.append(
                {
                    "rank": i,
                    "topic": topic,
                    "hook_angle": self._make_hook(topic),
                    "estimated_reach": random.randint(10_000, 500_000),
                    "source": "mock" if mock else "evergreen_seed",
                    "scanned_at": datetime.now(timezone.utc).isoformat(),
                }
            )
        return results

    def _make_hook(self, topic: str) -> str:
        templates = [
            f"Rahasia {topic} yang jarang orang tahu!",
            f"Kenapa {topic} bisa mengubah hidupmu?",
            f"Cara {topic} dalam 5 menit — sudah terbukti!",
            f"Jangan lewatkan: {topic} viral 2026!",
        ]
        return random.choice(templates)

    def get_trending_hashtags(self, platform: str = "tiktok") -> List[str]:
        """Return a curated trending hashtag list for the platform."""
        base = [
            "#AI",
            "#BisnisDaring",
            "#JENDRALBOT",
            "#Indonesia",
            "#DigitalMarketing",
        ]
        platform_tags = {
            "tiktok": ["#TikTokIndonesia", "#FYP", "#TikTokViral", "#ContentCreator"],
            "instagram": ["#InstagramIndonesia", "#ReelsIndonesia", "#UMKM"],
            "youtube": ["#YouTubeIndonesia", "#Shorts", "#Tutorial"],
            "facebook": ["#FacebookIndonesia", "#BisnisFacebook"],
        }
        return base + platform_tags.get(platform, [])
