from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
 spend: float
 revenue: float
 clicks: int
 impressions: int
 conversions: int
 commission: float =0.0

 def roas(self):
 return (self.revenue / self.spend) if self.spend else0.0

 def cpa(self):
 return (self.spend / self.conversions) if self.conversions else0.0

 def cpl(self):
 return (self.spend / self.clicks) if self.clicks else0.0

 def ctr(self):
 return (self.clicks / self.impressions) if self.impressions else0.0
