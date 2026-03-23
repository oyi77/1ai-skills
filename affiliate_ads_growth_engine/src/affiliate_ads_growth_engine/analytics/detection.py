from typing import List
from .metrics import PerformanceMetrics

class DetectionEngine:
 def __init__(self, thresholds: dict):
 self.thresholds = thresholds

 def is_winner(self, metrics: PerformanceMetrics):
 return metrics.roas() >= self.thresholds.get("winning_roas",2.0) and metrics.cpa() <= self.thresholds.get("max_cpa",50000)

 def is_loser(self, metrics: PerformanceMetrics):
 return metrics.roas() <= self.thresholds.get("losing_roas",0.8) or metrics.ctr() <= self.thresholds.get("min_ctr",0.01)

 def classify(self, metrics: PerformanceMetrics):
 if self.is_winner(metrics):
 return "winner"
 if self.is_loser(metrics):
 return "loser"
 return "neutral"
