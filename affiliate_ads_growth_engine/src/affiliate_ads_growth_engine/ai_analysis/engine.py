from dataclasses import dataclass
from typing import List

@dataclass
class AdRecord:
    campaign: str
    adset: str
    ad: str
    spend: float
    ctr: float
    roas: float
    conversions: int
    creative: str
    audience: str
    hook: str

class AIAnalysisEngine:
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {"roas": 3, "ctr": 0.02, "conversion_rate": 0.02}

    def classify(self, ad: AdRecord):
        if ad.roas >= self.thresholds["roas"] and ad.ctr >= self.thresholds["ctr"] and ad.conversions >= 1:
            return "winner"
        if ad.spend > 0 and ad.conversions == 0:
            return "loser"
        if ad.roas < 1:
            return "loser"
        return "neutral"

    def analyze(self, ads: List[AdRecord]):
        winners = []
        losers = []
        for ad in ads:
            result = self.classify(ad)
            if result == "winner":
                winners.append(ad)
            elif result == "loser":
                losers.append(ad)
        return winners, losers

    def summarize_winners(self, winners: List[AdRecord]):
        return [
            {
                "campaign": ad.campaign,
                "adset": ad.adset,
                "creative": ad.creative,
                "roas": ad.roas,
                "orders": ad.conversions,
                "hook": ad.hook,
                "audience": ad.audience
            }
            for ad in winners
        ]

    def summarize_losers(self, losers: List[AdRecord]):
        return [
            {
                "campaign": ad.campaign,
                "spend": ad.spend,
                "orders": ad.conversions
            }
            for ad in losers
        ]
